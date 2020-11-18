import discord
from discord import Activity, ActivityType
from discord.ext import commands

from .util.database import create_connection

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