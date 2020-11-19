from difflib import SequenceMatcher
from typing import List

from discord.abc import User
from discord.ext.commands import Cog, Bot, command, Context


class Fun(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="love")
    async def love(self, ctx: Context) -> None:
        mentions: List[User] = ctx.message.mentions
        if len(mentions) != 2:
            await ctx.send("{0}, you need to mention 2 people :/".format(ctx.author.mention))
            return
        x: int = mentions[0].id
        y: int = mentions[1].id
        love: int = round((100 * y / x) if (x > y) else (100 * x / y))
        await ctx.send(str(love) + "% yes")

    @command(name="howgay")
    async def howgay(self, ctx: Context) -> None:
        if len(ctx.message.mentions) != 1:
            await ctx.send("{0}, you need to mention 1 person :/".format(ctx.author.mention))
            return
        gay = 256911236761911297
        user = ctx.message.mentions[0].id
        howgay = round((100 * user / gay) if (gay > user) else (100 * gay / user))

        await ctx.send("{0} is {1}% gay".format(ctx.message.mentions[0].mention, str(howgay)))

    @command(name="howgay2")
    async def howgay2(self, ctx: Context):
        if len(ctx.message.mentions) != 1:
            await ctx.send("{0}, you need to mention 1 person :/".format(ctx.author.mention))
            return
        gay = "256911236761911297"
        user = str(ctx.message.mentions[0].id)
        howgay = round(SequenceMatcher(None, gay, user).ratio() * 100)
        await ctx.send("{0} is {1}% gay".format(ctx.message.mentions[0].mention, str(howgay)))


def setup(bot: Bot) -> None:
    bot.add_cog(Fun(bot))
