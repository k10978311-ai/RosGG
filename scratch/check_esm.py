with open(OUT, 'w') as f:
    try:
        import Globals, shared.switches as switches
        f.write('enterSelectModeFinished: ' + repr(getattr(Globals, 'enterSelectModeFinished', 'NONE')) + '\n')
        f.write('PCEnableMode: ' + repr(getattr(switches, 'PCEnableMode', 'NONE')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
