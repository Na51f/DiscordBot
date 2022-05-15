import discord
from discord.ext import commands
import os
import urllib.request
import re
import validators
import yt_dlp


class Bot(commands.Cog):
    paused = False

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def repeat(self, ctx, *, args):
        await ctx.send(args)

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vc.connect()
        else:
            await ctx.voice_client.move_to(vc)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        await self.join(ctx)

        url = search(args)

        vc = ctx.voice_client
        song_is_there = os.path.isfile("./resources/queues/song.mp3")
        try:
            if song_is_there:
                os.remove("./resources/queues/song.mp3")
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

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.replace(file, "./resources/queues/" + file)
                os.rename("./resources/queues/" + file, "./resources/queues/song.mp3")
        vc.play(discord.FFmpegPCMAudio("./resources/queues/song.mp3"))

    @commands.command(aliases=['leave', 'quit', 'stop', 'dc', 'skip'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected.')

    @commands.command()
    async def pause(self, ctx):
        if Bot.paused is False:
            await ctx.voice_client.pause()
            await ctx.send('Paused.')
            self.paused = True
        else:
            await ctx.voice_client.resume()
            await ctx.send('Resumed.')
            self.paused = False

    @commands.command(aliases=['pl', 'playlast'])
    async def play_last(self, ctx):
        await self.join(ctx)
        vc = ctx.voice_client
        vc.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command()
    async def backflip(self, ctx):
        await ctx.send('```*Does a backflip*```')
        await ctx.send('https://tenor.com/view/teamwork-back-flip-wearing-pants-gif-16289206')


def setup(client):
    client.add_cog(Bot(client))


def search(args):
    s = ' '.join(args).strip()
    if validators.url(s):
        return s

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + s.replace(" ", "+"))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    return "https://www.youtube.com/watch?v=" + video_ids[0]
