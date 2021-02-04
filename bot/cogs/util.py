from discord import Member
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

    # KotLis server
    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.guild.id == 709776102909935687:
            roles = {
                272335468698271744: [799639500137562143, 783755035825799198, 784079516926476348],  # peridot
                752468099751739392: [783755035825799198],  # ola
                734111281467883571: [783755035825799198, 792087581911285791, 785153543039746048],  # yaya
                243495771662581760: [783755035825799198, 785142345859203123, 785153543039746048],  # mydeo
                414766902246637570: [784079516926476348, 783755035825799198],  # blank
                337854110244012033: [783755035825799198, 783758215741571141],  # crystal
                239114767690629120: [775872404856635422, 783755035825799198, 784052330739138570],  # dawidek
                562216488082341888: [783755035825799198, 785153543039746048],  # natix
                253929382073073665: [783755035825799198, 783758799256813568],  # wilczu
                256911236761911297: [783755035825799198, 783755336392900628],  # kime
                256910661706055690: [801212504121802803],  # maks
                387206154931142656: [775872404856635422, 784052330739138570]  # lory
            }
            for role_id in roles.get(member.id):
                await member.add_roles(member.guild.get_role(role_id))


def setup(bot: Knotbot) -> None:
    bot.add_cog(Util(bot))
