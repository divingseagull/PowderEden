from typing import Union
import json

from .Errors import *


class JSONUtils:
    def load(filePath: str) -> Union[dict, list]:
        with open(file=filePath, mode="r") as File:
            return json.load(fp=File)

    def write(filePath: str, object: Union[dict, list], indent: int = 4) -> None:
        with open(file=filePath, mode="w") as File:
            json.dump(fp=File, obj=object, indent=indent)

    def update(filePath: str, object: Union[dict, list], indent: int = 4) -> None:
        with open(file=filePath, mode="r") as File:
            try:
                tmp: dict = json.load(fp=File)
                tmp.update()
            except TypeError:
                raise CannotUpdateListError("Can't update list")
