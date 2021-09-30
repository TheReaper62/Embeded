import discord
from discord.ext import commands
from discord.app import slash_command

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @slash_command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.respond(f'Hello {member.name}~')
        else:
            await ctx.respond(f'Hello {member.name}... This feels familiar.')
        self._last_member = member

def setup(client):
    client.add_cog(Greetings(client))
