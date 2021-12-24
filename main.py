import discord
from discord.ext import commands
from pyfiglet import figlet_format

print(figlet_format("Discord-CLI", font="big"), figlet_format("Version 1.0.0"), figlet_format("by aylonn and PosReady"))

token = input("\nВведите токен аккаунта: ")

bot = commands.Bot(command_prefix="POSREADYLOX", self_bot = True)

@bot.event
async def on_ready():
    print("\nDiscord CLI запущен успешно!")
    show_profile()
    await start()

async def start():
    cmd = input(">> ")
    while cmd != "exit":
        if cmd == "friends":
            for user in bot.user.friends:
                print(user.name+"#"+user.discriminator+" id"+user.id)
        cmd = input(">> ")
        if cmd == "sendmsg":
            recieverid = input("ID: ")
            user = await bot.get_user(recieverid)
            if user != None:
                msg = input("Сообщение: ")
                await user.send(msg)
            cmd = input(">> ")

def show_profile():
    tag = bot.user.name + bot.user.discriminator
    avatar = bot.user.avatar_url
    email = bot.user.email
    userid = bot.user.id
    friends = bot.user.friends 

    print(f"\n\tВаш профиль:\nНикнейм: {tag}\nАватарка: {avatar}\nПочта: {email}\nАйди: {userid}")

bot.run(token, bot=False)