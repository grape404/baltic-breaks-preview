#!/usr/bin/env python3
"""Generate the Baltic-Breaks static site from data/tours.json.

Outputs (relative to SITE_ROOT, which is the repo root):
  index.html
  tours/index.html
  tours/<slug>.html
  sitemap.xml

Reuses the existing img/ and uploads/ trees already in the repo, so no
image duplication. Run with:  python3 build.py
"""
import json, os, re, html, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "tours.json")
SITE_NAME = "Baltic-Breaks"
TAGLINE = "Golf Tour Operator"
CONTACT = {
    "email": "info@baltic-breaks.com",
    "phone": "+372 6311 796",
    "addr": "Mere pst 4, 10111 Tallinn, Estonia",
    "web": "baltic-breaks.com",
}

CAT_ORDER = ["Golf Travel", "Golf Travel for Groups", "Golf Tournaments",
             "Beach Holiday", "Culture Program", "Skiing Holidays", "Gourmet Tours"]


def esc(s):
    return html.escape(s or "", quote=True)


def rel(depth, path):
    """Prefix a repo-relative asset path for a page at given depth."""
    return ("../" * depth) + path


def money(p):
    if not p:
        return None
    return "€{:,.0f}".format(p).replace(",", " ")


def head(depth, title, desc, extra=""):
    base = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{base}favicon.png">
<link rel="stylesheet" href="{base}assets/site.css">
{extra}
</head>
<body>
"""


def header(depth, active=""):
    base = "../" * depth
    def cls(name):
        return ' class="on"' if name == active else ""
    return f"""
<header class="site-head">
  <div class="head-in">
    <a class="brand" href="{base}index.html">
      <img src="{base}assets/img/logo-icon.png" alt="{SITE_NAME}">
      <span class="bt"><b>{SITE_NAME}</b><span>{TAGLINE}</span></span>
    </a>
    <nav class="nav">
      <a href="{base}tours/index.html">Tours</a>
      <a href="{base}tours/index.html?c=Golf%20Tournaments">Tournaments</a>
      <a href="{base}tours/index.html?c=Golf%20Travel%20for%20Groups">Groups</a>
      <a href="#contact">Contact</a>
      <a class="cta" href="{base}tours/index.html">Browse tours</a>
    </nav>
  </div>
</header>
"""


def footer(depth):
    base = "../" * depth
    return f"""
<footer class="site-foot" id="contact">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>{SITE_NAME}</h4>
        <a href="mailto:{CONTACT['email']}">{CONTACT['email']}</a>
        <a href="tel:{CONTACT['phone'].replace(' ', '')}">{CONTACT['phone']}</a>
        <a>{CONTACT['addr']}</a>
      </div>
      <div>
        <h4>Explore</h4>
        <a href="{base}tours/index.html">All tours</a>
        <a href="{base}tours/index.html?c=Golf%20Travel">Golf travel</a>
        <a href="{base}tours/index.html?c=Culture%20Program">Culture programmes</a>
        <a href="{base}tours/index.html?c=Beach%20Holiday">Beach holidays</a>
      </div>
      <div>
        <h4>Languages</h4>
        <a href="{base}en/index.html">English</a>
        <a href="{base}ru/index.html">Русский</a>
        <a href="{base}ee/index.html">Eesti</a>
      </div>
    </div>
    <div class="foot-bot">
      <span>&copy; {SITE_NAME} Golf Tour Operator</span>
      <span>IAGTO member</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def card(t, depth):
    base = "../" * depth
    img = t["images"][0] if t["images"] else ""
    src = base + img if img else ""
    price = money(t.get("price"))
    if price:
        phtml = f'<span class="price">{price} <small>pp</small></span>'
    else:
        phtml = '<span class="price req">Price on request</span>'
    meta = esc(t.get("category", ""))
    return f"""
    <a class="card" href="{base}tours/{esc(t['slug'])}.html" data-cat="{esc(t.get('category',''))}" data-title="{esc(t['title'].lower())}">
      <div class="card-img">
        {'<img src="' + src + '" alt="' + esc(t['title']) + '" loading="lazy">' if src else ''}
        <span class="card-tag">{meta}</span>
      </div>
      <div class="card-body">
        <h3>{esc(t['title'])}</h3>
        <div class="card-foot">{phtml}<span class="card-arrow">&rarr;</span></div>
      </div>
    </a>"""


