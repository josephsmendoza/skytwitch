# SkyTwitch
This program allows twitch chat to send raw console commands into Creation Engine games. Specifically, any message which has a `~` in it will have the remainder of the message sent to the game console.
## Twitch points
This program uses it's own points system, and currently has no integration with the Twitch points system for affiliates and partners. If I do implement that feature, it will not be availible in builds provided by me for free.
## Requirements
[Python](https://www.python.org/downloads/) 3.9+

[pip](https://pip.pypa.io/en/stable/installation/) (should come with python)

[AutoHotKey](https://www.autohotkey.com/)
## Quick Setup
Run the program once to generate a template config file in the same folder as the program, then open that up. [Generate a login token](https://twitchapps.com/tmi/) and paste it inside the quotes next to `"password":`, replacing the url that was there. Replace `nobody` and `nowhere` with your username, all lowercase. If you want to use the points system, set `givePointTime` to the number of seconds a viewer must watch to earn a point, and `defaultCost` to the number of points sending a command should cost. If you're playing a different game, replace `Skyrim` with the window title of the game, for example `Fallout`. It doesn't need to be the full title, the first word will work fine. Then change the help url to a relevant link, for example [www.falloutcheats.com](https://www.falloutcheats.com). Don't include `https://` in the link, since twitch will hide it anyways. Now you can start the program let twitch chat control your console. Make sure to play with a controller so that you don't end up typing into the console when it opens and messing up the commands.
## Commands
All commands start with `~`, but the command can start anywhere in a message, and the rest of the message is taken as the command. There are a few special commands that control the bot instead of the game.

`~help` sends the help link into the chat.

The following commands can only be run by the streamer or moderators.

`~user username {+/-}#` will add the given # of points to the given username. For example, `~user nazeem -1000` would take 1000 points away from nazeem. If a user's points go into the negative, they must earn that many points back to be able to run any commands. You can set this number to something rediculous like `-3000000000` (that's almost 100 years in seconds) to effectively perma-ban someone.

`~cost command string #` will set the cost of the given command string to the given #. You can use a negative number to ban a command. All negative numbers are treated the same, there is no difference between `-1` and `-9999999999`
## Long Setup
The first time the program is run, it will install dependancies with `pip` and create a template config file in the program folder. You must edit this file to include your information and preferences and then restart the program. The entries are in order of importance, meaning you need to edit the top few but should never have to edit the bottom few.

Before starting, you should consider what account you want the bot to log in as. You can use your own account for simplicity, or you can create a new account for the bot. If you use a new account, it's a good idea to make the bot a moderator for your channel so that it's automatically excluded from automod rules. The bot doesn't need any moderator permissions, so if possible a better solution would be to create an exlusion for the bot from your automod.

Once you have the bot account, you can [generate a login token](https://twitchapps.com/tmi/) and set the password to that, including `oath:`. `username` should be set to the bot account username (allways lowercase) and `channel` should be set to your username. If you didn't set up a seperate bot account, these will be the same. `givePointTime` is the time in seconds that viewers earn a single point. Please note that the twitch api used to get viewers will count anyone who is watching your channel, vods included, after they watch for a certain amount of time. I don't know how long it takes for a user to show up in the list, but I suspect it's around 5 minutes. `defaultCost` is used for any command that isn't in the `commands` list. Any command with a negative cost is considered banned, so you could set this to a negative number in order to explicitly allow individual commands instead. `help` is the message that will be sent in chat if someone uses `~help`. The default is a link to a guide with all of Skyrim's console commands. You could change it to anything you like, but the idea is to provide a link to some sort of console command list for the game you're playing.

The following settings shouldn't need to be changed unless Twitch changes their IRC api, or you have an edge case setup. When `ssl` is `true`, communications to the IRC server (twitch) is encrypted. Turning this off is a bad idea, because your password will be sent unencrypted without it, allowing anyone on your network or on the way to the server to see it. Set to `false` to disable encryption. `host` is the name of the server to connect to, and `port` is the port number to connect to on the host. You shouldn't change this unless you already understand what they mean.

The following settings can be set via chat commands, and their syntax in the file is not obvious, so you'll probably want to use the commands to set them. `users` contains a list of all known viewers and their points. `commands` contains the list of commands with set costs.