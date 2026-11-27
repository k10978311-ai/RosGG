f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/obp_scene.txt", "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.onBecomePlayer
    if hasattr(fn, 'im_func'): fn = fn.im_func
    for c in fn.func_closure or []:
        if hasattr(c.cell_contents, 'func_code'):
            code = c.cell_contents.func_code
            raw = [ord(x) for x in code.co_code]
            f.write("code len: %d\n" % len(raw))
            import dis
            for i in range(0, len(raw)):
                op = raw[i]
                opname = dis.opname[op]
                if opname in ('LOAD_GLOBAL', 'LOAD_ATTR', 'STORE_ATTR', 'CALL_FUNCTION', 'LOAD_CONST'):
                    arg = raw[i+1] + (raw[i+2] << 8) if op >= dis.HAVE_ARGUMENT else 0
                    val = ""
                    if opname in ('LOAD_GLOBAL', 'LOAD_ATTR', 'STORE_ATTR') and arg < len(code.co_names):
                        val = code.co_names[arg]
                    elif opname == 'LOAD_CONST' and arg < len(code.co_consts):
                        val = repr(code.co_consts[arg])
                    f.write("%4d: %-15s %s\n" % (i, opname, val))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
