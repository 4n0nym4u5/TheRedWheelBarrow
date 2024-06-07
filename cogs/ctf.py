#!/usr/bin/python3

import random
from time import sleep
import os
import discord
from discord.ext import commands, tasks
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
import requests
import json
import string
from bs4 import BeautifulSoup
import lxml.html
from datetime import date, datetime
from time import strptime
from discord.ext.tasks import loop
import asyncio
import time
from datetime import date, datetime, timedelta
from time import strptime
from datetime import timezone
from datetime import datetime
from dateutil import tz
import sys
import traceback

sys.path.append("..")

class Ctfs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.group()
	async def ctf(self, ctx):
		if ctx.invoked_subcommand is None:
			# If the subcommand passed does not exist, its type is None
			ctf_commands = list(set([c.qualified_name for c in Ctfs.walk_commands(self)][1:]))
			await ctx.send(f"Current ctf commands are: {', '.join(ctf_commands)}") # update this to include params
	
	@ctf.command(name = "upcoming")
	async def upcoming(self, ctx, count=3):
		print("inside ctf upcoming")
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		r = requests.get("http://ctftime.org/", headers=headers)
		pd.set_option('max_colwidth',104)
		df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
		upcoming_ctfs = df_list[11]
		upcoming_ctfs.drop('Format', inplace=True, axis=1) 
		upcoming_ctfs.drop('Duration', inplace=True, axis=1) 
		# upcoming_ctfs = upcoming_ctfs.rename(columns=upcoming_ctfs.iloc[0]).drop(upcoming_ctfs.index[0])
		upcoming_ctfs = tabulate(upcoming_ctfs, showindex=False, headers="", tablefmt='plain')
		upcoming_ctfs = re.sub(r'[0-9]+ teams', '', upcoming_ctfs)
		upcoming_ctfs=upcoming_ctfs.replace("\n", "\n\n")
		print(upcoming_ctfs)
		await ctx.channel.send(f"""```{upcoming_ctfs}```""")
		print("done")

	@ctf.command(name = "create")
	@commands.has_role("root")
	async def create_func(self, ctx, ctf_name):
		ctf_name = strip_fuck_names(ctf_name)
		print("inside ctf create")
		perm = discord.Permissions(use_voice_activation = True, add_reactions = True, stream = True, read_messages = True, send_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, connect = True, speak = True)
		ctf_role = discord.utils.get(ctx.guild.roles, name = ctf_name)
		if not ctf_role:
			await ctx.channel.send(f"Do `>ctf create {ctf_name}` first")
			return
		overwrites = {
			discord.utils.get(ctx.guild.roles, name = ctf_name) : discord.PermissionOverwrite(use_voice_activation = True, add_reactions = True, stream = True, read_messages = True, send_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, connect = True, speak = True),
			ctx.guild.default_role : discord.PermissionOverwrite(read_messages = False, send_messages = False, read_message_history = False)
		}
		category = await ctx.guild.create_category(name = ctf_name, overwrites = overwrites, position = 1)
		guild = ctx.guild
		channel = discord.utils.get(guild.channels, name="ctfhall")
		ctf_msg = await channel.send("@here Looks like we will be playing `{}` join the ctf by `!ctf join {}` ".format(ctf_name, ctf_name))
		emoji = discord.utils.get(ctx.guild.emojis, name='tick')
		await ctf_msg.add_reaction(emoji)
		print("create done")
		await ctx.guild.create_voice_channel("pawry1", category=category)
		await ctx.guild.create_voice_channel("pawry2", category=category)
		await ctx.guild.create_voice_channel("pawry3", category=category)
		ctf_channel_null_bot = discord.utils.get(ctx.guild.channels, name=ctf_name)
		print(ctf_channel_null_bot)
		await ctf_channel_null_bot.edit(category=category, sync_permissions=True)

	
	@ctf.command(name = "join")
	async def join_func(self, ctx, ctf_name):
		print("join start")
		ctf_name = strip_fuck_names(ctf_name)
		ctf_role = discord.utils.get(ctx.guild.roles, name = ctf_name)
		channel = discord.utils.get(ctx.guild.channels, name=ctf_name)
		msg = await ctx.message.author.add_roles(ctf_role)
		emoji = discord.utils.get(ctx.guild.emojis, name='tick')
		await ctx.message.add_reaction(emoji)
		msg = await channel.send(f"{ctx.message.author.mention} has joined the pawry")
		await msg.add_reaction(emoji)


	@ctf.command(name = "leave")
	async def leave_func(self, ctx, ctf_name):
		print("leave start")
		ctf_name = strip_fuck_names(ctf_name)
		ctf_role = discord.utils.get(ctx.guild.roles, name = ctf_name)
		msg = await ctx.message.author.remove_roles(ctf_role)
		emoji = discord.utils.get(ctx.guild.emojis, name='tick')
		await ctx.message.add_reaction(emoji)
		ctf_category = discord.utils.get(ctx.guild.categories, name=ctf_name)
		for challs in ctf_category.channels:
			try:
				role = discord.utils.get(ctx.guild.roles, name = str(challs))
				await ctx.message.author.remove_roles(role)
			except:
				pass
		channel = discord.utils.get(ctx.guild.channels, name=ctf_name)
		await channel.send(f"{ctx.message.author.mention} left (╯°□°）╯︵ ┻━┻")

	@ctf.command(name="attempt")
	async def attempt_func(self, ctx, chall_name):
		await ctx.channel.send("nice attempt use threads instead xD [!ctf attempt has been deprecated]")
		"""
		attempt = False
		print(chall_name)
		channel_name = str(ctx.message.channel.name)
		categories = ctx.guild.categories
		for category in categories:
			if category.name == channel_name:
				attempt = True
				break
			else:
				pass
		if attempt:
			chall_name = strip_fuck_names(chall_name)
			print(chall_name)
			print("attempt")
			ctf_name = str(ctx.message.channel.name)
			perm = discord.Permissions(use_voice_activation = True, add_reactions = True, stream = True, read_messages = True, send_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, connect = True, speak = True)
			guild = ctx.guild
			emoji = discord.utils.get(ctx.guild.emojis, name='tick')
			existing_channel = discord.utils.get(guild.channels, name=chall_name)
			if not existing_channel:
				print("non existing")
				chall_name = strip_fuck_names(chall_name)
				await ctx.guild.create_role(name = chall_name, permissions = perm)

				overwrites = {
				discord.utils.get(ctx.guild.roles, name = chall_name) : discord.PermissionOverwrite(use_voice_activation = True, add_reactions = True, stream = True, read_messages = True, send_messages = True, embed_links = True, attach_files = True, read_message_history = True, mention_everyone = True, external_emojis = True, connect = True, speak = True),
				ctx.guild.default_role : discord.PermissionOverwrite(read_messages = False, send_messages = False, read_message_history = False)
				}
				category = discord.utils.get(ctx.guild.categories, name=ctf_name)
				print(f'Creating a new channel: {chall_name}')
				print(category)
				await guild.create_text_channel(chall_name, category=category, overwrites = overwrites)
				print("created text channel")
				role = discord.utils.get(ctx.guild.roles, name = chall_name)
				print(role)
				await ctx.message.author.add_roles(role)
				msg = await ctx.send("`{}` has been added to the db".format(chall_name))
				await ctx.message.add_reaction(emoji)
				await asyncio.sleep(1)
				channel = discord.utils.get(guild.channels, name=chall_name)
				msg = await channel.send(f"{ctx.message.author.mention} has attempted to solve the challenge")
				await msg.add_reaction(emoji)

			else:
				print("existing")
				role = discord.utils.get(ctx.guild.roles, name = chall_name)
				await ctx.message.author.add_roles(role)
				await asyncio.sleep(1)
				msg = await existing_channel.send(f"{ctx.message.author.mention} has attempted to solve the challenge")
				await ctx.message.add_reaction(emoji)
				await msg.add_reaction(emoji)
		else:
			print("else fucked")
			await ctx.channel.send("Mr.{} does this channel seem to be a ctf channel to you".format(ctx.message.author.mention))

	@ctf.command(name='solved')
	async def solved_func(self, ctx, chall_name = None):
		solved = True
		if chall_name == None:
			chall_name = str(ctx.message.channel.name)
		else:
			chall_name = str(strip_fuck_names(chall_name))

		role = discord.utils.get(ctx.guild.roles, name = chall_name)
		if not role:
			print("fail one")
			solved = False
		else:
			user_roles = ctx.message.author.roles
			categories = ctx.guild.categories
			for category in categories:
				if category.name == chall_name:
					solved = False
					break
				else:
					pass
			if solved:
				for roles in user_roles:
					if roles.name == chall_name:
						solved = True
						break
					else:
						print("fail two")
						solved = False
		if solved:
			print("checks passed")
			user_roles = ctx.message.author.roles
			guild = ctx.guild
			user = ctx.message.author
			channel = discord.utils.get(guild.channels, name=chall_name)
			print(channel.id)
			
			role = discord.utils.get(ctx.guild.roles, name = chall_name)
			print("solved done")
			if "--freeze" in ctx.message.content:
				await channel.send("@here `{}` has been solved :]".format(chall_name))
				user = ctx.message.author
				chall_name = str(ctx.message.channel.name)
				role_name = chall_name
				guild = ctx.guild
				chan = discord.utils.get(guild.channels, name = chall_name)
				role = discord.utils.get(ctx.guild.roles, name = role_name)
				new_name = "solved_" + str(chall_name)
				await channel.edit(name=new_name)
				await ctx.channel.send("This channel has been freezed... ")
				await chan.set_permissions(role, send_messages = False)
				await chan.set_permissions(role, read_messages = True)
				await chan.set_permissions(role, read_message_history = True)
			else:
				await channel.delete()
				await role.delete()
		else:
			emoji = discord.utils.get(ctx.guild.emojis, name='fuck_you')
			await ctx.channel.send("Kernel panic")
			time.sleep(1)
			await ctx.channel.send("Rebooting....")
			await ctx.channel.send("Failed to start")
			time.sleep(2)
			await ctx.channel.send(emoji)
"""

	@ctf.command(name = 'note')
	async def note_func(self, ctx, *msg):
		note = False
		print("notes")
		chall_name = str(ctx.message.channel.name)
		guild = ctx.guild
		user = ctx.message.author
		channel = discord.utils.get(guild.channels, name=chall_name)
		#msg = ctx.message.content
		print(msg)
		#msg=msg[10:]
		print(msg)
		pins = await ctx.message.channel.pins()
		print(pins)
		if len(pins) == 0:
			note = True
		else:
			print("in else")
			for msgs in pins:
				try:
					embed = msgs.embeds[0]
					desc = embed.description
					print(desc)
					junk = msg
					junk = "```" + junk + "```"
					if junk == desc:
						print("in else -> if")
						await ctx.channel.send("This has already been pinned")
						note = False
						break
					else:
						note = True
				except:
					pass
		if note:
			if "```" in msg:
				embed = discord.Embed(title=f"Note on {str(chall_name)} by {str(user)}", description=f"{msg}", color=15874645)
			else:
				embed = discord.Embed(title=f"Note on {str(chall_name)} by {str(user)}", description=f"```{msg}```", color=15874645)
			note = await ctx.channel.send(embed=embed)
			await ctx.message.delete()
			await note.pin()

	@ctf.command(name = "setcreds")
	@commands.has_role("root")
	async def setcreds_func(self, ctx, username, password):
		if password == "random":
			password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
		await ctx.channel.send(f"```random password := {password}```")
		ctf_name = str(ctx.message.channel.name)
		msg = ctx.message.content
		emoji = discord.utils.get(ctx.guild.emojis, name='tick')
		await ctx.message.add_reaction(emoji)
		pins = await ctx.message.channel.pins()
		if len(pins) == 0:
			msg = msg.split(" ")
			print(msg)
			embed = discord.Embed(title=f"{str(ctf_name)} Credentials", description=f"```CSS\nUsername : {str(username)}\nPassword : {str(password)}```", color=3066993)
			creds_msg = await ctx.channel.send(embed=embed)
			await creds_msg.pin()
		else:
			for creds in pins:
				try:
					embed = creds.embeds[0]
					title = embed.title
					if "Credentials" in title:
						await creds.unpin()
				except:
					pass
			msg = msg.split(" ")
			print(msg)
			embed = discord.Embed(title=f"{str(ctf_name)} Credentials", description=f"```CSS\nUsername : {str(username)}\nPassword : {str(password)}```", color=3066993)
			creds_msg = await ctx.channel.send(embed=embed)
			await creds_msg.pin()

	@ctf.command(name="event")
	async def event_func(self, ctx, ctftime_url, what=None):
		ctf_name, ctftime_url, ctf_url, logo, start_time, end_time, onsite_online, format_type, discord_invite, weight, ctf_start_time, ctf_end_time, description, duration_day, duration_time = get_info(ctftime_url)
		print("aaaa")

		embed=discord.Embed(title=f"{ctf_name} Info", url=f"{ctftime_url}", description="", color=0x00ff40)
		embed.set_thumbnail(url=f"{logo}")
		embed.add_field(name="CTF ", value=f"{ctf_url}", inline=True)
		embed.add_field(name="Discord", value=f"{discord_invite}", inline=True)
		embed.add_field(name="Onsite", value=f"{onsite_online}", inline=True)
		embed.add_field(name="Weight", value=f"{weight}", inline=True)
		embed.add_field(name="Format", value=f"{format_type}", inline=True)
		embed.add_field(name="Start Time (IST)", value=f"{start_time}", inline=True)
		embed.add_field(name="End Time (IST)", value=f"{end_time}", inline=True)
		embed.add_field(name="Duration", value=f"{duration_day} days {duration_time} hours", inline=True)
		if len(description) >= 1000:
			pass
		else:
			embed.add_field(name="Description", value=f"{description}", inline=False)
	
		embed.set_footer(text="Happy Hacking")
		info_msg = await ctx.channel.send(embed=embed)
		await ctx.message.delete()
		if what == "--pin":
			await info_msg.pin()
			print("creating reminder")
	
			self.bot.loop.create_task(countdown_start(self, ctx, ctf_name, start_time, end_time))
			print("done creating countdown_start")
