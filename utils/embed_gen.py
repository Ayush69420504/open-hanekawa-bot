import discord,json
from datetime import timedelta

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

def create_meme(title, url):
	embed = discord.Embed(title=title, color=embed_color)
	embed.set_image(url=url)
	return embed

def search_manga(title, manga_code, latest_chapter, author_name, imurl):
	embed = discord.Embed(title=title, color=embed_color)
	embed.add_field(name='Manga Code', value=manga_code, inline=False)
	embed.add_field(name='Latest Chapter', value=latest_chapter, inline=False)
	embed.add_field(name='Author Name', value=author_name, inline=False)
	embed.set_image(url=imurl)
	return embed
	
def whoami():
	data = open('data/whoami', 'r').read()
	embed = discord.Embed(title="I am Hanekawa-san", description=data, color=embed_color)
	file = discord.File('data/smile.gif', filename='smile.gif')
	embed.set_image(url='attachment://smile.gif')
	return file,embed

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
