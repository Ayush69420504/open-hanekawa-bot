import discord,json,logging,traceback,sys,os,time,uvicorn
from discord.ext import commands
from threading import Thread
from functools import partial
from fastapi import FastAPI

#decryptor.py having the function to decrypt the token 
from utils import decryptor
#defaults_generator.py generates a default config folder for every voice channel, containing the music_queue.json and player_env.json
from utils import defaults_generator
#webserver.py is the main web server will be used for monitoring
import webserver
#cogs.py contain command definitions
import cogs

defaults=json.load(open('defaults.json', 'r'))

#Waits until discord.com is reachable
#Certain cases where SBC server and router are wired to the same power supply will have different boot times
#Server will usually be available before network-online is
#Does not rely on any help from launch scripts and works with any process manager
os.system('until ping -c1 discord.com; do sleep 2; done;')

class MyBot(commands.Bot, cogs.Cogs):

	leftbutton = None
	rightbutton = None
	ready = False
	map = None

	def __init__(self, command_prefix, intents):
		activity = discord.Activity(type=discord.ActivityType.listening, name='!ara')
		status = discord.Status.idle
		commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, activity=activity, status=status)
		cogs.Cogs.__init__(self, defaults=defaults)
	
	async def on_ready(self):
		print('Discord.py: Logged in as '+str(self.user))
		self.leftbutton = discord.ui.Button(emoji=self.get_emoji(defaults['leftbutton']))
		self.rightbutton = discord.ui.Button(emoji=self.get_emoji(defaults['rightbutton']))
		self.ready = True
		#This map can also be defined in cogs.py
		self.map = {"whoami" : self.whoami, "ping" : self.ping, "hostinfo" : self.hostinfo, "urltoqr" : self.urltoqr, "wifitoqr" : self.wifitoqr, "animeme" : self.animeme,
		"meme" : self.meme, "uncensored-hentai-meme" : self.uncensored_hentai_meme, "search-manga" : self.search_manga, "list-chapters" : self.list_chapters,
		"search-song" : self.search_song, "search-radio-1" : self.search_radio_1, "joinvc" : self.joinvc, "leavevc" : self.leavevc, "pause" : self.pause, "resume" : self.resume,
		"current-volume" : self.current_volume, "volume" : self.volume, "now-playing" : self.now_playing, "skip-track" : self.skip_track, "queue" : self.queue,
		"play-radio" : self.play_radio, "stop-radio" : self.stop_radio, "list-queue" : self.list_queue, "drop-queue" : self.drop_queue, "hackernews" : self.hackernews,
		"search-radio-2" : self.search_radio_2}

	async def on_message(self, message):
		defaults_generator.gen(message.guild.id)
		#The tally list is used to check origin of error and return appropriate error messages
		tally_list = ['joinvc', 'leavevc', 'pause', 'resume', 'current-volume', 'volume', 'queue', 'play-radio', 'stop-radio', 'list-queue', 'now-playing', 'drop-queue', 'skip-track']
		content = message.content.split(" ")
		if message.author != self.user and content[0] == '!ara':
			content = content[1:]
			if len(content) == 0:
				await message.channel.send('User-kun! I don\'t know what you want? You have to tell me!');
			else:
				'''
				The idea is that the bot is initially idle, when it recevies a message,
				it changes activity to doing that, returns data and changes state to idle again.
				So it looks like the bot is "doing" some work, just a little metaphorical bullshit i like :)
				'''
				activity = discord.Game(name='!ara '+content[0])
				status = discord.Status.online
				await self.change_presence(activity=activity, status=status)
				try:
					#Magic function / Maps a text literal to a function call
					await self.map[content[0]](message)
				except Exception as e:
					if type(e).__name__ == 'AttributeError':
						match = False
						if content[0] == tally_list[0]:
							await message.channel.send("Not in a voice channel")
						else:
							for tally in tally_list:
								if content[0] == tally:
									match = True
									await message.channel.send('I am not connected to your voice channel!')
									break
							if match == False:
								await message.channel.send('Something went wrong, try again or use different arguments!')
					elif type(e).__name__ == 'KeyError':
						exceptions = traceback.format_exception(*sys.exc_info())
						err = ''
						for exception in exceptions:
							err += exception + '\n'
						open('logs/general_errors.log', 'a').write(err)
						await message.channel.send('User-kun I don\'t know what that command means (*＞ω＜*)')
					else:
						exceptions = traceback.format_exception(*sys.exc_info())
						err = ''
						for exception in exceptions:
							err += exception + '\n'
						open('logs/general_errors.log', 'a').write(err)
						await message.channel.send('Something went wrong, try again or use different arguments!')

			activity = discord.Activity(type=discord.ActivityType.listening, name='!ara')
			status = discord.Status.idle
			await self.change_presence(activity=activity, status=status)

intents = discord.Intents.default()
intents.message_content = True
bot = MyBot(command_prefix='!ara ', intents=intents)
bot_handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')

'''
Multiple ways of token encryption has been implemented

1. No encryption : decryptor.imposter() / Use this if you don't care about privacy, but to prevent accidental token breaches ignore this.
2. Fernet encryption : decryptor.decrypted_token() / Personal favourite, encrypts to prevent data loss in a breach, but is runtime lenient
/ You have to generate the .key and encrypted-token by yourself
3. GPG encryption -> / Use this if you are paranoid and need encryption during run time at EVERY step
decryptor.gnu_encrypt() / Will ask for a email and password to create a .asc and encrypted_token
decryptor.gnu_decrypt() / Will require the password as per gpg working rules.
'''

#Discord Bot is run as a seperate thread under the main thread running the uvicorn web server
partial_run = partial(bot.run, decryptor.imposter(), log_handler=bot_handler, log_level=logging.DEBUG)
Thread(target=partial_run).start()

#Web server starts after getting client data that the bot is connected to
while bot.ready == False:
	time.sleep(1)

app = FastAPI(title=__name__)
webserver = webserver.Webserver(static_folder='web/static', template_folder='web/templates', discord_bot=bot)
app.include_router(webserver.router)
if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=6900, reload=False)
