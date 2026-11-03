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
    "email": "hello@hafeezoyeneyin.com",     # forwards to oyeneyinhafeez@gmail.com (Namecheap email forwarding)
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
        "tagline": "A basketball recruiting brand whose entire site plays out like a game broadcast.",
        "card": "Recruiting guidance for high school and college athletes, presented through a scoreboard-inspired identity, clear packages and an owner-managed admin portal.",
        "built_short": [
            "Scoreboard identity with a live shot clock",
            "Distinct intake paths for parents and athletes",
            "Owner-managed team and testimonials",
        ],
        "brief": [
            "Courtside Connections guides high school and college basketball players through recruiting with honest evaluations and real coach relationships, never mass emails.",
            "The site needed to carry the seriousness of the athletes it represents, present four packages without overwhelming families, and convert visitors into free player profiles, while giving the owner full control over the team and testimonials.",
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
            ("The site is the game", "A shot clock, a home-and-away scoreboard, four quarters for the process, scouting reports for packages and a scorer's table for the form. The theme carries the explanation."),
            ("Two front doors", "Parents and athletes enter through separate paths, each asked only what matters to them, from graduation year to position and game film."),
            ("Owner-managed", "Team members and testimonials are updated from a private admin portal. Every change passes through a secure server, so nothing sensitive lives in the page."),
        ],
        "palette": [
            ("#E8712B", "Court orange"),
            ("#D4A017", "Gold"),
            ("#0C1526", "Night navy"),
            ("#FAF6EE", "Chalk"),
        ],
        "fonts": [
            ("Barlow Condensed", "'Barlow Condensed', sans-serif", "MAKE IT TO THE NEXT LEVEL", "800", "uppercase"),
            ("Caveat", "'Caveat', cursive", "Coach's notes", "600", "none"),
        ],
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
        "tagline": "A festival two years from opening, with a site that makes it feel inevitable.",
        "card": "A four-day festival uniting food, art, music and conflict resolution. Phase one is live; ticketing follows.",
        "built_short": [
            "Live countdown to opening day",
            "Multi-page site spanning every part of the festival",
            "Sponsor, vendor and exhibitor applications",
        ],
        "brief": [
            "America's Spring Canvas Festival is a four-day festival planned for Memorial Day weekend 2028, built around food, art, music, competition and a year-round conflict-resolution campaign.",
            "Two years out, the site must win over sponsors, exhibitors, vendors and an audience for an event no one has yet experienced, then grow into ticketing and registration without a rebuild.",
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
            ("History as the pitch", "Super Bowl XVI, WrestleMania III and the 1994 World Cup all came to Pontiac. Placing 2028 beside them conveys the ambition at a glance."),
            ("Momentum before tickets", "With nothing yet to sell, the countdown and update sign-up carry the momentum a ticket button ordinarily would."),
            ("Built in phases", "Phase one brings the festival to the public and secures sponsors now. Ticketing joins the same foundation later, with no need to start over."),
        ],
        "palette": [
            ("#FDD10A", "Canvas yellow"),
            ("#0E1618", "Stage black"),
            ("#FFFFFF", "White"),
        ],
        "fonts": [
            ("Oswald", "'Oswald', sans-serif", "THE CANVAS OPENS IN", "700", "uppercase"),
            ("Poppins", "'Poppins', sans-serif", "Four days · Eight stages", "600", "none"),
        ],
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
        "tagline": "A tutoring platform that shows parents precisely where the learning gap lies.",
        "card": "My own tutoring company. An interactive skill map leads the homepage, supported by bookings, payments and student dashboards.",
        "built_short": [
            "Interactive prerequisite map",
            "Session packages with online checkout",
            "Student accounts, homework and progress reports",
        ],
        "brief": [
            "NextGen Tutoring is my own company. Where most tutoring guesses at the problem, NextGen maps every math skill to the skills beneath it, tracing a seventh grader's trouble with ratios back to the fraction gap actually responsible.",
            "The site had to make that idea clear within seconds to a parent encountering it for the first time, then run the business behind it: bookings, payments, homework and progress reporting.",
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
            ("The product leads", "Rather than a stock photograph, the homepage opens on the skill map itself. Parents understand the method before reading a word."),
            ("Transparent pricing", "Three clear packages, per-session pricing shown openly and a complimentary first session. Nothing renews automatically."),
            ("It runs the business", "Beneath the public site sit accounts, payments, homework delivery and reporting, all on a single, cohesive stack."),
        ],
        "palette": [
            ("#C9A84C", "Gold"),
            ("#FBF7EC", "Paper"),
            ("#F1EBDC", "Sand"),
            ("#1C1A16", "Ink"),
        ],
        "fonts": [
            ("Fraunces", "'Fraunces', serif", "See exactly where the gap is.", "600", "none"),
            ("Instrument Sans", "'Instrument Sans', sans-serif", "Diagnose · Plan · Close the gap", "700", "none"),
        ],
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
        "card": "Custom tables, shelving and signage from reclaimed wood, steel and resin. A story-led site that turns admiration into qualified inquiries.",
        "built_short": ["Story-led homepage", "Lead time and deposit stated up front", "Quote request flow"],
        "brief": [
            "Timber & Forge Creations crafts custom tables, shelving and signage from reclaimed wood, steel and epoxy resin. Every piece is one of a kind.",
            "The site needed to convey the story behind the work, set honest expectations around time and investment, and turn that interest into qualified quote requests rather than price-shopping messages.",
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
            ("Expectations, stated plainly", "A 15–30 day lead time and 50% deposit sit directly beneath the first button, so every inquiry arrives already informed."),
            ("Story first", "The “perfectly imperfect” philosophy carries the page, which is precisely what distinguishes a handmade table from a catalog one."),
            ("Instagram as the living gallery", "New pieces are already shared on Instagram. The site points there, so the portfolio never grows stale."),
        ],
        "palette": [
            ("#0E1B2A", "Forge navy"),
            ("#C98B4F", "Walnut (accent)"),
            ("#FFFFFF", "White"),
            ("#F2FCFC", "Mist"),
        ],
        "fonts": [
            ("Inter", "'Inter', sans-serif", "Built to last.", "800", "none"),
        ],
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
        "tagline": "A Dallas bar crawl that can be understood and booked in under a minute, on a phone.",
        "card": "Guided bar crawls every Friday and Saturday in Dallas. A mobile-first site with a booking calendar that opens only on crawl nights.",
        "built_short": ["Friday and Saturday booking calendar", "Ticket selector with live total", "FAQ and private-event inquiries"],
        "brief": [
            "Tipsy Trail hosts guided bar crawls every Friday and Saturday night in Dallas's Bishop Arts District.",
            "Most visitors arrive on a phone from a social post. The site had to sell the night quickly: what it is, what the $40 ticket includes and how to reserve a place, before attention moves on.",
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
            ("Only the right nights", "The calendar offers Fridays and Saturdays alone, so no one can book an evening that doesn't exist."),
            ("Answers before questions", "Age requirements, solo guests, cover charges and what's included are all addressed on the page, so fewer questions need to be sent."),
            ("Personality in the type", "A bold, playful display face and vivid pink palette match the energy of a night out, not a corporate event."),
        ],
        "palette": [
            ("#E85DA8", "Party pink"),
            ("#FFF9F5", "Blush"),
            ("#333333", "Charcoal"),
            ("#FFFFFF", "White"),
        ],
        "fonts": [
            ("Boogaloo", "'Boogaloo', cursive", "TIPSY TRAIL", "400", "uppercase"),
            ("Nunito", "'Nunito', sans-serif", "Explore. Sip. Repeat.", "800", "none"),
        ],
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
<meta property="og:site_name" content="Hafeez Oyeneyin">
<meta property="og:image" content="{CONFIG['site_url']}/assets/brand/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Hafeez Oyeneyin: websites, crafted with intention.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{CONFIG['site_url']}/assets/brand/og-image.png">
<link rel="icon" href="{FAVICON}">
<link rel="icon" type="image/png" sizes="32x32" href="assets/brand/favicon-32.png">
<link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png">
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
        <p class="say">Let's build something <em>remarkable.</em></p>
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


