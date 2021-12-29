from discord import (utils,
                     errors)
import aiohttp
from os import (system,
                _exit,
                name)
from discord.ext import commands
from pyfiglet import figlet_format
from asgiref.sync import async_to_sync
import time
from aioconsole.stream import (ainput,
                               aprint)
import json
# pip install asgiref


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


clear()
print(figlet_format("Discord-CLI", font="big"),
      figlet_format("Version 1.0.0"), figlet_format("by aylonn and PosReady"))


bot = commands.Bot(command_prefix=".",
                   self_bot=True)
messages = []
current_chat = None


@bot.event
async def on_connect():
    print("\nDiscord CLI has been started!")
    await show_profile()
    await start()


@bot.event
async def on_message(message):
    if message.content:
        if message.channel == current_chat:
            messages.append({"username": message.author.name,
                             "content": message.content})
            print(message.author.name, ": ", message.content)
            await bot.wait_until_ready()


async def show_profile():
    tag = bot.user.name + "#" + bot.user.discriminator
    avatar = bot.user.avatar_url
    email = bot.user.email
    userid = bot.user.id
    friends = bot.user.friends

    await aprint(f"\nВаш профиль:"
                 + f"\nНикнейм: {tag}"
                 + f"\nАватарка: {avatar}"
                 + f"\nАйди: {userid}"
                 + f"\nДрузей: {len(bot.user.friends)}"
                 + f"\nСерверов: {len(bot.guilds)}")


async def start():
    cmd = input(">> ")
    while cmd != "exit":
        if cmd == "friends":
            for user in bot.user.friends:
                print(user.name+"#"+user.discriminator + "\n")
            cmd = input(">> ")
        if cmd == "sendmsg":
            name = input("Name: ")
            user = utils.get(bot.user.friends, name=name)
            if user != None:
                msg = input("Сообщение: ")
                await user.send(msg)
            else:
                print("error")
            cmd = input(">> ")
        if cmd == "listenchat":
            name = input("Name: ")
            global current_chat
            current_chat = utils.get(bot.user.friends, name=name)
            msgs = await current_chat.history(limit=None).flatten()
            msgs.reverse()
            for message in msgs:
                messages.append(
                    {"username": message.author.name,
                     "content": message.content})
            await restart_console(name)
            break
    _exit(0)


async def restart_console(chat):
    # sendmsg = ""
    sendmsg = await ainput()
    clear()
    for msg in messages:
        print(msg["username"], ": ", msg["content"])
    while True:
        if sendmsg != "":
            if sendmsg == "leave":
                await start()
            user = utils.get(bot.user.friends, name=chat)
            if user != None:
                await user.send(sendmsg)
            messages.append({"username": bot.user.name, "content": sendmsg})
            clear()
            for msg in messages:
                print(msg["username"], ": ", msg["content"])
            sendmsg = ""

        clear()
        for msg in messages:
            print(msg["username"], ": ", msg["content"])
        length = len(messages)
        sendmsg = await ainput()


def start_t(token):
    try:
        bot.run(token)
    except errors.LoginFailure:
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
        start_t(token)
