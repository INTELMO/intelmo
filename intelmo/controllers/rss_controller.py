import urllib.parse

from flask import Blueprint, render_template

from ..models.rss import RSS_SOURCES, RSS

rss_page = Blueprint('rss_page', __name__)


@rss_page.route('/')
def rss_page_index():
    context = {
        'rss_sources': RSS_SOURCES
    }
    return render_template('rss.html', **context)


@rss_page.route('/<string:rss_source_id>')
def rss_page_feed(rss_source_id):
    rss_source = next(filter(lambda x: x['id'] == rss_source_id, RSS_SOURCES), None)
    rss = RSS(rss_source["id"], rss_source['name'], rss_source['url'])

    # set entries link encoded
    for entry in rss.feed.entries:
        encoded_link = urllib.parse.quote_plus(entry.link)
        entry.href = f'/reader/article?url={encoded_link}'

    context = {
        'rss': rss
    }
    return render_template('feed.html', **context)
