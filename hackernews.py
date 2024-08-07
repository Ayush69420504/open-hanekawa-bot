import json,discord,aiohttp
from datetime import datetime
from utils import embed_gen
from fake_useragent import UserAgent
import multiprocessing as mp

ua = UserAgent()
headers = {'User-Agent':ua.firefox}

async def gate(keyword):
	tally_list = ['topstories', 'beststories', 'newstories']
	valid = False
	for tally in tally_list:
		if tally == keyword:
			valid = True
	if valid == False:
		return 'Not a valid search term :('
	else:
		return await process_query(keyword)

async def process_query(keyword):
	url = 'https://hacker-news.firebaseio.com/v0/'+keyword+'.json?print=pretty'
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	ids = (await page.json())[:10]
	await session.close()
	embeds = []
	for id in ids:
		embeds.append(await create_embed_pool(id))
	return embeds

async def create_embed_pool(id):
	url = 'https://hacker-news.firebaseio.com/v0/item/'+str(id)+'.json?print=pretty'
	session = aiohttp.ClientSession()
	page = await session.get(url, headers=headers)
	data = await page.json()
	await session.close()
	by = data['by']
	title = data['title']
	if 'url' in data.keys():
		url = data['url']
	else:
		url = ""
	time = datetime.utcfromtimestamp(int(data['time'])).strftime('%Y-%m-%d %H:%M:%S')
	return embed_gen.newsstamp(title, by, url, time)