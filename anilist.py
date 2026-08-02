import json,discord
from AnilistPython import Anilist

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

async def search_anime(keyphrase):
    entry = Anilist().get_anime(keyphrase, deepsearch=True)
    embed = discord.Embed(color=embed_color)
    embed.add_field(name="English Title", value=entry['name_english'], inline=False)
    embed.add_field(name="Romaji Title", value=entry['name_romaji'], inline=False)
    embed.add_field(name="Genres", value=str(entry['genres']), inline=False)
    embed.add_field(name="Description", value=entry['desc'][:1024], inline=False)
    embed.set_image(url=entry['cover_image'])
    return embed

async def search_manga(keyphrase):
    entry = Anilist().get_manga(keyphrase)
    embed = discord.Embed(color=embed_color)
    embed.add_field(name="English Title", value=entry['name_english'], inline=False)
    embed.add_field(name="Romaji Title", value=entry['name_romaji'], inline=False)
    embed.add_field(name="Genres", value=str(entry['genres']), inline=False)
    embed.add_field(name="Description", value=entry['desc'][:1024], inline=False)
    embed.set_image(url=entry['cover_image'])
    return embed

async def search_character(keyphrase):
    entry = Anilist().get_character(keyphrase)
    embed = discord.Embed(color=embed_color)
    if entry.get('last_name') == None:
        name = entry['first_name']
    else:
        name = entry['first_name']+' '+['last_name']
    embed.add_field(name="Name (eng)", value=name, inline=False)
    embed.add_field(name="Name (jap)", value=entry['native_name'], inline=False)
    embed.add_field(name="Description", value=entry['desc'][:1024], inline=False)
    embed.set_image(url=entry['image'])
    return embed