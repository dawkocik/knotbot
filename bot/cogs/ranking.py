from discord import Message
from discord.ext.commands import Bot
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context


class Ranking(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="rank")
    async def rank(self, ctx: Context) -> None:
        await ctx.send("no siema")

    @Cog.listener()
    async def on_message(self, msg: Message):
        pass


def setup(bot: Bot):
    bot.add_cog(Ranking(bot))