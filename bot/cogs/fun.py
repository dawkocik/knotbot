import asyncio
from datetime import datetime
from difflib import SequenceMatcher
from typing import List

import requests
from discord.abc import User, GuildChannel
from discord.ext import tasks
from discord.ext.commands import Cog, Bot, command, Context

from bot.util.other import get_mentions


class Fun(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="love")
    async def love(self, ctx: Context, arg1, arg2) -> None:
        mentions: List[User] = get_mentions(ctx, arg1, arg2, count=2)
        if mentions is None:
            await ctx.send(f'You have to mention 2 people, {ctx.author.name}')
            return
        x: int = mentions[0].id
        y: int = mentions[1].id
        love: int = round((100 * y / x) if (x > y) else (100 * x / y))
        await ctx.send(str(love) + "% yes")

    @command(name="howgay")
    async def howgay(self, ctx: Context, arg1) -> None:
        mentions = get_mentions(ctx, arg1, count=1)
        user = ctx.author.id if (mentions is None) else mentions[0].id
        gay = 256911236761911297
        howgay = round((100 * user / gay) if (gay > user) else (100 * gay / user))
        await ctx.send("{0} is {1}% gay".format(ctx.message.mentions[0].mention, str(howgay)))

    @command(name="howgay2")
    async def howgay2(self, ctx: Context, arg1):
        mentions = get_mentions(ctx, arg1, count=1)
        user = ctx.author.id if (mentions is None) else mentions[0].id
        gay = "256911236761911297"
        howgay = round(SequenceMatcher(None, gay, user).ratio() * 100)
        await ctx.send("{0} is {1}% gay".format(ctx.message.mentions[0].mention, str(howgay)))

    @tasks.loop(hours=24)
    async def daily_fox(self):
        resp = requests.get(url='https://randomfox.ca/floof/')
        channel: GuildChannel = self.bot.get_channel(488261604647895061)
        channel.send(url=resp.json()['image'])

    @daily_fox.before_loop
    async def before_daily_fox(self):
        now = datetime.now()
        print(f'Waiting for 12h to start the task...')
        for _ in range(60 * 60 * 24):
            if now.hour == 12:
                return
            await asyncio.sleep(1)


def setup(bot: Bot) -> None:
    bot.add_cog(Fun(bot))
