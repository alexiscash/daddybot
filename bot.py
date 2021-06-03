import os
import random

import logging
import discord
import requests
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

os.system('cls')

logging.basicConfig(level=logging.ERROR)

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_TOKEN = os.getenv("GIPHY_TOKEN")

bot = commands.Bot(command_prefix='.')
status = ['h3ll0fr1end.wav', 'd3bug.mkv', 'da3m0ns.mp4', '3xpl0its.wmv', 'k3rnel-pan1c.ksd', 'logic-b0mb.hc',
          'm4ster-s1ave.aes', 'h4ndshake.sme', 'succ3ss0r.p12', 'init_5.fve', 'h1dden-pr0cess.axx', 'runtime-error.r00', 'shutdown -r']

global not_started
not_started = True
@bot.event
async def on_ready():
  global not_started

  print(f'{bot.user.name} is mf ready.')
  # channel = bot.get_channel(749370616720654461)
  # await channel.send("oh wait im not real")
  if not_started:
    change_status.start()
    not_started = False

@tasks.loop(seconds=300)
async def change_status():
  await bot.change_presence(activity=discord.Game(random.choice(status)))

# ! deadass idk how to do this
# @bot.event
# async def on_member_join(member):
#   await member.create_dm()
#   await member.dm_channel.send(f"Hello {member.name}, welcome to {member.guild.name}'s server.")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    await ctx.send("command not found ya dumby")
    return
  raise error

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  response_dict = {
    'litty': 'titty',
    'beep': 'boop',
    'ping': 'pong',
    '!say': 'more arguments required'
  }

  c = message.content.lower()
  if c in response_dict:
    await message.channel.send(response_dict[c])
    return

  msg = message.content.split(' ')
  if 'yo' in msg and bot.user.name in msg:
    await message.channel.send('yo what up')
    return

  await bot.process_commands(message)

@bot.command(name='say', help="Says whatever you say. Nothing fancy.")
async def say(ctx):
  await ctx.trigger_typing()
  await ctx.send(ctx.message.content.split(' ', 1)[1])

# ! Deprecated  token dont work no more
# @bot.command(name='memeee', help='should generate a random meme')
# async def get_meme(ctx):
#   await ctx.trigger_typing()
#   url = "https://ronreiter-meme-generator.p.rapidapi.com/meme"
#   querystring = {"font":"Impact","font_size":"50","meme":"Condescending-Wonka","top":"Top text","bottom":"Bottom text"}
#   headers = {
#       'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com",
#       'x-rapidapi-key': "2a9c5fff77mshaabf4ba686b0433p1279eajsnb74d28ce170d"
#       }
#   response = requests.get(url, headers=headers, params=querystring)
#   await ctx.send(response.text)

@bot.command(name='joke', help='generates a funny ass joke from JokeAPI')
async def joke(ctx):
  await ctx.trigger_typing()
  url = "https://sv443.net/jokeapi/v2/joke/Any"
  response = requests.get(url)
  joke = response.json()

  if joke['error']:
    await ctx.send('something went wrong. please try again')
    return
  if joke['type'] == 'single':
    await ctx.send(joke['joke'])
    return

  await ctx.send(joke['setup'])
  await ctx.send(joke['delivery'])

@bot.command(name="gif", help="should return a gif from GIPHY API")
async def get_gif(ctx, q, *argv):
  await ctx.trigger_typing()
  await ctx.send("i accidentally deleted the password for this so just dont use this")
#   await ctx.trigger_typing()
#   url = f"http://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q={q}&limit=2"
#   response = requests.get(url)
#   embed_url = response.json()['data'][0]['embed_url']

#   await ctx.send(embed_url)

@bot.command(name="space", help="tells how many astronauts are in space rn")
async def get_mf_astronauts(ctx):
  await ctx.trigger_typing()
  url = "http://api.open-notify.org/astros.json"
  response = requests.get(url)
  json = response.json()
  await ctx.send(json)

@bot.command(name="ready", help="daddybot helpfully lets you know that he is ready to go.")
async def say_ready(ctx):
  await ctx.trigger_typing()
  await ctx.send(f"{bot.user.name} is ready to go")


 # ! BIG CHUNGUS   
 # !
 # !
@bot.command(name="chungus", help="controls the muting stuff for playing among us")
async def chungus(ctx):
  pass

global leader
leader = None

global ghostmode_on
ghostmode_on = False

global in_discussion
in_discussion = False

global dead_members
dead_members = []


