with open(OUT, 'w') as f:
    def test1():
        if True:
            return 1
        return 2
    for b in bytearray(test1.func_code.co_code):
        f.write(str(b) + ' ')
    f.write('\n')
