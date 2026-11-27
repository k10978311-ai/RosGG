with open(OUT, 'w') as f:
    try:
        import dis, Athlete, StringIO, sys
        raw = Athlete.PlayerAthlete.__dict__['enterHall']
        inner = raw.func_closure[0].cell_contents
        
        s = StringIO.StringIO()
        sys.stdout = s
        dis.dis(inner)
        sys.stdout = sys.__stdout__
        f.write(s.getvalue())
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
