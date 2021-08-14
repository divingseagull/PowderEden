from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed
import discord

import json
import os
import shutil

from Utils.JSONUtils import JSONUtils
from . import Main

class Game(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    def initializeGame(self, guildID: int):
        if os.path.exists(f"{Main.path}/Data/Guild/{guildID}"):
            shutil.rmtree(f"{Main.path}/Data/Guild/{guildID}", True)

        shutil.copytree(f"{Main.path}/Data/Base", f"{Main.path}/Data/Guild")
        os.rename(f"{Main.path}/Data/Guild/Base", f"{Main.path}/Data/Guild/{guildID}")    

    @commands.command(name="게임시작")
    async def startGame(self, ctx: Context, *players: discord.User):
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
            )
            self.initializeGame(guild.id)
            # with open(f"{Main.path}/Data/Guild/{guild.id}/Config.json", 'w') as configFile:
            with open(f"{Main.path}/Data/Guild/TestGuild/Config.json", 'w') as configFile:
                config: dict = {
                    "MapSize": [0, 0], # SizeX, SizeY FIXME: Map size cannot be (0, 0).
                    "Players": { }
                }
                for p in players:
                    config["Players"].update(
                        {
                            f"Player{players.index(p)}": {
                                "ID": p.id,
                                "Resources": { # FIXME
                                    "Oil": 0, 
                                    "Iron": 0,
                                    "Exot": 0
                                }
                            }
                        }
                    )
                json.dump(config, configFile, indent=4)

def setup(client):
    client.add_cog(Game(client))