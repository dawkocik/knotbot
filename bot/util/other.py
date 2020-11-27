from typing import Union, List

from discord.abc import User
from discord.ext.commands import Context


def get_mentions(ctx: Context, count: int = 0) -> Union[List[User], User, None]:
    if ctx.args is None:
        return None

    users = []

    if count == 0:
        if ctx.message.mentions is not None:
            return ctx.message.mentions
        for arg in ctx.args:
            try:
                user = ctx.bot.get_user(int(arg))
                if user is not None:
                    users.append(user)
                    continue
            except ValueError:
                pass

            got_a_user = False
            for member in ctx.guild.members:
                if arg.lower() == member.name.lower():
                    users.append(member)
                    got_a_user = True
                    break

            if not got_a_user:
                return None
