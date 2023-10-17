from __future__ import annotations
from enum import Enum
from typing import Callable, List, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from models.article import Article


class BlockTypeEnum(Enum):
    """Enum for type of block"""
    Normal = "normal"
    Bold = "bold"
    Italic = "italic"
    Underline = "underline"
    Light = "light"
    Title = "title"
    Custom = "custom"
    Quote = "quote"


class BlockLevelEnum(Enum):
    Paragraph = "paragraph"
    Sentence = "sentence"
    Word = "word"
    Global = "global"


class BlockStatusEnum(Enum):
    Untouched = "untouched"
    New = "new"
    Modified = "modified"


BlockAction = Callable[["Article"], "Article"]


class Block:
    def __init__(self, level: BlockLevelEnum, type: BlockTypeEnum, content: Optional[str],
                 children: Optional[List['Block']], status: Optional[BlockStatusEnum] = None,
                 extra: Optional['Block'] = None,
                 onclick: Optional['BlockAction'] = None
                 ):
        self.level = level
        self.type = type
        self.content = content
        self.children = children
        self.status = status if status is not None else BlockStatusEnum.Untouched
        self.extra = extra
        self.onclick = onclick

    def __dict__(self):
        children = []
        if self.children is not None:
            children = [subBlock.__dict__ for subBlock in self.children]
        return {
            "level": self.level.value,
            "type": self.type.value,
            "content": self.content,
            "blocks": children,
            "status": self.status.value,
            "extra": self.extra if self.extra is not None else ""
        }

    def print_tree(self, header="", last=True):
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        # content = self.content if self.content is not None else "" + "
        content = f"{self.content} ({self.status.value}) ({self.type.value}) ({self.level.value})"
        print((elbow if last else tee) + content)
        if self.children is not None:
            children = self.children
            for i, c in enumerate(children):
                c.print_tree(header=header + (blank if last else pipe),
                             last=i == len(children) - 1)

    def get_content(self):
        if self.content is None:
            return "".join([child.get_content() for child in self.children])
        return self.content
