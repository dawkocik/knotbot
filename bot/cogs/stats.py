import asyncio
import os
import time
from datetime import datetime
from random import randrange

import discord
import matplotlib.pyplot as plt
from discord.ext import tasks
from discord.ext.commands import Cog, Bot, command, Context, cooldown, BucketType

fig = plt.figure()
ax = plt.axes()
x = range(0, 24)


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


class Stats(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.global_messages = dict()
        self.server_messages = dict()
        self.temp_global_messages = dict()
        self.temp_server_messages = dict()
        self.task.start()

        ax.set_facecolor("#36393F")
        fig.set_facecolor("#2F3136")
        ax.xaxis.label.set_color('gray')
        ax.yaxis.label.set_color('gray')
        plt.subplots_adjust(bottom=0.15)
        ax.set(xlabel="time", ylabel="messages")
        for spine in ax.spines.values():
            spine.set_visible(False)
        labels = [f'{label}h' for label in x]
        plt.xticks(x, labels, rotation=45)
        plt.grid(color='#2F3136', linestyle='solid')
        ax.tick_params(colors='gray', direction='out')

        self.global_messages[239114767690629120] = [
            Message(1606348340, 239114767690629120, randrange(800)),
            Message(1606349340, 239114767690629120, randrange(800)),
            Message(1606350340, 239114767690629120, randrange(800)),
            Message(1606351340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606352340, 239114767690629120, randrange(800)),
            Message(1606346340, 239114767690629120, randrange(800)),
            Message(1606347340, 239114767690629120, randrange(800)),
            Message(1606348340, 239114767690629120, randrange(800)),
            Message(1606349340, 239114767690629120, randrange(800)),
            Message(1606350340, 239114767690629120, randrange(800)),
            Message(1606351340, 239114767690629120, randrange(800))
        ]

    @command(name="stats")
    @cooldown(1, 10.0, BucketType.user)
    async def stats(self, ctx: Context) -> None:
        await ctx.trigger_typing()
        messages = self.global_messages[ctx.author.id]

        y = [message.count for message in messages]
        ax.plot(x, y, color="#FF66FF")
        ax.set_title(f"{ctx.author.name}'s statistics", color="w")

        await send_plot(ctx)

    # @Cog.listener()
    # async def on_message(self, msg: discord.Message):
    #     if msg.author.id not in self.temp_global_messages:
    #         self.temp_global_messages[msg.author.id] = 1
    #     else:
    #         self.temp_global_messages[msg.author.id] = self.temp_global_messages[msg.author.id] + 1

    @tasks.loop(hours=1)
    async def task(self):
        print(f"Task update on {datetime.now().strftime('%H:%M:%S')}")
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
        for _ in range(60 * 60):
            print(datetime.now().minute)
            if datetime.now().minute == 0:
                return
            await asyncio.sleep(1)

    def get_max_messages(self, user_id: int) -> int:
        maxi = 0
        for message in self.global_messages[user_id]:
            maxi = message.count if message.count > maxi else maxi
        return maxi


async def send_plot(ctx: Context):
    path = f'temp/{ctx.author.id}.png'
    if not os.path.exists("temp/"):
        os.makedirs("temp/")
    plt.savefig(path)
    await ctx.send(file=discord.File(path))
    os.remove(path)


def compare_messages(x, y):
    return x.timestamp - y.timestamp


def setup(bot: Bot) -> None:
    bot.add_cog(Stats(bot))
