import asyncio
import discord
from discord.ext import commands
from Utills.JSONUtils import JSONUtils
import os
import json

modules = []
app = commands.Bot(command_prefix="!")

token = "TOKEN"
a = [['☐ ' for i in range(30)] for i in range(20)]
b = [['0 ' for i in range(30)] for i in range(20)]
UnitList = ['호위함','구축함','순양함','전함']
@app.command(name='배치')
async def set(ctx, Unit: str, xt:int, yt:int):
    
    
    if xt > 0 or yt > 0 and Unit in UnitList:
        
        
        

        print(xt,yt)
        x = int(xt)
        y = int(yt)
        a[x-1][y-1] = '■'
        if Unit == '호위함':
            b[x-1][y-1] = 1
            a[x-1][y-1] = 1 
            await ctx.send(f'{xt}x {yt}y에 {Unit}이(가) 배치되었습니다')
        if Unit == '구축함':
            b[x-1][y-1] = 2
            a[x-1][y-1] = 2 
            await ctx.send(f'{xt}x {yt}y에 {Unit}이(가) 배치되었습니다')
        if Unit == '순양함':
            b[x-1][y-1] = 3
            a[x-1][y-1] = 3 
            await ctx.send(f'{xt}x {yt}y에 {Unit}이(가) 배치되었습니다')
        if Unit == '전함':
            b[x-1][y-1] = 4
            a[x-1][y-1] = 4 
            await ctx.send(f'{xt}x {yt}y에 {Unit}이(가) 배치되었습니다')
        else:
            b[x-1][y-1] = 0
            a[x-1][y-1] = '☐ '
            print("fail")
            await ctx.send('올바른값을 입력하세요')
            
        
        JSONUtils.write("Data/Map.json", object=b)
        print("배치")
    else:
        x = int(xt)
        y = int(yt)
        b[x-1][y-1] = 0
        await ctx.send('올바른값을 입력하세요')
@app.command(name='이동')
async def moove(ctx, Unit:str, xm:int, ym:int, x:int, y:int):
    #await ctx.send(f'{x}x {y}y로 {Unit} 이(가) 이동되었습니다')
    if x > 0 or y > 0 and xm > 0 or ym > 0 and Unit in UnitList:
        
        
        

        print(x,y)
        print(xm,ym)
        #print(a)
        x = int(x)
        y = int(y)
        xm = int(xm)
        ym = int(ym)
        a[xm-1][ym-1] = '☐ '
        a[x-1][y-1] = '■ '
        if Unit == '호위함':
            b[x-1][y-1] = 1
            a[x-1][y-1] = 1 
            await ctx.send(f'{x}x {y}y로 {Unit} 이(가) 이동되었습니다')
        if Unit == '구축함':
            b[x-1][y-1] = 2
            a[x-1][y-1] = 2 
            await ctx.send(f'{x}x {y}y로 {Unit} 이(가) 이동되었습니다')
        if Unit == '순양함':
            b[x-1][y-1] = 3
            a[x-1][y-1] = 3 
            await ctx.send(f'{x}x {y}y로 {Unit} 이(가) 이동되었습니다')
        if Unit == '전함':
            b[x-1][y-1] = 4
            a[x-1][y-1] = 4 
            await ctx.send(f'{x}x {y}y로 {Unit} 이(가) 이동되었습니다')
        else:
            b[x-1][y-1] = 0
            a[x-1][y-1] = '☐ '
            print("fail")
            await ctx.send('올바른값을 입력하세요')
            
        
        JSONUtils.write("Data/Map.json", object=b)
        print("배치")
    else:
        x = int(x)
        y = int(y)
        b[x-1][y-1] = 0
        await ctx.send('올바른값을 입력하세요')
@app.command(name='생성')
async def create(ctx, Unit, Count):
    await ctx.send(f'{Unit}이(가) {Count}개 생성되었습니다')
    print("생성")

@app.command(name='맵')
async def map(ctx):
    print("맵")
    #await ctx.send(f'{str(a).split("], ")}')
    strmap: str = ""

    for i in a:   
        for j in i:
            strmap += str(j)
        strmap += "\n"
    await ctx.send(f'{strmap}')

@app.command(name='ㅆ')
async def fu__(ctx):
    await ctx.send('ㅂ!')
    print("ㅆ")
@app.command(name='아이디어')
async def idea(ctx):
    await ctx.send('@아이디어 !')
    print("아이디어")
@app.command(name='아이디어고갈')
async def no_idea(ctx):
    await ctx.send('@아이디어 !')
    print("아이디어")
@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("📁🎮 filegames")
    await app.change_presence(status=discord.Status.online, activity=game)

if __name__ == "__main__":
    for module in modules:
        app.load_extension(module)
        print(f"Module {module} has been loaded")
    print("------------------------------")

app.run(token)


#xt == int and yt == int and xt > 0 and yt > 0 and 
