from discord.ext.commands import Cog, Bot, command, Context

from bot.knotbot import Knotbot


class Util(Cog):
    def __init__(self, bot: Knotbot) -> None:
        self.bot = bot

    @command(name='avatar')
    async def avatar(self, ctx: Context):
        if len(ctx.message.mentions) != 1:
            await ctx.send("{0}, you need to mention 1 person :/".format(ctx.author.mention))
            return
        await ctx.send(ctx.message.mentions[0].avatar_url)


def setup(bot: Bot) -> None:
    bot.add_cog(Util(bot))
