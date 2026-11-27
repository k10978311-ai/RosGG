import sys
f = open(OUT, "w")
try:
    import ClientEntity
    co = ClientEntity.ClientEntity.prerequisites.im_func.func_code
    code = co.co_code
    for off in range(80, 110):
        f.write("%d: %d\n" % (off, ord(code[off])))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
