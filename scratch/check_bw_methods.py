with open(OUT, 'w') as f:
    try:
        import BigWorld
        # Let's inspect BigWorld.entities or client methods if exposed to Python
        # Or let's see how BigWorld handles client methods
        f.write('BigWorld dir: ' + repr([x for x in dir(BigWorld) if 'method' in x.lower() or 'desc' in x.lower() or 'entity' in x.lower()]) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
