import re
import argparse
from datetime import datetime

MD_FILE = "todo.md"
HTML_FILE = "todo.html"

def parse_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tasks = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = re.match(r'- \[( |x)\] (.+)', line)
        if match:
            done = match.group(1) == 'x'
            title = match.group(2)
            description = ""
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('>'):
                    description = next_line[1:].strip()
                    i += 1
            tasks.append({"id": len(tasks), "title": title, "done": done, "desc": description})
        i += 1
    return tasks

def remove_task(filepath, task_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    count = 0
    skip_next = False
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        if re.match(r'- \[( |x)\] .+', line.strip()):
            if count == task_id:
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('>'):
                    skip_next = True
            else:
                new_lines.append(line)
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('>'):
                    new_lines.append(lines[i + 1])
            count += 1
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def add_task(filepath, task_title, task_desc=""):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f"- [ ] {task_title}\n")
        if task_desc:
            f.write(f"> {task_desc}\n")
    print(f"🆕 Added task: {task_title}")
    if task_desc:
        print(f"   📝 Description: {task_desc}")

def generate_html(tasks):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""
    for task in tasks:
        status = "✅" if task["done"] else "🕒"
        row_class = "done" if task["done"] else "pending"
        content = f"<details><summary>{task['title']}</summary><p>{task['desc']}</p></details>" if task["desc"] else task["title"]
        rows += f"""
        <tr class="{row_class}">
            <td>{task['id'] + 1}</td>
            <td>{status}</td>
            <td>{content}</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>📝 Markdown To-Do List</title>
    <style>
        body {{
            margin: 0;
            display: flex;
            font-family: Arial, Helvetica, sans-serif;
            background-color: #1e1e1e;
            color: #f0f0f0;
        }}
        .sidebar {{
            width: 260px;
            background-color: #2b2b2b;
            padding: 20px;
            border-right: 1px solid #444;
            height: 100%;
        }}
        .sidebar h3 {{
            margin-top: 0;
            color: #ddd;
        }}
        .sidebar code {{
            display: block;
            margin: 6px 0;
            color: #ccc;
        }}
        .main {{
            flex-grow: 1;
            padding: 20px;
        }}
        h2 {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .legend {{
            text-align: center;
            font-size: 0.95em;
            color: #aaa;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #2a2a2a;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}
        thead {{
            background-color: #333;
        }}
        th {{
            padding: 12px;
            color: #ddd;
            border-bottom: 1px solid #444;
            cursor: pointer;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #444;
        }}
        tr.done {{
            background-color: #264d26;
            color: #cfc;
        }}
        tr.pending {{
            background-color: #4d4426;
            color: #ffe;
        }}
        tr:hover {{
            background-color: #444;
        }}
        details {{
            color: #eee;
        }}
        summary {{
            cursor: pointer;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 0.85em;
            color: #888;
            text-align: center;
            border-top: 1px solid #444;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <h3>🛠️ CLI Usage</h3>
        <code>python todo_dashboard.py</code>
        <code>python todo_dashboard.py --add "New Task"</code>
        <code>python todo_dashboard.py --add "New Task" --desc "Details"</code>
        <code>python todo_dashboard.py --remove 2</code>
            <p><small>Use the CLI to add or remove tasks. Descriptions are optional and shown here.</small></p>
    </div>
    <div class="main">
        
        <div class="legend">✅ = Done, 🕒 = Pending Updated:{timestamp}</div>
        <table id="todoTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)"><span id="arrow0">Line 🔽</span></th>
                    <th onclick="sortTable(1)"><span id="arrow1">Status 🔽</span></th>
                    <th onclick="sortTable(2)"><span id="arrow2">Task 🔽</span></th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        <div class="footer">
            &copy; Todo All rights enabled.
        </div>
    </div>
    <script>
        let sortDirection = [true, true, true];
        function sortTable(colIndex) {{
            const table = document.getElementById("todoTable");
            const rows = Array.from(table.rows).slice(1);
            const dir = sortDirection[colIndex] ? 1 : -1;

            rows.sort((a, b) => {{
                const aText = a.cells[colIndex].innerText.trim();
                const bText = b.cells[colIndex].innerText.trim();
                return aText.localeCompare(bText) * dir;
            }});

            sortDirection[colIndex] = !sortDirection[colIndex];
            const tbody = table.querySelector("tbody");
            rows.forEach(row => tbody.appendChild(row));

            for (let i = 0; i < 3; i++) {{
                document.getElementById("arrow" + i).textContent =
                    (i === colIndex ? (sortDirection[i] ? "🔽" : "🔼") : "🔽") + " " + ["Line", "Status", "Task"][i];
            }}
        }}
    </script>
</body>
</html>
    """

def main():
    parser = argparse.ArgumentParser(description="Markdown To-Do List Generator")
    parser.add_argument("--remove", type=int, help="Task ID to remove")
    parser.add_argument("--add", type=str, help="Task title to add")
    parser.add_argument("--desc", type=str, help="Optional task description")
    args = parser.parse_args()

    if args.remove is not None:
        remove_task(MD_FILE, args.remove)

    if args.add:
        add_task(MD_FILE, args.add, args.desc or "")

    tasks = parse_md(MD_FILE)
    html = generate_html(tasks)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ {HTML_FILE} generated successfully.")

if __name__ == "__main__":
    main()
