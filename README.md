Open source release of Hanekawa-san, my private discord bot

The original code is in a private repo, this is commit #37 adapted to public use.

Version : 1.2.3 release date: 08/08/24

Updated from : ver 1.2.0 release date: 22/04/24 Commit #25

Note: If you only care for functionality refer to Functions.md
Note: If you want to develop but are lost with the architecture of the system refer to How_to_develop.md

Changes :- Fixing the errors that came with ver 1.2.0 plus backend overhaul for music and webserver and logging.
1. Logging is still present but function memory stacks are no longer logged and no profiler exists. The issuses were more than the results. They are removed
2. Program start flows are changed, each step wrapped under a func and neatly packed into a async coroutine run under uvloop, for performance improvements.
-> Logs archival and processing -> Initialise bot class -> Asyncronously call bot class and webserver class.
3. Logging finally has archives, that are stored in a nested backups folder with the date and time mentioned
4. Youtube Music has been changed. Now it queries all its data from invidious instances resolved at boot, and updated every hour, they are sorted by lowest latency.
5. Radio Browser is revamped. Web scrapping internet-radios.com is stupid so ditched in favour of all.api.radio-browser.com. which has a huge library of json lists.
6. Two huge dependecies yt-dlp and beautifull soup 4 are ditched so significantly lighter i guess.
7. Uvicorn is ditched, reducing another big dependecy. Now it uses aiohttp lib's AppRunner class to run a async TCP site. Added new invidious log endpoint.
8. Music player is now asynchronous instead of multi threaded. Makes it smoother, less prone to errors. And is better than my old solution that i forgor to update :).
9. Stats reporting through bot added for jikan, invidious and radio-browser.
10. Is actually usable right out of box compared to previous release.

How to run :-
1. Barebones
 = Create a venv or not, i do not care. requirements.txt contains all libraries needed. Check the proper architecture for ffmpeg-static. defaults.json must be set with a ego, prefix and proper token be written to respective token file.
2. Docker
 = Set the ego, prefix, auth_token for your bot. And buid the image. Size should be around 500-600 MB on disk. Port 6900 is to be exposed, no other requirements.

Note: The data available in data folder is free to use :)

Note: Hanekawa-san.service is a systemd service file that manages starting of discord bot on boot time

Note: Message replies are hard coded in a speech manner resembling Hanekawa Tsubasa san a side character in the monogatari series and light novels by nisio isin

Note: https://www.youtube.com/watch?v=QmMcE3SZZlY see this video to understand her character

My request: Watch the Monogatari series :) You will experience literary knowledge and a existential crisis at the same time. Source : Trust me bro.
 
 
