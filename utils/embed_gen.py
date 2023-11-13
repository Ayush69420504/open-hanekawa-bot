import discord,json,time
from datetime import timedelta
from utils import oxo

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

def search_stations(icy_name, icy_genre, icy_url, icy_stream_url):
	embed = discord.Embed(title=icy_name, color=embed_color)
	embed.add_field(name=icy_genre, value="", inline=False)
	embed.add_field(name='Stream Url', value=icy_stream_url, inline=False)
	if icy_url != "":
		embed.add_field(name='Website', value=icy_url, inline=False)
	return embed

def newsstamp(title, by, url, time):
	embed = discord.Embed(color=embed_color)
	embed.add_field(name=title, value="", inline=False)
	embed.add_field(name="By", value=by, inline=False)
	embed.add_field(name="Time", value=time, inline=False)
	if url != "":
		embed.add_field(name='Url', value=url, inline=False)
	return embed

def play_radio(icy_name, icy_genre, icy_url):
	embed = discord.Embed(title=icy_name, color=embed_color)
	embed.add_field(name='Genre', value=icy_genre, inline=False)
	if icy_url != "":
		embed.add_field(name='Website', value=icy_url, inline=False)
	return embed

def search_manga(title, manga_code, latest_chapter, author_name, imurl):
	embed = discord.Embed(title=title, color=embed_color)
	embed.add_field(name='Manga Code', value=manga_code, inline=False)
	embed.add_field(name='Latest Chapter', value=latest_chapter, inline=False)
	embed.add_field(name='Author Name', value=author_name, inline=False)
	embed.set_image(url=imurl)
	return embed
	
def help(helpbook):
	embeds = []
	data = open('data/whoami', 'r').read()
	embed = discord.Embed(title="I am Hanekawa-san", description=data, color=embed_color)
	link = oxo.upload_file_path(path='data/smile.gif', expires=round(time.time())+900, secret=None)
	embed.set_image(url=link)
	embeds.append(embed)
	key_list = list(helpbook.keys())
	intervals = len(key_list)//5
	for i in range(0, intervals):
		embed = discord.Embed(color=embed_color)
		for key in key_list[5*i:5*(i+1)]:
			embed.add_field(name=key, value=helpbook[key], inline=False)
		embeds.append(embed)
	embed = discord.Embed(color=embed_color)
	for key in key_list[intervals*5:len(key_list)]:
		embed.add_field(name=key, value=helpbook[key], inline=False)
	embeds.append(embed)
	return embeds

def list_queue(music_queue):
	embed = discord.Embed(title="Next in Queue", color=embed_color)
	i = 1
	for x in music_queue:
		embed.add_field(name=str(i)+". "+x['Title']+" : "+str(timedelta(seconds=round(x['Duration']))), value='\n', inline=False)
		i += 1
	return embed
		
def now_playing(playing, ispaused): # General purpose nowplaying for the music player NOT the radio station
	embed = discord.Embed(title='Now Playing', color=embed_color)
	embed.add_field(name='Title', value=playing['Title'], inline=False)
	t_time = str(timedelta(seconds=round(playing['Duration'])))
	if ispaused is True:
		embed.add_field(name='Paused', value=t_time, inline=False)
	else:
		embed.add_field(name='Playing', value=t_time, inline=False)
	embed.set_image(url=playing['Thumbnail'])
	return embed

def skip_track(playing):
	embed = discord.Embed(title='Skipping track', color=embed_color)
	embed.add_field(name='Title', value=playing['Title'], inline=False)
	embed.add_field(name='Duration', value=str(timedelta(seconds=round(playing['Duration']))), inline=False)
	embed.set_image(url=playing['Thumbnail'])
	return embed
