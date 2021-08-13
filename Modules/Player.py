from discord.ext import commands
from discord.ext.commands import Context

class Player(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command(name="이동")
    async def move(self, ctx: Context):
        pass


def setup(client):
    client.add_cog(Player(client))