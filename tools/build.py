#!/usr/bin/env python3
"""Builds every page of hafeezoyeneyin.com from the data below.

Edit CONFIG or PROJECTS, then run from the repo root:
    python tools/build.py
Pages are written to the repo root. Shared styles and scripts live in assets/.
Optional: drop a video at assets/work/<slug>.mp4 (or .webm, with a .jpg poster) and the Work cards will play it.
`python tools/build.py --preview DIR` writes a copy for the claude.ai preview (no live iframes there).
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================ CONFIG ============================
CONFIG = {
    "site_url": "https://hafeezoyeneyin.com",
    "email": "oyeneyinhafeez@gmail.com",
    "phone": "(734) 552-5832",
    "business": "Oyeneyin Solutions LLC",
}

FONTS = (
    "https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500"
    "&family=Instrument+Serif:ital@0;1"
    "&family=Barlow+Condensed:wght@700;800&family=Caveat:wght@600&family=Boogaloo&family=Nunito:wght@800"
    "&family=Inter:wght@700;800&family=Oswald:wght@600;700&family=Poppins:wght@600"
    "&family=Fraunces:ital,wght@0,600;1,600&family=Instrument+Sans:wght@400;700&display=swap"
)

# HO monogram: two bars (H) joined by a ring (O)
MARK = ('<svg class="mark" viewBox="0 0 28 28" aria-hidden="true">'
        '<rect class="bar" x="3" y="3" width="4.5" height="22" rx="2.25"/>'
        '<rect class="bar" x="20.5" y="3" width="4.5" height="22" rx="2.25"/>'
        '<circle class="o" cx="14" cy="14" r="5"/></svg>')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 28 28'%3E"
           "%3Crect width='28' height='28' rx='7' fill='%2307080B'/%3E"
           "%3Crect x='5' y='5' width='3.6' height='18' rx='1.8' fill='%23F2F3F6'/%3E"
           "%3Crect x='19.4' y='5' width='3.6' height='18' rx='1.8' fill='%23F2F3F6'/%3E"
           "%3Ccircle cx='14' cy='14' r='4' fill='none' stroke='%23FF5BD6' stroke-width='2.2'/%3E%3C/svg%3E")

# ============================ PROJECTS ============================
# live: True loads the real site into the frame on its case study. Set False if a site can't be framed (e.g. no HTTPS yet).
# quote: add a real client quote (with their permission) as {"text": "...", "name": "Alexis R.", "role": "Director"}.
PROJECTS = [
    {
        "slug": "courtside-connections",
        "name": "Courtside Connections",
        "url": "https://courtsideconnectionsnetwork.com/",
        "live": True,
        "status": "Live",
        "kind": "Sports recruiting",
        "tags": "business",
        "accent": "#E8712B",
        "client_class": "cl-courtside",
        "tagline": "A basketball recruiting brand whose whole site plays like a game broadcast.",
        "card": "Recruiting help for high school and college players, with a scoreboard theme, clear packages and an owner-run admin panel.",
        "built_short": ["Scoreboard theme with a running shot clock", "Parent and athlete intake form", "Admin panel for team and testimonials"],
        "brief": [
            "Courtside Connections helps high school and college basketball players get recruited through honest evaluations and real coach relationships, not mass emails.",
            "They needed a site that felt as serious as the athletes they work with, explained four packages without overwhelming families, and turned visitors into free player profiles. The owner also needed to update the team and testimonials without calling a developer.",
        ],
        "features": [
            "Scoreboard-style homepage with a running shot clock",
            "Recruiting process told as four quarters",
            "Package comparison: free tier, Pro, Elite, Collegiate and add-ons",
            "Intake form with separate paths for parents and athletes",
            "Fullscreen background video served from cloud storage",
            "Private admin panel for team members and testimonials",
            "Server-side proxy so admin keys never reach the browser",
            "Coverage of every level, from NCAA D1 to JUCO and NAIA",
        ],
        "details": [
            ("The whole site is a game", "Shot clock, home and away score, quarters for the process, scouting reports for packages and a scorer's table for the form. The theme does the explaining."),
            ("Two front doors", "Parents and athletes start from separate buttons, so each sees the questions that fit them: grad year, position and a film link for athletes."),
            ("Owner-run", "Team members and testimonials are edited from a private admin panel. Changes go through a secure worker, so nothing sensitive sits in the page."),
        ],
        "palette": [("#E8712B", "Court orange"), ("#D4A017", "Gold"), ("#0C1526", "Night navy"), ("#FAF6EE", "Chalk")],
        "fonts": [("Barlow Condensed", "'Barlow Condensed', sans-serif", "MAKE IT TO THE NEXT LEVEL", "800", "uppercase"), ("Caveat", "'Caveat', cursive", "Coach's notes", "600", "none")],
        "stack": "HTML/CSS/JS · Cloudflare Workers + R2 · Firebase",
        "scope": "Design, build, admin panel, video hosting",
        "spec": {"sample": "3%", "font": "'Barlow Condensed', sans-serif", "bg": "#0C1526", "fg": "#E8712B", "size": "5.5rem", "weight": "800", "case": "uppercase"},
        "quote": None,
    },
    {
        "slug": "spring-canvas-festival",
        "name": "America's Spring Canvas Festival",
        "url": "https://ascfestival.com/",
        "live": True,
        "status": "Phase 1 live",
        "kind": "Festival · Community",
        "tags": "events community",
        "accent": "#FDD10A",
        "client_class": "cl-ascf",
        "client_label": "Spring Canvas Festival",
        "tagline": "A festival two years away, with a site that makes it feel inevitable.",
        "card": "A four-day festival built around food, art, music and conflict resolution. Phase 1 is live; ticketing comes next.",
        "built_short": ["Live countdown to opening day", "Multi-page site for every part of the festival", "Sponsor, vendor and exhibitor sign-ups"],
        "brief": [
            "America's Spring Canvas Festival is a four-day festival planned for Memorial Day weekend 2028, built around food, art, music, competition and a year-round conflict-resolution campaign.",
            "Two years out, the site has to win over sponsors, exhibitors, vendors and an audience for an event nobody has seen yet. It also has to grow into ticketing and registration later without being rebuilt.",
        ],
        "features": [
            "Multi-page site: mission, food, arts, entertainment, attractions and news",
            "Live countdown to opening day",
            "Timeline connecting the city's history of world-stage events to 2028",
            "Email sign-up for festival updates",
            "Sponsor, vendor and exhibitor interest forms",
            "Page for a 50,000-player Rock Paper Scissors tournament",
            "Self-serve admin so the team can post updates",
            "Phase 2 in progress: ticketing and registration built to scale",
        ],
        "details": [
            ("History as the pitch", "Super Bowl XVI, WrestleMania III and the 1994 World Cup all happened in Pontiac. The timeline puts 2028 next to them, which sells the ambition in one glance."),
            ("Urgency without a ticket", "There's nothing to buy yet, so the countdown and the update sign-up do the work a ticket button normally would."),
            ("Built in phases", "Phase 1 gets the festival public and collecting sponsors now. Ticketing plugs into the same site later instead of starting over."),
        ],
        "palette": [("#FDD10A", "Canvas yellow"), ("#0E1618", "Stage black"), ("#FFFFFF", "White")],
        "fonts": [("Oswald", "'Oswald', sans-serif", "THE CANVAS OPENS IN", "700", "uppercase"), ("Poppins", "'Poppins', sans-serif", "Four days · Eight stages", "600", "none")],
        "stack": "HTML/CSS/JS · Firebase",
        "scope": "Design, multi-page build, forms, admin",
        "spec": {"sample": "2028", "font": "'Oswald', sans-serif", "bg": "#FDD10A", "fg": "#0E1618", "size": "4.6rem", "weight": "700", "case": "uppercase"},
        "quote": None,
    },
    {
        "slug": "nextgen-tutoring",
        "name": "NextGen Tutoring",
        "url": "https://nextgentutoring.org/",
        "live": True,
        "status": "Live",
        "kind": "EdTech platform",
        "tags": "platform business",
        "accent": "#C9A84C",
        "client_class": "cl-nextgen",
        "tagline": "A tutoring platform that shows parents exactly where the learning gap is.",
        "card": "My own tutoring company. An interactive skill map on the homepage, with bookings, payments and student dashboards behind it.",
        "built_short": ["Interactive prerequisite map", "Session packs with online checkout", "Student accounts, homework and progress reports"],
        "brief": [
            "NextGen Tutoring is my own company. Most tutoring guesses at the problem. NextGen maps every math skill to the skills beneath it, so a 7th grader stuck on ratios gets traced back to the fraction gap that's actually causing it.",
            "The site had to make that idea obvious in seconds to a parent who has never heard of it, then run the business behind it: bookings, payments, homework and progress reports.",
        ],
        "features": [
            "Interactive prerequisite map: tap any skill to see what it depends on",
            "Free diagnostic booking as the first step",
            "Session packs with online checkout and no subscriptions",
            "Student logins and dashboards",
            "Homework delivered after each session, built from what was covered",
            "Admin view of every student's progress",
            "Monthly progress reports for parents",
            "AI-generated practice tied to the skill map",
        ],
        "details": [
            ("The product is the hero", "Instead of a stock photo of a smiling student, the homepage opens on the actual skill map. Parents see how it works before they read a word."),
            ("Pricing with no fine print", "Three clear packs, the per-session math shown, and the first session free. Nothing auto-renews."),
            ("It runs the business", "Behind the marketing site are accounts, payments, homework delivery and reports, all on the same stack."),
        ],
        "palette": [("#C9A84C", "Gold"), ("#FBF7EC", "Paper"), ("#F1EBDC", "Sand"), ("#1C1A16", "Ink")],
        "fonts": [("Fraunces", "'Fraunces', serif", "See exactly where the gap is.", "600", "none"), ("Instrument Sans", "'Instrument Sans', sans-serif", "Diagnose · Plan · Close the gap", "700", "none")],
        "stack": "HTML/CSS/JS · Firebase Auth + Firestore · Cloudflare Workers · Stripe · Claude API",
        "scope": "Product, design, full platform build",
        "spec": {"sample": "the gap", "font": "'Fraunces', serif", "bg": "#FBF7EC", "fg": "#1C1A16", "size": "3.4rem", "weight": "600", "case": "none", "italic": True},
        "quote": None,
    },
    {
        "slug": "timber-and-forge",
        "name": "Timber & Forge Creations",
        "url": "https://timberforgecreations1.com/",
        "live": True,
        "status": "Live",
        "kind": "Custom furniture",
        "tags": "business",
        "accent": "#C98B4F",
        "client_class": "cl-timber",
        "client_label": "Timber & Forge",
        "tagline": "A maker's story, told the way the work is made: by hand, with nothing hidden.",
        "card": "Custom tables, shelves and signs from reclaimed wood, steel and resin. A story-led site that turns interest into quote requests.",
        "built_short": ["Story-led homepage", "Four-step process with deposit and lead time up front", "Quote request form"],
        "brief": [
            "Timber & Forge Creations builds custom tables, shelves and signs from reclaimed wood, steel and epoxy resin. Every piece is one of a kind.",
            "The site needed to carry the story behind the work, set honest expectations about time and cost, and turn that interest into qualified quote requests instead of price-shopping messages.",
        ],
        "features": [
            "Story-led homepage built around the shop's philosophy",
            "Recent work gallery that links to Instagram",
            "Four-step process: discovery, design, build, delivery",
            "Lead time and deposit stated right in the hero",
            "Client testimonials",
            "FAQ for timing, requirements and delivery",
            "Quote request form with a 1–2 business day reply promise",
        ],
        "details": [
            ("Expectations up front", "\"15–30 days, 50% deposit\" sits right under the first button. People who reach out already know how this works."),
            ("Story first", "The \"perfectly imperfect\" philosophy carries the page, which is what sets a hand-built table apart from a catalog one."),
            ("Instagram stays the gallery", "New pieces go up on Instagram already. The site points there, so the portfolio never goes stale."),
        ],
        "palette": [("#0E1B2A", "Forge navy"), ("#C98B4F", "Walnut (accent)"), ("#FFFFFF", "White"), ("#F2FCFC", "Mist")],
        "fonts": [("Inter", "'Inter', sans-serif", "Built to last.", "800", "none")],
        "stack": "HTML/CSS/JS · GitHub Pages",
        "scope": "Design, copy structure, build",
        "spec": {"sample": "Built to last.", "font": "'Inter', sans-serif", "bg": "#0E1B2A", "fg": "#C98B4F", "size": "2.6rem", "weight": "800", "case": "none", "track": "-0.03em"},
        "quote": None,
    },
    {
        "slug": "tipsy-trail",
        "name": "Tipsy Trail Bar Crawl",
        "url": "http://tipsytrailbc.com/",
        "live": False,
        "status": "Live",
        "kind": "Nightlife · Events",
        "tags": "events business",
        "accent": "#E85DA8",
        "client_class": "cl-tipsy",
        "client_label": "Tipsy Trail",
        "tagline": "A Dallas bar crawl you can understand and book in under a minute, on your phone.",
        "card": "Guided bar crawls every Friday and Saturday in Dallas. A phone-first site with a booking calendar that only opens on crawl nights.",
        "built_short": ["Friday/Saturday-only booking calendar", "Ticket counter with live total", "FAQ and group booking contact"],
        "brief": [
            "Tipsy Trail runs guided bar crawls every Friday and Saturday night in Dallas's Bishop Arts District.",
            "Most visitors arrive on a phone from a social post. The site had to sell the night fast: what it is, what the $40 ticket covers, and how to grab a spot, before they scroll away.",
        ],
        "features": [
            "Bold, phone-first landing page",
            "Booking calendar that only opens Fridays and Saturdays",
            "Ticket counter with a running total",
            "How it works in four steps",
            "Reviews from past crawls",
            "FAQ covering 21+, solo guests and what's included",
            "Text and email contact for group and private crawls",
        ],
        "details": [
            ("Only the right nights", "The calendar only lets people pick Fridays and Saturdays, so nobody books a Tuesday that doesn't exist."),
            ("Answers before questions", "21+, solo-friendly, no cover and drinks not included are all on the page, which cuts down the DMs."),
            ("Personality in the type", "A loud, playful display face and hot-pink palette match a night out, not a corporate event."),
        ],
        "palette": [("#E85DA8", "Party pink"), ("#FFF9F5", "Blush"), ("#333333", "Charcoal"), ("#FFFFFF", "White")],
        "fonts": [("Boogaloo", "'Boogaloo', cursive", "TIPSY TRAIL", "400", "uppercase"), ("Nunito", "'Nunito', sans-serif", "Explore. Sip. Repeat.", "800", "none")],
        "stack": "HTML/CSS/JS · GitHub Pages",
        "scope": "Design, booking flow, build",
        "spec": {"sample": "Tipsy", "font": "'Boogaloo', cursive", "bg": "#E85DA8", "fg": "#FFFFFF", "size": "4.4rem", "weight": "400", "case": "none"},
        "quote": None,
    },
]

FEATURED = ["courtside-connections", "spring-canvas-festival", "nextgen-tutoring"]

TAG_LABELS = [("all", "All"), ("business", "Business"), ("events", "Events"), ("community", "Community"), ("platform", "Platforms")]

# ============================ HELPERS ============================
E = html.escape


def domain(url):
    return re.sub(r"^https?://", "", url).rstrip("/")


def page_file(p):
    return f"work-{p['slug']}.html"


def media(p):
    """Optional video for a project card (assets/work/<slug>.mp4/.webm)."""
    base = os.path.join(ROOT, "assets", "work", p["slug"])
    found = {ext: os.path.exists(f"{base}.{ext}") for ext in ("mp4", "webm", "jpg")}
    if not (found["mp4"] or found["webm"]):
        return ""
    src = "".join(f'<source src="assets/work/{p["slug"]}.{ext}" type="video/{ext}">' for ext in ("mp4", "webm") if found[ext])
    poster_attr = f' poster="assets/work/{p["slug"]}.jpg"' if found["jpg"] else ""
    return f'<video class="media" autoplay muted loop playsinline preload="metadata"{poster_attr}>{src}</video>'


def poster(p):
    s = p["slug"]
    if s == "courtside-connections":
        return """<div class="poster p-courtside" aria-hidden="true">
  <div class="board"><span>HOME<b>0</b></span><span class="clock">SHOT CLOCK<b data-shotclock>24.0</b></span><span>AWAY<b>0</b></span></div>
  <div class="big">3%</div>
  <div class="line">Make it to the next level</div>
  <div class="sub">built by players who lived it</div>
