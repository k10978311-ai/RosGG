import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        import world
        import logic.Globals as Globals
        import logic.gcommon.common.SceneSystem as SceneSystem
        import logic.gcommon.common.UIManager as UIManager

        f.write("scene: %r\n" % (getattr(world, "scene", None) or getattr(Globals, "scene", None)))
        f.write("currentMapId: %r\n" % (getattr(SceneSystem, "currentMapId", None),))
        f.write("curSceneName: %r\n" % (getattr(SceneSystem, "curSceneName", None),))

        # Check UIManager
        ui_mgr = getattr(UIManager, "UIManager", None)
        f.write("UIManager: %r\n" % ui_mgr)
        if hasattr(UIManager, "getUI"):
            for ui_name in ["UIMain", "UIR2Main", "UILogin", "UILoading", "UIBattle", "UIBag", "UILooks", "UISupply", "UIDepot"]:
                try:
                    ui = UIManager.getUI(ui_name)
                    f.write("UI %s: %r (visible=%r)\n" % (ui_name, ui, getattr(ui, "isVisible", None) if ui else None))
                except Exception as e:
                    f.write("UI %s error: %s\n" % (ui_name, e))
        
        # Check all registered UIs in UIManager if available
        for attr in ["_uiDict", "allUI", "_loadedUI", "uiList"]:
            if hasattr(UIManager, attr):
                f.write("UIManager.%s: %r\n" % (attr, getattr(UIManager, attr)))

    except Exception:
        f.write(traceback.format_exc())
