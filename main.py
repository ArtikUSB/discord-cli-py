################################################################
################################################################
################################################################
####                      TO-DO                             ####
####  1. добавить цвет ника по роли                         ####
####  2. .....                                              ####
####                                                        ####
####                                                        ####
####                                                        ####
####                                                        ####
####                                                        ####
####                                                        ####
####                                                        ####
################################################################
################################################################
################################################################

from json import dump, load
from os import _exit, name, system

from aioconsole.stream import ainput, aprint
from discord import ChannelType, errors, utils
from discord.ext import commands
from pyfiglet import figlet_format
from rich.console import Console

from custom import Edit

# pip install asgiref


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def custom_print(c, text: str):
    console = Console()
    console.print(text, style=c)

clear()
print(figlet_format("Discord-CLI", font="big"))


bot = commands.Bot(command_prefix="", self_bot=True)
messages = []
current_chat = None
edit = Edit()


@bot.event
async def on_connect():
    custom_print(
        "#46F079",
        f"""
        *********************************
        * Discord CLI has been started! *
        *********************************""",
    )
    await show_profile()
    await start()


@bot.event
async def on_message(message):
    if message.content:
        if message.channel == current_chat and message.author is not bot.user:
            colour = message.author.name.color.to_rgb()
            replymsg = None
            try:
                replymsg = await message.channel.fetch_message(
                    message.reference.message_id
                )
                messages.append(
                    {
                        "username": message.author.name,
                        "content": message.content,
                        "replied": replymsg,
                        "color": f"rgb({colour[0]},{colour[1]},{colour[2]})",
                    }
                )
            except:
                messages.append(
                    {
                        "username": message.author.name,
                        "content": message.content,
                        "replied": None,
                        "color": f"rgb({colour[0]},{colour[1]},{colour[2]})", # ставить ли виндаус 11? можно
                    }
                )
            if replymsg is not None:
                custom_print(colour, f"{message.author.name} : отвечает на сообщение: {replymsg.content}\n {message.content}")
            else:
                # ты чо наделол
                custom_print(colour, f"{message.author.name} : {message.content}")

            await bot.wait_until_ready()


async def show_profile():
    tag = bot.user.name + "#" + bot.user.discriminator
    avatar = bot.user.avatar_url
    userid = bot.user.id

    custom_print(
        "rgb(237,189,14)",
        f"""
        *****************************
        *        Ваш профиль        *
        *  Никнейм: {tag}    *
        *  Аватарка: {avatar} *
        *  Айди: {userid} *
        *  Друзей: {len(bot.user.friends)}               *
        *  Серверов: {len(bot.guilds)}             *
        *****************************
        """,
    )


