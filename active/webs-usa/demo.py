"""Build a professional bilingual demo website for a real Google Maps business (no website).

Usage:
  .venv/bin/python active/webs-usa/demo.py active/webs-usa/leads/demo_3.json
  .venv/bin/python active/webs-usa/demo.py active/webs-usa/leads/demo_3.json --only Chuy

Input: raw Apify items (compass/crawler-google-places, with reviews + imageUrls) and
leads/curacion.json (per business: display name, owner, hero photo, gallery order,
optional real services list). Each niche has its own skin (type, palette, copy).
Output: active/webs-usa/demos/<slug>/index.html. Local only: nothing is published or sent.
"""
import argparse, html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Service-area businesses on Maps often have no address: city from the phone's area code.
AREA = {**dict.fromkeys(["713", "281", "832", "346"], "Houston"),
        **dict.fromkeys(["214", "469", "972", "945", "817"], "Dallas"),
        **dict.fromkeys(["305", "786"], "Miami")}

SKINS = {
    "paint": dict(
        fonts="family=Archivo:wdth,wght@62..125,400..800",
        display="'Archivo', sans-serif", display_style="font-stretch:125%;font-weight:700;letter-spacing:-.02em",
        hero_size="clamp(2.3rem,5vw,4.4rem)", hero_ch="17ch",
        body="'Archivo', sans-serif",
        c=dict(bg="#F3F5F6", ink="#15212B", muted="#5B6670", line="#D6DCE0", accent="#B8893E", deep="#15212B", on_deep="#F3F5F6"),
        hero_en="Painting and remodeling in {city}, finished the way it was promised.",
        hero_es="Pintura y remodelación en {city}, terminada como se prometió.",
        sub_en="Interior and exterior painting, bathrooms, drywall and carpentry. Free estimates. Se habla español.",
        sub_es="Pintura interior y exterior, baños, durlock y carpintería. Presupuesto sin cargo. We speak English.",
        services=[("Interior painting", "Pintura interior", "Walls, ceilings, trim and cabinets, with clean lines and full protection of your floors.", "Paredes, techos, molduras y muebles, con terminaciones prolijas y pisos protegidos."),
                  ("Exterior painting", "Pintura exterior", "Siding, brick, fences and decks, prepped and sealed for the Texas weather.", "Revestimientos, ladrillo, cercos y decks, preparados y sellados para el clima de Texas."),
                  ("Bathroom remodeling", "Remodelación de baños", "From a new vanity to a full gut-and-rebuild, tile included.", "Desde un vanitory nuevo hasta rehacer el baño completo, con cerámica incluida."),
                  ("Drywall and repairs", "Durlock y arreglos", "Water damage, holes and ceilings repaired so you can't tell where.", "Daños por agua, agujeros y techos arreglados sin que se note dónde."),
                  ("Carpentry and rotten wood", "Carpintería y madera podrida", "Replacement of rotten wood, trim and custom built-ins.", "Cambio de madera podrida, molduras y muebles a medida.")],
        steps_en=["Call or send a WhatsApp with a few photos.", "{owner} visits and gives you a written estimate, free.", "We do the work on the agreed date and leave the house clean."],
        steps_es=["Llamá o mandá un WhatsApp con unas fotos.", "{owner} va a tu casa y te da un presupuesto por escrito, sin cargo.", "Hacemos el trabajo en la fecha acordada y dejamos la casa limpia."],
    ),
    "detail": dict(
        fonts="family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600",
        display="'Barlow Condensed', sans-serif", display_style="font-weight:800;letter-spacing:-.01em;text-transform:uppercase",
        body="'Barlow', sans-serif",
        c=dict(bg="#000000", ink="#FFFFFF", muted="#A3A9AF", line="#2A2D31", accent="#6CC8FF", deep="#16181B", on_deep="#FFFFFF"),
        hero_en="Showroom finish, in your driveway.",
        hero_es="Terminación de concesionaria, en la puerta de tu casa.",
        sub_en="Mobile car detailing in {city}. We bring the water, the power and the products. Se habla español.",
        sub_es="Detailing a domicilio en {city}. Llevamos el agua, la electricidad y los productos. We speak English.",
        services=[("Full detail", "Detailing completo", "Inside and out: foam wash, clay, wax, vacuum, steam and glass.", "Por dentro y por fuera: lavado con espuma, clay, cera, aspirado, vapor y vidrios."),
                  ("Interior deep clean", "Limpieza interior profunda", "Seats, carpets and headliner shampooed; stains and odors out.", "Tapizados, alfombras y techo lavados; manchas y olores afuera."),
                  ("Exterior wash and wax", "Lavado y encerado", "Hand wash, decontamination and a protective wax coat.", "Lavado a mano, descontaminado y una capa de cera protectora."),
                  ("Trucks and SUVs", "Camionetas y SUVs", "Big vehicles welcome, with no surprise fees for size.", "Vehículos grandes bienvenidos, sin recargos sorpresa por tamaño.")],
        steps_en=["Send a WhatsApp with your car and address.", "{owner} confirms the price and a time that works for you.", "We detail it at your home or office. You don't move."],
        steps_es=["Mandá un WhatsApp con tu auto y la dirección.", "{owner} te confirma el precio y un horario que te sirva.", "Lo hacemos en tu casa u oficina. Vos no te movés."],
    ),
    "landscap": dict(
        fonts="family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Figtree:wght@400;500;600",
        display="'Bricolage Grotesque', sans-serif", display_style="font-weight:700;letter-spacing:-.025em",
        body="'Figtree', sans-serif",
        c=dict(bg="#F1F5EE", ink="#14301F", muted="#52645A", line="#D3DECF", accent="#4C8C3A", deep="#14301F", on_deep="#F1F5EE"),
        hero_en="A yard you're proud to come home to.",
        hero_es="Un jardín que da gusto ver al volver a casa.",
        sub_en="Lawn care, landscaping and tree work in {city}. Free estimates. Se habla español.",
        sub_es="Mantenimiento, paisajismo y poda en {city}. Presupuesto sin cargo. We speak English.",
        services=[("Lawn mowing", "Corte de pasto", "", ""), ("Landscaping", "Paisajismo", "", ""), ("Tree trimming", "Poda", "", "")],
        steps_en=["Call or text {owner} anytime.", "We come by for a free quote, usually within a day.", "Your yard gets done, and stays done."],
        steps_es=["Llamá o escribile a {owner} cuando quieras.", "Pasamos a darte un presupuesto sin cargo, en general en el día.", "Tu jardín queda impecable, y se mantiene así."],
    ),
}
SKIN_FOR = {"paint": "paint", "remodel": "paint", "detail": "detail", "landscap": "landscap", "lawn": "landscap"}
DAYS_ES = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves",
           "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}


