try:
    import sys
    class Tee(object):
        def __init__(self, name, mode):
            self.file = open(name, mode)
            self.stdout = sys.stdout
            self.stderr = sys.stderr
            sys.stdout = self
            sys.stderr = self
        def __del__(self):
            sys.stdout = self.stdout
            sys.stderr = self.stderr
            self.file.close()
        def write(self, data):
            self.stdout.write(data)
            self.file.write(data)
            self.file.flush()

    Tee("log.txt","w")

except Exception:
    import traceback
    input(traceback.format_exc())

    while(True):
        try:
            import jsonpickle
            import ahk
            import requests
            break
        except ModuleNotFoundError as e:
            import os
            os.system("pip install "+e.name)

    from ahk import AHK
    from dataclasses import dataclass, field
    import jsonpickle
    import json
    import socket
    import multiprocessing
    import sys
    import requests

    @dataclass
    class Config:
        password: str = "https://twitchapps.com/tmi/"
        username: str = "nobody"
        channel: str = "nowhere"
        givePointTime: int = 0
        defaultCost: int = 0
        game: str = "Skyrim"
        help: str = "www.skyrimcommands.com"
        ssl: bool = True
        host: str = "irc.chat.twitch.tv"
        port: int = 6697
        users: dict[str, int] = field(default_factory=dict)
        commands: dict[str, int] = field(default_factory=dict)
    

    def print(msg):
        sys.stdout.write(msg)


    try:
        config = Config(**json.loads(open("config.json", "r").read()))
        open("config.json", "w").write(
            jsonpickle.encode(config, unpicklable=False, indent=4))
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

    def sendMessage(msg):
        send("privmsg #"+config.channel+" :"+msg)

    send("pass "+config.password)
    send("nick "+config.username)
    send("join #"+config.channel)
    sendMessage("skytwitch online")

    if(config.givePointTime > 0):
        @dataclass
        class Chatters:
            chatters: dict[str, list[str]] = field(default_factory=dict)
            _links: list[str] = field(default_factory=list)
            chatter_count: int = 0

        def givePoints():
            from time import sleep
            while(True):
                print("give point to: ")
                chatters = Chatters(
                    **json.loads(requests.get("http://tmi.twitch.tv/group/user/" + config.channel + "/chatters").text))
                for user in chatters.chatters["viewers"]:
                    print(user+", ")
                    if(user not in config.users):
                        config.users[user] = 1
                    else:
                        config.users[user] += 1
                print('\n')
                open("config.json", "w").write(
                    jsonpickle.encode(config, unpicklable=False, indent=4))
                sleep(config.givePointTime)

        import threading
        threading.Thread(target=givePoints).start()

    ahk = AHK()

    def isMod(user):
        if user == config.channel: return True
        chatters = Chatters(
            **json.loads(requests.get("http://tmi.twitch.tv/group/user/" + config.channel + "/chatters").text))
        return user in chatters.chatters["moderators"]

    class Commands():
        def user(user,cmd): # ~user username {+/-}#
            if not isMod(user): return
            user=cmd[1]
            points=int(cmd[2])
            if(user not in config.users): config.users[user]=0
            config.users[user]+=points
            open("config.json", "w").write(
                jsonpickle.encode(config, unpicklable=False, indent=4))
            sendMessage("gave "+user+" "+str(points)+" points")
        def cost(user,cmd): # ~cost command string #
            if not isMod(user): return
            cost=int(cmd[-1])
            cmd=" ".join(cmd[1:-1])
            config.commands[cmd]=cost
            open("config.json", "w").write(
                jsonpickle.encode(config, unpicklable=False, indent=4))
            sendMessage(cmd+" now costs "+str(cost)+" points")
            if(cost<0): sendMessage("meaning it's banned")
        def help(user,cmd): # ~help
            sendMessage(config.help)
        def cmd(user,cmd): # default
            msg=" ".join(cmd)
            cost = config.defaultCost
            for cmd in config.commands:
                if(msg.startswith(cmd)):
                    cost = config.commands[cmd]
                    break
            if(cost < 0):
                sendMessage(user+" that command is banned")
                return
            if(user not in config.users):
                config.users[user] = 0
            if(config.users[user] < cost):
                sendMessage(
                    user+" has "+str(config.users[user])+" ponts, needs "+str(cost)+" points")
                return
            game = ahk.find_window_by_title(config.game.encode())
            game.activate()
            ahk.set_capslock_state(False)
            ahk.key_up("shift")
            ahk.send("~")
            ahk.send(msg)
            ahk.key_press("enter")
            ahk.send("~")
            if(cost==0): return
            config.users[user]-=cost
            sendMessage(user+" now has "+str(config.users[user])+" points")

    while(True):
        msg = sock.recv(1024).decode()
        if not msg:
            input("connection closed")
            exit()
        print("> "+msg)
        if(msg.startswith("PING")):
            send("PONG"+msg[4:-1])
            continue
        msg=msg.lower()
        index = msg.find('~')
        if(index == -1):
            continue
        user = msg[1:msg.find("!")]
        print(user+":")
        msg = msg[index+1:].split()
        print(" ".join(msg)+"\n")
        try:
            getattr(Commands,msg[0],Commands.cmd)(user,msg)
        except Exception as e:
            import traceback
            print(traceback.format_exc()+"\n")

except Exception:
    import traceback
    input(traceback.format_exc())
