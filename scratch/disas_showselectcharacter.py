f = open(OUT, "w")
try:
    try:
        import entities.Athlete as Athlete
    except:
        import Athlete
    fn = Athlete.PlayerAthlete.showSelectCharacter
    if hasattr(fn, 'im_func'):
        fn = fn.im_func
    # unwrap closure if any
    while hasattr(fn, 'func_closure') and fn.func_closure:
        found = False
        for c in fn.func_closure:
            if hasattr(c.cell_contents, 'func_code'):
                fn = c.cell_contents
                found = True
                break
        if not found:
            break
            
    code = fn.func_code if hasattr(fn, 'func_code') else fn
    f.write("showSelectCharacter names: %r\n" % (code.co_names,))
    f.write("showSelectCharacter consts: %r\n" % (code.co_consts,))
    f.write("showSelectCharacter varnames: %r\n" % (code.co_varnames,))
    
    # Check sub-code objects
    for c in code.co_consts:
        if hasattr(c, 'co_name'):
            f.write("sub code %s:\n" % c.co_name)
            f.write("  names: %r\n" % (c.co_names,))
            f.write("  consts: %r\n" % (c.co_consts,))
            f.write("  varnames: %r\n" % (c.co_varnames,))
            # check if that subcode has subcode
            for sc in c.co_consts:
                if hasattr(sc, 'co_name'):
                    f.write("    nested sub code %s:\n" % sc.co_name)
                    f.write("      names: %r\n" % (sc.co_names,))
                    f.write("      consts: %r\n" % (sc.co_consts,))
                    f.write("      varnames: %r\n" % (sc.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