#			self.bot.loop.create_task(countdown_stop(self, ctx, ctf_name, end_time))
			print("done creating countdown_stop")
		elif what == "--countdown":
			now = datetime.now()
			countdown_time = start_time
			current_timestamp = datetime.timestamp(now)
			countdown_time = str(countdown_time)
			my_date = datetime.strptime(countdown_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=8, minutes=0)#  - timedelta(hours=2, minutes=30)
			my_timestamp = datetime.timestamp(my_date)
			time_left = my_timestamp - current_timestamp
			countdown_time = display_time(int(time_left))
			print(countdown_time)
			print(current_timestamp)
			print(my_timestamp)
			embed=discord.Embed(title=f"{ctf_name} will start in ", description=str(countdown_time), color=0x00ff40)
			msg = await ctx.channel.send(embed=embed)
		else:
			pass

	@ctf.command(name='show')
	async def show_func(self, ctx, what):
		print("show")
		what = ctx.message.content[10:]
		emoji = discord.utils.get(ctx.guild.emojis, name='tick')
		await ctx.message.add_reaction(emoji)
		print(what)
		if what == "creds" or what == "credentials":
			print("creds")
			ctf_name = str(ctx.message.channel.name)
			msg = ctx.message.content
			pins = await ctx.message.channel.pins()
			for creds in pins:
				try:
					embed = creds.embeds[0]
					title = embed.title
					if "Credentials" in title:
						await ctx.channel.send(embed=embed)
					else:
						pass
				except:
					pass

		elif what == "note" or what == "notes" :
			print("note")
			chall_name = str(ctx.message.channel.name)
			guild = ctx.guild
			user = ctx.message.author
			channel = discord.utils.get(guild.channels, name=chall_name)
			msg = ctx.message.content
			pins = await ctx.message.channel.pins()
			for note in pins:
				try:
					embedFromMessage = note.embeds[0]
					await ctx.channel.send(embed=embedFromMessage)
				except:
					await ctx.channel.send(note)

		elif what == "info" or what == "event" :
			print("event")
			pins = await ctx.message.channel.pins()
			for note in pins:
				try:
					embed = note.embeds[0]
					title = embed.title
					if "Info" in title:
						await ctx.channel.send(embed=embed)
					else:
						pass
				except:
					pass
		elif what == "challs" or "challenge" or "challenges" :
			print("show challs")
			category = discord.utils.get(ctx.guild.categories, name = ctx.message.channel.name)
			print(category)
			chall_channels = []
			for challs in category.channels:
				chall_channels.append(challs.name)
			chall_channels = "\n".join(chall_channels)
			embed=discord.Embed(title=f"Current {ctx.message.channel.name} challenges", description = f"{chall_channels}", color = 1752220)
			await ctx.channel.send(embed=embed)
			

	
	#deletes all roles and channels from the server so stay away im saying this to the fucker who took my script
	# @ctf.command(name='destroy')
	# async def creds(self, ctx):
	# 	for role in ctx.guild.roles:
	# 		try:
	# 			await role.delete()
	# 		except:
	# 			pass
	# 		#await role.delete()
	# 	for challs in ctx.guild.channels:
	# 		await challs.delete()

	@ctf.command(pass_context = True , aliases=['stats'])
	async def stat(self, ctx, ctf_name=None):
		print("inside stats")
		if ctf_name == None:
			ctf_name = ctx.message.channel.name
		print(ctf_name)
		guild=ctx.message.guild
		ctf_name = strip_fuck_names(ctf_name)
		ctf_channel = discord.utils.get(ctx.guild.channels, name = ctf_name)
		ctf_category = discord.utils.get(ctx.guild.categories, name = ctf_name)
		CTF_ROLES = {"Reversing":0, "Web":0, "Cryptography":0, "Pwn":0, "OSINT":0, "Forensics":0}
		role = discord.utils.get(ctx.guild.roles, name = ctf_name)
		all_members = ctx.guild.members
		#print(all_members)
		if role is None:
			await ctx.channel.send(f'There is no {role.name} CTF on this server or you are just being stupid!')
			return
		empty = True
		players = []
		for member in ctx.guild.members:
			if role in member.roles:
				players.append(member)
				empty = False
		#if empty:
		#	await ctx.channel.send("Nobody has the role {}".format(role.mention))
		for player_roles in CTF_ROLES.keys():
			role = discord.utils.get(ctx.guild.roles, name=player_roles)
			for kek in role.members:
				count=0
				if kek in players:
					CTF_ROLES[role.name]=CTF_ROLES[role.name]+1
					count+=1
				else:
					pass
		junk = ""
		for k, v in CTF_ROLES.items():
			junk += k.upper() + ' : ' + str(v) + '\n'

		print(junk)
		embed=discord.Embed(title=f"{ctf_name.upper()} STATS", description = f"""{junk}""", color = 1752220)
		await ctx.channel.send(embed=embed)
		print("done")

	@commands.has_role("root")
	@ctf.command(name = 'end')
	async def end_func(self, ctx):
		ctf_name = ctx.message.channel.name
		ctf_channel = discord.utils.get(ctx.guild.channels, name = ctf_name)
		ctf_category = discord.utils.get(ctx.guild.categories, name = ctf_name)
		print(ctf_name)
		print(ctf_channel)
		print(ctf_category)
		past_category = discord.utils.get(ctx.guild.categories, name = "past-ctfs-2")
		#await ctf_channel.edit(category=past_category)
		for challs in ctf_category.channels:
			try:
				print(challs)
				if challs == ctx.message.channel:
					print("main room channel")
					role = discord.utils.get(ctx.guild.roles, name = str(challs))
					await role.delete()
				else:
					print("challs : ")
					print(challs)
					role = discord.utils.get(ctx.guild.roles, name = str(challs))
					print("role : ")
					print(role)
					await challs.delete()
					await role.delete()
			except:
				pass
		await ctf_category.delete()
		await asyncio.sleep(1)
		ctf_channel = discord.utils.get(ctx.guild.channels, name = ctf_name)
		await ctf_channel.edit(category=past_category, sync_permissions=True)

