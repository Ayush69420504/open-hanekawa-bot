import discord,json
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
from datetime import timedelta

YTDL_PARAMS = {'format':'bestaudio/best', 'nocheckcertificate':True, 'source_address':'0.0.0.0', 'quiet':True}
defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

def playlist_extract(keyword):
	info = YTMusic().get_album(browseId=keyword)
	title = info['title']
	if info.get('description') == None:
		description = "No description"
	else:
		description = (info['description'][:min(len(info['description']), 1024)])
	duration = info['duration']
	if info.get('thumbnails') == None:
		thumb_url = "https://i.imgur.com/VcoRTU6.png"
	else:
		thumb_url = info['thumbnails'][0]['url']
	embed = discord.Embed(title=title, color=embed_color)
	embed.add_field(name="Description", value=description, inline=False)
	embed.add_field(name="Duration", value=duration, inline=False)
	embed.set_image(url=thumb_url)
	entries = info['tracks']
	playlist = []
	for entry in entries:
		if entry.get('videoId') == None:
			break
		videoid = entry['videoId']
		title = entry['title']
		duration = entry['duration_seconds']
		if entry.get('thumbnails') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['thumbnails'][0]['url']
		entry_form = {'Title':title,'Duration':duration, 'Thumbnail':thumb_url, 'VideoId':videoid}
		playlist.append(entry_form)
	return playlist,embed

def playlist_search(query):
	info = YTMusic().search(query, filter="albums")[:10]
	embeds = []
	for entry in info:
		title = entry['title']
		author = entry['artists'][0]["name"]
		playlistid = entry['browseId']
		if entry.get('thumbnails') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['thumbnails'][0]['url']
		embed = discord.Embed(title=title, color=embed_color)
		embed.add_field(name='Author', value=author, inline=False)
		embed.add_field(name='Playlist Id', value=playlistid, inline=False)
		embed.set_image(url=thumb_url)
		embeds.append(embed)
	return embeds

def ydl_extract(keyword):
	info = YTMusic().search(keyword, filter="songs")[0]
	title = info['title']
	duration = info['duration_seconds']
	if info.get('thumbnails') == None:
		thumbnail = "https://i.imgur.com/VcoRTU6.png"
	else:
		thumbnail = info['thumbnails'][1]['url']
	url = YoutubeDL(params=YTDL_PARAMS).extract_info(url='https://www.youtube.com/watch?v='+info['videoId'], download=False)['url']
	raw = [title, duration, thumbnail, url]
	embed = discord.Embed(title="Added to queue", color=embed_color)
	embed.add_field(name='Title', value=title, inline=False)
	embed.add_field(name='Duration', value=str(timedelta(seconds=round(duration))))
	embed.add_field(name='Album', value=info['album']['name'])
	embed.set_image(url=thumbnail)
	return raw,embed

def ydl_list_search(keyword):
	embeds = []
	entires = YTMusic().search(keyword, filter="songs")[:10]
	for entry in entires:
		embed = discord.Embed(color=embed_color)
		embed.add_field(name='Title', value=entry['title'], inline=False)
		embed.add_field(name='Album', value=entry['album']['name'], inline=False)
		embed.add_field(name='Duration', value=entry['duration'], inline=False)
		if entry.get('thumbnails') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['thumbnails'][1]['url']
		embed.set_image(url=thumb_url)
		embeds.append(embed)
	return embeds
	
