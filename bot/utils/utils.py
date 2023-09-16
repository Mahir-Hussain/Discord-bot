import os

import motor.motor_asyncio as motor
from discord.ext import commands

cluster = motor.AsyncIOMotorClient(os.environ["database"])
db = cluster["resolute"]


def bypass_for_owner(message):
    if message.author.id == 594551272468906003:
        return None
    return commands.Cooldown(1, 10)


async def Mongodb_afks(mt: str, find: int):
    """
    Access the Mongo DB for afks.
    """
    collection = db["afks"]
    if mt == "find_one":
        found = await collection.find_one({"_id": find})
        return found
    elif mt == "delete_one":
        await collection.delete_one({"_id": find})
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
        found = await collection.find_one({"_id": find})
        return found
    elif mt == "delete_one":
        await collection.delete_one({"_id": find})
    elif mt == "insert_one":
        await collection.insert_one(find)
