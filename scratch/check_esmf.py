OUT = '/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log'
f = open(OUT, 'w')
try:
    import Globals
    f.write('Globals.enterSelectModeFinished = %r\n' % getattr(Globals, 'enterSelectModeFinished', 'NO_ATTR'))
    f.write('Globals.rookieEnterHall = %r\n' % getattr(Globals, 'rookieEnterHall', 'NO_ATTR'))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
