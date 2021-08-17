import discord
from discord.ext import commands
from discord.ext.commands import Context

import pathlib
import sys

sys.path.append(pathlib.Path(__file__.replace("Modules/Main.py", "Utils")))

modules = [
    "Main",
    "Bot"
]

client = commands.Bot(
    command_prefix='!',
    owner_ids=[
        703196906700144752,  # filepile#2856
        434549321216688128,  # 샤프#8720
        480977114980417538,  # 잠ㅅ갊#3497
        258851710028480512  # deliqui#0406
    ],
    # intents=discord.flags.Intents.all()
)

path = pathlib.Path(__file__).parent.parent  # "../" 또는 ".." 사용시 경로 찾을 수 없음


class Core(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command(name="load")
    @commands.is_owner()
    async def load(self, ctx: Context, ext: str):
        try:
            self.client.load_extension(ext)
            await ctx.send("Loaded")
        except Exception as E:
            await ctx.send(E)

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: Context, ext: str):
        try:
            self.client.reload_extension(ext)
            await ctx.send("Reloaded")
        except Exception as E:
            await ctx.send(E)

    @commands.command(name="unload")
    @commands.is_owner()
    async def unload(self, ctx: Context, ext: str):
        try:
            self.client.unload_extension(ext)
            await ctx.send("Unload")
        except Exception as E:
            await ctx.send(E)

    @commands.command(name="ping")
    async def ping(self, ctx):
        return await ctx.send("pong!")


def setup(client: commands.Bot):
    client.add_cog(Core(client))


if __name__ == "__main__":
    try:
        for module in modules:
            client.load_extension(module)
            print(f"Module {module} has been loaded")
        print("------------------------------")

        with open(f"{path}/Data/Token/Token.txt") as TF:
            TOKEN = TF.read()
            client.run(TOKEN)
    except discord.errors.LoginFailure:
        print("Token was invalid. try again")
    except Exception as E:
        print(E)
