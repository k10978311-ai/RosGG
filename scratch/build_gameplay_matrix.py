#!/usr/bin/env python3
"""Build ros_server_v2/docs/gameplay_function_matrix.json from manifest + evidence files."""
from __future__ import annotations

import json
import os
import sys

try:
    import yaml
except ImportError:
    yaml = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "ros_server_v2", "docs")
MANIFEST = os.path.join(DOCS, "gameplay_function_ids.yaml")
EVIDENCE = os.path.join(DOCS, "gameplay_matrix_evidence.yaml")
OUT = os.path.join(DOCS, "gameplay_function_matrix.json")


def load_yaml(path):
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    manifest = load_yaml(MANIFEST)
    evidence = load_yaml(EVIDENCE)
    rows = []
    for cat in manifest["categories"]:
        cid = cat["id"]
        for fn in cat["functions"]:
            fid = fn["id"]
            ev = evidence.get(fid)
            if not ev:
                print(f"MISSING evidence for {fid}", file=sys.stderr)
                ev = {
                    "in_build_617289": "unknown",
                    "confidence": "generic_br_lore",
                    "client_evidence": [],
                    "data_evidence": [],
                    "server_status": "none",
                    "server_touchpoints": [],
                    "blockers": ["no evidence row yet"],
                }
            rows.append({
                "id": fid,
                "category": cid,
                "player_visible_name": fn["name"],
                "in_build_617289": ev.get("in_build_617289", "unknown"),
                "confidence": ev.get("confidence", "generic_br_lore"),
                "client_evidence": ev.get("client_evidence", []),
                "data_evidence": ev.get("data_evidence", []),
                "server_status": ev.get("server_status", "none"),
                "server_touchpoints": ev.get("server_touchpoints", []),
                "blockers": ev.get("blockers", []),
            })
    if len(rows) != 74:
        raise SystemExit(f"expected 74 functions, got {len(rows)}")
    doc = {
        "build": manifest.get("build", "1.610637.617289"),
        "package": manifest.get("package", "com.netease.chiji"),
        "generated_by": "scratch/build_gameplay_matrix.py",
        "function_count": len(rows),
        "functions": rows,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT} ({len(rows)} functions)")


if __name__ == "__main__":
    main()