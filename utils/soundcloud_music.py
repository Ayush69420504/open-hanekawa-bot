import discord,json
from yt_dlp import YoutubeDL
from datetime import timedelta

YTDL_PARAMS = {'format':'bestaudio/best', 'nocheckcertificate':True, 'source_address':'0.0.0.0', 'quiet':True}
defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

def ydl_extract(keyword):
	info = YoutubeDL(params=YTDL_PARAMS).extract_info(url='scsearch:'+keyword, download=False)['entries'][0]
	title = info['title']
	duration = round(info['duration'])
	url = info['url']
	global thumbnail
	try:
		for thumb in info['thumbnails']:
			if thumb['id'] == 't300x300':
				thumbnail = thumb['url']
				break
		raw = [title, duration, thumbnail, url]
		embed = discord.Embed(title=("Added to queue"), color=embed_color)
		embed.add_field(name="Title", value=title, inline=False)
		embed.add_field(name="Duration", value=str(timedelta(seconds=duration)), inline=False)
		embed.set_image(url=thumbnail)
		return raw,embed
	except:
		thumbnail = 'https://i.imgur.com/VcoRTU6.png'
		raw = [title, duration, thumbnail, url]
		embed = discord.Embed(title=("Added to queue"), color=embed_color)
		embed.add_field(name="Title", value=title, inline=False)
		embed.add_field(name="Duration", value=str(timedelta(seconds=duration)), inline=False)
		embed.set_image(url=thumbnail)
		return raw,embed

def ydl_list_search(message, keyword):
	embeds = []
	entires = YoutubeDL(params=YTDL_PARAMS).extract_info(url='scsearch3:'+keyword, download=False)['entries']
	for entry in entires:
		embed = discord.Embed(color=embed_color)
		embed.add_field(name='Title', value=entry['title'], inline=False)
		embed.add_field(name='Duration', value=str(timedelta(seconds=round(float(entry['duration'])))), inline=False)
		for thumbnail in entry['thumbnails']:
			if thumbnail['id'] == 'large':
				embed.set_image(url=thumbnail['url'])
		embeds.append(embed)
	return embeds
	
