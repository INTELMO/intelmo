from typing import List, Union

from flask import Flask, redirect

from . import Composition
from .controllers import rss_controller, reader_controller
from .models.task import TaskModelConfiguration
from .types.model import InteractiveTaskType, InteractiveTaskConfiguration, CompositionType


class Server(Flask):
    def __init__(self, configuration: TaskModelConfiguration):
        super().__init__(__name__)
        self.config['DEBUG'] = True
        self.config['model'] = configuration

        @self.route('/')
        def index():
            return redirect("/rss")

        self.register_blueprint(rss_controller.rss_page, url_prefix='/rss')
        self.register_blueprint(reader_controller.reader_page, url_prefix='/reader')


def create_server(name: str, description: str,
                  tasks: Union[InteractiveTaskConfiguration, Composition]):
    return Server(TaskModelConfiguration(name, description, tasks))
