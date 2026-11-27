import inspect
import package_client.PackageClient3 as pcp
import traceback

with open(OUT, "w") as f:
    try:
        cls = pcp.DtsAppearancePackageClient3
        f.write("DtsAppearancePackageClient3 mro: %r\n" % (cls.__mro__,))
        for method in ["createObjFromDict", "set_itemList", "onAddItem", "addItem", "_init_data", "readStream", "initPackage"]:
            if hasattr(cls, method):
                f.write("\n--- Method: %s ---\n" % method)
                try:
                    f.write(inspect.getsource(getattr(cls, method)))
                except Exception as e:
                    f.write("error getting source: %s\n" % e)
    except Exception:
        f.write(traceback.format_exc())