def build_index(tours):
    base = ""
    featured = [t for t in tours if t.get("price")][:6]
    if len(featured) < 6:
        featured += [t for t in tours if not t.get("price")][:6 - len(featured)]

    cats = {}
    for t in tours:
        c = t.get("category", "")
        cats[c] = cats.get(c, 0) + 1
    ordered = [c for c in CAT_ORDER if c in cats]

    cat_tiles = ""
    for c in ordered:
        cat_tiles += f"""
      <a class="card" href="{base}tours/index.html?c={c.replace(' ', '%20')}">
        <div class="card-body" style="padding:26px 24px">
          <h3 style="margin-bottom:6px">{esc(c)}</h3>
          <div class="card-meta" style="margin:0">{cats[c]} tour{'s' if cats[c] != 1 else ''}</div>
        </div>
      </a>"""

    cards = "".join(card(t, 0) for t in featured)

    return head(0, f"{SITE_NAME} — {TAGLINE} | Golf tours, tournaments and culture travel",
                "Golf travel, golf tournaments, culture programmes, beach holidays and spa breaks across Europe and beyond.") + header(0) + f"""
<section class="hero">
  <img class="hero-bg" src="assets/img/slide1.jpg" alt="">
  <div class="hero-in">
    <span class="kicker">Since 2003 · IAGTO member</span>
    <h1>Golf travel, thoughtfully arranged</h1>
    <p>Handpicked golf resorts, tournaments and culture programmes across Europe, the Mediterranean and beyond. One operator, every detail handled.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="tours/index.html">Browse all tours</a>
      <a class="btn btn-ghost" href="#contact">Talk to us</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>Featured tours</h2>
      <p>A selection from the current programme. Every itinerary can be adapted to your dates and group.</p>
    </div>
    <div class="grid">{cards}
    </div>
    <div style="text-align:center;margin-top:44px">
      <a class="btn btn-primary" href="tours/index.html">See all {len(tours)} tours</a>
    </div>
  </div>
</section>

<section class="sec sec-soft">
  <div class="wrap">
    <div class="sec-head">
      <h2>Browse by type</h2>
      <p>From single-resort golf breaks to multi-country culture journeys.</p>
    </div>
    <div class="grid">{cat_tiles}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>Why book with {SITE_NAME}</h2>
      <p>Twenty years of arranging golf travel for groups and individuals.</p>
    </div>
    <div class="grid">
      <div class="card"><div class="card-body">
        <h3>Real golf knowledge</h3>
        <div class="card-meta" style="margin:0">We play the courses we sell. Handicap requirements, tee times and transfer times are checked, not assumed.</div>
      </div></div>
      <div class="card"><div class="card-body">
        <h3>Groups are our normal</h3>
        <div class="card-meta" style="margin:0">From four-ball trips to 40-player tournaments, with the hotel, golf and transfers handled as one package.</div>
      </div></div>
      <div class="card"><div class="card-body">
        <h3>One point of contact</h3>
        <div class="card-meta" style="margin:0">You deal with the person arranging the trip, from first enquiry to the last transfer.</div>
      </div></div>
    </div>
  </div>
</section>
""" + footer(0)


def build_tours_index(tours):
    cats = {}
    for t in tours:
        c = t.get("category", "")
        cats[c] = cats.get(c, 0) + 1
    ordered = [c for c in CAT_ORDER if c in cats]

    chips = '<button class="chip on" data-f="">All tours</button>'
    for c in ordered:
        chips += f'<button class="chip" data-f="{esc(c)}">{esc(c)} ({cats[c]})</button>'

    cards = "".join(card(t, 1) for t in tours)

    return head(1, f"All tours — {SITE_NAME}", "Browse every golf tour, tournament and culture programme.") + header(1, "tours") + f"""
<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>All tours</h2>
      <p>{len(tours)} itineraries. Filter by type, or search by destination.</p>
    </div>
    <div class="filters">
      {chips}
    </div>
    <div style="margin-bottom:26px">
      <input id="q" type="search" placeholder="Search destination or tour name…"
        style="width:100%;max-width:420px;padding:13px 18px;border:1px solid var(--line);border-radius:999px;font-size:14.5px;font-family:inherit">
    </div>
    <div class="grid" id="grid">{cards}
    </div>
    <div class="empty" id="none" style="display:none">
      <h3>No tours match that</h3>
      <p>Try a different filter, or <a href="mailto:{CONTACT['email']}">ask us directly</a>.</p>
    </div>
  </div>
</section>
<script>
(function(){{
  var grid=document.getElementById('grid');
  var cards=[].slice.call(grid.querySelectorAll('.card'));
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  var q=document.getElementById('q');
  var none=document.getElementById('none');
  var active='';
  function apply(){{
    var term=(q.value||'').toLowerCase().trim();
    var shown=0;
    cards.forEach(function(c){{
      var okCat=!active||c.dataset.cat===active;
      var okTerm=!term||c.dataset.title.indexOf(term)>-1;
      var vis=okCat&&okTerm;
      c.style.display=vis?'':'none';
      if(vis)shown++;
    }});
    none.style.display=shown?'none':'block';
  }}
  chips.forEach(function(ch){{
    ch.addEventListener('click',function(){{
      chips.forEach(function(x){{x.classList.remove('on')}});
      ch.classList.add('on');
      active=ch.dataset.f||'';
      apply();
    }});
  }});
  q.addEventListener('input',apply);
  var m=/[?&]c=([^&]*)/.exec(location.search);
  if(m){{
    var want=decodeURIComponent(m[1].replace(/\\+/g,' '));
    chips.forEach(function(ch){{ if(ch.dataset.f===want){{ ch.click(); }} }});
  }}
}})();
</script>
""" + footer(1)


