"""Build a bilingual demo website for a real Google Maps business (no website).

Usage:
  .venv/bin/python active/webs-usa/demo.py leads/demo_3.json            # all places in the file
  .venv/bin/python active/webs-usa/demo.py leads/demo_3.json --only Chuy

Input: raw Apify items (compass/crawler-google-places, with reviews + imageUrls).
Output: active/webs-usa/demos/<slug>/index.html (gitignored: real third-party data).
Local only: nothing is published or sent.
"""
import argparse, html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = (ROOT / "demo" / "index.html").read_text()

NICHES = {
    "landscap": dict(color=("#1f5133", "#2e7a4c"),
        hero_en="Beautiful yards in {city}, done right and on time.",
        hero_es="Jardines impecables en {city}, bien hechos y a tiempo.",
        services=[("Lawn mowing", "Corte de pasto"), ("Landscaping", "Paisajismo"),
                  ("Tree trimming", "Poda de árboles"), ("Yard cleanup", "Limpieza de jardín")]),
    "lawn": "landscap",
    "detail": dict(color=("#14213d", "#274c77"),
        hero_en="Mobile car detailing in {city} — we come to you.",
        hero_es="Detailing de autos a domicilio en {city} — vamos a donde estés.",
        services=[("Interior detail", "Limpieza interior"), ("Exterior wash & wax", "Lavado y encerado"),
                  ("Paint correction", "Corrección de pintura"), ("Trucks & SUVs", "Camionetas y SUVs")]),
    "paint": dict(color=("#3d2b1f", "#7a5233"),
        hero_en="Painting & remodeling in {city}, finished on time.",
        hero_es="Pintura y remodelación en {city}, terminada a tiempo.",
        services=[("Interior & exterior painting", "Pintura interior y exterior"),
                  ("Bathroom remodeling", "Remodelación de baños"),
                  ("Drywall & repairs", "Durlock y arreglos"), ("Carpentry", "Carpintería")]),
    "remodel": "paint",
    "clean": dict(color=("#0b4f6c", "#01baef"),
        hero_en="Spotless homes in {city}. Trusted, insured, on time.",
        hero_es="Casas impecables en {city}. Confiables, con seguro y puntuales.",
        services=[("Regular cleaning", "Limpieza regular"), ("Deep cleaning", "Limpieza profunda"),
                  ("Move-in / move-out", "Mudanzas"), ("Airbnb turnover", "Airbnb")]),
}


# Service-area businesses on Maps often have no address: city from the phone's area code.
AREA = {**dict.fromkeys(["713", "281", "832", "346"], "Houston"),
        **dict.fromkeys(["214", "469", "972", "945", "817"], "Dallas"),
        **dict.fromkeys(["305", "786"], "Miami")}


def niche_for(p):
    key = f"{p.get('categoryName','')} {p.get('title','')}".lower()
    for k, v in NICHES.items():
        if k in key:
            return NICHES[v] if isinstance(v, str) else v
    raise SystemExit(f"Sin rubro para {p.get('title')!r} ({p.get('categoryName')}): agregalo a NICHES")


def cut(t, n=260):
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def e(s):
    return html.escape(str(s or ""), quote=True)


