Notes:-

1. Entry point for functions are defined in cogs.py, class Cogs of cogs.py is inherited by Bot class,
so every defined function in cogs.py has access to self and message.

2. Bot class has some general use functions such as :-
 = self.write_error() -> Writes error from stack trace
 = self.buttons -> List of defined emojis for buttons from defaults.json
 = self.helpbook() -> is a list of defined functions made available by the map
 = self.extract_query() -> Returns a ctx variable and a query processed from the third word till last
 = self.extract_keyword() -> Returns a ctx variable and a keyword which is the third word
 Note:- All of my defined interactions use Messagable Object but since many others use ctx, it is provided.
 = self.map -> Is a collection of function pointer mapped to a string, The bot when invoked by a prefix checks the next word, if that word matches a mapping,
 it invokes said function pointer with only two paramteres (self, message). This is a inherent limitation of this design, but the functionality of these two make up for it.

3. How to write a function :-
= This is completly up to you, i use a assembly line architecture for the entire program. So priviliged variables are only available upto cogs.py with imported functions only receving necessary data
and returning the output. The function in cogs.py must use these privileged functions to make a function pipeline from receving to sending. This ofcourse you can change.

4. Web-api :-
= class Webserver of webserver.py acts a api-server using aiohttp framework. Various endpoints for metrics are available. index.html loads this data through these endpoints, so it acts as a PWA without being a PWA?? lol.
(PWA = Progressive web app). New api-endpoints can be added.

5. Functions of bot in general :-
A. Housekeeping
-> hostinfo, ping, reset-env and others
B. AniList
-> Browse Anilist search for manga,anime and characters
C. Music
-> Browse youtube or radios (using pyradios api) for songs
-> Allows playing of songs,radios and youtube playlists
-> System is integrated, so if radio is running the other cant run
D. Soulseek
-> Soulseek is a p2p file sharing program most popularly used to share high quality flacs
-> Housekeeping functions for list,remove,add of (username, password) required to login to soulseek network
-> Search for songs on soulseek and use the search result to Download songs, exact pipeline usage in Functions.md