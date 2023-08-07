from feedparser import parse

RSS_SOURCES = [
    {
        "id": "1",
        "name": "CNN Top Stories",
        "url": "http://rss.cnn.com/rss/cnn_topstories.rss"
    },
    {
        "id": "2",
        "name": "CNN World",
        "url": "http://rss.cnn.com/rss/cnn_world.rss"
    },
    {
        "id": "3",
        "name": "BBC News",
        "url": "http://feeds.bbci.co.uk/news/rss.xml"
    },
    {
        "id": "4",
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml"
    },
    {
        "id": "5",
        "name": "ReadWrite",
        "url": "https://readwrite.com/feed/"
    },
    {
        "id": "6",
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/"
    },
    {
        "id": "7",
        "name": "New York Times",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    },
]


class RSS:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
        self.feed = parse(url)

