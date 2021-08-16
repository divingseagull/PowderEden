import math
import uuid

from typing import Optional
from Modules.Map import Map

from .Utils.Errors import *

class Entity:
    """
    모든 개체의 부모 클래스

    Map클래스의 인스턴스를 mapInstance로 받는다
    """
    
    def __init__(self, owner, mapInstance, shape, x, y, name: Optional[str]):
        self.uuid:     str = str(uuid.uuid4())
        self.owner:    str = owner
        self.map:      Map = mapInstance
        self.shape:    str = shape
        self.location: tuple = (x, y)
        self.mobilityPoint: int
        self.defensePoint:  int
        self.firepower:     int
        self.cost: dict = {
            "Iron": 0,
            "Oil":  0,
            "Exot": 0
        }
        self.destroyed: bool = False

        # 개체의 이름 (옵션)
        if name:
            self.name = name

        # 개체의 프로필
        self.profile = {
            self.uuid: {
                "entity": self, # 개체 인스턴스
                "entityOwner": self.owner, # 개체 소유자
                "entityType": type(self).__name__, # 개체 클래스 이름
                "entityBase": self.__class__.__bases__[0].__name__ # 개체 부모 클래스 이름
            }
        }
        
    # defensePoint가 0이하인 값으로 할당될 경우 파괴
    def __setattr__(self, name, value):
        if name == 'defensePoint':
            if value <= 0:
                self.destroy()
        super().__setattr__(name, value)

    # 개체가 파괴될 경우
    def __del__(self):
        self.map.obj_del(self)
        print(f'{self.name}이 파괴되었습니다!')

    def move(self, dx, dy):
        """
        dx, dy:  x, y 좌표 기준 이동 거리.\n
        이동력이 부족할 경우 오류가 발생합니다
        """

        # FIXME: 불필요한 에러?
        if self.mobilityPoint == 0: raise MobilityPointZeroError("can't move this entity. mobility point is 0")
        
        (x, y) = self.location
        (bx, by) = map.border
        mp = self.mobilityPoint
        
        # 이동력이 충분한지 확인
        if mp < math.sqrt(dx ** 2 + dy ** 2): raise NotEnoughMobilityPointError("can't move this entity. not enough mobility point")

        postX = x + dx
        postY = y + dy
        
        # 맵 경계를 벗어나는지 확인
        if not 0 <= postX < bx or not 0 <= postY < by: raise MapBorderOutError()
        
        # 맵에서 이동
        self.map.obj_mov(self, (postX, postY))
    
    def destroy(self) -> None:
        """
        유닛을 맵에서 제거합니다
        """

        self.destroyed = True
        self.__del__()

class Building(Entity):
    """
    모든 건물의 부모 클래스, Entity 클래스의 자식
    """

    def __init__(self):
        super().__init__()

        self.mobilityPoint = 0
        self.defensePoint: int
        self.firepower:   int
    
    def build(self, x, y) -> None:
        """
        현재 위치에 건물을 건설합니다
        """
        self.location = (x, y)
        self.map.map_add_obj(self)

class ResourceMine(Building):
    def __init__(self):
        super().__init__()

        self.resourceOutputMultiplier = 1
        self.defensePoint = 0
        
class Shipyard(Building):
    def __init__(self):
        super().__init__()

        self.unitSpawner  = True
        self.defensePoint = 0
        
class Ship(Entity):
    """
    모든 함선의 부모 클래스, Entity 클래스의 자식
    """
    def __init__(self):
        super().__init__()

    # 정찰함   4    iron  1  oil   3    hp  0 att
    # 호위함   15   iron  5  oil   10   hp  1 att
    # 구축함   60   iron  20 oil   30   hp  5 att
    # 순양함   240  iron  5  exot  90   hp  25 att
    # 전함     960  iron  20 exot  270  hp  125 att
    # 우주모함 3840 iron  80 exot  1100 hp  600 att

class Scout(Ship):
    def __init__(self):
        super().__init__()
        
        self.defensePoint  = 3
        self.mobilityPoint = 3
        self.firepower     = 0
        self.cost = {
            "Iron": 4,
            "Oil":  1
        } 

class Frigate(Ship):
    def __init__(self):
        super().__init__()

        self.defensePoint  = 10
        self.mobilityPoint = 3
        self.firepower     = 1,
        self.cost = {
            "Iron": 15,
            "Oil":  5
        }

class Destroyer(Ship):
    def __init__(self):
        super().__init__()

        self.defensePoint  = 30
        self.mobilityPoint = 2
        self.firepower     = 5
        self.cost = {
            "Iron": 60,
            "Oil":  20
        }

class Cruiser(Ship):
    def __init__(self):
        super().__init__()

        self.defensePoint  = 90
        self.mobilityPoint = 2
        self.firepower     = 25
        self.cost = {
            "Iron": 240,
            "Exot": 5
        }

class Battleship(Ship):
    def __init__(self):
        super().__init__()

        self.defensePoint  = 270
        self.mobilityPoint = 1
        self.firepower     = 125
        self.cost = {
            "Iron": 960,
            "Exot": 20
        }

class Carrier(Ship): 
    def __init__(self):
        super().__init__()

        self.defensePoint  = 1100
        self.mobilityPoint = 1
        self.firepower     = 600
        self.cost = {
            "Iron": 3840,
            "Exot": 80
        }