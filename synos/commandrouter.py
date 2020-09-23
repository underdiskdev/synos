from .servercontext import ServerContext

class CommandRouter:
	def __init__(self, client):
		self.client = client
		self.servers = {}

	async def treat(self, message):
		hash_id = hash(message.guild)
		if not hash_id in self.servers:
			self.servers[hash_id] = ServerContext(message.guild)
		
		await self.servers[hash_id].treat(message, self.client.user)