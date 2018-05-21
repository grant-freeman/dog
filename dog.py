import discord
from discord.ext import commands
import asyncio
import requests
import random
import config

bot = commands.Bot(command_prefix='d!', description='dog bot')
REACT_LIST = ['\U0001F44D', '\U0001F44E', '\U0001F937']
TERF_RESPONSES = ['https://cdn.discordapp.com/attachments/415296704376733698/447919447580213278/image.jpg',
'https://cdn.discordapp.com/attachments/415296704376733698/447953199689891850/image.jpg',
"don't be shitty!! trans women are not a fetish!!"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def dog(*breed: str):
    breed_str = urlify(breed)
    if breed_str == '':
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        json = r.json()
        embed = discord.Embed(title='Dog!', color=0xDEADBF)
        embed.set_author(name='dog', icon_url=bot.user.avatar_url)
        embed.set_image(url=json['message'])
        await bot.say(embed=embed)
    else:
        r = requests.get(f'https://dog.ceo/api/breed/{breed_str}/images/random')
        if r.status_code == requests.codes['ok']:
            json = r.json()
            embed = discord.Embed(title='Dog!', color=0xDEADBF)
            embed.set_author(name='dog', icon_url=bot.user.avatar_url)
            embed.set_image(url=json['message'])
            await bot.say(embed=embed)
        else:
            await bot.say('Invalid breed name!!')

@bot.command(pass_context=True)
async def poll(ctx, *question: str):
    await bot.say(responsify(question))
    async for message in bot.logs_from(ctx.message.channel, limit=2):
        if message.author == bot.user:
            for i in REACT_LIST:
                await bot.add_reaction(message, i)

@bot.command(pass_context=True)
async def say(ctx, *say: str):
    await bot.delete_message(ctx.message)
    await bot.say(responsify(say) + '!!')

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    await bot.say(random.choice(choices))

@bot.command(pass_context=True)
async def bite(ctx):
    await bot.say(f'*bites {ctx.message.mentions[0].mention}*')

def responsify(raw_response):
    tmp = list(raw_response)
    clean_response = ' '.join(tmp)
    return clean_response

def urlify(raw_response):
    tmp = reversed(list(raw_response))
    clean_response = '/'.join(tmp)
    return clean_response

def embedify(img_url):
    embed = discord.Embed(title='No terfs allowed', color=0xDEADBF)
    embed.set_image(url=img_url)
    return embed

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'traps' in message.content or 'trap' in message.content:
        tmp = random.choice(TERF_RESPONSES)
        if tmp[:5] == 'https':
            await bot.send_message(message.channel, embed=embedify(tmp))
        else:
            await bot.send_message(message.channel, tmp)

# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('d!test'):
#         counter = 0
#         tmp = await client.send_message(message.channel, 'Calculating messages...')
#         async for log in client.logs_from(message.channel, limit=100):
#             if log.author == message.author:
#                 counter += 1
#         await client.edit_message(tmp, 'You have {} messages.'.format(counter))

#     elif message.content.startswith('d!sleep'):
#         await asyncio.sleep(5)
#         await client.send_message(message.channel, 'Done sleeping')

#     elif message.content.startswith('d!dog'):
#         r = requests.get('https://dog.ceo/api/breeds/image/random')
#         json = r.json()
#         embed = discord.Embed(title='Dog!', color=0xDEADBF)
#         embed.set_author(name='dog', icon_url=client.user.avatar_url)
#         embed.set_image(url=json['message'])
#         await client.send_message(message.channel, embed=embed)

#     elif message.content.startswith('d!poll'):
#         await client.send_message(message.channel, message.content.)

#     elif 'dog' in message.content or 'woof' in message.content or client.user.id in message.content:
#         await client.send_message(message.channel, 'woof')

bot.run(config.token)
