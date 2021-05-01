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
#from qrtools import QR
import qrtools
from pyzbar import pyzbar
import argparse
import cv2

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
    if(imsg.startswith("$help")):
        async with message.channel.typing():
            await message.channel.send("$qrcode <link> to get the qrcode\n$rimg and attach image to read qr code")
    if(imsg.startswith("$startgame")):
        async with message.channel.typing():
            # await message.channel.send(message.author.guild.id)
            await message.reply(message.mentions)
    if(imsg.startswith("$qrcode")):
        async with message.channel.typing():
            link = imsg.split("$qrcode ", 1)[1]
            try:
                url = pyqrcode.create(link)
                url.png('myqr.png', scale=6)
                await message.reply(file=discord.File('myqr.png'))
                os.remove('myqr.png')
            except:
                await message.reply("sorry bot is unable to create qr")
    if(imsg.startswith("$rimg")):
        async with message.channel.typing():
            attachment = message.attachments
            await attachment[0].save(attachment[0].filename)
            image = cv2.imread(attachment[0].filename)
            barcodes = pyzbar.decode(image)
            for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
            os.remove(attachment[0].filename)
            await message.reply(barcodeData)


keep_alive()
my_secret = os.getenv('token')
client.run(my_secret)
