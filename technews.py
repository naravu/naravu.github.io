import feedparser
from html import escape
from datetime import datetime, timezone

FEEDS = [
    "https://www.darkreading.com/rss.xml",
    "https://lwn.net/headlines/rss",
    "https://lxer.com/rss/",
    "https://sysadvent.blogspot.com/feeds/posts/default",
    "https://www.schneier.com/feed/"
]

# Use timezone-aware UTC now to avoid deprecation warnings
YEAR = datetime.now(timezone.utc).year

def extract_image(entry):
    """Try common RSS image fields and links."""
    if 'media_content' in entry:
        mc = entry.media_content
        if isinstance(mc, (list, tuple)) and mc:
            return mc[0].get('url')
    if 'media_thumbnail' in entry:
        mt = entry.media_thumbnail
        if isinstance(mt, (list, tuple)) and mt:
            return mt[0].get('url')
    for link in entry.get('links', []):
        if link.get('type', '').startswith('image'):
            return link.get('href')
    if 'enclosures' in entry:
        for enc in entry.enclosures:
            if enc.get('type', '').startswith('image'):
                return enc.get('href')
    return None

def truncate(text, length=220):
    """Truncate text to a given length, adding an ellipsis if needed."""
    if not text:
        return "N/A"
    text = text.strip()
    return (text[:length].rstrip() + "…") if len(text) > length else text

def build_card(article):
    """Return HTML for a single article card. Title is the clickable 'read more' link."""
    img_html = f'<img src="{escape(article["image"])}" alt="News image">' if article["image"] else ""
    title_link = (
        f'<a href="{escape(article["link"])}" target="_blank" rel="noopener noreferrer" title="Read more">'
        f'{escape(article["title"])}</a>'
    )
    return f"""
    <article class="card" data-source="{escape(article['source'])}">
        {img_html}
        <h2 class="card-title">{title_link}</h2>
        <p class="card-meta"><strong>Date:</strong> {escape(article['date'])} &nbsp; • &nbsp; <strong>Source:</strong> {escape(article['source'])}</p>
        <p class="card-summary">{escape(article['summary'])}</p>
    </article>
    """

# Collect articles (optimized loop, graceful fallbacks)
articles = []
for url in FEEDS:
    feed = feedparser.parse(url)
    entries = getattr(feed, "entries", []) or []
    feed_title = feed.feed.get("title", url) if hasattr(feed, "feed") else url
    for entry in entries[:5]:
        articles.append({
            "title": entry.get("title", "Untitled"),
            "link": entry.get("link", "#"),
            "source": feed_title,
            "image": extract_image(entry),
            "date": entry.get("published", entry.get("updated", "N/A")),
            "summary": truncate(entry.get("summary", entry.get("description", "N/A")), length=220)
        })

