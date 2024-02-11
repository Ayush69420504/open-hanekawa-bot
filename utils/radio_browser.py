import discord,operator,json,requests,struct,re,os,random,time
from ytmusicapi import YTMusic
from pyradios import RadioBrowser
from utils import embed_gen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
try:
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2
from fake_useragent import UserAgent

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

def icy_extract(url):
	headers = {'User-Agent' : UserAgent().firefox, 'Icy-Metadata' : "1"}
	request = urllib2.Request(url, headers=headers)
	try:
		response = urllib2.urlopen(request, timeout=1)
		data = response.headers
		if "icy-url" in data.keys():
			website_link = data['icy-url']
		else:
			website_link = ""
		data = {"name" : data['icy-name'], "genre" : data['icy-genre'], "url" : website_link}
		return data
	except:
		return "timeout"

def search_stations_extended(keyword): #Querys https://www.internet-radio.com
	url = 'https://www.internet-radio.com/search/?radio='+keyword
	headers = {'User-Agent' : UserAgent().firefox}
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html5lib')
	elements = soup.findAll('tr')[:10]
	embeds = []
	for element in elements:
		tds = element.findAll('td')
		td = tds[1]
		icy_stream_url = resolve_stream_link(td.small.a['href'])
		td = tds[2]
		icy_name = td.h4.text
		tmp = td.findAll('a', attrs={'small text-success'}) # Class name used by icy_url is available
		if len(tmp) != 0:
			icy_url = tmp[0].text
		else:
			icy_url = ""
		icy_genre = td.text[td.text.rindex('Genres'):]
		embed = embed_gen.search_stations(icy_name, icy_genre, icy_url, icy_stream_url)
		embeds.append(embed)
	return embeds

def search_stations(keyword): #Querys pyradios
	embeds = []
	rb = RadioBrowser()
	entries = sorted(rb.search(name=keyword), key=lambda x: (-x['votes'], -x['clickcount']))[:10]
	for entry in entries:
		icy_name = entry['name']
		icy_genre = 'Genre: '+entry['tags']
		icy_url = entry['homepage']
		icy_stream_url = entry['url_resolved']
		embed = embed_gen.search_stations(icy_name, icy_genre, icy_url, icy_stream_url)
		embeds.append(embed)
	return embeds

def now_playing(path):
	player_env = json.load(open(path+'/player_env.json', 'r'))
	headers = {'User-Agent' : UserAgent().firefox, 'Icy-Metadata' : "1"}
	url = player_env['Playing']['Stream']
	request = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(request)
	if response.headers['icy-name'] == player_env['Playing']['Title']: #If you have anxiety issues then check through other params also :)
		metaint = int(response.headers['icy-metaint'])
		data = response.headers
		track_name = resolve_track_name(response, metaint)
		embed = discord.Embed(title='Now Playing', color=embed_color)
		embed.add_field(name='Station name', value=data['icy-name'], inline=False)
		embed.add_field(name='Genre', value=data['icy-genre'], inline=False)
		embed.add_field(name='Track Name', value=track_name, inline=False)
		link = YTMusic().search(track_name, filter="songs")[0]['thumbnails'][1]['url']
		embed.set_image(url=link)
		return embed
	else: #By no possible means should this ever happen / But if you end up here, you screwed up
		return 'code:youscrewedup'

def resolve_stream_link(link):
	link = link.split("=")[1] # Temporary eyeballing solution, maybe permanent :)
	link = link[:link.rfind('.')]
	if link[link.rfind('/')+1:] == 'listen':
		link = link[:link.rfind('/')+1] + 'play'
	return link

def resolve_track_name(response, metaint):
	encoding = 'latin1'
	for _ in range(10):
		response.read(metaint)  # skip to metadata
		metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
		metadata = response.read(metadata_length).rstrip(b'\0')
		# extract title from the metadata
		m = re.search(br"StreamTitle='([^']*)';", metadata)
		if m:
			title = m.group(1)
			if title:
				return title.decode(encoding, errors='replace')
		else:
			return "Unknown"