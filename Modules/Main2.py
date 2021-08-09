import asyncio
import discord
from discord.ext import commands
import os

app = commands.Bot(command_prefix="!")

token = "ODczMTY2MTU5ODIwNzgzNjY2.YQ0dWw.zuqkfUW0tLiKQIdy4w0F26efOSA"
a = [[0 for i in range(20)] for i in range(20)]
for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"Cogs.{filename[:-3]}")
@app.command(name='배치')
async def roll(ctx, Unit, xt, yt):
    await ctx.send(f'{xt}x {yt}y에 {Unit}이(가) 배치되었습니다')
    print(xt,yt)
    x = int(xt)
    y = int(yt)
    a[x-1][y-1] = 1
    for i in range(0,10):
        for j in range(0,10):
            print(a[j][i],end= ' ')
        print()

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
    game = discord.Game("TEST")
    await app.change_presence(status=discord.Status.online, activity=game)


app.run(token)
