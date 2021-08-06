from discord.ext import commands
import discord

class Battle(commands.Cog):
    DAMAGE_PRIORITY = [
        "FRIGATE",
        "DESTROYER",
        "CRUISER",
        "BATTLESHIP"
    ]

    def __init__(self, client):
        self.client: commands.Bot = client

    def calculateFirePower(ships: dict) -> int:
        """
        ships 인자로 들어온 함선의 수 만큼 전투력을 모두 더하여 반환합니다\n
        아래 함선 목록 외에는 모두 무시됩니다.\n
        함선 목록 (수정 필요)
        ```json
        {
            "battleship": 0,
            "destroyer":  0,
            "cruiser":    0,
            "frigate":    0
        }
        ```
        """
        # FIXME: change 0 value to each unit's firepower point
        return (ships.battleship * 0) + \
               (ships.destroyer  * 0) + \
               (ships.cruiser    * 0) + \
               (ships.frigate    * 0)
    
    def calculateDefensePoint(ships: dict) -> int:
        """
        ships 인자로 들어온 함선의 수 만큼 방어력을 모두 더하여 반환합니다\n
        아래 함선 목록 외에는 모두 무시됩니다.\n
        함선 목록 (수정 필요)
        ```json
        {
            "battleship": 0,
            "destroyer":  0,
            "cruiser":    0,
            "frigate":    0
        }
        ```
        """
        # FIXME: change 0 value to each unit's defense point
        return (ships.battleship * 0) + \
               (ships.destroyer  * 0) + \
               (ships.cruiser    * 0) + \
               (ships.frigate    * 0)

    # A의 체력 합 - 나머지의 공격력 합 = A의 남은 체력
    # 호위함들 전체 체력보다 피해량이 더 높다면, (피해량 - 호위함 전체 체력) / (구축함 수)

def setup(client):
    client.add_cog(Battle(client))