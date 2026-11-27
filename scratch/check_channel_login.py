f = open(OUT, "w")
try:
    import channel_login
    fn = channel_login.onLoginByServerSauth
    co = fn.func_code
    f.write("onLoginByServerSauth names: %r\n" % (co.co_names,))
    f.write("onLoginByServerSauth consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, 'co_names')],))
    for c in co.co_consts:
        if hasattr(c, 'co_names'):
            f.write("  sub %s names: %r\n" % (c.co_name, c.co_names))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
