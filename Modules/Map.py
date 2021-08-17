from typing import Union

import random

from .Utils.JSONUtils import JSONUtils
from .Utils.Errors import *
from .Utils.Utils import *

# TODO: map_index를 확장하기
# 1. 모든 (x, y)를 키로 하는 값을 생성
# 2. 천연자원 추가
# 3. Tile 클래스가 하는 일을 map_index로 옮기기
# => map_index를 NoSQL처럼 만들기
# 👍


class Map:
    def __init__(self, xy, groundShape="■", backgroundShape="□"):

        # 맵의 저장 경로
        self.dump_path = "Data/Map.json"
        
        # 땅의 모양
        self.groundShape = groundShape
        
        # 바다(배경) 의 모양
        self.backgroundShape = backgroundShape

        # 맵의 크기
        self.map_border = (xy[0], xy[1])

        # Map의 실질적인 정보
        self.map_index = dict()

    def map_init(self, xy):
        """
        map_index 생성

        :xy: 맵의 가로, 세로 = (x, y)
        make_chunks를 호출하여 바다(배경) 타일을 생성함 - 긴 시간이 소요됨
        """

        for kx in range(xy[0]):
            for ky in range(xy[1]):
                self.map_index[(kx, ky)] = {
                    "Owner": "", # 소유자
                    "Players": { # 현재 타일에 있는 Entity의 주인들
                        "nature": { # 자연적으로 생성된 개체 (주인이 없는 개체들/중립 몹?)
                            "Entity": {
                                # (x, y)에 있는 개체
                            }
                        }
                    },

                    "Type": set(), # 타일의 타입 (땅/바다/...다른 여러가지 속성들...)

                    "Shape": "", # 타일의 모양

                    "Resource": { # (x, y)에 있는 천연/합성 자원
                        "Iron": 0,
                        "Oil":  0,
                        "Exot": 0
                    }
                }

        # 바다(배경) 타일 생성
        xy_tuple_list = self.make_chunks()
        for xy in xy_tuple_list:
            self.map_index[xy]["Shape"] = self.backgroundShape
            self.map_index[xy]["Type"].add("sea")
    
    def make_chunks(self, divergence=0.72, smooth_val=2, rand_dir=True, fill_empty=True):
        """
        바다(배경) 속성을 가진 타일의 좌표를 생성함

        :divergence: 분산도(값이 커질 수록 땅이 조각조각 남)

        잠정적인 최대 크기:
        (80 x 80, 0.5)
        (100 x 100, 0.8)

        넓고 보기 좋지만 시간이 많이 걸림:
        (200 x 200, 1)  - 40초 ~ 1분 정도
        """

        def rand_direction(xy, i, ind):
            """
            바다(배경)의 확산 방향

            :xy: 기준 좌표
            :i: 기준 좌표로부터 떨어진 거리
            :ind: 8방향 중 하나를 가리킴
            """

            tt = [
                (xy[0] + i, xy[1]),
                (xy[0], xy[1] + i),
                (xy[0] - i, xy[1]),
                (xy[0], xy[1] - i),

                (xy[0] + i, xy[1] + i),
                (xy[0] + i, xy[1] - i),
                (xy[0] - i, xy[1] + i),
                (xy[0] - i, xy[1] - i)
            ]

            return tt[ind]

        sx = self.map_border[0]
        sy = self.map_border[1]

        map_size = sx * sy
        rand_count = int((map_size ** (1 / 2)) * divergence)
        rand_xy_set = set()

        # 맵에 무작위로 배경을 1단위씩 생성
        for i in range(rand_count):
            rand_xy_set.add((random.randrange(sx), random.randrange(sy)))

        xy_list = list(rand_xy_set)
        rand_dir_seed = int(map_size ** (1 / 5))

        for i in range(int((map_size ** (1 / 6)) / divergence)):
            xy_set = set()

            for xy in xy_list:

                xy_set.add((xy[0], xy[1]))
                
                # 배경 1단위 주위에 배경 1단위를 무작위로 배치 - 상하좌우
                if bool(random.getrandbits(1)):
                    if (xy[0] + 1, xy[1]) in xy_set \
                            and (xy[0], xy[1] + 1) in xy_set \
                            and (xy[0] - 1, xy[1]) in xy_set \
                            and (xy[0], xy[1] - 1) in xy_set:
                        continue

                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0] + 1, xy[1]))
                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0], xy[1] + 1))
                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0] - 1, xy[1]))
                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0], xy[1] - 1))

                # 배경 1단위 주위에 배경 1단위를 무작위로 배치 - 대각선1
                if bool(random.getrandbits(1)):
                    if (xy[0] + 1, xy[1] - 1) in xy_set \
                            and (xy[0] - 1, xy[1] + 1) in xy_set:
                        continue

                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0] + 1, xy[1] - 1))
                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0] - 1, xy[1] + 1))

                # 배경 1단위 주위에 배경 1단위를 무작위로 배치 - 대각선2
                if bool(random.getrandbits(1)):
                    if (xy[0] + 1, xy[1] + 1) in xy_set \
                            and (xy[0] - 1, xy[1] - 1) in xy_set:
                        continue

                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0] + 1, xy[1] + 1))
                    if bool(random.getrandbits(1)):
                        xy_set.add((xy[0] - 1, xy[1] - 1))

                # 배경 1단위에서 뻗어나가는 무작위 길이의 배경으로 이루어진 선 / rand_dir=True 에서 작동
                if bool(random.getrandbits(1)) and rand_dir:
                    rand_seed = random.choice(range(rand_dir_seed - random.choice([0, 1])))
                    rand_num = random.choice(range(8))

                    for d in range(rand_seed):
                        xy_set.add(rand_direction(xy, d, rand_num))

            xy_list = list(xy_set)

        # 부드럽게 만들기 : fill_empty=True 에서 작동
        if fill_empty:
            # 배경에서 고립된 작은 조각들이 얼마나 고립되었는지 기록
            empt_dict = dict()
            for xy in xy_list:
                for i in range(8):
                    empt_pix = rand_direction(xy, 1, i)
                    if empt_pix in xy_list:
                        continue
                    else:
                        if empt_pix in empt_dict:
                            empt_dict[empt_pix] += 1
                        else:
                            empt_dict[empt_pix] = 1

            # 배경에서 고립된 작은 조각 제거
            for xy in empt_dict:
                if empt_dict[xy] >= smooth_val:
                    xy_list.append(xy)

        r_t_set = set()

        # 배경 좌표가 맵 크기를 벗어나지 않는지 확인
        for xy in xy_list:
            xy: tuple

            if sx <= xy[0]:
                xy = (xy[0] - sx, xy[1])

            if sy <= xy[1]:
                xy = (xy[0], xy[1] - sy)

            if -sx <= xy[0] < 0:
                xy = (xy[0] + sx, xy[1])

            if -sy <= xy[1] < 0:
                xy = (xy[0], xy[1] + sy)

            r_t_set.add(xy)

        return list(r_t_set)

    def map_view(self):
        """
        Map의 겉모습 출력
        """

        mi = self.map_index
        mb = self.map_border

        # 맵의 겉모습
        mv = ""

        for y in mb[1]:
            for x in mb[0]:
                mv += mi[(x, y)]["Shape"]
            mv += "\n"

        print(mv)

    def map_update(self, xy, tileObj):
        """
        :xy: (x, y)에 대해 tileObj를 업데이트
        """

        self.map_index[xy].update(tileObj)
        return self.map_index
    
    def map_read(self):
        """
        map_index를 JSON파일에서 읽기
        """
        
        try:
            self.map_index = JSONUtils.load(self.dump_path)
            return True
        except:
            return False

    def map_write(self):
        """
        map_index를 JSON파일로 쓰기
        """
        
        try:
            JSONUtils.write(self.dump_path, self.map_index)
            return True
        except:
            return False

    def obj_add(self, obj, xy=None):
        """
        :param obj: obj를 map_index에 추가하기
        :param xy: (x, y)가 있다면, 그에 해당하는 타일에 obj를 추가함
        """

        placs = self.map_index[xy or obj.location]["Players"]

        if obj.owner not in placs:
            placs[obj.owner] = dict()

        placs[obj.owner]["Entity"].update({
            obj.uuid: obj.profile
        })
    
    def obj_del(self, obj):
        """
        obj를 map_index에서 삭제하기
        """

        del self.map_index[obj.location]["Players"][obj.owner]["Entity"][obj.uuid]

    def obj_mov(self, obj, xy):
        """
        obj를 xy: (x, y)로 옮기기
        """

        self.obj_del(obj)
        self.obj_add(obj, xy)
        obj.location = xy
       
    def get_owner(self, xy):
        """
        :xy: (x, y)에 해당하는 타일의 소유자를 반환함
        """

        return self.map_index[xy]["Owner"]
    
    def get_entity(self, xy, owner=None):
        """
        :xy: (x, y)에 해당하는 타일의 개체들을 반환함
        :owner: 이 있을 경우, owner의 개체들만 반환함
        """

        if owner:
            return self.map_index[xy]["Players"][owner]
        else:
            return self.map_index[xy]["Players"]
    
    def get_building(self, xy, owner):
        """
        :xy: (x, y)에 해당하는 타일에서 owner의 건물을 반환함
        """

        return self.map_index[xy]["Players"][owner]["Building"]
    
    def get_ship(self, xy, owner):
        """
        :xy: (x, y)에 해당하는 타일에서 owner의 함선을 반환함
        """

        return self.map_index[xy]["Players"][owner]["Ship"]
    
    def get_type(self, xy):
        """
        :xy: (x, y)에 해당하는 타일의 타입을 반환함
        """

        return self.map_index[xy]["Type"]

    def get_shape(self, xy):
        """
        :xy: (x, y)에 해당하는 타일의 모양을 반환함
        """

        return self.map_index[xy]["Shape"]

    def get_resource(self, xy):
        """
        :xy: (x, y)에 해당하는 타일의 자원을 반환함
        """

        return self.map_index[xy]["Resource"]
    
    def replace_owner(self, xy, new_owner):
        """
        :xy: (x, y)에 해당하는 타일의 소유자를 변경함
        """

        self.map_index[xy]["Owner"] = new_owner



class Tile(Map):
    _map: Union[dict, list] = None

    def __init__(self, x: int, y: int) -> None: 
        super().__init__()
        self.x: int = x
        self.y: int = y

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
        return self.getInfo()["Owner"]

    def getUnits(self) -> dict:
        # FIXME: getInfo()["Entity"]
        return { 
            "Home": self.getInfo()["Entity"],
            "Away": self.getInfo()["Entity"]
        }

    def getBuildings(self) -> dict:
        # FIXME: getInfo()["Entity"]
        return self.getInfo()["Entity"]["Building"]

    def getResourceInfo(self) -> dict:
        return self.getInfo()["Resources"]

    def replaceOwner(self) -> None:
        tmpData = self.getInfo()
        players: list = tmpData["Players"].keys()
        players.remove(tmpData["Owner"])
        tmpData["Owner"] = players[0]
        self._updateMap(tmpData)

    def deployUnits(self) -> None:
        pass
    
    def buildBuildings(self, buildingName: str) -> None:
        mapData: dict = self.getInfo()
        mapData["Players"][mapData["Owner"]]["Entity"].update({
            
        })