import io

import discord
import sr_api
from asyncdagpi import ImageFeatures
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from utils.image import dagpi_img
from utils.utils import bypass_for_owner


class Image(commands.Cog, name="🖼️ Image Manipulation"):
    """These commands change a profile picture."""

    def __init__(self, bot):
        self.bot = bot
        self.sr = sr_api.Client()

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def wanted(self, ctx, user: discord.Member = None):
        """Puts a members user avatar on a wanted poster."""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.wanted())
            await ctx.reply(content=f"{user.name} Is wanted", file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def jail(self, ctx, user: discord.Member = None):
        """Jail a user"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.jail())
            await ctx.reply(file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def deepfry(self, ctx, user: discord.Member = None):
        """Deepfry an avatar."""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.deepfry())
            await ctx.reply(file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def pixelate(self, ctx, user: discord.Member = None):
        """Pixelates someones pfp"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.pixel())
            await ctx.reply(file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def blur(self, ctx, user: discord.Member = None):
        """Blurs a pfp"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.blur())
            await ctx.reply(file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def invert(self, ctx, user: discord.Member = None):
        """Invert a pfp"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.invert())
            await ctx.reply(file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def communism(self, ctx, user: discord.Member = None):
        """Add a comunism overlay to someones pfp"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.communism())
            await ctx.reply(file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def trigger(self, ctx, user: discord.Member = None):
        """Trigger overlay on someones pfp"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.triggered())
            await ctx.reply(file=img_file)

    @commands.command(aliases=["colors"])
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def colours(self, ctx, user: discord.Member = None):
        """Shows you the top few colours in a persons pfp"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.colors())
            await ctx.reply(file=img_file)

    @commands.command()
    @commands.dynamic_cooldown(type=BucketType.user, cooldown=bypass_for_owner)
    async def swirl(self, ctx, user: discord.Member = None):
        """Swirl a pfp"""

        async with ctx.typing():
            user = user or ctx.author
            img_file = await dagpi_img(user, ImageFeatures.swirl())
            await ctx.reply(file=img_file)

    @commands.command()
    async def rgb(self, ctx, user: discord.Member = None):
        """RGB overlay"""

        async with ctx.typing():
            try:
                user = user or ctx.author
                img_file = await dagpi_img(user, ImageFeatures.hog())
                await ctx.reply(file=img_file)
            except KeyError:
                await ctx.reply(
                    "This command did not work with you profile picture possibly because it is a gif."
                )

    @commands.command()
    async def night(self, ctx, user: discord.Member = None):
        """No colour on a user"""

        async with ctx.typing():
            try:
                user = user or ctx.author
                img_file = await dagpi_img(user, ImageFeatures.night())
                await ctx.reply(file=img_file)
            except KeyError:
                await ctx.reply(
                    "This command did not work with you profile picture possibly because it is a gif."
                )

    @commands.command()
    async def rainbow(self, ctx, user: discord.Member = None):
        """Rainbow overlay"""

        async with ctx.typing():
            try:
                user = user or ctx.author
                img_file = await dagpi_img(user, ImageFeatures.rainbow())
                await ctx.reply(file=img_file)
            except KeyError:
                await ctx.reply(
                    "This command did not work with you profile picture possibly because it is a gif."
                )

    @commands.command()
    async def america(self, ctx, user: discord.Member = None):
        """America overlay"""

        async with ctx.typing():
            try:
                user = user or ctx.author
                img_file = await dagpi_img(user, ImageFeatures.america())
                await ctx.reply(file=img_file)
            except KeyError:
                await ctx.reply(
                    "This command did not work with you profile picture possibly because it is a gif."
                )

    @commands.command()
    async def wasted(self, ctx, user: discord.Member = None):
        """GTA V wasted meme"""

        async with ctx.typing():
            try:
                user = user or ctx.author
                img_file = await dagpi_img(user, ImageFeatures.wasted())
                await ctx.reply(file=img_file)
            except KeyError:
                await ctx.reply(
                    "This command did not work with you profile picture possibly because it is a gif."
                )

    @commands.command()
    async def youtube(self, ctx, member: discord.Member = None, *, comments: str):
        """Youtube comment as a member"""

        async with ctx.typing():
            member = member or ctx.author

            embed = discord.Embed(title=str(member), colour=ctx.author.colour)

            avatar = str(member.default_avatar.replace(static_format="png"))
            username = member.display_name
            comment = comments
            image = self.sr.youtube_comment(avatar, username, comment)

            embed.set_image(url="attachment://ytcomment.png")
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar
            )

            file = discord.File(
                io.BytesIO(await image.read()), filename="ytcomment.png"
            )

            await ctx.reply(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Image(bot))
