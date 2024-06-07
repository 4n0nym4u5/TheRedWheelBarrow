#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from time import sleep
import re
import urllib.parse


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.group()
	async def music(self, ctx):
		if ctx.invoked_subcommand is None:
			# If the subcommand passed does not exist, its type is None
			music_commands = list(set([c.qualified_name for c in Music.walk_commands(self)][1:]))
			await ctx.send(f"Current music commands are: {', '.join(music_commands)}")

	@music.command(name='download')
	async def download(self, ctx, link):
		print("in music")
		# thumbnail = <meta property="og:image" content="https://i.ytimg.com/vi/gXH7_XaGuPc/hqdefault.jpg" />
		# download_url = https://320ytmp3.com/en16/download?type=ytmp3&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DW7yCoQ7YV9E
		if "youtube" not in link:
			await ctx.channel.send("only youtube support integrated currently")
		if "m.youtube" in link:
			link = link.replace("m.youtube", "www.youtube")
		s = requests.Session()
		s.headers.update({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36'})

		link = "https://320ytmp3.com/en16/download?type=ytmp3&url=" + urllib.parse.quote(link)
		r=s.get(link)
		soup = BeautifulSoup(r.content, 'html.parser')

		url = re.findall(r'action=[\'"]?([^\'" >]+)', r)
		await ctx.channel.send(url)
		print("done music")

