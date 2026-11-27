import sys
import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        if p:
            pkg = getattr(p, "dtsAppearancePackage", None)
            if pkg:
                items_dict = getattr(pkg, "itemList", {})
                f.write("All Appearance Skin IDs in Wardrobe (%d total):\n" % len(items_dict))
                f.write("%r\n" % sorted(items_dict.keys()))
                
            f.write("\nCurrencies:\n")
            for i, c in enumerate(getattr(p, "currencyList", [])):
                val = getattr(c, "count", getattr(c, "value", None))
                if val is None and hasattr(c, "__getitem__"):
                    try:
                        val = c[1]
                    except Exception:
                        pass
                f.write("  cur[%d]: id=%r, val=%r, repr=%r\n" % (i, getattr(c, "id", None), val, c))

        f.write("\nMatching Modules in sys.modules:\n")
        mod_matches = [m for m in sys.modules.keys() if any(w in m.lower() for w in ['scene', 'hall', 'mall', 'draw', 'supply', 'wardrobe', 'appear', 'depot'])]
        f.write("%r\n" % sorted(mod_matches))
    except Exception:
        f.write(traceback.format_exc())
