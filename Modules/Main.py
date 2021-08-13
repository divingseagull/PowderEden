import discord
from discord.ext import commands
import pathlib
import sys

sys.path.append(pathlib.Path(__file__.replace("Modules/Main.py", "Utils")))

modules = [
    "Main",
    "Bot"
]

client = commands.Bot(
    command_prefix='!',
    owner_id=[
        703196906700144752, # filepile#2856
        434549321216688128, # 샤프#8720
        480977114980417538, # 잠ㅅ갊#3497
        258851710028480512  # deliqui#0406
    ],
    # intents=discord.flags.Intents.all()
)

path = "../"

class Core(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

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