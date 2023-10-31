import platform,re,psutil,datetime,time,sys,traceback,discord,json,os,subprocess

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

def getSystemInfo():
	try:
		conversion_constant = 1024**3
		embed = discord.Embed(title='HostInfo', color=embed_color)
		embed.add_field(name='Platform', value=platform.system())
		embed.add_field(name='Architecture', value=platform.machine())
		embed.add_field(name='Processor', value=get_processor_name())
		embed.add_field(name='Total Cpu usage', value=str(psutil.cpu_percent())+" %")
		embed.add_field(name='Total Ram usage', value=str(round(psutil.virtual_memory().used / conversion_constant, 2))+" / "+str(round(psutil.virtual_memory().total / conversion_constant, 2))+" GB")
		embed.add_field(name='Total Swap usage', value=str(round(psutil.swap_memory().used / conversion_constant, 2))+' / '+str(round(psutil.swap_memory().total / conversion_constant, 2))+' GB')
		embed.add_field(name='Uptime', value=str(datetime.timedelta(seconds=(time.time() - psutil.boot_time()))))
		return embed
	except:
		exception = str(traceback.format_exception(*sys.exc_info()))
		return exception

def get_processor_name():
	if platform.system() == "Windows":
		return platform.processor()
	elif platform.system() == "Darwin":
		os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
		command ="sysctl -n machdep.cpu.brand_string"
		return subprocess.check_output(command).strip()
	elif platform.system() == "Linux":
		command = "cat /proc/cpuinfo"
		all_info = subprocess.check_output(command, shell=True).decode().strip()
		for line in all_info.split("\n"):
			if "model name" in line:
				return re.sub( ".*model name.*:", "", line,1)
	return ""