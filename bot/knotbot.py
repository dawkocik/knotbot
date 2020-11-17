from discord.ext import commands
from discord import Activity, ActivityType
import discord
import sys


intents = discord.Intents.default()
intents.members = True


class Knotbot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="kn ", intents=intents, owner_id=239114767690629120, reconnect=True, case_insensitive=False)

    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=Activity(type=ActivityType.watching, name="kn"))
        print("I'm ready ^^")


def main():
    bot = Knotbot()
    bot.run(sys.argv[1])


if __name__ == "__main__":
    main()
