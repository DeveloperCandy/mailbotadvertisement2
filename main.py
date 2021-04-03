import keep_alive
import random
import discord
import time
import json
intents = discord.Intents.default()
intents.members = True
from discord import Webhook, AsyncWebhookAdapter
import requests
import aiohttp
from PIL import Image
from io import BytesIO
from discord.ext import commands
client = discord.Client()
client = commands.Bot(command_prefix=">",intents=intents)
default_embed_color = discord.Colour.from_rgb(0,255,255)

  
@client.command()
@commands.cooldown(1,600,commands.BucketType.user)
async def question(ctx):
  await ctx.send("**Please check dms**")
  embed = discord.Embed(colour=default_embed_color,title="Whats your question?")
  var = await ctx.author.send(embed=embed,content=None)
  question = await client.wait_for("message",check=lambda m:m.author.id==ctx.author.id and m.guild==None)
  embed.title = "We have send your questions to the admins, they will contact you via the thread. Please be patient as there might be other threads which my be awaiting response."
  await var.edit(embed=embed)
  role = discord.utils.get(ctx.guild.roles,name="Modmail License")
  overwrites = overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False,view_channel=False),
    role: discord.PermissionOverwrite(read_messages=True,send_messages=True)
}
  catoragry = discord.utils.get(ctx.guild.categories,id=825652446793433098)
  channel = await ctx.guild.create_text_channel(name="question "+str(ctx.author.id),overwrites=overwrites,category=catoragry,topic=str(ctx.author.id))
  await channel.edit(topic=str(ctx.author.id))
  roles = ""
  for i in ctx.author.roles:
    roles = f"{roles} {i.mention}"
  embed = discord.Embed(title="Question",description=question.content,colour=default_embed_color)
  embed.add_field(name="Roles",value=roles)
  embed.add_field(name="Nickname",value=ctx.author.display_name)
  embed.add_field(name="UserId",value=str(ctx.author.id))
  embed.set_author(name=str(ctx.author),icon_url=ctx.author.avatar_url)
  var = await channel.send(embed=embed,content=f"@everyone question is raised by {ctx.author.mention}")
  await var.pin()
  embed = discord.Embed(colour=default_embed_color,title="Commands")
  embed.add_field(name=">speak [mention_user/use userid] [message]",value="Used to speak with a user. Usable in a thread only")
  embed.add_field(name=">delete",value="Used to delete a thread. Usable in a thread channel ONLY.")
  var = await channel.send(embed=embed,content=None)
  await var.pin()

@client.command()
async def speak(ctx,user:discord.Member,*,speak):
  if ctx.channel.category_id == 825652446793433098:
    embed = discord.Embed(title="Response",description=speak,colour=default_embed_color)
    embed.set_footer(text="You can respond to this, if you like.")
    await user.send(embed=embed,content=None)
    embed.set_footer(text=f"Responsed by {ctx.author}")
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed,content=None)
    response = await client.wait_for("message",check=lambda message:message.author.id==user.id and message.guild == None)
    embed = discord.Embed(title="Question",description=response.content,colour=default_embed_color)
    embed.set_author(name=user.name,icon_url=user.avatar_url)
    await ctx.send(embed=embed,content=None)
  else:
    await ctx.send("Only possible in a Thread")

@client.command()
async def delete(ctx):
  if ctx.channel.category_id == 825652446793433098:
    embed = discord.Embed(colour=default_embed_color,title="Thread deleted by admin")
    channel_topic = ctx.channel.topic
    member = discord.utils.get(ctx.guild.members,id=int(channel_topic))
    await member.send(embed=embed,content=None)
    await ctx.channel.delete()
  else:
    await ctx.send("Possible only in a thread")


  
