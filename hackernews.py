import json,discord,requests
from datetime import datetime
from utils import embed_gen
from fake_useragent import UserAgent
import multiprocessing as mp

ua = UserAgent()
headers = {'User-Agent':ua.firefox}

def gate(keyword):
	tally_list = ['topstories', 'beststories', 'newstories']
	valid = False
	for tally in tally_list:
		if tally == keyword:
			valid = True
	if valid == False:
		return 'Not a valid search term :('
	else:
		return process_query(keyword)

def process_query(keyword):
	url = 'https://hacker-news.firebaseio.com/v0/'+keyword+'.json?print=pretty'
	page = requests.get(url, headers=headers)
	ids = json.loads(page.content)[:10]
	embeds = []
	pool = mp.Pool(processes=4)
	embeds = pool.map(create_embed_pool, ids)
	return embeds

def create_embed_pool(id):
	url = 'https://hacker-news.firebaseio.com/v0/item/'+str(id)+'.json?print=pretty'
	page = requests.get(url, headers=headers)
	data = json.loads(page.content)
	by = data['by']
	title = data['title']
	if 'url' in data.keys():
		url = data['url']
	else:
		url = ""
	time = datetime.utcfromtimestamp(int(data['time'])).strftime('%Y-%m-%d %H:%M:%S')
	return embed_gen.newsstamp(title, by, url, time)