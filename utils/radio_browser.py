import discord,operator,json,aiohttp,re,os,random,time
from pyradios import RadioBrowser
from utils import embed_gen
from fake_useragent import UserAgent

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

async def stats(instances):
	headers = {'User-Agent' : UserAgent().firefox}
	embeds = []
	session = aiohttp.ClientSession()
	for instance in instances:
		page = await session.get(url=instance+'/json/stats', headers=headers)
		data = await page.json()
		embed = discord.Embed(title=instance, color=embed_color)
		embed.add_field(name='STATUS', value=data['status'], inline=False)
		embed.add_field(name='Stations', value=data['stations'], inline=False)
		embed.add_field(name='Clicks', value=data['clicks_last_day'], inline=False)
		embeds.append(embed)
	await session.close()
	return embeds

async def icy_extract(url):
	headers = {'User-Agent' : UserAgent().firefox, 'Icy-Metadata' : "1"}
	session = aiohttp.ClientSession()
	try:
		response = await session.get(url, headers=headers, timeout=2)
		data = response.headers
		if "icy-url" in data.keys():
			website_link = data['icy-url']
		else:
			website_link = ""
		data = {"name" : data['icy-name'], "genre" : data['icy-genre'], "url" : website_link}
		await session.close()
		return data
	except:
		await session.close()
		return "timeout"

async def search_stations(keyword, instance): #Querys all.api.radio-browser.info
	embeds = []
	headers = {'User-Agent' : UserAgent().firefox}
	url = instance+'/json/stations/search?name='+keyword+'&limit=15'
	session = aiohttp.ClientSession()
	page = await session.get(url=url, headers=headers)
	entries = await page.json()
	await session.close()
	for entry in entries:
		icy_name = entry['name']
		icy_genre = 'Genre: '+entry['tags']
		icy_url = entry['homepage']
		icy_stream_url = entry['url_resolved']
		embed = embed_gen.search_stations(icy_name, icy_genre, icy_url, icy_stream_url)
		embeds.append(embed)
	return embeds

async def now_playing(path):
	player_env = json.load(open(path+'/player_env.json', 'r'))
	headers = {'User-Agent' : UserAgent().firefox, 'Icy-Metadata' : "1"}
	url = player_env['Playing']['Stream']
	session = aiohttp.ClientSession()
	response = await session.get(url=url, headers=headers)
	if response.headers['icy-name'] == player_env['Playing']['Title']: #If you have anxiety issues then check through other params also :)
		metaint = int(response.headers['icy-metaint'])
		track_name = ""
		track_name = await resolve_track_name(response, metaint)
		data = response.headers
		embed = discord.Embed(title='Now Playing', color=embed_color)
		embed.add_field(name='Station name', value=data['icy-name'], inline=False)
		embed.add_field(name='Genre', value=data['icy-genre'], inline=False)
		embed.add_field(name='Track Name', value=track_name, inline=False)
		hostname = json.load(open('defaults.json', 'r'))['current-invidious-instance']
		link = hostname+'/api/v1/search?q='+track_name+'&type=video'
		page = await session.get(url=link, headers={"User-Agent" : UserAgent().firefox})
		info = (await page.json())[0]
		if info.get('videoThumbnails') == None:
			link = "https://i.imgur.com/VcoRTU6.png"
		else:
			link = info['videoThumbnails'][1]['url']
		embed.set_image(url=link)
		await session.close()
		return embed
	else: #By no possible means should this ever happen / But if you end up here, you screwed up
		await session.close()
		return 'code:youscrewedup'

async def resolve_track_name(response, metaint):
	track_name = ""
	for _ in range(10):
		data = await response.content.read(metaint)  # skip to metadata
		m = re.search(br"StreamTitle='([^']*)';", data.rstrip(b'\0'))
		if m:
			title = m.group(1)
			if title:
				return title.decode("utf-8", errors='replace')
			else:
				track_name = "No title found"
		else:
			track_name = "No title found"
	return track_name