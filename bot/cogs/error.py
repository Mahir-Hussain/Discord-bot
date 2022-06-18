import asyncio
import difflib
import re

import discord
from discord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Global error handler
        """
        if isinstance(error, commands.CommandNotFound):
            if ctx.author.id == 594551272468906003 and ctx.prefix == "":
                return
            else:
                cmd_list = [
                    cmd.name for cmd in self.bot.commands if not cmd.hidden]
                failed_command = re.match(
                    rf"^({ctx.prefix})\s*(.*)",
                    ctx.message.content,
                    flags=re.IGNORECASE).group(2)
                matches = difflib.get_close_matches(failed_command, cmd_list)
                if not matches:
                    return
                reinvoke = await ctx.send(f"Command '{failed_command}' was not found. Did you mean `{matches[0]}`?")
                await reinvoke.add_reaction('<:TickSomeColour:780469518010155109>')
                await reinvoke.add_reaction('<:XSomeColour:784146174163681310>')

                def check(r, u):
                    return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and str(
                        r.emoji) in ["<:TickSomeColour:780469518010155109>", "<:XSomeColour:784146174163681310>"]

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    await reinvoke.remove_reacion()
                    return
                else:
                    if str(
                            reaction.emoji) == "<:TickSomeColour:780469518010155109>":
                        await reinvoke.delete()
                        try:
                            if matches[0] == "help":
                                await ctx.send_help()
                            else:
                                command = self.bot.get_command(matches[0])
                                if await command.can_run(ctx):
                                    await command(ctx)
                                else:
                                    await ctx.send("You do not have the correct permissions to run this command.")
                        except Exception:
                            await ctx.send("Something went wrong, you will have to invoke the command youself. You may not have permission.")
                    if str(
                            reaction.emoji) == "<:XSomeColour:784146174163681310>":
                        await reinvoke.delete()

        elif isinstance(error, commands.CheckFailure):
            return

        elif isinstance(error, commands.MaxConcurrencyReached):
            embed = discord.Embed(
                description="This commands can only be used by one user at a time.",
                colour=self.bot.colour)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(
                name="⚠️ | Command error!",
                value='```This command is reserved for the owner of the bot```')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="⚠️ | Command error!", value=f'```{error}```')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="⚠️ | Command error!", value=f'```{error}```')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="⚠️ | Command error!", value=f'```{error}```')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="⚠️ | Command error!", value=f'```{error}```')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="⚠️ | Command error!", value=f'```{error}```')
            await ctx.send(embed=embed)

        elif ctx.author.id == 594551272468906003:
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="⚠️ | Command error!", value=f'```{error}```')
            embed.set_footer(
                text=f'Guild ID: {ctx.guild.id} | Did not send to error channel as you own me :c',
                icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="⚠️ | Command error! This has been sent to my owner.", value=f'```{error}```')
            embed.add_field(
                name='Author:',
                value=f'> `{ctx.author}`',
                inline=False)
            embed.add_field(
                name='Invoked command:',
                value=f'> `{ctx.command.name}`',
                inline=False)
            embed.add_field(
                name='Server:',
                value=f'> `{ctx.guild.name}`',
                inline=False)
            embed.set_footer(
                text=f'Guild ID: {ctx.guild.id}',
                icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

            error_channel = self.bot.get_channel(796767809186299934)
            await error_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Error(bot))