from nicegui import ui
import urllib.parse

# from ..models.rss import RSS_SOURCES
from ..models.rss import RSS_SOURCES, RSS


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


def content() -> None:
    with ui.element('div').classes("px-6 py-12 max-w-2xl mx-auto"):
        ui.label('RSS Sources').classes('text-4xl font-bold mb-12')
        with ui.column():
            for rss in RSS_SOURCES:
                # with ui.card().classes('no-shadow'):

                ui.link(rss["name"], f'/{rss["id"]}').classes('w-full block p-4 border border-gray-200 '
                                                              'hover:border-gray-500 rounded-lg cursor-pointer '
                                                              'no-underline')


def detail_content(rss_source_id: str) -> None:
    rss_source = next(
        filter(lambda x: x['id'] == rss_source_id, RSS_SOURCES), None)

    rss = RSS(rss_source["id"], rss_source['name'], rss_source['url'])

    # set entries link encoded
    for entry in rss.feed.entries:
        encoded_link = urllib.parse.quote_plus(entry.link)
        entry.href = f'/reader/article?url={encoded_link}'

    with ui.element('div').classes("px-6 py-12 max-w-2xl mx-auto"):
        ui.label(rss.name).classes('text-4xl font-bold mb-12')
        with ui.column():
            for entry in rss.feed.entries:
                # with ui.card().classes('no-shadow'):
                ui.link(entry.title, entry.href).classes('w-full block p-4 border border-gray-200 '
                                                         'hover:border-gray-500 rounded-lg cursor-pointer '
                                                         'no-underline')
