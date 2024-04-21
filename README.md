Open source release of Hanekawa-san, my private discord bot

The original code is in a private repo, this is commit #25 adapted to public use.

Version : 1.2.0 release date: 22/04/24

Updated from : ver 1.1.5 release date: 11/02/24

Note: If you only care for functionality refer to Functions.md
Note: If you want to develop but are lost with the architecture of the system refer to How_to_develop.md

Changes :- This is the final update necessary for my intended goals of the public release.
1. A lot has changed so bear with me.
2. Functionality changes
 = Removed gnupg encryption because it's use case does not fit intended security
 = Dockerised the program, users can create a docker container using the provided docker file. Size should be around 500-600 MB on disk
 = Added ego's, a ego is a codename which tells the bot class which bot to load and changes prefix commands accordingly. Rest of user interaction is same.
 = Removed manganato.py and added jikan.py which uses the jikan api to query MAL databases. https://docs.api.jikan.moe/
 = Improved error messages, now errors are logged with uuid's so user's can report errors.
 = Improved the usability of paginated embeds, with the error of losing persistence fixed.
3. API changes
 = Completly redone metrics, logging and error handling. Now every function MUST (a suggestion) be wrapped in two provided wrappers or make your own.
  - @general_error_handelr and @music_error_handler are the two wrappers, aside from handling common errors it logs, reports improved messages to user, handles special
    cases (definition upto you), and finally does a performance logging for total function calls, cpu|io|usr time, and first 15 stacks.
 = ego's are handeled through defaults.json file. You must save a prefix for said ego. Eg: "ego" : "patient-bug" needs "prefix_patinet-bug" : "<prefix>" to be defined in the defaults.json
 = Removed old Paginator.py which was a custom handler in favor of dpy-paginator a publicly maintained PyPi package with regular updates, by default it uses the emojis provided
 by the package, but can be changed. default.json has a empty buttons array in order that can be filled like this [left-skip, left, right, right-skip]. Then self.buttons can be provied as a argument
 to the paginate function of dpy-paginator library. Buttons need to be in "<:name:id>" or UNICODE_EMOJI format. Pretty usefull if ya ask me lol.
 = Webserver's index.js now directly calls the static library api instead of a runtime resolution to support cases where localhost is unavailable.
 = Logging is done using cProfile, if not avilable use Profile, the bot by default has it's own profiler under self.profiler that you can use.
 = Dev side has reached my desired level of reproducibility, upgradibility, and readability. I am not going to post further updates this year, at least not on the public release. Hence the bumped version.
 = FFMPEG static is now used. The dockerfile automatically updates the static binary for architecture. By default amd64 binaries are available in the sources and bin folder, i have provided two source
 johnvansickle and mwader's binaries. https://www.johnvansickle.com/ffmpeg/ and https://hub.docker.com/r/mwader/static-ffmpeg/ .

How to run :-
1. Barebones
 = Create a venv or not, i do not care. requirements.txt contains all libraries needed. Check the proper architecture for ffmpeg-static. defaults.json must be set with a ego, prefix and proper token be written to respective token file.
2. Docker
 = Set the ego, prefix, auth_token for your bot. And buid the image. Size should be around 500-600 MB on disk. Port 6900 is to be exposed, no other requirements.

Final Thoughts: Final release for 2024, expect no new updates this year.

Note: The data available in data folder is free to use :)

Note: Hanekawa-san.service is a systemd service file that manages starting of discord bot on boot time

Note: Message replies are hard coded in a speech manner resembling Hanekawa Tsubasa san a side character in the monogatari series and light novels by nisio isin

Note: https://www.youtube.com/watch?v=QmMcE3SZZlY see this video to understand her character

My request: Watch the Monogatari series :) You will experience literary knowledge and a existential crisis at the same time. Source : Trust me bro.
 
 
