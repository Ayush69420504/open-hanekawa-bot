import json,os

def gen(guild_id):
	files_exist = os.path.exists('server-audio-sessions/'+str(guild_id))
	if not files_exist:
		default_queue = []
		playing = {'Title':None, 'Duration':None, 'Thumbnail':None, 'Genre':None, 'Stream':None}
		default_player_env = {'Playing':playing, 'IsRunning':False, 'Mode':'queue', 'Volume':[None, 100]}
		os.makedirs('server-audio-sessions/'+str(guild_id))
		with open('server-audio-sessions/'+str(guild_id)+'/music_queue.json', 'w') as music_queue:
			json.dump(default_queue, music_queue)
		with open('server-audio-sessions/'+str(guild_id)+'/player_env.json', 'w') as player_env:
			json.dump(default_player_env, player_env)
