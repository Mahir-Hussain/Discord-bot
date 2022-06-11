import discord
from discord.ext import commands
from utils.help import MyHelpCommand

import os
from datetime import datetime

import aiohttp

async def get_prefix(bot,message):
    if message.author.id == 594551272468906003:
        prefixes = ["resolute", "r.", "R.", ""]
    else:
        prefixes = ["resolute", "r.", "R."]
    return commands.when_mentioned_or(*prefixes)(bot,message)

allowed_mentions = discord.AllowedMentions(roles=False, everyone = False,
                                           users=True, replied_user=False)
bot = commands.Bot(command_prefix=get_prefix, case_sensitive=False, 
                   intents=discord.Intents.all(), allowed_mentions=allowed_mentions, 
                   help_command = MyHelpCommand())

async def startup():
    await bot.wait_until_ready()
    """
    Waits to do this until the bot is ready
    """
    bot.session = aiohttp.ClientSession()
    bot.colour = 0XFFFFFF
    cogs = ['cogs.owner',
            'cogs.meta',
            'cogs.management',
            'cogs.fun',
            'cogs.image',
            'cogs.music',
            'cogs.misc',
            'cogs.error',
            'cogs.events',
            'jishaku']
    for cog in cogs:
        bot.load_extension(cog)
        print(f'{cog} has been loaded.')

    await bot.change_presence(activity=discord.Game(name="r.help | @Resolute"))

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

bot.loop.create_task(startup())
bot.run(os.environ["BOT_TOKEN"])