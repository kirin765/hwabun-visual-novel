"""Native X11 input + responsiveness watchdog; no Ren'Py test-mode acceleration."""
import os,json,time,subprocess,signal
from pathlib import Path
from Xlib import display,X,XK,protocol
ROOT=Path(__file__).resolve().parents[1]
log=ROOT/'docs/freeze-diagnosis/native-stacks.log'
Path(str(log)+'.heartbeat').unlink(missing_ok=True)
env=os.environ.copy();env['DISPLAY']=':0';env['HWABUN_FREEZE_PROBE']=str(log)
p=subprocess.Popen([os.environ.get('HWABUN_LAUNCHER',str(ROOT/'play.sh')),'--savedir','/tmp/hwabun-native-repro'],env=env,stdout=open(str(log)+'.output','w'),stderr=subprocess.STDOUT)
D=display.Display(':0');root=D.screen().root;pidatom=D.intern_atom('_NET_WM_PID');w=None
try:
 deadline=time.time()+8
 while time.time()<deadline and w is None:
  for c in root.query_tree().children:
   value=c.get_full_property(pidatom,X.AnyPropertyType)
   if value is not None and value.value[0]==p.pid:w=c;break
  time.sleep(.1)
 assert w is not None,'No game window'
 env['HYPRLAND_INSTANCE_SIGNATURE']=next(Path('/run/user/1000/hypr').iterdir()).name
 subprocess.run(['hyprctl','dispatch',f'hl.dsp.focus({{window="pid:{p.pid}"}})'],env=env,stdout=subprocess.DEVNULL)
 time.sleep(.5)
 def key(name):
  code=D.keysym_to_keycode(XK.string_to_keysym(name))
  args=dict(time=X.CurrentTime,root=root,window=w,same_screen=1,child=X.NONE,root_x=0,root_y=0,event_x=10,event_y=10,state=0,detail=code)
  for kind,mask in [(protocol.event.KeyPress,X.KeyPressMask),(protocol.event.KeyRelease,X.KeyReleaseMask)]:w.send_event(kind(**args),event_mask=mask)
  D.sync()
 hb=Path(str(log)+'.heartbeat');records=[]
 for i in range(int(os.environ.get('HWABUN_PROBE_STEPS', '150'))):
  assert p.poll() is None, f'Game exited: {p.returncode}; see {log}.output'
  if i == 40:
   g=w.get_geometry()
   scale=min(g.width/1920,g.height/1080)
   args=dict(time=X.CurrentTime,root=root,window=w,same_screen=1,child=X.NONE,root_x=0,root_y=0,event_x=int((g.width-1920*scale)/2+200*scale),event_y=int((g.height-1080*scale)/2+490*scale),state=0,detail=1)
   motion=dict(args);motion['detail']=0
   w.send_event(protocol.event.MotionNotify(**motion),event_mask=X.PointerMotionMask)
   D.sync();time.sleep(.1)
   for kind,mask in [(protocol.event.ButtonPress,X.ButtonPressMask),(protocol.event.ButtonRelease,X.ButtonReleaseMask)]:w.send_event(kind(**args),event_mask=mask)
   D.sync()
  if i in (60,65,70,120,125,130) or (i > 150 and i % 10 == 0):key('Return')
  if i in (80,100):key('f')
  if i in (85,110):key('Escape')
  time.sleep(.2)
  if hb.exists():
   try:state=json.loads(hb.read_text())
   except ValueError:continue
   state['age']=round(time.time()-state['time'],3) if state['drawing'] else state['duration'];records.append(state)
  else:records.append({'age':round((i+1)*.2,2)})
 (ROOT/'docs/freeze-diagnosis/native-heartbeats.json').write_text(json.dumps(records,indent=2))
 worst=max(max(r['age'], r.get('max_draw_seconds',0)) for r in records)
 print('max event-loop stall:',worst,'seconds; final state:',records[-1])
 assert any(r.get('game_menu') for r in records), 'Native Esc did not open game menu'
 assert any(r.get('fullscreen') for r in records), 'Fullscreen toggle did not take effect'
 assert max(r.get('music_position') or 0 for r in records)>10, 'Music clock did not progress'
 assert worst < 2,'FREEZE: game event loop stopped processing input for >2 seconds'
 assert max(r.get('block',0) for r in records)>min(r.get('block',0) for r in records),'INPUT FAILURE: dialogue did not advance; check focus/coordinates before diagnosing a freeze'
 runtime_log = (Path(env['HWABUN_LAUNCHER']).parent if env.get('HWABUN_LAUNCHER') else ROOT/'sample')/'log.txt'
 swap_lines = [line for line in runtime_log.read_text().splitlines() if 'swap interval:' in line]
 print('Renderer:', swap_lines)
 expected_vsync = env.get('RENPY_GL_VSYNC', '0')
 assert swap_lines and all(line == f'swap interval: {expected_vsync} frames' for line in swap_lines), 'Unexpected native VSync setting'
 print('PASS: native keyboard advances and the event loop stays responsive')
finally:
 p.terminate()
 try:p.wait(timeout=3)
 except subprocess.TimeoutExpired:p.kill();p.wait()
