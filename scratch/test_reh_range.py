OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld, Globals, Athlete
    p = BigWorld.player()
    f.write("Testing statements between offset 15 and 588...\n")
    
    # 1. readGMRedhintMsg
    try:
        from entities.Athlete import updateReadGMRedhintMsg, readGMRedhintMsg
        f.write("1. import GMRedhint: OK\n")
    except Exception as e:
        f.write("1. import GMRedhint FAILED: %r\n" % e)
        
    # 2. Globals.settings
    try:
        f.write("2. Globals.settings: %r\n" % getattr(Globals, 'settings', 'NO_ATTR'))
        if hasattr(Globals, 'settings'):
            f.write("   settings.isColorAdjust: %r\n" % getattr(Globals.settings, 'isColorAdjust', 'NO_ATTR'))
    except Exception as e:
        f.write("2. Globals.settings FAILED: %r\n" % e)
        
    # 3. helpers.GameSDK
    try:
        import helpers
        f.write("3. helpers.GameSDK: %r\n" % getattr(helpers, 'GameSDK', 'NO_ATTR'))
    except Exception as e:
        f.write("3. helpers.GameSDK FAILED: %r\n" % e)
        
    # 4. SALogging
    try:
        import SALogging
        f.write("4. SALogging: %r\n" % SALogging)
    except Exception as e:
        f.write("4. SALogging FAILED: %r\n" % e)
        
    # 5. p.tryUploadRCVersion
    try:
        f.write("5. p.tryUploadRCVersion: %r\n" % getattr(p, 'tryUploadRCVersion', 'NO_ATTR'))
        fn = getattr(p, 'tryUploadRCVersion', None)
        if fn:
            # check what it does
            f.write("   tryUploadRCVersion names: %r\n" % (fn.im_func.func_code.co_names,))
    except Exception as e:
        f.write("5. tryUploadRCVersion FAILED: %r\n" % e)

    # 6. doRealnameAuthenAgain
    try:
        f.write("6. p.doRealnameAuthenAgain: %r\n" % getattr(p, 'doRealnameAuthenAgain', 'NO_ATTR'))
    except Exception as e:
        f.write("6. doRealnameAuthenAgain FAILED: %r\n" % e)

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
