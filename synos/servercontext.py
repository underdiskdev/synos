from .channelcontext import ChannelContext
from .commands import *

class ServerContext:
	def __init__(self, server):
		self.prefix = '%'
		self.server = server
		self.channels = {}
		self.commands = [CommandHelp(), SetPrefixCommand()]

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
