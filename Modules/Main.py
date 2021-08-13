from discord.ext import commands
import discord

TOKEN = "TOKEN"

modules = [
    "Main"
]

client = commands.Bot(
    command_prefix='!',
    owner_id=[
        703196906700144752, # filepile#2856
        434549321216688128, # 샤프#8720
        480977114980417538  # 잠ㅅ갊#3497
    ],
    # intents=discord.flags.Intents.all()
)

class Core(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command(name="ping")
    async def ping(self, ctx):
        return await ctx.send("pong!")

def setup(client: commands.Bot):
    client.add_cog(Core(client))

if __name__ == "__main__":
    for module in modules:
        client.load_extension(module)
        print(f"Module {module} has been loaded")
    print("------------------------------")
    client.run(TOKEN)