@client.command()
@commands.has_permissions(manage_channels = True)
async def snippet(ctx,action,*,name):
  await ctx.send("**Please check your dms**")
  if action == "create":
    embed = discord.Embed(title="Please enter the description you want this snippet to be visible",colour=default_embed_color)
    var = await ctx.author.send(embed=embed,content=None)
    description = await client.wait_for("message",check=lambda message: message.author.id == ctx.author.id and message.guild == None)
    embed = discord.Embed(title=name,description=description.content,colour=default_embed_color)
    await var.edit(content="This is how the embed will look: `type y/n`",embed=embed)
    check = await client.wait_for("message",check=lambda message: message.author.id == ctx.author.id and message.guild == None and message.content == "y" or message.content == "n")
    if check.content == "y":
      with open("snippets.json") as json_file:
        data = json.load(json_file)
        new_data = {
          "name": name,
          "content": description.content
        }
        data.append(new_data)
      with open("snippets.json","w") as j:
        json.dump(data,j,indent=3)
      embed = discord.Embed(title="Done",colour=default_embed_color)
      embed.set_image(url = "https://media.discordapp.net/attachments/824874641653760010/825655497813655592/hahayes.jpg?width=166&height=149")
      await var.edit(embed=embed,content=None)
    else:
      await var.edit(content="Cancelled",embed=None)
  elif action == "open":
    await ctx.send("Send the user id of the user who u wanna send the snippet")
    answer = await client.wait_for("message",check=lambda message: message.author.id == ctx.author.id and ctx.guild.id == message.guild.id)
    member = discord.utils.find(lambda m: m.id == int(answer.content),ctx.guild.members)  
    embed = discord.Embed(colour=discord.Colour.red(),title="Not found")
    var = await member.send(embed=embed,content=None)
    with open("snippets.json") as json_file:
      data = json.load(json_file)
      for i in data:
        if i["name"] == name:
          embed.title = name
          embed.description = i["content"]
          embed.colour = default_embed_color
          await var.edit(embed=embed,content=None)

@client.command()
@commands.has_permissions(manage_channels=True)
async def server_stats(ctx,channel:discord.TextChannel):
  embed = discord.Embed(title="Server Stats",colour=default_embed_color)
  embed.add_field(name="Members",value=str(ctx.guild.member_count))
  message = await channel.send(embed=embed,content=None)
  with open("server_stats.json") as json_file:
    data = json.load(json_file)
    new_data = {
      "message": message.id,
      "guild": ctx.guild.id,
      "channel": channel.id
    }
    data.append(new_data)
  with open("server_stats.json","w") as j:
    json.dump(data,j,indent=3)


@client.event
async def on_command_error(command,error):
  embed = discord.Embed(title="Error",description="**"+str(error)+"**",colour=discord.Colour.red())
  message = await command.message.channel.send(embed=embed,content="It seems like some error occured")


@client.event
async def on_ready():
  print("Bot is Ready")
  await client.change_presence(activity=discord.Game("Mailing >help"),status=discord.Status.do_not_disturb)
  client.load_extension("cogs.Partner")

@client.event
async def on_raw_reaction_add(payload):
  guild = discord.utils.find(lambda g: g.id == payload.guild_id,client.guilds)
  member = discord.utils.find(lambda m: m.id == payload.user_id,guild.members)
  channel = discord.utils.find(lambda c: c.id == payload.channel_id,guild.text_channels)
  message = await channel.fetch_message(payload.message_id)
  print(member)
  emoji = payload.emoji
  if member.id == 824866004685160469:
    return 
  with open("partner.json") as json_file:
    data = json.load(json_file)
    for i in data:
      if int(i["message"]) == int(payload.message_id):
        print(str(emoji))
        if str(emoji) == "✔":
          channel = discord.utils.get(guild.text_channels,id=824199678387945502) 
          post = i["partner"]
          author = i["user"]
          url = i["url"]
          embed=discord.Embed(colour=default_embed_color,title="Partnership",description=post)
          embed.set_author(name=author,icon_url=url)
          await channel.send(embed=embed,content=None)
          await message.delete()
        elif str(emoji) == "❌":
          await message.delete()

@client.event
async def on_member_join(member):
  guild = member.guild
  members = guild.member_count
  with open("server_stats.json") as json_file:
    data = json.load(json_file)
    for i in data:
      if i["guild"] == guild.id:
        channel = discord.utils.get(guild.channels,id=i["channel"])
        message = await channel.fetch_message(i["message"])
        embed = discord.Embed(title="Server Stats",colour=default_embed_color)
        embed.add_field(name="Members",value=str(guild.member_count))
        await message.edit(embed=embed,content=None)

@client.event
async def on_member_remove(member):
  guild = member.guild
  members = guild.member_count
  with open("server_stats.json") as json_file:
    data = json.load(json_file)
    for i in data:
      if i["guild"] == guild.id:
        channel = discord.utils.get(guild.channels,id=i["channel"])
        message = await channel.fetch_message(i["message"])
        print(message)
        embed = discord.Embed(title="Server Stats",colour=default_embed_color)
        embed.add_field(name="Members",value=str(guild.member_count))
        await message.edit(embed=embed,content=None)

@client.command()
async def load(ctx, extension):
  if ctx.author.id == 661235121285758987:
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
  if ctx.author.id == 661235121285758987:

    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx,extension):
  if ctx.author.id == 661235121285758987:
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Reloaded successfully")

with open("key.env","r") as txt:
  line = txt.readlines()
  token = line[0].strip()

for i in client.guilds:
  print(i.name)
print("Mains ready 👍")

client.run(token)
