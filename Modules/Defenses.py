from discord.ext import commands
import json

def build(buildingType, tier):
    pass

class Defenses(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

def setup(client):
    client.add_cog(Defenses(client))
