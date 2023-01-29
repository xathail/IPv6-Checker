# Imports
import discord
import socket
import requests
from colorama import Fore
from datetime import datetime, timedelta

# Setup Bot
bot = discord.Bot(activity = discord.Game(name="Around With IPv6 | By xerius"), status=discord.Status.idle)
print(Fore.GREEN+"[Bot Online]")



@bot.command()
async def txinfo(ctx, crypto: str, txid: str):
    crypto = crypto.lower()
    api_url = f'https://api.blockcypher.com/v1/{crypto}/main/txs/{txid}'
    response = requests.get(api_url)
    if response.status_code != 200:
        await ctx.respond(f"Transaction ID not found. Please check the input and try again.")
        return
    transaction_info = response.json()
    amount = transaction_info['total'] / 100000000
    embed = discord.Embed(title=f'Transaction Information ({crypto.upper()})',
                          color=discord.Color.green(),
                          description=f'Transaction ID: {txid}')
    embed.add_field(name='Confirmations:', value=transaction_info['confirmations'], inline=True)
    embed.add_field(name='Amount:', value=f'{amount:.8f} {crypto.upper()}', inline=True)
    embed.set_footer(text='Do Not Code When Tired!')
    await ctx.respond(embed=embed)


    
@bot.command()
async def wallet_info(ctx, crypto: str, wallet_address: str):
    crypto = crypto.lower()
    api_url = f'https://api.blockcypher.com/v1/{crypto}/main/addrs/{wallet_address}'
    response = requests.get(api_url)
    wallet_info = response.json()
    tx = wallet_info['txrefs'][0]
    timestamp = tx['confirmed'].split("T")[0] + " " + tx['confirmed'].split("T")[1][:-1]
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    timestamp_seconds = int(timestamp.timestamp()) + 3600
    embed = discord.Embed(title=f'Wallet Information ({crypto.upper()})',
                          color=discord.Color.green(),
                          description=f'Wallet Address: {wallet_address}')
    embed.add_field(name='Most Recent Transaction:', value=tx['tx_hash'], inline=True)
    embed.add_field(name='Amount Received:', value=f'{tx["value"]/10**8:.8f} {crypto.upper()}', inline=True)
    embed.add_field(name='Transaction Timestamp:', value=f'<t:{timestamp_seconds}:f>', inline=True)
    embed.set_footer(text='Do Not Code When Tired')
    await ctx.respond(embed=embed)





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
