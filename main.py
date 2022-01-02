from discord import (utils,
                     errors)
import aiohttp
from os import (system,
                _exit,
                name)
from discord.ext import commands
from pyfiglet import figlet_format
from asgiref.sync import async_to_sync
from aioconsole.stream import (ainput,
                               aprint)
from json import (load,
                  dump)
# pip install asgiref


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


clear()
print(figlet_format("Discord-CLI", font="big"),
      figlet_format("Version 1.0.0"), figlet_format("by aylonnn and PosReady"))


bot = commands.Bot(command_prefix=".",
                   self_bot=True)

current_chat = None


@bot.event
async def on_connect():
    print("\nDiscord CLI has been started!")
    await show_profile()
    await start()


@bot.event
async def on_message(message):
    if message.content:
        if message.channel == current_chat and message.author is not bot.user:
            replymsg = None
            try:
                replymsg = await message.channel.fetch_message(
                    message.reference.message_id)
            except:
                pass
            if replymsg is not None:
                print(message.author.name, ": ", "отвечает на сообщение:",
                      replymsg.content + "\n", message.content)
            else:
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
    print('''
        *****************************************
        *        Список комманд                 *
        *                                       *
        * 1. friends - список друзей            *
        *                                       *
        * 2. listenchat - чат с другом          *
        *                                       *
        * 3. server - присоединиться к серверу  *
        *                                       *
        *****************************************
        ''')
    cmd = input(">> ")
    while cmd != "exit":
        if cmd == "friends":
            for user in bot.user.friends:
                print(user.name+"#"+user.discriminator + "\n")
            cmd = input(">> ")
        if cmd == "sendmsg":
            name = input("Name: ")
            user = utils.get(bot.user.friends, name=name)
            if user is not None:
                msg = input("Сообщение: ")
                await user.send(msg)
            else:
                print("error")
            cmd = input(">> ")
        if cmd == "listenchat":
            friends = []
            for user in bot.user.friends:
                friends.append(user.name)
            for friend in friends:
                print(f"{friends.index(friend)}. {friend}\n")
            print("exit - выход")
            name = input("Выбор: ")
            if name == "exit":
                cmd = input(">> ")
                continue
            global current_chat
            try:
                current_chat = utils.get(
                    bot.user.friends, name=friends[int(name)])
                current_chat = current_chat.dm_channel
            except:
                print("Ошибка!")
                await start()
            try:
                msgs = await current_chat.history(limit=None).flatten()
                msgs.reverse()
            except:
                msgs = await current_chat.history(limit=100).flatten()
                msgs.reverse()
            clear()
            for message in msgs:
                replymsg = None
                try:
                    replymsg = await message.channel.fetch_message(
                        message.reference.message_id)
                except:
                    pass
                if replymsg is not None:
                    print(message.author.name, ": ", "отвечает на сообщение:",
                    replymsg.content + "\n", message.content)
                else:
                    print(message.author.name, ": ", message.content)
                
            await restart_console(friends[int(name)])
            break
        if cmd == "server":
            servers = []
            for server in bot.guilds:
                servers.append(server.name)
            for server in servers:
                print(f"{servers.index(server)}. {server}\n")
            print("exit - выход")
            name = input("Выбор: ")
            if name == "exit":
                cmd = input(">> ")
                continue
            await server_connect(servers[int(name)])
            break
    _exit(0)

async def editmsg():
    clientmsgs = []
    history = await current_chat.history(limit=None).flatten()
    history.reverse()
    for message in history:
        if message.author is bot.user:
            clientmsgs.append(message)
    for message in clientmsgs:
        print(f"{clientmsgs.index(message)}. {message.content}\n")
    print("exit - выход")
    msg = int(input("Выбор: "))
    try:
        content = input("Содержание: ")
        await clientmsgs[msg].edit(content=content)
    except:
        pass

async def replymsg():
    history = await current_chat.history(limit=None).flatten()
    history.reverse()
    for message in history:
        print(f"{history.index(message)}. {message.content}\n")
    print("exit - выход")
    msg = int(input("Выбор: "))
    try:
        content = input("Содержание: ")
        await history[msg].reply(content=content)
    except:
        pass


async def restart_console(chat):
    sendmsg = ""
    while True:
        if sendmsg != "":
            if sendmsg == "leave":
                await start()
                global current_chat
                current_chat = None
                break

            elif sendmsg == "editmsg":
                await editmsg()
            elif sendmsg == "replymsg":
                await replymsg()
            else:  
                user = utils.get(bot.user.friends, name=chat)
                if user is not None:
                    await user.send(sendmsg)
                sendmsg = ""
        sendmsg = await ainput(f"{bot.user.name}: ")


async def server_chat_connect(chat, server):
    sendmsg = ""
    while True:
        if sendmsg != "":
            if sendmsg == "leave":
                await start()
                global current_chat
                current_chat = None
                break
            elif sendmsg == "editmsg":
                await editmsg()
            elif sendmsg == "replymsg":
                await replymsg()
            else:
                user = utils.get(server.text_channels, name=chat)
                if user is not None:
                    await user.send(sendmsg)
            
        sendmsg = await ainput(f"{bot.user.name}: ")


async def server_connect(server):
    global current_chat
    server_discord = utils.get(bot.guilds, name=server)
    channels = []
    for channel in server_discord.text_channels:
        channels.append(channel.name)
    for channel in channels:
        print(f"{channels.index(channel)}. {channel}\n")
    print("exit - выход")
    name = input("Выбор: ")
    if name == "exit":
        await start()
    current_chat = utils.get(
        server_discord.text_channels, name=channels[int(name)])
    msgs = await current_chat.history(limit=100).flatten()
    msgs.reverse()
    clear()
    for message in msgs:
        replymsg = None
        try:
            replymsg = await message.channel.fetch_message(
                        message.reference.message_id)
        except:
            pass
        if replymsg is not None:
            print(message.author.name, ": ", "отвечает на сообщение:",
                    replymsg.content + "\n", message.content)
        else:
            print(message.author.name, ": ", message.content)

    await server_chat_connect(channels[int(name)], server_discord)


def start_t(token):
    try:
        bot.run(token)
    except errors.LoginFailure:
        print(f"Ошибка!")


with open("config.json", "r") as json_file:
    file = load(json_file)
    if file["token"] == "":
        token = input("\nВведите токен аккаунта: ")
        data = {"token": token}
        jsonf = open("config.json", "w")
        dump(data, jsonf)
        start_t(token)
    else:
        token = file["token"]
        start_t(token)
