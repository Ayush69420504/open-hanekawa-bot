import discord,json,logging,traceback,sys,uuid,os,socket,uvloop,asyncio,time,aiohttp
from discord.ext import commands,tasks

#decryptor.py having the function to decrypt the token 
from utils import decryptor
#defaults_generator.py generates a default config folder for every voice channel, containing the music_queue.json and player_env.json
from utils import defaults_generator
#webserver.py is the main web server will be used for monitoring
import webserver
#cogs.py contain command definitions
import cogs

defaults=json.load(open('defaults.json', 'r'))

#Waits until dns.google and discord.com is reachable
#Certain cases where SBC server and router are wired to the same power supply will have different boot times
#Server will usually be available before network-online is
#Does not rely on any help from launch scripts and works with any process manager
#Updated to work on containers with no access to basic linux tools

def ping(host, port, timeout):
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		print(host+" "+str(port)+" pinged successfully")
		return True
	except socket.error as ex:
		print(ex)
		return False


while True:
	ra = ping(host="dns.google", port=53, timeout=3)
	rb = ping(host="discord.com", port=53, timeout=3)
	if ra and rb == True:
		print("Network checks completed, Starting Bot")
		break

def process_and_archive_logs():
	fps = ['logs/discord.log', 'logs/webserver.log', 'logs/invidious.log']
	for fp in fps:
		data = open(fp, "r").read()
		if data == "": continue
		first = data.split('\n')[0][:22]
		last = data.split('\n')[len(data.split('\n'))-2][:22]
		backup = 'logs/backup/'+fp[5:len(fp)-4]+' '+first+' - '+last+' .log'
		open(backup, "w").write(data)


