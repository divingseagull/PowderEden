from discord.ext import commands
import discord

from Utils.JSONUtils import JSONUtils
from Utils.Errors import *

class Tile:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __repr__(self):
        map = None
        try: 
            map = JSONUtils.load("Data/Map.json")
            map[self.x][self.y]
        except IndexError:
            raise InvalidTileError("tile out of range")
        else:
            return map[self.x][self.y]

    def getOwner(self):
        pass

    def getUnits(self):
        pass

    def getBuildings(self):
        pass

    def replaceOwner(self): 
        pass

    def deployUnits(self):
        pass

    def buildBuildings(self):
        pass