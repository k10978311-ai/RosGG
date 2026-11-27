# READ-ONLY: valid characterType ids for legacyProperties.getCharactersData
import sys, BigWorld
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
lp = sys.modules['player.appearance.PlayerFPAppear'].legacyProperties
w('module %r' % lp)
p = BigWorld.player()
w('player %s characterType=%r' % (type(p).__name__, getattr(p, 'characterType', '<missing>')))
fn = lp.getCharactersData
w('getCharactersData co_names=%s consts=%r' % (list(fn.func_code.co_names), fn.func_code.co_consts[:10]))
for k in list(range(0, 12)) + [100, 101, 1001, 10001, 20001]:
    try: d = fn(k)
    except Exception as e: d = 'EXC %r' % e
    if d: w('%d -> %r' % (k, str(d)[:200]))
f.close()
