from typing import List

from flask import Flask, redirect

from .controllers import rss_controller, reader_controller
from .models.task import TaskModelConfiguration
from .types.model import InteractiveTaskType, InteractiveTaskConfiguration, CompositionType


class Server(Flask):
    def __init__(self, configuration: TaskModelConfiguration):
        super().__init__(__name__)
        self.config['DEBUG'] = True
        self.config['model'] = configuration.config

        @self.route('/')
        def index():
            return redirect("/rss")

        self.register_blueprint(rss_controller.rss_page, url_prefix='/rss')
        self.register_blueprint(reader_controller.reader_page, url_prefix='/reader')


def create_server(name: str, description: str, tasks: List[InteractiveTaskConfiguration], composition: CompositionType):
    processed_tasks = []
    for task in tasks:
        processed_tasks.append(InteractiveTaskType(task))

    return Server(TaskModelConfiguration(name, description, processed_tasks, composition))