def build_detail(t, depth=1):
    base = "../" * depth
    price = money(t.get("price"))
    checkout = t.get("checkoutUrl", "").strip()

    # gallery: up to 5 images, prefer full-size when it exists
    imgs = []
    for p in t["images"][:6]:
        full = p.replace("_tn.jpg", ".jpg")
        pick = full if os.path.exists(os.path.join(ROOT, full)) else p
        imgs.append(pick)
    gal = "".join(
        f'<a href="{base}{esc(i)}" target="_blank" rel="noopener">'
        f'<img src="{base}{esc(i)}" alt="{esc(t["title"])}" loading="lazy"></a>'
        for i in imgs
    )

    # description
    desc = t.get("description", "").strip()
    paras = ""
    if desc:
        chunk, buf = [], []
        for sent in re.split(r"(?<=[.!?])\s+", desc):
            buf.append(sent)
            if sum(len(x) for x in buf) > 320:
                chunk.append(" ".join(buf)); buf = []
        if buf:
            chunk.append(" ".join(buf))
        paras = "".join(f"<p>{esc(c)}</p>" for c in chunk)

    if price and checkout:
        buy = f"""
      <div class="amt">{price} <small>per person</small></div>
      <div class="per">Indicative price, from</div>
      <a class="btn btn-primary" href="{esc(checkout)}">Book and pay</a>
      <div class="note">Secure payment by card. Confirmation follows by email.</div>"""
    elif price:
        buy = f"""
      <div class="amt">{price} <small>per person</small></div>
      <div class="per">Indicative price, from</div>
      <a class="btn btn-primary" href="mailto:{CONTACT['email']}?subject={esc('Enquiry: ' + t['title'])}">Enquire about this tour</a>
      <div class="note">We confirm availability, dates and the final price by email.</div>"""
    else:
        buy = f"""
      <div class="amt" style="font-size:23px">Price on request</div>
      <div class="per">Depends on dates, group size and availability</div>
      <a class="btn btn-primary" href="mailto:{CONTACT['email']}?subject={esc('Enquiry: ' + t['title'])}">Request a quote</a>
      <div class="note">Send us your dates and group size and we will come back with a full quote.</div>"""

    return head(depth, f"{t['title']} — {SITE_NAME}",
                (desc[:150] if desc else t['title'] + " with " + SITE_NAME), "") + header(depth, "tours") + f"""
<article class="detail">
  <div class="wrap">
    <div class="crumbs">
      <a href="{base}index.html">Home</a> &nbsp;/&nbsp;
      <a href="{base}tours/index.html">Tours</a> &nbsp;/&nbsp;
      <a href="{base}tours/index.html?c={esc(t.get('category','')).replace(' ', '%20')}">{esc(t.get('category',''))}</a>
    </div>
    <div class="detail-grid">
      <div>
        <div class="gallery">{gal}</div>
      </div>
      <div>
        <div class="cat">{esc(t.get('category',''))}</div>
        <h1>{esc(t['title'])}</h1>
        <div class="buy">
          {buy}
          <ul>
            <li>Accommodation and golf arranged together</li>
            <li>Itinerary adapted to your dates</li>
            <li>Transfers and tee times coordinated</li>
          </ul>
        </div>
        <div class="prose">{paras}</div>
      </div>
    </div>
  </div>
</article>
""" + footer(depth)


def main():
    tours = json.load(open(DATA, encoding="utf-8"))
    tours.sort(key=lambda t: (t.get("category", ""), -1 if t.get("price") else 0, t["title"].lower()))

    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(build_index(tours))

    os.makedirs(os.path.join(ROOT, "tours"), exist_ok=True)
    open(os.path.join(ROOT, "tours", "index.html"), "w", encoding="utf-8").write(build_tours_index(tours))

    made = 0
    for t in tours:
        out = os.path.join(ROOT, "tours", t["slug"] + ".html")
        open(out, "w", encoding="utf-8").write(build_detail(t, 1))
        made += 1

    # sitemap
    urls = ["index.html", "tours/index.html"] + [f"tours/{t['slug']}.html" for t in tours]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>/{u}</loc></url>")
    sm.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))

    print(f"built index, tours/index, {made} tour pages, sitemap")


if __name__ == "__main__":
    main()
