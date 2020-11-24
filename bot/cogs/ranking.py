import time
from datetime import datetime

from discord import Message
from discord.ext import tasks
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
        self.global_messages = dict()
        self.server_messages = {}
        self.temp_global_messages = dict()
        self.temp_server_messages = {}
        self.task.start()

    @command(name="rank")
    async def rank(self, ctx: Context) -> None:
        user: User = get_global_user(ctx.author.id)
        server_user: ServerUser = get_server_user(ctx.guild.id, ctx.author.id)
        await ctx.send(
            f'id: {user.discord_id}, elo: {user.elo}, voice_time: {user.voice_time}, messages_sent: {user.messages_sent}')
        await ctx.send(
            f'server_id: {server_user.server_id}, {server_user.discord_id}, elo: {server_user.elo}, voice_time: {server_user.voice_time}, messages_sent: {server_user.messages_sent}')

    @command(name="stats")
    async def stats(self, ctx: Context) -> None:
        pass

    @Cog.listener()
    async def on_message(self, msg: Message):
        if msg.author.id not in self.temp_global_messages:
            self.temp_global_messages[msg.author.id] = 1
        else:
            self.temp_global_messages[msg.author.id] = self.temp_global_messages[msg.author.id] + 1

    @tasks.loop(seconds=10.0)
    async def task(self):
        print("Task update")
        for user, message_count in self.temp_global_messages.items():
            if user not in self.global_messages:
                self.global_messages[user] = list()
            self.global_messages[user].append(Message(time.time(), user, message_count))
            print(f'{self.bot.get_user(user).name}: {message_count} messages')
        self.temp_global_messages.clear()
        print('-\\/- global -\\/-')
        for user, messages in self.global_messages.items():
            for message in messages:
                print(
                    f'{self.bot.get_user(user).name}: {message.count} messages on: {datetime.utcfromtimestamp(message.timestamp).strftime("%Y-%m-%d %H:%M:%S")}'
                )
        print('-/\\- global -/\\-')

    @task.before_loop
    async def before_task(self):
        print("Waiting for the bot to be ready to start the task...")
        await self.bot.wait_until_ready()


class Message:
    def __init__(self, timestamp: int, user: int, count: int):
        self.timestamp: int = timestamp
        self.user: int = user
        self.count: int = count


class ServerMessage(Message):
    def __init__(self, timestamp: int, user: int, server: int):
        self.timestamp: int = timestamp
        self.user: int = user
        self.server: int = server


def setup(bot: Bot) -> None:
    bot.add_cog(Ranking(bot))
