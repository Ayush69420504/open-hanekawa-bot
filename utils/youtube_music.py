import discord,json
import aiohttp
from fake_useragent import UserAgent
from datetime import timedelta

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)
ua = UserAgent()
headers = {'User-Agent':ua.firefox}

async def current_invidious_instance():
	hostname = json.load(open('defaults.json', 'r'))['current-invidious-instance']
	session = aiohttp.ClientSession()
	page = await session.get(url=hostname+'/api/v1/stats', headers=headers)
	stats = await page.json()
	await session.close()
	embed = discord.Embed(title=hostname, color=embed_color)
	ver_string = stats['software']['name']+' '+stats['software']['branch']+' '+stats['software']['version']
	embed.add_field(name='Software', value=ver_string, inline=False)
	embed.add_field(name='Users', value=stats['usage']['users']['total'], inline=False)
	if stats['openRegistrations'] == True:
		embed.add_field(name='Open for registrations', value='', inline=False)
	else:
		embed.add_field(name='Closed for registrations', value='', inline=False)
	return embed

async def playlist_extract(keyword):
	hostname = json.load(open('defaults.json', 'r'))['current-invidious-instance']
	link = hostname+'/api/v1/playlists/'+keyword
	session = aiohttp.ClientSession()
	page = await session.get(url=link, headers=headers)
	info = await page.json()
	await session.close()
	title = info['title']
	if info.get('description') == None:
		description = "No description"
	else:
		description = (info['description'][:min(len(info['description']), 1024)])
	duration = 0
	for video in info['videos']:
		duration += video['lengthSeconds']
	duration = str(timedelta(seconds=round(duration)))
	if info.get('playlistThumbnail') == None:
		thumb_url = "https://i.imgur.com/VcoRTU6.png"
	else:
		thumb_url = info['playlistThumbnail']
	embed = discord.Embed(title=title, color=embed_color)
	embed.add_field(name="Description", value=description, inline=False)
	embed.add_field(name="Duration", value=duration, inline=False)
	embed.set_image(url=thumb_url)
	entries = info['videos']
	playlist = []
	for entry in entries:
		if entry.get('videoId') == None:
			break
		videoid = entry['videoId']
		title = entry['title']
		duration = entry['lengthSeconds']
		if entry.get('videoThumbnails') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['videoThumbnails'][1]['url']
		entry_form = {'Title':title,'Duration':duration, 'Thumbnail':thumb_url, 'VideoId':videoid}
		playlist.append(entry_form)
	return playlist,embed

async def playlist_search(query):
	hostname = json.load(open('defaults.json', 'r'))['current-invidious-instance']
	link = hostname+'/api/v1/search?q='+query+'&type=playlist'
	session = aiohttp.ClientSession()
	page = await session.get(url=link, headers=headers)
	info = (await page.json())[:10]
	await session.close()
	embeds = []
	for entry in info:
		title = entry['title']
		author = entry['author']
		playlistid = entry['playlistId']
		if entry.get('playlistThumbnail') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['playlistThumbnail']
		embed = discord.Embed(title=title, color=embed_color)
		embed.add_field(name='Author', value=author, inline=False)
		embed.add_field(name='Playlist Id', value=playlistid, inline=False)
		embed.set_image(url=thumb_url)
		embeds.append(embed)
	return embeds

async def ydl_extract(keyword):
	hostname = json.load(open('defaults.json', 'r'))['current-invidious-instance']
	link = hostname+'/api/v1/search?q='+keyword+'&type=video'
	session = aiohttp.ClientSession()
	page = await session.get(url=link, headers=headers)
	info = (await page.json())[0]
	await session.close()
	title = info['title']
	duration = info['lengthSeconds']
	if info.get('videoThumbnails') == None:
		thumbnail = "https://i.imgur.com/VcoRTU6.png"
	else:
		thumbnail = info['videoThumbnails'][1]['url']
	videoid = info['videoId']
	raw = [title, duration, thumbnail, videoid]
	embed = discord.Embed(title="Added to queue", color=embed_color)
	embed.add_field(name='Title', value=title, inline=False)
	embed.add_field(name='Duration', value=str(timedelta(seconds=round(duration))))
	embed.add_field(name='Author', value=info['author'])
	embed.set_image(url=thumbnail)
	return raw,embed

async def ydl_list_search(keyword):
	embeds = []
	hostname = json.load(open('defaults.json', 'r'))['current-invidious-instance']
	link = hostname+'/api/v1/search?q='+keyword+'&type=video'
	session = aiohttp.ClientSession()
	page = await session.get(url=link, headers=headers)
	entries = (await page.json())[:10]
	await session.close()
	for entry in entries:
		embed = discord.Embed(color=embed_color)
		embed.add_field(name='Title', value=entry['title'], inline=False)
		embed.add_field(name='Author', value=entry['author'], inline=False)
		embed.add_field(name='Duration', value=entry['lengthSeconds'], inline=False)
		if entry.get('videoThumbnails') == None:
			thumb_url = "https://i.imgur.com/VcoRTU6.png"
		else:
			thumb_url = entry['videoThumbnails'][1]['url']
		embed.set_image(url=thumb_url)
		embeds.append(embed)
	return embeds
	