def build(p):
    n = niche_for(p)
    name, phone = p["title"].rstrip("."), p.get("phone") or ""
    digits = "1" + re.sub(r"\D", "", phone)[-10:]
    city = p.get("city") or AREA.get(re.sub(r"\D", "", phone)[-10:][:3])
    if not city:
        raise SystemExit(f"{name}: sin ciudad ni código de área conocido ({phone}): agregalo a AREA")
    reviews = [r for r in (p.get("reviews") or []) if (r.get("text") or "").strip()][:3]
    imgs = (p.get("imageUrls") or [])[:3]
    rating = p.get("totalScore")
    nrev = p.get("reviewsCount") or 0

    s = TEMPLATE
    s = s.replace("#1f5133", n["color"][0]).replace("#2e7a4c", n["color"][1])
    s = s.replace("Martínez Landscaping · Houston, TX", f"{e(name)} · {e(city)}")
    s = s.replace("Martínez Landscaping", e(name))
    s = re.sub(r"<span data-en>Beautiful yards.*?</h1>",
               f"<span data-en>{e(n['hero_en'].format(city=city))}</span><span data-es>{e(n['hero_es'].format(city=city))}</span></h1>",
               s, flags=re.S)
    sub_en = f"{' · '.join(a for a, _ in n['services'])}. Free estimates — se habla español."
    sub_es = f"{' · '.join(b for _, b in n['services'])}. Presupuesto gratis — we speak English."
    s = s.replace("Lawn care, landscaping and tree trimming in Houston, TX. Free estimates. Se habla español.", e(f"{name} in {city}. {sub_en}"))
    s = s.replace("<span data-en>Lawn care, landscaping and tree trimming for homes and businesses. Free estimates — se habla español.</span><span data-es>Corte de pasto, paisajismo y poda para casas y negocios. Presupuesto gratis — we speak English.</span>",
                  f"<span data-en>{e(sub_en)}</span><span data-es>{e(sub_es)}</span>")
    s = s.replace('<span data-fill="city">Houston, TX</span>', f'<span data-fill="city">{e(city)}</span>')
    opts = "".join(f"<option>{e(a)} / {e(b)}</option>" for a, b in n["services"]) + "<option>Other / Otro</option>"
    s = re.sub(r"<select>.*?</select>", lambda m: f"<select>{opts}</select>", s, count=1, flags=re.S)
    s = s.replace("(713) 555-0100", e(phone)).replace("+17135550100", f"+{digits}").replace("17135550100", digits)
    s = s.replace("4.9 on Google", f"{rating} on Google · {nrev} reviews").replace("4,9 en Google", f"{str(rating).replace('.', ',')} en Google · {nrev} reseñas")
    s = s.replace("<span class=\"badge\"><span data-en>Licensed &amp; insured</span><span data-es>Con licencia y seguro</span></span>\n", "")
    cards = "".join(f'<div class="card"><h3><span data-en>{e(a)}</span><span data-es>{e(b)}</span></h3></div>' for a, b in n["services"])
    s = re.sub(r'(<div class="grid" data-fill="services">).*?(\n  </div>\n</div></section>)', lambda m: m[1] + cards + m[2], s, count=1, flags=re.S)
    ph = "".join(f'<div class="ph" style="background:url({e(u)}) center/cover"></div>' for u in imgs)
    s = re.sub(r'(<div class="grid" data-fill="photos">).*?(\n  </div>)', lambda m: m[1] + ph + m[2], s, count=1, flags=re.S)
    rv = "".join(f'<div class="card"><div class="stars">{"★" * int(r.get("stars") or 5)}</div><p>{e(cut(r["text"]))}</p><p style="margin-top:8px;font-weight:600">— {e((r.get("name") or "").split(" ")[0])}</p></div>' for r in reviews)
    s = re.sub(r'(<div class="grid" data-fill="reviews">).*?(\n  </div>)', lambda m: m[1] + rv + m[2], s, count=1, flags=re.S)
    s = s.replace('<ul data-fill="areas"><li>Houston</li><li>Katy</li><li>Sugar Land</li><li>Pasadena</li><li>Pearland</li><li>Spring</li></ul>',
                  f'<ul data-fill="areas"><li>{e(city)}</li></ul>')
    s = s.replace("<span data-en>Mon–Sat 7am–6pm</span><span data-es>Lun a sáb 7 a 18 h</span>", "")
    s = s.replace("<!-- DEMO TEMPLATE", '<meta name="robots" content="noindex"><!-- DEMO')
    # Leftover placeholder check: a demo with template data in it must not go out.
    for bad in ("Martínez", "555-0100", "Foto del cliente", "[Reseña", "Lawn care, landscaping", "Houston, TX", "Corte de pasto, paisajismo y poda", "Tree trimming / Poda</option>"):
        if bad in s:
            raise SystemExit(f"{name}: quedó texto de plantilla ({bad!r})")
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    out = ROOT / "demos" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    return out, len(reviews), len(imgs)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--only")
    a = ap.parse_args()
    items = json.load(open(a.json))
    for p in items:
        if a.only and a.only.lower() not in p["title"].lower():
            continue
        out, nr, ni = build(p)
        print(f"{p['title']}: {nr} reseñas, {ni} fotos → {out}")
