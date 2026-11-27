with open(OUT, 'w') as f:
    def f1():
        return None
    for b in bytearray(f1.func_code.co_code):
        f.write(str(b) + ' ')
    f.write('\n')
