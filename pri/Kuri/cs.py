import markdown
from bs4 import BeautifulSoup

def md_to_html_table(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_raw = markdown.markdown(md_content, extensions=['tables'])
    soup = BeautifulSoup(html_raw, 'html.parser')
    table = soup.find('table')

    html_final = f"""
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>&copy; Kuri</title>
      <style>
        body {{
          font-family: 'Segoe UI', sans-serif;
          background-color: #121212;
          color: #e0e0e0;
          padding: 10px;
          margin: 0;
        }}
        .search-bar {{
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          gap: 6px;
          margin-bottom: 10px;
        }}
        #searchBox {{
          padding: 8px;
          flex: 1;
          min-width: 200px;
          background-color: #1e1e1e;
          color: #e0e0e0;
          border: 1px solid #444;
          box-sizing: border-box;
        }}
        #countLabel {{
          padding: 8px 12px;
          background-color: #2c2c2c;
          color: #ffcc00;
          font-weight: normal;
          border: 1px solid #444;
          white-space: nowrap;
        }}
        .action-btn {{
          padding: 8px 12px;
          background-color: #2c2c2c;
          color: #e0e0e0;
          border: 1px solid #444;
          cursor: pointer;
          font-size: 14px;
          border-radius: 4px;
        }}
        .action-btn span {{
          font-size: 14px;
        }}
        .action-btn:hover {{
          background-color: #3a3a3a;
        }}
        .table-container {{
          overflow-x: auto;
          -webkit-overflow-scrolling: touch;
        }}
        table {{
          border-collapse: collapse;
          width: 100%;
          min-width: 600px;
        }}
        th, td {{
          border: 1px solid #444;
          padding: 6px;
          text-align: left;
        }}
        th {{
          background-color: #2c2c2c;
          cursor: pointer;
          font-weight: bold;
        }}
        td {{
          background-color: #1e1e1e;
        }}
        td code {{
          background: #2c2c2c;
          padding: 2px 4px;
          border-radius: 3px;
          color: #ffcc00;
        }}
        @media (max-width: 600px) {{
          th, td {{
            padding: 4px;
            font-size: 14px;
          }}
          #searchBox, .action-btn, #countLabel {{
            font-size: 12px;
            padding: 6px 10px;
            font-weight: normal;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="search-bar">
        <input type="text" id="searchBox" placeholder="🔍 Filter...">
        <div id="countLabel" title="Count">🔢 0</div>
        <button class="action-btn" onclick="resetFilter()" title="Reset">🔄</button>
        <button class="action-btn" onclick="exportTable()" title="Export XLS">📤</button>
        <button class="action-btn" onclick="showPrinter()" title="Print">🖨️</button>
                
        <button class="action-btn" onclick="showInfo()" title="Info"><span>🧠</span>Info</button>
        <button class="action-btn" onclick="showTools()" title="Tools"><span>🛠️</span>Tools</button>
        <button class="action-btn" onclick="runTest()" title="Test"><span>🧪</span>Test</button>
      </div>
      <div class="table-container">
        {str(table)}
      </div>
      <script>
        const searchBox = document.getElementById('searchBox');
        const table = document.querySelector('table');
        const countLabel = document.getElementById('countLabel');

        function updateCount() {{
          const visibleRows = Array.from(table.rows).slice(1).filter(row => row.style.display !== 'none');
          countLabel.textContent = '🔢' + visibleRows.length;
        }}

        searchBox.addEventListener('input', () => {{
          const query = searchBox.value.toLowerCase();
          Array.from(table.rows).slice(1).forEach(row => {{
            const match = row.textContent.toLowerCase().includes(query);
            row.style.display = match ? '' : 'none';
          }});
          updateCount();
        }});

        function sortTable(colIndex) {{
          const rows = Array.from(table.rows).slice(1);
          const sorted = rows.sort((a, b) => {{
            return a.cells[colIndex].textContent.localeCompare(b.cells[colIndex].textContent);
          }});
          sorted.forEach(row => table.appendChild(row));
          updateCount();
        }}

        Array.from(table.rows[0].cells).forEach((th, i) => {{
          th.addEventListener('click', () => sortTable(i));
        }});

        function resetFilter() {{
          searchBox.value = '';
          Array.from(table.rows).slice(1).forEach(row => row.style.display = '');
          updateCount();
        }}

        function exportTable() {{
          const htmlContent = document.documentElement.outerHTML;
          const encoded = encodeURIComponent(htmlContent);
          const link = document.createElement('a');
          link.setAttribute('href', 'data:text/html;charset=UTF-8,' + encoded);
          link.setAttribute('download', 'kuri.xls');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }}

        function showPrinter() {{
          window.print();
        }}

        updateCount();
      </script>
    </body>
    </html>
    """

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_final)

if __name__ == "__main__":
    md_to_html_table('commands.md', 'commands.html')
