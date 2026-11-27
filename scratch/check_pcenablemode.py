with open(OUT, 'w') as f:
    try:
        import shared.switches as switches
        f.write('PCEnableMode: ' + repr(getattr(switches, 'PCEnableMode', 'NOT_FOUND')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
