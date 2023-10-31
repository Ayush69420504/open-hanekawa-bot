import requests,json,discord,random
from utils import embed_gen
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent':ua.firefox}

def animeme():
	url = 'https://www.reddit.com/r/Animemes/random.json'
	page = requests.get(url, headers=headers)
	data = json.loads(page.content)[0]['data']['children'][0]['data']
	title = data['title']
	url = data['url']
	embed = embed_gen.create_meme(title, url)
	return embed

def meme():
	url = 'https://www.reddit.com/r/memes/random.json'
	page = requests.get(url, headers=headers)
	data = json.loads(page.content)[0]['data']['children'][0]['data']
	title = data['title']
	url = data['url']
	embed = embed_gen.create_meme(title, url)
	return embed

def uncensored_hentai_meme():
	url = 'https://www.reddit.com/r/hentaimemes/random.json'
	page = requests.get(url, headers=headers)
	data = json.loads(page.content)[0]['data']['children'][0]['data']
	title = data['title']
	url = data['url']
	embed = embed_gen.create_meme(title, url)
	return embed
