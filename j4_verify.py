import pathlib,subprocess,os,json,sys,xml.etree.ElementTree as ET
P=pathlib.Path;E=P('Evidence');E.mkdir(exist_ok=True)
c=json.loads(P('j4_config.json').read_text());os.environ['DJANGO_SETTINGS_MODULE']=c['settings'];os.environ['PYTHONPATH']=str(P.cwd())+':'+str(P('src').resolve())
m=int(os.environ.get('J4_MUTATION','-1'))
if m>=0:
 mutation=json.loads(P('j4_mutations.json').read_text())[m]
 f=P(mutation['file']);s=f.read_text();assert s.count(mutation['old'])==1,(f,'nonunique mutation');f.write_text(s.replace(mutation['old'],mutation['new']))
with (E/'tests.log').open('w') as log:
 r=subprocess.run([sys.executable,'-m','pytest',c['tests'],'--junitxml=Evidence/tests.xml','-q'],stdout=log,stderr=subprocess.STDOUT,timeout=540)
print((E/'tests.log').read_text()[-9000:])
assert (E/'tests.xml').exists(),'test infrastructure did not produce XML'
root=ET.parse(E/'tests.xml').getroot();cases=list(root.iter('testcase'));assert cases,'no tests collected'
errors=list(root.iter('error'));assert not errors,'test infrastructure/errors must not score detection'
inventory=sorted(x.attrib.get('classname','')+'::'+x.attrib['name'] for x in cases)
skips=sorted(x.attrib.get('classname','')+'::'+x.attrib['name'] for x in cases if x.find('skipped') is not None)
(E/'inventory.json').write_text(json.dumps({'tests':inventory,'skips':skips},indent=2))
if m<0 and P('j4-inventory.json').exists():assert json.loads(P('j4-inventory.json').read_text())=={'tests':inventory,'skips':skips},'test inventory changed'
project_detected=r.returncode!=0
if m<0:assert not project_detected,'project tests failed'
h=subprocess.run([sys.executable,'j4_http.py'],timeout=120)
assert (E/'surface.json').exists(),'boot/probe infrastructure failed'
model=subprocess.run([sys.executable,'j4_models.py'],timeout=30)
assert (E/'models.json').exists(),'model infrastructure failed'
harness_detected=h.returncode!=0 or model.returncode!=0
result=dict(mutation=m,tests=len(cases),skipped=len(skips),project_detected=project_detected,harness_detected=harness_detected,combined=project_detected or harness_detected)
(E/'result.json').write_text(json.dumps(result,indent=2));print(result)
if m<0:assert not harness_detected,'HTTP characterization drift'
