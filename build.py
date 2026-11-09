"""Builds the static website into public/ from content/<lang>.json. Run: python3 build.py"""
import html
import json
import shutil
from urllib.parse import urlsplit
from pathlib import Path

SITE = "https://e1iaas.github.io/medinder-website"  # change to "https://medinder.app" once the domain points here
EMAIL = "eliastestdev@gmail.com"
APP_ID = ""                             # App Store app ID (digits) once the app is live
UPDATED = "2026-11-09"

BASE = urlsplit(SITE).path.rstrip("/")  # "/medinder-website" on GitHub Pages, "" on an own domain
ORIGIN = SITE[: len(SITE) - len(BASE)]

ROOT = Path(__file__).parent
OUT = ROOT / "public"

# page key -> path under the language prefix; order is the sitemap order
PATHS = {
    "home": "",
    "tools": "tools/",
    "dose_calculator": "tools/dose-time-calculator/",
    "schedule_maker": "tools/medication-schedule-maker/",
    "guides": "guides/",
    "guide_remember": "guides/how-to-remember-to-take-medication/",
    "guide_iphone": "guides/medication-reminders-on-iphone/",
    "guide_elderly": "guides/medication-reminders-for-elderly-parents/",
    "support": "support/",
    "privacy": "privacy/",
}
TOOLS = ["dose_calculator", "schedule_maker"]
GUIDES = ["guide_remember", "guide_iphone", "guide_elderly"]
PARENT = {**{k: "tools" for k in TOOLS}, **{k: "guides" for k in GUIDES}}

LANGS = {p.stem: json.loads(p.read_text()) for p in sorted((ROOT / "content").glob("*.json"))}
ORDER = ["en"] + sorted(l for l in LANGS if l != "en")


def prefix(lang):
    return BASE + ("" if lang == "en" else f"/{lang}")


def url(lang, key):
    return f"{ORIGIN}{prefix(lang)}/{PATHS[key]}"


def fill(text, lang):
    return text.replace("{L}", prefix(lang)).replace("{EMAIL}", EMAIL)


def esc(s):
    return html.escape(s, quote=True)


def app_link(ui, cls="button store"):
    if not APP_ID:
        return f'<span class="{cls} soon">{esc(ui["soon"])}</span>'
    return f'<a class="{cls}" href="https://apps.apple.com/app/id{APP_ID}">{esc(ui["download"])}</a>'


def card_list(lang, keys, ui, label):
    p = LANGS[lang]["pages"]
    items = "".join(
        f'<li><h2><a href="{prefix(lang)}/{PATHS[k]}">{esc(p[k]["h1"])}</a></h2><p>{esc(p[k]["description"])}</p>'
        f'<a class="more" href="{prefix(lang)}/{PATHS[k]}">{esc(label)} →</a></li>' for k in keys)
    return f'<ul class="cards list">{items}</ul>'


