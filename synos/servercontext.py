from .channelcontext import ChannelContext
from .commands import *

class ServerContext:
	def __init__(self, server):
		self.prefix = '%'
		self.server = server
		self.channels = {}
		self.commands = [CommandHelp(), SetPrefixCommand()]

	async def treat(self, message, client_usr):
		hash_id = hash(message.channel)
		if not hash_id in self.channels:
			self.channels[hash_id] = ChannelContext(message.channel, self)

		if len(message.attachments) != 0:
			self.channels[hash_id].last_url = message.attachments[0].url
			self.channels[hash_id].last_filename = message.attachments[0].filename

		if message.author == client_usr:
			return

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
				if len(command) != 0:
					await self.channels[hash_id].command(message, command)
