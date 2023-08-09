from typing import List, Optional, Union

import nltk

from .composition import Composition, TaskTree
from ..models.article import Article
from ..models.block import Block, BlockLevelEnum, BlockTypeEnum, BlockStatusEnum
from ..types.model import ModelConfiguration, InteractiveTaskType, InteractiveFunctionType, \
    CompositionType, InteractiveTaskConfiguration


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


# class _TaskModelConfiguration:
#     def __init__(self, name: str, description: str,
#                  tasks: List[InteractiveTaskType],
#                  composition: Optional[CompositionType] = "parallel"):
#         functions = []
#         for task in tasks:
#             functions.append(get_interactive_function(task))
#
#         self.config = ModelConfiguration(name, description, functions, composition)


class TaskModelConfiguration:
    def __init__(self,
                 name: str,
                 description: str,
                 tasks: Union[InteractiveTaskConfiguration, Composition]
                 ):
        self.task_tree = TaskTree(tasks)
