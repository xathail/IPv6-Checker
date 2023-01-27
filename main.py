import discord
import socket

bot = discord.Bot()

@bot.command()
async def check(ctx, domain: discord.Option(discord.SlashCommandOptionType.string)):
    try:
        ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6)
        embed = discord.Embed(title=f'{domain} Supports IPv6:', description=f'IPv6 Address: {ipv6_address[0][4][0]}', color=0x32CD32)
        await ctx.respond(embed=embed)
    except socket.gaierror as e:
        embed = discord.Embed(title=f'Error Finding Compatibility:', description=f'{e}', color=0xFF0000)
        await ctx.respond(embed=embed)
bot.run("TOKEN")
