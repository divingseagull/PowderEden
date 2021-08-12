from typing import Union
from discord.ext import commands
import discord

from Utils.JSONUtils import JSONUtils
from Utils.Errors import *


# TODO: map_index를 확장하기
# 1. 모든 (x, y)를 키로 하는 값을 생성
# 2. 천연자원 추가
# 3. Tile 클래스가 하는 일을 map_index로 옮기기
# => map_index를 NoSQL처럼 만들기
# 👍

class Map: # 수정 예정
    def __init__(self, x, y, void="0"):
        self.void = void

        self.map_border = (x, y)
        self.map_data = self.map_init(x, y, self.void)

        # Map의 실질적인 정보
        self.map_index = dict()

    def map_init(self, x, y, void):
        """
        Map의 겉모습 및 map_index 생성
        """

        sub    = list()
        result = list()

        for kx in range(x):
            for ky in range(y):
                self.map_index[(x, y)] = {
                    "owner": {
                        # 소유자
                    },
                    "entity": {
                        # (x, y)에 있는 개체
                    },
                    "resource": { 
                        # (x, y)에 있는 천연자원
                    }
                }

        for i in range(x):
            sub.append(void)

        for i in range(y):
            result.append(sub[:])

        return result

    def map_view(self):
        """
        Map의 겉모습 출력
        """

        result = ""
        for col in self.map_data:
            for wid in col:
                result += wid
            result += '\n'

        print(result)

    def map_update(self, obj, mode: str):
        """
        Map의 겉모습 수정
        
        add일 경우 obj.shape를 해당 좌표에 놓음
        del일 경우 obj.location에 해당하는 좌표를 void로 교체
        """

        loc = obj.location
        if mode == "add":
            self.map_data[loc[0]][loc[1]] = obj.shape
        
        elif mode == "del":
            self.map_data[loc[0]][loc[1]] = self.void

    def map_add_obj(self, obj, postX: int = None, postY: int = None):
        """
        Map에 obj 추가하기
        """

        (x, y) = obj.location

        # 좌표가 명시되어 있는지 확인
        if postX and postY: 
            (x, y) = (postX, postY)

        # 같은 좌표에 객체가 있는지 확인
        if (x, y) in self.map_index: raise AlreadyObjectExistError(f'{(x, y)}에는 이미 {self.map_index[(x, y)]}이(가) 존재합니다!')

        else:
            obj = self.obj_init(obj_name, x, y, shape)
            self.map_index[(x, y)] = obj
            self.map_update(obj, "add")
    
    def map_del_obj(self, obj):
        """
        Map에서 obj 삭제하기
        """

        (x, y) = obj.location

        if (x, y) in self.map_index:
            del self.map_index[(x, y)]
            self.map_update(obj, "del")
    
    def map_mov_obj(self, obj, postX, postY):
        """
        Map에서 obj 이동하기
        """

        (x, y) = obj.location

        self.map_del_obj(obj)
        self.map_add_obj(obj, postX, postY)

class Tile(Map):
    _map: Union[dict, list] = None

    def __init__(self, x: int, y: int) -> None: 
        super().__init__()
        self.x: int = x
        self.y: int = y

        tileData = \
            {
                "Owner": None
            }
        for i in range(0, self.x+1):
            for j in range(0, self.y):
                pass

    def _updateMap(self, object: Union[dict, list]) -> None:
        tmpMap = self.getInfo()
        tmpMap.update(object)
        JSONUtils.write("Data/Map.json", tmpMap)
        
    def getInfo(self) -> dict:
        try:
            self._map = JSONUtils.load("Data/Map.json")
            self._map[self.x][self.y]
        except IndexError:
            raise InvalidTileError("tile out of range")
        else:
            return self._map[self.x][self.y]

    def getOwner(self) -> str:
        return self.getInfo()["Players"]["Home"]["Username"]

    def getUnits(self) -> dict:
        return { 
            "Home": self.getInfo()["Players"]["Home"]["Ships"], 
            "Away": self.getInfo()["Players"]["Away"]["Ships"]
        }

    def getBuildings(self) -> dict:
        return self.getInfo()["Players"]["Home"]["Buildings"]

    def getResourceInfo(self) -> dict:
        return self.getInfo()["Resources"]

    def replaceOwner(self) -> None:
        tmpData = self.getInfo()
        tmpData["Home"]["Username"] = tmpData["Away"]["Username"]
        self._updateMap(tmpData)

    def deployUnits(self) -> None:
        pass

    def buildBuildings(self) -> None:
        pass