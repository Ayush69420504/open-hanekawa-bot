import aiohttp,discord,json
from fake_useragent import UserAgent
#embed_gen contains template functions to generate embeds
from utils import embed_gen

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)
ua = UserAgent()
headers = {'User-Agent':ua.firefox}

async def health_jikan():
	url = 'https://api.jikan.moe/v4'
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = await page.json()
	await session.close()
	embed = discord.Embed(title=url+' is '+data['myanimelist_heartbeat']['status'], color=embed_color)
	embed.add_field(name='Score', value=str(data['myanimelist_heartbeat']['score']), inline=False)
	embed.add_field(name='Version', value=data['version'], inline=False)
	embed.add_field(name='Website', value=data['website_url'], inline=False)
	embed.add_field(name='Author', value=data['author_url'], inline=False)
	return embed

async def search_people(keyword):
	embeds = []
	url = 'https://api.jikan.moe/v4/people?q='+keyword
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = (await page.json())['data'][:10]
	await session.close()
	embeds = []
	for result in data:
		embed = discord.Embed(title=result['name']+' / '+str(result['given_name'] or "")+' / '+str(result['family_name'] or ""), color=embed_color)
		alternate_names = ""
		for alternate_name in result['alternate_names']:
			alternate_names += alternate_name + '\n'
		embed.add_field(name='Alternate names', value=alternate_names)
		embed.add_field(name="MAL Id", value=result['mal_id'])
		embed.add_field(name="Url", value=result['url'], inline=False)
		embed.add_field(name='Birthday', value=result['birthday'], inline=False)
		embed.add_field(name='About', value=str(result['about'] or "None")[:1024], inline=False)
		embed.set_image(url=result['images']['jpg']['image_url'])
		embeds.append(embed)
	return embeds


async def search_magazines(keyword):
	embeds = []
	url = "https://api.jikan.moe/v4/magazines?q="+keyword+"&order_by=count&sort=desc"
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = (await page.json())['data'][:10]
	await session.close()
	embeds = []
	for result in data:
		embed = discord.Embed(title=result['name'], color=embed_color)
		embed.add_field(name="MAL Id", value=result['mal_id'], inline=True)
		embed.add_field(name="Url", value=result['url'], inline=False)
		embed.add_field(name="Count", value=result['count'], inline=False)
		embeds.append(embed)
	return embeds

async def search_clubs(keyword):
	embeds = []
	url = 'https://api.jikan.moe/v4/clubs?q='+keyword+'&order_by=members_count&sort=desc'
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = (await page.json())['data'][:10]
	await session.close()
	embeds = []
	for result in data:
		embed = discord.Embed(title=result['name'], color=embed_color)
		embed.add_field(name="MAL Id", value=result['mal_id'], inline=False)
		embed.add_field(name="Url", value=result['url'], inline=False)
		embed.add_field(name='Members', value=result['members'], inline=False)
		embed.add_field(name='Category', value=result['category'], inline=False)
		embed.add_field(name='Created', value=result['created'], inline=False)
		embed.add_field(name="Access", value=result['access'], inline=False)
		embed.set_image(url=result['images']['jpg']['image_url'])
		embeds.append(embed)
	return embeds

async def search_characters(keyword):
	embeds = []
	url = 'https://api.jikan.moe/v4/characters?q='+keyword+'&order_by=favorites&sort=desc'
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = (await page.json())['data'][:10]
	await session.close()
	embeds = []
	for result in data:
		embed = discord.Embed(title=result['name']+' / '+str(result['name_kanji'] or ""), color=embed_color)
		nicknames = ""
		for nickname in result['nicknames']:
			nicknames += nickname + '\n'
		embed.add_field(name='Nicknames', value=nicknames)
		embed.add_field(name="MAL Id", value=result['mal_id'])
		embed.add_field(name="Url", value=result['url'], inline=False)
		embed.add_field(name='About', value=str(result['about'] or "None")[:1024], inline=False)
		embed.set_image(url=result['images']['jpg']['image_url'])
		embeds.append(embed)
	return embeds

