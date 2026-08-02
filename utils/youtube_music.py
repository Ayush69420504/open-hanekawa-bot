import discord,json
from ytmusicapi import YTMusic

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

async def playlist_extract(keyword):
	info = YTMusic().get_playlist(playlistId=keyword)
	json.dump(info, open('data.json', 'w'))
	title = info['title']
	if info.get('description') == None:
		description = "No description"
	else:
		description = (info['description'][:min(len(info['description']), 1024)])
	duration = info['duration']
	if len(info['thumbnails']) == 0:
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
		duration = entry['duration']
		if entry.get('thumbnails') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['thumbnails'][0]['url']
		entry_form = {'Title':title,'Duration':duration, 'Thumbnail':thumb_url, 'VideoId':videoid}
		playlist.append(entry_form)
	return playlist,embed

async def playlist_search(query):
	info = YTMusic().search(query=query, filter='albums', limit=10)[:10]
	embeds = []
	for entry in info:
		title = entry['title']
		author = entry['artists'][0]['name']
		playlistid = entry['playlistId']
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

async def ydl_extract(keyword):
	info = YTMusic().search(query=keyword, filter='songs', limit=1)[0]
	title = info['title']
	duration = info['duration']
	if info.get('thumbnails') == None:
		thumbnail = "https://i.imgur.com/VcoRTU6.png"
	else:
		thumbnail = info['thumbnails'][0]['url']
	videoid = info['videoId']
	raw = [title, duration, thumbnail, videoid]
	embed = discord.Embed(title="Added to queue", color=embed_color)
	embed.add_field(name='Title', value=title, inline=False)
	embed.add_field(name='Duration', value=duration)
	embed.add_field(name='Author', value=info['artists'][0]['name'])
	embed.set_image(url=thumbnail)
	return raw,embed

async def ydl_list_search(keyword):
	embeds = []
	entries = YTMusic().search(query=keyword, filter='songs', limit=10)[:10]
	for entry in entries:
		embed = discord.Embed(color=embed_color)
		embed.add_field(name='Title', value=entry['title'], inline=False)
		embed.add_field(name='Author', value=entry['artists'][0]['name'], inline=False)
		embed.add_field(name='Duration', value=entry['duration'], inline=False)
		if entry.get('thumbnails') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['thumbnails'][0]['url']
		embed.set_image(url=thumb_url)
		embeds.append(embed)
	return embeds
	
