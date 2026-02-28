import os

BOOKMARKS_FILE = 'bm.md'
HTML_FILE = 'bm1.html'

def load_bookmarks():
    bookmarks = []
    if not os.path.exists(BOOKMARKS_FILE):
        return bookmarks

    with open(BOOKMARKS_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    rows = [line.strip() for line in lines if line.startswith('|') and not line.startswith('|--')]
    for row in rows[1:]:
        parts = [col.strip() for col in row.strip('|').split('|')]
        if len(parts) == 4:
            bookmarks.append({
                'title': parts[0],
                'url': parts[1],
                'tags': parts[2],
                'notes': parts[3]
            })
    return bookmarks

def generate_html(bookmarks):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>📌🅝🅞🅞🅡🅚🅤🅡🅘</title>
  <style>
    body {
      background: linear-gradient(to bottom, #f5f7fa, #eaeef3);
      color: #333;
      margin: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
      font-size: 0.95em;
      padding-top: 60px; /* space for fixed header */
    }
    .dark-mode {
      background: #111;
      color: #eee;
    }
    header {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      background: #1e2a38;
      color: #fff;
      padding: 10px 15px;
      font-size: 1em;
      font-weight: bold;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      z-index: 1000;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .container {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      justify-content: center;
      padding: 10px;
    }
    .card {
      flex: 1 1 260px;
      background: linear-gradient(135deg, #ffffff, #f0f4ff);
      border: 1px solid #ddd;
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      cursor: pointer;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    .card a {
      color: #0366d6;
      text-decoration: none;
      word-break: break-word;
      font-weight: bold;
      font-size: 1em;
    }
    .card a:hover {
      text-decoration: underline;
    }
    .dark-mode .card {
      background: #222;
      border-color: #444;
    }
    .dark-mode a {
      color: #1e90ff;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85em; /* smaller font for status */
      margin-bottom: 6px;
    }
    .status {
      font-size: 0.8em;
      color: #555;
    }
    input[type="text"] {
      padding: 6px;
      margin-left: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      width: 200px;
    }
    .dark-mode input[type="text"] {
      background-color: #222;
      color: #fff;
      border: 1px solid #444;
    }
    button {
      margin-left: 10px;
      padding: 6px 10px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      background: #FFD700;
      color: #000;
      font-weight: bold;
    }
    .card[title] {
      position: relative;
    }
    .card[title]:hover::after {
      content: attr(title);
      position: absolute;
      bottom: 100%;
      left: 10px;
      background: #0366d6;
      color: #fff;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 0.8em;
      white-space: nowrap;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
  </style>
  <script>
    function filterCards() {
      const input = document.getElementById("filterInput").value.toLowerCase();
      const cards = document.querySelectorAll(".card");
      cards.forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(input) ? "" : "none";
      });
    }

    async function validateURLs() {
      const links = document.querySelectorAll(".bookmark-link");
      for (const link of links) {
        const status = link.closest(".card").querySelector(".status");
        try {
          await fetch(link.href, { method: "HEAD", mode: "no-cors" });
          status.textContent = "✅";
        } catch {
          status.textContent = "❌";
        }
      }
    }

    window.addEventListener("DOMContentLoaded", validateURLs);
  </script>
</head>
<body>
  <header>
    <div>📌🅝🅞🅞🅡🅚🅤🅡🅘</div>
    <div>
      <input type="text" id="filterInput" placeholder="Search..." onkeyup="filterCards()">
      <button id="theme-button">☀️</button>
    </div>
    <div class="watermark">© Naravu. All rights reserved.</div><div></div>

<style>
  .watermark {
    position: fixed;
    top: 50%;
    left: 0;
    transform: rotate(-90deg) translate(-50%, 0);
    transform-origin: left top;
    font-size: 0.8em;
    color: rgba(0,0,0,0.3); /* subtle watermark color */
    pointer-events: none;    /* ensures it doesn’t block clicks */
    z-index: 9999;
  }
</style>

    </div>
  </header>
  <div class="container">
"""
    for idx, b in enumerate(bookmarks, 1):
        url = b['url'].strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        html += f"""    <div class="card" onclick="window.open('{url}', '_blank')" title="{b['title']}">
      <div class="card-header"><b>🔢 {idx}</b><span class="status">⏳</span></div>
      <div><a href="{url}" class="bookmark-link" target="_blank">{b['title']}</a></div>
      <div>🔗 {url}</div>
      <div>🏷️ {b['tags']}</div>
      <div>🔖 {b['notes']}</div>
    </div>
"""

    html += """  </div>
  <script>
    const themeButton = document.getElementById("theme-button");
    const body = document.body;
    themeButton.addEventListener("click", () => {
      body.classList.toggle("dark-mode");
      themeButton.textContent = body.classList.contains("dark-mode") ? "🌙" : "☀️";
    });
  </script>
</body>
</html>"""

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ HTML exported {HTML_FILE}")

if __name__ == "__main__":
    generate_html(load_bookmarks())
