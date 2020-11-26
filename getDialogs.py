from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from datetime import datetime
import time 
import random as rnd

api_id = 1155244
api_hash = "cfb16f25f9ee8b62b945b47be963ae19"
phone = "+380973329565"

client = TelegramClient("Checker", api_id, api_hash)
client.start()

for dialog in client.iter_dialogs():
	print(dialog.id, "\tNAME ->", dialog.name)

