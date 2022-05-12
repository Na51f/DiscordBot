import discord
from discord.ext import commands
import youtube_dl
import ffmpeg
import os


class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.paused = False

    @commands.command()
    async def repeat(self, ctx, arg):
        await ctx.send(arg)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vc.connect()
        else:
            await ctx.voice_client.move_to(vc)

    @commands.command(aliases=['p'])
    async def play(self, ctx, url):
        await self.join(ctx)
        vc = ctx.voice_client
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        vc.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command(aliases=['leave', 'quit', 'stop'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected.')

    @commands.command()
    async def pause(self, ctx):
        if self.paused is False:
            await ctx.voice_client.pause()
            await ctx.send('Paused.')
            self.paused = True
        else:
            await ctx.voice_client.resume()
            await ctx.send('Resumed.')
            self.paused = False


def setup(client):
    client.add_cog(Bot(client))
