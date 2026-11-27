# READ-ONLY: disassemble the real PlayerAthlete.onBecomePlayer body (unwrapping the decorator).
import sys, dis, StringIO, types
f = open(OUT, 'w')
import Athlete
fn = Athlete.PlayerAthlete.__dict__['onBecomePlayer']
def inner(fn):
    for cell in (fn.func_closure or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): return v
    return fn
g = inner(fn)
buf = StringIO.StringIO(); old = sys.stdout; sys.stdout = buf
try: dis.dis(g)
finally: sys.stdout = old
f.write(buf.getvalue())
f.close()
