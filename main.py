# imports
from ast import Load
import glob
import imghdr
import os
import keep_alive
from platform import win32_edition
from pydoc import describe
import random
import json
from unicodedata import name
from warnings import warn_explicit
import aiohttp
import requests
import string
import asyncio
from asyncio import sleep
import time
import datetime
from datetime import timedelta
import lists
import disnake as discord
from disnake.ext import commands
from disnake.errors import Forbidden
import os.path
import json
import random
from random import choice
import sqlite3
from random import randint
from disnake.ui import View


determine_flip = [1, 0]




# CONFIG
bot = commands.Bot(command_prefix='/',intents = discord.Intents.all())
bot.remove_command('help')



# events
@bot.event
async def on_ready():
    activity = discord.Streaming(
        name=
        f"Protecting {len(bot.guilds)} server(s)|User(s):{len(bot.users)}!",
        url = "https://www.twitch.tv/404",type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    bot.remove_command('help')
    print("Zenite Protect protected!")




connection = sqlite3.connect('main.sqlite')
cursor = connection.cursor()
lconnection = sqlite3.connect('leave.sqlite')
lcursor = lconnection.cursor()
lgconnection = sqlite3.connect('logs.sqlite')
lgcursor = lgconnection.cursor()
connection = sqlite3.connect('database.sqlite')
cursor = connection.cursor()
data = sqlite3.connect('data.sqlite3', timeout=1)
cursor = data.cursor()
connection = sqlite3.connect('database.sqlite')
cursor = connection.cursor()
lcursor.execute("CREATE TABLE IF NOT EXISTS leave (guild_id INT,channel_id INT,msg TEXT)")
lconnection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS main (guild_id INT,channel_id INT,msg TEXTurl TEXT)")
connection.commit()
lgcursor.execute("""CREATE TABLE IF NOT EXISTS logs (guild_id INT,channel_id INT)""")
lgconnection.commit()





@bot.event
async def on_guild_remove(guild):
    activity = discord.Streaming(
        name=
        f"Protecting {len(bot.guilds)} server(s)|User(s):{len(bot.users)}!",
        url = "https://www.twitch.tv/404",type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)


@bot.event
async def on_guild_role_update(before, after):
    global rlid
    global prms
    global oldprms
    global gld


# system


# Moderation


@bot.slash_command(description="Clear up to 1000 messages")
async def clear( ctx, amount:int = None):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.message.add_reaction("<:NO:934789609932611594>")
        Embed = discord.Embed(title='<:NO:934789609932611594>|Error!', description = 'You do not have the required rights :(', color=discord.Color.red())
        await ctx.response.send_message(embed = Embed)
        return
    if not amount:
        Embed = discord.Embed(title='<:NO:934789609932611594>|Error!', description = 'No number of messages specified :(', color=0x30d5c8)
        await ctx.response.send_message(embed = Embed)
        return
    if amount<1 or amount > 1000:
        Embed = discord.Embed(title='<:NO:934789609932611594>|Error!', description ='Maximum 1000,Minimum 1', color=discord.Color.red())
        await ctx.response.send_message(embed=Embed)
        return
    else:
        x = await ctx.channel.purge(limit=amount)
        Embed = discord.Embed(title='Cleared', description =f'Cleared {len(x)} messages from {amount} specified,enjoy :)', color=discord.Color.green())
        await ctx.response.send_message(embed=Embed)

# Mute and unmute comands




@bot.slash_command(description="Kick user from server")
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason='you broke the rules'):
    print( 'someone used a kick command!' )

    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} was kicked ')



@bot.slash_command(description="Ban user on the server")
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, args):
    await member.ban(reason=args)
    await ctx.send(f'{ctx.author.mention} ban {member.mention} because of "{args}"')
    print('someone used a ban command!')



@bot.slash_command(description="Unban user on the server")
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    print( 'someone used a unban command!' )
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        await ctx.send(f'{user.mention} unban {ctx.author.mention}')
        return


