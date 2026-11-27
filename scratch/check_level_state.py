f = open(OUT, "w")
try:
    from libclaudia.Classes.Application import Application as app
    f.write("app.____current_level__: %r\n" % (getattr(app, '____current_level__', None),))
    f.write("app.____loaded_level__: %r\n" % (getattr(app, '____loaded_level__', None),))
    f.write("app.____next_level__: %r\n" % (getattr(app, '____next_level__', None),))
    f.write("app.____next_level_callback__: %r\n" % (getattr(app, '____next_level_callback__', None),))
    
    # Check levels in app.____loaded_level__
    ll = getattr(app, '____loaded_level__', {})
    for k, lvl in ll.items():
        f.write("Level %r: preloadPercent=%r, coro=%r\n" % (k, getattr(lvl, 'preloadPercent', None), getattr(lvl, 'coro', None)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
