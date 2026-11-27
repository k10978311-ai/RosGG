import sys, dis, StringIO, types
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.__dict__.get("onBecomePlayer")
    def inner(fn):
        for cell in (getattr(fn, "func_closure", None) or ()):
            try: v = cell.cell_contents
            except ValueError: continue
            if isinstance(v, types.FunctionType): return inner(v)
        return fn
    real_fn = inner(fn)
    co = real_fn.func_code
    code = co.co_code
    i = 0
    n = len(code)
    while i < n:
        offset = i
        op = ord(code[i])
        i += 1
        opname = dis.opname[op]
        argval = ""
        arg = None
        if op >= dis.HAVE_ARGUMENT:
            arg = ord(code[i]) | (ord(code[i+1]) << 8)
            i += 2
            if op in dis.hasname:
                argval = co.co_names[arg]
            elif op in dis.hasconst:
                argval = repr(co.co_consts[arg])
            elif op in dis.haslocal:
                argval = co.co_varnames[arg]
            elif op in dis.hasjabs:
                argval = "to %d" % arg
            elif op in dis.hasjrel:
                argval = "to %d" % (i + arg)
            else:
                argval = str(arg)
        f.write("%4d %-20s %5s %s\n" % (offset, opname, str(arg) if arg is not None else "", argval))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
