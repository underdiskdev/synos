from .channelcontext import ChannelContext
from .commands import *

class ServerContext:
	def __init__(self, server):
		self.prefix = '%'
		self.server = server
		self.channels = {}
		self.commands = [CommandHelp()]

	async def treat(self, message):
		hash_id = hash(message.channel)
		if not hash_id in self.channels:
			self.channels[hash_id] = ChannelContext(message.channel)

		if message.content.startswith(self.prefix):
			command = message.content[1:].split(" ")
			if command[0] == 'bot':
				command.pop(0)
				if len(command) == 0:
					command.append("help")
				for cmd in self.commands:
					if cmd.keyword == command[0]:
						await cmd.execute(command[1:], message, self)
			else:
				await self.channels[hash_id].command(message, command)

	async def server_command(self, message, command):
		argslen = len(command)
		if argslen == 0:
			await message.channel.send("Invalid bot command. Do '" + self.prefix + "bot help' for help")
		else:
			if command[0] == 'setprefix':
				if argslen != 2:
					await message.channel.send('Usage : ' + self.prefix + 'bot setprefix <prefix>')
				else:
					if len(command) != 1 and command[1].isalnum():
						await message.channel.send('Prefix should be 1 character long and NOT alphanumeric')
					else:
						self.prefix = command[1]
						await message.channel.send('Changed the prefix to ' + self.prefix)
						#todo: save this data for reboots
			elif command[0] == 'help':
						await message.channel.send(self.server_command_help())
			elif command[0] == 'status':
				pass #todo

	def server_command_help(self):
		return	self.prefix + "bot setprefix <prefix>\n\tchange bot prefix\n\n" +\
				self.prefix + "bot help\n\tdisplay this help\n\n" +\
				self.prefix + "bot status\n\tdisplay bot status\n\n"