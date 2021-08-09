import asyncio
import discord
from discord.ext import commands
from Utills.JSONUtils import JSONUtils
import os
import json
modules = []
app = commands.Bot(command_prefix="!")

token = "afdsssssssssssssssssssss"
a = [[0 for i in range(20)] for i in range(20)]

@app.command(name='배치')
async def roll(ctx, Unit, xt, yt):
    await ctx.send(f'{xt}x {yt}y에 {Unit}이(가) 배치되었습니다')
    print(xt,yt)
    #print(a)
    x = int(xt)
    y = int(yt)
    a[x-1][y-1] = 1
    for i in range(0,10):
        for j in range(0,10):
            print(a[j][i],end= ' ')
        print()
    JSONUtils.write("Data/Map.json", object=a)
@app.command(name='생성')
async def roll(ctx, Unit, Count):
    await ctx.send(f'{Unit}이(가) {Count}개 생성되었습니다')
@app.command(name='이동')
async def roll(ctx, Unit, x, y):
    await ctx.send(f'{x}x {y}y로 {Unit}이(가) 이동되었습니다')

@app.command(name='생성')
async def roll(ctx, Unit, Count):
    await ctx.send(f'{Unit}이(가) {Count}개 생성되었습니다')

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game(":exploding_head:")
    await app.change_presence(status=discord.Status.online, activity=game)

if __name__ == "__main__":
    for module in modules:
        app.load_extension(module)
        print(f"Module {module} has been loaded")
    print("------------------------------")

app.run(token)