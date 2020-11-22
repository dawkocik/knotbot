from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from ..util.database import get_global_user, User, database_connect


class Ranking(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        if not database_connect(bot):
            print("An error occured while connecting to the database")
            bot.close()

    @command(name="rank")
    async def rank(self, ctx: Context) -> None:
        user: User = get_global_user(ctx.author.id)
        await ctx.send(f'id: {user.discord_id}, elo: {user.elo}, voice_time: {user.voice_time}, messages_sent: {user.messages_sent}')

    @Cog.listener()
    async def on_message(self, msg: Message):
        pass


def setup(bot: Bot) -> None:
    bot.add_cog(Ranking(bot))
