import discord
from discord.ext import commands, tasks
from utils.help import MyHelpCommand

import random
import asyncio
import os
import aiohttp

async def get_prefix(bot,message):
    if message.author.id == 594551272468906003:
        prefixes = ["resolute", "r.", "R.", ""]
    else:
        prefixes = ["resolute", "r.", "R."]
    return commands.when_mentioned_or(*prefixes)(bot,message)

class Resolute(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone = False,
                                                   users=True, replied_user=False)

        super().__init__(command_prefix=get_prefix, case_insensitive=True, 
                        intents=discord.Intents.all(), allowed_mentions=allowed_mentions, 
                        help_command = MyHelpCommand())
        self.initial_extensions = [
            'cogs.owner',
            'cogs.meta',
            'cogs.management',
            'cogs.fun',
            'cogs.image',
            'cogs.music',
            'cogs.misc',
            'cogs.error',
            'cogs.events',
            'jishaku']

    async def setup_hook(self):
        self.background_task.start()
        for cog in self.initial_extensions:
            await self.load_extension(cog)
            print(f"{cog} has been loaded")

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=10)
    async def background_task(self):
        statuses = [
            "r. help | @resolute",
            "Resolute",
            "Watching you"
            "Beep bop"]
        await bot.change_presence(activity=discord.Game(name=random.choice(statuses)))


    async def on_ready(self):
        bot.colour = 0XFFFFFF

bot = Resolute()

async def main():
    async with aiohttp.ClientSession() as session:
        async with bot:
            bot.session = session
            os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
            os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
            os.environ["JISHAKU_HIDE"] = "True"
            await bot.start(os.environ["BOT_TOKEN"])

asyncio.run(main())