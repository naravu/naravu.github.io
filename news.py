import feedparser

# List of Tamil and English RSS feed URLs
RSS_FEEDS = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "Reuters": "https://www.reutersagency.com/feed/?best-topics",
    "NY Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "OneIndia Tamil": "https://tamil.oneindia.com/rss/feeds/tamil-news-fb.xml",
    "News18 Tamil": "https://tamil.news18.com/rss/tamilnadu.xml",
    "Hindustan Times Tamil": "https://tamil.hindustantimes.com/rss/tamilnadu"
}

def fetch_rss_news():
    """Fetch latest news from multiple RSS feeds."""
    all_news = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:  # Get latest 5 articles per source
            all_news.append({
                "source": source,
                "title": entry.title,
                "summary": entry.get("summary", "No description available."),
                "link": entry.link
            })
    return all_news

def generate_html(news_list):
    """Generate a responsive HTML page with CSS and JavaScript."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latest News</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f8f9fa; }
        .filter-container { text-align: center; margin-bottom: 20px; }
        .filter-btn { padding: 10px; border: none; background: #007bff; color: white; cursor: pointer; margin: 5px; }
        .filter-btn:hover { background: #0056b3; }
        .news-container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
        .news-item { width: 300px; background: white; border: 1px solid #ddd; padding: 15px; border-radius: 5px; box-shadow: 2px 2px 5px #ddd; }
        .news-item h2 { font-size: 16px; }
        .news-item p { font-size: 14px; }
        .news-source { font-weight: bold; color: #555; }
        .hidden { display: none; }
    </style>
    <script>
        function filterNews(category) {
            let items = document.querySelectorAll('.news-item');
            items.forEach(item => {
                if (category === 'All' || item.dataset.source.includes(category)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        }
    </script>
</head>
<body>
    <div class="filter-container">
        <button class="filter-btn" onclick="filterNews('All')">All News</button>
        <button class="filter-btn" onclick="filterNews('Tamil')">Tamil News</button>
        <button class="filter-btn" onclick="filterNews('English')">English News</button>
    </div>
    <div class="news-container">
"""

    for news in news_list:
        category = "Tamil" if "Tamil" in news['source'] else "English"
        html_content += f"""
        <div class="news-item" data-source="{category}">
            <p class="news-source">{news['source']}</p>
            <h2>{news['title']}</h2>
            <p>{news['summary']}</p>
            <a href="{news['link']}" target="_blank">Read More</a>
        </div>
        """

    html_content += """
    </div>
</body>
</html>
"""
    return html_content

if __name__ == "__main__":
    news_data = fetch_rss_news()
    html_page = generate_html(news_data)

    with open("news.html", "w", encoding="utf-8") as file:
        file.write(html_page)

    print("✅ News page generated: latest_rss_news.html")
