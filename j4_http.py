import os,pathlib,json,sys,subprocess,time,urllib.request,urllib.error,re,hashlib,signal
P=pathlib.Path;c=json.loads(P('j4_config.json').read_text());E=P('Evidence')
# Boot uses test project's URLConf and a disposable on-disk SQLite database.
P('j4_boot_settings.py').write_text('from '+c['settings']+' import *\nDEBUG=False\nALLOWED_HOSTS=["127.0.0.1","localhost","testserver"]\nDATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":"j4.sqlite3"}}\nEMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"\n')
env=os.environ.copy();env['DJANGO_SETTINGS_MODULE']='j4_boot_settings'
with (E/'migrate.log').open('w') as log:subprocess.run([sys.executable,'-m','django','migrate','--noinput'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
opener=urllib.request.build_opener(NoRedirect)
with (E/'boot.log').open('w') as log:
 server=subprocess.Popen([sys.executable,'-m','django','runserver','127.0.0.1:3000','--noreload'],env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 try:
  rows=[]
  for route in c['routes']:
   for attempt in range(40):
    try:
     try:resp=opener.open('http://127.0.0.1:3000'+route,timeout=3)
     except urllib.error.HTTPError as exc:resp=exc
     break
    except urllib.error.URLError:time.sleep(.5)
   else:raise RuntimeError('server did not boot')
   raw=resp.read().decode();assert resp.code<500,('HTTP 5xx infrastructure/runtime error',route)
   raw=re.sub(r'(name="csrfmiddlewaretoken" value=")[^"]+',r'\1NORMALIZED',raw)
   if c['name']=='wiki' and route=='/_accounts/sign-up/':
    # Exact random honeypot class and JS function, generated in UserCreationForm.
    tokens=re.findall(r'function (f[A-Z0-9]{10})\(\)|class="([A-Z0-9]{10})"',raw)
    for pair in tokens:
     for token in pair:
      if token:raw=raw.replace(token,'HONEYPOT_NORMALIZED')
   (E/('body-'+str(len(rows))+'.html')).write_text(raw)
   rows.append(dict(route=route,status=resp.code,content_type=resp.headers.get('Content-Type'),location=resp.headers.get('Location'),body_sha256=hashlib.sha256(raw.encode()).hexdigest()))
  (E/'surface.json').write_text(json.dumps(rows,indent=2))
  if P('surface.json').exists():assert rows==json.loads(P('surface.json').read_text()),'HTTP drift'
 finally:
  os.killpg(server.pid,signal.SIGTERM);server.wait(timeout=15)
