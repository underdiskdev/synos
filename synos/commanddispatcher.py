from .servercontext import ServerContext

class CommandDispatcher:
	def __init__(self, client):
		self.client = client
		self.servers = {}

	async def dispatch(self, message):
		hash_id = hash(message.guild)
		if not hash_id in self.servers:
			self.servers[hash_id] = ServerContext(message.guild)

		if message.author == self.client.user:
			return
		
		await self.servers[hash_id].dispatch(message)