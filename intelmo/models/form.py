from typing import Union

from pydantic import BaseModel


class FormItem(BaseModel):
    name: str
    label: str
    type: str

    defaultValue: Union[str, int, float, bool] = None
    # slider specific
    min: Union[int, float] = None
    max: Union[int, float] = None
    step: Union[int, float] = None
    # text specific
    placeholder: str = ""
    # select specific
    multiple: bool = False
    options: list = None

    def __init__(self, **data):
        super().__init__(**data)
        assert self.name is not None
        assert self.label is not None
        assert self.type is not None
        if self.type == "number":
            assert self.min is not None
            assert self.max is not None
            assert self.step is not None
        elif self.type == "select":
            assert self.options is not None


Form = list[FormItem]