</div>"""
    if s == "tipsy-trail":
        cells = "".join(f'<span class="hd">{d}</span>' for d in "SMTWTFS")
        for i in range(1, 15):
            cells += f'<span class="{"on" if i % 7 in (6, 0) else ""}">{i}</span>'
        return f"""<div class="poster p-tipsy" aria-hidden="true">
  <div class="tag">DALLAS NIGHTLIFE · 21+</div>
  <div class="big">TIPSY<br>TRAIL</div>
  <div class="cal">{cells}</div>
  <div class="price">$40 · Fri &amp; Sat · 8 PM</div>
</div>"""
    if s == "timber-and-forge":
        return """<div class="poster p-timber" aria-hidden="true">
  <div class="grain"></div>
  <p class="kick">TIMBER &amp; FORGE CREATIONS</p>
  <p class="big">Bespoke wood &amp; metal creations, built to last.</p>
  <p class="note">Lead time 15–30 days · 50% deposit</p>
  <span class="btnish">Request a quote</span>
</div>"""
    if s == "spring-canvas-festival":
        return """<div class="poster p-ascf" aria-hidden="true">
  <p class="kick">America's Spring Canvas Festival</p>
  <p class="lbl">The canvas opens in</p>
  <p class="count"><b data-countdown="2028-05-26T12:00:00-04:00">--</b><small>days</small></p>
  <div class="time"><span>1982</span><span>1987</span><span>1994</span><span class="now">2028</span></div>
