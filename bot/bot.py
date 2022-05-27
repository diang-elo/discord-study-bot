import discord
import json
from discord.ext import commands
from discord.utils import get
import asyncio

# client = discord.Client()
client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("!info | Technical#0001"))
    print("Bot is ready.")


@client.event
async def on_guild_join(guild):
    
    with open('info.json', 'r') as f:
        info = json.load(f)

    info[str(guild.id)] = {}
    
    with open('info.json', 'w') as f:
        json.dump(info, f, indent = 4)


@client.event
async def on_guild_remove(guild):
    with open('info.json', 'r') as f:
        info = json.load(f)

    info.pop(str(guild.id))

    with open('info.json', 'w') as f:
        json.dump(info, f, indent = 4)


#takes in 2 strings, makes arg the key and arg2 and value
@client.command()
async def add(ctx, arg, arg2):
    with open('info.json', 'r') as f:
        info = json.load(f)


    for item in info[str(ctx.guild.id)].items():
        if item[0] == arg:
            old = str(item[1])
            
            #change to previous answer right away

            # info[str(ctx.guild.id)][arg] = old
            # with open('info.json', 'w') as f:
            #     json.dump(info, f, indent = 4)


            emote = ["👍", "👎"]
            embed = discord.Embed(title="This question has already been answered, After 45 seconds the answer will changed based off the vote", description=old,colour=discord.Color(0xffc300))
            embed.add_field(name=("Current answer | vote 👎 to keep current answer"), value=(str(item[1])), inline = False)
            embed.add_field(name=("Proposed answer | vote 👍 to change to proposed answer"), value=(str(arg2)), inline = False)
            x = await ctx.send(embed=embed)
            for emoji in emote:
                await x.add_reaction(emoji)
            
            await asyncio.sleep(45)
            #need to add count


            

            new_x = await ctx.channel.fetch_message(x.id)
            up = get(new_x.reactions, emoji="👍")
            down = get(new_x.reactions, emoji="👎")

            
            # if up and up.count > down.count:
            #     print("it works")
            #     info[str(ctx.guild.id)][arg] = arg2  
            #     with open('info.json', 'w') as f:
            #         json.dump(info, f, indent = 4)
            #     print("after dump")
            if up and up.count > down.count:
                with open('info.json', 'r') as f:
                    fresh = json.load(f)
                fresh[str(ctx.guild.id)][arg] = arg2  
                
                with open('info.json', 'w') as f:
                    json.dump(fresh, f, indent = 4)
                await ctx.send(f"The answer has been changed to the propsed answer: {ctx.author.name}")
                return None
            
            if down and down.count >= up.count:
                with open('info.json', 'r') as f:
                    fresh = json.load(f)
                fresh[str(ctx.guild.id)][arg] = old  
                
                with open('info.json', 'w') as f:
                    json.dump(fresh, f, indent = 4)
                await ctx.send(f"The current answer still remains: {ctx.author.name}")
                return None
                # arg2 = old
           
        
    
    info[str(ctx.guild.id)][arg] = arg2    
    await ctx.send(f"Your question and answer has been recorded: {ctx.author.name}")

    with open('info.json', 'w') as f:
        json.dump(info, f, indent = 4)
    

@client.command()
async def check(ctx, arg):
    with open('info.json', 'r') as f:
        info = json.load(f)

    # for item in info[str(ctx.guild.id)].items():
    #     print(item[1])
    for item in info[str(ctx.guild.id)].items():
        if item[0] == arg:
            # await ctx.send("The answer is: " + (str(item[1])))
            answer = (str(item[1]))
            question = str(item[0])
            embed = discord.Embed(title="Question", description=question,colour=discord.Color(0xffc300))
            embed.add_field(name="Answer", value=answer)
            # embed.set_thumbnail(url = 'https://i.pinimg.com/originals/91/c4/6c/91c46cf34db636debabd85f1090841d0.jpg')
            embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
   
    await ctx.send("If answer is not above this message, no answer has been provided yet")


@client.command()
async def all(ctx):
    with open('info.json', 'r') as f:
        info = json.load(f)
    
    embed = discord.Embed(title="All questions and answers",colour=discord.Color(0xffc300))
    counter = 0
    for item in info[str(ctx.guild.id)].items():
        counter += 1
        answer = (str(item[1]))
        question = str(item[0])
        embed.add_field(name=("Question " + str(counter)), value=question, inline = False)
        embed.add_field(name=("Answer "), value=answer, inline = False)
    await ctx.send(embed=embed)    
reactions = ["👍", "👎"]

@client.command()
async def info(ctx):
    embed = discord.Embed(title="Bot Commands", description="The purpose of this bot is to post the correct question and answer, as well as being able to check questions. Only add a question and answer if you are 100% certain of the answer.", colour=discord.Color(0xffc300)) #,color=Hex code
    embed.add_field(name = "!add | Command to Add inputed Question to Corresponding inputed Answer", value = "Both question and answer must be in quotations seperated by space ", inline = False)
    embed.add_field(name = "example", value = "!add \"This is how you add your question\" \"and answer\"", inline = False)
    embed.add_field(name = "!check | Command to Check an inputed Question", value = "Must be in quotation", inline = False)
    embed.add_field(name = "example", value = "!check \"This is where you enter your question\"", inline = False)
    embed.add_field(name = "!all | (Shows All Questions and Answers)",value=".", inline = False)
    
    

    x = await ctx.send(embed=embed)
    await x.add_reaction("👍")


# @client.event
# async def on_n(message):












client.run('')
