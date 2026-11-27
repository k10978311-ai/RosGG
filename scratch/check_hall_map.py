f = open(OUT, "w")
try:
    import const, maps_utils
    f.write("const.HALL_MAP_ID: %r\n" % (getattr(const, "HALL_MAP_ID", None),))
    hall_id = getattr(const, "HALL_MAP_ID", 101)
    f.write("getMapData: %r\n" % (getattr(maps_utils, "getMapData", lambda x: None)(hall_id),))
    f.write("getScenePath: %r\n" % (getattr(maps_utils, "getScenePath", lambda x: None)(hall_id),))
    
    # Check Globals.uiMgr
    import Globals
    f.write("Globals.uiMgr: %r\n" % (Globals.uiMgr,))
    if Globals.uiMgr:
        f.write("loaded_ui: %r\n" % (getattr(Globals.uiMgr, "_loaded_ui", None),))
        f.write("visible_ui: %r\n" % (getattr(Globals.uiMgr, "_visible_ui", None),))
        loading = Globals.uiMgr.get_ui("UILoading")
        f.write("UILoading: %r\n" % (loading,))
        if loading:
            f.write("UILoading is_visible: %r\n" % (getattr(loading, "is_visible", None),))
            f.write("UILoading is_show: %r\n" % (getattr(loading, "is_show", None),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