@bot.slash_command(description='Mass ban of several users (must be specified with a space and ID (not ping))')
async def massban(ctx, lists):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.response.send_message(embed=discord.Embed(title=':x:|Error', description='no permissions to run the command', color=discord.Color.red()), ephemeral=True)    
    else:
        await ctx.response.send_message('starting a ban')
        a = lists.split(' ')
        c = 0
        d = 0
        for b in a:
            try:
                user = await bot.fetch_user(b)
            except:
                d += 1
                continue
            if user in ctx.guild.members:
                member = await ctx.guild.fetch_member(b)
                await member.ban()
                c+=1
            else:
                await ctx.guild.ban(user)
                c+=1
        await ctx.send(embed=discord.Embed(title=f'Banned {c} users/ Not banned {d} users',description='If you didn’t ban who you need, try specifying all users separated by a space', color=discord.Color.green()))


# anti crash system

@bot.slash_command(description="Delete spam role without @")
async def delspamroles(ctx, name):
    if ctx.author.guild_permissions.manage_roles:
        await ctx.response.send_message(f'Start removing spam roles with name **{name}**', ephemeral=True)
        length = 0
        l = 0
        for role in ctx.guild.roles:
            if role.name == name:
                length +=1
                l +=1
        msg = await ctx.channel.send(embed=discord.Embed(title='🕐|Delete spam roles', description='Left: ...', color=discord.Color.green()))
        if length == 0:
            await msg.edit(embed=discord.Embed(title='❌|Delete spam roles', description=f'Roles with this name were not found\n Requested: {ctx.author.mention}', color=discord.Color.red()))
        else:
            for role in ctx.guild.roles:
                if role.name == name:
                    await role.delete()
                    length -= 1
                    await msg.edit(embed=discord.Embed(title='🕐|Delete spam roles', description=f'Left: {length}\n Requested: {ctx.author.mention}', color=discord.Color.green()))
            await msg.edit(embed=discord.Embed(title='✅|Delete spam roles', description=f'Removed {l} roles\n Requested: {ctx.author.mention}', color=discord.Color.green()))
    else:
        await ctx.response_send_message('You do not have `manage roles` rights', ephemeral=True)


@bot.slash_command(description="Remove spam channels by writing the channel itself without #")
async def delspamchannels(ctx, name):
    if ctx.author.guild_permissions.manage_channels:
        await ctx.response.send_message(f'Start deleting channels with a name **{name}**', ephemeral=True)
        length = 0
        l = 0
        for channel2 in ctx.guild.channels:
            if channel2.name == name:
                if channel2.id != ctx.channel.id:
                    length +=1
                    l +=1
        msg = await ctx.channel.send(embed=discord.Embed(title='🕐|Removing spam channels', description='Left: ...', color=discord.Color.green()))
        if length == 0:
            await msg.edit(embed=discord.Embed(title='❌|Removing spam channels', description=f'No channels found with this name\n Requested: {ctx.author.mention}', color=discord.Color.red()))
        else:
            for channel1 in ctx.guild.channels:
                if channel1.name == name:
                    if channel1.id != ctx.channel.id:
                        await channel1.delete()
                        length -= 1
                        await msg.edit(embed=discord.Embed(title='🕐|Removing spam channels', description=f'Left: {length}\n Requested: {ctx.author.mention}', color=discord.Color.green()))
            await msg.edit(embed=discord.Embed(title='✅|Removing spam channels', description=f'Deleted {l} channels\n Requested: {ctx.author.mention}', color=discord.Color.green()))
    else:
        await ctx.response_send_message('You do not have `manage channels` rights', ephemeral=True)

@bot.slash_command(description='Ban all crashers from the bot blacklist')
async def bancrashers(ctx):
    if ctx.author.id not in lists.blacklist:
        if not ctx.author.guild_permissions.ban_members:
            return await ctx.response.send_message(embed=discord.Embed(title=':x:|Error!', description='You do not have the required rights :(', color=discord.Color.red()), ephemeral=True)
        else:
            await ctx.response.send_message('Starting of the ban.....',  ephemeral=True)
            l = ""
            for crasher in lists.crashers:
                user = await bot.fetch_user(crasher)
                l += "`" + user.name + "#" + user.discriminator + "`" + "\n"
                await ctx.guild.ban(user)
            embed=discord.Embed(title='Banned', description=f'Successfully banned **{len(lists.crashers)}** crashers:\n{l}', color=discord.Color.green())
            embed.set_footer(text=f'Request from {ctx.author}')
            await ctx.channel.send(embed=embed)


