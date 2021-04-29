from re import S
import discord
import os
from discord import channel
import requests
import json
from keep_alive import keep_alive
from dotenv import load_dotenv
import pyqrcode
import png
from pyqrcode import QRCode

load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
    print("We have succesfully connected the bot")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    imsg = message.content
    async with message.channel.typing():
        if(imsg.startswith("$help")):
            await message.channel.send("$qrcode <link> to get the qrcode")
        if(imsg.startswith("$startgame")):
            # await message.channel.send(message.author.guild.id)
            await message.reply(message.mentions)
        if(imsg.startswith("$qrcode")):
            link = imsg.split("$qrcode ", 1)[1]
            try:
                url = pyqrcode.create(link)
                url.png('myqr.png', scale=6)
                await message.reply(file=discord.File('myqr.png'))
            except:
                await message.reply("sorry bot is unable to create qr")


keep_alive()
my_secret = os.getenv('token')
client.run(my_secret)
