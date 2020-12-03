import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context

from ..util.database import get_global_user, User, database_connect, ServerUser, get_server_user, update_global_user


class Ranking(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.temp_global_messages = dict()
        self.temp_server_messages = dict()
        self.temp_global_elo = dict()
        if not database_connect(bot):
            print("An error occured while connecting to the database")
            bot.close()
        self.task.start()

    @Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.id not in self.temp_global_messages:
            self.temp_global_messages[msg.author.id] = 1
        else:
            self.temp_global_messages[msg.author.id] += 1

        if msg.author.id not in self.temp_global_elo:
            self.temp_global_elo[msg.author.id] = 0.5
        else:
            self.temp_global_elo[msg.author.id] += 0.5

    @tasks.loop(seconds=10)
    async def task(self):
        for user, message_count in self.temp_global_messages.items():
            user = get_global_user(user)
            update_global_user(user, 0, 0, user.messages_sent + message_count)

    @command(name="rank")
    async def rank(self, ctx: Context) -> None:
        user: User = get_global_user(ctx.author.id)
        server_user: ServerUser = get_server_user(ctx.guild.id, ctx.author.id)
        await ctx.send(
            f'id: {user.discord_id}, elo: {user.elo}, voice_time: {user.voice_time}, messages_sent: {user.messages_sent}')
        await ctx.send(
            f'server_id: {server_user.server_id}, {server_user.discord_id}, elo: {server_user.elo}, voice_time: {server_user.voice_time}, messages_sent: {server_user.messages_sent}')


def setup(bot: Bot) -> None:
    bot.add_cog(Ranking(bot))