async def search_anime(keyword):
	embeds = []
	url = "https://api.jikan.moe/v4/anime?q="+keyword+"&order_by=score&sort=desc"
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = (await page.json())['data'][:10]
	await session.close()
	embeds = []
	for result in data:
		embed = discord.Embed(title=result['title'], color=embed_color)
		titles = str(result['title_english'] or "") + '\n' + str(result['title_japanese'] or "")
		embed.set_thumbnail(url=result['images']['jpg']['small_image_url'])
		embed.add_field(name='Titles', value=titles)
		embed.add_field(name='MAL Id', value=result['mal_id'])
		embed.add_field(name='Url', value=result['url'], inline=False)
		status = "{stat} with {epi} episodes".format(stat=result['status'], epi=result['episodes'])
		embed.add_field(name=status, value='\n', inline=False)
		embed.add_field(name="Aired", value=result['aired']["string"], inline=False)
		score = "Ranked : {rank}, Scored : {score} by {people}".format(score=result['score'], people=result['scored_by'], rank=result['rank'])
		embed.add_field(name=score, value='\n', inline=False)
		embed.add_field(name='Synopsis', value=str(result['synopsis'] or "None")[:1024], inline=False)
		embed.add_field(name='Background', value=str(result['background'] or "None")[:1024], inline=False)
		studios = ""
		for studio in result['studios']:
			studios += studio['name'] + '\n'
		embed.add_field(name="Studios", value=studios, inline=False)
		genres = ""
		for demographic in result['demographics']:
			genres += demographic['name'] + ', '
		for genre in result['genres']:
			genres += genre['name'] + ', '
		for theme in result['themes']:
			genres += theme['name'] + ', '
		embed.add_field(name='Genres', value=genres, inline=False)
		embed.set_image(url=result['images']['jpg']['image_url'])
		embeds.append(embed)
	return embeds


async def search_manga(keyword):	
	embeds = []
	url = "https://api.jikan.moe/v4/manga?q="+keyword+"&order_by=score&sort=desc"
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = (await page.json())['data'][:10]
	await session.close()
	embeds = []
	for result in data:
		embed = discord.Embed(title=result['title'], color=embed_color)
		titles = str(result['title_english'] or "") + '\n' + str(result['title_japanese'] or "")
		embed.set_thumbnail(url=result['images']['jpg']['small_image_url'])
		embed.add_field(name='Titles', value=titles)
		embed.add_field(name='MAL Id', value=result['mal_id'])
		embed.add_field(name='Url', value=result['url'], inline=False)
		status = "{stat} with {vol} volumes and {chp} chapters".format(stat=result['status'], vol=result['volumes'], chp=result['chapters'])
		embed.add_field(name=status, value='\n', inline=False)
		embed.add_field(name="Published", value=result['published']["string"], inline=False)
		score = "Ranked : {rank}, Scored : {score} by {people}".format(score=result['score'], people=result['scored_by'], rank=result['rank'])
		embed.add_field(name=score, value='\n', inline=False)
		embed.add_field(name='Synopsis', value=str(result['synopsis'] or "None")[:1024], inline=False)
		embed.add_field(name='Background', value=str(result['background'] or "None")[:1024], inline=False)
		authors = ""
		for author in result['authors']:
			authors += author['name'] + '\n'
		embed.add_field(name='Authors', value=authors, inline=False)
		genres = ""
		for demographic in result['demographics']:
			genres += demographic['name'] + ', '
		for genre in result['genres']:
			genres += genre['name'] + ', '
		for theme in result['themes']:
			genres += theme['name'] + ', '
		embed.add_field(name='Genres', value=genres, inline=False)
		embed.set_image(url=result['images']['jpg']['image_url'])
		embeds.append(embed)
	return embeds
