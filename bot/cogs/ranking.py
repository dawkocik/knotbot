from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from ..util.database import get_global_user, User, database_connect, ServerUser, get_server_user


class Ranking(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        if not database_connect(bot):
            print("An error occured while connecting to the database")
            bot.close()

    @command(name="rank")
    async def rank(self, ctx: Context) -> None:
        user: User = get_global_user(ctx.author.id)
        server_user: ServerUser = get_server_user(ctx.guild.id, ctx.author.id)
        await ctx.send(f'id: {user.discord_id}, elo: {user.elo}, voice_time: {user.voice_time}, messages_sent: {user.messages_sent}')
        await ctx.send(f'server_id: {server_user.server_id}, {server_user.discord_id}, elo: {server_user.elo}, voice_time: {server_user.voice_time}, messages_sent: {server_user.messages_sent}')

    @Cog.listener()
    async def on_message(self, msg: Message):
        pass


def setup(bot: Bot) -> None:
    bot.add_cog(Ranking(bot))