</div>"""
    if s == "nextgen-tutoring":
        return """<div class="poster p-nextgen" aria-hidden="true">
  <div><p class="kick">NEXTGEN TUTORING</p><p class="big">See exactly where the <em>gap</em> is.</p></div>
  <svg viewBox="0 0 200 170">
    <line class="e" x1="100" y1="22" x2="55" y2="70"/><line class="e" x1="100" y1="22" x2="145" y2="70"/>
    <line class="e" x1="55" y1="70" x2="30" y2="120"/><line class="e" x1="55" y1="70" x2="80" y2="120"/>
    <line class="e" x1="145" y1="70" x2="120" y2="120"/><line class="e" x1="145" y1="70" x2="170" y2="120"/>
    <line class="e" x1="30" y1="120" x2="55" y2="155"/><line class="e" x1="80" y1="120" x2="55" y2="155"/>
    <line class="e" x1="120" y1="120" x2="145" y2="155"/><line class="e" x1="170" y1="120" x2="145" y2="155"/>
    <circle class="n" cx="100" cy="22" r="10"/>
    <circle class="n pulse" cx="55" cy="70" r="10"/><circle class="n" cx="145" cy="70" r="10"/>
    <circle class="n solid" cx="30" cy="120" r="10"/><circle class="n pulse" cx="80" cy="120" r="10" style="animation-delay:.9s"/>
    <circle class="n solid" cx="120" cy="120" r="10"/><circle class="n solid" cx="170" cy="120" r="10"/>
    <circle class="n solid" cx="55" cy="155" r="10"/><circle class="n solid" cx="145" cy="155" r="10"/>
  </svg>
