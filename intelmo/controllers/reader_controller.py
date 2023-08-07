import urllib.parse
from collections import defaultdict
from typing import List, DefaultDict

from flask import Blueprint, render_template, request, current_app, redirect

from ..models.article import Article
from ..models.block import BlockTypeEnum, BlockLevelEnum, BlockStatusEnum, Block
from ..types.model import ModelConfiguration, InteractiveFunctionType
from ..utils.extraction import extract_url_to_article

reader_page = Blueprint('reader_page', __name__)

function_results = {}

function_forms = defaultdict(lambda: {})  # type: DefaultDict[str, dict]


def save_result(_id, url, result):
    global function_results
    if _id not in function_results:
        function_results[_id] = {}
    function_results[_id][url] = result


def parallel_functions(functions: List[InteractiveFunctionType], original_article: Article) -> Article:
    res_list = []
    for function in functions:
        if function.id in function_results and original_article.url in function_results[function.id]:
            res_list.append(function_results[function.id][original_article.url])
        else:
            if function.form is not None:
                params = [original_article, function_forms[function.id]]
            else:
                params = [original_article]
            res = function.function(*params)
            res_list.append(res)
            # save_result(function.id, original_article.url, res)

    article = original_article.copy()
    blocks = []
    global_block = None
    for res in res_list:
        if res.global_block is not None:
            if global_block is not None:
                global_block = Block(BlockLevelEnum.Global, BlockTypeEnum.Normal,
                                     global_block.content + "\n" + res.global_block.content, None)
            else:
                global_block = res.global_block

    iters = [iter(res.blocks) for res in res_list]
    origin_iter = iter(article.blocks)
    while True:
        target_block = None
        for it in iters:
            try:
                block = next(it)
                while block.status == BlockStatusEnum.New:
                    blocks.append(block)
                    block = next(it)

                if block.status == BlockStatusEnum.Modified:
                    target_block = block

            except StopIteration:
                pass

        if target_block is not None:
            blocks.append(target_block)
            next(origin_iter)
        else:
            try:
                block = next(origin_iter)
                blocks.append(block)
            except StopIteration:
                break

    return Article(article.title, article.url, blocks, global_block)


def exclusive_functions(functions: List[InteractiveFunctionType], original_article: Article) -> Article:
    # just run the last function
    target_id = functions[-1].id
    if target_id in function_results and original_article.url in function_results[target_id]:
        return function_results[target_id][original_article.url]
    else:
        function = functions[-1]
        if function.form is not None:
            params = [original_article, function_forms[function.id]]
        else:
            params = [original_article]
        res = function.function(*params)
    return Article(original_article.title, original_article.url, res.blocks, res.global_block)


def pipeline_functions(functions: List[InteractiveFunctionType], original_article: Article) -> Article:
    # sort functions by id
    functions.sort(key=lambda x: int(x.id))
    new_article = original_article.copy()

    for function in functions:
        if function.form is not None:
            params = [new_article, function_forms[function.id]]
        else:
            params = [new_article]
        res = function.function(*params)
        new_article = Article(original_article.title, original_article.url, res.blocks, res.global_block)
    return Article(original_article.title, original_article.url, new_article.blocks, new_article.global_block)


@reader_page.route('/article')
def reader_page_index():
    global function_results
    args = request.args

    url = args.get('url', default=None, type=str)
    enabled_functions = args.get('functions', default="", type=str)
    if enabled_functions == "":
        enabled_functions = []
    else:
        enabled_functions = enabled_functions.split(',')

    # decode url
    if url is None:
        return "404"
    url_decoded = urllib.parse.unquote_plus(url)
    model = current_app.config['model']  # type: ModelConfiguration
    composition = model.composition

    article = extract_url_to_article(url_decoded)

    if len(enabled_functions) != 0:
        functions = list(map(lambda x: model.get_function(x), enabled_functions))

        if composition == "parallel":
            function_result = parallel_functions(functions, article)
        elif composition == "exclusive":
            function_result = exclusive_functions(functions, article)
        elif composition == "pipeline":
            function_result = pipeline_functions(functions, article)
        else:
            raise Exception("Unknown composition type: " + composition)

        article.blocks = function_result.blocks
        article.global_block = function_result.global_block

    context = {
        "article": article,
        "BlockTypeEnum": BlockTypeEnum,
        "BlockLevelEnum": BlockLevelEnum,
        "functions": model.functions,
        "enabled_functions": enabled_functions,
        "url": url,
        "function_forms": function_forms,
    }
    return render_template('reader.html', **context)


@reader_page.route('/set_form', methods=['POST'])
def set_form():
    args = request.args
    function_id = args.get('id', default=None, type=str)
    print(request.form.to_dict())
    function_forms[function_id] = request.form.to_dict()
    # return to the same page
    return redirect(request.referrer)


@reader_page.route('/toggle_function')
def toggle_function():
    args = request.args
    function = args.get('function', default=None, type=str)
    url = args.get('url', default=None, type=str)
    enabled_functions = args.get('enabled_functions', default='', type=str)
    if enabled_functions == "":
        enabled_functions = []
    else:
        enabled_functions = enabled_functions.split(',')

    model = current_app.config['model']  # type: ModelConfiguration
    composition = model.composition

    if function is None or url is None:
        return "404"

    if composition == "exclusive":
        enabled_functions = [function]
    else:
        if function in enabled_functions:
            enabled_functions.remove(function)
        else:
            enabled_functions.append(function)

    return redirect(f"/reader/article?url={url}&functions={','.join(enabled_functions)}")
