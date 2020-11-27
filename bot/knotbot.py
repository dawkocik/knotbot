import traceback

import discord
from discord import Activity, ActivityType
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, Context, CommandError

intents = discord.Intents.default()
intents.members = True
cogs = [
    "ranking",
    "fun",
    "stats",
    "util"
]


class Knotbot(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(command_prefix="kn ", intents=intents, owner_id=239114767690629120, reconnect=True,
                         case_insensitive=False)
        self.remove_command("help")
        for cog in cogs:
            self.load_extension("bot.cogs." + cog)

    async def on_ready(self) -> None:
        await self.wait_until_ready()
        await self.change_presence(activity=Activity(type=ActivityType.watching, name="kn"))
        print("I'm ready ^^")

    async def on_command_error(self, ctx: Context, exception: CommandError) -> None:
        if isinstance(exception, CommandOnCooldown):
            await ctx.send(str(exception))
        else:
            await ctx.send(f'''
sorry m8, an error occurred while executing this command:
`{str(exception)}`
please report this error to <@239114767690629120>
            '''.strip())
            tb = traceback.TracebackException.from_exception(exception)
            print(''.join(tb.format()))
