import discord
import configparser

import synos

client = discord.Client()
config_file = configparser.ConfigParser()

config_file.read("cfg/config.ini")
token = config_file["PRIVATE"]["Token"]

router = None

@client.event
async def on_ready():
	global router
	print('Logged in as {0.user}'.format(client))

	# this object will route commands depending on the server and channel
	router = synos.CommandRouter(client)

@client.event
async def on_message(message):
	global router
	await router.treat(message)

# token defined in cfg/config.ini
if token != "":
	client.run(token)
else:
	print("Error: Invalid token")