"""Fixed, side-effect-free model fixtures; no wall-clock-dependent output."""
import os,json,pathlib,datetime
import django
django.setup()
c=json.loads(pathlib.Path('j4_config.json').read_text())
if c['name']=='todo':
 from todo.models import Task,TaskList,Attachment
 t=Task(id=7,title='J4 fixture',due_date=datetime.date(2000,1,1))
 a=Attachment(file='fixtures/report.txt')
 data={'completed':t.completed,'title':str(t),'url':t.get_absolute_url(),'overdue':t.overdue_status(),'extension':a.extension(),'list':str(TaskList(name='J4 list'))}
elif c['name']=='helpdesk':
 from helpdesk.models import Ticket,Queue
 q=Queue(id=1,slug='support',title='Support');t=Ticket(id=7,title='J4 fixture',queue=q,priority=1,status=1)
 data={'title':str(t),'ticket':t.ticket_for_url,'assigned':str(t.get_assigned_to),'priority':t.get_priority_css_class,'status_badge':t.get_status_badge_class,'url':str(t.get_absolute_url())}
else:
 from django.contrib.auth.models import AnonymousUser
 from wiki.models import Article
 from wiki.core import permissions
 a=Article();u=AnonymousUser()
 data={name:getattr(permissions,name)(a,u) for name in ['can_assign','can_assign_owner','can_change_permissions','can_delete','can_moderate','can_admin']}
p=pathlib.Path('Evidence/models.json');p.write_text(json.dumps(data,indent=2));print(data)
f=pathlib.Path('models.json')
if f.exists():assert data==json.loads(f.read_text()),'model characterization drift'
