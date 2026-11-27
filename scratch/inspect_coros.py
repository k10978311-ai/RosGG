f = open(OUT, "w")
try:
    import Athlete
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem") if scene else None
    
    # Check coroutines in ss
    f.write("ss: %r\n" % (ss,))
    if ss:
        for a in dir(ss):
            if 'coro' in a.lower() or 'task' in a.lower() or 'load' in a.lower():
                try:
                    f.write("  ss.%s = %r\n" % (a, getattr(ss, a)))
                except:
                    pass
                    
    # Check Application loading state
    from libclaudia.Classes.Application import Application as app
    f.write("app.is_loading(): %r\n" % (getattr(app, 'is_loading', lambda: '<none>')(),))
    f.write("app.____current_level__: %r\n" % (getattr(app, '____current_level__', '<none>'),))
    f.write("app.____loaded_level__: %r\n" % (getattr(app, '____loaded_level__', '<none>'),))
    f.write("app.____next_level__: %r\n" % (getattr(app, '____next_level__', '<none>'),))
    f.write("app.____next_level_callback__: %r\n" % (getattr(app, '____next_level_callback__', '<none>'),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
