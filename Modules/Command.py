class Command:
    """
    명령어 클래스
    """

    def __init__(self):
        pass


class GameCommand(Command):
    """
    게임 시스템 명령어 클래스
    """

    def __init__(self):
        super().__init__()
        pass

    def start_game(self):
        """
        게임 시작
        """
        pass

    def end_game(self):
        """
        게임 종료
        """
        pass

    def start_turn(self):
        """
        턴 시작
        """
        pass

    def end_trun(self):
        """
        턴 종료
        """
        pass


class EntityCommand(Command):
    """
    개체 조작 명령어 클래스
    """

    def __init__(self):
        super().__init__()
        pass

    def create(self):
        """
        개체 생성
        """
        pass

    def deploy(self):
        """
        개체 배치
        """
        pass

    def move(self):
        """
        개체 위치 이동
        """
        pass

    def delete(self):
        """
        개체 삭제
        """
        pass

    def group(self):
        """
        개체 그룹화 / 해체
        """
        pass


class BuildingCommand(EntityCommand):
    """
    건물 명령어 클래스
    """

    def __init__(self):
        super().__init__()

    def produce(self):
        """
        유닛 생산 (생산용 건물에서)
        """
        pass

    def store(self):
        """
        유닛 저장 (저장용 건물에서)
        """
        pass


class ShipCommand(EntityCommand):
    """
    함선 명령어 클래스
    """

    def __init__(self):
        super().__init__()

    def advance(self):
        """
        진격하기
        """
        pass

    def attack(self):
        """
        공격하기
        """
        pass

    def defence(self):
        """
        방어하기
        """
        pass

    def explore(self):
        """
        탐색하기
        """
        pass




