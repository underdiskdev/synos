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
			await message.channel.send("At least " + str(len(self.args)) + " arguments requested. Got " + str(len(args)) + ".")
			return True
		if len(args) > len(self.args) + len(self.optargs):
			await message.channel.send("A maximum of " + str(len(self.args) + len(self.optargs)) + " arguments requested. Got " + str(len(args)) + ".")
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
