#!/usr/bin/env python3
"""Genereert de statische site presseggersee.nl in 5 talen naar ./dist"""
import json, os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
BOOK = "https://app.bookingexperts.com/{code}/ra/2550/170233/yPRubT8wL8fEWsHmhLcCUjPLvu7WBb44R3rdTbEs"
SITE = "https://presseggersee.nl"
INDEXABLE = True  # False = noindex (niet in Google)

LANGS = json.load(open(os.path.join(ROOT, "content.json"), encoding="utf-8"))
ORDER = ["nl", "de", "en", "it", "pl"]

def path_of(code):
    return "/" if code == "nl" else f"/{code}/"

def e(s):
    return html.escape(s, quote=False)

def photo(t, key, label, cls="photo"):
    src = t.get("photos", {}).get(key)
    img = f'<img src="{src}" alt="{e(label)}" loading="lazy">' if src else f'[FOTO: {e(label)}]'
    return f'<div class="{cls}">{img}</div>'

def page(code):
    t = LANGS[code]
    book = BOOK.format(code=t["book_code"])
    langs = "".join(
        (f'<span aria-current="page">{c.upper()}</span>' if c == code
         else f'<a href="{path_of(c)}" lang="{c}" hreflang="{c}">{c.upper()}</a>')
        for c in ORDER)
    alt = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{SITE}{path_of(c)}">' for c in ORDER)
    alt += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/en/">'
    robots = "index,follow" if INDEXABLE else "noindex,nofollow"
    why = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in t["why"])
    acts = json.dumps({"spring": t["spring"], "autumn": t["autumn"]}, ensure_ascii=False)
    first = "".join(
        f'<div class="act"><p class="when">{e(w)}</p><div class="what"><h3>{e(h)}</h3><p class="muted">{e(p)}</p></div></div>'
        for w, h, p in t["spring"])
    chips = "".join(f"<span>{e(c)}</span>" for c in t["chips"])
    park = "".join(f"<span>{e(c)}</span>" for c in t["park"])
    facts = "".join(f"<span>✓ {e(f)}</span>" for f in t["facts"])
    f = t["form"]
    gal = "".join(f'<figure><img src="{src}" alt="{e(cap)}" loading="lazy" width="920" height="515"><figcaption>{e(cap)}</figcaption></figure>' for src, cap in t.get("gallery", []))
    nature = "".join(f'<figure><img src="{src}" alt="{e(cap)}" loading="lazy" width="1200" height="675"><figcaption>{e(cap)}</figcaption></figure>' for src, cap in t.get("nature", []))
    kids = ""
    for i, (age, title, items) in enumerate(t["kids"]):
        lis = "".join(f'<li><strong>{e(n)}</strong><span>{e(d)}</span></li>' for n, d in items)
        kids += f'<div class="kid kid{i}"><p class="age">{e(age)}</p><h3>{e(title)}</h3><ul>{lis}</ul></div>'
    kidpics = "".join(f'<figure><img src="{src}" alt="{e(cap)}" loading="lazy" width="1000" height="563"><figcaption>{e(cap)}</figcaption></figure>' for src, cap in t["kidpics"])
    ridge = '<svg class="ridge" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70V48l110-30 90 22 130-36 110 32 120-24 100 30 140-38 120 34 110-20 130 28 90-14 100 22v26z" fill="#16302E"/></svg>'
    tips = ""
    for cat, items in t["cats"]:
        cards = ""
        for name, place, text, url in items:
            link = f'<a href="{url}" rel="noopener" target="_blank">{e(t["more"])} ↗</a>' if url else ""
            cards += f'<div class="tip"><p class="place">{e(place)}</p><h4>{e(name)}</h4><p class="muted">{e(text)}</p>{link}</div>'
        tips += f'<h3 class="tipcat">{e(cat)}</h3><div class="tips">{cards}</div>'

    return f"""<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{html.escape(t['meta'])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{SITE}{path_of(code)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(t['title'])}">
<meta property="og:description" content="{html.escape(t['meta'])}">
<meta property="og:image" content="{SITE}/img/hero.jpg">
<meta property="og:url" content="{SITE}{path_of(code)}">
<meta property="og:locale" content="{t['og_locale']}">
{alt}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="{path_of(code)}">presseggersee<span>.nl</span></a>
<nav class="menu" aria-label="{e(t['nav_label'])}">
<a href="#huis">{e(t['nav'][0])}</a><a href="#kids">{e(t['nav'][1])}</a><a href="#omgeving">{e(t['nav'][2])}</a><a href="#tips">{e(t['nav_tips'])}</a><a href="#boeken">{e(t['nav'][3])}</a>
</nav>
<div class="right"><div class="langs">{langs}</div>
<a class="btn btn-accent btn-head" href="{book}" rel="noopener">{e(t['cta_avail'])}</a></div>
</div></header>
<main>
<div class="wrap hero">
<div class="txt">
<p class="eyebrow">{e(t['eyebrow'])}</p>
<h1>{e(t['h1'])}</h1>
<p class="lead muted">{e(t['lead'])}</p>
<div class="row"><a class="btn btn-accent" href="{book}" rel="noopener">{e(t['cta_dates'])}</a><a class="btn btn-line" href="#huis">{e(t['cta_house'])}</a></div>
<div class="facts">{facts}</div>
</div>
<div class="heropic">{photo(t, 'hero', t['ph_hero'])}<span class="sticker">{e(t['sticker'])}</span><img class="inset" src="/img/family-walk.jpg" alt="{e(t['ph_family'])}" width="1000" height="563"></div>
</div>

{ridge}
<section id="seizoen" class="dark"><div class="wrap">
<div class="head"><p class="eyebrow">{e(t['why_eyebrow'])}</p><h2>{e(t['why_h2'])}</h2></div>
<div class="cards">{why}</div>
</div></section>

<section id="kids"><div class="wrap">
<div class="head"><p class="eyebrow">{e(t['kids_eyebrow'])}</p><h2>{e(t['kids_h2'])}</h2><p class="muted" style="font-size:18px">{e(t['kids_intro'])}</p></div>
<div class="kids">{kids}</div>
<div class="morepics kidpics">{kidpics}</div>
<p class="small">{e(t['kids_note'])}</p>
</div></section>

<section id="huis" class="white"><div class="wrap">
<div class="head"><p class="eyebrow">{e(t['house_eyebrow'])}</p><h2>Panorama Lodge</h2><p class="muted" style="font-size:18px">{e(t['house_text'])}</p></div>
<div class="gallery">{photo(t,'living',t['ph_living'],'photo big')}<div class="col">{photo(t,'kitchen',t['ph_kitchen'])}{photo(t,'terrace',t['ph_terrace'])}</div></div>
<div class="morepics">{gal}</div>
<div class="chips">{chips}</div>
<h3 style="font-size:22px;margin:40px 0 16px">{e(t['park_h3'])}</h3>
<div class="chips">{park}</div>
</div></section>

<section id="omgeving"><div class="wrap">
<div class="split"><div class="head" style="margin:0"><p class="eyebrow">{e(t['todo_eyebrow'])}</p><h2>{e(t['todo_h2'])}</h2></div>
<div class="toggle" role="group" aria-label="{e(t['toggle_label'])}">
<button type="button" data-s="spring" aria-pressed="true">{e(t['spring_label'])}</button>
<button type="button" data-s="autumn" aria-pressed="false">{e(t['autumn_label'])}</button>
</div></div>
<div class="morepics nature">{nature}</div>
<div id="acts" aria-live="polite">{first}</div>
<p class="small" style="margin-top:20px">{e(t['todo_note'])}</p>
</div></section>

<section id="tips" class="white"><div class="wrap">
<div class="head"><p class="eyebrow">{e(t['tips_eyebrow'])}</p><h2>{e(t['tips_h2'])}</h2><p class="muted" style="font-size:18px">{e(t['tips_intro'])}</p></div>
{tips}
</div></section>

<section id="boeken"><div class="wrap book">
<div class="txt">
<p class="eyebrow">{e(t['book_eyebrow'])}</p>
<h2>{e(t['book_h2'])}</h2>
<p class="muted" style="font-size:17px">{e(t['book_text'])}</p>
<a class="btn btn-accent" href="{book}" rel="noopener">{e(t['cta_book'])}</a>
<p style="margin-top:16px;font-weight:600">{e(t['addr_label'])}</p>
<p class="muted">EuroParcs Pressegger See · Presseggen 29, 9620 Presseggen, {e(t["country"])}</p>
</div>
<form class="req" name="aanvraag" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="{path_of(code)}{t['thanks_slug']}">
<input type="hidden" name="taal" value="{code}">
<input type="hidden" name="subject" value="Aanvraag presseggersee.nl ({code.upper()})">
<p class="hp"><label>Leave empty <input name="bot-field"></label></p>
<h3>{e(f['h3'])}</h3>
<label>{e(f['name'])}<input type="text" name="naam" required autocomplete="name"></label>
<label>{e(f['email'])}<input type="email" name="email" required autocomplete="email"></label>
<div class="row" style="gap:12px">
<label>{e(f['arrive'])}<input type="date" name="aankomst"></label>
<label>{e(f['leave'])}<input type="date" name="vertrek"></label>
<label style="flex-basis:100px">{e(f['guests'])}<input type="number" name="personen" min="1" max="6"></label>
</div>
<label>{e(f['msg'])}<textarea name="bericht" rows="3"></textarea></label>
<button type="submit">{e(f['send'])}</button>
<p class="small">{e(f['privacy'])}</p>
</form>
</div></section>
</main>
<div class="bookbar"><span>{e(t['bar_text'])}</span><a class="btn btn-accent" href="{book}" rel="noopener">{e(t['cta_avail'])}</a></div>
<footer><div class="wrap"><p>© 2026 presseggersee.nl · {e(t['footer'])}</p><div class="links"><span>{e(t['social'])}:</span><a href="https://www.instagram.com/presseggersee310/" rel="noopener">Instagram</a><a href="https://www.facebook.com/people/Pressegger-See/100095342058628/" rel="noopener">Facebook</a><div class="langs">{langs}</div></div></div></footer>
<script>
(function(){{var d={acts};var box=document.getElementById('acts');
function esc(s){{var x=document.createElement('div');x.textContent=s;return x.innerHTML}}
document.querySelectorAll('.toggle button').forEach(function(b){{b.addEventListener('click',function(){{
document.querySelectorAll('.toggle button').forEach(function(o){{o.setAttribute('aria-pressed',o===b)}});
box.innerHTML=d[b.dataset.s].map(function(a){{return '<div class="act"><p class="when">'+esc(a[0])+'</p><div class="what"><h3>'+esc(a[1])+'</h3><p class="muted">'+esc(a[2])+'</p></div></div>'}}).join('');
}})}});
if(new Date().getMonth()>=6){{document.querySelector('.toggle button[data-s=autumn]').click()}}
}})();
</script>
</body>
</html>
"""

