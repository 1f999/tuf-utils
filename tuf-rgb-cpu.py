from time import sleep
from os import system

def writered(value):
    with open('/sys/devices/platform/faustus/kbbl/kbbl_red', "w") as f:
        f.write(str(hex(int(value))))

def writegreen(value=0): #static for now
    with open('/sys/devices/platform/faustus/kbbl/kbbl_green', "w") as f:
        f.write(str(hex(int(value))))

def writeblue(value):
    with open('/sys/devices/platform/faustus/kbbl/kbbl_blue', "w") as f:
        f.write(str(hex(int(value))))

def readscreenbrightness():
    with open('/sys/class/backlight/amdgpu_bl1/brightness','r') as f:
        return int((f.read()))

def readgpuutilization():
    with open('/run/nvidiautilization','r') as f:
        return f.readlines()[19]

def commit():
    with open('/sys/devices/platform/faustus/kbbl/kbbl_set', "w") as f:
        f.write("2")


with open('/sys/devices/platform/faustus/kbbl/kbbl_mode', "w") as f:
    f.write("0")
with open('/sys/devices/platform/faustus/kbbl/kbbl_speed', "w") as f:
    f.write("0")
with open('/sys/devices/platform/faustus/kbbl/kbbl_flags', "w") as f:
    f.write("ff")
lastidle = lasttotal = 0
with open('/run/nvidiautilization', "w") as f:
    f.write("")


while True:
    system('/usr/bin/nvidia-smi -f=/run/nvidiautilization -q -d UTILIZATION,TEMPERATURE,MEMORY')
    gpuutilization = 2.55 * int(readgpuutilization().strip(' Gpu:%\n'))
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idledelta, totaldelta = idle - lastidle, total - lasttotal
    lastidle, lasttotal = idle, total
    cpuutilization = 255 * (1.0 - idledelta / totaldelta)
    screenbrightnesscoef = readscreenbrightness() / 255
    writered(screenbrightnesscoef * cpuutilization)
    writegreen(screenbrightnesscoef * gpuutilization)
    if cpuutilization >= gpuutilization:
        writeblue(screenbrightnesscoef * (255 - cpuutilization))
    else:
        writeblue(screenbrightnesscoef * (255 - gpuutilization))
    commit()
    sleep(0.1)
