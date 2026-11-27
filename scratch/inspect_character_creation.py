f = open(OUT, "w")
try:
    import Athlete, dis, StringIO, sys
    pa = Athlete.PlayerAthlete
    f.write("PlayerAthlete found: %r\n" % (pa,))
    
    # Check onBecomePlayer
    fn = pa.__dict__.get("onBecomePlayer")
    if fn:
        buf = StringIO.StringIO()
        old = sys.stdout; sys.stdout = buf
        dis.dis(fn)
        sys.stdout = old
        f.write("=== onBecomePlayer ===\n" + buf.getvalue() + "\n")
        
    # Check showSelectCharacter
    fn = pa.__dict__.get("showSelectCharacter")
    if fn:
        buf = StringIO.StringIO()
        old = sys.stdout; sys.stdout = buf
        dis.dis(fn)
        sys.stdout = old
        f.write("=== showSelectCharacter ===\n" + buf.getvalue() + "\n")
        
    # Check onCreateCharacter
    fn = pa.__dict__.get("onCreateCharacter")
    if fn:
        buf = StringIO.StringIO()
        old = sys.stdout; sys.stdout = buf
        dis.dis(fn)
        sys.stdout = old
        f.write("=== onCreateCharacter ===\n" + buf.getvalue() + "\n")

    # Check onRoleCreateSuc
    fn = pa.__dict__.get("onRoleCreateSuc")
    if fn:
        buf = StringIO.StringIO()
        old = sys.stdout; sys.stdout = buf
        dis.dis(fn)
        sys.stdout = old
        f.write("=== onRoleCreateSuc ===\n" + buf.getvalue() + "\n")
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
