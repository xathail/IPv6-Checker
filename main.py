import discord
import socket
import requests

bot = discord.Bot(activity = discord.Game(name="Around With IPv6 | By xerius"), status=discord.Status.idle)
print("Bot Online!")

@bot.command(description="Sends the bot's latency.")
async def ping(ctx):
    embed = discord.Embed(title="Bot Ping:", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44 if round(bot.latency * 1000) <= 50 else 0xffd000 if round(bot.latency * 1000) <= 100 else 0xff6600 if round(bot.latency * 1000) <= 200 else 0x990000)
    await ctx.respond(embed=embed)
    
@bot.command(description="Check a domain to see if it supports cloudflare.")
async def cloudflare(ctx, domain: str):
    domain = domain if 'https://' in domain or 'http://' in domain else 'http://'+domain
    response = requests.get(domain)
    embed = discord.Embed(title=f'{domain} Uses Cloudflare' if 'cf-ray' in response.headers else f'{domain} Does Not Use Cloudflare', color=0x32CD32 if 'cf-ray' in response.headers else 0xFF0000)
    await ctx.respond(embed=embed)

@bot.command(description="Check a domain to see if it supports IPv6.")
async def check(ctx, domain: discord.Option(discord.SlashCommandOptionType.string)):
    domain = domain.replace("http://","").replace("https://","").replace("www.","")
    try:
        ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6)
        embed = discord.Embed(title=f'{domain} Supports IPv6', description=f'IPv6 Address: {ipv6_address[0][4][0]}', color=0x32CD32)
        await ctx.respond(embed=embed)
    except socket.gaierror as e:
        domain = 'www.'+domain
        try:
            ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6)
            embed = discord.Embed(title=f'{domain} Supports IPv6', description=f'IPv6 Address: {ipv6_address[0][4][0]}', color=0x32CD32)
            await ctx.respond(embed=embed)
        except socket.gaierror as e:
            embed = discord.Embed(title=f'Error Finding Compatibility', description=f'I was unable to find IPv6 compatibility for the domain {domain} \n\n*{e}*', color=0xFF0000)
            await ctx.respond(embed=embed)

bot.run("TOKEN")
