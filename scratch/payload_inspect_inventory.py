import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("=== INSPECTING INVENTORY / DEPOT PACKAGES ===\n")
        
        # Check all package properties on PlayerAthlete
        pkgs = [
            "dtsRos2RepertoryPackage",
            "dtsRos2BattleItemPackage",
            "dtsRos2EquipBarPackage",
            "dtsRos2DefenderEquipBarPackage",
            "dtsRos2DfdBattleItemPackage",
            "dtsAppearancePackage"
        ]
        for pname in pkgs:
            pkg = getattr(p, pname, None)
            f.write("\n--- %s ---\n" % pname)
            f.write("  obj: %r\n" % pkg)
            if pkg:
                f.write("  type: %s\n" % type(pkg).__name__)
                for a in ["itemList", "packageCapacity", "_packageCapacity", "PackageCapacity", "canAddItem", "getUsedGridNum", "getItemCnt"]:
                    if hasattr(pkg, a):
                        val = getattr(pkg, a)
                        if callable(val):
                            try:
                                val = val()
                            except Exception as e:
                                val = "error: %s" % e
                        f.write("  %s: %r\n" % (a, val))
        
        # Check inventory methods on PlayerAthlete
        f.write("\n=== INVENTORY METHODS ON ATHLETE ===\n")
        inv_methods = [m for m in dir(p) if any(k in m.lower() for k in ["repertory", "depot", "warehouse", "safebox", "package", "bag"])]
        for m in sorted(inv_methods):
            f.write("  %s\n" % m)

    except Exception:
        f.write(traceback.format_exc())
