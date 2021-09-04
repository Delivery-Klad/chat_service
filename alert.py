import subprocess
from pathlib import Path

startup = subprocess.STARTUPINFO()
startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW

path = str(Path.home()) + "/AppData/Roaming/CorporationChat/alert/alert.mp3"
subprocess.call(["ffplay", "-nodisp", "-autoexit", path], startupinfo=startup)
