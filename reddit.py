import requests,json,discord,time
from utils import embed_gen,oxo
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent':ua.firefox}
defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

def search_reddit_posts(query):
	url = 'https://www.reddit.com/search.json?q='+query
	page = requests.get(url, headers=headers)
	children = json.loads(page.content)['data']['children'][:10]
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

def search_subreddits(query):
	url = 'https://www.reddit.com/search/.json?q='+query+'&type=sr'
	page = requests.get(url, headers=headers)
	children = json.loads(page.content)['data']['children'][:10]
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

def random_sub_post(keyword):
	url = 'https://www.reddit.com/r/'+keyword+'/random.json'
	page = requests.get(url, headers=headers)
	data = json.loads(page.content)
	if isinstance(data, list):
		children_data = data[0]['data']['children'][0]['data']
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
		link = oxo.upload_file_path(path='data/error.gif', expires=round(time.time()+900), secret=None)
		embed.set_image(url=link)
		return embed