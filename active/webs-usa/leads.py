"""Pull US local businesses WITHOUT a website from Google Maps (via Apify) into a CSV.

Usage:
  .venv/bin/python active/webs-usa/leads.py "landscaping" "Houston, TX" --max 60

Needs APIFY_API_TOKEN in ~/facu-os/.env (free plan = US$5/month of credit).
Read-only: it contacts nobody. Output: active/webs-usa/leads/<niche>_<city>.csv (gitignored data).
"""
import argparse, csv, os, re, sys, time
from pathlib import Path
import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parents[1] / ".env")
ACTOR = "compass~crawler-google-places"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("niche")
    ap.add_argument("city")
    ap.add_argument("--max", type=int, default=60, help="places to crawl (cost ~US$0.004 each)")
    a = ap.parse_args()

    token = os.getenv("APIFY_API_TOKEN", "").strip()
    if not token:
        sys.exit("APIFY_API_TOKEN vacío en .env — pegá la key de console.apify.com/settings/integrations")

    run_input = {
        "searchStringsArray": [a.niche],
        "locationQuery": a.city,
        "maxCrawledPlacesPerSearch": a.max,
        "language": "en",
        "skipClosedPlaces": True,
        "maxReviews": 3,
    }
    r = httpx.post(
        f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items",
        params={"token": token, "timeout": 300},
        json=run_input,
        timeout=330,
    )
    r.raise_for_status()
    items = r.json()
    if not items:
        sys.exit("Apify devolvió 0 lugares — eso es un error, no un dato (regla 2). Revisar búsqueda/ciudad.")

    sin_web = [p for p in items if not (p.get("website") or "").strip() and p.get("phone")]
    out_dir = ROOT / "leads"
    out_dir.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", f"{a.niche}_{a.city}".lower()).strip("-")
    out = out_dir / f"{slug}.csv"
    cols = ["title", "phone", "address", "categoryName", "totalScore", "reviewsCount", "url", "review_1"]
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for p in sorted(sin_web, key=lambda p: -(p.get("reviewsCount") or 0)):
            rev = (p.get("reviews") or [{}])[0].get("text") or ""
            w.writerow([p.get("title"), p.get("phone"), p.get("address"), p.get("categoryName"),
                        p.get("totalScore"), p.get("reviewsCount"), p.get("url"), rev[:300]])
    print(f"{len(items)} lugares crawleados · {len(sin_web)} sin web y con teléfono → {out}")


if __name__ == "__main__":
    main()