"""async def countdown_start(ctx, ctf_name, countdown_time):
	print("inside countdown start")
	now = datetime.now()
	current_timestamp = datetime.timestamp(now)
	countdown_time = str(countdown_time)
	my_date = datetime.strptime(countdown_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=8, minutes=0)
	my_timestamp = datetime.timestamp(my_date)
	time_left = my_timestamp - current_timestamp

	countdown_time = display_time(int(time_left))
	print(countdown_time)
	print(current_timestamp)
	print(my_timestamp)
	embed=discord.Embed(title=f"{ctf_name} will start in ", description=str(countdown_time), color=0x00ff40)
	msg = await ctx.channel.send(embed=embed)
	await msg.pin()
	time_left = int(time_left)
	while time_left >= 0:
		time_left = time_left - 1
		countdown_time = display_time(int(time_left))
		#print(time_left)
		new_embed=discord.Embed(title=f"{ctf_name} will start in ", description=str(countdown_time), color=0x00ff40)
		await asyncio.sleep(1)
		await msg.edit(embed=new_embed)
	await ctx.channel.send(f"@here `{ctf_name}` has been started good luck... :]")
	self.bot.loop.create_task(countdown_stop(ctx, ctf_name, end_time))"""

async def countdown_start(self, ctx, ctf_name, countdown_time, end_time):
	print("inside countdown start")
	now = datetime.now()
	current_timestamp = datetime.timestamp(now)
	popo = countdown_time
	countdown_time = str(countdown_time)
	my_date = datetime.strptime(countdown_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=30)# - timedelta(hours=2, minutes=30)
	my_timestamp = datetime.timestamp(my_date)
	time_left = my_timestamp - current_timestamp
	junk = display_time(int(time_left))
	embed=discord.Embed(title=f"{ctf_name} will start in ", description=str(junk), color=0x00ff40)
	msg = await ctx.channel.send(embed=embed)
	print("countdown_time : ")
	print(countdown_time)
	await msg.pin()
	olkudi = 0
	while time_left >= 0:
		now = datetime.now()
		current_timestamp = datetime.timestamp(now)
		my_date = datetime.strptime(countdown_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=30)
		my_timestamp = datetime.timestamp(my_date)
		time_left = my_timestamp - current_timestamp
		junk = display_time(int(time_left))
		new_embed=discord.Embed(title=f"{ctf_name} will start in ", description=str(junk), color=0x00ff40)
		await msg.edit(embed=new_embed)
		if time_left <= 0:
			print("done")
			await msg.delete()
			await ctx.channel.send(f"@here `{ctf_name}` has been started good luck... :]")
			self.bot.loop.create_task(countdown_stop(ctx, ctf_name, end_time))
			break
		elif time_left <= 900 and olkudi != 1:
			print("15 mins left")
			await ctx.channel.send(f"@here 15 more minutes left for `{ctf_name}` to start _UwU_ ...")
			olkudi = 1
	#await ctx.channel.send(f"@here `{ctf_name}` has been started good luck... :]")
	#self.bot.loop.create_task(countdown_stop(ctx, ctf_name, end_time))
