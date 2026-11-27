
with open(OUT, 'w') as f:
    try:
        import BigWorld
        p = BigWorld.player()
        f.write('player: ' + repr(p) + '\n')
        f.write('player type: ' + repr(type(p)) + '\n')
        f.write('hasattr base: ' + repr(hasattr(p, 'base')) + '\n')
        if hasattr(p, 'base'):
            f.write('base: ' + repr(p.base) + '\n')
            f.write('base dir: ' + repr([x for x in dir(p.base) if 'request' in x.lower() or 'leave' in x.lower()]) + '\n')
            f.write('base all methods count: ' + str(len(dir(p.base))) + '\n')
        f.write('hasattr cell: ' + repr(hasattr(p, 'cell')) + '\n')
        if hasattr(p, 'cell'):
            f.write('cell: ' + repr(p.cell) + '\n')
            f.write('cell dir: ' + repr([x for x in dir(p.cell) if 'request' in x.lower() or 'leave' in x.lower()]) + '\n')
            f.write('cell all methods count: ' + str(len(dir(p.cell))) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
