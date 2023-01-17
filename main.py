import discord
import socket
bot = discord.Bot()

@bot.command()
async def check(
  ctx,
  domain: discord.Option(discord.SlashCommandOptionType.string)
):
    try:
        ipv6_address = socket.getaddrinfo(domain, None, socket.AF_INET6)
        await ctx.respond(f':white_check_mark: {domain} supports IPv6')
    except:
        await ctx.respond(f':x: {domain} does not support IPv6')

bot.run("MTA2NDU4MTcxNjc3OTQ3MDg4OQ.GQab44.dINa6h2ZIzy8OppQmI8BWEMAL3Ugn_5QDO6BZI")