"""
async def countdown_stop(ctx, ctf_name, countdown_time):
	print("inside countdown start")
	now = datetime.now()
	current_timestamp = datetime.timestamp(now)
	countdown_time = str(countdown_time)
	print(str(countdown_time))
	my_date = datetime.strptime(countdown_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=8, minutes=0)
	my_timestamp = datetime.timestamp(my_date)
	time_left = my_timestamp - current_timestamp

	countdown_time = display_time(int(time_left))
	embed=discord.Embed(title=f"{ctf_name} will end in ", description=str(countdown_time), color=0x00ff40)
	msg = await ctx.channel.send(embed=embed)
	await msg.pin()
	while time_left >= 0:
		time_left = time_left - 1
		countdown_time = display_time(int(time_left))
		#print(time_left)
		new_embed=discord.Embed(title=f"{ctf_name} will end in ", description=str(countdown_time), color=0x00ff40)
		await asyncio.sleep(1)
		await msg.edit(embed=new_embed)
	await ctx.channel.send(f"@here `{ctf_name}` has been ended nice play... :]")
"""
async def countdown_stop(ctx, ctf_name, countdown_time):
	print("inside countdown stop")
	now = datetime.now()
	current_timestamp = datetime.timestamp(now)
	countdown_time = str(countdown_time)
	my_date = datetime.strptime(countdown_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=30)
	my_timestamp = datetime.timestamp(my_date)
	time_left = my_timestamp - current_timestamp
	junk = display_time(int(time_left))
	embed=discord.Embed(title=f"{ctf_name} will end in ", description=str(junk), color=0x00ff40)
	msg = await ctx.channel.send(embed=embed)
	await msg.pin()
	flag = 0
	while time_left >= 0:
		now = datetime.now()
		current_timestamp = datetime.timestamp(now)
		countdown_time = str(countdown_time)
		my_date = datetime.strptime(countdown_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=5, minutes=30)# - timedelta(hours=2, minutes=30)
		my_timestamp = datetime.timestamp(my_date)
		time_left = my_timestamp - current_timestamp
		junk = display_time(int(time_left))
		new_embed=discord.Embed(title=f"{ctf_name} will end in ", description=str(junk), color=0x00ff40)
		await msg.edit(embed=new_embed)
		if time_left <= 0:
			break
		elif time_left <= 3600 and flag != 1:
			await ctx.channel.send(f"@here 1 hour left for `{ctf_name}` to end ... _Ara Ara_")
			flag = 1
	await ctx.channel.send(f"@here `{ctf_name}` has been ended... :]")
	await msg.delete()
	#await ctx.channel.send(f"Fuck u bitch the bot works :] (Read the fucking help menu)")

