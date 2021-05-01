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
# from qrtools import QR
import qrtools
from pyzbar import pyzbar
import argparse
import cv2

load_dotenv()

client = discord.Client()
logfile = open('logs.txt', 'a')


@client.event
async def on_ready():
    print("We have succesfully connected the bot")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    imsg = message.content
    logfile.write(imsg+'\n')
    if(imsg.startswith("$help")):
        async with message.channel.typing():
            await message.channel.send("$qrcode <link> to get the qrcode\n$rimg and attach image to read qr code")

    if(imsg.startswith("$qrcode")):
        async with message.channel.typing():
            link = imsg.split("$qrcode ", 1)[1]
            try:
                url = pyqrcode.create(link)
                url.png('myqr.png', scale=6)
                await message.reply(file=discord.File('myqr.png'))
                os.remove('myqr.png')
                logfile.write("succesfully created qr\n")
            except:
                logfile.write("qr create unsuccesful \n")
                await message.reply("sorry bot is unable to create qr")
    if(imsg.startswith("$rimg")):
        async with message.channel.typing():
            attachment = message.attachments
            await attachment[0].save(attachment[0].filename)
            try:
                image = cv2.imread(attachment[0].filename)
                barcodes = pyzbar.decode(image)
                for barcode in barcodes:
                    barcodeData = barcode.data.decode("utf-8")
                os.remove(attachment[0].filename)
                await message.reply(barcodeData)
                logfile.write("read qr succesful\n")
            except:
                logfile.write("read qr unsuccesful\n")
                await message.reply("sorry,the bot is not optimised for this qr code,I am working on it")


keep_alive()
my_secret = os.getenv('token')
print(my_secret)
client.run(my_secret)