</div>"""
    return ""


def frame(p, fid=None, interactive=False):
    """Browser frame. Listing frames show the recorded video if there is one, otherwise the live site
    (desktop only), otherwise the poster. Case-study frames always try the live, clickable site."""
    vid = media(p)
    live = p["live"] and (interactive or not vid)
    attrs = [
        'class="frame' + (" interactive" if interactive else "") + '"',
        f'data-url="{E(p["url"])}"',
        f'data-name="{E(p["name"])}"',
        f'data-live="{1 if live else 0}"',
        f'style="--acc:{p["accent"]}"',
    ]
    if fid:
        attrs.append(f'id="{fid}"')
    if not interactive:
        attrs.append('data-lazy-desktop="1"')
    return f"""<div {' '.join(attrs)}>
  <div class="chrome" aria-hidden="true"><i></i><i></i><i></i><em>{E(domain(p["url"]))}</em><b></b></div>
  <div class="frame-view">{poster(p)}{vid}</div>
</div>"""


def head(title, desc, path, preview=False):
    canon = CONFIG["site_url"] + ("/" if path == "index.html" else "/" + path.replace(".html", ""))
    pv = "<script>window.SITE_PREVIEW = true;</script>\n" if preview else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#07080B">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css">
{pv}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


NAV = [("work.html", "Work"), ("services.html", "Services"), ("about.html", "About"), ("contact.html", "Contact")]


def header(active):
    def cur(href):
        return ' aria-current="page"' if href == active else ""
    desk = "\n      ".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV if h != "contact.html")
    mob = "\n      ".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in [("index.html", "Home")] + NAV)
    return f"""<header class="site-header{' solid' if active != 'index.html' else ''}" id="header">
  <div class="wrap">
    <a class="wordmark" href="index.html" aria-label="Hafeez Oyeneyin, home">{MARK}<span>Hafeez Oyeneyin</span></a>
    <nav class="nav" aria-label="Main">
      {desk}
      <a class="btn btn-primary" href="contact.html">Start a project</a>
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span><span></span></button>
    </nav>
  </div>
  <div class="mobile-menu" id="mobile-menu" hidden>
    <div class="wrap">
      {mob}
    </div>
  </div>
</header>
"""


def footer():
    work = "".join(f'<li><a href="{page_file(p)}">{E(p.get("client_label", p["name"]))}</a></li>' for p in PROJECTS)
    site = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in [("index.html", "Home")] + NAV)
    em = E(CONFIG["email"])
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div>
        <p class="say">Let's build <em>something good.</em></p>
        <a class="foot-mail" href="mailto:{em}">{em}</a>
      </div>
      <div class="foot-cols">
        <div><h4>Site</h4><ul>{site}</ul></div>
        <div><h4>Work</h4><ul>{work}</ul></div>
      </div>
    </div>
    <div class="foot-row">
      <a class="wordmark" href="index.html" aria-label="Home">{MARK}<span>Hafeez Oyeneyin</span></a>
      <p>© <span id="year">2026</span> · A service of {CONFIG['business']} · Working with clients worldwide</p>
    </div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


def cta(title="Have a project <em>in mind?</em>", text="Tell me what you're working on. You'll hear back within two business days to set up a free 15-minute call."):
    return f"""<section class="cta" aria-labelledby="cta-title">
  <div class="wrap reveal">
    <h2 class="display" id="cta-title">{title}</h2>
    <p>{text}</p>
    <a class="btn btn-primary" href="contact.html">Start a project <span class="arr" aria-hidden="true">→</span></a>
  </div>
