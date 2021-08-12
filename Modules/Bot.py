from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed
import discord

import json
import os
import shutil

from Utils.JSONUtils import JSONUtils
from . import Main

class Bot(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    def initializeGame(self, guildID: int):
        if os.path.exists(f"{Main.path}/Data/Guild/{guildID}"):
            shutil.rmtree(f"{Main.path}/Data/Guild/{guildID}", True)

        shutil.copytree(f"{Main.path}/Data/Base", f"{Main.path}/Data/Guild")
        os.rename(f"{Main.path}/Data/Guild/Base", f"{Main.path}/Data/Guild/{guildID}")    

    @commands.command(name="게임시작")
    async def startGame(self, ctx: Context, players: int, roleColor=None):
        if players < 2:
            return await ctx.send(embed=Embed(
                title="오류",
                description="게임 참가 인원은 최소 2명이어야 합니다",
                color=0xFF0000
            ))
        else:
            guild: discord.Guild = ctx.guild
            participant = guild.create_role(
                name="참가자",
                colour=roleColor,
            )
            self.initializeGame(guild.id)
            with open(f"{Main.path}/Data/{guild.id}", 'w') as configFile:
                config: dict = {
                    "MapSize": ["SizeX", "SizeY"], # FIXME: 'SizeX' and 'SizeY' is int. not str
                    "Players": []
                }
                for i in players:
                    config["Players"].append(
                        {
                            f"Player{i}": {
                                "Resources": { # FIXME
                                    "Oil": 0, 
                                    "Iron": 0,
                                    "Exot": 0
                                }
                            }
                        }
                    )
                json.dump(pass, configFile, indent=4) # FIXME: pass to another value

def setup(client):
    client.add_cog(Bot(client))