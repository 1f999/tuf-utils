from os import chmod
from time import sleep
from configparser import ConfigParser as config

def readgamemode():
    with open('/run/gamemode', 'r') as gamemode:
        return int(gamemode.read())

def gamemodeon():
    with open('/sys/devices/platform/faustus/throttle_thermal_policy', 'w') as throttlepolicy:
            throttlepolicy.write('1')
    with open('/run/gamemode', 'w') as gamemode:
        gamemode.write('1')

def gamemodeoff():
    with open('/sys/devices/platform/faustus/throttle_thermal_policy', 'w') as throttlepolicy:
        throttlepolicy.write('0')
    with open('/run/gamemode', 'w') as gamemode:
        gamemode.write('0')


gamemodeoff()
chmod('/run/gamemode',0o0777)

while True:
    isgamemode = readgamemode()
    if isgamemode == 1:
        gamemodeon()
    elif isgamemode == -1:
        gamemodeoff()
    sleep(1)
