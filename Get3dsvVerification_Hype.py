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
       await client.send_message('Rico3Cap', 'Richiesta inviata in app, Per favore conferma scrivendo "OK" quando hai confermato!')

       @client.on(events.NewMessage(chats="ricos"))
       async def Getcode(event):
           if "OK" in event.raw_text:
               print ("confirmed")
               await event.reply('Grazie per la conferma!')
               await client.disconnect()
       await client.run_until_disconnected()

asyncio.run(Get3DS())