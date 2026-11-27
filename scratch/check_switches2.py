f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/sw_dump2.txt", "w")
try:
    import ClientEntity
    sw = getattr(ClientEntity, 'switches', None)
    f.write("switches: %r\n" % sw)
    if sw:
        f.write("dir: %r\n" % dir(sw))
        for k in dir(sw):
            if 'flow' in k.lower() or 'enter' in k.lower() or 'plane' in k.lower() or 'prereq' in k.lower():
                f.write("switch %s = %r\n" % (k, getattr(sw, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