</section>
"""


SERVICES = [
    ("Launch", "get online, properly", "A sharp site that makes you look established from day one.",
     ["1–3 pages, built phone-first", "Contact form sent to your email", "Domain, hosting and launch handled", "Page titles and Google basics set up"], "tipsy-trail"),
    ("Grow", "room for everything you do", "A fully custom site built around your brand, services and story.",
     ["Multi-page site designed around your brand", "Two homepage designs to choose from", "Sign-up and inquiry forms sent to the right inbox", "Calendars, booking or social feeds built in"], "timber-and-forge"),
    ("Platform", "a site that does work for you", "For sites that need to run things: admin portals, accounts, payments.",
     ["Admin portal so you can edit content yourself", "Registrations, waitlists and member logins", "Online payments and ticketing", "A plain-English guide to running it"], "courtside-connections"),
]


def svc_rows(with_examples=False):
    out = []
    for name, sub, desc, items, eg in SERVICES:
        ex = ""
        if with_examples:
            p = next(x for x in PROJECTS if x["slug"] == eg)
            ex = f'<span class="eg">Example: <a href="{page_file(p)}">{E(p["name"])}</a></span>'
        lis = "".join(f"<li>{E(i)}</li>" for i in items)
        out.append(f"""<article class="svc reveal">
  <h3>{name}<small>{sub}</small></h3>
  <p>{desc}{ex}</p>
  <ul>{lis}</ul>
</article>""")
    return "\n".join(out)


STEPS = """<ol class="steps" id="steps">
  <li><h3>Free 15-minute call</h3><p>Tell me what you do, who you want to reach and what the site needs to handle.</p></li>
  <li><h3>Fixed quote + two designs</h3><p>You get a fixed price, then two homepage directions to pick from.</p></li>
  <li><h3>Build with a live preview</h3><p>A private link lets you watch the site come together and send feedback.</p></li>
  <li><h3>Launch + handoff</h3><p>I connect your domain, launch the site and hand you a simple guide.</p></li>
</ol>"""


def faq(items):
    return '<div class="faq reveal">' + "".join(
        f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in items) + "</div>"


FAQ_GENERAL = [
    ("How much does a website cost?", "Every project gets a fixed quote after a free 15-minute call, based on what the site needs to do. You'll know the full price before any work starts, and it won't change unless the scope does."),
    ("Will I have to pay every month?", "No. Your site is custom-coded, so there's no website-builder subscription to keep paying. The only ongoing cost is your domain name, usually about $10–15 a year. Sites with logins or payments may have small usage-based service costs, which the quote spells out."),
    ("Can I update the site myself?", "Yes, if you need to. Sites can include an admin portal for editing programs, events, photos and announcements, plus a guide that walks you through it. For simpler sites, send me small text changes and I'll make them at no charge."),
    ("I already have a website. Can you rebuild it?", "Yes. I'll bring your content over from your current site or website builder, rebuild it properly and move your domain without breaking your email. Keep your current plan running until the new site is live."),
    ("Do you work with clients outside my area?", "Yes. Everything runs remotely: calls, design reviews and a live preview link you can open from anywhere."),
    ("How long does it take?", "Most sites take one to three weeks from the first call to launch. Sites with admin portals, accounts or payments take longer, and you'll get a timeline with the quote."),
    ("How does payment work?", f"Invoices are issued by {CONFIG['business']}, with payment details on each invoice. Anything outside the agreed scope is quoted separately before I start on it."),
]


def quotes_block():
    qs = [p for p in PROJECTS if p.get("quote")]
    if not qs:
        return ""
    figs = "".join(
        f'<figure class="quote reveal" style="--acc:{p["accent"]}"><blockquote>“{E(p["quote"]["text"])}”</blockquote>'
        f'<figcaption>{E(p["quote"]["name"])} <span>{E(p["quote"].get("role", ""))}, {E(p["name"])}</span></figcaption></figure>'
        for p in qs)
    return f"""<section class="section" aria-labelledby="quotes-title">
  <div class="wrap">
    <div class="section-head reveal"><div><p class="eyebrow">Clients</p><h2 id="quotes-title" class="display">In their <em>words</em></h2></div></div>
    <div class="quotes">{figs}</div>
  </div>
</section>
"""


# ============================ PAGES ============================
def page_home(pv):
    feats = []
    for slug in FEATURED:
        p = next(x for x in PROJECTS if x["slug"] == slug)
        built = "".join(f"<li>{E(b)}</li>" for b in p["built_short"])
        feats.append(f"""<article class="feature reveal" style="--acc:{p['accent']}">
  <a class="frame-link" href="{page_file(p)}" aria-label="{E(p['name'])} case study">{frame(p)}</a>
  <div class="feature-copy">
    <p class="kind">{E(p['kind'])}</p>
    <h3><a href="{page_file(p)}">{E(p['name'])}</a></h3>
    <p>{E(p['card'])}</p>
    <ul class="built">{built}</ul>
    <a class="link-arrow" href="{page_file(p)}">View case study <span aria-hidden="true">→</span></a>
  </div>
</article>""")
    specs = []
    for p in PROJECTS:
        sp = p["spec"]
        style = (f"--sbg:{sp['bg']};--sfg:{sp['fg']};--sfont:{sp['font']};--ssize:{sp['size']};--sweight:{sp['weight']};"
                 f"--scase:{sp.get('case','none')};--strack:{sp.get('track','0')}")
        sample = f"<em>{E(sp['sample'])}</em>" if sp.get("italic") else E(sp["sample"])
        sw = "".join(f'<i style="background:{c}"></i>' for c, _ in p["palette"][:4])
        specs.append(f"""<a class="spec" href="{page_file(p)}" style="{style}">
  <span class="sample">{sample}</span>
  <span class="meta"><b>{E(p['name'])}</b>{E(p['fonts'][0][0])}<span class="sw">{sw}</span></span>
