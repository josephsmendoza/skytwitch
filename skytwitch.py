# this is shitty python, don't use this as an example

from dataclasses import dataclass, field
import jsonpickle
import json
import socket
import multiprocessing
import sys


@dataclass
class Config:
    password: str = "https://twitchapps.com/tmi/"
    username: str = "nobody"
    channel: str = "nowhere"
    game: str = "Skyrim"
    givePointTime: int = 0
    defaultCost: int = 0
    ssl: bool = True
    host: str = "irc.chat.twitch.tv"
    port: int = 6697
    users: dict[str, int] = field(default_factory=dict)
    commands: dict[str, int] = field(default_factory=dict)


def print(msg):
    sys.stdout.write(msg)


try:
    config = Config(**json.loads(open("config.json", "r").read()))
except FileNotFoundError:
    config = Config()
    open("config.json", "x").write(
        jsonpickle.encode(config, unpicklable=False, indent=4))
    input("close this program and edit config.json to continue")
    exit()

sock = socket.socket()
if(config.ssl):
    import ssl
    sock = ssl.wrap_socket(sock)

sock.connect((config.host, config.port))


def send(msg):
    msg += '\n'
    if(msg.startswith("pass")):
        print("< pass redacted\n")
    else:
        print("< "+msg)
    sock.send(msg.encode())


send("pass "+config.password)
send("nick "+config.username)
send("join #"+config.channel)

while(True):
    msg = sock.recv(1024).decode()
    if not msg:
        input("connection closed")
        exit()
    print("> "+msg)
    if(msg.startswith("PING")):
        send("PONG"+msg[4:-1])
        continue
    #TODO command processing and ahk python library