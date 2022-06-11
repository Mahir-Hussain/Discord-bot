import asyncio
import datetime
import io
import json
import sys
import time

import os
import aiohttp
import async_cse
import discord
import motor.motor_asyncio as motor
import psutil
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from PyDictionary import PyDictionary
from utils.utils import Mongodb_afks as collection
from utils.utils import Mongodb_t as cogs_t


class Meta(commands.Cog, name="🤖 Meta"):
    """
    These commands give some information
    """
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}  # Dict for storing sniped messages
        self.esnipes = {}  # Dict for storing edited

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.author.bot:
            return

        guild = before.guild
        channel = before.channel

        guildEditedMsgs = self.esnipes.get(guild.id, {})
        channelEditedMsgs = guildEditedMsgs.get(channel.id, [])

        if len(channelEditedMsgs) >= 5:
            channelEditedMsgs = channelEditedMsgs[-5:]
        channelEditedMsgs.append({'before': before, 'after': after})
        guildEditedMsgs[channel.id] = channelEditedMsgs
        self.esnipes[guild.id] = guildEditedMsgs

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        # Ignore bots and messages without actual content, such as images
        if message.author.bot or not message.content:
            return

        # Store the message in dict, with the channel ID as the key
        self.messages[message.channel.id] = message

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def google(self, ctx, *, query: str):
        """
        Google whatever you want.
        """
        cse = async_cse.Search(os.environ["google"])
        results = await cse.search(query, safesearch=True)

        how_many = 10 if len(results) > 10 else len(results)

        embed_list = []

        for i in range(1):
            embed = discord.Embed(colour=self.bot.colour)
            embed.title = results[i].title
            embed.description = results[i].description
            embed.url = results[i].url
            embed.set_image(url=results[i].image_url)
            print(results[i].image_url)
            embed.set_footer(
                text=f'Requested by {ctx.author}',
                icon_url=ctx.author.avatar_url)

            embed_list.append(embed)

        await cse.close()
        await ctx.send(embed=embed)

    @commands.command(aliases=["ud", "urban"])
    @commands.cooldown(1, 5, BucketType.user)
    async def urbandictionary(self, ctx, *, definition: str):
        """
        Get a urban dictionary definition of almost any word!
        """
        if len(definition) == 0:
            return await ctx.send("You need to send the word that you want defined")

        if " " in definition:
            definition = definition.replace(" ", "-")
        async with self.bot.session.get("http://api.urbandictionary.com/v0/define?term=" + definition) as response:

            if response.status != 200:
                return await ctx.send("Couldn't find that word.")

            data = await response.json()

            if not data["list"]:
                return await ctx.send("There were no results for that look up.")

        word = data["list"][0]["word"]
        author = data["list"][0]["author"]
        definition = data["list"][0]["definition"]
        example = data["list"][0]["example"]
        perma_link = data["list"][0]["permalink"]

        if len(definition) > 1024 or len(example) > 1024:
            return await ctx.send("The lookup for this word is way too big to show.")

        embed = discord.Embed(title=f"Definition of {word}", colour=self.bot.colour)
        embed.set_author(name=f"Definition by: {author}")
        embed.url = perma_link
        embed.set_footer(
            text=f"Requested by {ctx.author.name} | Urban dictionary.",
            icon_url=ctx.author.avatar_url,
        )
        embed.add_field(name="Definition:", value=definition, inline=False)
        embed.add_field(name="Example:", value=example, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["df", "define"])
    async def dictionary(self, ctx, definition: str):
        """
        Get a definition from an actual dictionary.
        You can get an urban definition from the command `urban <definition`.
        """
        if len(definition) == 0:
            return await ctx.send("You need to send the word that you want defined")

        embed = discord.Embed(
            title=f"definition of {definition}",
            description=str(
                PyDictionary.meaning(definition)),
            colour=self.bot.colour)
        embed.set_footer(
            text=f"Requested by {ctx.author.name} | Dictionary.",
            icon_url=ctx.author.avatar_url,
        )
        try:
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send('Too big to show.')

    @commands.command(aliases=["ss"])
    async def screenshot(self, ctx, url):
        """
        Takes a screenshot of any site.
        """
        start = time.perf_counter()
        await ctx.send('This may take some time.')

        ss = discord.Embed(title=f"Screenshot of {url}", colour=self.bot.colour)

        async with self.bot.session.get(f'https://image.thum.io/get/width/1920/crop/0/maxAge/1/noanimate/https://{url}/') as r:
            res = await r.read()
            ss.set_image(url="attachment://webreq.png")
            end = time.perf_counter()
            ss.set_footer(
                text=f"Requested by {ctx.author.name} | Image fetched in {round((end - start) * 1000)} ms",
                icon_url=ctx.author.avatar_url)

            file_ss = await ctx.send(file=discord.File(io.BytesIO(res), filename="webreq.png"), embed=ss)
            await file_ss.add_reaction("\U0001f6ae")
            await asyncio.sleep(1)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0)
            except asyncio.TimeoutError:
                await file_ss.delete()
                return
            else:
                if str(reaction.emoji) == "\U0001f6ae":
                    await file_ss.delete()
                    await ctx.send('The file has been deleted by a user.')

    @commands.command(aliases=["w"])
    @commands.cooldown(1, 10, BucketType.user)
    async def weather(self, ctx, *, city_name: str):
        """
        Get the weather of a city/town by its name.
        """
        # Code By CraziiAce#0001
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + \
            city_name + f"&appid={os.environ['weather']}&units=metric"

        async with self.bot.session.get(url) as response:
            weather_response = await response.json()

            if weather_response['cod'] != 200:
                await ctx.send(f"An error ocurred: `{weather_response['message']}`.")
            else:

                currentUnix = time.time()
                localSunrise = weather_response['sys']['sunrise'] + \
                    weather_response['timezone']
                sunriseTime = datetime.datetime.utcfromtimestamp(
                    localSunrise)
                localSunset = weather_response['sys']['sunset'] + \
                    weather_response['timezone']
                sunsetTime = datetime.datetime.utcfromtimestamp(
                    localSunset)
                localTimeUnix = currentUnix + weather_response['timezone']
                localTime = datetime.datetime.utcfromtimestamp(
                    localTimeUnix)

                embed = discord.Embed(
                    title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                    url=f"https://openweathermap.org/city/{weather_response['id']}",
                    description=weather_response['weather'][0]['description'],
                    colour=self.bot.colour,
                )
                embed.add_field(
                    name='Location:',
                    value=f"**🏙️ City:** {weather_response['name']}",
                    inline=False)
                embed.add_field(
                    name='Weather',
                    value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}°\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}° \n**🌡️ Daily High:** {weather_response['main']['temp_max']}°\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}° \n**<:water_drop:791328777023258665> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph",
                    inline=False)
                embed.add_field(
                    name='Time',
                    value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n**🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n**🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                embed.set_thumbnail(
                    url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                embed.set_footer(
                    text=f'Requested by {ctx.author}',
                    icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                embed.set_author(
                    name=ctx.author, icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 20, BucketType.user)
    async def afk(self, ctx, *, reason: str = 'AFK'):
        """
        Set an AFK.
        """
        try:
            time = str(ctx.message.created_at).split(
                ' ')[1].replace(':', '').replace('.', '')
            finaltime = round(int(time) / 100000000)

            await ctx.send(f'{ctx.author.mention}, I have successfully marked your **AFK** as: {reason}')
            await asyncio.sleep(15)

            post = {
                "_id": ctx.author.id + ctx.guild.id,
                "name": str(
                    ctx.author),
                "message": reason,
                "guild": ctx.guild.id,
                "time": finaltime}
            await collection(mt="insert_one", find=post)
        except Exception:
            await ctx.send('This command errored. This may be due to you setting multiple afks in different servers. Issue will be fixed soon. **Notice** This error should have been fixed. If not please contact Elite#1296')

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def snipe(self, ctx):
        """
        Snipe the last deleted message.
        """
        # Get the snipe message for this channel
        message = self.messages.get(ctx.channel.id)

        # React with cross if bot can't find it
        if message is None:
            await ctx.message.add_reaction('<:XSomeColour:784146174163681310>')

        else:

            embed = discord.Embed(colour=self.bot.colour)
            embed.add_field(name="Last deleted message.",
                            value=f"> Sniped message: `{message.content}`"
                            + f"\n> Author: `{message.author}`")
            embed.set_footer(text=f'Requested by {ctx.author}',
                             icon_url=ctx.author.avatar_url)

            try:
                await ctx.reply(embed=embed)
            except Exception:
                await ctx.send('Too big to show')

    @commands.command(aliases=['es'])
    async def editsnipe(self, ctx):
        """
        Show's the last edited message
        """
        gsn = self.esnipes.get(ctx.guild.id, {})
        if gsn:
            csn = gsn.get(ctx.channel.id, [])
            if csn:
                msg = csn[-1]
                bf, af = msg['before'], msg['after']

                embed = discord.Embed(colour=self.bot.colour)
                embed.add_field(
                    name='Edit snipe',
                    value=f'> Original Message: `{bf.content}`\n > Edited Message: `{af.content}` \n > Author: `{bf.author}`')
                embed.set_footer(text=f'Requested by {ctx.author}',
                                 icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                await ctx.message.add_reaction('<:XSomeColour:784146174163681310>')
        else:
            await ctx.message.add_reaction('<:XSomeColour:784146174163681310>')

    @commands.command()
    async def ping(self, ctx):
        """
        Get info on the bots ping.
        """
        embed = discord.Embed(colour=self.bot.colour)
        embed.add_field(
            name="<:server:783423084199280720> Server",
            value=f'```autohotkey\n{round(self.bot.latency * 1000)} ms```')
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar_url)

        start = time.perf_counter()
        message = await ctx.send("You wanted a ping?")
        end = time.perf_counter()
        duration = (end - start) * 1000

        embed.add_field(
            name="<:type:783423629664452649> Typing",
            value='```autohotkey\n{:.2f} ms```'.format(duration))

        start = time.perf_counter()
        await collection(mt="command", find="ping")
        end = time.perf_counter()
        duration = (end - start) * 1000

        embed.add_field(
            name="<:mongodb:798091872748568646> Database",
            value='```autohotkey\n{:.2f} ms```'.format(duration))

        await message.edit(embed=embed)

    @commands.command(aliases=["p"])
    async def permissions(self, ctx, user: discord.Member = None):
        """
        Check a users discord permissions.
        """
        user = user or ctx.author
        await ctx.send(" | ".join([perm for perm, val in dict(user.permissions_in(ctx.channel)).items() if val]).replace("_", " "))

    @commands.command(aliases=["whois"])
    @commands.cooldown(1, 3, BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        """
        This command looks at a user's profile
        """
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author

        if member.bot is False:
            emoji = '<:XSomeColour:784146174163681310>'
        else:
            emoji = '<:TickSomeColour:780469518010155109>'

        roles = ' '.join([r.mention for r in member.roles if r !=
                          ctx.guild.default_role] or ['`No roles.`'])

        embed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at,
            title=f"User Info")
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar_url)
        embed.add_field(
            name='General Info',
            value=f'Username: `{member}` \nNickname: `{member.display_name}` \nID: `{member.id}` \nAccount creation: `{member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}` \nBot: {emoji}',
            inline=False)
        try:

            embed.add_field(
                name='Guild Info',
                value=f'Joined: `{member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}` \nRoles: {roles}',
                inline=False)

        except Exception:
            return False

        embed.set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=embed)
        # embed = discord.Embed(
        #    colour=(colour),
        #    timestamp=ctx.message.created_at,
        #    title=f"User Info")
        # embed.set_footer(
        #    text=f'Requested by {ctx.author}',
        #    icon_url=ctx.author.avatar_url)
        # embed.add_field(
        #    name='General Info',
        #    value=f'Username: `{member}` \nNickname: `{member.display_name}` \nID: `{member.id}` \nAccount creation: `{member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}` \nBot: {emoji}',
        #    inline=False)
        # embed.add_field(
        #    name='Guild Info',
        #    value=f'Joined: `{member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")}` \nRoles: Too many to display',
        #    inline=False)
        # embed.set_thumbnail(url=member.avatar_url)

        # await ctx.send(embed=embed)

    @commands.command(aliases=['si'])
    async def serverinfo(self, ctx):
        """
        Send some info about the server
        """
        all_mem = len(ctx.guild.members)
        bots = sum(m.bot for m in ctx.guild.members)
        members = all_mem - bots

        embed = discord.Embed(title='Server info', colour=self.bot.colour)
        embed.add_field(
            name='Owner info',
            value=f'Owner: `{ctx.guild.owner}` \nOwner ID: `{ctx.guild.owner.id}`')
        embed.add_field(
            name='Server',
            value=f'Members: `{members}` \nBots: `{bots}` \nTotal: `{all_mem}` \nRoles: `{len(ctx.guild.roles)}` \nChannels: `{len(ctx.guild.text_channels)}` \nServer ID: `{ctx.guild.id}` \nCreated at: `{ctx.guild.created_at}`',
            inline=False)
        embed.set_thumbnail(url=str(ctx.guild.icon_url))
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['about'])
    @commands.guild_only()
    async def botinfo(self, ctx):
        """
        Gives you some info on the bot
        """

        embed = discord.Embed(
            title=f'Info',
            description=f'A few things to know! Made by Elite#1296',
            colour=self.bot.colour)
        embed.add_field(
            name='<:cog:780007481216204820> Bot stats',
            value=f"Server count: {len(self.bot.guilds)} \nMembers: {len(self.bot.users)}",
            inline=False)
        embed.add_field(
            name=f'<:cog:780007481216204820> Hosting stats',
            value=f'Python version: `{sys.version[:5]}` \nDPY version: `{discord.__version__}` \nCurrent ping: `{round(self.bot.latency * 1000)} ms`  \nCPU usage: `{psutil.cpu_percent()}%` \nRAM usage: `{psutil.virtual_memory().percent}%`',
            inline=False)
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Meta(bot))
