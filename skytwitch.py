try:
    import pip
    pip.main(['install','ahk','elevate','dataclasses','jsonpickle'])
except Exception:
    from traceback import print_exc
    print('An exception occured during dependancy checks')
    print_exc()
    print('please ensure ahk and elevate are installed')

from elevate import elevate
elevate()

import tee
tee.Tee("skytwitch.log", "w")

from time import sleep
from ahk import AHK
from dataclasses import dataclass, field
import jsonpickle
import json
import sys
import time

@dataclass
class Config:
    games: list[str] = field(default_factory=["Skyrim","Fallout"])

try:
    config = Config(**json.loads(open("skytwitch.json", "r").read()))
    open("skytwitch.json", "w").write(
        jsonpickle.encode(config, unpicklable=False, indent=4))
except FileNotFoundError:
    config = Config()
    open("skytwitch.json", "x").write(
        jsonpickle.encode(config, unpicklable=False, indent=4))

open('skytwitch.txt','w').close()
ahk = AHK()
print('SkyTwitch ready')
while True:
    command=''
    with open('skytwitch.txt','r+') as file:
        command=file.read().replace('~', '')
        file.seek(0)
        file.truncate()
    if not command:
        sleep(1)
        continue
    print(command)
    for title in config.games :
        game = ahk.find_window_by_title(title.encode())
        if game:
            break
    pre=ahk.get_active_window()
    game.activate()
    game.activate_bottom()
    ahk.set_capslock_state("off")
    ahk.key_up("shift")
    script_text='blockinput on\nsendinput ``\nsleep 100\nsendraw '+command+'\nsleep 100\nsendinput {enter}\nsleep 100\nsendinput ``'
    ahk.run_script(script_text)
    pre.activate()
    pre.activate_bottom()
    