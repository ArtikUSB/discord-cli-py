import discord
import aiohttp
import os
from discord.ext import commands
from pyfiglet import figlet_format
from asgiref.sync import async_to_sync
import time
from aioconsole.stream import ainput
import json
# pip install asgiref

os.system("cls")
print(figlet_format("Discord-CLI", font="big"), figlet_format("Version 1.0.0"), figlet_format("by aylonn and PosReady"))


bot = commands.Bot(command_prefix="POSREADYANDAYLONNLOX", self_bot = True)
messages = []
current_chat = None

@bot.event
async def on_ready():
    print("\nDiscord CLI запущен успешно!")
    await show_profile()
    await start()

@bot.event
async def on_message(message):
    if message.content:
        if message.author == (bot.user.name + "#" + bot.user.discriminator) or message.author == current_chat:
            messages.append({"username": message.author.name, "content": message.content})
            print(message.author.name, ": ", message.content)
            await bot.wait_until_ready() 
        
        
async def start():
    cmd = input(">> ")
    while cmd != "exit":
        if cmd == "friends":
            for user in bot.user.friends:
                print(user.name+"#"+user.discriminator + "\n")
            cmd = input(">> ")
        if cmd == "sendmsg":
            name = input("Name: ")
            user = discord.utils.get(bot.user.friends, name=name)
            if user != None:
                msg = input("Сообщение: ")
                await user.send(msg)
            else:
                print("error")
            cmd = input(">> ")
        if cmd == "listenchat":
            name = input("Name: ")
            global current_chat
            current_chat = discord.utils.get(bot.user.friends, name=name)
            msgs = await current_chat.history(limit=None).flatten() 
            msgs.reverse()
            for message in msgs:
                messages.append({"username": message.author.name, "content": message.content})
            await restart_console(name)
            break

          
async def restart_console(chat):
    sendmsg = ""
    os.system("cls")
    for msg in messages:
            print(msg["username"], ": ", msg["content"])
    while True:
        if sendmsg != "":
            if sendmsg == "leave":
                break
            user = discord.utils.get(bot.user.friends, name=chat)
            if user != None:
                await user.send(sendmsg)
            messages.append({"username": bot.user.name, "content": sendmsg})
            os.system("cls")
            for msg in messages:
                print(msg["username"], ": ", msg["content"])
            sendmsg = ""

        os.system("cls")
        for msg in messages:
            print(msg["username"], ": ", msg["content"])
        length = len(messages)
        sendmsg = await ainput()
        

async def show_profile():
    tag = bot.user.name + "#" + bot.user.discriminator
    avatar = bot.user.avatar_url
    email = bot.user.email
    userid = bot.user.id
    friends = bot.user.friends 

    print(f"\n\tВаш профиль:\nНикнейм: {tag}\nАватарка: {avatar}\nПочта: {email}\nАйди: {userid}")

def run(token):
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        print(f"Ошибка!")

with open("config.json", "r") as json_file:
    file = json.load(json_file)
    if file["token"] == "":
        token = input("\nВведите токен аккаунта: ")
        data = {"token": token}
        jsonf = open("config.json", "w")
        json.dump(data, jsonf)
        run(token)
    else:
        token = file["token"]
        run(token)