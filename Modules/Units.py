import math

from .Map import Map

from Utils.Errors import *

class Entity:
    """
    모든 개체의 부모 클래스

    Map클래스의 인스턴스를 mapInstance로 받는다
    """
    def __init__(self, mapInstance, name, shape, x, y):
        self.map:      Map = mapInstance
        self.name:     str = name
        self.shape:    str = shape
        self.location: tuple = (x, y)
        self.healthPoint:   int
        self.mobilityPoint: int
        self.defensePoint:  int
        self.firepower:     int
        self.cost: dict = {
            "Iron": 0,
            "Oil":  0,
            "Exot": 0
        }
        self.destroyed: bool = False
    
    def __call__(self):
        if self.healthPoint <= 0: self.destroy()
    
    def __del__(self):
        self.map.map_del_obj(self)
        print(f'{self.name}이 파괴되었습니다!')

    def move(self, dx, dy):
        """
        dx, dy:  x, y 좌표 기준 이동 거리.\n
        이동력이 부족할 경우 오류가 발생합니다
        """
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
        self.map.map_mov_obj(self, postX, postY)
        self.location = (postX, postY)
    
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
        self.healthPoint: int
        self.firepower:   int
    
    def build(self, x, y) -> None:
        """
        현재 위치에 건물을 건설합니다
        """
        self.location = (x, y)
        self.map.map_add_obj(self)
        
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
        
        self.healthPoint   = 3
        self.mobilityPoint = 3
        self.firepower     = 0
        self.cost = {
            "Iron": 4,
            "Oil":  1
        } 

class Frigate(Ship):
    def __init__(self):
        super().__init__()

        self.healthPoint   = 10
        self.mobilityPoint = 3
        self.firepower     = 1,
        self.cost = {
            "Iron": 15,
            "Oil":  5
        }

class Destroyer(Ship):
    def __init__(self):
        super().__init__()

        self.healthPoint   = 30
        self.mobilityPoint = 2
        self.firepower     = 5
        self.cost = {
            "Iron": 60,
            "Oil":  20
        }

class Cruiser(Ship):
    def __init__(self):
        super().__init__()

        self.healthPoint   = 90
        self.mobilityPoint = 2
        self.firepower     = 25
        self.cost = {
            "Iron": 240,
            "Exot": 5
        }

class Battleship(Ship):
    def __init__(self):
        super().__init__()

        self.healthPoint   = 270
        self.mobilityPoint = 1
        self.firepower     = 125
        self.cost = {
            "Iron": 960,
            "Exot": 20
        }

class Carrier(Ship): 
    def __init__(self):
        super().__init__()

        self.healthPoint   = 1100
        self.mobilityPoint = 1
        self.firepower     = 600
        self.cost = {
            "Iron": 3840,
            "Exot": 80
        }