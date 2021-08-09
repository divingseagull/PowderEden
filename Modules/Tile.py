from typing import Union
from discord.ext import commands
import discord

from Utils.JSONUtils import JSONUtils
from Utils.Errors import *

class Tile:
    # TODO: _map testing
    _map: Union[dict, list] = None

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> dict:
        try: 
            self._map = JSONUtils.load("Data/Map.json")
            self._map[self.x][self.y]
        except IndexError:
            raise InvalidTileError("tile out of range")
        else:
            return self._map[self.x][self.y]

    def getOwner(self) -> str:
        pass

    def getUnits(self) -> dict:
        pass

    def getBuildings(self) -> dict:
        pass

    def replaceOwner(self) -> None: 
        pass

    def deployUnits(self) -> None:
        pass

    def buildBuildings(self) -> None:
        pass