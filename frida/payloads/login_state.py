# READ-ONLY: did onChannelLogin/onLogin run? Inspect Globals/Checkpoints/UI state.
import sys
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import BigWorld
w('player=%r' % (BigWorld.player(),))
G = None
for mname in ('Globals', 'helpers.Globals', 'common.Globals'):
    if mname in sys.modules:
        G = sys.modules[mname]; w('Globals module=%s' % mname); break
if G is None:
    for mname, mod in sys.modules.items():
        if mod is not None and hasattr(mod, 'serverSauthInfo'):
            G = mod; w('Globals-like module=%s' % mname); break
if G is not None:
    for k in ('serverSauthInfo', 'playerUID', 'isPCServer', 'channelInfo', 'loginResReady', 'useQuickLogin'):
        try: w('  Globals.%s=%r' % (k, getattr(G, k)))
        except Exception as e: w('  Globals.%s ERR %r' % (k, e))
    um = getattr(G, 'uiMgr', None)
    if um is not None:
        for attr in ('_uiStack', 'uiStack', '_ui_dict', 'ui_dict', '_uis', 'uis', 'cur_ui', '_cur_ui'):
            if hasattr(um, attr):
                v = getattr(um, attr)
                try: v = list(v.keys()) if hasattr(v, 'keys') else v
                except Exception: pass
                w('  uiMgr.%s=%r' % (attr, v if not isinstance(v, list) else v[:40]))
        w('  uiMgr attrs=%s' % [a for a in dir(um) if not a.startswith('__')][:80])
for mname in ('Checkpoints', 'helpers.Checkpoints'):
    m = sys.modules.get(mname)
    if m is not None:
        for k in dir(m):
            if 'check' in k.lower() or 'point' in k.lower():
                v = getattr(m, k)
                if isinstance(v, (list, dict, tuple)): w('%s.%s=%r' % (mname, k, v if len(repr(v)) < 2000 else repr(v)[-2000:]))
f.close()
