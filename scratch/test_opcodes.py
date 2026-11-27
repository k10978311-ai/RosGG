f = open(OUT, "w")
try:
    import dis
    # Let's inspect a simple known function:
    def test_fn(x):
        if x:
            return 1
        return 0
    co = test_fn.func_code
    bc = bytearray(co.co_code)
    for i, b in enumerate(bc):
        f.write("%d: %d\n" % (i, b))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
