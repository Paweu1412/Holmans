import discord
import requests
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.custom, state="Byłem tu, tam i tam")
    await bot.change_presence(activity=activity)

@bot.command()
async def mem(ctx):
    requestMeme = requests.get('https://ivall.pl/memy')
    if requestMeme:
        json_data = requestMeme.json()
        image_url = json_data['url']
        if json_data and image_url:
            await ctx.send(image_url)


@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name="Niezarejestrowany")
    if role:
        await member.add_roles(role)

        embed = discord.Embed(title=member.name + "#" + member.discriminator + " witaj w Holman's Motel Community!",
                              description="Wybierz sobie odpowiednią rangę: mieszkańca - jeśli wynajmujesz pokój lub gościa - jeśli chcesz integrować się i być na bieżąco.",
                              color=0xff0000)
        embed.add_field(name="Wybierz, jeśli jesteś mieszkańcem:",
                        value="!rejestruj <imię i nazwisko ic> <numer mieszkania>")
        embed.add_field(name="Wybierz, jeśli jesteś gościem:", value="!rejestruj")
        channel_by_id = discord.utils.get(bot.get_all_channels(), name="rejestracja")

        if channel_by_id:
            search_role = get(member.guild.roles, name="Holman")
            if search_role:
                await channel_by_id.send(search_role.mention + " attention, attention!" + member.mention, embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.AttributeError):
        


@bot.command()
@commands.has_role("Niezarejestrowany")
async def rejestruj(ctx, arg1="not typed", arg2="not_typed", arg3="not_typed"):
    if arg1 != "not_typed" and arg2 != "not_typed" and arg1 != "not_typed":
        await ctx.guild.create_role(name=arg1 + " " + arg2, color=0xffffff)
        name_role = get(ctx.guild.roles, name=arg1 + " " + arg2)
        await ctx.author.add_roles(name_role)

        role = get(ctx.guild.roles, name="Niezarejestrowany")
        await ctx.author.remove_roles(role)

        role_apartment = get(ctx.guild.roles, name="Apartment No. " + arg3)
        await ctx.author.add_roles(role_apartment)

        role_mieszkaniec = get(ctx.guild.roles, name="Mieszkaniec")
        await ctx.author.add_roles(role_mieszkaniec)

        embed = discord.Embed(
            title=ctx.author.name + "#" + ctx.author.discriminator + " zarejestrował się w Holman's Motel Community!",
            description="Baw się dobrze, integruj, rozmawiaj.. rób wszystko, ale mając na uwadze pewne granice.",
            color=0xff0000)
        channel_by_id = discord.utils.get(bot.get_all_channels(), name="off-topic")
        await channel_by_id.send(embed=embed)
    elif arg1 == "not_typed" or arg2 == "not_typed" or arg3 == "not_typed":
        role = get(ctx.guild.roles, name="Niezarejestrowany")
        await ctx.author.remove_roles(role)

        role_mieszkaniec = get(ctx.guild.roles, name="Gość")
        await ctx.author.add_roles(role_mieszkaniec)

        embed = discord.Embed(
            title=ctx.author.name + "#" + ctx.author.discriminator + " zarejestrował się w Holman's Motel Community!",
            description="Baw się dobrze, integruj, rozmawiaj.. rób wszystko, ale mając na uwadze pewne granice.",
            color=0xff0000)
        channel_by_id = discord.utils.get(bot.get_all_channels(), name="off-topic")
        await channel_by_id.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send("Błąd")
    return


@bot.event
async def on_member_remove(member):
    for role in member.roles:
        role_name = str(role)
        length = len(role_name)
        s = role_name.replace(" ", "")
        st = len(s)
        if st != length:
            await role.delete()


@bot.command(pass_context=True)
async def purge(ctx, amount=30):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
        messages.append(message)

    await channel.delete_messages(messages)


bot.run("ODkxNzY1MjQzNjAzMjAyMTE4.YVDHGg" + ".-4dFOYSXpwjvktX4JQtajtwKB4k")
