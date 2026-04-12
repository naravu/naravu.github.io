import os

BOOKMARKS_FILE = 'pri/bm/bm.md'
HTML_FILE = 'pri/bm/bm1.html'

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>📌🅝🅞🅞🅡🅚🅤🅡🅘</title>
  <script>
    function filterTable() {
      const input = document.getElementById("filterInput").value.toLowerCase();
      const rows = document.querySelectorAll("#bookmarkTable tbody tr");
      rows.forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(input) ? "" : "none";
      });
    }

    function sortTable(n) {
      const table = document.getElementById("bookmarkTable");
      const tbody = table.tBodies[0];
      const rows = Array.from(tbody.rows);
      const asc = table.getAttribute("data-sort-dir") !== "asc";
      rows.sort((a, b) => {
        const valA = a.cells[n].textContent.trim().toLowerCase();
        const valB = b.cells[n].textContent.trim().toLowerCase();
        return asc ? valA.localeCompare(valB) : valB.localeCompare(valA);
      });
      rows.forEach(row => tbody.appendChild(row));
      table.setAttribute("data-sort-dir", asc ? "asc" : "desc");
    }

    async function validateURLs() {
      const rows = document.querySelectorAll("#bookmarkTable tbody tr");
      for (const row of rows) {
        const link = row.querySelector(".bookmark-link");
        const cell = row.querySelector(".status");
        try {
          await fetch(link.href, { method: "HEAD", mode: "no-cors" });
          cell.textContent = "✅";
        } catch {
          cell.textContent = "❌";
        }
      }
    }

    window.addEventListener("DOMContentLoaded", validateURLs);
  </script>
</head>
<body style="background-color:white;color:black;transition:background-color 0.3s,color 0.3s;margin:4px;font-family:Arial,sans-serif;">
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px;align-items:center;">
    <span style="font-weight:bold;font-size:1.1rem;">📌🅝🅞🅞🅡🅚🅤🅡🅘</span>
    <input type="text" id="filterInput" placeholder="Search..." onkeyup="filterTable()" 
           style="flex:1;min-width:150px;padding:6px;border:1px solid #ccc;background-color:#f9f9f9;color:#000;font-size:1rem;">
    <button id="theme-button" style="padding:6px 10px;font-size:1.2rem;cursor:pointer;">☀️</button>
  </div>
  <div style="overflow-x:auto;">
    <table id="bookmarkTable" data-sort-dir="asc" 
           style="width:100%;border-collapse:collapse;font-size:0.9rem;min-width:500px;">
      <thead>
        <tr>
          <th onclick="sortTable(0)" title="Serial Number" 
              style="background:#FFD700;color:#fff;cursor:pointer;font-size:0.95rem;padding:6px;border-bottom:1px solid #ddd;text-align:left;">🔢</th>
          <th onclick="sortTable(1)" title="URL" 
              style="background:#FFD700;color:#fff;cursor:pointer;font-size:0.95rem;padding:6px;border-bottom:1px solid #ddd;text-align:left;">🔗</th>
          <th onclick="sortTable(2)" title="Tags" 
              style="background:#FFD700;color:#fff;cursor:pointer;font-size:0.95rem;padding:6px;border-bottom:1px solid #ddd;text-align:left;">🏷️</th>
          <th onclick="sortTable(3)" title="Description" 
              style="background:#FFD700;color:#fff;cursor:pointer;font-size:0.95rem;padding:6px;border-bottom:1px solid #ddd;text-align:left;">🔖</th>
          <th onclick="sortTable(4)" title="URL Status" 
              style="background:#FFD700;color:#fff;cursor:pointer;font-size:0.95rem;padding:6px;border-bottom:1px solid #ddd;text-align:left;">✅/❌</th>
        </tr>
      </thead>
      <tbody>
"""
    for idx, b in enumerate(bookmarks, 1):
        url = b['url'].strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        html += f"""        <tr style="border-bottom:1px solid #ddd;">
          <td style="padding:6px;text-align:left;vertical-align:top;">{idx}</td>
          <td style="padding:6px;text-align:left;vertical-align:top;">
            <a href="{url}" class="bookmark-link" title="{b['title']}" target="_blank" 
               style="color:#0366d6;text-decoration:none;word-break:break-word;">{url}</a>
          </td>
          <td style="padding:6px;text-align:left;vertical-align:top;">{b['tags']}</td>
          <td style="padding:6px;text-align:left;vertical-align:top;">{b['notes']}</td>
          <td class="status" style="padding:6px;text-align:left;vertical-align:top;">⏳</td>
        </tr>
"""

    html += """      </tbody>
    </table>
  </div>
  <script>
    const themeButton = document.getElementById("theme-button");
    const body = document.body;
    themeButton.addEventListener("click", () => {
      body.classList.toggle("dark-mode");
      if (body.classList.contains("dark-mode")) {
        body.style.backgroundColor = "black";
        body.style.color = "white";
        themeButton.textContent = "🌙";
      } else {
        body.style.backgroundColor = "white";
        body.style.color = "black";
        themeButton.textContent = "☀️";
      }
    });
  </script>
</body>
</html>"""

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ HTML exported {HTML_FILE}")

if __name__ == "__main__":
    generate_html(load_bookmarks())
