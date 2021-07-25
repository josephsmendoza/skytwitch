# SkyTwitch
This program allows twitch chat to send raw console commands into Skyrim Special Edition. Specifically, any message which has a `~` in it will have the remainder of the message sent to the skyrim console.
## WIP
This program is in its early stages, and is not production ready. Features required before release 1.0.0, in order of priority, include:
- SSL support
- ~~Command filtering~~
- ~~User filtering~~
- ~~Points system~~
- Moderation commands
- Error logging
## Twitch points
This program uses it's own points system, and currently has no integration with the Twitch points system for affiliates and partners. If I do implement that feature, it will not be availible in builds provided by me for free.
## Usage
The first time the program is run, it will create a template config file in the program folder. You must edit this file to include your information and preferences and then restart the program.

The bot will print out everything it receives from twitch and all points it assigns on `stdout`.