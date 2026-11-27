with open(OUT, 'w') as f:
    try:
        import sys
        classes_with_prereq = []
        for mod_name, mod in sys.modules.items():
            if not mod: continue
            for k, v in getattr(mod, '__dict__', {}).items():
                if isinstance(v, type) or hasattr(v, '__mro__'):
                    vd = getattr(v, '__dict__', None)
                    if vd and hasattr(vd, '__contains__') and 'prerequisites' in vd:
                        classes_with_prereq.append(getattr(v, '__name__', str(v)))
        f.write('Classes defining prerequisites: ' + repr(classes_with_prereq) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
