#!/usr/bin/python3

import discord
from discord.ext import commands, tasks
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
import sys
import traceback
import subprocess
import hashlib
import os
import re
from time import sleep

class Pwn(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.group()
	async def pwn(self, ctx):
		if ctx.invoked_subcommand is None:
			# If the subcommand passed does not exist, its type is None
			pwn_commands = list(set([c.qualified_name for c in Pwn.walk_commands(self)][1:]))
			await ctx.send(f"Current pwn commands are: {', '.join(pwn_commands)}")

	@pwn.command(name = "syscall")
	async def get_sys_info(self, ctx, arch, syscall_num_name):
		print("inside syscalls")
		result = subprocess.check_output(['syscalls', arch, syscall_num_name])
		result = (result).decode('utf-8')
		if "Architecture not found" in result:
			embed = discord.Embed(title=f"HELP", description = "```Available architectures: ['arm', 'x86', 'armthumb', 'x64']\nUsage: !pwn syscalls <arch> <syscall name / syscall number>```", color=0x00FFFF, inline=False)
		else:
			embed=discord.Embed(title=f"{str(arch)} {str(syscall_num_name)} syscall", description="```{}```".format(result), color=0x00FFFF)
		await ctx.channel.send(embed=embed)

	@pwn.command(name = "magic")
	async def magic(self, ctx, md5_hash):
		print("inside get libc offset")
		libc_db_path = "/root/TheRedWheelBarrow/libc_db/db/"
		validHash = re.findall(r"([a-fA-F\d]{32})", md5_hash)	
		if validHash != []: 
		    pass
		else:
			embed=discord.Embed(title=f"Chutiya ¯\_ಠ_ಠ_/¯", description="```Not a valid MD5 hash```", color=0x00FFFF)
			await ctx.channel.send(embed=embed)
			return
		symbols = ["system", "__malloc_hook", "__free_hook", "stdout", "stdin", "_IO_2_1_stdin_", "_IO_wfile_overflow", "_IO_default_uflow", "_IO_file_xsputn", "_IO_file_jumps", "binsh", "main_arena"]
		msgs = "# symbols\n"
		found = False
		libc_hashes = os.listdir(libc_db_path)
		if md5_hash in libc_hashes:
			# found = True
			libc_file = libc_db_path + md5_hash
		else:
			# found = False
		# for file in os.listdir(libc_db_path):
		# 	md5_hash = file
		# 	file = libc_db_path + file
		# 	libc_md5 = subprocess.check_output(f"md5sum {file}| awk '{{print $1}}'", shell=True).strip(b"\n").decode('latin')
		# 	if libc_md5 == md5_hash:
		# 		libc_file = file
		# 		# print(libc_file)
		# 		found = True
		# 		break 
		# if not found:
			embed=discord.Embed(title=f"Libc -> {md5_hash}", description="```libc not found in database```", color=0x00FFFF)
			await ctx.channel.send(embed=embed)
			return
		offsets_list = subprocess.check_output(f"magic {libc_file}", shell=True).split(b"\n")[:-1]
		# print(offsets_list)
		for i in range(len(offsets_list)):
			msgs += symbols[i] + " = 0x" + offsets_list[i].decode('latin') + "\n"
		f=open(libc_file, "rb")
		f.seek(4, 1)
		bit_set = f.read(1)
		# print(bit_set)
		msgs += "# ROP gadgets\n"
		gadgets_x64 = ["pop_rax", "pop_rbx", "pop_rcx", "pop_rdx", "pop_rdi", "pop_rsi", "pop_rbp", "leave_ret", "ret", "syscall"]
		gadgets_x32 = ["pop_eax", "pop_ebx", "pop_ecx", "pop_edx", "pop_edi", "pop_esi", "pop_ebp", "leave_ret", "ret", "syscall"]
		if bit_set == b'\x02':
			rop_gadgets_x64 = subprocess.check_output(f"magic_rop_x64 {libc_file}", shell=True).replace(b":", b"").split(b"\n")
			# print(rop_gadgets_x64)
			for i in range(len(gadgets_x64)):
				msgs += gadgets_x64[i] + " = " + rop_gadgets_x64[i].decode('latin') + "\n"
		else:
			rop_gadgets_x32 = subprocess.check_output(f"magic_rop_x32 {libc_file}", shell=True).replace(b":", b"").split(b"\n")
			# print(rop_gadgets_x32)
			# sleep(5)
			for i in range(len(gadgets_x32)):
				print(rop_gadgets_x32[i])
				msgs += gadgets_x32[i] + " = " + rop_gadgets_x32[i].decode('latin') + "\n"
		one_gadgets = oneshot(libc_file)
		print(one_gadgets)
		msgs += "# One gadgets\n"
		msgs += "onegadget = " + str(one_gadgets) + '\n"""\n'
		msgs += subprocess.check_output(f"one_gadget -f -l 1 {libc_file}", shell=True).decode('latin') + '"""'
		embed=discord.Embed(title=f"Libc -> {md5_hash}", description=f"```{msgs}```", color=0x00FFFF)
		await ctx.channel.send(embed=embed)

def oneshot(libc, libc_base=0x0, log=False):
    return [hex(int(i)) for i in subprocess.check_output(['one_gadget', '-l', '1', '--base', str(libc_base), '--raw', libc]).decode().split(' ') ]

def setup(bot):
	bot.add_cog(Pwn(bot))
