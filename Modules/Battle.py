from discord.ext import commands
import discord
import math

from Tile import Tile

from Units import *

from Utils.Errors import *
from Utils.Utils import *

class Battle(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
        # 전투를 진행할 타일 목록
        self.battleQueue = [ ]
        # 피해 우선순위
        self.damagePriority = [
            "SCOUT",
            "FRIGATE",
            "DESTROYER",
            "CRUISER",
            "BATTLESHIP"
        ]

        # 방어 건물 정보
        # FIXME: DefensePoint.a, b name
        self.defenderInfo = {
            "DefensePoint": {
                "a": 0,
                "b": 0
            }
        }

    def calculateBase(self, baseDict: dict, goalDict: dict, mode=None):
        """
        능력치 계산 함수

        :param baseDict: 연산으로 구분된 계산 항목

        
        {   // 예시
            calc_mode: {
                obj: {
                    const: int or float... numeric
                }
            }

            plus: {
                // 함선1의 화력에 5를 더한다
                함선1 : {
                    화력: 5
                }
            },

            minus: {...},

            multiply: {
                // 건물2의 방어력에 1.2를, 내구도에 1.5를 곱한다
                건물2: {
                    방어력: 1.2,
                    내구도: 1.5
                }
            },

            divide: {...},

            power: {...}, // 넣지 말까... 

            log: {...} // idk...
        }

        :param goalDict: 연산을 적용할 항목
        :param mode: 연산 적용 후 내보낼 mode, None일 경우 dict로 내보냄, "sum"일 경우 합산한 것을 내보냄
        :return: 적용된 연산을 반환
        """
        
        resultDict: dict = {}
        sumFloat: float = 0

        for calc_mode in baseDict:
            for obj in baseDict[calc_mode]:
                for const in baseDict[calc_mode][obj]:
                    result = calc(recursiveLookup(obj, goalDict, dict)[const], obj[const], calc_mode)
                    resultDict[calc_mode] = {
                        obj: {
                            const: result
                        }
                    }
                    sumFloat += result

        if mode == "sum":
            return sumFloat
        else:
            return resultDict

    def calculateFirePower(self, ships: dict) -> int:
        # FIXME: SHIP_INFO 
        """
        ships 인자로 들어온 함선의 수 만큼 전투력을 모두 더하여 반환합니다
        """
        shipDict: dict = {
            'multiply': {
            }
        }

        for ship in SHIP_INFO:
            shipDict['multiply'][ship] = {
                'FirePower': ship['FirePower']
            }

        return self.calculateBase(shipDict, ships, 'sum')
    
    def calculateDefensePoint(self, ships: dict, buildings: dict) -> int:
        # FIXME: SHIP_INFO
        """
        `ships` 인자로 들어온 함선의 수와 해당 타일의 방어 건물만큼 방어력을 모두 더하여 반환합니다
        """

        defenceDict: dict = {
            'multiply': {
            }
        }

        for ship in SHIP_INFO:
            defenceDict['multiply'][ship] = {
                'DefensePoint': ship['DefensePoint']
            }

        # TODO: 방어 건물 dict도 baseDict에 추가

        return self.calculateBase(defenceDict, [ships, buildings], 'sum')

    def startBattle(self, x: int, y: int) -> None:
        """
        해당 타일이 전투 대기열에 존재하면 전투를 시작합니다
        """

        # A의 체력 합 - 나머지의 공격력 합 = A의 남은 체력
        # 호위함들 전체 체력보다 피해량이 더 높다면, (피해량 - 호위함 전체 체력) / (구축함 수)

        if (x or y) not in self.battleQueue:
            raise InvalidTileError("can't find tile from battle queue")

        tile  = Tile(x, y)
        units = tile.getUnits()

        damageResult: int = 0
        battleResult = self.calculateFirePower(units["Home"]) - \
                       self.calculateDefensePoint(units["Away"], tile.getBuildings()["Defense"])
        
        if battleResult < 0: Tile.replaceOwner()

        for shipType in self.damagePriority:
            if units["Away"][shipType] == 0: continue # if ship count is 0: continue
            damageResult += math.floor((self.calculateDefensePoint(units["Home"], tile.getBuildings()["Defense"]) - \
                units["Away"]["Frigate"]) / units["Away"][shipType])     

def setup(client):
    client.add_cog(Battle(client))
