import discord
import configparser

import synos

client = discord.Client()
config_file = configparser.ConfigParser()

config_file.read("cfg/config.ini")
token = config_file["PRIVATE"]["Token"]

dispatcher = None

@client.event
async def on_ready():
	global dispatcher
	print('Logged in as {0.user}'.format(client))

	# this object will dispatch commands depending on the server and channel
	dispatcher = synos.CommandDispatcher(client)

@client.event
async def on_message(message):
	global dispatcher
	await dispatcher.dispatch(message)

# token defined in cfg/config.ini
if token != "":
	client.run(token)
else:
	print("Error: Invalid token")