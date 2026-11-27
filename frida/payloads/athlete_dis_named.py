# READ-ONLY: disassemble PlayerAthlete.onBecomePlayer; resolve name/const indices ourselves
# (NeoX remaps opcodes, so dis prints wrong mnemonics but the arguments are still indices).
import types
f = open(OUT, 'w')
import Athlete
fn = Athlete.PlayerAthlete.__dict__['onBecomePlayer']
for cell in (fn.func_closure or ()):
    try:
        v = cell.cell_contents
        if isinstance(v, types.FunctionType): fn = v
    except ValueError: pass
co = fn.func_code
f.write('names=%r\n' % (list(co.co_names),))
f.write('consts=%r\n' % ([c if not isinstance(c, types.CodeType) else '<code %s>' % c.co_name for c in co.co_consts],))
code = co.co_code; i = 0
lnotab = {}
while i < len(code):
    op = ord(code[i])
    if op >= 90:
        arg = ord(code[i+1]) | (ord(code[i+2]) << 8)
        ref = ''
        if op in (155, 160, 176, 106, 109, 108, 116, 101, 90, 95): ref = co.co_names[arg] if arg < len(co.co_names) else ''
        f.write('%4d op%-3d %5d %s\n' % (i, op, arg, ref)); i += 3
    else:
        f.write('%4d op%-3d\n' % (i, op)); i += 1
f.close()
