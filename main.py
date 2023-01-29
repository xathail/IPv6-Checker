# Imports
import discord
import socket
import requests
from colorama import Fore
from datetime import datetime

# Setup Bot
bot = discord.Bot(activity = discord.Game(name="Around With IPv6 | By xerius"), status=discord.Status.idle)
print(Fore.GREEN+"[Bot Online]")

# Ping Command
@bot.command(description="Ping? Pong!")
async def ping(ctx):
    embed = discord.Embed(title="Bot Ping:", description=f"The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44 if round(bot.latency * 1000) <= 50 else 0xffd000 if round(bot.latency * 1000) <= 100 else 0xff6600 if round(bot.latency * 1000) <= 200 else 0x990000)
    await ctx.respond(embed=embed)
    
# Check Command
@bot.command(description="Checks IPv6 & Cloudflare Compatibility")
async def check(ctx, domain: str):
    print(Fore.LIGHTMAGENTA_EX + f"[Command Used: 'check']" + Fore.RED + f"[User: {ctx.author.name}#{ctx.author.discriminator}]" + Fore.YELLOW + f"[Domain: {domain}]" + Fore.BLUE + f"[Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]" + Fore.CYAN + f"[Server: {ctx.guild.name}]")
    domain = domain.replace("http://","").replace("https://","").replace("www.","") # Removes http://, https:// and www.
    head, sep, tail = domain.partition('/')
    domain = head
    try:
        ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6) # Tries To Get IPv6 Address
        domain = "http://"+domain # Setup For CF Request
        try:
            response = requests.get(domain, timeout=2)
            if 'cf-ray' in response.headers: # If Site Uses Cloudflare
                embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:white_check_mark: Cloudflare", color=0x32CD32)
                embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
                await ctx.respond(embed=embed)

            else: # If Site Doesn't Use Cloudflare
                embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:white_check_mark: Cloudflare", color=0x32CD32)
                embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
                await ctx.respond(embed=embed)
        except requests.exceptions.Timeout:
            embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:question: Cloudflare", color=0x32CD32)
            embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
            await ctx.respond(embed=embed)
        except requests.exceptions.RequestException:
            embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:question: Cloudflare", color=0x32CD32)
            embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
            await ctx.respond(embed=embed)           
    except socket.gaierror as e: # If An Error Occures Trying To Get IPv6 Address
        domain = 'www.'+domain 
        try:
            ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6)
            domain = domain.replace("www.","http://")
            try:
                response = requests.get(domain, timeout=2)
                if 'cf-ray' in response.headers:
                    embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:white_check_mark: Cloudflare", color=0x32CD32)
                    embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:white_check_mark: Cloudflare", color=0x32CD32)
                    embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
                    await ctx.respond(embed=embed)
            except requests.exceptions.Timeout:
                embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:question: Cloudflare", color=0x32CD32)
                embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
                await ctx.respond(embed=embed)
            except requests.exceptions.RequestException:
                embed = discord.Embed(title=f"{domain} Information", description=f"\n:white_check_mark: IPv6\n:question: Cloudflare", color=0x32CD32)
                embed.set_footer(text=f"IPv6 Address: {ipv6_address[0][4][0]}")
                await ctx.respond(embed=embed)           
        except socket.gaierror as e: # If There Is No IPv6 Address
            domain = domain.replace("www.","http://")
            try:
                response = requests.get(domain, timeout=2)
                if 'cf-ray' in response.headers:
                    embed = discord.Embed(title=f"{domain} Information", description=f"\n:x: IPv6\n:white_check_mark: Cloudflare", color=0xFF0000)
                    embed.set_footer(text=f"{e}")
                    await ctx.respond(embed=embed)
                else:
                    embed = discord.Embed(title=f"{domain} Information", description=f"\n:x: IPv6\n:x: Cloudflare", color=0xFF0000)
                    embed.set_footer(text=f"{e}")
                    await ctx.respond(embed=embed)
            except requests.exceptions.Timeout:
                embed = discord.Embed(title=f"{domain} Information", description=f"\n:x: IPv6\n:question: Cloudflare", color=0x32CD32)
                await ctx.respond(embed=embed)
            except requests.exceptions.RequestException:
                embed = discord.Embed(title=f"{domain} Information", description=f"\n:x: IPv6\n:question: Cloudflare", color=0x32CD32)
                await ctx.respond(embed=embed) 
    log_string = f"[Command Used: 'check']" + f"[User: {ctx.author.name}#{ctx.author.discriminator}]" + f"[Domain: {domain}]" + f"[Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]" + f"[Server: {ctx.guild.name}]"
    with open("command_logs.txt", "a") as f:
    	f.write(log_string + "\n")

# Runs Bot
bot.run("TOKEN")
