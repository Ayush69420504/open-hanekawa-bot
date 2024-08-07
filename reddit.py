import aiohttp,json,discord,random
from utils import embed_gen,OxO
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent':ua.firefox}
defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

async def search_reddit_posts(query):
	url = 'https://www.reddit.com/search.json?q='+query
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	children = (await page.json())['data']['children'][:10]
	await session.close()
	embeds = []
	for child in children:
		sub_name = child['data']['subreddit_name_prefixed'] 
		post_title = child['data']['title']
		permalink = 'https://www.reddit.com'+child['data']['permalink']
		if child['data'].get('url_overridden_by_dest') != None:
			url = child['data']['url_overridden_by_dest']
		else:
			url = 'https://i.imgur.com/VcoRTU6.png'
		embed = discord.Embed(title=sub_name, color=embed_color)
		embed.add_field(name=post_title, value="", inline=False)
		embed.add_field(name='Permalink', value=permalink, inline=False)
		embed.set_image(url=url)
		embeds.append(embed)
	return embeds

async def search_subreddits(query):
	url = 'https://www.reddit.com/search/.json?q='+query+'&type=sr'
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	children = (await page.json())['data']['children'][:10]
	await session.close()
	embeds = []
	for child in children:
		name = child['data']['display_name_prefixed']
		thumbnail = child['data']['icon_img']
		image = child['data']['banner_img']
		description = child['data']['public_description']
		embed = discord.Embed(title=name, color=embed_color)   
		embed.add_field(name='Description', value=description, inline=False)
		embed.set_thumbnail(url=thumbnail)
		embed.set_image(url=image)
		embeds.append(embed)
	return embeds

async def random_sub_post(keyword):
	url = 'https://www.reddit.com/r/'+keyword+'/.json'
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = (await page.json())['data']['children']
	await session.close()
	if isinstance(data, list):
		children_data = data[random.randrange(0, len(data)-1)]['data']
		sub_name = children_data['subreddit_name_prefixed']
		post_title = children_data['title']
		if children_data.get('url_overridden_by_dest') != None:
			url = children_data['url_overridden_by_dest']
		else:
			url = 'https://i.imgur.com/VcoRTU6.png'
		embed = discord.Embed(title=sub_name, color=embed_color)
		embed.add_field(name=post_title, value="", inline=False)
		embed.set_image(url=url)
		return embed
	else:
		embed = discord.Embed(title="No results found", color=embed_color)
		embed.add_field(name='How to solve error', value='Use search-reddit to search an approprtiate name and input it in the command', inline=False)
		url = await OxO.upload(fp='data/error.gif', expires=600)
		embed.set_image(url=url)
		return embed