
with open(OUT, 'w') as f:
    try:
        import BigWorld
        p = BigWorld.player()
        f.write('player id: ' + repr(p.id) + '\n')
        f.write('all entities: ' + repr([(e.id, type(e)) for e in BigWorld.entities.values()]) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
