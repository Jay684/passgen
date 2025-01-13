import discord
import os
import random
import requests
from discord.ext import commands
from main import gen_pass

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

bins = {
    "recyclable": ["plastic bottle", "aluminum can", "glass jar"],
    "organic": ["apple core", "banana peel", "vegetable scraps"]
}

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
        await guild.system_channel.send(to_send)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh=5):
    await ctx.send("he" * count_heh)

@bot.command()
async def gen(ctx, count_heh=5):
    await ctx.send(gen_pass(count_heh))

@bot.command()
async def spam_emoji(ctx, emoji='😀'):
    await ctx.send(emoji * 15)

@bot.command()
async def mem(ctx):
    image_file = random.choice(os.listdir('image'))

    with open(f'image/{image_file}', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
   # Kita kemudian dapat mengirim file ini sebagai tolok ukur!
    await ctx.send(file=picture)


def get_woof_image_url():    
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('woof')
async def woof(ctx):
    '''Setelah kita memanggil perintah woof, program akan memanggil fungsi get_woof_image_url'''
    image_url = get_woof_image_url()
    await ctx.send(image_url)

def get_random_image_url():    
    url = 'https://meme-api.com/gimme'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('RandomMeme')
async def RandomMeme(ctx):
    '''Setelah kita memanggil perintah random_meme, program akan memanggil fungsi get_random_meme_image_url'''
    image_url = get_random_image_url()
    await ctx.send(image_url)

@bot.command()
async def throw_trash(ctx, trash: str, bin_name: str):
    """Buang sampah ke tempat sampah yang benar. Contohnya: $throw_trash <trash> <bin_name>"""
    
    print(f"Received trash: '{trash}', bin_name: '{bin_name}'")

    if bin_name not in bins:
        await ctx.send("Salah bin! Pilih 'recyclable' atau 'organic'.")
        return

    if trash in bins[bin_name]:
        await ctx.send(f"Benar! Kamu membuang {trash} ke {bin_name} bin.")
    else:
        correct_bins = [name for name, items in bins.items() if trash in items]
        if correct_bins:
            await ctx.send(f"Sampah ini seharusnya dibuang di {correct_bins[0]} bin.")
        else:
            await ctx.send("Sampah ini tidak milik ke bin apapun!")


bot.run("YOUR_TOKEN")
