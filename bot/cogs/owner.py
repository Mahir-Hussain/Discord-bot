import discord
from discord.ext import commands

import random
import subprocess as sp

from humanize import activate


class Owner(commands.Cog, name="👑 Owner", command_attrs=dict(hidden=True)):
    """
    Commands for the owner of the bot
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
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
    async def dm(self, ctx, user: discord.Member, *, content):
        """
        DM someone
        """
        embed = discord.Embed(colour=self.bot.colour)
        embed.set_author(name=f"Sent from {ctx.author}",
                         icon_url=ctx.author.avatar)
        embed.add_field(name="Message:", value=f'{content}')
        embed.set_footer(text="Resolute |")
        await user.send(embed=embed)
        await ctx.reply(
            f'<:ADeliteTick:741313902868168715> Message sent to {user}'
        )

    @commands.command()
    async def status(self, ctx, type, *, status=None):
        """
        Change the bot status:
        Playing, listening, watching, bot, competing, streaming, reset.
        """
        if type == "playing":
            await self.bot.change_precense(acitivity=discord.Game(name=status))
        else:
            await self.bot.change_precense(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

    @commands.command()
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
    async def gleave(self, ctx, id: int):
        """
        Leave a specified Guild.
        """
        embed = discord.Embed(
            title=f'Leaving the guild.',
            colour=self.bot.colour)
        await ctx.reply(embed=embed)
        get_guild = self.bot.get_guild(id)
        await get_guild.leave()

    @commands.command()
    async def nick(self, ctx, *, name: str):
        """
        Change the nickname for the bot.
        """
        await ctx.guild.me.edit(nick=name)
        await ctx.reply(f"Changed my username to `{name}`")

    @commands.command()
    async def load(self, ctx, extension):
        """
        Load a cog
        """
        await self.bot.load_extension(f'cogs.{extension}')
        await ctx.reply(f'`{extension}`' " loaded")

    @commands.command()
    async def unload(self, ctx, extension):  # Don't unload this cog lol
        """
        Unload a cog.
        """
        await self.bot.unload_extension(f'cogs.{extension}')
        await ctx.reply(f'`{extension}`' " unloaded")

    @commands.command()
    async def reload(self, ctx, *extension):
        """
        Reload a cog.
        """
        for e in extension:
            await self.bot.unload_extension(f'cogs.{e}')
            await self.bot.load_extension(f'cogs.{e}')
            await ctx.reply(f':repeat: `{e}`' " reloaded")

    @commands.command()
    async def colour(self, ctx, new):
        """
        Change the bot's embed colour
        """
        self.bot.colour = int(new, 16)

        embed = discord.Embed(colour=self.bot.colour)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
