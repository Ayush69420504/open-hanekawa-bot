import discord,json,shutil,decorator,pstats
from dpy_paginator import paginate
from threading import Thread

#hackernews.py uses the https://hacker-news.firebaseio.com/v0/ api to get news!
import hackernews
#reddit.py is contains functions to scrape certain reddit websites
import reddit
#hostinfo.py having the function to return formatted data regarding system info
from utils import hostinfo
#soundcloud_music.py having youtube music playback capability
from utils import youtube_music
#radio_browser.py is an abstraction of the RadioBrowserApi in python using pyradios
from utils import radio_browser
#rmpq.py acroynm for recursive music queue player, it sucks, i know :(
import rmqp
#jikan.py is a multi-purpose MAL scrapper using the jikan api
import jikan
#embed_gen.py contains functions generating template embeds. Used to reduce code in main.py
from utils import embed_gen
#defaults_generator.py generates a default config folder for every voice channel, containing the music_queue.json and player_env.json
from utils import defaults_generator

class Cogs:
	
	leftbutton = None
	rightbutton = None

	@decorator.decorator
	async def general_error_handler(coro, self, message):
		actions = "For errors originating from human nature, please try fixing them yourself.\nFor more technical errors since these are recorded, report with uuid to the bot's admin or you may contact the dev.\nNote: It is not guranteed that the dev or admin will always have access to the logs :)"
		try:
			self.profiler.enable()
			await coro(self, message)
			self.profiler.disable()
			self.profiler.dump_stats('logs/profiler.prof')
			stream = open('logs/profiler.log', 'a')
			stats = pstats.Stats('logs/profiler.prof', stream=stream)
			stats.sort_stats('cumtime')
			stats.print_stats(15)
		except Exception as e:
			_uuid = self.write_error()
			embed = embed_gen.generate_error(str(e), actions, _uuid)
			await message.channel.send(embed=embed)
	
	@decorator.decorator
	async def music_error_handler(coro, self, message):
		try:
			self.profiler.enable()
			await coro(self, message)
			self.profiler.disable()
			self.profiler.dump_stats('logs/profiler.prof')
			stream = open('logs/profiler.log', 'a')
			stats = pstats.Stats('logs/profiler.prof', stream=stream)
			stats.sort_stats('cumtime')
			stats.print_stats(15)
		except AttributeError:
			_uuid = self.write_error()
			actions = 'This error is most likely caused by you not being in a voice channel !\nIf this is not the case, it is logged so report the error with uuid'
			embed = embed_gen.generate_error("No connected voice channel found!", actions, _uuid)
			await message.channel.send(embed=embed)
		except Exception as e:
			_uuid = self.write_error()
			actions = "For errors originating from human nature, please try fixing them yourself.\nFor more technical errors since these are recorded, report with uuid to the bot's admin or you may contact the dev.\nNote: It is not guranteed that the dev or admin will always have access to the logs :)"
			embed = embed_gen.generate_error(str(e), actions, _uuid)
			await message.channel.send(embed=embed)

	def __init__(self, defaults):
		self.leftbutton = discord.ui.Button(emoji=self.get_emoji(defaults['leftbutton']))
		self.rightbutton = discord.ui.Button(emoji=self.get_emoji(defaults['rightbutton']))

	@general_error_handler
	async def search_playlists(self, message):
		'''
		Searches 10 playlists from Youtube
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = youtube_music.playlist_search(query)
		output = paginate(embeds=embeds, timeout=600)
		await message.channel.send(embed=output.embed, view=output.view)

	@general_error_handler
	async def search_reddit_posts(self, message):
		'''
		Searches 10 relevant posts to the query using reddit json api
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = reddit.search_reddit_posts(query)
		output = paginate(embeds=embeds, timeout=600)
		await message.channel.send(embed=output.embed, view=output.view)

	@general_error_handler
	async def random_sub_post(self, message):
		'''
		Uses a subreddit name to display a random subreddit post that is available is guest user through reddit json api
		Note: Provide the subreddit name with no prefix
		Aceepts : Keyword (subreddit_name_noprefix)
		Returns : Sucess Embed or Error Embed
		'''
		ctx,keyword = await self.extract_keyword(message)
		embed = reddit.random_sub_post(keyword)
		await message.channel.send(embed=embed)
	
	@general_error_handler
	async def search_subreddits(self, message):
		'''
		Uses the reddit json api to query search results for 10 subreddits
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = reddit.search_subreddits(query)
		output = paginate(embeds=embeds, timeout=600)
		await message.channel.send(embed=output.embed, view=output.view)
		
	@general_error_handler
	async def search_radio_1(self, message):
		'''
		Queries radio database in pyradios,
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = radio_browser.search_stations(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send('No search results :(')

	@general_error_handler
	async def hackernews(self, message):
		'''
		Searches hackernews by topstories/beststories/newstories,
		Accepts : keyword
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_keyword(message)
		results = hackernews.gate(query)
		if type(results) is str:
			await message.channel.send(results)
		elif type(results) is list:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)

	@general_error_handler
	async def help(self, message):
		'''
		Help function, lists a whoami and pages of commands help
		Accepts : None
		Returns : Paginated Embed
		'''
		ctx = await self.get_context(message)
		embeds = embed_gen.help(self.helpbook)
		output = paginate(embeds=embeds, timeout=600)
		await message.channel.send(embed=output.embed, view=output.view)
	
	@general_error_handler
	async def ping(self, message):
		'''
		Ping -> Pong, measures latency of bot connection to server,
		Accepts : None
		Returns : Text
		'''
		await message.channel.send(f'Pong: {int(self.latency*1000)}ms')

	@general_error_handler
	async def hostinfo(self, message):
		'''
		Returns a htop / Task Manager view of system usage
		Accepts : None
		Returns : Embed
		'''
		await message.channel.send(embed=hostinfo.getSystemInfo())
	
	@general_error_handler
	async def urltoqr(self, message):
		'''
		Converts a url/link to a qr code using googleapis,
		Accepts : keyword
		Returns : url/type-img
		'''
		ctx,url = await self.extract_keyword(message)
		url = 'https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl='+url+'&choe=UTF-8'
		await message.channel.send(url)
	
	@general_error_handler
	async def wifitoqr(self, message):
		'''
		Converts a list of data to a wifi qr code
		Accepts : ssid (string), encryption (string), password (string)
		Returns : url/type-img
		'''
		content = message.content.split(" ")[2:]
		ssid = content[0]
		encryption = content[1]
		password = content[2]
		chl = 'WIFI:S:'+ssid+';T:'+encryption+';P:'+password+';H:false;;'
		url = 'https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl='+chl+'&choe=UTF-8'
		await message.channel.send(url)

	@general_error_handler
	async def search_people(self, message):
		'''
		Searches for people in the MAL database using jikan api
		Accepts : Query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = jikan.search_people(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send("No results :(")

	@general_error_handler
	async def search_magazines(self, message):
		'''
		Searches for MAL magazines using jikan api
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = jikan.search_magazines(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send("No results :(")
	
	@general_error_handler
	async def search_clubs(self, message):
		'''
		Searches for MAL clubs using jikan api
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = jikan.search_clubs(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send("No results :(")

	@general_error_handler
	async def search_characters(self, message):
		'''
		Searches for anime and manga characters using jikan api
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = jikan.search_characters(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send("No results :(")

	@general_error_handler
	async def search_anime(self, message):
		'''
		Searches for anime using jikan api
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = jikan.search_anime(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send("No results :(")

	@general_error_handler
	async def search_manga(self, message):
		'''
		Searches for manga using jikan api
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = jikan.search_manga(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send("No results :(")
		
	@general_error_handler
	async def search_song(self, message):
		'''
		Searches for a song in soundcloud database
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = youtube_music.ydl_list_search(query)
		output = paginate(embeds=embeds, timeout=600)
		await message.channel.send(embed=output.embed, view=output.view)

	@general_error_handler
	async def search_radio_2(self, message):
		'''
		Queries radio database in https://www.internet-radio.com/,
		Accepts : query
		Returns : Paginated Embed
		'''
		ctx,query = await self.extract_query(message)
		embeds = radio_browser.search_stations_extended(query)
		if len(embeds) != 0:
			output = paginate(embeds=embeds, timeout=600)
			await message.channel.send(embed=output.embed, view=output.view)
		else:
			await message.channel.send("No search results :(")
	
	@music_error_handler
	async def joinvc(self, message):
		'''
		Joins the voice chat of user, errors out if no voice channel,
		Accepts : None
		Returns : Text
		'''
		try:
			await message.author.voice.channel.connect()
			await message.channel.send('Joined: '+str(message.author.voice.channel))
		except Exception as e:
			if type(e).__name__ == "ClientException":
				await message.channel.send('I cannot have more than one instance in guild: '+message.author.guild.name)
			elif type(e).__name__ == "AttributeError":
				await message.channel.send("Not in a voice channel !")
		
	@music_error_handler
	async def leavevc(self, message):
		'''
		Leaves the currently joined voice chat, errors out when no voice channel
		Accepts : None
		Returns : Text
		'''
		vc = message.guild.voice_client
		await vc.disconnect()
		await message.channel.send('Left: '+str(vc.channel))

	@music_error_handler
	async def pause(self, message):
		'''
		Pauses the music player of guild,
		Accepts : None
		Returns : Text
		'''
		vc = message.guild.voice_client
		vc.pause()
		await message.channel.send('Paused audio in '+str(vc.channel))
	
	@music_error_handler
	async def resume(self, message):
		'''
		Resumes the music player in guild,
		Accepts : None
		Returns : Text
		'''
		vc = message.guild.voice_client
		vc.resume()
		await message.channel.send('Resumed audio in '+str(vc.channel))

	@general_error_handler
	async def reset_env(self, message):
		'''
		Resets the player_env.json music_queue.json playlist.json of a guild
		Accepts : None
		Returns : Text (String)
		'''
		path = 'server-audio-sessions/'+str(message.guild.id)
		shutil.rmtree(path)
		defaults_generator.gen(message.guild.id)
		await message.channel.send("Reset env variables in "+message.author.guild.name)

	@general_error_handler
	async def current_volume(self, message):
		'''
		Returns the saved volume setting for a particular guild,
		Accepts : None
		Returns : Text (String) : Text (int)
		'''
		path = 'server-audio-sessions/'+str(message.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		await message.channel.send('Current Volume: '+str(player_env['Volume'][1]))

	@music_error_handler
	async def volume(self, message):
		'''
		Sets the volume of a particular guild, this is saved,
		Accepts : keyword (int)
		Returns : Conformation message (Text/String)
		'''
		ctx,keyword = await self.extract_keyword(message)
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		vol = int(keyword)
		if 0 <= vol <= 100:
			player_env = json.load(open(path+'/player_env.json', 'r'))
			player_env['Volume'][0] = player_env['Volume'][1]
			player_env['Volume'][1] = vol
			if (vc.source != None):
				vc.source.volume = player_env['Volume'][1]*(vc.source.volume/player_env['Volume'][0])
			await message.channel.send('Changed volume to '+str(vol))
			json.dump(player_env, open(path+'/player_env.json', 'w'))
		else:
			await message.channel.send('Send a volume between 0 and 100!')
	
	@music_error_handler
	async def now_playing(self, message):
		'''
		Shows the currently playing track in queue or the radio stream,
		Requires : Queue Mode or Radio Mode
		Accepts : None
		Returns : Embed
		'''
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue' or player_env['Mode'] == 'playlist':
			if player_env['Playing']['Title'] is None:
				await message.channel.send("No music is playing")
			else:
				embed = embed_gen.now_playing(player_env['Playing'], vc.is_paused())
				await message.channel.send(embed=embed)
		elif player_env['Mode'] == 'radio':
			results = radio_browser.now_playing(path)
			if results != 'code:youscrewedup':
				await message.channel.send(embed=results)
			else:
				await message.channel.send('Ring O security breach !!!.\nEither data has been tampered by malicious author :(\nOr it is the admin messing around :)')
	
	@music_error_handler
	async def skip_track(self, message):
		'''
		Skips playing track in queue, removes it from list and moves on to next,
		Requires : Queue Mode
		Accepts : None
		Returns : Conformation Embed
		'''
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue' or player_env['Mode'] == 'playlist':
			vc.stop()
			embed = embed_gen.skip_track(player_env['Playing'])
			await message.channel.send(embed=embed)
		elif player_env['Mode'] == 'radio':
			await message.channel.send('You are playing radio, there is nothing to skip!')

	@music_error_handler
	async def playlist(self, message):
		'''
		Accepts a playlist-id that is supplied from search-playlists and uses it to create a music queue
		If other modes on, then it will stop them and start "playlist" mode
		Requires : Any Mode
		Accepts : keyword (playlist-id)
		Returns : Embed
		'''
		ctx,keyword = await self.extract_keyword(message)
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		playlist,embed = youtube_music.playlist_extract(keyword)
		json.dump(playlist, open(path+'/playlist.json', 'w'))
		player_env = json.load(open(path+'/player_env.json', 'r'))
		player_env['Mode'] = 'playlist'
		player_env['IsRunning'] = True
		json.dump(player_env, open(path+'/player_env.json', 'w'))
		thread = Thread(target=rmqp.play_list, args=(vc, path, ))
		thread.start()
		await message.channel.send(embed=embed)
		
	@music_error_handler
	async def stop_playlist(self, message):
		'''
		Stops the currently playing playlist, this method should be reffered instead of a drop_queue
		like system of stopping in case of playlists
		Requires : Queue Mode
		Accepts : None
		Returns : Text
		'''
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		playlist = json.load(open(path+'/playlist.json', 'r'))
		if player_env['Mode'] == 'playlist':
			playlist = []
			json.dump(playlist, open(path+'/playlist.json', 'w'))
			playing = {'Title':None, 'Duration':None, 'Thumbnail':None, "Genre":None, "Stream":None}
			player_env['Playing'] = playing
			player_env['Mode'] = 'queue'
			player_env['IsRunning'] = False
			json.dump(playlist, open(path+'/playlist.json', 'w'))
			json.dump(player_env, open(path+'/player_env.json', 'w'))
			vc.stop()
			await message.channel.send('Switched to queue mode')
		elif player_env['Mode'] == 'queue':
			await message.channel.send('Queue mode has no access over radio!')
		elif player_env['Mode'] == 'radio':
			await message.channel.send('Radio mode has no access over radio!')
	
	@music_error_handler
	async def queue(self, message):
		'''
		accepts a query, searches in soundcloud and add it the guild's music playlist,
		if playing, it will be added to queue,
		if paused, it will be added to queue and music player will be started
		Requires : Queue Mode or Radio Mode
		Accepts : query
		Returns : Embed
		'''
		ctx,query = await self.extract_query(message)
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		raw,embed = youtube_music.ydl_extract(query)
		music_queue = json.load(open(path+'/music_queue.json', 'r'))
		music_queue.append({'Title':raw[0],'Duration':raw[1], 'Thumbnail':raw[2], 'Url':raw[3]})
		json.dump(music_queue, open(path+'/music_queue.json', 'w'))
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			await message.channel.send(embed=embed)
			if player_env['IsRunning'] == False:
				thread = Thread(target=rmqp.play, args=(vc, path, ))
				thread.start()

	@music_error_handler
	async def play_radio(self, message):
		'''
		Plays a radio station on basis of it's stream url, that can be obtained from search_radios,
		Requires : Queue Mode or Radio Mode
		Accepts : keyword
		Returns : Embed
		'''
		ctx,keyword = await self.extract_keyword(message)
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		stream_url = keyword
		player_env = json.load(open(path+'/player_env.json', 'r'))
		player_env['Mode'] = 'radio'
		player_env['IsRunning'] = True
		json.dump(player_env, open(path+'/player_env.json', 'w'))
		embed = rmqp.play_radio(vc, path, stream_url)
		await message.channel.send(embed=embed)
	
	@music_error_handler
	async def stop_radio(self, message):
		'''
		Stops the radio player and switches to queue mode,
		Requires : Queue Mode
		Accepts : None
		Returns : Text
		'''
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
		elif player_env['Mode'] == 'playlist':
			await message.channel.send('Playlist mode has no access over radio!')

	@music_error_handler
	async def list_queue(self, message):
		'''
		Lists queue in queue mode
		Requires :: Queue Mode
		Accepts : None
		Returns : Embed
		'''
		ctx = await self.get_context(message)
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			embed = embed_gen.list_queue(json.load(open(path+'/music_queue.json', 'r')))
			await message.channel.send(embed=embed)
		elif player_env['Mode'] == 'playlist':
			embed = embed_gen.list_queue(json.load(open(path+'/playlist.json', 'r')))
			await message.channel.send(embed=embed)
		elif player_env['Mode'] == 'radio':
			await message.channel.send('You are playing radio, there is no playlist, only magic!')

	@music_error_handler
	async def drop_queue(self, message):
		'''
		Drops the music queue and stops music player in queue mode,
		Requires : Queue Mode
		Accepts : None
		Returns : Text
		'''
		vc = message.guild.voice_client
		path = 'server-audio-sessions/'+str(vc.guild.id)
		player_env = json.load(open(path+'/player_env.json', 'r'))
		if player_env['Mode'] == 'queue':
			music_queue = json.load(open(path+'/music_queue.json', 'r'))
			music_queue = []
			json.dump(music_queue, open(path+'/music_queue.json', 'w'))
			vc.stop()
			await message.channel.send('Music-queue for '+str(vc.channel)+' in '+message.author.guild.name+' dropped')
		elif player_env['Mode'] == 'playlist':
			await message.channel.send("To drop the playlist, stop it using stop-playlist\nThis function has no access over playlist mode")
		elif player_env['Mode'] == 'radio':
			await message.channel.send('Queue can only be dropped when in queue mode')
