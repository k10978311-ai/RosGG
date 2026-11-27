import sys
f = open(OUT, "w")
try:
    import helpers.channel.channel_login as cl
    f.write("cl.channel: %r\n" % (cl.__dict__.get('channel'),))
    ch = cl.__dict__.get('channel')
    if ch:
        f.write("dir(ch): %r\n" % (dir(ch),))
        fn = getattr(ch, 'game_login_success', None)
        if fn:
            co = fn.func_code
            f.write("names: %r\n" % (co.co_names,))
            f.write("consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, 'co_names')],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
