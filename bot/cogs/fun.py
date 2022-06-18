import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from aiohttp import request

import asyncio
import datetime
import random

from utils.utils import Mongodb_t as cogs_t


class Fun(commands.Cog, name="🎉 Fun"):
    """
    Fun commands for you to use
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["coin"])
    @commands.guild_only()
    async def coinflip(self, ctx):
        """
        A random generator for flipping the coin.
        """
        choices = ["Heads", "Tails"]
        embed = discord.Embed(
            title="Coin Flip",
            description=(
                random.choice(choices)),
            colour=(self.bot.colour))
        await ctx.send(embed=embed)

    @commands.command(name='8ball')
    @commands.guild_only()
    async def _ball(self, ctx, *, question: str):
        """
        An 8ball command.
        """
        choices = [
            "Yes totally",
            "No wtf.",
            "Ask again later",
            "I guess so",
            "Maybe",
            "Not sure",
            "Sources say yes",
            "Sources say no"]
        embed = discord.Embed(
            title=f"You asked 8ball: {question}",
            description=f'Answer: `{random.choice(choices)}`',
            colour=self.bot.colour)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, BucketType.user)
    async def wyr(self, ctx):
        """
        Does a random would you rather question.
        """
        s = open("bot/utils/questions.txt")
        m = s.readlines()
        l = []
        for i in range(0, len(m) - 1):
            x = m[i]
            z = len(x)
            a = x[:z - 1]
            l.append(a)
        l.append(m[i + 1])
        o = random.choice(l)
        await ctx.send(o)
        s.close()

    @commands.command()
    async def fact(self, ctx):
        """
        Sends a random fact.
        """
        async with self.session.get("https://uselessfacts.jsph.pl/random.json?language=en") as r:
            data = await r.json()
            fact = data["text"]

        embed = discord.Embed(colour=self.bot.colour)
        embed.add_field(name=f'Random fact', value=fact)
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def dice(self, ctx):
        """
        Roll a 6 sided dice.
        """
        num = [1, 2, 3, 4, 5, 6]
        di = random.choice(num)
        await ctx.send(f'You got {di}')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    @commands.max_concurrency(1, per=BucketType.channel, wait=False)
    async def cookie(self, ctx):
        """
        Get the cookie!
        This is a reaction based game.
        """

        rand = [
            "threw it!",
            "ate it.",
            "gave it to the homeless, how nice.",
            "fed it to a dog",
            "choked on it, sad.",
            "was allergic."]
        choice = random.choice(rand)

        m = await ctx.send(embed=discord.Embed(title="The Cookie is coming", colour=self.bot.colour))
        await asyncio.sleep(3)
        await m.edit(embed=discord.Embed(title="The Cookie is coming in 3", colour=self.bot.colour))
        await asyncio.sleep(1)
        await m.edit(embed=discord.Embed(title="The Cookie is coming in 2", colour=self.bot.colour))
        await asyncio.sleep(1)
        await m.edit(embed=discord.Embed(title="The Cookie is coming in 1", colour=self.bot.colour))
        random_time = random.randint(1, 5)
        await asyncio.sleep(random_time)
        await m.edit(embed=discord.Embed(title=":cookie: Grab the Cookie", colour=self.bot.colour))

        await m.add_reaction("\U0001f36a")

        try:
            r, u = await self.bot.wait_for("reaction_add", check=lambda r, u: str(r.emoji) == "\U0001f36a" and r.message == m and r.message.channel == ctx.channel and not u.bot, timeout=10)
        except asyncio.TimeoutError:
            await ctx.send("No one got the cookie so it rotted :(")
        else:
            await m.edit(embed=discord.Embed(title=f"**{u}** got the cookie in {round((datetime.datetime.utcnow()-m.edited_at).total_seconds(), 3)} seconds and {choice}"))

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def meme(self, ctx):
        """
        Get a random meme from reddit, you can also do r.reddit enter_subreddit to get a sub-reddit of your choice.
        """
        reddit = ['comedyheaven',
                  'memes',
                  'programmerhumor',
                  'dankmemes',
                  'funny'
                  ]
        sub = random.choice(reddit)
        async with self.session.get('https://meme-api.herokuapp.com/gimme/' + sub) as resp:
            resp = await resp.json()

        if resp['nsfw'] and not ctx.channel.is_nsfw():
            return await ctx.send("⚠️ | This meme is marked as NSFW and I can't post it in a non-nsfw channel.")
        else:
            embed = discord.Embed(
                title=f"{resp['title']} by u/{resp['author']}",
                url=resp['postLink'],
                colour=self.bot.colour)
            embed.set_image(url=resp['url'])
            embed.set_footer(
                text=f"r/{sub} | Requested by {ctx.author}",
                icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @commands.command(aliases=['r'])
    @commands.cooldown(1, 5, BucketType.user)
    async def reddit(self, ctx, subreddit: str):
        """
        Choose any sub-reddit of your choice
        """
        try:
            async with self.session.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}") as resp:
                resp = await resp.json()

            if resp['nsfw'] and not ctx.channel.is_nsfw():
                return await ctx.send("⚠️ | This meme is marked as NSFW and I can't post it in a non-nsfw channel.")
            else:
                embed = discord.Embed(
                    title=f"{resp['title']} by u/{resp['author']}",
                    url=resp['postLink'],
                    colour=self.bot.colour)
                embed.set_image(url=resp['url'])
                embed.set_footer(
                    text=f"r/{subreddit} | Requested by {ctx.author}",
                    icon_url=ctx.author.avatar)
                await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("That may not be a valid sub-reddit, try another.")

    @commands.command(aliases=["rps"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def rockpaperscissors(self, ctx):
        """
        Play rock paper scissors with the bot!
        """
        options = f"What's your choice {ctx.author}? Rock, Paper or Scissors..."
        embed = discord.Embed(title=options, colour=self.bot.colour)

        msg = await ctx.send(embed=embed)

        # Rock  # Paper  # Scissors
        emojis = ["\U0001faa8", "\U0001f4f0", "\U00002702"]

        bots_choice = random.choice(emojis)

        for _ in emojis:
            await msg.add_reaction(_)

        def check(reaction, user):
            return (
                user == ctx.author
                and str(reaction.emoji) in emojis
                and reaction.message == msg
            )

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=30.0, check=check
            )
        except asyncio.TimeoutError:
            try:
                await msg.clear_reactions()
            except discord.Forbidden:
                pass

            embed.description = "You ran out of time!"
            await msg.edit(embed=embed)
        else:
            if str(reaction) == bots_choice:
                embed.description = f"You drew!"
                embed.colour = self.bot.colour

            elif str(reaction) == emojis[0] and bots_choice == emojis[2]:
                embed.description = f"You have won. The bot chose {bots_choice}"
                embed.colour = self.bot.colour

            elif str(reaction) == emojis[1] and bots_choice == emojis[0]:
                embed.description = f"You have won. The bot chose {bots_choice}"
                embed.colour = self.bot.colour

            elif str(reaction) == emojis[2] and bots_choice == emojis[1]:
                embed.description = f"You have won. The bot chose {bots_choice}"
                embed.colour = self.bot.colour

            else:
                embed.description = f"You lost, how sad. The bot chose {bots_choice}"
                embed.colour = self.bot.colour

            try:
                await msg.clear_reactions()
            except discord.Forbidden:
                pass

            await msg.edit(embed=embed)

    @commands.command()
    async def dankrate(self, ctx, member: discord.Member = None):
        """
        Check yours or others dankrate.
        """

        member = member or ctx.author

        dankrate = random.randint(1, 100)

        embed = discord.Embed(colour=self.bot.colour)
        embed.add_field(
            name=f"{member}'s dankrate",
            value=f"<:dank:798565204353875968> {dankrate}% dankness")
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
