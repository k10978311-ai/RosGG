#!/usr/bin/env python3
"""Rebuild RoS APK: launcher icon, optional same-length app label, optional file overlays, sign."""
from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / "game" / "patches" / "v003_2026-11-18_phone-trustall" / "game.apk"
OUT_UNSIGNED = ROOT / "scratch" / "ros_custom_unsigned.apk"
OUT_SIGNED_DIR = ROOT / "scratch" / "signed_apk"
JAVA = ROOT / "decompile" / "tools" / "jdk" / "bin" / "java.exe"
SIGNER = ROOT / "decompile" / "tools" / "uber-apk-signer.jar"
LABEL_OLD = b"Rules of Survival"


def make_round(img: Image.Image) -> Image.Image:
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img.width, img.height), fill=255)
    res = img.copy()
    res.putalpha(mask)
    return res


def icon_replacements(icon_path: Path) -> dict[str, bytes]:
    master = Image.open(icon_path).convert("RGBA")
    out: dict[str, bytes] = {}
    sizes = {
        "ldpi": 36,
        "mdpi": 48,
        "hdpi": 72,
        "xhdpi": 96,
        "xxhdpi": 144,
        "xxxhdpi": 192,
    }
    for density, sz in sizes.items():
        sq = master.resize((sz, sz), Image.Resampling.LANCZOS)
        buf_sq = io.BytesIO()
        sq.save(buf_sq, "PNG")
        sq_bytes = buf_sq.getvalue()
        rnd = make_round(sq)
        buf_rnd = io.BytesIO()
        rnd.save(buf_rnd, "PNG")
        rnd_bytes = buf_rnd.getvalue()
        out[f"res/drawable-{density}/ic_launcher.png"] = sq_bytes
        out[f"res/mipmap-{density}/ic_launcher.png"] = sq_bytes
        out[f"res/mipmap-{density}/ic_launcher_round.png"] = rnd_bytes
    bg_sizes = {
        "ldpi": 81,
        "mdpi": 108,
        "hdpi": 162,
        "xhdpi": 216,
        "xxhdpi": 324,
        "xxxhdpi": 432,
    }
    for density, sz in bg_sizes.items():
        bg = master.resize((sz, sz), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        bg.save(buf, "PNG")
        out[f"res/drawable-{density}/ic_launcher_background.png"] = buf.getvalue()
    out["res/drawable/ic_launcher.png"] = out["res/drawable-xxhdpi/ic_launcher.png"]
    return out


def patch_label(arsc: bytes, label: str) -> bytes:
    n = len(LABEL_OLD)
    label = label[:n].ljust(n)
    new_b = label.encode("utf-8")
    if len(new_b) != n:
        raise ValueError(f'App label must fit in {n} UTF-8 bytes (got {len(new_b)} for "{label}")')
    if LABEL_OLD not in arsc:
        raise RuntimeError("Could not find default app label in resources.arsc")
    return arsc.replace(LABEL_OLD, new_b, 1)


def parse_overlay(spec: str) -> tuple[str, Path]:
    if "=" not in spec:
        raise ValueError(f"Overlay must be LOCAL=apk/path/in/zip — got {spec!r}")
    local, inner = spec.split("=", 1)
    return inner.lstrip("/"), Path(local)


def build(
    base_apk: Path,
    icon_path: Path,
    label: str | None,
    overlays: list[tuple[str, Path]],
) -> Path:
    if not base_apk.is_file():
        raise FileNotFoundError(base_apk)
    icons = icon_replacements(icon_path)
    replace_map = dict(icons)
    for inner_path, local in overlays:
        if not local.is_file():
            raise FileNotFoundError(local)
        replace_map[inner_path] = local.read_bytes()

    exclude_prefixes = ("META-INF/",)
    exclude_exact = {
        "res/mipmap-anydpi-v26/ic_launcher.xml",
        "res/mipmap-anydpi-v26/ic_launcher_round.xml",
    }

    OUT_UNSIGNED.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(base_apk, "r") as zin:
        with zipfile.ZipFile(OUT_UNSIGNED, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                name = item.filename
                if any(name.startswith(p) for p in exclude_prefixes):
                    continue
                if name in exclude_exact:
                    continue
                if name in replace_map:
                    continue
                data = zin.read(name)
                if label and name == "resources.arsc":
                    data = patch_label(data, label)
                zout.writestr(item, data)
            for path_in_apk, data in replace_map.items():
                zout.writestr(path_in_apk, data)

    print(f"[+] unsigned: {OUT_UNSIGNED} ({OUT_UNSIGNED.stat().st_size} bytes)")

    if not JAVA.is_file():
        raise FileNotFoundError(f"Missing JDK: {JAVA}")
    if not SIGNER.is_file():
        raise FileNotFoundError(f"Missing signer: {SIGNER}")
    OUT_SIGNED_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [str(JAVA), "-jar", str(SIGNER), "-a", str(OUT_UNSIGNED), "-o", str(OUT_SIGNED_DIR), "--allowResign"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        raise RuntimeError("signing failed")
    apks = sorted(OUT_SIGNED_DIR.glob("*.apk"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not apks:
        raise RuntimeError("no signed apk in scratch/signed_apk")
    signed = apks[0]
    print(f"[+] signed:   {signed}")
    return signed


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base", type=Path, default=DEFAULT_BASE, help="Base APK (phone-trustall v003 recommended)")
    p.add_argument("--icon", type=Path, required=True, help="PNG/JPG master icon (square)")
    p.add_argument("--label", default="", help=f'Launcher name, exactly {len(LABEL_OLD)} chars UTF-8')
    p.add_argument(
        "--overlay",
        action="append",
        default=[],
        help="Replace/add APK entry: C:\\path\\file.png=assets/foo.png",
    )
    args = p.parse_args()
    overlays = [parse_overlay(s) for s in args.overlay]
    label = args.label.strip() or None
    build(args.base, args.icon, label, overlays)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())