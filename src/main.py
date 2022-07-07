import discord

TOKEN = 'OTk0NzM4NDg0NzMwNDE3MzEz.GskNCF.3JAxRtDT2AtSWrZ2doN48SvywLf-VjSob2iWnI'
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


client.run(TOKEN)