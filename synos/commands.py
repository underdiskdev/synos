class CommandArgument:
	def __init__(self, name, optdesc):
		self.name = name
		self.optdesc = optdesc

class Command:
	def __init__(self):
		self.keywords = []
		self.args = []
		self.optargs = []
		self.desc = ""

	async def pre_execute(self, args, message):
		if len(args) < len(self.args):
			await message.channel.send("At least " + str(len(self.args)) + " argument(s) requested. Got " + str(len(args)) + ".")
			return True
		if len(args) > len(self.args) + len(self.optargs):
			await message.channel.send("A maximum of " + str(len(self.args) + len(self.optargs)) + " argument(s) requested. Got " + str(len(args)) + ".")
			return True

		return False

	def usage_str(self):
		string = str(self.keyword)
		if len(self.args) != 0:
			string = string + " <"
			for arg in self.args:
				string = string + str(arg.name)
				if arg.optdesc != "":
					string = string + "(" + arg.optdesc + ")"
				string = string + ">"

		if len(self.optargs) != 0:
			string = string + " ["
			for arg in self.optargs:
				string = string + str(arg.name)
				if arg.optdesc != "":
					string = string + "(" + arg.optdesc + ")"
				string = string + "]"
		return string

class ServerCommand(Command):
	pass

class ChannelCommand(Command):
	pass

######################"


class CommandHelp(ServerCommand):
	def __init__(self):
		Command.__init__(self)
		self.keyword = "help"
		self.args = []
		self.desc = "Display help"

	async def execute(self, args, message, context):
		status = await self.pre_execute(args, message)
		if status:
			return

		string = ""

		for command in context.commands:
			string = string + context.prefix + "bot " + command.usage_str() + "\n\t" + command.desc + "\n\n"

		await message.channel.send(string)

class HelpCommand(ChannelCommand):
	def __init__(self):
		Command.__init__(self)
		self.keyword = "help"
		self.args = []
		self.desc = "Display help"

	async def execute(self, args, message, context):
		status = await self.pre_execute(args, message)
		if status:
			return

		string = ""

		for command in context.commands:
			string = string + context.serverContext.prefix + command.usage_str() + "\n\t" + command.desc + "\n\n"

		await message.channel.send(string)

class SetPrefixCommand(ServerCommand):
	def __init__(self):
		Command.__init__(self)
		self.keyword = "setprefix"
		self.args = [CommandArgument("new prefix", "")]
		self.desc = "Change the bot prefix"

	async def execute(self, args, message, context):
		status = await self.pre_execute(args, message)
		if status:
			return
		if len(args[0]) != 1:
			await message.channel.send("Prefix should be 1 character long")
		elif args[0].isalnum():
			await message.channel.send("Prefix cannot be alphanumerical")
		else:
			context.prefix = args[0]
			await message.channel.send('Changed the prefix to ' + context.prefix)
			#todo: save this data for reboots