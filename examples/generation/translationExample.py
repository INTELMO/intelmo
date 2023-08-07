import random
from typing import List

from deep_translator import GoogleTranslator
from intelmo import Article, Block, BlockLevelEnum, BlockTypeEnum, BlockStatusEnum


def translate_to_zh(paragraphs: List[str], config: dict) -> List[dict]:
    to_lang = config.get("to_lang", "zh-CN")
    translator = GoogleTranslator(source="auto", target=to_lang)
    translated_paragraphs = []
    for index, paragraph in enumerate(paragraphs):
        translation = translator.translate(paragraph)
        translated_paragraphs.append({
            "position": index,
            "content": translation
        })
    return translated_paragraphs


def custom_translate(article: Article) -> Article:
    new_article = article.copy()
    new_blocks = []
    for block in new_article.blocks:
        new_blocks.append(block)
        # 50% chance to translate
        if random.random() < 0.3:

            translation = """
                <div class="flex flex-col gap-2">
                    <div class="text-lg font-semibold"> Leave your comments of this paragraph! </div>
                    <textarea type="text"></textarea>
                </div>
            """
            block.extra = translation
    return new_article


def translate(paragraphs: List[str], to_lang) -> List[dict]:
    translator = Translator(to_lang=to_lang)
    translated_paragraphs = []
    for index, paragraph in enumerate(paragraphs):
        translation = translator.translate(paragraph)
        translated_paragraphs.append({
            "position": index,
            "content": translation
        })
    return translated_paragraphs
