from discord.ext import commands
import discord, datetime, time
from discord import Member, Status
from datetime import date, datetime
import random

from full_game import Game

bard_assigned = []
commandsEnabled = {}
player123 = []
intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)
new_game = Game()

@bot.event
async def on_ready():
	print("The bard is ready!")
	print('logged in as: ')
	print(bot.user.name)
	print(bot.user.id)
	print('-----')



    # user = ctx.message.author
    # role = discord.utils.get(user.guild.roles, name="bard")
    # if(len(role.members)!=0):
    # 	bard_assigned.append(role.members)
    # 	print("bard hai already")
	
@bot.event
async def enabler1(guild):
	commandsEnabled[str(guild.id)] = {}
	for cmd in bot.commands:
		commandsEnabled[str(guild.id)][cmd.name] = True



@bot.event
async def Toggle(ctx, command, guild):
    try:
        commandsEnabled[str(guild.id)][command] = not commandsEnabled[str(guild.id)][command]
        await ctx.send(f"{command} command {['disabled','enabled'][int()]}")
    except KeyError:
        await ctx.send(":x:Command with that name not found")

# @bot.command
# async def Example(ctx):
#     if not commandsEnabled[str(ctx.guild.id)]["Example"]:
#         await ctx.send(":x:This command has been disabled")
#         return
#     await ctx.send("Hello world!")



