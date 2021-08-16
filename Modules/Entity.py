import uuid

from typing import Optional
from Modules.Map import Map

from .Utils.Errors import *
from .Utils.Utils import *


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
        self.mobilityPoint: int = 0
        self.defensePoint:  int = 0
        self.firepower:     int = 0
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

    def deploy(self, xy) -> None:
        """
        xy: (x, y)에 개체를 배치합니다
        """

        self.location = (xy[0], xy[1])
        self.map.obj_add(self)

    def move(self, dxy=None, pxy=None):
        """
        dxy: 현재 위치 기준 이동 거리.
        pxy: 절대 위치 기준 이동 거리.
        이동력이 부족할 경우 오류가 발생합니다
        """

        # FIXME: 불필요한 에러?
        if self.mobilityPoint == 0:
            raise MobilityPointZeroError("can't move this entity. mobility point is 0")
        
        (x, y) = self.location
        (bx, by) = self.map.map_border
        mp = self.mobilityPoint
        
        # 이동력이 충분한지 확인

        if dxy:
            if mp < distance((0, 0), (dxy[0], dxy[1])):
                raise NotEnoughMobilityPointError("can't move this entity. not enough mobility point")

            postX = x + dxy[0]
            postY = y + dxy[1]

        elif pxy:
            if mp < distance(self.location, pxy):
                raise NotEnoughMobilityPointError("can't move this entity. not enough mobility point")

            postX = pxy[0]
            postY = pxy[1]

        else:
            raise Exception("이동할 좌표가 존재하지 않습니다.")
        
        # 맵 경계를 벗어나는지 확인
        if not 0 <= postX < bx or not 0 <= postY < by:
            raise MapBorderOutError()
        
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mobilityPoint = 0
        self.defensePoint: int
        self.firepower:   int


class ResourceMine(Building):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.resourceOutputMultiplier = 1
        self.defensePoint = 0


class Shipyard(Building):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.unitSpawner  = True
        self.defensePoint = 0


class Ship(Entity):
    """
    모든 함선의 부모 클래스, Entity 클래스의 자식

    정찰함   4    iron  1  oil   3    hp  0 att
    호위함   15   iron  5  oil   10   hp  1 att
    구축함   60   iron  20 oil   30   hp  5 att
    순양함   240  iron  5  exot  90   hp  25 att
    전함     960  iron  20 exot  270  hp  125 att
    우주모함 3840 iron  80 exot  1100 hp  600 att
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.trace_xy = tuple()
        self.trace_entity: Entity = None
        self.trace_path = list()
        self.obstacle_type = ["sea"]

    def targeting(self, target):
        """
        타겟팅 함수

        정해진 위치나, 개체를 타겟팅 한다.
        Ship 개체는 타겟으로 자동 접근한다.
        """

        if type(target) == tuple and len(target) == 2:
            self.trace_xy = target
        else:
            self.trace_entity = target

    def trace(self):
        """
        목적지 좌표로 추적, 이동
        거리가 이동력보다 멀 경우, 이동력 만큼 근접하도록 이동함

        1. self.trace_xy: 정해진 (x, y)로 이동
        2. self.trace_entity: 타겟 개체의 (x, y)로 이동
        """

        if self.trace_xy or (self.trace_entity and not self.trace_entity.destroyed):
            target_xy = self.trace_xy or self.trace_entity.location

            # BiAStar 알고리즘으로 경로 (x, y)리스트 생성
            path = path_finding(self.map, self.obstacle_type, self.location, target_xy)

            best_xy = tuple()
            best_distance = 0

            # 최적 좌표 선택
            for xy in path:
                tmp_distance = distance(self.location, xy)
                if self.mobilityPoint >= tmp_distance > best_distance:
                    best_xy = xy[:]
                    best_distance = tmp_distance

            # 절대 좌표 기준 이동
            self.move(pxy=best_xy)

            # 도착시 타겟이 정해진 위치일 경우 초기화, 타겟이 개체일 경우 타겟팅 유지
            if self.location == self.trace_xy:
                self.trace_xy = tuple()


class Scout(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.defensePoint  = 3
        self.mobilityPoint = 3
        self.firepower     = 0
        self.cost = {
            "Iron": 4,
            "Oil":  1
        }


class Frigate(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.defensePoint  = 10
        self.mobilityPoint = 3
        self.firepower     = 1,
        self.cost = {
            "Iron": 15,
            "Oil":  5
        }


class Destroyer(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.defensePoint  = 30
        self.mobilityPoint = 2
        self.firepower     = 5
        self.cost = {
            "Iron": 60,
            "Oil":  20
        }


class Cruiser(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.defensePoint  = 90
        self.mobilityPoint = 2
        self.firepower     = 25
        self.cost = {
            "Iron": 240,
            "Exot": 5
        }


class Battleship(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.defensePoint  = 270
        self.mobilityPoint = 1
        self.firepower     = 125
        self.cost = {
            "Iron": 960,
            "Exot": 20
        }


class Carrier(Ship):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.defensePoint  = 1100
        self.mobilityPoint = 1
        self.firepower     = 600
        self.cost = {
            "Iron": 3840,
            "Exot": 80
        }