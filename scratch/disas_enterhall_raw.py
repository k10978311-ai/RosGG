import sys, types
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.__dict__.get("enterHall")
    def inner(fn):
        for cell in (getattr(fn, "func_closure", None) or ()):
            try: v = cell.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): return inner(v)
        return fn
    real_fn = inner(fn)
    co = real_fn.func_code
    code = co.co_code
    f.write("code length: %d\n" % len(code))
    i = 0
    while i < len(code):
        op = ord(code[i])
        if op >= 90:
            arg = ord(code[i+1]) | (ord(code[i+2]) << 8)
            f.write("%4d: op=%d arg=%d\n" % (i, op, arg))
            i += 3
        else:
            f.write("%4d: op=%d\n" % (i, op))
            i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
