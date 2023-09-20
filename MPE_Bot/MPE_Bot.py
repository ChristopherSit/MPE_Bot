import discord
from discord.ext import tasks
import workers
import helpers
import queue
import time
import asyncio
from structs import Signal

intents = discord.Intents.all()
intents.message_content = True
event_queue = queue.Queue()
client = discord.Client(intents=intents)
emojiNumbers = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # create event queue
    workers.onStartup(event_queue, client)
    # channel = client.get_channel(1151228286630899744)
    # await channel.send('Hello i have booted')
    event_handler.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('<@1151222704909852673> hello')
        event_queue.put(Signal(event='weeklyReset',
                                   payload='none'))
        event_queue.put(Signal(event='dailyReset',
                                   payload='none'))

@tasks.loop(seconds=5)
async def event_handler():
    channel = client.get_channel(1151228286630899744)
    try:
        eventSignal = event_queue.get(False) # Non blocking call
        if(eventSignal.event == 'dailyReset'):
            message = await channel.send('Daily Reset time + Time to next Reset is: ' + str(eventSignal.payload))
            for emoji in emojiNumbers:
                await message.add_reaction(emoji)
            mpe_event_handler.start(message)
            mpe_event_cleaner.start(message)

        elif(eventSignal.event == 'weeklyReset'):
            message = await channel.send('Weekly Reset time + Time to next Reset is: ' + str(eventSignal.payload))
        
        elif(eventSignal.event == 'mpeGroupFound'):
            message = await channel.send('MPE group found')

    except queue.Empty:
            pass
    
@event_handler.before_loop
async def before_event_handler():
    print('waiting')
    await client.wait_until_ready()

@tasks.loop(seconds=10, count=480)
async def mpe_event_handler(mpeMessage):
    await asyncio.sleep(2)
    reactors = []
    cached_message = discord.utils.get(client.cached_messages, id=mpeMessage.id)
    try:
        for reaction in cached_message.reactions:
            if(reaction.count >= 2):
                async for user in reaction.users():
                    if(user.name != 'MPE_Bot'):
                        reactors.append(user)
                for reaction in cached_message.reactions:
                    async for user in reaction.users():
                        if(user in reactors):
                            await cached_message.remove_reaction(emoji=reaction.emoji, member=user)
                event_queue.put(Signal(event='mpeGroupFound',
                                    payload = reactors))
                reactors = []
                break
    except Exception: 
        pass

@tasks.loop(count=9)
async def mpe_event_cleaner(mpeMessage):
    await asyncio.sleep(60)
    cached_message = discord.utils.get(client.cached_messages, id=mpeMessage.id)
    reaction = cached_message.reactions[0]
    async for user in reaction.users():
        await cached_message.remove_reaction(emoji=reaction.emoji, member=user)

client.run('MTE1MTIyMjcwNDkwOTg1MjY3Mw.GJMwxL.9cxKVDMgq-G2mWkwXsd1Rcd9y0Zi3w33e9xqyo')