def e(s):
    return html.escape(str(s or ""), quote=True)


def cut(t, n=280):
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def bi(en, es, tag="span"):
    return f'<{tag} lang="en">{e(en)}</{tag}><{tag} lang="es">{e(es)}</{tag}>'


def skin_for(p):
    key = f"{p.get('categoryName','')} {' '.join(p.get('categories') or [])} {p.get('title','')}".lower()
    for k, v in SKIN_FOR.items():
        if k in key:
            return SKINS[v]
    raise SystemExit(f"Sin estética para {p.get('title')!r} ({p.get('categoryName')}): agregala a SKINS")


def img(u, w):
    return re.sub(r"=w\d+-h\d+", f"=w{w}-h{int(w * .75)}", u)


def build(p, cur):
    k = skin_for(p)
    c = k["c"]
    name = cur.get("name") or p["title"].rstrip(".")
    owner = cur.get("owner") or "our team"
    phone = p.get("phone") or ""
    d10 = re.sub(r"\D", "", phone)[-10:]
    city = p.get("city") or AREA.get(d10[:3])
    if not city:
        raise SystemExit(f"{name}: sin ciudad ni código de área conocido ({phone}): agregalo a AREA")
    wa = f"https://wa.me/1{d10}"
    rating, nrev = f'{float(p.get("totalScore") or 0):.1f}', p.get("reviewsCount") or 0
    maps = p.get("url") or ""
    photos = p.get("imageUrls") or []
    hero = img(photos[cur.get("hero", 0)], 2000)
    gallery = [img(photos[i], 1200) for i in cur.get("gallery", range(1, 6)) if i < len(photos)]
    side = img(photos[cur["side"]], 1200) if cur.get("side") is not None else ""
    if not gallery:
        raise SystemExit(f"{name}: sin fotos para la galería")
    reviews = [r for r in (p.get("reviews") or []) if len((r.get("text") or "").strip()) > 40][:3]
    if len(reviews) < 2:
        raise SystemExit(f"{name}: menos de 2 reseñas con texto: no alcanza para la demo")
    services = [(s[0], s[1], "", "") for s in cur["services"]] if cur.get("services") else k["services"]
    hours = p.get("openingHours") or []
    tag_en = cur.get("tagline_en") or k["hero_en"].format(city=city)
    tag_es = cur.get("tagline_es") or k["hero_es"].format(city=city)
    area_en, area_es = cur.get("area_en", city), cur.get("area_es", city)

    svc_html = "".join(
        f'<li><h3>{bi(a, b)}</h3>' + (f'<p>{bi(da, db)}</p>' if da else "") + "</li>"
        for a, b, da, db in services)
    gal_html = "".join(f'<figure class="g{i}"><img src="{e(u)}" alt="" loading="lazy"></figure>' for i, u in enumerate(gallery))
    best, rest = reviews[0], reviews[1:]
    rev_html = "".join(
        f'<blockquote><p>{e(cut(r["text"], 240))}</p><footer>{e((r.get("name") or "").split(" ")[0])} <span class="st">{"★" * int(r.get("stars") or 5)}</span></footer></blockquote>'
        for r in rest)
    steps_html = "".join(f"<li>{bi(a.format(owner=owner), b.format(owner=owner))}</li>" for a, b in zip(k["steps_en"], k["steps_es"]))
    hours_html = "".join(
        f'<tr><th>{bi(h["day"], DAYS_ES.get(h["day"], h["day"]))}</th><td>{e(h["hours"].replace(chr(8239), " ").replace(" to ", "–"))}</td></tr>'
        for h in hours)
    opts = "".join(f'<option value="{e(a)}">{e(a)} / {e(b)}</option>' for a, b, *_ in services)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{e(name)} · {e(city)}</title>
