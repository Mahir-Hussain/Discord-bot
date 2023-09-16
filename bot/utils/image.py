import os
from io import BytesIO

import asyncdagpi
import discord
from discord.ext import commands


async def dagpi_img(user, feature) -> discord.File:
    """
    Access the Dagpi API
    """
    dagpi = asyncdagpi.Client(os.environ["dagpi"])
    url = str(user.avatar.replace(static_format="png"))
    img = await dagpi.image_process(feature, url)
    if feature == "colors":
        img_file = discord.File(fp=img.image, filename="image.png")
    else:
        img_file = discord.File(fp=img.image, filename=f"image.{img.format}")
    await dagpi.close()
    return img_file