</a>""")
    clients = "".join(f'<li><a class="{p["client_class"]}" href="{page_file(p)}">{E(p.get("client_label", p["name"]))}</a></li>' for p in PROJECTS)
    return head("Hafeez Oyeneyin | Custom-Coded Websites", "Custom-coded websites for businesses, nonprofits and teams anywhere. No templates, no monthly platform fees.", "index.html", pv) + header("index.html") + f"""
<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <canvas id="field" aria-hidden="true"></canvas>
    <div class="wrap">
      <p class="status-pill"><i aria-hidden="true"></i>Available for new projects</p>
      <h1 id="hero-title" class="display">
        <span class="line"><span>Websites, built</span></span>
        <span class="line"><span>from <em>scratch.</em></span></span>
      </h1>
      <p class="lede">I design and code custom websites for businesses, nonprofits and teams. No templates, no monthly platform fees. A fast site that fits you, and you own all of it.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="contact.html">Start a project <span class="arr" aria-hidden="true">→</span></a>
        <a class="btn" href="work.html">See the work</a>
      </div>
    </div>
  </section>

  <section class="clients" aria-label="Clients">
    <div class="wrap">
      <p>Recent sites, each built from scratch</p>
      <ul class="client-list">{clients}</ul>
    </div>
  </section>

  <section class="section" aria-labelledby="work-title">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Selected work</p><h2 id="work-title" class="display">Built to do <em>a job</em></h2></div>
        <p>Each site was designed and coded around what that client actually needed day to day.</p>
      </div>
      <div class="feature-list">
        {''.join(feats)}
      </div>
      <p style="margin-top:80px"><a class="btn" href="work.html">See all {len(PROJECTS)} projects <span class="arr" aria-hidden="true">→</span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="look-title">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Identity</p><h2 id="look-title" class="display">Every client gets <em>their own</em> look</h2></div>
        <p>No shared template. Each site gets its own type, colors and personality, picked to fit the business.</p>
      </div>
      <div class="specimens reveal">
        {''.join(specs)}
      </div>
    </div>
  </section>
{quotes_block()}
  <section class="section" aria-labelledby="services-title">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Services</p><h2 id="services-title" class="display">What I build</h2></div>
        <p>Every project gets a fixed quote after a free call, so you know the full price before any work starts.</p>
      </div>
      <div class="svc-list">
        {svc_rows()}
      </div>
      <p style="margin-top:40px"><a class="link-arrow" href="services.html">Everything I can build <span aria-hidden="true">→</span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="process-title">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Process</p><h2 id="process-title" class="display">How a project runs</h2></div>
        <p>You always know what's happening, what's next and what it costs.</p>
      </div>
      {STEPS}
    </div>
  </section>
{cta()}</main>
""" + footer()


def page_work(pv):
    counts = {k: sum(1 for p in PROJECTS if k == "all" or k in p["tags"].split()) for k, _ in TAG_LABELS}
    btns = "".join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}<span>{counts[k]}</span></button>' for k, v in TAG_LABELS if counts[k])
    cards = []
    for p in PROJECTS:
        cards.append(f"""<a class="card reveal" href="{page_file(p)}" data-tags="{p['tags']}" style="--acc:{p['accent']}">
  {frame(p)}
  <div class="card-body">
    <div class="card-top"><p class="kind">{E(p['kind'])}</p><span class="status">{E(p['status'])}</span></div>
    <h3>{E(p['name'])}</h3>
    <p>{E(p['card'])}</p>
  </div>
</a>""")
    return head("Work | Hafeez Oyeneyin", "Websites designed and coded from scratch: recruiting, events, furniture makers, festivals and an EdTech platform.", "work.html", pv) + header("work.html") + f"""
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Work</p>
      <h1 class="display">Sites that do <em>a job</em></h1>
      <p class="intro">Every project here is live. Open any one to see the real site running inside the page, exactly as its customers see it.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="filters" role="group" aria-label="Filter projects">{btns}</div>
      <div class="cards">
        {''.join(cards)}
      </div>
    </div>
  </section>
{cta()}</main>
""" + footer()


def page_case(p, i, pv):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    brief = "".join(f"<p>{E(b)}</p>" for b in p["brief"])
    feats = "".join(f"<li>{E(f)}</li>" for f in p["features"])
    details = "".join(f'<article class="detail reveal"><h3>{E(t)}</h3><p>{E(d)}</p></article>' for t, d in p["details"])
    sw = "".join(f'<div class="swatch"><i style="background:{c}"></i><span>{E(n)}<br><code>{c}</code></span></div>' for c, n in p["palette"])
    fonts = "".join(
        f'<div><span class="as" style="font-family:{f[1]};font-weight:{f[3]};text-transform:{f[4]}">{E(f[2])}</span><span class="name">{E(f[0])}</span></div>'
        for f in p["fonts"])
    fid = "live-" + p["slug"]
    notice = ""
    if not p["live"]:
        notice = '<p class="notice">The interactive preview for this project is paused while its security certificate is renewed.</p>'
    quote = ""
    if p.get("quote"):
        q = p["quote"]
        quote = f"""<section class="cs-sec"><div class="wrap cs-grid reveal"><h2><small>client</small>In their words</h2>
<figure class="big-quote"><blockquote>“{E(q['text'])}”</blockquote><figcaption>{E(q['name'])}, {E(q.get('role', ''))}</figcaption></figure></div></section>"""
    note = "This is the live site. Scroll and click inside it, or switch to the phone view." if p["live"] else ""
    return head(f"{p['name']} | Case study | Hafeez Oyeneyin", p["tagline"], page_file(p), pv) + header("work.html") + f"""
