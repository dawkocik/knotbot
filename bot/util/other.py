from typing import Union, List

from discord.abc import User
from discord.ext.commands import Context


def get_mentions(ctx: Context, *args, count: int = 0) -> Union[List[User], User, None]:
    if args is None:
        return None

    users = []

    if count == 0:
        if len(ctx.message.mentions) > 0:
            return ctx.message.mentions
        for arg in args:
            try:
                user = ctx.bot.get_user(int(arg))
                if user is not None:
                    users.append(user)
                    continue
            except ValueError:
                pass

            got_user = False
            for member in ctx.guild.members:
                if member.name.lower().startswith(arg.lower()):
                    users.append(member)
                    got_user = True
                    break

            if not got_user:
                return None
    else:
        if len(ctx.message.mentions) >= count:
            return ctx.message.mentions[:count]

        for arg in range(count + 1):
            try:
                user = ctx.bot.get_user(int(args[arg]))
                if user is not None:
                    users.append(user)
            except ValueError:
                pass

            got_user = False
            for member in ctx.guild.members:
                if member.name.lower().startswith(args[arg].lower):
                    users.append(member)
                    got_user = True
                    break

            if not got_user:
                return None

    return users if users else None
