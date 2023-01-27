import discord
import socket
import requests

bot = discord.Bot()

@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(title="Bot Ping:", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(title="Bot Ping:", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
        embed=discord.Embed(title="Bot Ping:", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="Bot Ping:", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.respond(embed=embed)
    
@bot.command(description="Check a domain to see if it supports cloudflare.")
async def cloudflare(ctx, domain: str):
    if 'https://' in domain or 'http://' in domain: 
        response = requests.get(domain)
        if 'cf-ray' in response.headers:
            embed = discord.Embed(title=f'{domain} Uses Cloudflare', color=0x32CD32)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=f'{domain} Does Not Use Cloudflare', color=0xFF0000)
            await ctx.respond(embed=embed)
    else:
        domain = 'http://'+domain
        response = requests.get(domain)
        if 'cf-ray' in response.headers:
            embed = discord.Embed(title=f'{domain} Uses Cloudflare', color=0x32CD32)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=f'{domain} Does Not Use Cloudflare', color=0xFF0000)
            await ctx.respond(embed=embed)
    
@bot.command(description="Check a domain to see if it supports IPv6.")
async def ipv6(ctx, domain: discord.Option(discord.SlashCommandOptionType.string)):
    try:
        ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6)
        embed = discord.Embed(title=f'{domain} Supports IPv6', description=f'IPv6 Address: {ipv6_address[0][4][0]}', color=0x32CD32)
        await ctx.respond(embed=embed)
    except socket.gaierror as e:
        embed = discord.Embed(title=f'Error Finding Compatibility:', description=f'{e}', color=0xFF0000)
        await ctx.respond(embed=embed)
        
bot.run("TOKEN")
