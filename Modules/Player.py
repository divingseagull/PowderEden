from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed


class Player(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command(name="턴종료", aliases=["끝내기"])
    async def endTurn(self, ctx: Context):
        pass

    @commands.group(name="유닛")
    async def unit(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                embed=Embed(
                    title="오류",
                    description="명령을 입력해주세요",
                    color=0xFF0000
                )
            )

    @unit.command(name="이동")
    async def moveUnit(self, ctx: Context):
        pass

    @unit.command(name="생산")
    async def productUnit(self, ctx: Context):
        pass


def setup(client):
    client.add_cog(Player(client))
