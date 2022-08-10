import telethon
from telethon import *
import configparser
import sys
import asyncio

#read ini files
config=configparser.ConfigParser()
config.read("config.ini")

#Setting Config_Values
api_id=config.get('telegram', 'api_id')
api_hash=config.get('telegram', 'api_hash')

api_hash = str(api_hash)

phone=config.get('telegram', 'phone')
username=config.get('telegram', 'username')

async def Get3DS():
    async with TelegramClient('3DS_Session', api_id, api_hash) as client:
       await client.send_message('Rico3Cap', 'Inserisci il codice 3DS che ti è arrivato')

       @client.on(events.NewMessage(chats="ricos"))
       async def Getcode(event):
           await event.reply('Grazie!')
           code_3ds = event.raw_text
           print (code_3ds)
           await client.disconnect()
       await client.run_until_disconnected()


asyncio.run(Get3DS())