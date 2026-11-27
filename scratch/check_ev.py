with open(OUT, 'w') as f:
    try:
        import elkLogging, const
        ver = elkLogging.getEngineVersion()
        f.write('engine version: ' + repr(ver) + '\n')
        f.write('RC3: ' + repr(const.EngineVersion.RC3) + '\n')
        f.write('less than RC3? ' + repr(ver < const.EngineVersion.RC3) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
