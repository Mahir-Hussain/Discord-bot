import discord
from discord.ext import commands

import random
import subprocess as sp

class Owner(commands.Cog, name="👑 Owner", command_attrs=dict(hidden=True)):
    """
    Commands for the owner of the bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, text):
        """
        Say any message through the bot.
        """
        await ctx.send(text)

        try:
            await ctx.message.delete()
        except Exception:
            return False

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.Member, *, content):
        """
        DM someone
        """
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=f"Sent from {ctx.author}",
                         icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message:", value=f'{content}')
        embed.set_footer(text="Resolute |")
        await user.send(embed=embed)
        await ctx.reply(
            f'<:ADeliteTick:741313902868168715> Message sent to {user}'
        )

    @commands.command()
    # Stolen from Isirk [https://github.com/isirk/Sirk/]
    @commands.is_owner()
    async def status(self, ctx, types, *, status=None):
        """
        Change the bot status:
        Playing, listening, watching, bot, competing, streaming, reset.
        """
        if types == "playing":
            await self.bot.change_presence(activity=discord.Game(name=f"{status}"))
            await ctx.reply(f'<:TickSomeColour:780469518010155109> Changed status to `Playing {status}`')
        elif types == "listening":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
            await ctx.reply(f'<:TickSomeColour:780469518010155109>  Changed status to `Listening to {status}`')
        elif types == "watching":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
            await ctx.reply(f'<:TickSomeColour:780469518010155109>  Changed status to `Watching {status}`')
        elif types == "bot":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.bot.users)} users in {len(self.bot.guilds)} servers"))
            await ctx.reply(f'<:TickSomeColour:780469518010155109> Changed status to `Watching {len(self.bot.users)} users in {len(self.bot.guilds)} servers`')
        elif types == "competing":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"{status}"))
            await ctx.reply(f'<:TickSomeColour:780469518010155109>  Changed status to `Competing in {status}`')
        elif types == "streaming":
            await self.bot.change_presence(activity=discord.Streaming(name=f"{status}", url="https://www.twitch.tv/rickroll"))
            await ctx.relpy(f'<:TickSomeColour:780469518010155109>  Changed status to `Streaming {status}`')
        elif types == "reset":
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.reply("<:TickSomeColour:780469518010155109>  Reset Status")
        else:
            await ctx.reply("Type needs to be either `playing|listening|watching|streaming|competing|bot|reset`")

    @commands.command()
    @commands.is_owner()
    async def guilds(self, ctx):
        """
        Sends the guilds the bot is in.
        """
        a = ""
        for x in self.bot.guilds:
            a = f"{x.name}, {x.id}\n"

        paste = await self.bot.mystbin_client.post(a, syntax="python")
        await ctx.send(paste)

    @commands.command()
    @commands.is_owner()
    async def get_invite(self, ctx, ids: int):
        """
        Get the invite link for a server
        """
        guild = self.bot.get_guild(ids)

        for channel in guild.text_channels:
            channels = [channel.id]

        picked = random.choice(channels)
        channel = self.bot.get_channel(picked)

        invite = await channel.create_invite(max_uses=1)

        await ctx.author.send(invite)

    @commands.command()
    @commands.is_owner()
    async def gleave(self, ctx, id: int):
        """
        Leave a specified Guild.
        """
        embed = discord.Embed(title=f'Leaving the guild.', colour=self.bot.colour)
        await ctx.reply(embed=embed)
        get_guild = self.bot.get_guild(id)
        await get_guild.leave()

    @commands.command()
    @commands.is_owner()
    async def nick(self, ctx, *, name: str):
        """
        Change the nickname for the bot.
        """
        await ctx.guild.me.edit(nick=name)
        await ctx.reply(f"Changed my username to `{name}`")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        """
        Load a cog
        """
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.reply(f'`{extension}`' " loaded")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):  # Don't unload this cog lol
        """
        Unload a cog.
        """
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.reply(f'`{extension}`' " unloaded")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *extension):
        """
        Reload a cog.
        """
        for e in extension:
            self.bot.unload_extension(f'cogs.{e}')
            self.bot.load_extension(f'cogs.{e}')
            await ctx.reply(f':repeat: `{e}`' " reloaded")
    
    @commands.command()
    @commands.is_owner()
    async def colour(self, ctx, new):
        """
        Change the bot's embed colour
        """
        self.bot.colour = int(new, 16)
        
        embed = discord.Embed(colour=self.bot.colour)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))
