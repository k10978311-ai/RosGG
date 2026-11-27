with open(OUT, 'w') as f:
    try:
        import ClientEntity
        pfn = ClientEntity.ClientEntity.prerequisites
        co = pfn.im_func.func_code if hasattr(pfn, 'im_func') else pfn.func_code
        code = bytearray(co.co_code)
        names = co.co_names
        consts = co.co_consts
        varnames = co.co_varnames
        
        i, n = 0, len(code)
        while i < n:
            offset = i
            op = code[i]
            i += 1
            arg_str = ''
            if op >= 90:
                arg = code[i] | (code[i+1] << 8)
                i += 2
                arg_str = str(arg)
                if arg < len(names): arg_str += ' (n: ' + str(names[arg]) + ')'
                if arg < len(consts): arg_str += ' (c: ' + repr(consts[arg]) + ')'
                if arg < len(varnames): arg_str += ' (v: ' + str(varnames[arg]) + ')'
            f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
