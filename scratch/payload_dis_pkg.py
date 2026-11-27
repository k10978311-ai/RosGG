import dis
import StringIO
import sys
import package_client.PackageClient3 as pcp
import package_common.Package3 as pcommon
import traceback

with open(OUT, "w") as f:
    try:
        cls = pcp.DtsAppearancePackageClient3
        f.write("cls dir: %r\n" % dir(cls))
        
        # Disassemble createObjFromDict
        for c in [pcp.DtsAppearancePackageClient3, pcommon.DtsAppearancePackage3, pcommon.Package3]:
            if hasattr(c, "createObjFromDict"):
                fn = getattr(c, "createObjFromDict")
                code = getattr(fn, "func_code", getattr(fn, "im_func", None))
                if hasattr(code, "func_code"):
                    code = code.func_code
                if code:
                    s = StringIO.StringIO()
                    old = sys.stdout
                    sys.stdout = s
                    try:
                        dis.dis(code)
                    finally:
                        sys.stdout = old
                    f.write("\n--- %s.createObjFromDict ---\n" % c.__name__)
                    f.write("consts: %r\nnames: %r\n" % (code.co_consts, code.co_names))
                    f.write(s.getvalue())
                    break
    except Exception:
        f.write(traceback.format_exc())