#@commands.has_role('RoleName')
#@bot.command(name='hello', aliases=['h','he','hl'])
@bot.command()
async def hello(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["hello"]:
		await ctx.send(":x:This command has been disabled")
		return
	await ctx.send("Hello! this is the message")

# @bot.event
# async def on_member_join(member):
# 	role = discord.utils.get(member.guild.roles, name="herd")
# 	await bot.add_roles(member, role)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="herd")
    await member.add_roles(role)
    await ctx.send(f"{ member.name } joined as herd. Use command <!leavecave> to spectate")

@bot.command()
@commands.has_role('admin')
async def remove(ctx, member: discord.Member, role: discord.Role):
	if not commandsEnabled[str(ctx.guild.id)]["remove"]:
		await ctx.send(":x:This command has been disabled")
		return
	await member.remove_roles(role)

@bot.command(name="ping")
async def _ping(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["ping"]:
		await ctx.send(":x:This command has been disabled")
		return
	await ctx.send(f"Ping: {bot.latency}")

@bot.event
async def on_member_update(before, after):
    if str(after.status) == "offline":
        print("{} has gone {}.".format(after.name,after.status))


@bot.command(pass_context=True, name='status')
async def status(ctx, member: Member):
	if not commandsEnabled[str(ctx.guild.id)]["status"]:
		await ctx.send(":x:This command has been disabled")
		return
	print(member)
	await ctx.send(str(member.status))

#@bot.command(pass_context=True, name='status')
async def status1(ctx, member: Member):
	print(member)
	return member.status


@bot.command(pass_context=True)
async def bardmeup(ctx):
	guilds = await bot.fetch_guilds(limit=150).flatten()
	print(guilds)
	for i in range(len(guilds)):
		await enabler1(guilds[i])
	if not commandsEnabled[str(ctx.guild.id)]["bardmeup"]:
		await ctx.send(":x:This command has been disabled")
		return
	print(commandsEnabled)
	user = ctx.message.author
	role = discord.utils.get(user.guild.roles, name="herd")
	print("\n=======\n\n")
	print(bard_assigned)
	print("\n\n=======\n")
	if(len(bard_assigned) == 0):
		if role in ctx.author.roles:
			await ctx.author.remove_roles(role)
		role = discord.utils.get(user.guild.roles, name="bard")
		await user.add_roles(role)
		await ctx.send(f"{ user } is the bard now")
		bard_assigned.append(user)
	else:
		await ctx.send(f"Sorry, { bard_assigned[0].name } is the bard.(Bard can step down using <!unbardme> command )")

@bot.command(pass_context=True)
async def entercave(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["entercave"]:
		await ctx.send(":x:This command has been disabled")
		return
	user = ctx.message.author
	role = discord.utils.get(user.guild.roles, name="herd")
	await user.add_roles(role)
	

@bot.command(pass_context=True)
@commands.has_role('bard')
async def unbardme(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["unbardme"]:
		await ctx.send(":x:This command has been disabled")
		return
	user = ctx.message.author
	role = discord.utils.get(user.guild.roles, name="bard")
	await ctx.author.remove_roles(role)
	bard_assigned.pop()
	role = discord.utils.get(user.guild.roles, name="herd")
	await user.add_roles(role)

@bot.command(pass_context=True)
@commands.has_any_role('bard','herd')
async def leavecave(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["leavecave"]:
		await ctx.send(":x:This command has been disabled")
		return
	user = ctx.message.author
	role1 = discord.utils.get(user.guild.roles, name="bard")
	role2 = discord.utils.get(user.guild.roles, name="herd")
	if role1 in ctx.author.roles:
			await ctx.author.remove_roles(role1)
	if role2 in ctx.author.roles:
			await ctx.author.remove_roles(role2)
			bard_assigned.pop()


@bot.command(pass_context=True)  
@commands.has_role('herd')
async def bombard(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["bombard"]:
		await ctx.send(":x:This command has been disabled")
		return
	#print("hello")
	#print(bard_assigned)
	if(len(bard_assigned) == 0):
		user = ctx.message.author
		role = discord.utils.get(user.guild.roles, name="herd")
		#print(role.members)
		l = []
		for players in role.members:
			status0 = await status1(ctx,players)
			print(status0==discord.Status.online)
			if status0 == discord.Status.online:
				l.append(players)
		print(l)
		newbard = random.choice(l)
		role = discord.utils.get(newbard.guild.roles, name="bard")
		await newbard.add_roles(role)
		await ctx.send(f"{ newbard.name } is the bard now")
		bard_assigned.append(newbard)

	    # empty = True
	    # for member in ctx.message.guild.members:
	    #     if role in member.roles:
	    #         await bot.say("{0.name}: {0.id}".format(member))
	    #         empty = False
	    # if empty:
	    #     await bot.say("Nobody has the role {}".format(role.mention))
	else:
		await ctx.send(f"Sorry, { bard_assigned[0].name } is the bard.(Bard can step down using <!unbardme> command )")


@bot.event
async def on_message(message):
	if(not(message.content.startswith("!"))):

		#new_game.invoke_AI()

		ctx = await bot.get_context(message)
		userInput = message.content
		try:
			if not commandsEnabled[str(ctx.guild.id)]["bombard"]:
				
				user = str(ctx.message.author).split("#")[0]
				# print(user)
				# print(new_game.story_teller.char_name)
				#role = discord.utils.get(user.guild.roles, name="bard")
				if(new_game.story_teller.char_name == user):
					new_game.recieve_from_teller(userInput)

		except:
			pass
	await bot.process_commands(message)

@bot.command(pass_context = True)
@commands.has_role("bard")
async def meadumbfuck(ctx):
	await ctx.send(new_game.story_teller.current_story)

@bot.command(pass_context = True)
@commands.has_role("herd")
async def me(ctx):
	my_cards = new_game.player_setup()
	for i in range(len(my_cards)):
		await ctx.send(str(i)+". "+my_cards[i])
	await ctx.send(str(i+1)+". Invoke A.I.")



@bot.command(pass_context = True)
@commands.has_role("bard")
async def startgame(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["startgame"]:
		await ctx.send(":x:This command has been disabled")
		return

	
	guilds = await bot.fetch_guilds(limit=150).flatten()
	print(guilds)
	for i in range(len(guilds)):
		await enabler1(guilds[i])
	await Toggle(ctx, "bombard", guilds[0])
	await Toggle(ctx, "leavecave", guilds[0])
	await Toggle(ctx, "entercave", guilds[0])
	await Toggle(ctx, "bardmeup", guilds[0])
	await Toggle(ctx, "unbardme", guilds[0])
	await Toggle(ctx, "startgame", guilds[0])


	user = ctx.message.author
	role = discord.utils.get(user.guild.roles, name="herd")
	#print(role.members)
	l = []
	for players in role.members:
		status0 = await status1(ctx,players)
		print(status0==discord.Status.online)
		if status0 == discord.Status.online:
			l.append(players)
	print(l)
	print(l[0].name)

	#### Game logic starts here ####
	# role = discord.utils.get(user.guild.roles, name="bard")
	storyteller = bard_assigned[0].name
	new_game.register_storyteller(storyteller)
	for player in l:
		new_game.register_user(player.name)

	story_start, story_end = new_game.start_procedure()
	
	await ctx.send(new_game.story_teller.current_story)

	print("\n========\n\n")
	print(story_start)
	print("\n\n========\n")

@bot.command(pass_context = True)
@commands.has_role("bard")
async def endgame(ctx):
	if not commandsEnabled[str(ctx.guild.id)]["endgame"]:
		await ctx.send(":x:This command has been enabled")
		return
	# guilds = await bot.fetch_guilds(limit=150).flatten()
	# print(guilds)
	# for i in range(len(guilds)):
	# 	await enabler1(guilds[i])
	await Toggle(ctx, "bombard", guilds[0])
	await Toggle(ctx, "leavecave", guilds[0])
	await Toggle(ctx, "entercave", guilds[0])
	await Toggle(ctx, "bardmeup", guilds[0])
	await Toggle(ctx, "unbardme", guilds[0])
	await Toggle(ctx, "startgame", guilds[0])


	####   Remove everyone's roles  ########


# @bot.command(pass_context=True)
# @commands.has_role('herd')
# async def leave_role(member):
#     role = discord.utils.get(member.guild.roles, name='herd')
#     await member.remove_roles(role)
#     await bot.say("{} has been muted from chat".format(user.name))


bot.run('Nzg5NTU0MTA5ODExNjU0NzA2.X9zvkA.LavhJpmXw0T_BkbMpVp89nt7n1M')


"""


import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("The bard is ready!")

client = discord.Client()

# @client.event
# async def on_ready():
# 	await ctx.send(f"{client.user} has connected...")

@bot.event()
async def on_member_join(ctx):
	print(f"{client.user} has connected...")
	member = ctx.message.author
	role = get(member.server.roles, name="herd")
	await bot.add_roles(member, role)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! this is the message")

@bot.command()
async def sup(ctx):
    await ctx.send("bhag chutiye Hello! this is the message")

bot.run('Nzg5NTU0MTA5ODExNjU0NzA2.X9zvkA.LavhJpmXw0T_BkbMpVp89nt7n1M')

"""