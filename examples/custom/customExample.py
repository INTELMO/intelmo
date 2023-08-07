import spacy
from typing import List
from intelmo import Block, BlockLevelEnum, BlockTypeEnum, \
    BlockStatusEnum, Article

import hashlib


def string_to_color(input_string, saturation=80, lightness=70):
    # Generate MD5 hash of the input string
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()

    # Convert the first 6 characters of the hash to an integer
    hash_int = int(md5_hash[:6], 16)

    # Map the integer to a hue value between 0 and 360
    hue = hash_int % 360

    # Format the HSL values as a CSS-style color code
    color_code = "hsl({}, {}%, {}%)".format(hue, saturation, lightness)

    return color_code


def get_ent_html(ent):
    color = string_to_color(ent.label_)
    return f'<span class="entity" data-entity-type="{ent.label_}" style="background-color:{color}">{ent.text}</span>'


# customFunction is InteractiveFunctionType
class SpaCyAnnotator:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def annotate(self, rss: Article) -> Article:
        blocks = []  # type: List[Block]
        res_article = rss
        for paragraph in rss.blocks:
            # split paragraph into sentences
            paragraph_block = Block(BlockLevelEnum.Paragraph, BlockTypeEnum.Normal, None, [
            ], BlockStatusEnum.Modified)
            doc = self.nlp(paragraph.content)
            for sentence in doc.sents:
                sentence_block = Block(BlockLevelEnum.Sentence, BlockTypeEnum.Normal, sentence.text, [],
                                       BlockStatusEnum.Modified)
                cur_pos = 0
                for ent in sentence.ents:
                    if ent.start_char > cur_pos:
                        sentence_block.children.append(
                            Block(BlockLevelEnum.Word, BlockTypeEnum.Normal, sentence.text[cur_pos:ent.start_char],
                                  None,
                                  BlockStatusEnum.Modified))
                    sentence_block.children.append(
                        Block(BlockLevelEnum.Word, BlockTypeEnum.Normal, get_ent_html(ent), None,
                              BlockStatusEnum.New))
                    cur_pos = ent.end_char
                if cur_pos < len(sentence.text):
                    sentence_block.children.append(
                        Block(BlockLevelEnum.Word, BlockTypeEnum.Normal, sentence.text[cur_pos:], None,
                              BlockStatusEnum.Modified))
                paragraph_block.children.append(sentence_block)
            blocks.append(paragraph_block)

        res_article.blocks = blocks

        return res_article
