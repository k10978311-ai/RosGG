with open(OUT, 'w') as f:
    import opcode
    for k, v in sorted(opcode.opmap.items(), key=lambda x: x[1]):
        f.write('%s: %d\n' % (k, v))
