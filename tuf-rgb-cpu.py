from time import sleep
from os import system,path,chmod
from ProcessMappingScanner import scanAllProcessesForMapping
from multiprocessing import Process,set_start_method

def initled():
    if path.isfile('/sys/class/backlight/amdgpu_bl0/brightness'):
        brightnessdev = "0"
    else:
        brightnessdev = "1"
    with open('/sys/devices/platform/faustus/kbbl/kbbl_mode', "w") as f:
        f.write("0")
    with open('/sys/devices/platform/faustus/kbbl/kbbl_speed', "w") as f:
        f.write("0")
    with open('/sys/devices/platform/faustus/kbbl/kbbl_flags', "w") as f:
        f.write("ff")
    with open('/run/nvidiautilization', "w") as f:
        f.write("")
    return brightnessdev

def initgamemode():
    with open('/run/gamemode', 'w') as f:
        f.write('0')
    chmod('/run/gamemode',0o0777)

def isonbattery():
    with open('/sys/class/power_supply/BAT1/status') as f:
        if 'Discharging' in f.read():
            return True
        else:
            return False

def readbrightness(dev):
    with open(dev,'r') as f:
        return int((f.read()))

def readgpuutilization():
    system('/usr/bin/nvidia-smi -f=/run/nvidiautilization -q -d UTILIZATION,TEMPERATURE,MEMORY')
    with open('/run/nvidiautilization','r') as f:
        return f.readlines()[19]

def readgamemode(): #temporary solution - !requires setting these lines in /etc/gamemode.ini: start=echo "1" > /run/gamemode 
                    #                                                                         end=echo "0" > /run/gamemode
                    #!todo - develop gamemode controller service
    with open('/run/gamemode', 'r') as f:
        return int(f.read())

def readthermalthrottlepolicy():
    with open('/sys/devices/platform/faustus/throttle_thermal_policy', 'r') as f:
        return int(f.read())

def setled(color,value):
    with open('/sys/devices/platform/faustus/kbbl/kbbl_' + color, "w") as f:
        f.write(str(hex(int(value))))

def commitled():
    with open('/sys/devices/platform/faustus/kbbl/kbbl_set', "w") as f:
        f.write("2")
    
def setthermalthrottlepolicy(mode):
    with open('/sys/devices/platform/faustus/thermalthrottle_thermal_policy', 'w') as f:
            f.write(str(mode))


def controlkeyboardled(brightnessdev,lastidle=0,lasttotal=0,lastgpuutilization=0,is2tick=False):
    while True:
        with open('/proc/stat') as f:
            fields = [float(column) for column in f.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields) # calculating cpu utilization
        idledelta, totaldelta = idle - lastidle, total - lasttotal
        lastidle, lasttotal = idle, total
        cpuutilization = 255 * (1.0 - idledelta / totaldelta)
        if is2tick:
            gpuutilization = 2.55 * int(readgpuutilization().strip(' Gpu:%\n'))
        else:
            gpuutilization = lastgpuutilization
        brightnesscoef = readbrightness('/sys/class/backlight/amdgpu_bl' + brightnessdev + '/brightness') / 255
        setled("red", brightnesscoef * cpuutilization)
        setled("green", brightnesscoef * gpuutilization)
        if cpuutilization >= gpuutilization:
            setled("blue", brightnesscoef * (255 - cpuutilization) )
        else:
            setled("blue", brightnesscoef * (255 - gpuutilization) )
        commitled()
        is2tick = not is2tick
        if isonbattery():
            sleep(1)
        else:
            sleep(0.1)

def controlthermalthrottle():
    while True:
        thermalthrottlepolicy = readthermalthrottlepolicy()
        if thermalthrottlepolicy != 2 and isonbattery():
            setthermalthrottlepolicy(2)
        else:
            gamemode = readgamemode()
            if thermalthrottlepolicy != 1 and gamemode == 1:
                setthermalthrottlepolicy(1)
            else:
                if scanAllProcessesForMapping("clang") != {}:
                    setthermalthrottlepolicy(1)
                elif thermalthrottlepolicy != 0 and gamemode == 0:
                    setthermalthrottlepolicy(0)
    if isonbattery():
        sleep(5)
    else:
        sleep(2.5)


if __name__ == "__main__":
    initgamemode()
    brightnessdev = initled()
    #set_start_method("forkserver")
    thermalthrottleprocess = Process(target=controlthermalthrottle)
    keyboardledprocess = Process(target=controlkeyboardled, args=(brightnessdev))
    thermalthrottleprocess.start()
    keyboardledprocess.start()
