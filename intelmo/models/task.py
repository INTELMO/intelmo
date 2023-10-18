from __future__ import annotations

from typing import List, Union, Callable, Optional, Literal, NotRequired, TypedDict
import itertools
from ..models.form import Form
from ..models.article import Article
from ..models.block import Block, BlockLevelEnum, BlockTypeEnum, BlockStatusEnum

import nltk

from bigtree import Node, print_tree, findall

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


TaskType = Literal["modification", "insertion", "generation", "custom"]


class InteractiveTaskConfiguration(TypedDict):
    name: str
    description: str
    task_type: TaskType
    # task is one of the values in TaskType
    task: Callable
    form: NotRequired[Form]


class InteractiveFunctionType:
    def __init__(self, id: str, name: str, description: str,
                 function: Callable[[Article, dict], Article],
                 form: Optional[Form] = None,
                 ):
        self.id = id
        self.name = name
        self.description = description
        self.function = function
        self.form = form


class InteractiveTaskType:
    id_iter = itertools.count()

    def __init__(self, config: InteractiveTaskConfiguration):
        self.id = str(next(self.id_iter))
        self.name = config['name']
        self.description = config['description']
        self.task_type = config['task_type']
        self.task = config['task']

        if 'form' in config:
            self.form = config['form']
        else:
            self.form = None


def compatible_functions(functions: List[InteractiveFunctionType], original_article: Article,
                         function_forms: dict) -> Article:
    res_list = []
    for function in functions:
        if function.form is not None:
            params = [original_article, function_forms[function.id]]
        else:
            params = [original_article]
        res = function.function(*params)
        res_list.append(res)

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


def exclusive_functions(functions: List[InteractiveFunctionType], original_article: Article,
                        function_forms: dict) -> Article:
    function = functions[-1]
    if function.form is not None:
        params = [original_article, function_forms[function.id]]
    else:
        params = [original_article]
    res = function.function(*params)
    return Article(original_article.title, original_article.url, res.blocks, res.global_block)


def pipeline_functions(functions: List[InteractiveFunctionType], original_article: Article,
                       function_forms: dict) -> Article:
    # sort functions by id
    functions.sort(key=lambda x: int(x.id))
    new_article = original_article.copy()

    for function in functions:
        if function.form is not None:
            params = [new_article, function_forms[function.id]]
        else:
            params = [new_article]
        res = function.function(*params)
        new_article = Article(original_article.title,
                              original_article.url, res.blocks, res.global_block)
    return Article(original_article.title, original_article.url, new_article.blocks, new_article.global_block)


def get_interactive_function(task: InteractiveTaskType) -> InteractiveFunctionType:
    res_func = None
    if task.task_type == "modification":
        def modification_func(article: Article, form: Optional[dict] = None) -> Article:
            new_article = article.copy()
            paragraphs = article.blocks
            total_text = '\n'.join(map(lambda p: p.content, paragraphs))
            modification_res = task.task(
                total_text, form) if form is not None else task.task(total_text)
            processed_paragraphs = []
            for paragraph in paragraphs:
                # split the paragraph into sentences
                sentences = nltk.sent_tokenize(paragraph.content)
                processed_sentences = []
                for sentence in sentences:
                    # if the sentence is modificationed, add it to the list
                    if sentence in modification_res:
                        processed_sentences.append(
                            Block(BlockLevelEnum.Sentence, BlockTypeEnum.Bold, sentence, None, BlockStatusEnum.New))
                    else:
                        processed_sentences.append(
                            Block(BlockLevelEnum.Sentence, BlockTypeEnum.Light, sentence, None, BlockStatusEnum.New))
                processed_paragraphs.append(
                    Block(BlockLevelEnum.Paragraph, BlockTypeEnum.Normal, None, processed_sentences,
                          BlockStatusEnum.Modified))

            new_article.blocks = processed_paragraphs

            return new_article

        res_func = modification_func

    elif task.task_type == "generation":
        def generation_func(article: Article, form: Optional[dict] = None) -> Article:
            new_article = article.copy()
            # paragraphs = list(map(lambda p: Block(
            #     BlockLevelEnum.Paragraph, BlockTypeEnum.Normal, p.content, None), article.blocks))
            total_text = article.get_content()

            generation_res = task.task(
                total_text, form) if form is not None else task.task(total_text)

            global_block = Block(BlockLevelEnum.Global, BlockTypeEnum.Normal,
                                 generation_res, None, BlockStatusEnum.New)
            new_article.global_block = global_block
            return new_article

        res_func = generation_func

    elif task.task_type == "insertion":
        def insertion_func(article: Article, form: Optional[dict] = None) -> Article:
            old_paragraphs = article.blocks
            new_article = article.copy()
            new_paragraphs = []
            insertion_func_res = task.task(
                list(map(lambda p: p.content, old_paragraphs)),
                form
            ) if form is not None else task.task(list(map(lambda p: p.content, old_paragraphs)))
            # the type of insertion_func_res is like this:
            # [{"position": 1, "content": "hello world"}, {"position": 3, "content": "hello world"}]
            for index, paragraph in enumerate(old_paragraphs):
                new_paragraphs.append(
                    Block(BlockLevelEnum.Paragraph, BlockTypeEnum.Normal, paragraph.content, None,
                          BlockStatusEnum.Untouched))
                for insert_res in insertion_func_res:
                    if insert_res["position"] == index:
                        new_paragraphs.append(
                            Block(BlockLevelEnum.Paragraph, BlockTypeEnum.Quote, insert_res["content"], None,
                                  BlockStatusEnum.New))

            new_article.blocks = new_paragraphs
            return new_article

        res_func = insertion_func

    elif task.task_type == "custom":
        res_func = task.task

    return InteractiveFunctionType(
        id=task.id,
        name=task.name,
        form=task.form if task.form is not None else None,
        description=task.description,
        function=res_func
    )


