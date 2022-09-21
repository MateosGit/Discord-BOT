from discord.ext import commands
import discord
import random
import asyncio

intents = discord.Intents.default()
client = discord.Client(intents=intents)

intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)
bot.author_id = 285116466565742594  # Change to your discord id


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    '''
        Pong
    '''
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    '''
        Bot command to send the name of the member calling the command
    '''
    await ctx.send(ctx.author.name)

@bot.command()
async def d6(ctx):
    '''
        Bot command to roll a 6 faces dice
    '''
    await ctx.send(random.randint(1, 6))

@bot.command()
async def admin(ctx, username):
    '''
        Bot command to add an Admin role (only if it doesn't exists) and assign it to the member having the username arg.
        Admin can kick and ban people.
    '''
    # If no username is specify the command end doing nothing
    if username is None:
        await ctx.send("You need to provide a username")
        return

    # find username member in the guild member list
    user = discord.utils.get(ctx.guild.members, name=username)

    if user is None: 
        await ctx.send("Can't find " + username)
        return

    roles = await ctx.guild.fetch_roles()

    # Looking for Admin role in the discord role list
    new_role = None
    for role in roles:
        if role.name == "Admin":
            new_role = role
            break
    
    # if admin role doesn't exists
    if new_role is None:
        await ctx.send("Creating Admin role")
        # Creating admin role 
        new_role = await ctx.guild.create_role(name="Admin")

        # Adding permissions to admin role
        permissions = discord.Permissions()
        permissions.update(kick_members=True)
        permissions.update(manage_channels=True)
        permissions.update(ban_members=True)

        # attach permission to admin role
        await new_role.edit(permissions=permissions)
    
    # Giving username the admin role
    await user.add_roles(new_role)

    await ctx.send(username + " has now Admin role")

@bot.command()
async def ban(ctx, username):
    '''
        Bot command to ban some. Don't test this command on yourself. Please.
    '''
    # if no username is specify
    if username is None:
        await ctx.send("You need to provide a username")
        return

    user = discord.utils.get(ctx.guild.members, name=username)

    # if user doesn't exist in this discord
    if user is None: 
        await ctx.send("Can't find " + username)
        return

    await user.ban(reason="La racaille ça degage")

    await ctx.send("Adieu " + username)

@bot.command()
async def count(ctx):
    '''
        Bot command to count the number of people for each status
    '''
    # Retrieving all discord member list
    members = ctx.guild.members
    if members is None:
        return
    
    count_dict = {}

    for member in members:
        if count_dict.get(member.raw_status) is None:
            count_dict[member.raw_status] = 1
        else:
            count_dict[member.raw_status] += 1
    
    res = ""

    for name, count in count_dict.items():
        res += str(count) + " members are " + name + ", "

    await ctx.send(res)

@bot.command()
async def xkcd(ctx):
    '''
        Bot command to send a random comic from https://xkcd.com/
    '''
    await ctx.send("https://xkcd.com/" + str(random.randint(1, 1000)) + "/")

@bot.command()
async def poll(ctx, question, time_in_seconds: int = 5):
    '''
        Bot command to add poll. time_in_seconds is the number of second the bot will waiting until sending the poll result
    '''
    await ctx.send(content = "@here " + question + " (" + str(time_in_seconds) + " seconds remaining)", 
        allowed_mentions = discord.AllowedMentions(everyone=True))

    poll_message = await ctx.send(question)

    await poll_message.add_reaction('👍')
    await poll_message.add_reaction('👎')

    await asyncio.sleep(time_in_seconds)

    # reloading poll message after sleep to get reactions
    poll_message = await ctx.fetch_message(poll_message.id)
    reactions = poll_message.reactions

    up = reactions[0].count - 1
    down = reactions[1].count - 1

    # Delete poll message
    await poll_message.delete()
    await ctx.send(str(up) + " people voted " + "👍 and " + str(down) + " voted 👎")


@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        await message.channel.send("Salut tout seul " +  message.author.mention)

    # Sans cette ligne ne bot ne pourra plus lire les messages pour les commandes
    await bot.process_commands(message)

token = "MTAyMjE5MjcwOTkyNDA0MDg1NQ.GRQEp4.9Ieump3krnUTpfFeRWwcqIg5jPcgRWkHIM4ri8"
bot.run(token)  # Starts the bot