class DiscordBot(commands.Bot, cogs.Cogs):

	buttons = None
	ready = False
	map = None
	helpbook = None
	logger = None

	def __init__(self, command_prefix, intents):
		activity = discord.Activity(type=discord.ActivityType.listening, name=defaults["prefix_"+defaults["ego"]])
		status = discord.Status.idle
		commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, activity=activity, status=status)
		cogs.Cogs.__init__(self, defaults=defaults)
		self.logger = logging.getLogger('discord')
		self.logger.setLevel(logging.DEBUG)
		bot_handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
		bot_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
		self.logger.addHandler(bot_handler)

	async def on_ready(self):
		print('Discord.py: Logged in as '+str(self.user))
		self.buttons = defaults['buttons']
		#This map can also be defined in cogs.py
		self.map = {"help" : self.help, "ping" : self.ping, "hostinfo" : self.hostinfo, "urltoqr" : self.urltoqr, "wifitoqr" : self.wifitoqr, "search-subreddits" : self.search_subreddits,
		"random-sub-post" : self.random_sub_post, "search-reddit-posts" : self.search_reddit_posts, "search-people" : self.search_people, "search-magazines" : self.search_magazines, "search-clubs" : self.search_clubs, "search-characters" : self.search_characters, "search-anime" : self.search_anime, "search-manga" : self.search_manga, "search-song" : self.search_song,
		"search-playlists" : self.search_playlists, "search-radios" : self.search_radio, "joinvc" : self.joinvc, "leavevc" : self.leavevc, "pause" : self.pause, "stats.invidious" : self.report_invidious_stats, "stats.jikan" : self.report_jikan_stats, 'stats.RB' : self.report_RB_stats,
		"resume" : self.resume, "reset-env" : self.reset_env, "current-volume" : self.current_volume, "volume" : self.volume, "now-playing" : self.now_playing, "skip-track" : self.skip_track, "queue" : self.queue,
		"playlist" : self.playlist, "stop-playlist" : self.stop_playlist, "play-radio" : self.play_radio, "stop-radio" : self.stop_radio, "list-queue" : self.list_queue, "drop-queue" : self.drop_queue,
		"hackernews" : self.hackernews}
		self.helpbook = self.generate_helpbook()
		self.ready = True

	async def setup_hook(self):
		task = asyncio.create_task(self.resolve_invidious_instances_onboot())
		task = asyncio.create_task(self.rDNS_lookup_RB_api())

	async def async_cleanup(self):
		print("Bot closes?")

	async def close(self):
		await self.async_cleanup()
		await super().close()

	def generate_share_data(self):
		helpbook = self.generate_helpbook()
		data = {'bot_name': str(self.user), 'bot_ego' : defaults['ego'], 'num_guilds' : len(self.guilds), 'num_functions' : len(self.map), 'workdir' : os.getcwd(), 'ego_prefix' : defaults["prefix_"+defaults["ego"]].strip(), 'helpbook' : helpbook}
		return data
	
	def generate_helpbook(self):
		key_list = list(self.map.keys())
		helpbook = {}
		for key in key_list:
			helpbook[key] = str(self.map[key].__doc__)
		return helpbook
	
	async def write_error(self):
		exceptions = traceback.format_exception(*sys.exc_info())
		_uuid = str(uuid.uuid4())
		err = "UUID = "+_uuid+"\n"
		for exception in exceptions:
			err += exception + '\n'
		open('logs/general_errors.log', 'a').write(err)
		return _uuid
	
	async def extract_query(self, message):
		ctx = await self.get_context(message)
		content = message.content.split(" ")[2:]
		query = ""
		for word in content:
			query += word + ' '
		return ctx,query
	
	async def extract_keyword(self, message):
		ctx = await self.get_context(message)
		keyword = message.content.split(" ")[2]
		return ctx,keyword
	
	async def on_message(self, message):
		defaults_generator.gen(message.guild.id)
		#The tally list is used to check origin of error and return appropriate error messages
		content = message.content.split(" ")
		if message.author != self.user and content[0] == defaults["prefix_"+defaults["ego"]].strip():
			content = content[1:]
			if len(content) == 0:
				await message.channel.send('User-kun! I don\'t know what you want? You have to tell me!');
			else:
				'''
				The idea is that the bot is initially idle, when it recevies a message,
				it changes activity to doing that, returns data and changes state to idle again.
				So it looks like the bot is "doing" some work, just a little metaphorical bullshit i like :)
				'''
				activity = discord.Game(name=defaults["prefix_"+defaults["ego"]]+content[0])
				status = discord.Status.online
				await self.change_presence(activity=activity, status=status)
				try:
					#Magic function / Maps a text literal to a function call
					await self.map[content[0]](message)
				except Exception as e:
					if type(e).__name__ == 'KeyError':
						await self.write_error()
						await message.channel.send('User-kun, I don\'t know what that command means (*＞ω＜*)')
					else:
						await self.write_error()
						await message.channel.send('User-kun, You should not be reading this.\nSomething very yabai has happened.\nReport to your bot admins immediately.')

			activity = discord.Activity(type=discord.ActivityType.listening, name=defaults["prefix_"+defaults["ego"]])
			status = discord.Status.idle
			await self.change_presence(activity=activity, status=status)

async def main():
	process_and_archive_logs()
	intents = discord.Intents.default()
	intents.message_content = True
	bot = DiscordBot(command_prefix=defaults["prefix_"+defaults["ego"]], intents=intents)
	await webserver.Server(discord_bot=bot, static_folder='web/static', template_folder='web/templates').start_server()
	await bot.start(token=decryptor.imposter())

'''
Multiple ways of token encryption has been implemented

1. No encryption : decryptor.imposter() / Use this if you don't care about privacy, but to prevent accidental token breaches ignore this.
2. Fernet encryption : decryptor.decrypted_token() / Personal favourite, encrypts to prevent data loss in a breach, but is runtime lenient
/ You have to generate the .key and encrypted-token by yourself
'''

if __name__ == "__main__":
	if sys.version_info >= (3, 11):
		with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
			runner.run(main())
	else:
		uvloop.install()
		asyncio.run(main())
