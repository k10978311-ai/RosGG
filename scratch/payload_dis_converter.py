import inspect
import dis
import StringIO
import sys
import package_common.PackageConvert3 as pconv
import traceback

with open(OUT, "w") as f:
    try:
        f.write("PackageConvert3 dir: %r\n" % dir(pconv))
        converter = getattr(pconv, "dtsAppearancePackageConvert3", None)
        f.write("converter: %r\n" % converter)
        if converter:
            f.write("converter dir: %r\n" % dir(converter))
            for m in ["createObjFromDict", "getDictFromObj", "isSameType"]:
                if hasattr(converter, m):
                    fn = getattr(converter, m)
                    code = getattr(fn, "func_code", None)
                    if code:
                        s = StringIO.StringIO()
                        old = sys.stdout
                        sys.stdout = s
                        try:
                            dis.dis(code)
                        finally:
                            sys.stdout = old
                        f.write("\n--- %s ---\n" % m)
                        f.write("consts: %r\nnames: %r\n" % (code.co_consts, code.co_names))
                        f.write(s.getvalue())
    except Exception:
        f.write(traceback.format_exc())
