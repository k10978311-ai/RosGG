with open(OUT, 'w') as f:
    def test_op(arg):
        g = len(arg)
        return g
    co = test_op.func_code
    f.write('consts: ' + repr(co.co_consts) + '\n')
    f.write('names: ' + repr(co.co_names) + '\n')
    f.write('varnames: ' + repr(co.co_varnames) + '\n')
    for i, b in enumerate(bytearray(co.co_code)):
        f.write('%d: %d\n' % (i, b))
