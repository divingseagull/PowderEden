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
        
    def getMap(self) -> dict:
        try:
            self._map = JSONUtils.load("Data/Map.json")
            self._map[self.x][self.y]
        except IndexError:
            raise InvalidTileError("tile out of range")
        else:
            return self._map[self.x][self.y]

    def _updateMap(self, object: Union[dict, list]):
        pass

    def getOwner(self) -> str:
        return self.getMap()["Players"]["Home"]["Username"]

    def getUnits(self) -> dict:
        return { 
            "Home": self.getMap()["Players"]["Home"]["Ships"], 
            "Away": self.getMap()["Players"]["Away"]["Ships"]
        }

    def getBuildings(self) -> dict:
        pass

    def replaceOwner(self) -> None:
        tmpData = self.getMap()
        tmpData["Home"]["Username"] = tmpData["Away"]["Username"]
        self._updateMap(tmpData)

    def deployUnits(self) -> None:
        pass

    def buildBuildings(self) -> None:
        pass
