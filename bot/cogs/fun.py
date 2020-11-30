from difflib import SequenceMatcher
from typing import List

from discord.abc import User
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


def setup(bot: Bot) -> None:
    bot.add_cog(Fun(bot))