async def start():
    custom_print(
        "rgb(237,189,14)",
        """
        ******************************************
        *        Список комманд                  *
        *                                        *
        *  friends - список друзей               *
        *                                        *
        *  listenchat - чат с другом             *
        *                                        *
        *  server - написать на сервере          *
        *                                        *
        *  change - изменить что-то в аккаунте   *
        *                                        *
        *  guild - написать в групповом чате     *
        ******************************************
        """,
    )
    cmd = input(">> ")
    while cmd != "exit":
        if cmd == "friends":
            custom_print("rgb(237,189,14)", "********************************")
            for user in bot.user.friends:
                colour = user.color.to_rgb()
                custom_print(
                    f"rgb({colour[0]},{colour[1]},{colour[2]})",
                    "* " + user.name + "#" + user.discriminator + " *",
                )
            custom_print("rgb(237,189,14)", "********************************")
            await start()
        elif cmd == "sendmsg":
            name = input(
                """
                ********************
                * Введите имя ниже *
                ********************\n>> 
                """,
            )
            user = utils.get(bot.user.friends, name=name)
            if user is not None:
                msg = input(
                    """
                    ***************************
                    * Введите сообщение ниже *
                    ***************************\n>> """,
                )
                await user.send(msg)
            else:
                print("error")
            await start()
        elif cmd == "listenchat":
            friends = []
            for user in bot.user.friends:
                friends.append(user.name)
            for friend in friends:
                print(f"{friends.index(friend)}. {friend}\n")
            print("exit - выход")
            name = input(
                """
                ******************************
                * Выберите лс с другом ниже *"
                ******************************\n>> """,
            )
            if name == "exit":
                custom_print(
                    "rgb(237,189,14)",
                    """
        ******************************************
        *        Список комманд                  *
        *                                        *
        *  friends - список друзей               *
        *                                        *
        *  listenchat - чат с другом             *
        *                                        *
        *  server - написать на сервере          *
        *                                        *
        *  change - изменить что-то в аккаунте   *
        *                                        *
        *  guild - написать в групповом чате     *
        ******************************************
        """,
                )
                cmd = input(">> ")
                continue
            global current_chat
            try:
                current_chat = utils.get(bot.user.friends, name=friends[int(name)])
                current_chat = current_chat.dm_channel
            except:
                custom_print(
                    "rgb(237,189,14)",
                    """
                    ***********
                    * Ошибка! *
                    ***********""",
                )
                await start()
            try:
                msgs = await current_chat.history(limit=None).flatten()
                msgs.reverse()
            except:
                msgs = await current_chat.history(limit=100).flatten()
                msgs.reverse()
            for message in msgs:
                try:
                    colour = message.author.color.to_rgb()
                    replymsg = await message.channel.fetch_message(
                        message.reference.message_id
                    )
                    messages.append(
                        {
                            "username": message.author.name,
                            "content": message.content,
                            "replied": replymsg,
                            "color": f"rgb({colour[0]},{colour[1]},{colour[2]})",
                        }
                    )
                except:
                    colour = message.author.color.to_rgb()
                    messages.append(
                        {
                            "username": message.author.name,
                            "content": message.content,
                            "replied": None,
                            "color": f"rgb({colour[0]},{colour[1]},{colour[2]})",
                        }
                    )
            await restart_console(friends[int(name)])
            break
        elif cmd == "change":
            custom_print(
                "rgb(237,189,14)",
                """
        **********************************************
        *        Список комманд                      *
        *                                            *
        * 1. name - изменить имя на аккаунте         *
        *                                            *
        * 2. password - изменить пароль на аккаунте  *
        *                                            *
        * 3. hypesquad - изменить значок HypeSquad   *
        *                                            *
        * 4. email - изменить email аккаунта         * 
        **********************************************
            """,
            )
            ans = input(">> ")
            while True:
                if ans == "name":
                    await edit.name(bot.user)
                    return await start()
                elif ans == "password":
                    await edit.password(bot.user)
                    return await start()
                elif ans == "hypesquad":
                    await edit.house(bot.user)
                    return await start()
                elif ans == "email":
                    await edit.email(bot.user)
                    return await start()
                else:
                    custom_print(
                        "#F04646",
                        """
        *****************************************************************
        * Ошибка, возможно вы написали не правильно. Попробуйте еще раз *
        *****************************************************************
                        """,
                    )
                    custom_print(
                        "rgb(237,189,14)",
                        """
        **********************************************
        *        Список комманд                      *
        *                                            *
        * 1. name - изменить имя на аккаунте         *
        *                                            *
        * 2. password - изменить пароль на аккаунте  *
        *                                            *
        * 3. hypesquad - изменить значок HypeSquad   *
        *                                            *
        * 4. email - изменить email аккаунта         *
        **********************************************
            """,
                    )
                    ans = input(">> ")

        elif cmd == "server":
            servers = []
            for server in bot.guilds:
                servers.append(server.name)
            for server in servers:
                print(f"{servers.index(server)}. {server}\n")
            print("exit - выход")
            name = int(
                input(
                    """
        *******************
        * Выберите число  * 
        *******************
                    \n>> """,
                )
            )
            if name == "exit":
                await start()
                continue
            await server_connect(servers[int(name)])
            break
        elif cmd == "group":
            groups = []
            channels = bot.private_channels
            for _channel in channels:
                if bool(_channel.type == ChannelType.group):
                    groups.append(_channel.name)
            for group in groups:
                print(f"{groups.index(group)}. {group}\n")
            print("exit - выход")
            name = int(
                input(
                    """
        *******************
        * Выберите число  * 
        *******************
                    \n>> """,
                )
            )
            if name == "exit":
                await start()
            current_chat = channels[name]
            msgs = await current_chat.history(limit=100).flatten()
            msgs.reverse()
            clear()
            for message in msgs:
                colour = message.author.color.to_rgb()
                replymsg = None
                try:
                    replymsg = await message.channel.fetch_message(
                        message.reference.message_id
                    )
                except:
                    pass
                if replymsg is not None:
                    custom_print(colour, f"{message.author.name} : отвечает на сообщение: {replymsg.content}\n {message.content}")
                else:
                    custom_print(colour, f"{message.author.name} : {message.content}")
            await group_connect(channels[name].id)
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
    msg = int(
        input(
            """
        *******************
        * Выберите число  * 
        *******************
                    \n>> """,
        )
    )
    try:
        content = input(
            """
        ****************************
        * Напишите новое сообщение *
        ****************************
        """,
        )
        await clientmsgs[msg].edit(content=content)
    except:
        pass


