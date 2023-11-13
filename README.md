This is the open source public release of Hanekawa-san, my discord bot.

The original code is closed off in a private repo, and is basically my archive

Version : 1.420 Release Date: 14/11/23

Updated from : ver 1.0 Release Date: 1/11/23

Changes : Quite a lot so stick with me ->

1.Completly rewritten reddit.py which can search posts,subreddits and view a random post from a subreddit, soundcloud_music.py -> youtube_music.py
2.Admin web server has been drastically changed, now uses a api end points based backend to return data, home page uses said api to display data
3.Added the ability to play playlists, music provider is changed to youtube_music (ytmusicapi, speed improvements by 1 or 1.5 seconds)
4.Help function is added, contains a whoami and function documentation. Added a documentation autogenration so that any newly written function in cogs get automatically documented (provided you have written the __doc__ string of a function)
5.By default file uploads from bot are done by uploading it to 0x0.st and using that link in embeds. Done to improve speed and upload capability, all fair practises of 0x0.st are done with the expiry_time set to 900 seconds of upload epoch_time. 

external-libraries.txt contains a repo of binaries that will be required

requirements.txt will have all the needed libraries in this code

defaults.json contains default definitions of embeds and other quirks that are used in the program.

How to run:

   1.Save your bot token in the token file in auth folder
   2.Choose a method of encryption, by default it has no encryption
   3.Different types of encryption are defined in utils/decryptor.py
   4.Their usage is explained in a comment in main.py at the last lines

This is not perfect, i intend to make it fully customizable with more options.

Note: The data available in data folder is free to use :)

Note: Hanekawa-san.service is a systemd service file that manages starting of discord bot on boot time

Note: Message replies are hard coded in a speech manner resembling Hanekawa Tsubasa chan a side character in the monogatari series and light novels by nisio isin

Note: https://www.youtube.com/watch?v=QmMcE3SZZlY see this video to understand her character

My request: Watch the Monogatari series :) It looks ecchi but the monolouges and story is very good. Source : Trust me bro.

