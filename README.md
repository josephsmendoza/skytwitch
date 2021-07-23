# SkyTwitch
This program allows twitch chat to send raw console commands into Skyrim Special Edition. Specifically, any message which has a `~` in it will have the remainder of the message sent to the skyrim console.
## WIP
This program is in its early stages, and is not production ready. Features required before release 1.0.0, in order of priority, include:
- SSL support
- Command filtering
- User filtering
- Points system
## Usage
`skytwitch oath:token botuser channelname`

The bot will print out everything it receives from twitch on `stdout`. If you only want to know when something goes wrong, then ready only `stderr`.