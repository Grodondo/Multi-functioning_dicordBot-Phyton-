import discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
import random
import os
import youtube_dl

class Soundtrack(commands.Cog):

    def __init__(self, client):
        self.client = client

    #@commands.cog.Listener           #Events
    #@commands.command                #Commands

    @commands.command(pass_context=True, aliases=["play"])              #Commands
    async def Play(self, ctx, url: str):
        #JOIN--------------------------------------------
        global voice
        song_played = os.path.isfile("song.mp3")
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            if song_played:
                pass
            else:
                await voice.move_to(channel)
        else: 
            voice = await channel.connect()
            print(f"The bot has connected to {channel}")
        #-------------------------------------------------
        try:
            if song_played:
                os.remove("song.mp3")
        except PermissionError:
            print("Trying to delete a song file, but its being played at the moment.")
            await ctx.send("Error: Music is being played at the moment.")
            return

        ydl_opts = {
            "format": "beataudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now...\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed file: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.value = 0.1
    
        new_name = name.rsplit("-", 2)
        await ctx.send(f"Playing {new_name}")

#--------------------------------------------------------------------------------------------------------------

    @commands.command(pass_context=True, aliases=["Leave"])              #Commands
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has been dissconnected from {channel}")
        else:   
            print("Client was not able to leave voice channel, becouse it wasnt on any.")
   
def setup(client):
    client.add_cog(Soundtrack(client))   
