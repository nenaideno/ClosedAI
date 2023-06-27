import os
import discord
from dotenv import load_dotenv
import openai

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')
CREATOR_ID = os.getenv("CREATOR_ID")

users = {}

def generate_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt, }], max_tokens=1024)
    return completion.choices[0].message.content


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content:
        if (message.author.id not in users):
            users[f'{message.author.name}#{message.author.discriminator}'] = message.author.id

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    elif (message.content.startswith('/попуск')):
        bot_response = await message.channel.send(f""" 
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    Занят. Генерирую ответ для {message.author.mention}...
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛""")
        print(f'ID{message.author.id} : {message.content[8:]}')
        response = generate_response(message.content[8:])
        print(f'Сообщение чата: {response}')
        await bot_response.delete()
        bot_response = await message.channel.send(f"{message.author.mention}, {response}")
        # await bot_response.edit(content=response)
    elif (message.content.startswith('/ai')):
        bot_response = await message.channel.send(f""" 
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    Занят. Генерирую ответ для {message.author.mention}...
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛""")
        print(f'ID{message.author.id} : {message.content[4:]}')
        response = generate_response(message.content[4:])
        print(f'Сообщение чата: {response}')
        await bot_response.delete()
        bot_response = await message.channel.send(f"{message.author.mention}, {response}")
        # await bot_response.edit(content=response)
    elif (message.content.startswith('\\') and (message.author.id == int(CREATOR_ID))):
        if (message.content[1:4] == 'ban'):
            print(f'ID{message.author.id} : {message.content[5:]}')
            if message.content[5:] in users:           
                user = await discord.utils.find(users[message.content[5:]])
                await message.guild.ban(user.id)
                await message.channel.send(f'Пользователь {user.name} был забанен.')
        else:
            print(users)
            bot_response = await message.channel.send(f""" 
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    Занят. Генерирую ответ для {message.author.mention}...
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛""")
            print(f'ID{message.author.id} : {message.content[2:]}')
            response = generate_response(message.content[2:])
            print(f'Сообщение чата: {response}')
            await bot_response.delete()
            bot_response = await message.channel.send(f"{message.author.mention}, {response}")
    

        # await bot_response.edit(content=response)

client.run(TOKEN)
