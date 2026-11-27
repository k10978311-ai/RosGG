import sys
import traceback

with open(OUT, "w") as f:
    try:
        import iSupplement
        f.write("iSupplement dir: %r\n" % dir(iSupplement))
        
        import iLottery
        f.write("iLottery dir: %r\n" % dir(iLottery))
        
        import iTreasureMall
        f.write("iTreasureMall dir: %r\n" % dir(iTreasureMall))

        import iOpenSupplyGift
        f.write("iOpenSupplyGift dir: %r\n" % dir(iOpenSupplyGift))

        # Check methods on PlayerAthlete relating to openSupply, draw, lottery, box
        import Athlete
        pa = Athlete.PlayerAthlete
        draw_methods = [m for m in dir(pa) if any(k in m.lower() for k in ["supply", "draw", "lottery", "box", "carnival", "lucky"])]
        f.write("Draw/Supply methods on PlayerAthlete:\n")
        for m in sorted(draw_methods):
            f.write("  %s\n" % m)
    except Exception:
        f.write(traceback.format_exc())
