import discord,json

#hackernews.py uses the https://hacker-news.firebaseio.com/v0/ api to get news!
import hackernews
#reddit.py is contains functions to scrape certain reddit websites
import reddit
#External library, makes creation of paginated embeds hecka lot easier
#https://pypi.org/project/discord.py-pagination/
#Has been saved locally becuase i doubt this being updated, and is perfect for my use-case
from utils import Paginator
#hostinfo.py having the function to return formatted data regarding system info
from utils import hostinfo
#soundcloud_music.py having youtube music playback capability
from utils import soundcloud_music
#radio_browser.py is an abstraction of the RadioBrowserApi in python using pyradios
from utils import radio_browser
#rmpq.py acroynm for recursive music queue player, it sucks, i know :(
import rmqp
#manganato.py has manga functions
import manganato
#embed_gen.py contains functions generating template embeds. Used to reduce code in main.py
from utils import embed_gen

class Cogs:
	
	leftbutton = None
	rightbutton = None

	def __init__(self, defaults):
		self.leftbutton = discord.ui.Button(emoji=self.get_emoji(defaults['leftbutton']))
		self.rightbutton = discord.ui.Button(emoji=self.get_emoji(defaults['rightbutton']))
	
	async def search_radio_1(self, message):
		ctx = await self.get_context(message)
		content = message.content.split(" ")[2:]
		keyword = ""
		for word in content:
			keyword += word + ' '
		embeds = radio_browser.search_stations(keyword)
		if len(embeds) != 0:
			await Paginator.Simple(timeout=600, PreviousButton=self.leftbutton, NextButton=self.rightbutton).start(ctx, pages=embeds)
		else:
			await message.channel.send('No search results :(')

	async def hackernews(self, message):
		ctx = await self.get_context(message)
		keyword = message.content.split(" ")[2]
		results = hackernews.gate(keyword)
		if type(results) is str:
			await message.channel.send(results)
		elif type(results) is list:
			await Paginator.Simple(timeout=600, PreviousButton=self.leftbutton, NextButton=self.rightbutton).start(ctx, pages=results)	

	async def whoami(self, message):
		file,embed = embed_gen.whoami()
		await message.channel.send(embed=embed, file=file)

	async def ping(self, message):
		await message.channel.send(f'Pong: {int(self.latency*1000)}ms')

	async def hostinfo(self, message):
		await message.channel.send(embed=hostinfo.getSystemInfo())
	
	async def urltoqr(self, message):
		content = message.content.split(" ")[1:]
		url = content[1]
		url = 'https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl='+url+'&choe=UTF-8'
		await message.channel.send(url)
	
	async def wifitoqr(self, message):
		content = message.content.split(" ")[1:]
		ssid = content[1]
		encryption = content[2]
		password = content[3]
		chl = 'WIFI:S:'+ssid+';T:'+encryption+';P:'+password+';H:false;;'
		url = 'https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl='+chl+'&choe=UTF-8'
		await message.channel.send(url)

	async def animeme(self, message):
		await message.channel.send(embed=reddit.animeme())

	async def meme(self, message):
		await message.channel.send(embed=reddit.meme())

	async def uncensored_hentai_meme(self, message):
		await message.channel.send(embed=reddit.uncensored_hentai_meme())

	async def search_manga(self, message):
		content = message.content.split(" ")[1:]
		ctx = await self.get_context(message)
		keyword = ""
		for word in content[1:]:
			keyword += word + '_'
		embeds = manganato.search_manga(message, keyword)
		await Paginator.Simple(timeout=600, PreviousButton=self.leftbutton, NextButton=self.rightbutton).start(ctx, pages=embeds)

	async def list_chapters(self, message):
		content = message.content.split(" ")[1:]
		ctx = await self.get_context(message)
		keyword = content[1]
		if len(content) < 3:
			start = None
		else:
			start = content[2]
		if len(content) < 4:
			end = None
		else:
			end = content[3]
		embeds = manganato.list_chapters(message, keyword, start, end)
		await Paginator.Simple(timeout=600, PreviousButton=self.leftbutton, NextButton=self.rightbutton).start(ctx, pages=embeds)
		
	async def search_song(self, message):
		content = message.content.split(" ")[1:]
		ctx = await self.get_context(message)
		keyword = ""
		for word in content[1:]:
			keyword += word + " "
		embeds = soundcloud_music.ydl_list_search(message, keyword)
		await Paginator.Simple(timeout=600, PreviousButton=self.leftbutton, NextButton=self.rightbutton).start(ctx, pages=embeds)

	async def search_radio_2(self, message):
		content = message.content.split(" ")[1:]
		ctx = await self.get_context(message)
		keyword = ""
		for word in content[1:]:
			keyword += word + " "
		embeds = radio_browser.search_stations_extended(keyword)
		if len(embeds) != 0:
			await Paginator.Simple(timeout=600, PreviousButton=self.leftbutton, NextButton=self.rightbutton).start(ctx, pages=embeds)
		else:
			await message.channel.send("No search results :(")
	
	async def joinvc(self, message):
		try:
			await message.author.voice.channel.connect()
			await message.channel.send('Joined: '+str(message.author.voice.channel))
		except discord.errors.ClientException as e:
			await message.channel.send('I cannot have more than one instance in guild: '+message.author.guild.name)

	async def leavevc(self, message):
		vc = message.guild.voice_client
		await vc.disconnect()
		await message.channel.send('Left: '+str(vc.channel))

	async def pause(self, message):
		vc = message.guild.voice_client
		vc.pause()
		await message.channel.send('Paused audio in '+str(vc.channel))
	
	async def resume(self, message):
		vc = message.guild.voice_client
		vc.resume()
		await message.channel.send('Resumed audio in '+str(vc.channel))

	async def current_volume(self, message):
		path = 'server-audio-sessions/'+str(message.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		await message.channel.send('Current Volume: '+str(player_env['Volume'][1]))

	async def volume(self, message):
		content = message.content.split(" ")[1:]
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		vol = int(content[1])
		if 0 <= vol <= 100:
			player_env = json.load(open(path+'/player_env.json', 'r'))
			player_env['Volume'][0] = player_env['Volume'][1]
			player_env['Volume'][1] = vol
			if (vc.source != None):
				vc.source = discord.PCMVolumeTransformer(vc.source)
				vc.source.volume = player_env['Volume'][1]*(vc.source.volume/player_env['Volume'][0])
			await message.channel.send('Changed volume to '+str(vol))
			json.dump(player_env, open(path+'/player_env.json', 'w'))
		else:
			await message.channel.send('Send a volume between 0 and 100!')
	
	async def now_playing(self, message):
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			if player_env['Playing']['Title'] is None:
				await message.channel.send("No music is playing")
			else:
				embed = embed_gen.now_playing(player_env['Playing'], vc.is_paused())
				await message.channel.send(embed=embed)
		elif player_env['Mode'] == 'radio':
			results,file = radio_browser.now_playing(path)
			if results != 'code:youscrewedup' and file != None:
				await message.channel.send(embed=results, file=file)
			else:
				await message.channel.send('Ring O security breach !!!.\nEither data has been tampered by malicious author :(\nOr it is the admin messing around :)')
	
	async def skip_track(self, message):
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			vc.stop()
			embed = embed_gen.skip_track(player_env['Playing'])
			await message.channel.send(embed=embed)
		elif player_env['Mode'] == 'radio':
			await message.channel.send('You are playing radio, there is nothing to skip!')

	async def queue(self, message):
		content = message.content.split(" ")[1:]
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		keyword = ""
		for word in content[1:]:
			keyword += word + " "
		raw,embed = soundcloud_music.ydl_extract(keyword)
		music_queue = json.load(open(path+'/music_queue.json', 'r'))
		music_queue.append({'Title':raw[0],'Duration':raw[1], 'Thumbnail':raw[2], 'Url':raw[3]})
		json.dump(music_queue, open(path+'/music_queue.json', 'w'))
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			await message.channel.send(embed=embed)
			if player_env['IsRunning'] == False:
				rmqp.play(vc, path)

	async def play_radio(self, message):
		content = message.content.split(" ")[1:]
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		stream_url = content[1]
		player_env = json.load(open(path+'/player_env.json', 'r'))
		player_env['Mode'] = 'radio'
		player_env['IsRunning'] = True
		json.dump(player_env, open(path+'/player_env.json', 'w'))
		embed = rmqp.play_radio(vc, path, stream_url)
		await message.channel.send(embed=embed)
	
	async def stop_radio(self, message):
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'radio':
			vc.stop()
			playing = {'Title':None, 'Duration':None, 'Thumbnail':None, "Genre":None, "Stream":None}
			player_env['Playing'] = playing
			player_env['Mode'] = 'queue'
			player_env['IsRunning'] = False
			json.dump(player_env, open(path+'/player_env.json', 'w'))
			await message.channel.send('Switched to queue mode')
		elif player_env['Mode'] == 'queue':
			await message.channel.send('Queue mode has no access over radio!')

	async def list_queue(self, message):
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			embed = embed_gen.list_queue(json.load(open(path+'/music_queue.json', 'r')))
			await message.channel.send(embed=embed)
		elif player_env['Mode'] == 'radio':
			await message.channel.send('You are playing radio, there is no playlist, only magic!')

	async def drop_queue(self, message):
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			music_queue = json.load(open(path+'/music_queue.json', 'r'))
			music_queue = []
			json.dump(music_queue, open(path+'/music_queue.json', 'w'))
			vc.stop()
			await message.channel.send('Music-queue for '+str(vc.channel)+' in '+message.author.guild.name+' dropped')
		elif player_env['Mode'] == 'radio':
			await message.channel.send('Queue can only be dropped when in queue mode')
