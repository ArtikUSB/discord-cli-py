from discord import HypeSquadHouse
from os import system

try:
    from rich.console import Console
except:
    system("pip install rich")
    from rich.console import Console


def custom_input(c, text: str):
    console = Console()
    console.input(text, style=c)


def custom_print(c, text: str):
    console = Console()
    console.print(text, style=c)


class Edit:
    async def name(self, bot):
        """
        Arguments:
            bot - bot argument for ClientUser
        """
        a = input("Введите новое имя аккаунта\n\n>> ")
        try:
            await bot.edit(username=a)
        except:
            pass

    async def password(self, bot):
        """
        Arguments:
            bot - bot argument for ClientUser
        """
        a = input("Введите старый пароль\n\n>> ")
        b = input("Введите новый пароль\n\n>> ")
        try:
            await bot.edit(password=a, new_password=b)
        except:
            pass

    async def email(self, bot):
        """
        Arguments:
            bot - bot argument for ClientUser
        """
        a = input("Введите новый e-mail\n\n>> ")
        try:
            await bot.edit(email=a)
        except:
            pass

    async def house(self, bot):
        """
        Arguments:
            bot - bot argument for ClientUser
        """
        a = input(
            "Введите значок который хотите выбрать:\n"
            + "(bravery, brilliance, balance, off - удалить значок)"
        )
        while True:
            if a == "bravery":
                try:
                    await bot.edit(house=HypeSquadHouse.bravery)
                    break
                except Exception as e:
                    print(e)
                    break
            elif a == "brilliance":
                try:
                    await bot.edit(house=HypeSquadHouse.brilliance)
                    break
                except:
                    pass
            elif a == "balance":
                try:
                    await bot.edit(house=HypeSquadHouse.balance)
                    break
                except:
                    pass
            elif a == "off":
                try:
                    await bot.edit(house=None)
                    break
                except:
                    pass
            else:
                print("Введите еще раз")
                a = input(
                    "Введите значок который хотите выбрать:\n"
                    + "(bravery, brilliance, balance, "
                    + "off - удалить значки)"
                )
