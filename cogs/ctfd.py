#!/usr/bin/python3

import json
import ast
import pandas as pd
from time import sleep
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
import sys
import traceback
import subprocess
from tabulate import tabulate
from prettytable import PrettyTable
from texttable import Texttable


class CTFD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.username = "zh3r0"
        self.password = "ctfteam@zh3r0"
        self.api = "https://ctftime.org/"
        self.PAGE_COUNTER = 0


    @commands.group()
    async def ctfd(self, ctx):
        if ctx.invoked_subcommand is None:
            # If the subcommand passed does not exist, its type is None
            ctfd_commands = list(set([c.qualified_name for c in CTFD.walk_commands(self)][1:]))
            await ctx.send(f"Current ctfd commands are: {', '.join(ctfd_commands)}")

    @ctfd.command(name = "start")
    async def start(self, ctx, ctf_link):
        print("inside check_creds")
        channel = ctx.message.channel
        pins = await ctx.message.channel.pins()
        if len(pins) == 0:
            await  ctx.channel.send("Creds for the CTF has not been set. Set the creds with !ctf setcreds <username> <password>")
        else:
            for creds in pins:
                embed = creds.embeds[0]
                title = embed.title
                if "Credentials" in title:
                    desc = embed.description
                    desc = desc.split("\n")
                    print(desc)

                self.ctfd.username = desc[1].split(" : ")[1]
                self.ctfd.password = desc[2].split(" : ")[1]
                print(self.ctfd.username)
                print(self.ctfd.password)
        ctf_link = ctf_link.replace("/login", "")
        print(ctf_link)
        ctf_link = ctf_link[:(len(ctf_link) - 1)]
        print(ctf_link)
        self.ctfd.api = ctf_link + "/api/v1/"
        print(self.ctfd.api)
        whitelist = set(string.ascii_letters+string.digits+' '+'-'+'!'+'#'+'_'+'['+']'+'('+')'+'?'+'@'+'+'+'<'+'>')
        fingerprint = "Powered by CTFd"
        s = requests.session()
        
        if ctf_link[-1] == "/": ctf_link = ctf_link[:-1]
        r = s.get(f"{ctf_link}/login")
        if fingerprint not in r.text:
            await  ctx.channel.send("CTF is not based on CTFd :((")
        else:
            # Get the nonce from the login page.
            try:
                nonce = r.text.split("csrfNonce': \"")[1].split('"')[0]
            except: # sometimes errors happen here, my theory is that it is different versions of CTFd
                try:
                    nonce = r.text.split("name=\"nonce\" value=\"")[1].split('">')[0]
                except:
                    pass
            # Login with the username, password, and nonce
            r = s.post(f"{ctf_link}/login", data={"name": self.ctfd.username, "password": self.ctfd.password, "nonce": nonce})
            if "Your username or password is incorrect" in r.text:
                await  ctx.channel.send("Invalid login credentials ヽ(`Д´)ﾉ. Fuck you burd 凸-_-凸 ")
            else:
                await  ctx.channel.send(" The creds are correct :)) Good luck with the CTF. ")
        ctf_name = str(ctx.message.channel.name)
        category = discord.utils.get(ctx.guild.categories, name=ctf_name)
        scoreboard_channel = await ctx.guild.create_text_channel("scoreboard", category = category)
        r = s.get(self.ctfd.api + "scoreboard")
        dict_macha = json.loads(r.text)
        print(type(dict_macha))
        print(len(dict_macha['data']))
        print(dict_macha['data'][0]['pos'])
        lmao_op = []
        
        print(len(dict_macha['data']))
        NO_OF_PAGES = (len(dict_macha['data']) / 10)
        print(NO_OF_PAGES)
        for i in range(10):
            test = [dict_macha['data'][i]['pos'], dict_macha['data'][i]['name'], dict_macha['data'][i]['score']]
            lmao_op.append(test)
        final_scoreboard = str(tabulate(lmao_op, headers=["Rank", "Team name", "Score"], tablefmt="pretty"))
        scoreboard_msg = await scoreboard_channel.send(f"```{final_scoreboard}```")
        await scoreboard_msg.add_reaction("⬆")
        await scoreboard_msg.add_reaction("⬇")
        await scoreboard_msg.add_reaction("♻")
        print(scoreboard_msg.reactions)
        print("done stuff")
        def check(reaction, user):
            return str(reaction.emoji) == '♻' or str(reaction.emoji) == '⬆' or str(reaction.emoji) == '⬇' and user != self.bot.user

        async def get_to_first_page(s, final_scoreboard):
            print("inside get_to_first_page")
            print(self.PAGE_COUNTER)
            r = s.get(self.ctfd.api + "scoreboard")
            dict_macha = json.loads(r.text)
            print(type(dict_macha))
            print(len(dict_macha['data']))
            print(dict_macha['data'][0]['pos'])
            lmao_op = []        
        
            print(len(dict_macha['data']))
            NO_OF_PAGES = (len(dict_macha['data']) / 10)
            print(NO_OF_PAGES)
            try:
                for i in range(10):
                    test = [dict_macha['data'][i]['pos'], dict_macha['data'][i]['name'], dict_macha['data'][i]['score']]
                    lmao_op.append(test)
                    print(i)
            except:
                pass
            final_scoreboard = str(tabulate(lmao_op, headers=["Rank", "Team name", "Score"], tablefmt="pretty"))
            await scoreboard_msg.edit(content=f"```{final_scoreboard}```")
            self.PAGE_COUNTER = 1
            
        async def page_up_or_down(s, final_scoreboard):
            print(self.PAGE_COUNTER)
            print("inside page up")
            r = s.get(self.ctfd.api + "scoreboard")
            dict_macha = json.loads(r.text)
            # print(type(dict_macha))
            # print(len(dict_macha['data']))
            # print(dict_macha['data'][0]['pos'])
            lmao_op = []
            print(len(dict_macha['data']))
            if str(reaction.emoji) == '⬆':
                print(self.PAGE_COUNTER)
                self.PAGE_COUNTER += 1
                print("incremented")
                print(self.PAGE_COUNTER)
            elif str(reaction.emoji) == '⬇':
                self.PAGE_COUNTER -= 1
            else:
                print("lmao some error happened")
                print(reaction.emoji)
                print("is the imposter")
            NO_OF_PAGES = (len(dict_macha['data']) / 10)
            print(NO_OF_PAGES)
            try:
                for i in range(self.PAGE_COUNTER*10, (self.PAGE_COUNTER*10) + 10):
                    test = [dict_macha['data'][i]['pos'], dict_macha['data'][i]['name'], dict_macha['data'][i]['score']]
                    lmao_op.append(test)
                    # print(i)
            except:
                pass
            final_scoreboard = str(tabulate(lmao_op, headers=["Rank", "Team name", "Score"], tablefmt="pretty"))
            await scoreboard_msg.edit(content=f"```{final_scoreboard}```")
            
        option = ""
        while True:
            print("in while true")
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            print(reaction)
            if str(reaction.emoji) == '♻' and user != self.bot.user:
                await get_to_first_page(s, final_scoreboard)
            elif str(reaction.emoji) == '⬆' or str(reaction.emoji) == "⬇" and user != self.bot.user:
                await page_up_or_down(s, final_scoreboard)
def split(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]

def setup(bot):
    bot.add_cog(CTFD(bot))