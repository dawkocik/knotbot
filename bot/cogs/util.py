from discord.ext.commands import Cog, Bot, command, Context

from bot.knotbot import Knotbot
from bot.util.other import get_mentions


class Util(Cog):
    def __init__(self, bot: Knotbot) -> None:
        self.bot = bot

    @command(name='avatar')
    async def avatar(self, ctx: Context, arg1):
        mentions = get_mentions(ctx, arg1, 1)
        print(len(mentions))
        if mentions is None or len(mentions) is not 1:
            await ctx.send("wesh mentionne 1 personne")
            return
        await ctx.send(mentions[0].avatar_url)


def setup(bot: Bot) -> None:
    bot.add_cog(Util(bot))