def thanks(code):
    t = LANGS[code]
    return f"""<!doctype html>
<html lang="{code}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['thanks_h'])} · presseggersee.nl</title><meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css"></head>
<body><main class="wrap thanks"><a class="logo" href="{path_of(code)}">presseggersee<span>.nl</span></a>
<h1 style="font-size:44px">{e(t['thanks_h'])}</h1><p class="muted" style="font-size:18px">{e(t['thanks_p'])}</p>
<a class="btn btn-dark" href="{path_of(code)}">{e(t['thanks_back'])}</a></main></body></html>
"""

if __name__ == "__main__":
    shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(DIST)
    shutil.copy(os.path.join(ROOT, "src", "style.css"), DIST)
    shutil.copy(os.path.join(ROOT, "src", "favicon.svg"), DIST)
    if os.path.isdir(os.path.join(ROOT, "src", "img")):
        shutil.copytree(os.path.join(ROOT, "src", "img"), os.path.join(DIST, "img"))
    for c in ORDER:
        d = DIST if c == "nl" else os.path.join(DIST, c)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(c))
        os.makedirs(os.path.join(d, LANGS[c]["thanks_slug"]), exist_ok=True)
        open(os.path.join(d, LANGS[c]["thanks_slug"], "index.html"), "w", encoding="utf-8").write(thanks(c))
    robots = "User-agent: *\nAllow: /\nSitemap: https://presseggersee.nl/sitemap.xml\n" if INDEXABLE else "User-agent: *\nDisallow: /\n"
    open(os.path.join(DIST, "robots.txt"), "w").write(robots)
    redirects = """# Oude WordPress-adressen
/over-ons/*            /#seizoen   301
/familie/*             /#kids      301
/het-vakantiehuis/*    /#huis      301
/omgeving/*            /#omgeving  301
/ervaringen/*          /           301
/tips/*                /#tips      301
/contact/*             /#boeken    301
/boeking/*             /#boeken    301
/2025/12/16/verplicht-mee-in-de-auto/*      /#tips  301
/2025/12/03/gasthof-waldemar/*              /#tips  301
/2025/12/03/wintersport-millenium-express/* /#tips  301
/2023/05/02/hello-world-3/*                 /#tips  301
/wp-admin/*            /           301
/wp-login.php          /           301
/feed/*                /           301
"""
    open(os.path.join(DIST, "_redirects"), "w").write(redirects)
    sm = "".join(f"<url><loc>{SITE}{path_of(c)}</loc></url>" for c in ORDER)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    print("ok")
