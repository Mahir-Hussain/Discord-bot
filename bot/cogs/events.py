import discord
from discord.ext import commands
from utils.utils import Mongodb_afks as collection

import json
import random

import motor.motor_asyncio as motor
import pymongo


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        elif message.content in ("<@!769137475942613023>", "<@769137475942613023>"):
            await message.channel.send("Hey! My prefix's are: `resolute `, `r.` ")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.content != after.content:
            ctx = await self.bot.get_context(after)
            await self.bot.invoke(ctx)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        all_members = len(guild.members)
        bots = sum(m.bot for m in guild.members)
        members = all_members - bots

        join_channel = self.bot.get_channel(803287405268041788)
        embed_join = discord.Embed(colour=self.bot.colour)
        embed_join.add_field(
            name="Guild Joined",
            value=f"I have joined `{guild.name}`. It has `{members}` members and `{bots}` bots. The guild ID is `{guild.id}`")
        await join_channel.send(embed=embed_join)

        embed = discord.Embed(colour=self.bot.colour)
        embed.add_field(
            name="Hello!",
            value="My prefixes are `resolute ` and `r.`! You can run r.info to learn more :)")
        embed.set_footer(text='Resolute')
        await guild.system_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        leave_channel = self.bot.get_channel(805818734236925953)
        await leave_channel.send(f"I have been removed from `{guild.name}`, the ID is `{guild.id}`. I am now in `{len(self.bot.guilds)}` guilds.")

    @commands.Cog.listener(name="on_message")
    async def on_afk_say(self, message):

        if message.guild:
            try:
                aid = message.author.id + message.guild.id
                data = await collection(mt="find_one", find=aid)
                if data:
                    if data.get('guild') == message.guild.id:
                        await message.channel.send(f'{message.author.mention}, I have removed your AFK', delete_after=5)

                        await collection(mt="delete_one", find=aid)

            except KeyError:
                pass

    @commands.Cog.listener(name="on_message")
    async def on_afk_ping(self, message):

        if message.author.bot or message.author == self.bot.user:
            return False

        for i in message.mentions:
            to_find = i.id + message.guild.id
            a = await collection(mt='find_one', find=to_find)
            try:
                found = a['_id'] - message.guild.id

                if i.id == found:
                    await message.channel.send(f'{message.author.mention}, **{i.display_name}** is currently AFK for: {a["message"]}')
                    return True
            except Exception:
                return False


async def setup(bot):
    await bot.add_cog(Events(bot))
