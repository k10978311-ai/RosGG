import sys, dis
f = open(OUT, "w")
try:
    import Avatar
    fn = Avatar.Avatar.enterWorld
    co = fn.im_func.func_code
    f.write("Avatar.enterWorld names: %r\n" % (co.co_names,))
    f.write("Avatar.enterWorld consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
    code = co.co_code
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