def cta(title="Begin your <em>project.</em>", text="Share a few details about what you're building. You'll receive a reply within two business days to arrange a complimentary consultation."):
    return f"""<section class="cta" aria-labelledby="cta-title">
  <div class="wrap reveal">
    <h2 class="display" id="cta-title">{title}</h2>
    <p>{text}</p>
    <a class="btn btn-primary" href="contact.html">Start a project <span class="arr" aria-hidden="true">→</span></a>
  </div>
</section>
"""


SERVICES = [
    ("Launch", "a polished first impression", "A refined, focused site that establishes credibility from the first visit.",
     ["One to three pages, designed mobile-first", "Inquiry form delivered to your inbox", "Domain, hosting and launch fully handled", "Search-ready titles and descriptions"], "tipsy-trail"),
    ("Grow", "a complete brand presence", "A fully bespoke, multi-page site that tells your story and showcases your services.",
     ["Multi-page site shaped around your brand", "Two homepage concepts to choose between", "Sign-up and inquiry forms routed to the right inbox", "Integrated calendars, booking and social feeds"], "timber-and-forge"),
    ("Platform", "a site that runs your operations", "For organizations that need more than a website: portals, accounts and payments, built in.",
     ["Admin portal to manage your own content", "Registrations, waitlists and member logins", "Online payments and ticketing", "A clear, plain-language operating guide"], "courtside-connections"),
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
  <li><h3>Discovery</h3><p>A complimentary 15-minute conversation about your business, your audience and what the site must accomplish.</p></li>
  <li><h3>Proposal &amp; direction</h3><p>A fixed-price proposal, followed by two distinct homepage concepts to choose between.</p></li>
  <li><h3>Build &amp; refinement</h3><p>Follow progress on a private preview link and refine the details together as it takes shape.</p></li>
  <li><h3>Launch &amp; handover</h3><p>Your domain is connected, the site goes live, and you receive a clear guide to managing it.</p></li>
</ol>"""


def faq(items):
    return '<div class="faq reveal">' + "".join(
        f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in items) + "</div>"


FAQ_GENERAL = [
    ("How is a project priced?", "Every project is quoted at a fixed price following a complimentary 15-minute consultation, based on what the site needs to accomplish. You'll know the full investment before work begins, and it changes only if the scope does."),
    ("Are there ongoing monthly fees?", "No. Because your site is custom-built, there's no website-builder subscription. The only recurring cost is your domain name, typically $10–15 per year. Sites with accounts or payments may carry modest usage-based service fees, which are outlined in your proposal."),
    ("Can I update the site myself?", "Yes. Sites can include an admin portal for managing programs, events, imagery and announcements, accompanied by a clear guide. On simpler sites, small text changes are handled for you at no charge."),
    ("I already have a website. Can you rebuild it?", "Yes. Your existing content is carried over from your current site or builder, rebuilt to a higher standard, and your domain is moved without disrupting your email. Keep your current plan active until the new site launches."),
    ("Do you work with clients remotely?", "Yes. Clients are welcome from anywhere. Consultations, design reviews and a private live preview all take place online."),
    ("What is the typical timeline?", "Most sites launch within one to three weeks of the initial consultation. Projects with portals, accounts or payments take longer, and a detailed timeline accompanies every proposal."),
    ("How does payment work?", f"Invoices are issued by {CONFIG['business']}, with payment details included on each. Any work beyond the agreed scope is quoted separately before it begins."),
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
    return head("Hafeez Oyeneyin | Custom-Coded Websites", "Bespoke websites designed and engineered for businesses, nonprofits and founders. Fast, distinctive and entirely yours.", "index.html", pv) + header("index.html") + f"""
<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <canvas id="field" aria-hidden="true"></canvas>
    <div class="wrap">
      <p class="status-pill"><i aria-hidden="true"></i>Accepting new projects</p>
      <h1 id="hero-title" class="display">
        <span class="line"><span>Websites, crafted</span></span>
        <span class="line"><span>with <em>intention.</em></span></span>
      </h1>
      <p class="lede">I design and engineer bespoke websites for businesses, nonprofits and founders. Every site is fast, distinctive and entirely yours, with no templates and no platform fees.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="contact.html">Start a project <span class="arr" aria-hidden="true">→</span></a>
        <a class="btn" href="work.html">View the work</a>
      </div>
    </div>
  </section>

  <section class="clients" aria-label="Clients">
    <div class="wrap">
      <p>Selected clients</p>
      <div class="client-viewport"><div class="client-track">
        <ul class="client-list">{clients}</ul>
        <ul class="client-list dup" aria-hidden="true">{clients.replace('<a ', '<a tabindex="-1" ')}</ul>
      </div></div>
    </div>
  </section>

  <section class="section" aria-labelledby="work-title">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Selected work</p><h2 id="work-title" class="display">Work that <em>performs</em></h2></div>
        <p>Every engagement begins with how a client actually operates. The site is then designed and engineered around it.</p>
      </div>
      <div class="feature-list">
        {''.join(feats)}
      </div>
      <p style="margin-top:80px"><a class="btn" href="work.html">View all {len(PROJECTS)} projects <span class="arr" aria-hidden="true">→</span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="look-title">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Identity</p><h2 id="look-title" class="display">A distinct identity <em>for every client</em></h2></div>
        <p>Nothing is templated. Typography, color and voice are chosen for each brand, so no two sites look alike.</p>
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
        <div><p class="eyebrow">Services</p><h2 id="services-title" class="display">Services, <em>tailored</em></h2></div>
        <p>Each engagement is scoped on a complimentary call and priced as a fixed quote, agreed before any work begins.</p>
      </div>
      <div class="svc-list">
        {svc_rows()}
      </div>
      <p style="margin-top:40px"><a class="link-arrow" href="services.html">Explore all services <span aria-hidden="true">→</span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="process-title">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Process</p><h2 id="process-title" class="display">A <em>considered</em> process</h2></div>
        <p>Transparent at every stage: what is happening, what comes next and what it costs.</p>
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
      <h1 class="display">Selected <em>work</em></h1>
      <p class="intro">Every project shown here is live. Open any case study to explore the real site, running exactly as its customers experience it.</p>
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
    note = "This is the live site. Explore it directly, or switch to the mobile view." if p["live"] else ""
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
          <button type="button" data-device="phone" data-target="{fid}" aria-pressed="false">Mobile</button>
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
      <h2><small>Brief</small>The challenge</h2>
      <div class="prose">{brief}</div>
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap cs-grid reveal">
      <h2><small>Build</small>The solution</h2>
      <ul class="featlist">{feats}</ul>
    </div>
  </section>

  <section class="cs-sec">
    <div class="wrap">
      <div class="cs-grid reveal" style="margin-bottom:48px"><h2><small>Details</small>Considered details</h2><div></div></div>
      <div class="details">{details}</div>
    </div>
  </section>
{quote}
  <section class="cs-sec">
    <div class="wrap">
      <div class="cs-grid reveal" style="margin-bottom:48px"><h2><small>Identity</small>Visual identity</h2><div class="prose"><p style="font-size:1.12rem;color:var(--text-2)">The palette and typography defined for this brand.</p></div></div>
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
{cta("Your site, <em>built to this standard.</em>")}</main>
""" + footer()


def page_services(pv):
    addons = [
        ("Admin portal", "Update programs, team members, events and imagery yourself, from any device.", "courtside-connections"),
        ("Bookings + calendars", "Event calendars and booking flows that offer only the times you actually run.", "tipsy-trail"),
        ("Sign-up + application forms", "Registrations and vendor or sponsor applications, routed to the right inbox and securely stored.", "spring-canvas-festival"),
        ("Online payments", "Seamless checkout for sessions, packages or tickets, with receipts handled automatically.", "nextgen-tutoring"),
        ("Accounts + dashboards", "Private member logins with personal dashboards, history and downloads.", "nextgen-tutoring"),
        ("Migration from a website builder", "Your content carried over and rebuilt properly, with your domain moved and your email left undisturbed.", None),
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
      <h1 class="display">Services, <em>tailored</em></h1>
      <p class="intro">From a refined single page to a full platform with accounts and payments. Every engagement is priced as a fixed quote after a complimentary consultation, with no monthly platform fees and full ownership from day one.</p>
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
        <div><p class="eyebrow">Add-ons</p><h2 class="display">Capabilities, <em>proven live</em></h2></div>
        <p>Each can be added to any project, and each is already running on a client site today.</p>
      </div>
      <div class="addons">{''.join(cards)}</div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="section-head reveal">
        <div><p class="eyebrow">Process</p><h2 class="display">A <em>considered</em> process</h2></div>
        <p>Transparent at every stage: what is happening, what comes next and what it costs.</p>
      </div>
      {STEPS}
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="section-head reveal"><div><p class="eyebrow">FAQ</p><h2 class="display">Frequently <em>asked</em></h2></div></div>
      {faq(FAQ_GENERAL)}
    </div>
  </section>
{cta()}</main>
""" + footer()


def page_about(pv):
    principles = [
        ("Bespoke by default", "No themes and no page builders. Every site is designed and engineered for the business it represents."),
        ("Full ownership", "The code, the domain and the content are yours. No platform can raise your price or lock you in."),
        ("Mobile-first performance", "Most visitors arrive on a phone. Every site is built for that experience first and tested on real devices."),
        ("Clarity throughout", "A fixed quote before work begins, a timeline you can rely on, and advance notice before anything affects scope."),
    ]
    pr = "".join(f'<article class="principle reveal"><h3>{E(t)}</h3><p>{E(d)}</p></article>' for t, d in principles)
    stack = ["HTML", "CSS", "JavaScript", "Firebase", "Firestore", "Cloudflare Workers", "Cloudflare R2", "Stripe", "GitHub Pages", "Formspree", "Claude API"]
    st = "".join(f"<li>{E(s)}</li>" for s in stack)
    return head("About | Hafeez Oyeneyin", "A direct line to the builder: how I design and engineer bespoke websites.", "about.html", pv) + header("about.html") + f"""
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">About</p>
      <h1 class="display">A direct line to <em>the builder</em></h1>
      <p class="intro">I'm Hafeez, a software engineer. I design and engineer every site personally, and you work directly with me from the first conversation through launch and beyond, wherever you're based.</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <div class="section-head reveal"><div><p class="eyebrow">Principles</p><h2 class="display">How I <em>work</em></h2></div></div>
      <div class="principles">{pr}</div>
    </div>
  </section>
  <section class="section">
    <div class="wrap two-col reveal">
      <div><p class="eyebrow">Stack</p><h2 class="display">The <em>toolkit</em></h2></div>
      <div>
        <div class="prose"><p>Lean, fast front-end code, supported by proven infrastructure for accounts, data, payments and storage. Heavier frameworks are used only when a project calls for them.</p></div>
        <ul class="stack">{st}</ul>
      </div>
    </div>
  </section>
{cta()}</main>
""" + footer()


def page_contact(pv):
    em, ph = CONFIG["email"], CONFIG["phone"]
    return head("Contact | Hafeez Oyeneyin", "Begin your project. Share a few details and receive a reply within two business days.", "contact.html", pv) + header("contact.html") + f"""
<main id="main">
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Contact</p>
      <h1 class="display">Let's discuss your <em>project</em></h1>
      <p class="intro">Share a few details and you'll receive a reply within two business days to arrange a complimentary 15-minute consultation.</p>
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
          <li><b>Your inquiry is reviewed</b><span>with a reply within two business days.</span></li>
          <li><b>A complimentary consultation</b><span>to discuss your business and what the site must accomplish.</span></li>
          <li><b>A fixed-price proposal</b><span>with a clear timeline, before any work begins.</span></li>
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
          <legend>What are you looking for?</legend>
          <div class="chips">
            <label class="chip"><input type="radio" name="project_type" id="t-new" value="New website"><span>New website</span></label>
            <label class="chip"><input type="radio" name="project_type" id="t-redo" value="Redesign of an existing site"><span>Redesign of an existing site</span></label>
            <label class="chip"><input type="radio" name="project_type" id="t-custom" value="Admin portal, bookings or payments"><span>Admin portal, bookings or payments</span></label>
            <label class="chip"><input type="radio" name="project_type" id="t-unsure" value="Still exploring"><span>Still exploring</span></label>
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
          <label for="f-when">Ideal timeline</label>
          <select id="f-when" name="timeline">
            <option value="">Choose one</option>
            <option>As soon as possible</option>
            <option>Within a month</option>
            <option>1–3 months</option>
            <option>Just exploring</option>
          </select>
        </div>
        <div class="field"><label for="f-msg">Project details</label><textarea id="f-msg" name="message" placeholder="Your business, what the site should accomplish, and any sites you admire…"></textarea></div>
        <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="form-foot">
          <button class="btn btn-primary" type="submit" id="f-submit">Send inquiry <span class="arr" aria-hidden="true">→</span></button>
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
