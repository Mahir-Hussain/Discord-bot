import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from utils.utils import Mongodb_logs as collection
from utils.utils import bypass_for_owner

class Management(commands.Cog, name="⚔️ Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx, limit=50):
        """
        Purge the bot's message, limit is 50
        You require `manage messages` permission.
        """
        channel = ctx.message.channel

        def is_bot(m):
            return m.author == self.bot.user

        deleted = await channel.purge(limit=limit, check=is_bot, bulk=False)
        await channel.send(f"I have deleted `{len(deleted)}` messages.", delete_after=10)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def logs(self, ctx):
        """
        Shows what log types have been activated
        """
        if await collection(mt="find_one", find=ctx.guild.id):
            embed = discord.Embed(colour=ctx.author.colour)
            embed.add_field(name='Emoji Logging', value='On')
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=ctx.author.colour)
            embed.add_field(name='Emoji Logging', value='Off')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def emoji_logging_set(self, ctx, channel: discord.TextChannel):
        """
        Start logging added emojis to messages
        Permission needed: `manage guild`.
        """
        if await collection(mt="find_one", find=ctx.guild.id):
            await ctx.send('You already have an emoji_logged channel!')
        else:
            post = {
                "_id": ctx.guild.id,
                "Author": ctx.author.id,
                "Log_type": "emoji",
                "Logging_channel": channel.id}
            await collection(mt="insert_one", find=post)

            await ctx.send(f'Set {channel.mention} to be the emoji-logged channel.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def emoji_logging_remove(self, ctx):
        """
        Remove logging added emojis to messages
        Required permissions: `manage guild`.
        """
        if ctx.guild:

            try:
                if await collection(mt="find_one", find=ctx.guild.id):
                    await collection(mt="delete_one", find=ctx.guild.id)
                    await ctx.send('I have removed emoji-logging for the channel.')

            except KeyError:
                pass

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):

        try:
            s = await collection(mt='find_one', find=reaction.message.guild.id)
            guild = s['_id']
            channel = s['Logging_channel']
            emoji = s['Log_type']
            if user.bot:
                pass
            else:
                if (reaction.message.guild.id) == guild:
                    if emoji == "emoji":

                        embed = discord.Embed(colour=0xFFFFFF)
                        embed.add_field(
                            name="Reaction removed",
                            value=f"""> Emoji content sent: {reaction.emoji} \n> Emoji author: `{user}`""")
                        embed.set_footer(
                            text="""This command is in the experimental phase any issues DM elite.""")

                        log_channel = self.bot.get_channel(channel)
                        await log_channel.send(embed=embed)
        except BaseException:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        try:
            if await collection(mt="find_one", find=guild.id):
                await collection(mt="delete_one", find=guild.id)

        except KeyError:
            pass


async def setup(bot):
    await bot.add_cog(Management(bot))
