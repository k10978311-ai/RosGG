with open(OUT, 'w') as f:
    try:
        import Globals
        f.write('Globals.player: ' + repr(Globals.player) + '\n')
        # check if property
        cls = Globals.__class__ if hasattr(Globals, '__class__') else None
        f.write('Globals class: ' + repr(cls) + '\n')
        if hasattr(Globals, '__dict__'):
            f.write('Globals.__dict__ player: ' + repr(Globals.__dict__.get('player')) + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
