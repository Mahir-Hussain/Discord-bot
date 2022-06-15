import discord
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType

import os
import discord
import humanize

from utils.utils import Mongodb_t as cogs_t


class Misc(commands.Cog, name="🔨 Misc"):
    """
    Some random commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.auth = os.environ["TopGG"]
        self.headers = dict(Authorization=self.auth)
        self.ep = "https://top.gg/api/"
        self.updatestats.start()

    @tasks.loop(minutes=100)
    async def updatestats(self):
        """Updates the bot's guild / shard count on top.gg"""

        await self.bot.wait_until_ready()

        guilds = len(self.bot.guilds)
        shards = None
        if isinstance(self.bot, commands.AutoShardedBot):
            shards = len(self.bot.shards)

        url = "{}bots/{}/stats".format(self.ep, self.bot.user.id)

        data = dict(server_count=guilds)
        if shards:
            data['shard_count'] = shards

        response = await self.session.post(
            url=url,
            headers=self.headers,
            data=data
        )

        if response.status != 200:
            #raise Exception(
            #    "During DBL update loop received code {}: {}".format(
            #        response.status, response.reason))
            pass

    @commands.command()
    @commands.cooldown(1, 100, BucketType.user)
    async def poll(self, ctx, title, *options):
        """
        Make a poll. Up to 10 options.
        """
        reactions = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
            10: "🔟"}
        s = ""
        num = 1
        for i in options:
            s += f"{num} - {i}\n"
            num += 1
        embed = discord.Embed(title=title, description=s, colour=self.bot.colour)
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar)
        try:
            await ctx.channel.purge(limit=1)
        except BaseException:
            pass
        msg = await ctx.send(embed=embed)
        for i in range(1, len(options) + 1):
            await msg.add_reaction(reactions[i])

    @commands.command(name="steal")
    @commands.has_permissions(manage_emojis=True)
    async def steal_emoji(self, ctx, emoji: discord.PartialEmoji, *, name: str = None):
        """
        Steals a given emoji and you're able to give it a new name.
        Permissions needed: `Manage Emojis`
        """
        emoji_name = name or emoji.name

        emoji_bytes = await emoji.read()

        if len(ctx.guild.emojis) == ctx.guild.emoji_limit:
            return await ctx.send("I can't add that as the server has reached its emoji limit")

        new_emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=emoji_bytes, reason=f"Responsible user: {ctx.author}")

        await ctx.send(f"Successfully stolen {new_emoji} with the name `{new_emoji.name}`")

    @commands.command(aliases=['vote_check'])
    async def votecheck(self, ctx, member: discord.Member = None):
        """
        Checks the voting status of a specified member.
        """
        if not member:
            member = ctx.author

        url = "{}bots/{}/check".format(self.ep, ctx.me.id)

        params = dict(userId=member.id)

        response = await self.session.get(
            url=url,
            headers=self.headers,
            params=params
        )

        if response.status != 200:
            return await ctx.send("Received code {}: {}".format(response.status, response.reason))

        data = await response.json()
        voted = bool(data['voted'])
        status = 'has' if voted else 'has not'

        return await ctx.send("{} {} voted!".format(member.display_name, status))

    @commands.command(aliases=['vote'])
    async def invite(self, ctx):
        """
        Send's the bots invite link, you can also vote using this link
        """
        embed = discord.Embed(
            title='TOP.GG link, thanks if you vote/invite!',
            url="https://top.gg/bot/769137475942613023",
            colour=self.bot.colour)

        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx):
        """
        Gives info about the source code
        """
        embed = discord.Embed(colour=self.bot.colour)
        embed.add_field(
            name='Source',
            value="Don't mind the mess, this code is quite old and will be improved !https://github.com/LtCustard/Resolute/")

        await ctx.send(embed=embed)

    @commands.command()
    async def credits(self, ctx):
        """
        Send credit's regarding the bot.
        """
        user1 = self.bot.get_user(434734486404726785)
        embed = discord.Embed(colour=self.bot.colour)
        embed.add_field(
            name="Credit's",
            value=f"{user1.name} - Helped make the bot's profile picture.")
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar)

        await ctx.send(embed=embed)

    @commands.command()
    async def support(self, ctx):
        """
        If you really need help, you can join this server.
        """
        embed = discord.Embed(
            title='Discord invite',
            description='[Invite](https://discord.gg/jpVmkbbnBE)',
            colour=self.bot.colour)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Misc(bot))
