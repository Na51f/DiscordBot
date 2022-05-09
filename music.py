import discord
from discord.ext import commands
import youtube_dl


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.paused = False

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await ctx.voice_client.move_to(vc)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send('Disconnected.')

    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1'
                                            '-reconnect_delay_max 5', 'options': '-vn'}
        vdl_options = {'format':"bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(vdl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
            vc.play(source)

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
    client.add_cog(Music(client))
