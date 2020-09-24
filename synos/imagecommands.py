from .commands import *
import discord
import aiohttp
import os
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

class ImageChannelCommand(ChannelCommand):
	async def download_image(self, hash_id, context):
		path = os.getcwd() + "/data/{" + str(hash_id) + "}/"
		if not os.path.exists(path):
			os.makedirs(path)
		async with aiohttp.ClientSession() as session:
			async with session.get(context.last_url) as data:
				if data.status == 200:
					if os.path.exists(path + context.last_filename):
  						os.remove(path + context.last_filename)
					file = open(path + context.last_filename, "xb")
					file.write(await data.read())
					file.close()
		return path + context.last_filename

class VideoChannelCommand(ChannelCommand):
	async def prepare_vid(self, img):
		pass

#################

class SaturateCommand(ImageChannelCommand):
	def __init__(self):
		Command.__init__(self)
		self.keyword = "saturate"
		self.args = [CommandArgument("intensity", "")]
		self.desc = "Saturate image by a specified amount"

	async def execute(self, args, message, context):
		status = await self.pre_execute(args, message)
		if status:
			return

		intensity = None
		try:
			intensity = float(args[0])
		except Exception as e:
			await message.channel.send("Error: " + str(e))
			return

		if context.last_url.endswith(".jpg") or context.last_url.endswith(".jpeg") or context.last_url.endswith(".png"):
			image_path = await self.download_image(hash(message.channel), context)
			
			image = Image.open(image_path)
			image = image.convert("RGB")
			converter = ImageEnhance.Color(image)
			try:
				image2 = converter.enhance(intensity)
				image2.save(image_path, "PNG")
			except Exception as e:
				await message.channel.send("Error: " + str(e))

			await message.channel.send(file=discord.File(image_path))
			if os.path.exists(image_path):
  				os.remove(image_path)

		else:
			await message.channel.send("Error: Can only saturate images (jpeg or png)")

class BlurCommand(ImageChannelCommand):
	def __init__(self):
		Command.__init__(self)
		self.keyword = "blur"
		self.args = [CommandArgument("radius", "")]
		self.desc = "Apply gaussian blur with a specified radius"

	async def execute(self, args, message, context):
		status = await self.pre_execute(args, message)
		if status:
			return

		radius = None
		try:
			radius = float(args[0])
		except Exception as e:
			await message.channel.send("Error: " + str(e))
			return

		if context.last_url.endswith(".jpg") or context.last_url.endswith(".jpeg") or context.last_url.endswith(".png"):
			image_path = await self.download_image(hash(message.channel), context)
			
			image = Image.open(image_path)
			image = image.convert("RGB")
			try:
				image2 = image.filter(ImageFilter.GaussianBlur(radius=radius))
				image2.save(image_path, "PNG")
			except Exception as e:
				await message.channel.send("Error: " + str(e))

			await message.channel.send(file=discord.File(image_path))
			if os.path.exists(image_path):
  				os.remove(image_path)

		else:
			await message.channel.send("Error: Can only blur images (jpeg or png)")