import discord
from discord.ext import commands
import random
import subprocess
import os
import time
import json
import psutil
from functools import lru_cache


# -*- coding: utf-8 -*-
time.sleep(8)
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
with open("../secret.txt") as f:
    passwd = f.read()
TOKEN = passwd

@client.event
async def on_ready():
    print("起動")

def roll(arr):
    a = int(arr[0])
    b = int(arr[1])
    ret = []
    for _ in range(a):
        ret.append(random.randint(1,b))
    num = sum(ret)
    for i in range(a):
        ret[i] = str(ret[i])
    if a<=20 and b<=20:
        try:
            Per = P(a,b,num)
        except:
            Per = -1
    else:
        Per = -1
    return ret, num, Per

@lru_cache(maxsize=1000)
def P(a,b,num):
    # b面サイコロをa回振って合計numになる確率
    ret = 0
    if a>0:
        for x in range(1,b+1):
            ret += (1/b) * P(a-1,b,num-x)
    elif a==0 and num==0:
        ret = 1
    else:
        ret = 0
    return ret

@client.event
async def on_message(message):
    if not message.author.bot:
        args = message.content.split()
        print(message.content)
        if len(args)>0:
            if (args[0] == 'roll' or args[0] == '-roll') and len(args) == 2:
                tar = args[1].split('d')
                if len(tar) == 2:
                    ret, num, per = roll(tar)
                    if len(ret) == 1:
                        ans = f"**{tar[0]}d{tar[1]}** ！\n**" + str(num) + "**"
                    else:
                        ans = f"**{tar[0]}d{tar[1]}** ！\n" + ", ".join(ret) + "\n**" + str(num) + "**"
                    ans += f"\t/{int(tar[0])*int(tar[1])}" 
                    if per != -1:
                        ans += "  ({:>2d} %)".format(int((per*100)//1))
                    print(ans)
                    await message.channel.send(ans)

            elif (args[0] == 'roll' or args[0] == '-roll') and len(args) == 4:
                if args[2] == 'd':
                    ret,num,per = roll([int(args[1]), int(args[3])])
                    if len(ret) == 1:
                        ans = f"**{args[1]}d{args[3]}** ！\n**" + str(num) + "**"
                    else:
                        ans = f"**{args[1]}d{args[3]}** ！\n" + ", ".join(ret) + "\n**" + str(num) + "**"
                    ans += f"\t/{int(args[1])*int(args[3])}" 
                    if per != -1:
                        ans += "  ({:>2d} %)".format(int((per*100)//1))
                    print(ans)
                    await message.channel.send(ans)

            if args[0] == 'generateimage':
                print(args)
                if len(args) >= 2:
                    if args[-1] == 'debug':
                        await message.channel.send(args)
                    
                    with open('C:/mine/timer.json') as f:
                        data = json.load(f)

                    mem = psutil.virtual_memory()
                    # if mem.available < 7000000000:
                    #     await message.channel.send("メモリが少ないから時間かかるよ……")
                    if data['working']:
                        await message.channel.send("生成中……ちょっと待ってね")

                        with open('C:/mine/timer.json', 'w') as f:
                            json.dump({"working":True}, f)

                        queries = []
                        queries.append("cd C:/AI/stable-diffusion-main")
                        queries.append("C:/Users/user/anaconda3/Scripts/activate")
                        queries.append("conda activate ldm")
                        queries.append('python optimizedSD/optimized_txt2img.py --prompt "' + ' '.join(args[1:]) + f'" --H 512 --W 512 --seed {random.randrange(10000)} --n_iter 1 --n_samples 3 --ddim_steps 50')

                        subprocess.run("&& ".join(queries),shell=True)
                        print("生成完了")

                        DIR = "C:/AI/stable-diffusion-main/outputs/txt2img-samples/"+ "_".join(args[1:])
                        if len("_".join(args[1:]))>len("Medium_shot,_alone,_an_anime_girl,_Otaku,_Daisuki,_Senpai,_Kawaii,_hq,_wallpaper,_style_of_Moe,_VTuber,_Manga,_character_introduction,_sharp_eyes,_best_scene,_import,_official,_capture,_winning_works,_winning_creative,_best_illustr"):
                            DIR = DIR[:len("C:/AI/stable-diffusion-main/outputs/txt2img-samples/Medium_shot,_alone,_an_anime_girl,_Otaku,_Daisuki,_Senpai,_Kawaii,_hq,_wallpaper,_style_of_Moe,_VTuber,_Manga,_character_introduction,_sharp_eyes,_best_scene,_import,_official,_capture,_winning_works,_winning_creative,_best_illustr")]
                        number = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))

                        await message.channel.send("> " + message.content[14:])

                        files = []
                        for index in range(3):
                            files.append(discord.File(DIR + f"/0000{number-3+index}.png"))
                        await message.channel.send(files=files)
                    elif not data['working']:
                        await message.channel.send("ひとやすみ中だよ")

                else:
                    await message.channel.send("> generate [文章]")
                    
            if args[0] == 'catimage':
                if len(args) >= 2:
                    files = []
                    DIR = "C:/AI/stable-diffusion-main/outputs/txt2img-samples/"+ "_".join(args[1:])
                    number = sum(os.path.isfile(os.path.join(DIR, name)) for name in os.listdir(DIR))
                    for index in range(3):
                        files.append(discord.File(DIR + f"/0000{number-3+index}.png"))
                    await message.channel.send(files=files)
            if args[0] == 'stopimage':
                with open('C:/mine/timer.json', 'w') as f:
                    json.dump({"working":False}, f)
                await message.channel.send("動作停止！")
            if args[0] == 'startimage':
                with open('C:/mine/timer.json', 'w') as f:
                    json.dump({"working":True}, f)
                await message.channel.send("動作開始！")

                    


            # channel = client.get_channel(CHANNELID)
            # await channel.send(message.content)
            # print(message.content)

client.run(TOKEN)