@bot.command()
async def host(ctx):
  global leader 

  if leader == None:
    leader= ctx.author
    await ctx.trigger_typing()
    await ctx.send(f"Host connected: {ctx.author.name}")
  elif leader != None and leader != ctx.author:
    await ctx.trigger_typing()
    await ctx.send(f"Sorry, {leader} is already a host. The host can disconnect by typing .host again.")
  else:
    await ctx.trigger_typing()
    await ctx.send(f"Host disconnected: {ctx.author.name}")
    leader = None

@bot.command()
async def users(ctx):
  global leader

  await ctx.trigger_typing()
  try:
    if leader == None:
      await ctx.send("The host must first connect by typing '.host'.")
    else:
      await ctx.trigger_typing()
      string = "Users connected: \n"

      for member in list(bot.get_channel(leader.voice.channel.id).members):
        string = string + f"- {member}\n"

      await ctx.send(f"```{string}```")
  except AttributeError as err:
    await ctx.send('host is not in a voice channel')

@bot.command()
async def deadrn(ctx):
  global leader
  global dead_members 

  if leader == None:
    await ctx.trigger_typing()
    await ctx.send("The host must first connect by typing '.host'.")
  else:
    await ctx.trigger_typing()
    string = "Users dead rn: \n"

    for member in dead_members:
      string = string + f"- {member}\n"

    await ctx.send(f"```{string}```")

@bot.command()
async def mute(ctx):
  global leader 
  global ghostmode_on

  global in_discussion
  in_discussion = False

  if ctx.author != leader:
    await ctx.trigger_typing()
    await ctx.send("Only the host can use this command")
    return

  for member in list(bot.get_channel(leader.voice.channel.id).members):
    if member.id in dead_members and ghostmode_on:
      await member.edit(mute = False)
    elif member.id not in dead_members and ghostmode_on:
      await member.edit(deafen = True, mute = True)
    else:
      await member.edit(mute = True)
    
@bot.command()
async def unmute(ctx):
  global leader
  global dead_members
  global ghostmode_on

  global in_discussion
  in_discussion = True

  if ctx.author != leader:
    await ctx.trigger_typing()
    await ctx.send("Only the host can use this command")
    return
  
  for member in list(bot.get_channel(leader.voice.channel.id).members):
      if member.id in dead_members and ghostmode_on:
          await member.edit(mute = True)
      elif member.id in dead_members and ghostmode_on == False:
          await member.edit(mute = True)
      elif member.id not in dead_members and ghostmode_on:
          await member.edit(deafen = False, mute = False)
      else:
          await member.edit(mute = False)

@bot.command()
async def clear(ctx):
  global leader 

  global dead_members
  dead_members = []

  if ctx.author != leader:
    await ctx.trigger_typing()
    await ctx.send("Only the host can use this command")
    return

  for member in list(bot.get_channel(leader.voice.channel.id).members):
    await member.edit(deafen = False, mute = False)

@bot.command()
async def dead(ctx):
  global ghostmode_on
  global dead_members

  if ghostmode_on:
    await ctx.author.edit(mute = False, deafen = False)
  else:
    await ctx.author.edit(mute = True)

  if ctx.author not in dead_members:
    dead_members.append(ctx.author.id)

@bot.command()
async def kill(ctx, *members: discord.Member):
  global leader
  global dead_members
  global ghostmode_on

  for member in members:
    if member not in list(bot.get_channel(leader.voice.channel.id).members):
      await ctx.trigger_typing()
      await ctx.send(f"User not in channel: {member}")
      continue

    try:
      if ghostmode_on and in_discussion:
        await member.edit(mute = True)
        valid = True
      elif ghostmode_on and in_discussion == False:
        await member.edit(deafen = False, mute = False)
        valid = True
      else:
        await member.edit(mute = True)
        valid = True
    except Exception as e:
      print(e)
      await ctx.trigger_typing()
      await ctx.send(f"Invalid user: {member}")

    if valid and member.id not in dead_members:
      dead_members.append(member.id)

@bot.command()
async def ghostmode(ctx):
  global ghostmode_on

  if ctx.author != leader:
    await ctx.trigger_typing()
    await ctx.send("Only the host can use this command")
  else:
    if ghostmode_on:
      ghostmode_on = False
      await ctx.trigger_typing()
      await ctx.send("``` Ghost mode activated ```")
    else:
      ghostmode_on = True
      await ctx.trigger_typing()
      await ctx.send("``` Ghost mode activated ```")

# !
# ! end chungus


@bot.command(help="used for testing purposes by that dickhead alexis")
async def test(ctx):
  await ctx.trigger_typing()
  await ctx.send(f"There are {len(ctx.guild.members)} members on this server")


bot.run(DISCORD_TOKEN)
