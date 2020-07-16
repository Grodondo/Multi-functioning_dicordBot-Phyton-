import discord
from discord.ext import commands

class balance(commands.Cog):

    def __init__(self, client):
        self.client = client

    #@commands.cog.Listener           #Events
    #@commands.command()              #Commands


def setup(client):
    client.add_cog(balance(client))   
