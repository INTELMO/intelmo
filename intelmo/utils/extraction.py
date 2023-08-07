import newspaper

from ..models.article import Article
from ..models.block import Block, BlockLevelEnum, BlockTypeEnum


def extract_url(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    return article


def extract_url_to_article(url: str) -> Article:
    article = extract_url(url)
    blocks = []
    for paragraph in article.text.split("\n"):
        if paragraph == "":
            continue
        block = Block(BlockLevelEnum.Paragraph, BlockTypeEnum.Normal, paragraph, None)
        blocks.append(block)
    return Article(article.title, article.url, blocks)
