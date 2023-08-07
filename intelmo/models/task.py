from typing import List, Optional

import nltk

from ..models.article import Article
from ..models.block import Block, BlockLevelEnum, BlockTypeEnum, BlockStatusEnum
from ..types.model import ModelConfiguration, InteractiveTaskType, InteractiveFunctionType, \
    CompositionType

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def get_interactive_function(task: InteractiveTaskType) -> InteractiveFunctionType:
    res_func = None
    if task.task_type == "highlight":
        def highlight_func(article: Article, form: Optional[dict] = None) -> Article:
            new_article = article.copy()
            paragraphs = article.blocks
            total_text = '\n'.join(map(lambda p: p.content, paragraphs))
            highlight_res = task.task(total_text, form) if form is not None else task.task(total_text)
            processed_paragraphs = []
            for paragraph in paragraphs:
                # split the paragraph into sentences
                sentences = nltk.sent_tokenize(paragraph.content)
                processed_sentences = []
                for sentence in sentences:
                    # if the sentence is highlighted, add it to the list
                    if sentence in highlight_res:
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

        res_func = highlight_func

    elif task.task_type == "generation":
        def generation_func(article: Article, form: Optional[dict] = None) -> Article:
            new_article = article.copy()
            # paragraphs = list(map(lambda p: Block(
            #     BlockLevelEnum.Paragraph, BlockTypeEnum.Normal, p.content, None), article.blocks))
            total_text = article.get_content()

            generation_res = task.task(total_text, form) if form is not None else task.task(total_text)

            global_block = Block(BlockLevelEnum.Global, BlockTypeEnum.Normal, generation_res, None, BlockStatusEnum.New)
            new_article.global_block = global_block
            return new_article

        res_func = generation_func

    elif task.task_type == "insert":
        def insert_func(article: Article, form: Optional[dict] = None) -> Article:
            old_paragraphs = article.blocks
            new_article = article.copy()
            new_paragraphs = []
            insert_func_res = task.task(
                list(map(lambda p: p.content, old_paragraphs)),
                form
            ) if form is not None else task.task(list(map(lambda p: p.content, old_paragraphs)))
            # the type of insert_func_res is like this:
            # [{"position": 1, "content": "hello world"}, {"position": 3, "content": "hello world"}]
            for index, paragraph in enumerate(old_paragraphs):
                new_paragraphs.append(
                    Block(BlockLevelEnum.Paragraph, BlockTypeEnum.Normal, paragraph.content, None,
                          BlockStatusEnum.Untouched))
                for insert_res in insert_func_res:
                    if insert_res["position"] == index:
                        new_paragraphs.append(
                            Block(BlockLevelEnum.Paragraph, BlockTypeEnum.Quote, insert_res["content"], None,
                                  BlockStatusEnum.New))

            new_article.blocks = new_paragraphs
            return new_article

        res_func = insert_func

    elif task.task_type == "custom":
        res_func = task.task

    return InteractiveFunctionType(
        id=task.id,
        name=task.name,
        form=task.form if task.form is not None else None,
        description=task.description,
        function=res_func
    )


# class TaskModelConfiguration(BaseModel):
#     name: str
#     description: str
#     tasks: List[InteractiveTaskType]
#     composition: Optional[CompositionType] = "parallel"
#
#     def __init__(self, name: str, description: str,
#                  tasks: List[InteractiveTaskConfiguration],
#                  composition: Optional[CompositionType] = "parallel"):
#         processed_tasks = []
#         for task in tasks:
#             processed_tasks.append(InteractiveTaskType(task))
#
#         super().__init__(name=name, description=description, tasks=processed_tasks, composition=composition)


class TaskModelConfiguration:
    def __init__(self, name: str, description: str,
                 tasks: List[InteractiveTaskType],
                 composition: Optional[CompositionType] = "parallel"):
        functions = []
        for task in tasks:
            functions.append(get_interactive_function(task))

        self.config = ModelConfiguration(name, description, functions, composition)
