import package_common.PackageConvert3 as pconv
import traceback

with open(OUT, "w") as f:
    try:
        c = pconv.dtsAppearancePackageConvert3
        for name in ['convertItemListTODict', 'convertItemListsIntoDict', 'convertDictToItemList', 'convertDictToItemsList']:
            fn = getattr(c, name, None)
            if fn:
                code = getattr(fn, 'func_code', None)
                f.write("%s:\n  args: %r\n  varnames: %r\n  consts: %r\n  names: %r\n" % (
                    name, code.co_argcount if code else None,
                    code.co_varnames if code else None,
                    code.co_consts if code else None,
                    code.co_names if code else None
                ))
    except Exception:
        f.write(traceback.format_exc())