# Events

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, no comand', colour = discord.Color.red()))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name}, no arg in command ', colour=discord.Color.orange()))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, You do not have sufficient rights to execute this command', colour = discord.Color.red()))




@bot.slash_command(description="Show server member avatar")
async def avatar(ctx, *,  member: discord.Member):
    if ctx.author.id not in lists.blacklist:
        embed = discord.Embed(description =  f"User avatar **`{member.name}`**", color = discord.Color.purple())
        embed.set_image(url = member.avatar)
        embed.set_footer(text=f'{member.name}', icon_url = member.avatar)
        await ctx.send(embed=embed)
        print('someone used a avatar command!')



@bot.event
async def on_message(message):
   if '@978362279131238440' in message.content:
      await message.channel.send(f"{message.author.mention} I work on slash commands prefixed with **`/`** ")
   else:
      await bot.process_commands(message)





@bot.slash_command(description="Remove mute (timeout) from user")
async def rmtimeout(ctx, member: discord.Member=None):
    if ctx.author.id not in lists.blacklist:
            print(f"rmtimeout, user: {ctx.author} ({ctx.author.id}), server: {ctx.guild}")	
            duration = timedelta(days = 0, hours = 0, minutes = 0, seconds = 0.000000000000000000000001)
            if not ctx.author.guild_permissions.manage_messages:
                Embed = discord.Embed(title='Error!', description = 'You do not have sufficient rights to execute this command :(', color=discord.Color.red())
                await ctx.response.send_message(embed = Embed)
                return
            if not member:
                Embed = discord.Embed(title='Error!', description = 'User not specified! Check if you have chosen correctly!', color=discord.Color.red())
                await ctx.response.send_message(embed = Embed)
                return
            if member == ctx.author:
                Embed = discord.Embed(title='Error!', description = 'Unknow Error! Try running the command again otherwise contact the developers for help', color=discord.Color.red())
                await ctx.response.send_message(embed=Embed)
                return
            if member.top_role >= ctx.author.top_role:
                Embed = discord.Embed(title='Error!', description = 'The bot role or your role does not allow you to remove the timeout from this member :(', color=discord.Color.red())
                await ctx.response.send_message(embed=Embed)
                return

            try:
                owner = ctx.guild.owner

                await member.timeout(duration=duration, reason=None)

                embed = discord.Embed(title='Succesfully!', description=f'Timeout removed by user:{ctx.author.mention}\nTimeout removed from user: {member.mention}', color=discord.Color.green())
                await ctx.response.send_message(embed=embed)

                embed = discord.Embed(title=f'Timeout has been removed from you for {ctx.guild.name} server', description=f'Timeout removed by user:{ctx.author.mention}', color=0xffff00)
                await member.send(embed=embed)

                embed = discord.Embed(title='The timeout has been removed from the user', description=f'Timeout removed by user:{ctx.author.mention}\nTimeout removed from user: {member.mention}', color=discord.Color.green())
                await owner.send(embed=embed)




            except discord.Forbidden:
                return

            except discord.HTTPException:
                return



