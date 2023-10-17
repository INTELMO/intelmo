
from typing import List
from models.form import Form
from models.task import InteractiveTaskType
from nicegui import ui

enabled_functions = []
function_forms = {}


def toggle_function(function_id: str, status: bool = None, on_update: callable = None):
    global enabled_functions, function_forms

    if status is None:
        if function_id in enabled_functions:
            enabled_functions.remove(function_id)
        else:
            enabled_functions.append(function_id)

    else:
        if status:
            enabled_functions.append(function_id)
        else:
            enabled_functions.remove(function_id)

    if on_update is not None:
        on_update(enabled_functions, function_forms)

    # remove all headers
    # ui.header.clear()
    make_header.refresh()
    # make_header_item.refresh()


def make_form(form: Form, function_id: str, on_update: callable = None):

    global function_forms

    values = {}
    for formItem in form:
        form_value = function_forms.get(function_id, {}).get(formItem["name"])

        if form_value is None:
            form_value = formItem["defaultValue"]

        if formItem["type"] == "text":
            ui.input(label=formItem["label"], value=form_value,
                     on_change=lambda e: values.update({formItem["name"]: e.value}))
        elif formItem["type"] == "number":
            ui.number(label=formItem["label"], value=form_value, min=formItem["min"],
                      max=formItem["max"], step=formItem["step"], on_change=lambda e: values.update({formItem["name"]: e.value}))
        elif formItem["type"] == "select":
            ui.select(label=formItem["label"], value=form_value, options=formItem["options"], multiple=formItem["multiple"],
                      on_change=lambda e: values.update({formItem["name"]: e.value}))
        elif formItem["type"] == "boolean":
            ui.checkbox(label=formItem["label"], value=form_value,
                        on_change=lambda e: values.update({formItem["name"]: e.value}))

    def update(values):
        function_forms.update({function_id: values})
        toggle_function(function_id, True, on_update=on_update)

    ui.button("Submit").on(
        "click", lambda: update(values))


@ui.refreshable
def make_header_item(function: InteractiveTaskType, enabled: bool, on_update: callable = None):

    class MenuOpen:
        def __init__(self, visibility: bool = False):
            self.visibility = visibility

    menu_open = MenuOpen(False)

    # if enabled, underline
    if function.form:
        with ui.element("div").on("mouseover", lambda: setattr(menu_open, "visibility", True)).on("mouseout", lambda: setattr(menu_open, "visibility", False)):
            ui.label(function.name).classes(
                "underline cursor-pointer group" if enabled else "cursor-pointer group").on("click", lambda: toggle_function(function.id, None, on_update=on_update))
            with ui.element("div").classes("group-hover:visible z-50 p-5 w-60 flex-col space-y-4 bg-white rounded-lg shadow-lg absolute z-50").bind_visibility_from(menu_open, "visibility"):
                make_form(function.form, function_id=function.id,
                          on_update=on_update)

    else:
        ui.label(function.name).classes(
            "underline cursor-pointer" if enabled else "cursor-pointer").on("click", lambda: toggle_function(function.id, None, on_update=on_update))


@ui.refreshable
def make_header(functions: List[InteractiveTaskType], on_update: callable = None):

    global enabled_functions
    # with ui.header().classes("bg-white text-black shadow-lg z-20"):
    with ui.element("header").classes("fixed mx-[-16px] top-0 w-full shadow-lg p-4 bg-white space-x-4 flex flex-row z-40"):
        for function in functions:
            make_header_item(
                function, function.id in enabled_functions, on_update=on_update)
