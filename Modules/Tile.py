from discord.ext import commands
import json
import Main

def getResources():
    pass



class Tile(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
    
def setup(client):
    client.add_cog(Tile(client))