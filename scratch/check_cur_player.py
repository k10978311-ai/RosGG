with open(OUT, 'w') as f:
    try:
        import BigWorld
        p = BigWorld.player()
        f.write('player: ' + repr(p) + '\n')
        f.write('player class: ' + repr(p.__class__) + '\n')
        f.write('player id: ' + repr(getattr(p, 'id', None)) + '\n')
        base = getattr(p, 'base', None)
        f.write('base: ' + repr(base) + '\n')
        if base:
            f.write('base dir: ' + repr(dir(base)) + '\n')
        cell = getattr(p, 'cell', None)
        f.write('cell: ' + repr(cell) + '\n')
        if cell:
            f.write('cell dir: ' + repr(dir(cell)) + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
