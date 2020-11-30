from discord.ext.commands import Cog, Bot, command, Context

from bot.knotbot import Knotbot
from bot.util.other import get_mentions


class Util(Cog):
    def __init__(self, bot: Knotbot) -> None:
        self.bot = bot

    @command(name='avatar')
    async def avatar(self, ctx: Context, arg1):
        mentions = get_mentions(ctx, arg1, count=1)
        if mentions is None:
            await ctx.send("You have to mention 1 person, khey")
            return
        await ctx.send(mentions[0].avatar_url)


def setup(bot: Bot) -> None:
    bot.add_cog(Util(bot))
