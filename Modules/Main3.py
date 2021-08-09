import asyncio
import discord
from discord.ext import commands
from Utills.JSONUtils import JSONUtils
import os
import json
modules = []
app = commands.Bot(command_prefix="!")
yt = 0
xm = 0
ym = 0
token = "ㅁㄴㅇㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹㄹ"
a = [[0 for i in range(20)] for i in range(20)]

@app.command(name='배치')
async def roll(ctx, Unit, xt, yt):
    await ctx.send(f'{xt}x {yt}y에 {Unit}이(가) 배치되었습니다')
    print(xt,yt)
    #print(a)
    x = int(xt)
    y = int(yt)
    a[x-1][y-1] = 1
    for i in range(0,20):
        for j in range(0,20):
            print(a[j][i],end= ' ')
        print()
    JSONUtils.write("discord/Data/Map.json", object=a)
@app.command(name='생성')
async def roll(ctx, Unit, Count):
    await ctx.send(f'{Unit}이(가) {Count}개 생성되었습니다')
@app.command(name='이동')
async def roll(ctx, Unit,xt,yt, xm, ym):
    await ctx.send(f'{xm}x {ym}y로 {Unit}이(가) 이동되었습니다')

    print(xm,ym)
    #print(a)
    xt = int(xt)
    yt = int(yt)
    x = int(xm)
    y = int(ym)
    a[xt-1][yt-1] = 0
    a[x-1][y-1] = 1
    for i in range(0,20):
        for j in range(0,20):
            print(a[j][i],end= ' ')
        print()

@app.command(name='맵')
async def roll(ctx):
    await ctx.send(f'{a}')


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
