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
            break
        except ModuleNotFoundError as e:
            import os
            os.system("pip install "+e.name)

    from ahk import AHK
    from dataclasses import dataclass, field
    import jsonpickle
    import json
    import sys

    @dataclass
    class Config:
    games: list[str] = field(default_factory=["Skyrim","Fallout"])

    try:
        config = Config(**json.loads(open("config.json", "r").read()))
        open("config.json", "w").write(
            jsonpickle.encode(config, unpicklable=False, indent=4))
    except FileNotFoundError:
        config = Config()
        open("config.json", "x").write(
            jsonpickle.encode(config, unpicklable=False, indent=4))

    ahk = AHK()
for title in config.games :
    game = ahk.find_window_by_title(title.encode())
    if game:
                    break
            game.activate()
game.activate_bottom()
            ahk.set_capslock_state(False)
            ahk.key_up("shift")
ahk.key_press("~")
ahk.send(" ".join(sys.argv[1:]).replace("~", ""))
            ahk.key_press("enter")
ahk.key_press("~")