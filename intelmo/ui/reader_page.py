from typing import List
import urllib.parse
from nicegui import ui
from models.task import InteractiveTaskType, TaskModelConfiguration

from models.block import Block, BlockTypeEnum, BlockLevelEnum
from models.article import Article
from utils.extraction import extract_url_to_article
from ui.header import make_header, function_forms

article = Article("", "", [])


def get_block_classname_by_level(level: BlockLevelEnum) -> str:
    if level == BlockLevelEnum.Paragraph:
        return "rounded-md block p-4 relative"
    elif level == BlockLevelEnum.Global:
        return "fixed top-16 right-0 m-4 p-4 z-30 bg-white shadow-lg rounded-lg"
    else:
        return "inline"


def get_block_classname_by_type(btype: BlockTypeEnum) -> str:
    if btype == BlockTypeEnum.Bold:
        return "font-bold"
    elif btype == BlockTypeEnum.Italic:
        return "italic"
    elif btype == BlockTypeEnum.Underline:
        return "underline"
    elif btype == BlockTypeEnum.Light:
        return "text-gray-400"
    elif btype == BlockTypeEnum.Title:
        return "text-2xl font-bold"
    elif btype == BlockTypeEnum.Quote:
        return "border-2 border-blue-500 bg-blue-200 text-blue-800 underline"
    else:
        return ""


def make_block(block: Block) -> None:
    cname = f"{get_block_classname_by_level(block.level)} {get_block_classname_by_type(block.type)}"
    if block.children and len(block.children) > 0:
        with ui.element("span").classes(cname):
            for child in block.children:
                make_block(child)

    else:
        def onclick():
            if block.onclick is None:
                return
            global article
            new_article = block.onclick(article)
            make_article.refresh(new_article)
            article = new_article

        ui.label(block.content).classes(cname).on("click", onclick)
        # ui.label(block.content)

    if block.extra:
        with ui.element("span").classes("absolute top-0 left-full p-2 bg-white rounded-lg shadow-lg w-max"):
            make_block(block.extra)


@ui.refreshable
def make_article(cur_article: Article) -> None:
    with ui.element("article").classes("mt-12 px-6 py-12 max-w-2xl mx-auto text-lg"):
        ui.label(cur_article.title).classes("text-4xl font-bold mb-12")

        if cur_article.global_block:
            make_block(cur_article.global_block)

        for block in cur_article.blocks:
            make_block(block)


def handle_function_update(model: TaskModelConfiguration, original_article: Article, enabled_functions: List[str], function_forms: dict):
    function_result = model.task_tree.run_function(
        enabled_functions,
        original_article,
        function_forms
    )

    make_article.refresh(function_result)


def content(encoded_url: str, functions: List[InteractiveTaskType], model: TaskModelConfiguration) -> None:
    global article
    url = urllib.parse.unquote_plus(encoded_url)

    article = extract_url_to_article(url)

    # update function_forms with default values
    for function in functions:
        if function.form:
            function_forms.update({function.id: {}})
            for formItem in function.form:
                function_forms[function.id].update(
                    {formItem["name"]: formItem["defaultValue"]})

    make_article(article)

    make_header(functions, on_update=lambda enabled_functions, function_forms: handle_function_update(
        model, article, enabled_functions, function_forms
    ))
