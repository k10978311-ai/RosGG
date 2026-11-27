import package_common.PackageConvert3 as pconv
import traceback

with open(OUT, "w") as f:
    try:
        c = pconv.dtsAppearancePackageConvert3
        test_item = {
            "uuid": "0123456789abcdef",
            "itemID": 120901,
            "number": 1,
            "info": {}
        }
        # Test 1: with itemList only
        d1 = {
            "itemList": [test_item],
            "itemsList": [],
            "_packageCapacity": 200,
            "layoutInfo": {}
        }
        obj1 = c.createObjFromDict(d1)
        f.write("obj1 itemList: %r\n" % getattr(obj1, "itemList", None))

        # Test 2: with itemsList only
        d2 = {
            "itemList": [],
            "itemsList": [[test_item]],
            "_packageCapacity": 200,
            "layoutInfo": {}
        }
        obj2 = c.createObjFromDict(d2)
        f.write("obj2 itemList: %r\n" % getattr(obj2, "itemList", None))

        # Test 3: getDictFromObj on obj1
        d_back = c.getDictFromObj(obj1)
        f.write("d_back keys: %r\n" % d_back.keys())
        f.write("d_back itemList: %r\n" % d_back.get("itemList"))
        f.write("d_back itemsList: %r\n" % d_back.get("itemsList"))
    except Exception:
        f.write(traceback.format_exc())
