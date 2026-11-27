OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    GameObject = real_fn.func_globals.get('GameObject')
    scene_go = GameObject.Find('Scene')
    ss = scene_go.GetComponent('SceneSystem')
    
    fn = ss.loadHallScene.im_func
    code = bytearray(fn.func_code.co_code)
    names = fn.func_code.co_names
    consts = fn.func_code.co_consts
    varnames = fn.func_code.co_varnames
    
    f.write("loadHallScene len: %d\n" % len(code))
    f.write("names: %r\n" % (names,))
    f.write("consts: %r\n" % (consts,))
    f.write("varnames: %r\n" % (varnames,))
    
    i = 0
    n = len(code)
    while i < n:
        offset = i
        op = code[i]
        i += 1
        arg_val = ""
        arg = None
        if op >= 90:
            arg = code[i] | (code[i+1] << 8)
            i += 2
            arg_val = "%d" % arg
            if op in (101, 116):
                if arg < len(names): arg_val += " (name: %s)" % names[arg]
            elif op in (96, 155, 156):
                if arg < len(names): arg_val += " (name: %s)" % names[arg]
            elif op == 100 or op in (124, 125):
                if arg < len(consts):
                    c = consts[arg]
                    arg_val += " (const: %s)" % (c.co_name if hasattr(c, 'co_name') else repr(c))
            elif op in (110, 111, 112, 113, 114, 120, 121, 122, 148):
                arg_val += " -> %d" % arg
        f.write("%4d: op=%3d %s\n" % (offset, op, arg_val))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
