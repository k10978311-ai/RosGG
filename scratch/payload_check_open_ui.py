import Globals
import traceback

with open(OUT, "w") as f:
    try:
        uiMgr = Globals.uiMgr
        all_ui = getattr(uiMgr, "_UIMgr____all_ui__", None)
        f.write("all_ui type: %s, len: %r\n" % (type(all_ui), len(all_ui) if hasattr(all_ui, '__len__') else None))
        if all_ui:
            for k in all_ui:
                v = all_ui[k]
                f.write("  %s: %r (active=%r, visible=%r)\n" % (
                    k, v,
                    getattr(v, "isActiveAndEnabled", getattr(v, "active", None)),
                    getattr(v, "isVisible", getattr(v, "visible", None))
                ))
        main_ui = getattr(uiMgr, "____focus_main_ui__", None)
        f.write("focus_main_ui: %r\n" % main_ui)
    except Exception:
        f.write(traceback.format_exc())
