from discord.ext import commands
from discord import Activity, ActivityType
from .util.database import create_connection
import discord
import sys


intents = discord.Intents.default()
intents.members = True
cogs = [
    "ranking"
]


class Knotbot(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(command_prefix="kn ", intents=intents, owner_id=239114767690629120, reconnect=True, case_insensitive=False)
        self.remove_command("help")
        for cog in cogs:
            self.load_extension("bot.cogs." + cog)
        create_connection("ranking.db")

    async def on_ready(self) -> None:
        await self.wait_until_ready()
        await self.change_presence(activity=Activity(type=ActivityType.watching, name="kn"))
        print("I'm ready ^^")


def main() -> None:
    bot = Knotbot()
    bot.run(sys.argv[1])


if __name__ == "__main__":
    main()