from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder


def recursiveLookup(k, d, t=None):
    """
    list 및 dict 가 여러번 중첩되어 있는 object 에서 key 및 value 의 type 을 통해 value 를 찾는 함수

    :param k: 접근하려는 항목의 key
    :param d: 검색 대상인 list 나 dict
    :param t: key 에 해당하는 value 의 type, 기본값은 None (None 일 경우 제일 상위의 일치하는 key 에 대한 value 를 반환)
    :return: key 에 해당하는 value
    """
    if k in d:
        if t is not None:
            if isinstance(d[k], t):
                return d[k]
        else:
            return d[k]

    if isinstance(d, dict):
        for v in d.values():
            if isinstance(v, list) or isinstance(v, dict):
                a = recursiveLookup(k, v, t)
                if a is not None:
                    return a

    elif isinstance(d, list):
        for e in d:
            if isinstance(e, list) or isinstance(e, dict):
                a = recursiveLookup(k, e, t)
                if a is not None:
                    return a

    return None


def calc(a, b, mode): 
    """
    mode에 따라 사칙연산된 값을 반환
    """

    def plus_cal(a, b): return a + b

    def minus_cal(a, b): return a - b

    def multipy_cal(a, b): return a * b

    def divide_cal(a, b): return a / b
    
    calcDict = {
        'plus': plus_cal,
        'minus': minus_cal,
        'multipy': multipy_cal,
        'divide': divide_cal
    }

    return calcDict[mode](a, b)


def distance(xy1, xy2):
    """
    :return: xy1, xy2간 거리를 반환함
    """

    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** (1 / 2)


def path_finding(map_instance, obstacle_type: list, start, end):
    """
    :requirements: pathfinding

    :param map_instance: Map 인스턴스
    :param obstacle_type: 장애물 타입 (예를 들어 바다 등...)
    :param start: 출발지 xy 좌표 = (x, y)
    :param end: 목적지 xy 좌표 = (x, y)
    """

    mb = map_instance.border
    mi = map_instance.map_index

    # 맵 그리드를 1로 초기화
    map_data = [[1 for col in range(mb[0])] for row in range(mb[1])]

    # 장애물 좌표에서 1을 0으로 교체
    for xy in mi:
        for obs in obstacle_type:
            if obs in mi(xy)["Type"]:
                map_data[xy[1]][xy[0]] = 0

    grid = Grid(matrix=map_data)
    finder = BiAStarFinder()
    path, runs = finder.find_path(start, end, grid)
    return path
