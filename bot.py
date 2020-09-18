import os
import random

import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_TOKEN = os.getenv("GIPHY_TOKEN")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
  print(f'{bot.user.name} is mf ready.')

@bot.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(f"Hello {member.name}, welcome to daddy's server.")

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

@bot.command(name='memeee', help='should generate a random meme')
async def get_meme(ctx):
  await ctx.trigger_typing()
  url = "https://ronreiter-meme-generator.p.rapidapi.com/meme"
  querystring = {"font":"Impact","font_size":"50","meme":"Condescending-Wonka","top":"Top text","bottom":"Bottom text"}
  headers = {
      'x-rapidapi-host': "ronreiter-meme-generator.p.rapidapi.com",
      'x-rapidapi-key': "2a9c5fff77mshaabf4ba686b0433p1279eajsnb74d28ce170d"
      }
  response = requests.get(url, headers=headers, params=querystring)
  await ctx.send(response.text)

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
  url = f"http://api.giphy.com/v1/gifs/search?api_key={GIPHY_TOKEN}&q={q}&limit=2"
  response = requests.get(url)
  embed_url = response.json()['data'][0]['embed_url']

  await ctx.send(embed_url)


@bot.command(name="space", help="tells how many astronauts are in space rn")
async def get_mf_astronauts(ctx):
  await ctx.trigger_typing()
  url = "http://api.open-notify.org/astros.json"
  response = requests.get(url)
  json = response.json()
  await ctx.send(json)

@bot.command(name="test", help="used by that dickhead alexis for testing stuff")
async def test(ctx):
  await ctx.trigger_typing()
  await ctx.send("ayyy lmao", tts=True)

bot.run(DISCORD_TOKEN)
