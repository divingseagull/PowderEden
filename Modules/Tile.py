from typing import Union
from discord.ext import commands
import discord

from Utils.JSONUtils import JSONUtils
from Utils.Errors import *

class Tile:
    _map: Union[dict, list] = None

    def __init__(self, x: int, y: int) -> None: 
        self.x: int = x
        self.y: int = y

        tileData = \
            {
                "Owner": None
            }
        for i in range(0, self.x+1):
            for j in range(0, self.y):
                pass
        
    def currentMap(self) -> dict:
        try:
            self._map = JSONUtils.load("Data/Map.json")
            self._map[self.x][self.y]
        except IndexError:
            raise InvalidTileError("tile out of range")
        else:
            return self._map[self.x][self.y]

    def getOwner(self) -> str:
        return self.currentMap()["Owner"]

    def getUnits(self) -> dict:
        return { 
            "Home": self.currentMap()["Home"], 
            "Away": self.currentMap()["Away"]
        }

    def getBuildings(self) -> dict:
        pass

    def replaceOwner(self) -> None:
        tileData = JSONUtils.load("Data/Map.json")
        tileData[self.x][self.y][]

    def deployUnits(self) -> None:
        pass

    def buildBuildings(self) -> None:
        pass