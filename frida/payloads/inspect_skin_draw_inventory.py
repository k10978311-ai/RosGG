# READ-ONLY: Skin, Draw, and Inventory Inspector for Rules of Survival Athlete
import sys, traceback

f = open(OUT, 'w')
def w(s): f.write(str(s) + '\n')

w("=== SKIN, DRAW & INVENTORY DEEP INSPECTION ===")

try:
    import BigWorld, Globals

    p = BigWorld.player()
    w("\n--- [Player Identity & Class] ---")
    w("player = %r" % (p,))
    if p is not None:
        w("class: %s (id=%r)" % (p.__class__.__name__, getattr(p, 'id', None)))
        
        # 1. Economy & Currencies
        w("\n--- [Currencies & Economy] ---")
        w("freeYuanbao: %r" % getattr(p, 'freeYuanbao', None))
        w("payYuanbao: %r" % getattr(p, 'payYuanbao', None))
        w("diamond: %r" % getattr(p, 'diamond', None))
        w("gold: %r" % getattr(p, 'gold', None))
        curr_list = getattr(p, 'currencyList', None)
        w("currencyList: len=%d %r" % (len(curr_list) if curr_list else 0, curr_list))

        # 2. Appearance & Skins Package
        w("\n--- [Appearance / Skin Package (dtsAppearancePackage)] ---")
        pkg = getattr(p, 'dtsAppearancePackage', None)
        if pkg is not None:
            w("pkg type: %s" % type(pkg))
            w("pkg dir: %r" % [attr for attr in dir(pkg) if not attr.startswith('__')])
            # Check itemList or items
            for attr in ('itemList', 'itemsList', '_packageCapacity', 'layoutInfo'):
                val = getattr(pkg, attr, None)
                if isinstance(val, (list, tuple, dict)):
                    w("  pkg.%s: len=%d sample=%r" % (attr, len(val), str(val)[:150]))
                else:
                    w("  pkg.%s: %r" % (attr, val))
        else:
            w("dtsAppearancePackage is None!")

        # 3. Equipped Appearances / Outfits
        w("\n--- [Equipped Appearance Slots] ---")
        for attr in [
            'dtsAppearanceGender', 'currentGender',
            'dtsShowWearableAppearanceList', 'dtsWearableAppearanceList',
            'dtsShowBodyAppearanceList', 'dtsBodyAppearanceList',
            'dtsShowWeaponAppearanceList', 'dtsWeaponAppearanceList',
            'dtsShowVehicleAppearanceList', 'dtsVehicleAppearanceList',
            'dtsShowAircraftAppearanceID', 'dtsHallThemeID', 'dtsPetAppearance'
        ]:
            w("  %s = %r" % (attr, getattr(p, attr, '<missing>')))

        # 4. Ros2 Inventory Packages (Repertory, Battle, EquipBar)
        w("\n--- [Ros2 Inventory & Depot Packages] ---")
        for pkg_name in [
            'dtsRos2RepertoryPackage', 'dtsRos2BattleItemPackage',
            'dtsRos2EquipBarPackage', 'dtsRos2DfdBattleItemPackage'
        ]:
            pkg = getattr(p, pkg_name, None)
            if pkg is not None:
                items = getattr(pkg, 'itemList', getattr(pkg, 'items', None))
                cap = getattr(pkg, '_packageCapacity', getattr(pkg, 'capacity', None))
                if isinstance(items, (list, tuple, dict)):
                    w("  %s: cap=%r, items_len=%d sample=%r" % (pkg_name, cap, len(items), str(items)[:200]))
                else:
                    w("  %s: cap=%r, items=%r" % (pkg_name, cap, items))
            else:
                w("  %s: None" % pkg_name)

        # 5. Supply & Draw Systems
        w("\n--- [Supply & Draw Systems] ---")
        avail_sup = getattr(p, 'availSupplementDict', getattr(p, 'availSupplement', None))
        if avail_sup is not None:
            w("availSupplement count: %d" % len(avail_sup))
            if isinstance(avail_sup, dict):
                sample_keys = list(avail_sup.keys())[:10]
                w("  sample box IDs: %r" % sample_keys)
                for sk in sample_keys[:3]:
                    w("    box %r: %r" % (sk, avail_sup[sk]))
        else:
            w("availSupplement is None")

        lucky_data = getattr(p, 'luckyCarnivalData', None)
        w("luckyCarnivalData: %r" % (lucky_data,))

    # 6. UI Manager & Active Panels
    w("\n--- [Active UI Stack & Panels] ---")
    um = getattr(Globals, 'uiMgr', None)
    if um:
        vis = getattr(um, '_UIMgr____all_ui__vis', {})
        if isinstance(vis, dict):
            visible_uis = {k: v for k, v in vis.items() if v}
            w("Visible UIs (%d): %r" % (len(visible_uis), visible_uis))
        times = getattr(um, '_UIMgr____all_ui_enter_times', {})
        if isinstance(times, dict):
            w("Entered UIs: %r" % (list(times.keys()),))
        stack = getattr(um, '_UIMgr____ui_stack', None)
        w("UI Stack: %r" % (stack,))

except Exception:
    w("EXCEPTION IN INSPECTOR:")
    w(traceback.format_exc())

w("\n=== END OF INSPECTION ===")
f.close()
