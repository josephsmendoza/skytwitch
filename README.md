# SkyTwitch
This program allows you to send raw console commands into Creation Engine games. Specifically, all args passed to this program will be stripped of any `~` and typed into the game console window.
## Requirements
[AutoHotKey](https://www.autohotkey.com/)
## Building/Running from Source
Python 3.9+ and AutoHotKey are currently the only requirements. Eventually I hope to remove AutoHotKey so that this program can run on multiple operating systems, but for now that means Windows. The file [build.cmd](https://github.com/josephsmendoza/skytwitch/blob/master/build.cmd) is the script used to set up the build environment and then build the file on the releases page, or you could use [skytwitch.py](https://github.com/josephsmendoza/skytwitch/blob/master/skytwitch.py) directly for a much smaller program size.