<meta name="description" content="{e(k['sub_en'].format(city=city))}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{k['fonts']}&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{e(hero)}">
<style>
:root{{--bg:{c['bg']};--ink:{c['ink']};--muted:{c['muted']};--line:{c['line']};--accent:{c['accent']};--deep:{c['deep']};--on-deep:{c['on_deep']};--wa:#1FAF54;
  --display:{k['display']};--body:{k['body']};--pad:clamp(16px,5vw,64px);--max:1240px}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--body);background:var(--bg);color:var(--ink);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}}
img{{display:block;width:100%;height:100%;object-fit:cover}}
a{{color:inherit}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
html.lang-es body [lang=en],html:not(.lang-es) body [lang=es]{{display:none}}
.wrap{{max-width:var(--max);margin:0 auto;padding:0 var(--pad)}}
.disp{{font-family:var(--display);{k['display_style']};line-height:1.02}}

header{{position:fixed;inset:0 0 auto;z-index:20;transition:background .3s,border-color .3s;border-bottom:1px solid transparent;color:#fff}}
header.solid{{background:var(--bg);color:var(--ink);border-color:var(--line)}}
header .wrap{{display:flex;align-items:center;gap:20px;height:72px}}
.brand{{font-family:var(--display);{k['display_style']};font-size:1.25rem;text-decoration:none;margin-right:auto;line-height:1}}
.lang{{background:none;border:0;color:inherit;font:inherit;font-size:.9rem;cursor:pointer;opacity:.85;padding:8px}}
.hcall{{text-decoration:none;font-weight:600;font-size:.95rem;border:1px solid currentColor;border-radius:999px;padding:9px 18px}}

.hero{{position:relative;min-height:100svh;display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:#111}}
.hero img{{position:absolute;inset:0;animation:settle 1.8s cubic-bezier(.2,.7,.2,1) both}}
.hero::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,0) 28%,rgba(0,0,0,.1) 50%,rgba(0,0,0,.78) 100%)}}
.hero .wrap{{position:relative;z-index:1;width:100%;padding-bottom:clamp(40px,8vh,88px)}}
.hero h1{{font-size:{k.get('hero_size','clamp(2.6rem,7.4vw,6.4rem)')};max-width:{k.get('hero_ch','13ch')};animation:rise 1s .25s cubic-bezier(.2,.7,.2,1) both}}
.hero p{{max-width:46ch;font-size:clamp(1.02rem,1.6vw,1.2rem);margin-top:20px;opacity:.92;animation:rise 1s .4s cubic-bezier(.2,.7,.2,1) both}}
.rate{{display:inline-flex;align-items:center;gap:10px;font-size:.95rem;text-decoration:none;margin-bottom:22px;animation:rise 1s .1s both}}
.rate .st{{color:#FFC542;letter-spacing:1px}}
.ctas{{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px;animation:rise 1s .55s both}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:16px 26px;border-radius:999px;font-weight:600;text-decoration:none;font-size:1rem;border:0;cursor:pointer;font-family:var(--body)}}
.btn-main{{background:var(--accent);color:{'#000' if c['bg'] == '#000000' else '#fff'}}}
.btn-wa{{background:var(--wa);color:#fff}}
.btn svg{{width:18px;height:18px;flex:none}}
@keyframes settle{{from{{transform:scale(1.08)}}to{{transform:none}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}

section{{padding:clamp(72px,11vw,140px) 0}}
h2{{font-size:clamp(2rem,4.4vw,3.6rem);max-width:18ch}}
.lede{{color:var(--muted);max-width:52ch;margin-top:18px;font-size:1.08rem}}

.intro .wrap{{display:grid;grid-template-columns:1.35fr 1fr;gap:clamp(32px,6vw,96px);align-items:start}}
.intro blockquote p{{font-family:var(--display);font-size:clamp(1.5rem,2.8vw,2.3rem);line-height:1.22;{k['display_style'].replace('text-transform:uppercase','')}}}
.intro blockquote footer{{margin-top:20px;color:var(--muted)}}
.facts{{border-top:1px solid var(--line)}}
.facts div{{display:flex;justify-content:space-between;gap:16px;padding:16px 0;border-bottom:1px solid var(--line)}}
.facts dt{{color:var(--muted)}}
.facts dd{{font-weight:600;text-align:right}}

.svc{{background:var(--deep);color:var(--on-deep)}}
.svc .wrap{{display:grid;grid-template-columns:1fr 1.25fr;gap:clamp(32px,6vw,96px)}}
.svc .side{{position:sticky;top:110px;align-self:start}}
.svc .side figure{{margin-top:40px;aspect-ratio:4/5;border-radius:4px;overflow:hidden}}
.svc ul{{list-style:none;border-top:1px solid color-mix(in srgb,var(--on-deep) 22%,transparent)}}
.svc li{{padding:26px 0;border-bottom:1px solid color-mix(in srgb,var(--on-deep) 22%,transparent)}}
.svc h3{{font-family:var(--display);font-size:clamp(1.3rem,2.2vw,1.75rem);{k['display_style']};line-height:1.15}}
.svc li p{{color:color-mix(in srgb,var(--on-deep) 70%,transparent);margin-top:8px;max-width:52ch}}

.gal{{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:clamp(150px,19vw,250px);gap:12px;margin-top:48px}}
.gal figure{{overflow:hidden;border-radius:4px;grid-column:span 2}}
.gal .g0{{grid-column:span 4;grid-row:span 2}}
.n4 .g1,.n5 .g1{{grid-row:span 2}}
.n4 .g2,.n4 .g3{{grid-column:span 3}}
.n2 figure{{grid-column:span 3!important;grid-row:span 2}}
.n1 figure{{grid-column:span 6!important;grid-row:span 2}}

.rev .wrap>div{{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(24px,4vw,56px);margin-top:48px}}
.rev blockquote{{border-top:2px solid var(--ink);padding-top:22px}}
.rev blockquote p{{font-size:1.08rem}}
.rev footer{{margin-top:16px;font-weight:600;display:flex;gap:10px;align-items:center}}
.rev .st,.intro .st{{color:var(--accent);letter-spacing:1px}}
.more{{display:inline-block;margin-top:40px;font-weight:600;text-underline-offset:4px}}

.how ol{{list-style:none;counter-reset:s;display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(20px,3vw,40px);margin-top:48px}}
.how li{{counter-increment:s;padding-top:20px;border-top:1px solid var(--line);font-size:1.1rem;max-width:30ch}}
.how li::before{{content:counter(s);display:block;font-family:var(--display);font-size:3rem;line-height:1;color:var(--accent);margin-bottom:14px;{k['display_style']}}}

.contact{{background:var(--deep);color:var(--on-deep)}}
.contact .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(32px,6vw,96px)}}
.contact h2{{color:var(--on-deep)}}
form{{display:grid;gap:14px}}
label{{display:grid;gap:6px;font-size:.92rem;color:color-mix(in srgb,var(--on-deep) 75%,transparent)}}
input,select,textarea{{font:inherit;font-size:1rem;color:var(--on-deep);background:transparent;border:0;border-bottom:1px solid color-mix(in srgb,var(--on-deep) 35%,transparent);padding:10px 0;border-radius:0}}
select option{{color:#000}}
input:focus,select:focus,textarea:focus{{outline:none;border-color:var(--accent)}}
form .btn{{margin-top:12px;justify-self:start}}
table{{border-collapse:collapse;margin-top:28px;width:100%;max-width:360px}}
th,td{{text-align:left;padding:7px 0;font-weight:400;border-bottom:1px solid color-mix(in srgb,var(--on-deep) 15%,transparent)}}
td{{text-align:right}}
.contact .tel{{font-family:var(--display);font-size:clamp(1.8rem,3.6vw,2.8rem);text-decoration:none;display:inline-block;margin-top:24px;{k['display_style']}}}

footer.site{{padding:36px 0 110px;color:var(--muted);font-size:.9rem}}
footer.site .wrap{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}}
.bar{{display:none}}

@media (max-width:860px){{
  .hcall{{display:none}}
  .intro .wrap,.svc .wrap,.contact .wrap{{grid-template-columns:1fr}}
  .svc .side{{position:static}} .svc .side figure{{display:none}}
  .gal{{grid-template-columns:repeat(2,1fr);grid-auto-rows:42vw}}
  .gal figure{{grid-column:auto!important;grid-row:auto!important}}
  .gal .g0,.n2 .g1,.n4 .g3{{grid-column:span 2!important}}
  .hero .ctas{{display:none}}
  .rev .wrap>div,.how ol{{grid-template-columns:1fr}}
  .bar{{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:fixed;inset:auto 0 0;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:var(--bg);border-top:1px solid var(--line);z-index:30}}
  .bar .btn{{padding:14px 10px}}
}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}html{{scroll-behavior:auto}}}}
</style>
</head>
<body>
<header id="top"><div class="wrap">
  <a class="brand" href="#">{e(name)}</a>
  <button class="lang" type="button" onclick="document.documentElement.classList.toggle('lang-es')">{bi('Español', 'English')}</button>
  <a class="hcall" href="tel:+1{d10}">{e(phone)}</a>
</div></header>

<main>
<section class="hero" style="padding:0">
  <img src="{e(hero)}" alt="{e(name)}" fetchpriority="high">
  <div class="wrap">
    <a class="rate" href="{e(maps)}" target="_blank" rel="noopener"><span class="st">★★★★★</span>{bi(f'{rating} on Google, {nrev} reviews', f'{str(rating).replace(".", ",")} en Google, {nrev} reseñas')}</a>
    <h1 class="disp">{bi(tag_en, tag_es)}</h1>
    <p>{bi(k['sub_en'].format(city=city), k['sub_es'].format(city=city))}</p>
    <div class="ctas">
      <a class="btn btn-main" href="tel:+1{d10}">{PHONE_SVG}{bi(f'Call {phone}', f'Llamar al {phone}')}</a>
      <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a>
    </div>
  </div>
</section>

<section class="intro"><div class="wrap">
  <blockquote><p>“{e(cut(best['text'], 230))}”</p><footer>{e((best.get('name') or '').split(' ')[0])}, {bi('Google review', 'reseña en Google')} <span class="st">★★★★★</span></footer></blockquote>
  <dl class="facts">
    <div><dt>{bi('Rating', 'Calificación')}</dt><dd>{rating} ★ ({nrev})</dd></div>
    <div><dt>{bi('Area', 'Zona')}</dt><dd>{bi(area_en, area_es)}</dd></div>
    <div><dt>{bi('Estimates', 'Presupuesto')}</dt><dd>{bi('Free', 'Sin cargo')}</dd></div>
    <div><dt>{bi('Language', 'Idioma')}</dt><dd>English · Español</dd></div>
  </dl>
</div></section>

<section class="svc"><div class="wrap">
  <div class="side">
    <h2 class="disp">{bi('What we do', 'Lo que hacemos')}</h2>
    {f'<figure><img src="{e(side)}" alt="" loading="lazy"></figure>' if side else ''}
  </div>
  <ul>{svc_html}</ul>
</div></section>

<section class="work"><div class="wrap">
  <h2 class="disp">{bi('Recent work', 'Trabajos recientes')}</h2>
  <p class="lede">{bi(f'Real jobs by {name} in {city}.', f'Trabajos reales de {name} en {city}.')}</p>
  <div class="gal n{len(gallery)}">{gal_html}</div>
</div></section>

<section class="rev" style="padding-top:0"><div class="wrap">
  <h2 class="disp">{bi('What customers say', 'Lo que dicen los clientes')}</h2>
  <div>{rev_html}</div>
  <a class="more" href="{e(maps)}" target="_blank" rel="noopener">{bi(f'Read all {nrev} reviews on Google', f'Ver las {nrev} reseñas en Google')}</a>
</div></section>

<section class="how" style="padding-top:0"><div class="wrap">
  <h2 class="disp">{bi('How it works', 'Cómo trabajamos')}</h2>
  <ol>{steps_html}</ol>
</div></section>

<section class="contact" id="contact"><div class="wrap">
  <div>
    <h2 class="disp">{bi('Get your free estimate', 'Pedí tu presupuesto sin cargo')}</h2>
    <a class="tel" href="tel:+1{d10}">{e(phone)}</a>
    <table>{hours_html}</table>
  </div>
  <form id="f">
    <label>{bi('Your name', 'Tu nombre')}<input name="n" required autocomplete="name"></label>
    <label>{bi('Service', 'Servicio')}<select name="s">{opts}</select></label>
    <label>{bi('Address or area', 'Dirección o zona')}<input name="a" autocomplete="street-address"></label>
    <label>{bi('Details', 'Detalles')}<textarea name="d" rows="3"></textarea></label>
    <button class="btn btn-wa" type="submit">{WA_SVG}{bi('Send on WhatsApp', 'Enviar por WhatsApp')}</button>
  </form>
</div></section>
</main>

<footer class="site"><div class="wrap">
  <span>{e(name)}, {e(city)}</span><span>{e(phone)}</span>
</div></footer>

<nav class="bar">
  <a class="btn btn-main" href="tel:+1{d10}">{PHONE_SVG}{bi('Call', 'Llamar')}</a>
  <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a>
</nav>
<script>
const h=document.getElementById('top'),hero=document.querySelector('.hero');
const on=()=>h.classList.toggle('solid',scrollY>hero.offsetHeight-80);addEventListener('scroll',on,{{passive:true}});on();
if((navigator.language||'').startsWith('es'))document.documentElement.classList.add('lang-es');
document.getElementById('f').addEventListener('submit',ev=>{{ev.preventDefault();const f=ev.target;
  const t=`Hi! I'm ${{f.n.value}}. I'd like a free estimate for: ${{f.s.value}}.`+(f.a.value?` Area: ${{f.a.value}}.`:'')+(f.d.value?` ${{f.d.value}}`:'');
  open('{wa}?text='+encodeURIComponent(t),'_blank','noopener');}});
</script>
</body>
</html>
"""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    out = ROOT / "demos" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return out, len(reviews), len(gallery)


PHONE_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.7 1.2 1.6 2 1.1 1 2 1.3 2.3 1.4.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg>'


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--only")
    a = ap.parse_args()
    items = json.load(open(a.json))
    curacion = json.load(open(ROOT / "leads" / "curacion.json"))
    for p in items:
        if a.only and a.only.lower() not in p["title"].lower():
            continue
        out, nr, ng = build(p, curacion.get(p["title"], {}))
        print(f"{p['title']}: {nr} reseñas, {ng} fotos → {out}")