def display_time(seconds, granularity=4):
	intervals = (
		('weeks', 604800),  # 60 * 60 * 24 * 7
		('days', 86400),    # 60 * 60 * 24
		('hours', 3600),    # 60 * 60
		('minutes', 60),
		('seconds', 1),
		)
	result = []
	for name, count in intervals:
		value = seconds // count
		if value:
			seconds -= value * count
			if value == 1:
				name = name.rstrip('s')
			result.append("{} {}".format(value, name))
	return ', '.join(result[:granularity])

def utc_to_ist(date_time):
	# METHOD 1: Hardcode zones:
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('Asia/Kolkata')
	
	# METHOD 2: Auto-detect zones:
	from_zone = tz.tzutc()
	to_zone = tz.tzlocal()
	print("inside utc to ist")
	# utc = datetime.utcnow()
	utc = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S')
	
	# Tell the datetime object that it's in UTC time zone since 
	# datetime objects are 'naive' by default
	#utc = utc.replace(tzinfo=from_zone)
	#
	## Convert time zone
	#central = str(utc.astimezone(to_zone))
	#central = central.split('+')[0]
	#return central
	ist = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S') + timedelta(hours=8, minutes=0) - timedelta(hours=2, minutes=30)
	print(ist)
	return ist

def get_info(url):
	try:
		print(url)
		print("inside")
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
		s = requests.session()
		url = url.strip('https://ctftime.org/event/')
		ctftime_url = "https://ctftime.org/api/v1/events/" + str(url) + "/"
		event_code = url.split("/")
		print(event_code)
		r = s.get(ctftime_url, headers=headers, timeout=5)
		print(ctftime_url)
		#print(r.text)
		troll_flag = re.findall(r"([a-fA-F\d]{32})", r.text)
		print(troll_flag)
		info = r.json()
		print(info)
		ctf_name = info['title']
		ctftime_url = info['ctftime_url']
		ctf_url = info['url']
		logo = info['logo']
		start_time = info['start']
		start_time = start_time.split("+")[0]
	
		date_ = start_time.split("T")[0]
		time_ = start_time.split("T")[1]
		
		print(date_)
		print(time_)
		
		date_time = date_ + " " + time_
		start_time = utc_to_ist(date_time)
		
		print(start_time)
	
		end_time = info['finish']
		end_time = end_time.split("+")[0]
		
		date_ = end_time.split("T")[0]
		time_ = end_time.split("T")[1]
		
		print(date_)
		print(time_)
		
		date_time = date_ + " " + time_
		end_time = utc_to_ist(date_time)
		print("end time")
		print(end_time)
	
		onsite_online = info['onsite']
	
		format_type = info['format']
		print(format_type)
		try:
			if len(re.findall(r"\bhttps://discord.gg/\w+", r.text)) != 0:
				print("inside if")
				discord_invite = str(re.findall(r"\bhttps://discord.gg/\w+", r.text)[0])
			else:
				try:
					print("inside elif")
					r_ctf = s.get(ctf_url, headers=headers, timeout=5)
					print(r_ctf)
			
					discord_invite = str(re.findall(r"\bhttps://discord.gg/\w+", r_ctf.text)[0])
					print(discord_invite)
				except:
					discord_invite = "https://discord.gg/404_error"
		except:
			discord_invite = "https://discord.gg/404_error"
		print(discord_invite)
	
		weight = info['weight']
		print(weight)
		description = info['description']
		duration_day = info['duration']
		duration_day = duration_day['days']
	
		duration_time = info['duration']
		duration_time = duration_time['hours']
		print(ctf_name, ctftime_url, ctf_url, logo, start_time, end_time, onsite_online, format_type, discord_invite, weight, start_time, end_time, description, duration_day, duration_time)
		return ctf_name, ctftime_url, ctf_url, logo, start_time, end_time, onsite_online, format_type, discord_invite, weight, start_time, end_time, description, duration_day, duration_time
	except:
		pass


def strip_fuck_names(name):
	name = str(name)
	name = name.lower()
	name = name.replace(" ", "-")
	name = name.replace('"', "")
	name = name.replace("'", "")
	name = name.replace("/", "-")
	name = name.replace("\\", "-")
	print("NAME :  ")
	print(name)
	return name

def setup(bot):
	bot.add_cog(Ctfs(bot))
