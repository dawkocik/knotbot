from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from ..util.database import database_connect, get_global_elo


class Ranking(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        database_connect()

    @command(name="rank")
    async def rank(self, ctx: Context) -> None:
        await ctx.send("ur elo is {}".format(get_global_elo(ctx.author.id)))

    @Cog.listener()
    async def on_message(self, msg: Message):
        pass


class User:
    def __init__(self, id: int, elo: int, time_on_voice: int, messages_sent: int) -> None:
        self.id = id
        self.elo = elo
        self.time_on_voice = time_on_voice
        self.messages_sent = messages_sent


class ServerUser:
    pass


def setup(bot: Bot) -> None:
    bot.add_cog(Ranking(bot))