def page(lang, key):
    c = LANGS[lang]
    ui, p = c["ui"], c["pages"][key]
    pre = prefix(lang)
    body = fill(p["body"], lang)
    if key == "tools":
        body = card_list(lang, TOOLS, ui, ui["open_tool"])
    if key == "guides":
        body = card_list(lang, GUIDES, ui, ui["read_more"])

    schema = []
    if key == "home":
        schema.append({"@context": "https://schema.org", "@type": "MobileApplication", "name": "Medinder",
                       "operatingSystem": "iOS 26", "applicationCategory": "HealthApplication",
                       "description": p["description"], "url": url(lang, "home"), "inLanguage": lang,
                       "image": f"{SITE}/assets/icon-512.png",
                       **({"installUrl": f"https://apps.apple.com/app/id{APP_ID}"} if APP_ID else {})})
        schema.append({"@context": "https://schema.org", "@type": "Organization", "name": "Medinder",
                       "url": SITE, "logo": f"{SITE}/assets/icon-512.png", "email": EMAIL})
    if key in GUIDES:
        schema.append({"@context": "https://schema.org", "@type": "Article", "headline": p["h1"],
                       "description": p["description"], "inLanguage": lang, "dateModified": UPDATED,
                       "author": {"@type": "Organization", "name": "Medinder", "url": SITE},
                       "publisher": {"@type": "Organization", "name": "Medinder", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon-512.png"}},
                       "mainEntityOfPage": url(lang, key)})
    if key in TOOLS:
        schema.append({"@context": "https://schema.org", "@type": "WebApplication", "name": p["h1"],
                       "description": p["description"], "url": url(lang, key), "applicationCategory": "HealthApplication",
                       "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}})
    if p.get("faq"):
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
    crumbs = [("home", ui["breadcrumb_home"])]
    if key in PARENT:
        crumbs.append((PARENT[key], c["pages"][PARENT[key]]["h1"]))
    if key != "home":
        crumbs.append((key, p["h1"]))
        schema.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": url(lang, k)} for i, (k, n) in enumerate(crumbs)]})

    alternates = "".join(f'<link rel="alternate" hreflang="{l}" href="{url(l, key)}">' for l in ORDER)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{url("en", key)}">'
    langs = "".join(f'<li><a href="{prefix(l)}/{PATHS[key]}" hreflang="{l}" lang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{esc(LANGS[l]["native"])}</a></li>' for l in ORDER)
    faq = ""
    if p.get("faq"):
        faq = f'<section class="faq"><h2>{esc(ui["faq_title"])}</h2>' + "".join(
            f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p["faq"]) + "</section>"
    trail = ""
    if key != "home":
        trail = '<nav class="crumbs" aria-label="breadcrumb"><ol>' + "".join(
            f'<li><a href="{pre}/{PATHS[k]}">{esc(n)}</a></li>' for k, n in crumbs[:-1]) + f'<li aria-current="page">{esc(crumbs[-1][1])}</li></ol></nav>'
    related = ""
    if key in TOOLS + GUIDES:
        others = [k for k in TOOLS + GUIDES if k != key][:3]
        related = f'<section class="related"><h2>{esc(ui["related"])}</h2><ul>' + "".join(
            f'<li><a href="{pre}/{PATHS[k]}">{esc(c["pages"][k]["h1"])}</a></li>' for k in others) + "</ul></section>"
    hero_img = ""
    if key == "home":
        hero_img = (f'<figure class="phone"><img src="{BASE}/assets/today-{lang if (ROOT / "assets" / f"today-{lang}.webp").exists() else "en"}.webp" '
                    f'width="600" height="1304" alt="{esc(p["h1"])}" fetchpriority="high"></figure>')
    updated = f'<p class="small">{esc(ui["updated"])}: <time datetime="{UPDATED}">{UPDATED}</time></p>' if key in GUIDES + ["privacy"] else ""
    cta = "" if key in ("privacy",) else (
        f'<section class="cta"><h2>{esc(ui["cta_title"])}</h2><p>{esc(ui["cta_text"])}</p>{app_link(ui)}<p class="small">{esc(ui["requires"])}</p></section>')
    script = ""
    if key in TOOLS:
        script = f'<script>window.T={json.dumps({**p.get("js", {}), "lang": lang}, ensure_ascii=False)}</script><script src="{BASE}/assets/tools.js" defer></script>'
    banner = f'<meta name="apple-itunes-app" content="app-id={APP_ID}">' if APP_ID else ""

    return f"""<!doctype html>
<html lang="{lang}" dir="{c["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["description"])}">
<link rel="canonical" href="{url(lang, key)}">
{alternates}
<meta property="og:type" content="{"article" if key in GUIDES else "website"}">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["description"])}">
<meta property="og:url" content="{url(lang, key)}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:locale" content="{lang.replace("-", "_")}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A6E6E">
{banner}
<link rel="icon" href="{BASE}/assets/icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{BASE}/assets/icon-180.png">
<link rel="stylesheet" href="{BASE}/assets/style.css">
{"".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)}
</head>
<body>
<a class="skip" href="#main">{esc(ui["skip"])}</a>
<header class="top">
<a class="brand" href="{pre}/"><img src="{BASE}/assets/icon-64.png" width="32" height="32" alt="">Medinder</a>
<nav aria-label="main"><a href="{pre}/tools/">{esc(ui["nav_tools"])}</a><a href="{pre}/guides/">{esc(ui["nav_guides"])}</a><a href="{pre}/support/">{esc(ui["nav_support"])}</a></nav>
</header>
<main id="main">
{trail}
<article class="{key}">
<header class="hero"><div><h1>{esc(p["h1"])}</h1><p class="lead">{esc(p["lead"])}</p>{app_link(ui) if key == "home" else ""}{f'<p class="small">{esc(ui["requires"])}</p>' if key == "home" else ""}</div>{hero_img}</header>
{body}
{faq}
{updated}
</article>
{related}
{cta}
</main>
<footer>
<details class="langs"><summary>{esc(ui["language"])}: {esc(c["native"])}</summary><ul>{langs}</ul></details>
<p><a href="{pre}/privacy/">{esc(ui["footer_privacy"])}</a> · <a href="{pre}/support/">{esc(ui["footer_support"])}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p class="small">{esc(ui["footer_note"])}</p>
</footer>
{script}
</body>
</html>
"""


def check():
    """Every language must have the same pages and keys as English, or the build stops."""
    en = LANGS["en"]
    for lang, c in LANGS.items():
        assert set(c["ui"]) >= set(en["ui"]), (lang, set(en["ui"]) - set(c["ui"]))
        for key, pe in en["pages"].items():
            pl = c["pages"][key]
            assert set(pl) >= set(pe) - {"js"} and len(pl.get("faq", [])) == len(pe.get("faq", [])), (lang, key)
            if "js" in pe:
                assert set(pl["js"]) == set(pe["js"]), (lang, key)
            for tag in ("<a ", "<h2>", "<li>", 'id="'):
                assert pl["body"].count(tag) == pe["body"].count(tag), (lang, key, tag)


def main():
    check()
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for lang in ORDER:
        for key in PATHS:
            f = OUT / ("" if lang == "en" else lang) / PATHS[key] / "index.html"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(page(lang, key))
    en = LANGS["en"]["ui"]
    (OUT / "404.html").write_text(page("en", "home").split("<main")[0] + f'<main id="main"><h1>{esc(en["not_found_title"])}</h1><p><a href="{BASE}/">{esc(en["not_found_text"])}</a></p></main></body></html>')

    urls = []
    for key in PATHS:
        for lang in ORDER:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, key)}"/>' for l in ORDER)
            urls.append(f"<url><loc>{url(lang, key)}</loc><lastmod>{UPDATED}</lastmod>{alts}</url>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
                                     + "".join(urls) + "</urlset>\n")
    # AI crawlers are named so a host-level default block does not shut them out
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    (OUT / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")

    p = LANGS["en"]["pages"]
    (OUT / "llms.txt").write_text(
        "# Medinder\n\n> " + p["home"]["lead"] + "\n\n"
        "Medinder is an iPhone app (iOS 26 or later) by an independent developer in Sweden. Reminders ring like an alarm through silent mode and Focus. "
        "No account, no ads, no analytics; medication data stays on the iPhone. It never gives medical advice. Subscription, with reminders that keep ringing if the subscription ends. "
        f"Available in {len(ORDER)} languages: " + ", ".join(LANGS[l]["native"] for l in ORDER) + f". Contact: {EMAIL}\n\n"
        "## Key facts\n\n" + "".join(f"- {q} {a}\n" for q, a in p["home"]["faq"]) + "\n## Pages\n\n"
        + "".join(f"- [{p[k]['h1']}]({url('en', k)}): {p[k]['description']}\n" for k in PATHS))
    # App Store metadata and target keywords per language, for copying into App Store Connect
    rows = ["# App Store metadata and target keywords\n\nGenerated by build.py from content/*.json. Name and subtitle max 30 characters, keywords max 100.\n"]
    for l in ORDER:
        a, k = LANGS[l]["aso"], LANGS[l]["keywords"]
        rows.append(f"\n## {LANGS[l]['native']} ({l})\n\n- Name ({len(a['name'])}): `{a['name']}`\n- Subtitle ({len(a['subtitle'])}): `{a['subtitle']}`\n"
                    f"- Keywords ({len(a['keywords'])}): `{a['keywords']}`\n- Primary: {', '.join(k['primary'])}\n- Secondary: {', '.join(k['secondary'])}\n- Long tail: {', '.join(k['long_tail'])}\n")
        assert len(a["name"]) <= 30 and len(a["subtitle"]) <= 30 and len(a["keywords"]) <= 100, l
    (ROOT / "ASO_KEYWORDS.md").write_text("".join(rows))
    print(f"built {len(ORDER)} languages × {len(PATHS)} pages into {OUT}")


if __name__ == "__main__":
    main()
