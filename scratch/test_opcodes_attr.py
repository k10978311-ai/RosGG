with open(OUT, 'w') as f:
    def dummy():
        global x
        a = x.y
        x.z = 1
    co = dummy.func_code
    code = bytearray(co.co_code)
    for i, b in enumerate(code):
        f.write('%d: %d\n' % (i, b))
