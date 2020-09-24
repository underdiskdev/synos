from .imagecommands import *
from .commands import *

class ChannelContext:
	def __init__(self, channel, serverContext):
		self.serverContext = serverContext
		self.commands = [HelpCommand(), SaturateCommand(), BlurCommand(), InvertCommand()]
		self.channel = channel # Discord.py channel class
		self.last_url = "" # URL to the last attachment sent on this channel
		self.last_filename = ""

	async def command(self, message, command):
		for cmd in self.commands:
			if cmd.keyword == command[0]:
				await cmd.execute(command[1:], message, self)
				return