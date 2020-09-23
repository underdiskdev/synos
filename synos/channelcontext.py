class ChannelContext:
	def __init__(self, channel):
		self.commands = []
		self.channel = channel # Discord.py channel class
		self.last_url = "" # URL to the last attachment sent on this channel

	async def command(self, message, command):
		print("Command: " + str(command) + " on server '" + message.guild.name + "' (" + str(message.guild.id) + ")");