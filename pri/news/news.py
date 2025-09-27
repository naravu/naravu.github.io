import feedparser

# Define RSS feeds
rss_feeds = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "Guardian": "https://www.theguardian.com/world/rss",
    "Wired": "https://www.wired.com/feed/rss"
}

# Collect entries
all_entries = []
for source, url in rss_feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:10]:
        all_entries.append({
            "source": source,
            "title": entry.get("title", "No title"),
            "link": entry.get("link", "#"),
            "summary": entry.get("summary", entry.get("description", "No summary available")),
            "published": entry.get("published", "No date"),
        })

# HTML generator
def generate_html(entries):
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>RSS News Dashboard</title>
<link rel="stylesheet" href="style.css">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<div class="hamburger" onclick="toggleSidebar()">☰</div>
<div class="sidebar" id="sidebar">
  <center><h2>Sources</h2></center>
  <button onclick="filterNews('All')">All</button>
"""
    for source in rss_feeds.keys():
        html += f'<button onclick="filterNews(\'{source}\')">{source}</button>\n'

    html += """
</div>
<div class="content" id="news-container">
"""

    for entry in entries:
        html += f"""
  <div class="card" data-source="{entry['source']}">
    <h3>{entry['title']}</h3>
    <p><em>{entry['published']}</em></p>
    <p>{entry['summary'][:200]}...</p>
    <a href="{entry['link']}" target="_blank">Read more</a>
  </div>
"""

    html += """
</div>
<script>
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('visible');
}

function filterNews(source) {
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    card.style.display = (source === 'All' || card.dataset.source === source) ? 'block' : 'none';
  });
}
</script>
</body>
</html>
"""
    return html

# Write to file
with open("news.html", "w", encoding="utf-8") as f:
    f.write(generate_html(all_entries))
