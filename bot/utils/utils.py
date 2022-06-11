from io import BytesIO
import os
import aiozaneapi
import asyncdagpi
import discord
import motor.motor_asyncio as motor
from discord.ext import commands

cluster = motor.AsyncIOMotorClient(
    os.environ["database"])
db = cluster["resolute"]

async  def Mongodb_t(mt: str, find: str):
    """
    Acess the Mongo DB for cog highlights
    """
    collection = db["cogs"]
    if mt == "find_one":
        found = await collection.find_one({'_id': find})
        return found
    elif mt == "delete_one":
        await collection.delete_one({'_id': find})
    elif mt == "insert_one":
        await collection.insert_one(find)  

async def Mongodb_highlight(mt: str, find: str):
    """
    Acess the Mongo DB for highlights
    """
    collection = db["highlight"]
    if mt == "find_one":
        found = await collection.find_one({'_id': find})
        return found
    elif mt == "delete_one":
        await collection.delete_one({'_id': find})
    elif mt == "insert_one":
        await collection.insert_one(find)

async def Mongodb_afks(mt: str, find: int):
    """
    Access the Mongo DB for afks.
    """
    collection = db["afks"]
    if mt == "find_one":
        found = await collection.find_one({'_id': find})
        return found
    elif mt == "delete_one":
        await collection.delete_one({'_id': find})
    elif mt == "insert_one":
        await collection.insert_one(find)
    elif mt == "command":
       found = await db.command(find)
       return found

async def Mongodb_logs(mt: str, find: str):
    """
    Access the Mongo DB for logging.
    """
    collection = db["emoji_logging"]
    if mt == "find_one":
        found = await collection.find_one({'_id': find})
        return found
    elif mt == "delete_one":
        await collection.delete_one({'_id': find})
    elif mt == "insert_one":
        await collection.insert_one(find)

async def zane_img(user, zt: str, types: str) -> discord.File: # -> BytesIO:
    """
    Access Zane API
    """
    zane = aiozaneapi.Client(os.environ["zane"])
    url = str(user.avatar_url_as(static_format="png"))
    if zt == "magic":
        image = await zane.magic(url)
    elif zt == "dots":
        image = await zane.dots(url)
    elif zt == "floor":
        image = await zane.floor(url)
    elif zt == "spread":
        image = await zane.spread(url)
    elif zt == "sobel":
        image = await zane.sobel(url)
    elif zt == "sort":
        image = await zane.sort(url)

    if types == "png":
        img_file = discord.File(fp=image, filename=f"{str(user)}.png")

    elif types == "gif":
        img_file = discord.File(fp=image, filename=f"{str(user)}.gif")

    await zane.close()
    return img_file

async def dagpi_img(user, feature) -> discord.File:
    """
    Access the Dagpi API
    """
    dagpi = asyncdagpi.Client(
        os.environ["dagpi"])
    url = str(user.avatar_url_as(static_format="png"))
    img = await dagpi.image_process(feature, url)
    if feature == "colors":
        img_file = discord.File(fp=img.image, filename="image.png")
    else:
        img_file = discord.File(fp=img.image, filename=f"image.{img.format}")
    await dagpi.close()
    return img_file
