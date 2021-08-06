from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command(name="testMethod")
    async def method1(self, ctx: commands.Context):
        pass

def setup(client: commands.Bot):
    client.add_cog(Test(client))