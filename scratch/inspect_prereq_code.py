import sys, dis
f = open(OUT, "w")
try:
    import ClientEntity, BigWorld, Globals
    fn = ClientEntity.ClientEntity.prerequisites
    co = fn.im_func.func_code
    f.write("co_varnames: %r\n" % (co.co_varnames,))
    f.write("co_names: %r\n" % (co.co_names,))
    f.write("co_consts: %r\n" % (co.co_consts,))
    
    # Let's inspect the code bytes
    bc = bytearray(co.co_code)
    i = 0
    while i < len(bc):
        op = bc[i]
        opname = dis.opname[op]
        if op >= dis.HAVE_ARGUMENT:
            arg = bc[i+1] | (bc[i+2] << 8)
            val = ""
            if op in dis.hasname:
                val = "name=" + co.co_names[arg]
            elif op in dis.hasconst:
                val = "const=" + repr(co.co_consts[arg])
            elif op in dis.haslocal:
                val = "local=" + co.co_varnames[arg]
            f.write("%4d: %-20s %5d %s\n" % (i, opname, arg, val))
            i += 3
        else:
            f.write("%4d: %-20s\n" % (i, opname))
            i += 1
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