<main id="main" class="cs" style="--brand:{p['accent']}">
  <section class="cs-hero">
    <div class="wrap">
      <a class="crumb" href="work.html">← All work</a>
      <p class="eyebrow">{E(p['kind'])}</p>
      <h1 class="display">{E(p['name'])}</h1>
      <p class="cs-tagline">{E(p['tagline'])}</p>
      <dl class="cs-meta">
        <div><dt>Role</dt><dd>{E(p['scope'])}</dd></div>
        <div><dt>Built with</dt><dd>{E(p['stack'])}</dd></div>
        <div><dt>Status</dt><dd>{E(p['status'])}</dd></div>
        <div><dt>Visit</dt><dd><a href="{E(p['url'])}" target="_blank" rel="noopener">{E(domain(p['url']))} ↗</a></dd></div>
      </dl>
    </div>
  </section>

  <section class="cs-preview" aria-label="Live preview">
    <div class="wrap">
      <div class="toolbar">
        <div class="seg" role="group" aria-label="Preview size">
          <button type="button" data-device="desktop" data-target="{fid}" aria-pressed="true">Desktop</button>
          <button type="button" data-device="phone" data-target="{fid}" aria-pressed="false">Phone</button>
        </div>
        <a class="btn" href="{E(p['url'])}" target="_blank" rel="noopener">Visit the live site <span class="arr" aria-hidden="true">↗</span></a>
      </div>
      {frame(p, fid=fid, interactive=True)}
      <p class="frame-note">{note}</p>
      {notice}
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap cs-grid reveal">
      <h2><small>The brief</small>What they needed</h2>
      <div class="prose">{brief}</div>
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap cs-grid reveal">
      <h2><small>The build</small>What I built</h2>
      <ul class="featlist">{feats}</ul>
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap">
      <div class="cs-grid reveal" style="margin-bottom:48px"><h2><small>Details</small>Worth noticing</h2><div></div></div>
      <div class="details">{details}</div>
    </div>
  </section>
{quote}
  <section class="cs-sec">
    <div class="wrap">
      <div class="cs-grid reveal" style="margin-bottom:48px"><h2><small>Identity</small>Look and feel</h2><div class="prose"><p style="font-size:1.12rem;color:var(--text-2)">The colors and type chosen for this brand.</p></div></div>
      <div class="look reveal">
        <div class="swatches">{sw}</div>
        <div class="type-spec">{fonts}</div>
      </div>
    </div>
  </section>

  <section class="section" aria-label="Next project">
    <div class="wrap">
      <a class="next-proj reveal" href="{page_file(nxt)}" style="--next:{nxt['accent']}">
        <div><p class="label">Next project →</p><h2 class="display">{E(nxt['name'])}</h2></div>
        {frame(nxt)}
      </a>
    </div>
  </section>
{cta("Want a site <em>like this?</em>")}</main>
""" + footer()


def page_services(pv):
    addons = [
        ("Admin portal", "Edit programs, team members, events and photos yourself, from any device.", "courtside-connections"),
        ("Bookings + calendars", "Date pickers, event calendars and booking flows that only allow the slots you run.", "tipsy-trail"),
        ("Sign-up + application forms", "Registrations, vendor and sponsor applications, sent to the right inbox and saved.", "spring-canvas-festival"),
        ("Online payments", "Checkout for sessions, packages or tickets, with receipts handled for you.", "nextgen-tutoring"),
        ("Accounts + dashboards", "Member logins with their own dashboard, history and downloads.", "nextgen-tutoring"),
        ("Moving off a website builder", "Your content brought over, rebuilt properly and your domain moved without breaking email.", None),
    ]
    cards = []
    for t, d, slug in addons:
        seen = ""
        if slug:
            p = next(x for x in PROJECTS if x["slug"] == slug)
            seen = f'<span class="seen">See it on <a href="{page_file(p)}">{E(p["name"])}</a></span>'
        cards.append(f'<article class="addon reveal"><h3>{E(t)}</h3><p>{E(d)}</p>{seen}</article>')
    return head("Services | Hafeez Oyeneyin", "Custom websites from a sharp launch site to platforms with admin portals, bookings and payments. Fixed quotes, no monthly platform fees.", "services.html", pv) + header("services.html") + f"""
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Services</p>
      <h1 class="display">What I <em>build</em></h1>
      <p class="intro">From a sharp one-page site to a platform with logins and payments. Every project gets a fixed quote after a free call, with no monthly platform fees, and you own everything.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="svc-list">
        {svc_rows(with_examples=True)}
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Add-ons</p><h2 class="display">Things your site <em>can do</em></h2></div>
        <p>Mix these into any project. Each one is already running on a client site.</p>
      </div>
      <div class="addons">{''.join(cards)}</div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Process</p><h2 class="display">How a project runs</h2></div>
        <p>You always know what's happening, what's next and what it costs.</p>
      </div>
      {STEPS}
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="section-head reveal"><div><p class="eyebrow">FAQ</p><h2 class="display">Questions</h2></div></div>
      {faq(FAQ_GENERAL)}
    </div>
  </section>
{cta()}</main>
""" + footer()


def page_about(pv):
    principles = [
        ("Built from scratch", "No themes, no page builders. Every site is designed and coded for the business it belongs to."),
        ("Yours to keep", "You own the code, the domain and the content. No platform can raise your price or lock you in."),
        ("Fast on a phone", "Most of your visitors are on a phone. Sites are built for that first and tested on real devices."),
        ("Straight answers", "A fixed quote before work starts, a timeline you can hold me to, and a heads-up before anything changes scope."),
    ]
    pr = "".join(f'<article class="principle reveal"><h3>{E(t)}</h3><p>{E(d)}</p></article>' for t, d in principles)
    stack = ["HTML", "CSS", "JavaScript", "Firebase", "Firestore", "Cloudflare Workers", "Cloudflare R2", "Stripe", "GitHub Pages", "Formspree", "Claude API"]
    st = "".join(f"<li>{E(s)}</li>" for s in stack)
    return head("About | Hafeez Oyeneyin", "One builder, a direct line. How I design and build websites.", "about.html", pv) + header("about.html") + f"""
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">About</p>
      <h1 class="display">You work with <em>me, directly</em></h1>
      <p class="intro">I'm Hafeez, a software engineer. I design and code every site myself, and you talk to me from the first call through launch day and after, wherever you're based.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="section-head reveal"><div><p class="eyebrow">Principles</p><h2 class="display">How I work</h2></div></div>
      <div class="principles">{pr}</div>
    </div>
  </section>
  <section class="section">
    <div class="wrap two-col reveal">
      <div><p class="eyebrow">Stack</p><h2 class="display">What I build with</h2></div>
      <div>
        <div class="prose"><p>Plain, fast web code on the front end, and proven services behind it for logins, data, payments and file storage. No heavy frameworks unless a project needs one.</p></div>
        <ul class="stack">{st}</ul>
      </div>
    </div>
  </section>
{cta()}</main>
""" + footer()


def page_contact(pv):
    em, ph = CONFIG["email"], CONFIG["phone"]
    return head("Contact | Hafeez Oyeneyin", "Start a project. Tell me what you're building and I'll reply within two business days.", "contact.html", pv) + header("contact.html") + f"""
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Contact</p>
      <h1 class="display">Tell me what you're <em>building</em></h1>
      <p class="intro">Send the details and I'll get back to you within two business days to set up a free 15-minute call.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap contact-grid">
      <div class="reveal">
        <div class="direct">
          <div class="direct-row"><b>Email</b><div class="direct-line"><span id="email-text">{E(em)}</span><button class="copy" type="button" data-copy="email-text">Copy</button></div></div>
          <div class="direct-row"><b>Call or text</b><div class="direct-line"><span id="phone-text">{E(ph)}</span><button class="copy" type="button" data-copy="phone-text">Copy</button></div></div>
        </div>
        <p class="side-label">What happens next</p>
        <ol class="next-steps">
          <li><b>I read your message</b><span>and reply within two business days.</span></li>
          <li><b>We have a free 15-minute call</b><span>about what you do and what the site needs to handle.</span></li>
          <li><b>You get a fixed quote</b><span>and a timeline, before any work starts.</span></li>
        </ol>
      </div>
      <form class="intake reveal" id="intake" data-email="{E(em)}" novalidate>
        <div class="field-row">
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        </div>
        <div class="field"><label for="f-org">Business or organization</label><input id="f-org" name="organization" autocomplete="organization"></div>
        <div class="field"><label for="f-site">Current website, if you have one</label><input id="f-site" name="current_site" inputmode="url" placeholder="example.com"></div>
        <fieldset class="field">
          <legend>What do you need?</legend>
          <div class="chips">
            <label class="chip"><input type="radio" name="project_type" id="t-new" value="New website"><span>New website</span></label>
            <label class="chip"><input type="radio" name="project_type" id="t-redo" value="Redesign of an existing site"><span>Redesign my current site</span></label>
            <label class="chip"><input type="radio" name="project_type" id="t-custom" value="Admin portal, bookings or payments"><span>Admin portal, bookings or payments</span></label>
            <label class="chip"><input type="radio" name="project_type" id="t-unsure" value="Not sure yet"><span>Not sure yet</span></label>
          </div>
        </fieldset>
        <fieldset class="field">
          <legend>Budget</legend>
          <div class="chips">
            <label class="chip"><input type="radio" name="budget" id="b-1" value="Under $500"><span>Under $500</span></label>
            <label class="chip"><input type="radio" name="budget" id="b-2" value="$500–$1,500"><span>$500–$1,500</span></label>
            <label class="chip"><input type="radio" name="budget" id="b-3" value="$1,500–$5,000"><span>$1,500–$5,000</span></label>
            <label class="chip"><input type="radio" name="budget" id="b-4" value="$5,000+"><span>$5,000+</span></label>
            <label class="chip"><input type="radio" name="budget" id="b-5" value="Not sure"><span>Not sure</span></label>
          </div>
        </fieldset>
        <div class="field">
          <label for="f-when">When do you need it?</label>
          <select id="f-when" name="timeline">
            <option value="">Choose one</option>
            <option>As soon as possible</option>
            <option>Within a month</option>
            <option>1–3 months</option>
            <option>Just exploring</option>
          </select>
        </div>
        <div class="field"><label for="f-msg">Tell me about the project</label><textarea id="f-msg" name="message" placeholder="What you do, what the site needs to handle, sites you like…"></textarea></div>
        <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="form-foot">
          <button class="btn btn-primary" type="submit" id="f-submit">Send project details <span class="arr" aria-hidden="true">→</span></button>
          <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
        </div>
      </form>
    </div>
  </section>
