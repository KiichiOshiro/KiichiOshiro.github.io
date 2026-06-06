import discord
import asyncio
from discord.ext import commands

TOKEN = "BOTのトークン"
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def call(ctx, member: discord.Member, channel_name: str = None):
    """特定のユーザーに通話のリンクを送るコマンド"""
    if channel_name:
        channel = discord.utils.get(ctx.guild.voice_channels, name=channel_name)
        if not channel:
            await ctx.send(f"🔴 ボイスチャンネル '{channel_name}' が見つかりません。")
            return
    else:
        channel = ctx.guild.voice_channels[0] if ctx.guild.voice_channels else None

    if not channel:
        await ctx.send("🔴 サーバーにボイスチャンネルがありません。")
        return

    invite = await channel.create_invite(max_age=300)
    message = f"{member.mention} さん、通話に参加してください！\n🔗 {invite.url}"
    attempts = 0

    while True:
        attempts += 1
        try:
            await member.send(f"[Attempt {attempts}] {message}")
            await ctx.send(f"✅ {member.mention} に通話リンクを送りました！『{attempts}回目』",delete_after=30)
        except discord.Forbidden:
            await ctx.send(f"❌ {member.mention} に DM を送ることができません。")
            return

        await asyncio.sleep(3)

        if member in channel.members:
            await ctx.send(f"🎉 {member.mention} が通話に参加しました！")
            break

bot.run(TOKEN)
