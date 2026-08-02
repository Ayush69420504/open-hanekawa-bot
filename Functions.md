Hanekawa-san is a multipurpose discord bot, it has multimedia functions and no admin functions.

I must clarify that in no way i intend to turn this into a moderation bot. But if the bot requires admin privliges,
a developer can add such functions, Refer to How_to_develop.md

Functions as of version 1.5.0

Total: 32 functions

help
Help function, lists a whoami and pages of commands help
Accepts : None
Returns : Paginated Embed

ping
Ping -> Pong, measures latency of bot connection to server,
Accepts : None
Returns : Text

hostinfo
Returns a htop / Task Manager view of system usage
Accepts : None
Returns : Embed

search-songs-yt
Searches for a song in youtube database
Accepts : query
Returns : Paginated Embed

search-anime
Searches for a anime in AniList Database
Accepts : query
Returns : Embed

search-manga
Searches for a manga in AniList Database
Accepts : query
Returns : Embed

search-character
Searches for a character in AniList Database
Accepts : query
Returns : Embed

list-slsk-credentials
List the usernames of all the soulseek credentials of a guild
Accepts : None
Returns : Embed

remove-slsk-credentials
Removes a specified soulseek credential for a guild, Only allows removal if both parameters match.
Accepts : Query (Username + Password with a space in b/w)
Returns : Confirmation embed

add-slsk-credentials
Adds soulseek credentials for a guild, Adds a new entry if more than one, does not allow addition of duplicates
Accepts : Query (Username + Password with a space in b/w)
Returns : Confirmation embed

search-songs-slsk
Searches the soulseek network for songs
Accepts : Query (Username + Query)
Returns : Paginated Embeds or Failure Embed

download-song-slsk
Downloads a song/file from the soulseek network
Accepts : Query (Username + Peer Username + Filepath)
Retuns : Animated (By means of editing) embed which eventually returns a upload url of tmpfiles.org

search-playlists
Searches 10 playlists from Youtube
Accepts : query
Returns : Paginated Embed

search-radios
Queries radio database in all.api.radio-browser.info,
Accepts : query
Returns : Paginated Embed

joinvc
Joins the voice chat of user, errors out if no voice channel,
Accepts : None
Returns : Text

leavevc
Leaves the currently joined voice chat, errors out when no voice channel
Accepts : None
Returns : Text

pause
Pauses the music player of guild,
Accepts : None
Returns : Text

stats.RB
Reports the stats of all Radio Browser instances
Accepts : None
Returns : Embed

resume
Resumes the music player in guild,
Accepts : None
Returns : Text

reset-env
Resets the player_env.json music_queue.json playlist.json of a guild
Accepts : None
Returns : Text (String)

current-volume
Returns the saved volume setting for a particular guild,
Accepts : None
Returns : Text (String) : Text (int)

volume
Sets the volume of a particular guild, this is saved,
Accepts : keyword (int)
Returns : Conformation message (Text/String)

now-playing
Shows the currently playing track in queue or the radio stream,
Requires : Queue Mode or Radio Mode
Accepts : None
Returns : Embed

skip-track
Skips playing track in queue, removes it from list and moves on to next,
Requires : Queue Mode
Accepts : None
Returns : Conformation Embed

queue
accepts a query, searches in youtube and add it the guild's music playlist,
if playing, it will be added to queue,
if paused, it will be added to queue and music player will be started
Requires : Queue Mode or Radio Mode
Accepts : query
Returns : Embed

playlist
Accepts a playlist-id that is supplied from search-playlists and uses it to create a music queue
If other modes on, then it will stop them and start "playlist" mode
Requires : Any Mode
Accepts : keyword (playlist-id)
Returns : Embed

stop-playlist
Stops the currently playing playlist, this method should be reffered instead of a drop_queue
like system of stopping in case of playlists
Requires : Queue Mode
Accepts : None
Returns : Text

play-radio
Plays a radio station on basis of it's stream url, that can be obtained from search_radios,
Requires : Queue Mode or Radio Mode
Accepts : keyword
Returns : Embed

stop-radio
Stops the radio player and switches to queue mode,
Requires : Queue Mode
Accepts : None
Returns : Text

list-queue
Lists queue in queue mode
Requires :: Queue Mode
Accepts : None
Returns : Embed

drop-queue
Drops the music queue and stops music player in queue mode,
Requires : Queue Mode
Accepts : None
Returns : Text

hackernews
Searches hackernews by topstories/beststories/newstories,
Accepts : keyword
Returns : Paginated Embed