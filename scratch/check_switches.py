f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/sw_dump.txt", "w")
try:
    import switches
    f.write("switches dir: %r\n" % dir(switches))
    for k in dir(switches):
        if 'flow' in k.lower() or 'enter' in k.lower() or 'plane' in k.lower() or 'prereq' in k.lower():
            f.write("switch %s = %r\n" % (k, getattr(switches, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
