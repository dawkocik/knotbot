import os
import time
from datetime import datetime

import discord
import matplotlib.pyplot as plt
from discord.ext import tasks
from discord.ext.commands import Cog, Bot, command, Context

fig = plt.figure()
ax = plt.axes()


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
        self.global_messages[239114767690629120] = [
            Message(1606346340, 239114767690629120, 6),
            Message(1606347340, 239114767690629120, 2),
            Message(1606348340, 239114767690629120, 3),
            Message(1606349340, 239114767690629120, 13),
            Message(1606350340, 239114767690629120, 1),
            Message(1606351340, 239114767690629120, 5),
            Message(1606352340, 239114767690629120, 7),
        ]

    @command(name="stats")
    async def stats(self, ctx: Context) -> None:
        messages = self.global_messages[ctx.author.id]
        #  sorted(messages, key=cmp_to_key(compare_messages))

        x = range(0, len(messages))
        y = []
        for message in messages:
            y.append(message.count)
        ax.set(xlabel="time", ylabel="messages")
        labels = []
        for message in messages:
            labels.append(datetime.fromtimestamp(message.timestamp).strftime("%H:%M:%S"))
        ax.set_title(f"{ctx.author.name}'s statistics", color="w")
        ax.plot(x, y, color="#FF66FF")
        ax.set_facecolor("#36393F")
        fig.set_facecolor("#2F3136")
        ax.xaxis.label.set_color('gray')
        ax.yaxis.label.set_color('gray')
        plt.xticks(x, labels)
        plt.subplots_adjust(bottom=0.15)

        plt.grid(color='#2F3136', linestyle='solid')
        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.tick_params(colors='gray', direction='out')
        for tick in ax.get_xticklabels():
            tick.set_color('gray')
        for tick in ax.get_yticklabels():
            tick.set_color('gray')

        await send_plot(ctx)

    # @Cog.listener()
    # async def on_message(self, msg: discord.Message):
    #     if msg.author.id not in self.temp_global_messages:
    #         self.temp_global_messages[msg.author.id] = 1
    #     else:
    #         self.temp_global_messages[msg.author.id] = self.temp_global_messages[msg.author.id] + 1

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