@bot.slash_command(description="Mute (timeout) user")
@commands.has_permissions(administrator=True)
async def timeout(ctx, member: discord.Member=None, days:int=0,hours:int=0,minutes:int=0, seconds:int=0, reason=0):
    if ctx.author.id not in lists.blacklist:
            print(f"timeout, user: {ctx.author} ({ctx.author.id}), server: {ctx.guild}")	
            if not ctx.author.guild_permissions.manage_messages:
                Embed = discord.Embed(title='Error', description = 'You do not have sufficient rights to execute this command :(', color=discord.Color.red())
                await ctx.response.send_message(embed = Embed)
                return
            duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
            if duration >= timedelta(days = 28):
                Embed = discord.Embed(title='Error', description = 'You did not specify a specific time (up to 28 days)', color=discord.Color.red())
                await ctx.response.send_message(embed = Embed)
            if not member:
                Embed = discord.Embed(title='Error', description = 'User not specified! Check if you have chosen correctly!', color=discord.Color.red())
                await ctx.response.send_message(embed = Embed)
                return
            if member == ctx.author:
                
                Embed = discord.Embed(title='Error', description = 'Unknow Error! Try running the command again otherwise contact the developers for help', color=discord.Color.red())
                await ctx.response.send_message(embed=Embed)
                return
            if member == ctx.guild.owner:
                
                Embed = discord.Embed(title='Error', description = 'Unable to give timeout to server owner', color=discord.Color.red())
                await ctx.response.send_message(embed=Embed)
                return
            if member.top_role >= ctx.author.top_role:
                
                Embed = discord.Embed(title='Error', description = 'The bot role or your role does not allow you to timeout this user!', color=discord.Color.red())
                await ctx.response.send_message(embed=Embed)
                return        
            if member.top_role >= ctx.me.top_role:
                
                Embed = discord.Embed(title='Error', description = 'The bot role or your role does not allow you to timeout this user!', color=discord.Color.red())
                await ctx.response.send_message(embed=Embed)
                return                          
            try:
                await member.timeout(duration=duration, reason=reason)
                
                embed = discord.Embed(title='Successfully!', description=f'Timeout issued:{ctx.author.mention}\nTimeout given to user: {member.mention}\nTimeout duration: {days} days {hours} hours {minutes} minute(s) {seconds} second(s)\nreason: **{reason}**', color=discord.Color.green())
                await ctx.response.send_message(embed=embed)

                embed = discord.Embed(title=f'You have been given a timeout on the server {ctx.guild.name}', description=f'Timeout issued:{ctx.author.mention}\nTimeout duration: {days} days {hours} hours {minutes} minute(s) {seconds} secound(s)\nreason: **{reason}**', color=0xffff00)
                await member.send(embed=embed)
                
            except discord.Forbidden:
                return
            except discord.HTTPException:
                return






@bot.event
async def on_message(message):
   if 'мать ебал, шлюха ,безмамный, безмамная, уебище, твоя мать в канаве, пидор, еблан' in message.content:
      await message.delete()
      await message.channel.send(f"{message.author.mention} Don't swear!")
   else:
      await bot.process_commands(message)


@bot.event
async def on_message(message):
   if 'https://tenor.com/view/%D0%B8%D0%BD%D1%82%D1%80%D0%BE-intro-channel-%D0%BD%D0%B0%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB-%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB-gif-24514255' in message.content:
      await message.delete()
      await message.channel.send(f"{message.author.mention} Don't swear!")
   else:
      await bot.process_commands(message)


@bot.event
async def on_guild_join(guild):
    cict = []
    randchan = None
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages == True:
            cict.append(channel)
        else:
            pass
    randchan = random.choice(cict)
    if randchan == None:
        pass
    else:
        emb = discord.Embed(description =  f'Hello! I **`Zenite Protect`**! \n I was created to protect your Discord server :) \n I work on slash commands prefixed with **`/`** \n Enjoy!)', title = "Zenite Protect", url='https://discord.com/api/oauth2/authorize?client_id=978362279131238440&permissions=8&scope=bot%20applications.commands', color = discord.Color.green())
        await randchan.send(embed=emb)
        activity = discord.Streaming(
        name=
        f"Protecting {len(bot.guilds)} server(s)!",
        url = "https://www.twitch.tv/404",type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)


@bot.slash_command(description="Lock a channel")
@commands.has_permissions(administrator=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')
    print("User has locked channel!")





@bot.slash_command(description="Unlock a locked channel")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + "has been unlocked")
    print("User has unlocked channel!")


@bot.slash_command(description="Enable slowmode in the channel")
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.response.send_message(f'Slowmode enadled.Enjoy :)', ephemeral=True)





@bot.slash_command(description="About Zenite Protect")
async def info(ctx):
    Embed = discord.Embed(title = 'About Zenite Protect', color=0x30d5c8)
    Embed = discord.Embed(description = 'This bot listens to restore your server after crash and raid.\nBot Creators:Ati4-n Games#1863 and YT|дима читер#0641\nPython version:3.10.5 x64\nCurrent bot version:2.2 (installed:09.09.2022)', color=0x30d5c8)
    await ctx.response.send_message(embed = Embed)



