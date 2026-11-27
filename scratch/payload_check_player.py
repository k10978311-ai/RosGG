import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("player: %r\n" % p)
        f.write("player id: %r\n" % (getattr(p, 'id', None),))
        f.write("player class: %r\n" % (p.__class__.__name__ if p else None,))
        f.write("has dtsAppearancePackage: %r\n" % hasattr(p, 'dtsAppearancePackage'))
        f.write("has dtsRos2RepertoryPackage: %r\n" % hasattr(p, 'dtsRos2RepertoryPackage'))
        f.write("has dtsAppearanceRepertoryPackage: %r\n" % hasattr(p, 'dtsAppearanceRepertoryPackage'))
        if hasattr(p, 'dtsRos2RepertoryPackage'):
            rpkg = p.dtsRos2RepertoryPackage
            f.write("dtsRos2RepertoryPackage: %r\n" % rpkg)
            f.write("rpkg itemList: %r\n" % getattr(rpkg, 'itemList', None))
    except Exception:
        f.write(traceback.format_exc())
