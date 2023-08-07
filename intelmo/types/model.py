from typing import Callable, List, TypedDict, Optional
from typing_extensions import NotRequired, Literal

from ..models.block import Block
import itertools

from ..models.form import Form
from ..models.article import Article

# composition type: parallel, exclusive
CompositionType = Literal["parallel", "exclusive", "pipeline"]


class InteractiveRssType:
    def __init__(self, title: str, url: str, paragraphs: list[Block]):
        self.title = title
        self.url = url
        self.paragraphs = paragraphs


class InteractiveFunctionResultType:
    def __init__(self, blocks: List[Block], global_block: Optional[Block]):
        self.blocks = blocks
        self.global_block = global_block


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


TaskType = Literal["highlight", "insert", "generation", "custom"]


class InteractiveTaskConfiguration(TypedDict):
    name: str
    description: str
    task_type: TaskType
    # task is one of the values in TaskType
    task: Callable
    form: NotRequired[Form]


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


class ModelConfiguration:
    def __init__(self, name: str, description: str,
                 functions: List[InteractiveFunctionType],
                 composition: CompositionType):
        self.name = name
        self.description = description
        self.functions = functions
        self.composition = composition

    def get_function(self, _id: str) -> InteractiveFunctionType or None:
        for function in self.functions:
            if function.id == _id:
                return function
        return None

    def __str__(self):
        return f'{self.name}: {self.description}'

    def __repr__(self):
        return f'{self.name}: {self.description}'

    def __dict__(self):
        return {
            'name': self.name,
            'description': self.description,
        }
