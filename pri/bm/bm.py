import os
import re

BOOKMARKS_FILE = 'pri/bm/bm.md'
HTML_FILE = 'pri/bm/bm.html'

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
            background-color: white;
            color: black;
            transition: background-color 0.3s, color 0.3s;
            margin: 2px;
        }
        .dark-mode {
            background-color: black;
            color: white;
        }
          
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.95rem;
    }
    th, td {
      padding: 1px 1px;
      border-bottom: 1px solid #ddd;
      text-align: left;
    }
    th {
      background: #FFD700;
      color: #fff;
      cursor: pointer;
    }
    tr:hover {
      background-color: #f1f1f1;
    }
    a {
      color: #0366d6;
      text-decoration: none;
      word-break: break-word;
    }
    a:hover {
      text-decoration: underline;
    }
    .dark-mode a {
  color: #1e90ff;
}

.dark-mode tr:hover {
  background-color: #333;
}

.dark-mode th {
  background: #555;
  color: #FFD700;
}

input[type="text"] {
  padding: 4px;
  margin-left: 6px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  color: #000;
}

.dark-mode input[type="text"] {
  background-color: #222;
  color: #fff;
  border: 1px solid #444;
}

  </style>
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
<body>
  📌🅝🅞🅞🅡🅚🅤🅡🅘<input type="text" id="filterInput" placeholder="Search..." onkeyup="filterTable()"><button id="theme-button">☀️</button>
  <table id="bookmarkTable" data-sort-dir="asc">
    <thead>
      <tr>
        <th onclick="sortTable(0)" title="Serial Number">🔢</th>
        <th onclick="sortTable(1)" title="URL">🔗</th>
        <th onclick="sortTable(2)" title="Tags">🏷️</th>
        <th onclick="sortTable(3)" title="Description">🔖</th>
        <th onclick="sortTable(4)" title="URL Status">✅/❌</th>
      </tr>
    </thead>
    <tbody>
"""
    for idx, b in enumerate(bookmarks, 1):
        url = b['url'].strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        html += f"""      <tr>
        <td>{idx}</td>
        <td><a href="{url}" class="bookmark-link" title="{b['title']}" target="_blank">{url}</a></td>
        <td>{b['tags']}</td>
        <td>{b['notes']}</td>
        <td class="status">⏳</td>
      </tr>
"""

    html += """    </tbody>
  </table>
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
