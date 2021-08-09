import json
from typing import Union

class JSONUtils:
    def load(filePath:str) -> Union[dict, list]:
        with open(file=filePath, mode="r") as File: 
            return json.load(fp=File)

    def write(filePath: str, object: Union[dict, list], indent: int=4) -> None:
        with open(file=filePath, mode="w") as File:
            json.dump(fp=File, obj=object, indent=indent)

def setup(app):
    app.add_cog(JSONUtils(app))