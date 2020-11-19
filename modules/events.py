import discord
import json
from discord.ext import commands
from datetime import datetime
from json import load, dump

welcomeChannel = '' # Welcome channel ID (without ', only ID, need to be a integer)
autoRole = '' # Name of role to autorole when a member join the server
helpCommand = 'ajuda' # Put here the name or alias of default help command
eventsChannel = '' # Put here ID of events channel, need to be a integer
botID = '' # Put here bot ID, need to be a integer

class Events(commands.Cog, name = 'Eventos'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member): # When a member join the server
        # Welcome message
        e = discord.Embed(colour = 0x3AFE00, timestamp = datetime.utcnow())
        e.set_author(name = member, icon_url = member.avatar_url)
        e.add_field(name = 'Bem-vindo(a)!', value = f'{member.mention}, seja bem vindo(a) ao {member.guild.name}! Use {self.client.command_prefix}{helpCommand} para ver a lista de comandos!')
        e.set_image(url = member.guild.icon_url)
        e.set_footer(icon_url = member.avatar_url, text = f'ID: {member.id}')
        await self.client.get_channel(welcomeChannel).send(embed = e)

        # Autorole
        role = discord.utils.get(member.guild.roles, name = autoRole)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message_delete(self, ctx): # When a member delete a message
        # Discord return
        if ctx.author.id != botID:
            e = discord.Embed(colour = 0xFE0000, timestamp = datetime.utcnow())
            e.set_author(name = '📌 Mensagem deletada')
            e.add_field(name = '📝 Mensagem', value = f'`{str(ctx.content)}`')
            e.set_footer(icon_url = ctx.author.avatar_url, text = f'{ctx.author.name}#{ctx.author.discriminator}')
            await self.client.get_channel(eventsChannel).send(embed = e)

            # Console return
            print('\n', f'-'*30)
            print(f'\n[+] A message has deleted!\n\nLog: Author: {ctx.author}')
        else:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, ctx, after): # When a member edit a message
        # Discord return
        if ctx.author.id != botID:
            e = discord.Embed(colour = 0xFE0000, timestamp = datetime.utcnow())
            e.set_author(name = '📌 Mensagem modificada')
            e.add_field(name = '⏪ Antes', value = f'`{str(ctx.content)}`')
            e.add_field(name = '⏩ Depois', value = f'`{str(after.content)}`')
            e.set_footer(icon_url = ctx.author.avatar_url, text = f'{ctx.author.name}#{ctx.author.discriminator}')
            await self.client.get_channel(eventsChannel).send(embed = e)

            # Console return
            print('\n', f'-'*30)
            print(f'\n[+] A message has modified!\n\nLog: Author: {ctx.author}')
        else:
            pass

# Cog setup
def setup(client):
    client.add_cog(Events(client))