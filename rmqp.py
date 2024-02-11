import discord,json,time
from yt_dlp import YoutubeDL
from utils import embed_gen
from utils import radio_browser

FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}
YTDL_PARAMS = {'format':'bestaudio/best', 'nocheckcertificate':True, 'source_address':'0.0.0.0', 'quiet':True}
defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

'''
This file will look weird as play_list and play are being run in a seperate thread.

I know that vc.play has an after= parameter which can be used to make a playlist system

But in favour of simplicity and that this was my original design, i will not change it.

anon code suggestions to update rmqp.py will be reviewed.
'''

def play_list(vc, path):
	#I have named this function play_list with a underscore like a complete madman to differenciate from the playlist python object :)
	vc.stop()
	playlist = json.load(open(path+'/playlist.json', 'r'))
	player_env = json.load(open(path+'/player_env.json', 'r'))
	if len(playlist) != 0:
		stream_url = YoutubeDL(params=YTDL_PARAMS).extract_info(url=playlist[0]['VideoId'], download=False)['url']
		source = discord.FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS)
		source = discord.PCMVolumeTransformer(source)
		source.volume = player_env['Volume'][1]/100
		vc.play(source) 
		player_env['Playing']['Title'] = playlist[0]['Title']
		player_env['Playing']['Duration'] = playlist[0]['Duration']
		player_env['Playing']['Thumbnail'] = playlist[0]['Thumbnail']
		player_env['IsRunning'] = True
		json.dump(player_env, open(path+'/player_env.json', 'w'))
		playlist.pop(0)
		json.dump(playlist, open(path+'/playlist.json', 'w'))
		while vc.is_playing() or vc.is_paused():
			time.sleep(0.1)
		play_list(vc, path)
	else:
		playing = {'Title':None, 'Duration':None, 'Thumbnail':None, "Genre":None, "Stream":None}
		player_env['Playing'] = playing
		player_env['IsRunning'] = False
		player_env['Mode'] = 'queue'
		json.dump(player_env, open(path+'/player_env.json', 'w'))
	
def play_radio(vc, path, stream_url):
	#Uses a stream link queried from https://www.internet-radio.com or pyradios
	#Variable "stream_url" is the stream url / and data["url"] is website link if any
	vc.stop()
	data = radio_browser.icy_extract(stream_url)
	player_env = json.load(open(path+'/player_env.json', 'r'))
	if data != 'timeout':
		embed = embed_gen.play_radio(data['name'], data['genre'], data['url'])
		source = discord.FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS)
		source = discord.PCMVolumeTransformer(source)
		source.volume = player_env['Volume'][1]/100
		player_env['Playing']['Title'] = data['name']
		player_env['Playing']['Genre'] = data['genre']
		player_env['Playing']['Stream'] = stream_url
		player_env['Mode'] = 'radio'
		player_env['IsRunning'] = True
		json.dump(player_env, open(path+'/player_env.json', 'w'))
		vc.play(source)
		return embed
	else:
		player_env['IsRunning'] = False
		player_env['Mode'] = 'queue'
		json.dump(player_env, open(path+'/player_env.json', 'w'))
		embed = discord.Embed(title='Timeout error, choose another station :)', color=embed_color)
		return embed

def play(vc, path):
	music_queue = json.load(open(path+'/music_queue.json', 'r'))
	player_env = json.load(open(path+'/player_env.json', 'r'))
	if len(music_queue) != 0:
		source = discord.FFmpegPCMAudio(music_queue[0]['Url'], **FFMPEG_OPTIONS)
		source = discord.PCMVolumeTransformer(source)
		source.volume = player_env['Volume'][1]/100
		vc.play(source) 
		player_env['Playing']['Title'] = music_queue[0]['Title']
		player_env['Playing']['Duration'] = music_queue[0]['Duration']
		player_env['Playing']['Thumbnail'] = music_queue[0]['Thumbnail']
		player_env['IsRunning'] = True
		json.dump(player_env, open(path+'/player_env.json', 'w'))
		music_queue.pop(0)
		json.dump(music_queue, open(path+'/music_queue.json', 'w'))
		while vc.is_playing() or vc.is_paused():
			time.sleep(0.1)
		play(vc, path)
	else:
		playing = {'Title':None, 'Duration':None, 'Thumbnail':None, "Genre":None, "Stream":None}
		player_env['Playing'] = playing
		player_env['IsRunning'] = False
		player_env['Mode'] = 'queue'
		json.dump(player_env, open(path+'/player_env.json', 'w'))