@bot.slash_command(description="Say text")
async def echo(ctx, message=None):
    await ctx.send(message)








@bot.slash_command(description="Add a number to a number")
async def add(ctx, num1 : float, num2 : float):
  answer = num1 + num2

  ans_em = discord.Embed(title = 'Addition', description = f'Question: {num1} + {num2}\n\nAnswer: {answer}', colour = discord.Colour.from_rgb(13, 255, 251))
  await ctx.send(embed = ans_em)



@bot.slash_command(description="Ask Ben a Question 🐶")
async def ben(ctx, *, args):
    OTVET = ["No", "Yes", "Hohoho", "Ugh"]
    OTVETA = random.choice(OTVET)
    embedben = discord.Embed(title="Ben",description=f"Question: \'{args}' Ben's answer: \n **{OTVETA}**")
    if OTVETA == "Ugh":
        embedben.set_image(url="https://c.tenor.com/fr6i8VzKJuEAAAAd/talking-ben-ugh.gif")
        embedben.color = 0xffee38
        await ctx.send(embed=embedben)
    elif OTVETA == "Hohoho":
        embedben.set_image(url="https://c.tenor.com/agrQMQjQTzgAAAAd/talking-ben-laugh.gif")
        embedben.color = 0xffee38
        await ctx.send(embed=embedben)
    elif OTVETA == "Yes":
        embedben.set_image(url="https://c.tenor.com/6St4vNHkyrcAAAAd/yes.gif")
        embedben.color = 0x4dff6a
        await ctx.send(embed=embedben)
    elif OTVETA == "No":
        embedben.color = 0xff4d4d
        embedben.set_image(url="https://c.tenor.com/x2u_MyapWvcAAAAd/no.gif")
        await ctx.send(embed=embedben)



@bot.slash_command(description="Will remove the selected role from all members who have it")
async def remrole(ctx, role:discord.Role=None):
    if ctx.author.id not in lists.blacklist:
        if not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title='Error!', description=f'You do not have permission to execute this command :(', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return
        if not role:
            embed = discord.Embed(title='Error!', description=f'Unknown error, please try the command again. If an error appears again, contact the developers of the bot!', color=discord.Color.red())
            await ctx.channel.send(embed=embed)
        else:
            number = 0
            number1 = 0
            for mroles in role.members:
                number +=1
                number1 +=1
            lroles = len(ctx.guild.members) - number1
            embed = discord.Embed(title='🕰️REMOVING ROLES...', description=f'Role is being removed.... \nRole name:{role.mention}\nRequestet by:{ctx.author.mention}', color=discord.Color.green())
            msg = await ctx.channel.send(embed=embed)
            for member in ctx.guild.members:
                await member.remove_roles(role)
                number1 -= 1
                embed = discord.Embed(title='🕰️REMOVING ROLES...', description=f'Role is being removed.... \nRole name:{role.mention}\nRequestet by:{ctx.author.mention}', color=discord.Color.green())
                await msg.edit(embed=embed)
            embed = discord.Embed(title='✅COMPLETED', description=f'The role {role.mention} has been removed from:**{int(number)}** members', color=discord.Color.green())
            await msg.edit(embed=embed)











