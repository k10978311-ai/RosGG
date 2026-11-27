OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    fn = p.doRealnameAuthenAgain
    co = fn.im_func.func_code
    f.write("doRealnameAuthenAgain names: %r\n" % (co.co_names,))
    f.write("doRealnameAuthenAgain consts: %r\n" % (co.co_consts,))
    f.write("doRealnameAuthenAgain varnames: %r\n" % (co.co_varnames,))

    # Disassemble
    code = bytearray(co.co_code)
    i = 0
    n = len(code)
    while i < n:
        offset = i
        op = code[i]
        i += 1
        arg_val = ""
        if op >= 90:
            arg = code[i] | (code[i+1] << 8)
            i += 2
            arg_val = str(arg)
            if op in (101, 116, 96, 155, 156):
                if arg < len(co.co_names): arg_val += " (name: %s)" % co.co_names[arg]
            elif op == 100:
                if arg < len(co.co_consts): arg_val += " (const: %r)" % (co.co_consts[arg],)
        f.write("%4d: op=%d %s\n" % (offset, op, arg_val))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