</main>
""" + footer()


def page_404(pv):
    return head("Page not found | Hafeez Oyeneyin", "This page doesn't exist.", "404.html", pv) + header("") + """
<main id="main">
  <section class="section lost">
    <div class="wrap">
      <p class="code">404</p>
      <h1 class="display" style="font-size:var(--step-3);margin-bottom:32px">This page <em>doesn't exist</em></h1>
      <a class="btn btn-primary" href="index.html">Back home <span class="arr" aria-hidden="true">→</span></a>
    </div>
  </section>
</main>
""" + footer()


def build(out, preview=False):
    pages = {
        "index.html": page_home(preview),
        "work.html": page_work(preview),
        "services.html": page_services(preview),
        "about.html": page_about(preview),
        "contact.html": page_contact(preview),
        "404.html": page_404(preview),
    }
    for i, p in enumerate(PROJECTS):
        pages[page_file(p)] = page_case(p, i, preview)
    os.makedirs(out, exist_ok=True)
    for name, text in pages.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)
    urls = "".join(f"<url><loc>{CONFIG['site_url']}/{'' if n == 'index.html' else n.replace('.html', '')}</loc></url>" for n in pages if n != "404.html")
    with open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    return list(pages)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        print(build(sys.argv[2], preview=True))
    else:
        print(build(ROOT))