@bot.slash_command(description="Show information about user")
async def user(ctx, member: discord.Member = None):
    if member is None:
        user = ctx.author
    else:
        user = member
    embed = discord.Embed(description=user.mention)
    embed.set_footer(text='ID: ' + str(user.id))
    embed.add_field(name="Joined to server:", value='<t:{}:D>'.format(int(time.mktime(user.joined_at.timetuple()))))
    embed.add_field(name="Registred to Discord:", value='<t:{}:D>'.format(int(time.mktime(user.created_at.timetuple()))))
    if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles: [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    await ctx.send(embed = embed)





@bot.slash_command(description="Get invite on bot support server")
async def support (ctx):
    await ctx.response.send_message(f'https://discord.gg/UVrcQnSWHy', ephemeral=True)





@bot.slash_command(description="The command in development")
async def switch_lang(ctx, lang=commands.Param(choices=['ru', 'en'])):
    if ctx.author.guild_permissions.administrator:
        with open("settings.json", "r") as file:
            settings = json.load(file)
        settings[str(ctx.guild.id)]['lang'] = lang
        with open("settings.json", "w") as file:
            json.dump(settings, file, indent=4)
        with open("text.json", "r", encoding="utf-8") as file:
            text = json.load(file)
        embed = discord.Embed(
            title=text[lang]['done'], 
            description=text[lang]['switch_lang'], 
            color=discord.Color.green())
        await ctx.send(embed=embed)


@bot.event
async def on_member_join(member):
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT channel_id FROM 'main' WHERE guild_id = {member.guild.id}")
	result = cursor.fetchone()
	if result is None:return
	else:
		cursor.execute(f"SELECT msg FROM 'main' WHERE guild_id = {member.guild.id}")
		result1 =  cursor.fetchone()
		channel = bot.get_channel(int(result[0]))
		welcometext = str(result1[0])

		embed = discord.Embed(description=welcometext, color=0xED4245)
		embed.set_author(name=member)
		embed.set_footer(text=f'Now members:{len(member.guild.members)}')
		try:embed.set_image(url=member.avatar.url)
		except AttributeError:pass
		try:await channel.send(embed = embed)    
		except:pass


@bot.event
async def on_member_remove(member):
	db = sqlite3.connect('logs.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT * FROM 'main' WHERE guild = {member.guild.id}")
	result = cursor.fetchone()
	if result is None:
		pass
	else:
		channel_id = result[1]
		channel = await bot.get_channel(channel_id)
		embed = discord.Embed(description=f'{member.mention} leave the server :(', color=discord.Color.red())
		try:embed.set_author(name=member, icon_url=member.avatar.url)
		except AttributeError:embed.set_thumbnail(url = member.display_avatar.url)
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
		embed.set_footer(text = f'{member.guild.name} - Today at {now}')
		try:await channel.send(embed = embed)
		except:pass

@bot.event
async def on_member_ban(guild, member):
	db = sqlite3.connect('logs.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {guild.id}")
	result = cursor.fetchone()
	if result is None:return
	else:
		channel = bot.get_channel(int(result[0]))
		embed = discord.Embed(description=f'{member.mention} has been banned on the server!', color=discord.Color.red())
		try:embed.set_author(name=member, icon_url=member.avatar.url)
		except AttributeError:embed.set_thumbnail(url = member.display_avatar.url)
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
		embed.set_footer(text = f'{guild.name} - Today at {now}')
		try:await channel.send(embed = embed)
		except:pass

@bot.event
async def on_member_unban(guild, member):
	db = sqlite3.connect('logs.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {guild.id}")
	result = cursor.fetchone()
	if result is None:return
	else:
		channel = bot.get_channel(int(result[0]))
		embed = discord.Embed(description=f'{member.mention} has been unbanned on the server!', color=discord.Color.green())
		try:embed.set_author(name=member, icon_url=member.avatar.url)
		except AttributeError:embed.set_thumbnail(url = member.display_avatar.url)
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
		embed.set_footer(text = f'{guild.name} - Today at {now}')
		try:await channel.send(embed = embed)
		except:pass



@bot.event
async def on_guild_role_create(role):
	db = sqlite3.connect('logs.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {role.guild.id}")
	result = cursor.fetchone()
	if result is None:return
	else:
		channel = bot.get_channel(int(result[0]))
		embed = discord.Embed(description=f'{role} created!', color=discord.Color.green())
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
		embed.set_footer(text = f'{role.guild.name} - Today at {now}')
		try:embed.set_author(name=role.guild, icon_url=role.guild.icon.url)
		except AttributeError:embed.set_author(name=role.guild)
		try:await channel.send(embed = embed)
		except:pass

@bot.event
async def on_guild_role_delete(role):
	db = sqlite3.connect('logs.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {role.guild.id}")
	result = cursor.fetchone()
	if result is None:return
	else:
		channel = bot.get_channel(int(result[0]))
		embed = discord.Embed(description=f'{role} deleted!', color=discord.Color.red())
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
		embed.set_footer(text = f'{role.guild.name} - Today at {now}')
		try:embed.set_author(name=role.guild, icon_url=role.guild.icon.url)
		except AttributeError:embed.set_author(name=role.guild)
		try:await channel.send(embed = embed)
		except:pass


@bot.event
async def on_guild_channel_create(channel):
	db = sqlite3.connect('logs.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {channel.guild.id}")
	result = cursor.fetchone()
	if result is None:return
	else:
		channel1 = bot.get_channel(int(result[0]))
		embed = discord.Embed(description=f'{channel} created', color=discord.Color.green())
		try:embed.set_author(name=channel.guild, icon_url=channel.guild.icon.url)
		except AttributeError:embed.set_author(name=channel.guild)
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
		embed.set_footer(text = f'{channel.guild.name} - Today at {now}')
		try:await channel1.send(embed = embed)
		except:pass

@bot.event
async def on_guild_channel_delete(channel):
	db = sqlite3.connect('logs.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = {channel.guild.id}")
	result = cursor.fetchone()
	if result is None:return
	else:
		channel1 = bot.get_channel(int(result[0]))
		embed = discord.Embed(description=f'{channel} deleted!', color=discord.Color.red())
		try:embed.set_author(name=channel.guild, icon_url=channel.guild.icon.url)
		except AttributeError:embed.set_author(name=channel.guild)
		now = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
		embed.set_footer(text = f'{channel.guild.name} - Today at {now}')
		try:await channel1.send(embed = embed)
		except:pass



@bot.slash_command(description="Set the log channel")
async def setlog(ctx, channel:discord.TextChannel):
		if ctx.author.id not in lists.blacklist:
			if ctx.author.guild_permissions.administrator:
				db = sqlite3.connect('logs.sqlite')
				cursor = db.cursor()
				cursor.execute(f"SELECT channel_id FROM logs WHERE guild_id = '{ctx.guild.id}'")
				result =  cursor.fetchone()
				if result is None:
					sql = ("INSERT INTO logs(guild_id, channel_id) VALUES(?,?)")
					val = (ctx.guild.id, channel.id)
					embed = discord.Embed(title = 'DONE!',description=f'Selected log channel:{channel.mention}\nTo disable the logging system, delete the selected channel ', color=discord.Color.green())
					await ctx.response.send_message(embed=embed)
				elif result is not None:
					sql = ("UPDATE logs SET channel_id = ? WHERE guild_id = ?")
					val = (channel.id, ctx.guild.id)
					embed = discord.Embed(title = 'DONE!',description=f'Selected log channel:{channel.mention}\nTo disable the logging system, delete the selected channel', color=discord.Color.green())
					await ctx.response.send_message(embed=embed)
				cursor.execute(sql, val)
				db.commit()
				cursor.close()
				db.close()
				return
			else:
				embed = discord.Embed(title='ERROR!', description = 'An error has occurred!\nPerhaps you do not have rights or the bot does not have them', color=discord.Color.red())
				await ctx.response.send_message(embed=embed)


@bot.event
async def on_member_join(member):
    async for entry in member.guild.audit_logs(
        limit=1, action=discord.AuditLogAction.bot_add
    ):
        if member.bot:
            if member.public_flags.verified_bot:
                verification_bot = f"Verified"
            else:
                verification_bot = f"Unverified"
                await member.kick(
                    reason=f"The bot is not verified and can be dangerous for the server!",
                )

@bot.slash_command(description="Bot ping. Developers only")
async def ping(ctx):
  if ctx.author.id in [884004459074703392]:
    await ctx.response.send_message(f'Bot ping is {bot.latency}!', ephemeral=True)

@bot.event
async def on_message(message):
   if '@978362279131238440' in message.content:
      await message.channel.send(f"Hello again!  The bot uses slash commands, if for some reason they are not shown to you, re-add the bot to the server. If the bot does not respond to commands, then the bot may have a high load, no rights, or you are blacklisted")
   else:
      await bot.process_commands(message)

@bot.slash_command(description="Turn off bot (developers only)")
async def close_(ctx):
 if ctx.author.id in [884004459074703392, 971805315572039780, 691943936138412114]:
  embed=discord.Embed(title="⚠️ CAUTION ", description="The bot is shutting down...", color=0xff0000)
  await ctx.send(embed=embed)
 await bot.close()
  
keep_alive.keep_alive()
bot.run(os.environ.get('TOKEN'), reconnect=True)
my_secret = os.environ['TOKEN']