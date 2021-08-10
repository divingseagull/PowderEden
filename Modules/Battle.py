from discord.ext import commands
import discord

from Tile import Tile

from Utils.Errors import *

class Battle(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
        # 전투를 진행할 타일 목록
        self.battleQueue = [ ]
        # 피해 우선순위
        self.damagePriority = [
            "FRIGATE",
            "DESTROYER",
            "CRUISER",
            "BATTLESHIP"
        ]
        # 함선 정보
        self.shipInfo = {
            # FIXME: FirePower, DefensePoint ships value
            "FirePower": {
                "carrier":    0,
                "battleship": 0,
                "destroyer":  0,
                "cruiser":    0,
                "frigate":    0
            },
            "DefensePoint": {
                "carrier":    0,
                "battleship": 0,
                "destroyer":  0,
                "cruiser":    0,
                "frigate":    0
            }
        }
        # 방어 건물 정보
        # FIXME: DefensePoint.a, b name
        self.defenderInfo = {
            "DefensePoint": {
                "a": 0,
                "b": 0
            }
        }

    def calculateBase(self, baseDict: dict, goalDict: dict) -> int:
        sum: int = 0
        
        for goalTuple in goalDict.items():
            if goalTuple[0] in baseDict.keys():
                sum += baseDict(goalTuple[0]) * goalTuple[1]
        
        return sum

    def calculateFirePower(self, ships: dict) -> int:
        """
        ships 인자로 들어온 함선의 수 만큼 전투력을 모두 더하여 반환합니다
        """
        return self.calculateBase(self.shipInfo['FirePower'], ships)
    
    def calculateDefensePoint(self, ships: dict, buildings: dict) -> int:
        """
        `ships` 인자로 들어온 함선의 수와 해당 타일의 방어 건물만큼 방어력을 모두 더하여 반환합니다
        """
        return self.calculateBase(self.shipInfo['DefensePoint'], ships) + \
               self.calculateBase(self.defenderInfo['DefensePoint'], buildings)

    def startBattle(self, x: int, y: int) -> None:
        """
        해당 타일이 전투 대기열에 존재하면 전투를 시작합니다
        """

        # A의 체력 합 - 나머지의 공격력 합 = A의 남은 체력
        # 호위함들 전체 체력보다 피해량이 더 높다면, (피해량 - 호위함 전체 체력) / (구축함 수)

        if (x or y) not in self.battleQueue:
            raise InvalidTileError("can't find tile from queue")

        tile  = Tile(x, y)
        units = tile.getUnits()

        battleResult = self.calculateFirePower(units["Home"]) - \
                       self.calculateDefensePoint(units["Away"])

        if battleResult < 0:
            Tile.replaceOwner()
            
            for shipType in self.damagePriority:
                if shipType == 0: continue
                (self.calculateFirePower(units["Away"]) - units["Away"]["Frigate"]) / units["Away"][shipType]

def setup(client):
    client.add_cog(Battle(client))