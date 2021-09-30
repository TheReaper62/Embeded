import os, socket, asyncio
import random
import discord
from discord.ext import commands

client = commands.Bot(command_prefix="|")

# Load Modules
def return_available_extensions():
    ActiveModules = []
    InActiveModules = ["functionals"]
    for filename in os.listdir('./modules'):
        try:
            if filename[:-3] in InActiveModules or filename[-3:] != ".py":
                continue
            ActiveModules.append(filename[:-3])
        except Exception as e:
            print(f"{filename} could not be loaded due to an error: {e}")
    return ActiveModules
for i in return_available_extensions():
    print(f"Loading {i}...")
    client.load_extension(f"modules.{i}")

local_restarts = 0

@client.event
async def on_ready():
    global local_restarts
    status_log_chan = client.get_channel(876714045208678400)
    await status_log_chan.send(embed=discord.Embed(title="Embeded Status Update",description=f"Running on `{socket.gethostname()}`\nLocal Restart: `{local_restarts}`"))
    local_restarts+=1

async def change_p():
	await client.wait_until_ready()
	statuses = [
	    f"{len(client.guilds)} Servers",
	    f"Latency: {round(client.latency*1000)}ms"
	]
	while not client.is_closed():
		await client.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.watching, name=random.choice(statuses)))
		await asyncio.sleep(2)

client.loop.create_task(change_p())
client.run(os.getenv("discord_auth"))