async def replymsg():
    history = await current_chat.history(limit=None).flatten()
    history.reverse()
    for message in history:
        print(f"{history.index(message)}. {message.content}\n")
    print("exit - выход")
    msg = int(
        input(
            """
        *******************
        * Выберите число  * 
        *******************
                    \n>> """,
        )
    )
    try:
        content = input(
            """
        *******************************
        * Напишите ответ на сообщение *
        *******************************
        """,
        )
        await history[msg].reply(content=content)
    except:
        pass


async def group_connect(chat):
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
                user = utils.get(bot.private_channels, id=chat)
                if user is not None:
                    await user.send(sendmsg)
                sendmsg = ""
        sendmsg = await ainput(f"{bot.user.name}: ")


async def restart_console(chat):
    sendmsg = ""
    clear()
    for msg in messages:
        colour = msg["color"]
        replymsg = msg["replied"]
        if replymsg is not None:
            custom_print(colour, f"{msg['username']} : отвечает на сообщение: {replymsg}\n {msg['content']}")
        else:
            custom_print(colour, f"{msg['username']} : {msg['content']}")
        sendmsg = await ainput()

    while True:
        if sendmsg != "":
            if sendmsg == "leave":
                await start()
            user = utils.get(bot.user.friends, name=chat)
            if user is not None:
                await user.send(sendmsg)
            clear()
            for msg in messages:
                colour = msg["color"]
                replymsg = msg["replied"]
                if replymsg is not None:
                    custom_print(colour, f"{msg['username']} : отвечает на сообщение: {replymsg}\n {msg['content']}")
                else:
                    custom_print(colour, f"{msg['username']} : {msg['content']}")
            sendmsg = ""

        clear()
        for msg in messages:
            colour = msg["color"]
            replymsg = msg["replied"]
            if replymsg is not None:
                custom_print(colour, f"{msg['username']} : отвечает на сообщение: {replymsg.content}\n {msg['content']}")
            else:
                custom_print(colour, f"{msg['username']} : {msg['content']}")
        sendmsg = await ainput()


async def server_chat_connect(chat, server):
    sendmsg = ""
    clear()
    global messages
    for msg in messages:
        replymsg = msg["replied"]
        if replymsg is not None:
            print(
                msg["username"],
                ": ",
                "отвечает на сообщение:",
                replymsg.content + "\n",
                msg["content"],
            )
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
                    custom_print(msg["color"], f"{msg['username']} : отвечает на сообщение: {replymsg.content}\n {msg['content']}")
                else:
                    custom_print(msg["color"], f"{msg['username']} : {msg['content']}")

            sendmsg = ""

        clear()
        for msg in messages:
            replymsg = msg["replied"]
            if replymsg is not None:
                custom_print(msg['color'], f"{msg['username']} : отвечает на сообщение: {replymsg.content}\n {msg['content']}")
            else:
                custom_print(msg['color'], f"{msg['username']} : {msg['content']}")

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
    name = int(
        input(
            """
        *******************
        * Выберите число  * 
        *******************
                        \n>> """
        )
    )
    if name == "exit":
        await start()
    current_chat = utils.get(server_discord.text_channels, name=channels[int(name)])
    msgs = await current_chat.history(limit=100).flatten()
    msgs.reverse()
    for message in msgs:
        colour = message.author.color.to_rgb()
        try:
            replymsg = await message.channel.fetch_message(message.reference.message_id)
            messages.append(
                {
                    "username": message.author.name,
                    "content": message.content,
                    "replied": replymsg,
                    "color": f"rgb({colour[0]},{colour[1]},{colour[2]})"
                }
            )
        except:
            messages.append(
                {
                    "username": message.author.name,
                    "content": message.content,
                    "replied": None,
                    "color": f"rgb({colour[0]},{colour[1]},{colour[2]})"
                }
            )
    await server_chat_connect(channels[int(name)], server_discord)


async def get_user_info(user):
    user = bot.get_user(user)
    user_profile = await bot.fetch_user_profile(user.id)
    bio = user_profile.bio
    return await aprint(
        f"""
        ********************************************************************
        * Имя#тег: {user}                                              *
        * ID: {user.id}                                           *
        * Аватар: {user.avatar_url}
        *                                                                  *
        * Дефолтный аватар: {user.default_avatar_url} *
        * Биография: {bio}     *
        * Бот? {'Да' if bool(user.bot) else 'Нет'}                                                         *
        * Открыт лс с ним? {'Да' if bool(user.dm_channel) else 'Нет'}                                              *
        * Заблокирован? {'Да' if user.is_blocked() else 'Нет'}                                                *
        * Вы с ним друг? {'Да' if user.is_friend() else 'Нет'}                                                *
        ********************************************************************"""
    )


def start_t(token):
    try:
        bot.run(token)
    except errors.LoginFailure:
        print(f"Ошибка! Не валид токен")


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
