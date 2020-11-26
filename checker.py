from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from datetime import datetime
import json
import os
import colorama


def writeToUserLog(event, name):
	user_path = os.path.join(name, name+"_online")

	if not os.path.isdir(name):
		os.mkdir(name)

	if not os.path.isfile(user_path):
		f = open(user_path, "w")
		f.close()

	with open(user_path, "a") as user_file:
		user_status = event.online
		user_last_seen = event.last_seen
		user_until = event.until
		date_now = datetime.now()

		data_line = name+"|Status:"+str(user_status)+"|LastSeen:"+str(user_last_seen)+"|Until:"+str(user_until)+"|Now:"+str(date_now)+"\n"
		user_file.write(data_line)


def writeGlobalLog(event, name):
	with open(LOG_PATH, "a") as log_file:
		date_now = datetime.now()
		
		data_line = name+"|"+str(date_now)+"\n"
		log_file.write(data_line)


def get_json(path):
	with open(path, "r") as json_file:
		data = json_file.read()
	return json.loads(data)


def get_chats(users):
	for user in users:
		yield user["chat_id"]


def get_names(users):
	for user in users:
		yield user["name"]




colorama.init(autoreset=True)

LOG_PATH = "log"


settings = get_json("settings.json")
api_id = settings["API_ID"]
api_hash = settings["API_HASH"]

users = get_json("users.json")
users_ids = list(get_chats(users))
user_names = list(get_names(users))


client = TelegramClient("Checker", api_id, api_hash)


@client.on(events.UserUpdate(chats=users_ids, func=lambda e: e.online))
async def handler(event):
	try:
		user_name = user_names[users_ids.index(event.user_id)]
		print(user_name, "online")
		writeToUserLog(event, user_name)
		writeGlobalLog(event, user_name)
		print(user_name, "data saved")
		print()
	except Exception as e:
		print(colorama.Fore.RED + str(e))


client.start()
client.run_until_disconnected()

