Hanekawa-san is a multipurpose discord bot, it has multimedia functions and no admin functions.

I must clarify that in no way i intend to turn this into a moderation bot. But if the bot requires admin privliges,
a developer can add such functions, Refer to How_to_develop.md

Functions as of version 1.2.3

Total: 35 functions

1. help
Help function, lists a whoami and pages of commands help
Accepts : None
Returns : Paginated Embed

2. ping
Ping -> Pong, measures latency of bot connection to server,
Accepts : None
Returns : Text

3. hostinfo
Returns a htop / Task Manager view of system usage
Accepts : None
Returns : Embed

4. urltoqr
Converts a url/link to a qr code using googleapis,
Accepts : keyword
Returns : url/type-img

5. wifitoqr
Converts a list of data to a wifi qr code
Accepts : ssid (string), encryption (string), password (string)
Returns : url/type-img

6. search-subreddits
Uses the reddit json api to query search results for 10 subreddits
Accepts : query
Returns : Paginated Embed

7. random-sub-post
Uses a subreddit name to display a random subreddit post that is available is guest user through reddit json api
Note: Provide the subreddit name with no prefix
Aceepts : Keyword (subreddit_name_noprefix)
Returns : Sucess Embed or Error Embed

8. search-reddit-posts
Searches 10 relevant posts to the query using reddit json api
Accepts : query
Returns : Paginated Embed

9. search-people
Searches for people in the MAL database using jikan api
Accepts : Query
Returns : Paginated Embed

10. search-magazines
Searches for MAL magazines using jikan api
Accepts : query
Returns : Paginated Embed

11. search-clubs
Searches for MAL clubs using jikan api
Accepts : query
Returns : Paginated Embed

12. search-characters
Searches for anime and manga characters using jikan api
Accepts : query
Returns : Paginated Embed

13. search-anime
Searches for anime using jikan api
Accepts : query
Returns : Paginated Embed

14. search-manga
Searches for manga using jikan api
Accepts : query
Returns : Paginated Embed

15. search-song
Searches for a song in soundcloud database
Accepts : query
Returns : Paginated Embed

16. search-playlists
Searches 10 playlists from Youtube
Accepts : query
Returns : Paginated Embed

17. search-radios
Queries radio database in https://all.api.radio-browser.info,
Accepts : query
Returns : Paginated Embed

18. joinvc
Joins the voice chat of user, errors out if no voice channel,
Accepts : None
Returns : Text

19. leavevc
Leaves the currently joined voice chat, errors out when no voice channel
Accepts : None
Returns : Text

20. pause
Pauses the music player of guild,
Accepts : None
Returns : Text

21. resume
Resumes the music player in guild,
Accepts : None
Returns : Text

22. reset-env
Resets the player_env.json music_queue.json playlist.json of a guild
Accepts : None
Returns : Text (String)

23. current-volume
Returns the saved volume setting for a particular guild,
Accepts : None
Returns : Text (String) : Text (int)

24. volume
Sets the volume of a particular guild, this is saved,
Accepts : keyword (int)
Returns : Conformation message (Text/String)

25. now-playing
Shows the currently playing track in queue or the radio stream,
Requires : Queue Mode or Radio Mode
Accepts : None
Returns : Embed

26. skip-track
Skips playing track in queue, removes it from list and moves on to next,
Requires : Queue Mode
Accepts : None
Returns : Conformation Embed

27. queue
accepts a query, searches in soundcloud and add it the guild's music playlist,
if playing, it will be added to queue,
if paused, it will be added to queue and music player will be started
Requires : Queue Mode or Radio Mode
Accepts : query
Returns : Embed

28. playlist
Accepts a playlist-id that is supplied from search-playlists and uses it to create a music queue
If other modes on, then it will stop them and start "playlist" mode
Requires : Any Mode
Accepts : keyword (playlist-id)
Returns : Embed

29. stop-playlist
Stops the currently playing playlist, this method should be reffered instead of a drop_queue
like system of stopping in case of playlists
Requires : Queue Mode
Accepts : None
Returns : Text

30. play-radio
Plays a radio station on basis of it's stream url, that can be obtained from search_radios,
Requires : Queue Mode or Radio Mode
Accepts : keyword
Returns : Embed

31. stop-radio
Stops the radio player and switches to queue mode,
Requires : Queue Mode
Accepts : None
Returns : Text

32. list-queue
Lists queue in queue mode
Requires :: Queue Mode
Accepts : None
Returns : Embed

33. drop-queue
Drops the music queue and stops music player in queue mode,
Requires : Queue Mode
Accepts : None
Returns : Text

34. hackernews
Searches hackernews by topstories/beststories/newstories,
Accepts : keyword
Returns : Paginated Embed
