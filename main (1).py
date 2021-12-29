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
            replymsg = None
            try:
                replymsg = await message.channel.fetch_message(
                    message.reference.message_id)
                messages.append(
                    {"username": message.author.name,
                     "content": message.content, "replied": replymsg})
            except:
                messages.append(
                    {"username": message.author.name,
                     "content": message.content, "replied": None})
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
            for message in msgs:
                try:
                    replymsg = await message.channel.fetch_message(
                        message.reference.message_id)
                    messages.append(
                        {"username": message.author.name,
                         "content": message.content, "replied": replymsg})
                except:
                    messages.append(
                        {"username": message.author.name,
                         "content": message.content, "replied": None})
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


async def restart_console(chat):
    sendmsg = ""
    clear()
    for msg in messages:
        replymsg = msg["replied"]
        if replymsg is not None:
            print(msg["username"], ": ", "отвечает на сообщение:",
                  replymsg.content + "\n", msg["content"])
        else:
            print(msg["username"], ": ", msg["content"])

    while True:
        if sendmsg != "":
            if sendmsg == "leave":
                await start()
            user = utils.get(bot.user.friends, name=chat)
            if user is not None:
                await user.send(sendmsg)
            clear()
            for msg in messages:
                replymsg = msg["replied"]
                if replymsg is not None:
                    print(msg["username"], ": ", "отвечает на сообщение:",
                          replymsg.content + "\n", msg["content"])
                else:
                    print(msg["username"], ": ", msg["content"])
            sendmsg = ""

        clear()
        for msg in messages:
            replymsg = msg["replied"]
            if replymsg is not None:
                print(msg["username"], ": ", "отвечает на сообщение:",
                      replymsg.content + "\n", msg["content"])
            else:
                print(msg["username"], ": ", msg["content"])
        length = len(messages)
        sendmsg = await ainput()


async def server_chat_connect(chat, server):
    sendmsg = ""
    clear()
    global messages
    for msg in messages:
        replymsg = msg["replied"]
        if replymsg is not None:
            print(msg["username"], ": ", "отвечает на сообщение:",
                  replymsg.content + "\n", msg["content"])
        else:
            print(msg["username"], ": ", msg["content"])
    while True:
        if sendmsg != "":
            if sendmsg == "leave":
                await start()
                global current_chat
                current_chat = None
                messages = []
                break
            user = utils.get(server.text_channels, name=chat)
            if user is not None:
                await user.send(sendmsg)
            clear()
            for msg in messages:
                replymsg = msg["replied"]
                if replymsg is not None:
                    print(msg["username"], ": ", "отвечает на сообщение:",
                          replymsg.content + "\n", msg["content"])
                else:
                    print(msg["username"], ": ", msg["content"])
            sendmsg = ""

        clear()
        for msg in messages:
            replymsg = msg["replied"]
            if replymsg is not None:
                print(msg["username"], ": ", "отвечает на сообщение:",
                      replymsg.content + "\n", msg["content"])
            else:
                print(msg["username"], ": ", msg["content"])
        length = len(messages)
        sendmsg = await ainput()


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
    for message in msgs:
        try:
            replymsg = await message.channel.fetch_message(
                message.reference.message_id)
            messages.append(
                {"username": message.author.name,
                 "content": message.content, "replied": replymsg})
        except:
            messages.append(
                {"username": message.author.name,
                 "content": message.content, "replied": None})
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