CompositionType = Literal["exclusive", "pipelined", "compatible"]


class Composition:

    # tasks could be either InteractiveTaskType or Composition
    def __init__(self, type: CompositionType, *tasks: Union[InteractiveTaskConfiguration, Composition]):
        self.type = type
        self.tasks = tasks


class Exclusive(Composition):
    def __init__(self, *t: Union[InteractiveTaskConfiguration, Composition]):
        super().__init__("exclusive", *t)


class Pipelined(Composition):
    def __init__(self, *t: Union[InteractiveTaskConfiguration, Composition]):
        super().__init__("pipelined", *t)


class Compatible(Composition):
    def __init__(self, *t: Union[InteractiveTaskConfiguration, Composition]):
        super().__init__("compatible", *t)


class TaskTree:

    @staticmethod
    def to_node(task: Union[InteractiveTaskConfiguration, Composition]) -> Node:
        if isinstance(task, Composition):
            node = Node(task.type, "/", type=task.type)
            for subtask in task.tasks:
                sub = TaskTree.to_node(subtask)
                sub.parent = node
            return node

        else:
            task = InteractiveTaskType(task)
            return Node(task.id, "/", task=task)

    def __init__(self, root: Union[InteractiveTaskConfiguration, Composition]):
        self.tree = TaskTree.to_node(root)

    def get_leaves(self) -> List[InteractiveTaskType]:
        leaves = findall(self.tree, lambda node: node.is_leaf)
        return list(map(lambda node: node.task, leaves))

    def run_function(self, task_ids: list[str], article: Article, function_forms: dict) -> Article:
        def iter_node(node: Node) -> InteractiveFunctionType | None:
            node_task = node.get_attr("task")
            if node_task is not None:

                if node_task.id in task_ids:
                    return get_interactive_function(node_task)
                else:
                    return None
            else:
                functions = []
                ids = []
                for child in node.children:
                    child_function = iter_node(child)
                    if child_function is not None:
                        functions.append(child_function)
                        ids.append(child_function.id)

                node_type = node.get_attr("type")

                if node_type == "exclusive":
                    def exclusive(_article: Article, _function_forms: dict) -> Article:
                        return exclusive_functions(functions, _article, _function_forms)

                    return InteractiveFunctionType(
                        id="-".join(ids),
                        name="exclusive" + "-".join(ids),
                        description="exclusive" + "-".join(ids),
                        function=exclusive,
                    )
                elif node_type == "pipelined":
                    def pipelined(_article: Article, _function_forms: dict) -> Article:
                        return pipeline_functions(functions, _article, _function_forms)

                    return InteractiveFunctionType(
                        id="-".join(ids),
                        name="pipelined" + "-".join(ids),
                        description="pipelined" + "-".join(ids),
                        function=pipelined,
                    )
                elif node_type == "compatible":
                    def compatible(_article: Article, _function_forms: dict) -> Article:
                        return compatible_functions(functions, _article, _function_forms)

                    return InteractiveFunctionType(
                        id="-".join(ids),
                        name="compatible" + "-".join(ids),
                        description="compatible" + "-".join(ids),
                        function=compatible,
                    )
                else:
                    raise NotImplementedError

        return iter_node(self.tree).function(article, function_forms)


class TaskModelConfiguration:
    def __init__(self,
                 name: str,
                 description: str,
                 tasks: Union[InteractiveTaskConfiguration, Composition]
                 ):
        self.name = name
        self.description = description
        self.task_tree = TaskTree(tasks)
