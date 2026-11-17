"""Search MakeFree (Tech Robin Hood) for free/open-source alternatives to a paid app.

The site is a static catalogue (data/core.json + data/m|r/NNN.json shards); this reads the
same files the page reads, so no browser is needed. Read-only: never votes, reports or suggests.

    .venv/bin/python execution/makefree.py "vercel"
    .venv/bin/python execution/makefree.py "elevenlabs" --top 15
    .venv/bin/python execution/makefree.py --list "video"      # paid apps whose name/scope matches

Page for humans: https://www.techrobinhood.com/updowndownleftrightleftrightbastart/?q=<name>
"""
import argparse
import json
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

BASE = "https://www.techrobinhood.com/updowndownleftrightleftrightbastart/data/"
CACHE = Path.home() / ".cache" / "makefree"
UA = {"User-Agent": "Mozilla/5.0"}
LISTABLE_LINKS = {"source_checked", "reported_repository", "unverified_candidate"}


def slug(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", s).lower()).strip()


def fetch(rel: str, version: str = "") -> dict:
    path = CACHE / (version or "head") / rel
    if path.exists():
        return json.loads(path.read_text())
    url = BASE + rel + (f"?v={version}" if version else "")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        data = r.read()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return json.loads(data)


def load_core() -> dict:
    # core.json is always re-read (small, carries the build version that keys the shard cache)
    with urllib.request.urlopen(urllib.request.Request(BASE + "core.json", headers=UA), timeout=30) as r:
        return json.loads(r.read())


def targets(core: dict) -> list[dict]:
    ids = core.get("targetIds") or {}
    out = []
    for i, (name, aliases, scope, bucket) in enumerate(core["targets"]):
        out.append({"id": ids.get(str(i)) or slug(name), "name": name, "aliases": aliases,
                    "scope": scope, "bucket": bucket})
    return out


def find_target(core: dict, query: str) -> list[dict]:
    q = norm(query)
    exact, partial = [], []
    for t in targets(core):
        keys = [norm(t["name"])] + [norm(a) for a in t["aliases"]]
        if q in keys or q.replace(" ", "") in [k.replace(" ", "") for k in keys]:
            exact.append(t)
        elif any(q in k for k in keys):
            partial.append(t)
    return exact + partial


def alternatives(core: dict, t: dict) -> tuple[list[dict], int]:
    b = f"{t['bucket']:03d}"
    v = core["v"]
    matches = fetch(f"m/{b}.json", v)
    rows = {r[0]: r for r in fetch(f"r/{b}.json", v)["rows"]}
    out = []
    for rid in matches["matches"].get(t["id"], []):
        r = rows.get(rid)
        if not r:
            continue
        pricing = core["pricing"][r[2]]
        link_state = core["linkStates"][r[5]]
        status = core["statuses"][r[9]] if len(r) > 9 and r[9] is not None else "live"
        if pricing not in ("Free", "Freemium") or link_state not in LISTABLE_LINKS or status == "not_software":
            continue
        out.append({"name": r[1], "pricing": pricing, "open_source": len(r) > 7 and r[7] == 1,
                    "url": r[4] if len(r) > 8 and r[8] == 1 else None, "checked": link_state == "source_checked",
                    "discontinued": status == "discontinued",
                    "about": (r[13].strip()[:160] if len(r) > 13 and isinstance(r[13], str) else "")})
    return out, matches.get("totals", {}).get(t["id"], len(out))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--list", action="store_true", help="only list matching paid apps")
    a = ap.parse_args()
    core = load_core()
    found = find_target(core, a.query)
    if a.list:
        q = norm(a.query)
        for t in targets(core):
            if q in norm(t["name"]) or q in norm(t["scope"]):
                print(f"{t['name']:40} {t['scope']}")
        return 0
    if not found:
        print(f"'{a.query}' no está en el catálogo de MakeFree. Probá --list con una palabra del rubro.")
        return 1
    t = found[0]
    alts, total = alternatives(core, t)
    others = ", ".join(x["name"] for x in found[1:6])
    print(f"== {t['name']} — {t['scope']}" + (f"  (también: {others})" if others else ""))
    print(f"   {len(alts)} alternativas listables (catálogo dice {total})")
    for x in alts[: a.top]:
        tag = "OSS" if x["open_source"] else x["pricing"]
        mark = "✓" if x["checked"] else " "
        dead = " [discontinuado]" if x["discontinued"] else ""
        print(f" {mark} {x['name'][:34]:34} {tag:9} {x['url'] or '(sin link)'}{dead}")
        if x["about"]:
            print(f"     {x['about']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
