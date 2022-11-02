from os import chmod
from time import sleep
from ProcessMappingScanner import scanAllProcessesForMapping

def readgamemode():
    with open('/run/gamemode', 'r') as f:
        return int(f.read())

def readperfmode():
    with open('/sys/devices/platform/faustus/throttle_thermal_policy', 'r') as f:
        return int(f.read())
    
def changeperfmode(mode):
    with open('/sys/devices/platform/faustus/throttle_thermal_policy', 'w') as f:
            f.write(str(mode))

def isonbattery():
    with open('/sys/class/power_supply/BAT1/status') as f:
        if 'Discharging' in f.read():
            return True
        else:
            return False


with open('/run/gamemode', 'w') as f:
    f.write('-1')
chmod('/run/gamemode',0o0777)
while True:
    perfmode = readperfmode()
    gamemode = readgamemode()
    if perfmode != 1 and isonbattery():
        changeperfmode(2)
    elif perfmode != 1 and gamemode == 1:
        changeperfmode(1)
    elif perfmode != 0 and gamemode == -1:
        changeperfmode(0)
    sleep(1)