# Build HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gradua — News Aggregator</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  :root{{
    --bg:#f4f6f8;
    --card:#ffffff;
    --muted:#6b7280;
    --accent:#1e90ff;
    --accent-contrast:#ffffff;
    --shadow-1: 0 8px 20px rgba(16,24,40,0.12);
    --shadow-3: 0 20px 60px rgba(16,24,40,0.12);
    --radius:14px;
    --header-height:55px;
    --max-width:1280px;
  }}

  html,body{{height:100%;margin:0;}}
  body{{
    font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,"Helvetica Neue",Arial;
    background:var(--bg);
    color:#0f172a;
    margin:0;
    padding-top:var(--header-height);
    transition:background 0.45s ease,color 0.45s ease;
    -webkit-font-smoothing:antialiased;
    -moz-osx-font-smoothing:grayscale;
  }}
  body.dark{{
    --bg:#0b0f12;
    --card:#0f1720;
    --muted:#9aa6b2;
    --accent:#90caf9;
    --accent-contrast:#0b1726;
  }}

  /* Fixed header */
  header{{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:var(--header-height);
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    padding:12px 20px;
    box-sizing:border-box;
    background:linear-gradient(90deg,var(--accent),#0f7be6);
    color:var(--accent-contrast);
    z-index:1200;
    transition:background 0.45s ease,backdrop-filter 0.45s ease;
    backdrop-filter: blur(6px);
  }}
  body.dark header{{ background:linear-gradient(90deg,#2b2b2b,#1f2937); }}

  .left-controls{{ display:flex; align-items:center; gap:12px; }}

  /* Hamburger button */
  .hamburger{{
    width:44px;
    height:44px;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    border-radius:10px;
    background:rgba(255,255,255,0.12);
    border:0;
    color:var(--accent-contrast);
    cursor:pointer;
    transition:transform 0.15s ease, background 0.2s ease;
    font-size:20px;
  }}
  .hamburger:active{{ transform:translateY(1px); }}
  body.dark .hamburger{{ background:rgba(255,255,255,0.06); }}

  .brand{{ font-weight:700; letter-spacing:0.2px; font-size:16px; }}

  .header-controls{{ display:flex; align-items:center; gap:12px; font-size:13px; }}

  .search-box input{{
    width:260px;
    max-width:40vw;
    padding:8px 10px;
    border-radius:8px;
    border:0;
    outline:none;
    font-size:13px;
    background:rgba(255,255,255,0.95);
    color:#0f172a;
    box-shadow:0 1px 0 rgba(0,0,0,0.03) inset;
    transition:background 0.25s ease, color 0.25s ease;
  }}
  body.dark .search-box input{{ background:#0b1220; color:var(--muted); }}

  .theme-toggle{{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:8px;
    padding:8px 10px;
    border-radius:8px;
    border:0;
    cursor:pointer;
    background:var(--card);
    color:var(--accent);
    font-weight:600;
    box-shadow:var(--shadow-1);
    transition:transform 0.18s ease, box-shadow 0.18s ease;
  }}
  .theme-toggle:active{{ transform:translateY(1px); }}
  body.dark .theme-toggle{{ background:#111827; color:var(--accent); box-shadow:none; }}

  /* Off-canvas menu */
  .offcanvas {{
    position: fixed;
    top: 0;
    left: -320px;
    width: 300px;
    height: 100vh;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    background: linear-gradient(180deg, #ffffff, #f7fbff);
    box-shadow: 8px 0 30px rgba(2,6,23,0.12);
    z-index: 1250;
    padding: 20px;
    box-sizing: border-box;
    transition: left 0.32s cubic-bezier(.2,.9,.2,1);
    border-right: 1px solid rgba(15,23,42,0.04);
  }}
  body.dark .offcanvas {{ background: linear-gradient(180deg,#0b0f12,#071018); border-right-color: rgba(255,255,255,0.03); }}
  .offcanvas.open {{ left: 0; }}

  .offcanvas h3 {{ margin:0 0 12px 0; font-size:16px; }}
  .menu-list {{ list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:8px; }}
  .menu-list a {{
    display:flex;
    align-items:center;
    gap:10px;
    padding:10px 12px;
    border-radius:8px;
    text-decoration:none;
    color:#0f172a;
    font-weight:600;
    background:transparent;
    transition:background 0.18s ease, color 0.18s ease;
  }}
  .menu-list a:hover {{ background:rgba(30,144,255,0.08); color:var(--accent); }}
  body.dark .menu-list a {{ color:#cbd5e1; }}
  body.dark .menu-list a:hover {{ background:rgba(144,202,249,0.06); color:var(--accent); }}

  .offcanvas-footer {{
    margin-top:16px;
    padding-top:12px;
    border-top:1px solid rgba(15,23,42,0.04);
    font-size:12px;
    color:var(--muted);
  }}
  body.dark .offcanvas-footer {{ border-top-color: rgba(255,255,255,0.03); color:var(--muted); }}

  /* Page title */
  .page-title{{ text-align:center; margin:18px 0 6px; font-size:20px; font-weight:600; color:inherit; }}

  /* Grid: 4 columns on wide screens */
  .container{{
    width:100%;
    max-width:var(--max-width);
    margin:0 auto;
    padding:18px;
    box-sizing:border-box;
    display:grid;
    grid-template-columns: repeat(4, minmax(240px, 1fr));
    gap:20px;
  }}

  /* Responsive fallbacks */
  @media (max-width:1200px) {{
    .container {{ grid-template-columns: repeat(3, minmax(220px, 1fr)); }}
  }}
  @media (max-width:900px) {{
    .container {{ grid-template-columns: repeat(2, minmax(220px, 1fr)); }}
  }}
  @media (max-width:640px) {{
    .container {{ grid-template-columns: 1fr; }}
    .search-box input{{ width:140px; }}
    header{{ padding:10px 12px; }}
    body{{ padding-top:72px; }}
    .offcanvas{{ width:260px; left:-280px; }}
    .offcanvas.open{{ left:0; }}
  }}

  /* Card with 3D shadow effect */
  .card{{ background:var(--card); border-radius:var(--radius); padding:16px; box-sizing:border-box; box-shadow: var(--shadow-1), 0 6px 18px rgba(16,24,40,0.06); transform-style:preserve-3d; transition: transform 0.35s cubic-bezier(.2,.9,.2,1), box-shadow 0.35s ease, background 0.35s ease; will-change:transform, box-shadow; overflow:hidden; border: 1px solid rgba(15,23,42,0.03); }}
  body.dark .card{{ border-color: rgba(255,255,255,0.03); }}

  .card:hover{{ transform: translateY(-14px) rotateX(1.2deg) scale(1.02); box-shadow: var(--shadow-3), 0 28px 80px rgba(2,6,23,0.35); }}

  .card img{{ width:100%; height:auto; display:block; border-radius:10px; margin-bottom:12px; object-fit:cover; background:#e6eefc; }}

  .card-title{{ margin:0 0 8px 0; font-size:16px; line-height:1.25; font-weight:600; }}
  .card-title a{{ color:var(--accent); text-decoration:none; transition:color 0.2s ease, text-decoration 0.2s ease; }}
  .card-title a:hover{{ text-decoration:underline; }}
  .card-meta{{ margin:0 0 10px 0; color:var(--muted); font-size:12px; }}
  .card-summary{{ margin:0 0 12px 0; color: #0b1220; font-size:13px; line-height:1.45; }}
  body.dark .card-summary{{ color:#cbd5e1; }}

  /* Back to top */
  #backToTop{{ position:fixed; right:28px; bottom:28px; width:48px; height:48px; border-radius:50%; border:0; background:var(--accent); color:var(--accent-contrast); font-size:20px; display:none; align-items:center; justify-content:center; box-shadow:0 10px 30px rgba(16,24,40,0.2); cursor:pointer; z-index:1300; transition:transform 0.18s ease, opacity 0.18s ease; }}
  #backToTop:hover{{ transform:translateY(-4px); }}

  /* Overlay when offcanvas open */
  .overlay {{ position: fixed; inset: 0; background: rgba(2,6,23,0.35); opacity: 0; pointer-events: none; transition: opacity 0.28s ease; z-index:1240; }}
  .overlay.show {{ opacity: 1; pointer-events: auto; }}
</style>
</head>
<body>
<header>
  <div class="left-controls">
    <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false">☰</button>
    <div class="brand">Gradua</div>
  </div>

  <div class="header-controls">
    <div class="search-box"><input id="searchInput" type="search" placeholder="Search news..." aria-label="Search news"></div>
    <button class="theme-toggle" id="themeToggle" aria-pressed="false" title="Toggle dark theme">🌙</button>
  </div>
</header>

<!-- Off-canvas menu -->
<aside class="offcanvas" id="offcanvas" aria-hidden="true">
  <div>
    <h3>Menu</h3>
    <nav>
      <ul class="menu-list">
        <li><a href="#" data-action="all">🏠 Home</a></li>
        <li><a href="#" data-action="security">🔒 Security</a></li>
        <li><a href="#" data-action="linux">🐧 Linux</a></li>
        <li><a href="#" data-action="devops">⚙️ DevOps</a></li>
        <li><a href="#" data-action="about">ℹ️ About</a></li>
        <li><a href="#" data-action="settings">⚙️ Settings</a></li>
      </ul>
    </nav>
  </div>

  <div class="offcanvas-footer" role="contentinfo">
    <div>© {YEAR} Gradua All rights reserved.</div>
  </div>
</aside>

<div class="overlay" id="overlay" tabindex="-1"></div>

<main>
  
  <section class="container" id="newsContainer">
"""

# Append cards
for article in articles:
    html_content += build_card(article)

# Close HTML with JS
html_content += """
  </section>
</main>

<button id="backToTop" aria-label="Back to top">⬆️</button>

<script>
/* Off-canvas menu logic */
const hamburger = document.getElementById('hamburger');
const offcanvas = document.getElementById('offcanvas');
const overlay = document.getElementById('overlay');

function openMenu() {
  offcanvas.classList.add('open');
  overlay.classList.add('show');
  hamburger.setAttribute('aria-expanded', 'true');
  offcanvas.setAttribute('aria-hidden', 'false');
}
function closeMenu() {
  offcanvas.classList.remove('open');
  overlay.classList.remove('show');
  hamburger.setAttribute('aria-expanded', 'false');
  offcanvas.setAttribute('aria-hidden', 'true');
}

hamburger.addEventListener('click', () => {
  const open = offcanvas.classList.contains('open');
  if (open) closeMenu(); else openMenu();
});
overlay.addEventListener('click', closeMenu);
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeMenu();
});

/* Menu item actions (filter by data-action) */
document.querySelectorAll('.menu-list a').forEach(a => {
  a.addEventListener('click', (e) => {
    e.preventDefault();
    const action = a.getAttribute('data-action');
    closeMenu();
    // Simple client-side filters for demo: filter by keyword
    const qmap = {
      'all': '',
      'security': 'security',
      'linux': 'linux',
      'devops': 'devops',
      'about': '',
      'settings': ''
    };
    const q = qmap[action] || '';
    const input = document.getElementById('searchInput');
    input.value = q;
    input.dispatchEvent(new Event('input'));
  });
});

/* Theme toggle */
const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark');
  const pressed = document.body.classList.contains('dark');
  themeToggle.setAttribute('aria-pressed', pressed ? 'true' : 'false');
});

/* Search filter */
const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('input', (e) => {
  const q = e.target.value.trim().toLowerCase();
  const cards = document.querySelectorAll('.card');
  if (!q) {
    cards.forEach(c => c.style.display = '');
    return;
  }
  cards.forEach(card => {
    const text = card.innerText.toLowerCase();
    card.style.display = text.includes(q) ? '' : 'none';
  });
});

/* Back to top button */
const backBtn = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  const show = window.scrollY > 240;
  backBtn.style.display = show ? 'flex' : 'none';
});
backBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* Accessibility: focus outline for keyboard users */
document.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    document.body.classList.add('show-focus');
  }
});
</script>
</body>
</html>
"""

# Write to file
with open("technews.html", "w", encoding="utf-8") as f:
    f.write(html_content)