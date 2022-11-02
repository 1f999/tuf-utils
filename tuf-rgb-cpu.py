from time import sleep


def writered(value):
    with open('/sys/devices/platform/faustus/kbbl/kbbl_red', "w") as f:
        f.write(str(hex(int(value))))

def writegreen(value=0): #static for now
    with open('/sys/devices/platform/faustus/kbbl/kbbl_green', "w") as f:
        f.write(str(value))

def writeblue(value):
    with open('/sys/devices/platform/faustus/kbbl/kbbl_blue', "w") as f:
        f.write(str(hex(int(value))))

def readscreenbrightness():
    with open('/sys/class/backlight/amdgpu_bl0/brightness','r') as f:
        return int((f.read()))

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


while True:
    with open('/proc/stat') as cpu:
        fields = [float(column) for column in cpu.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idledelta, totaldelta = idle - lastidle, total - lasttotal
    lastidle, lasttotal = idle, total
    utilisation = 255 * (1.0 - idledelta / totaldelta)
    screenbrightnesscoef = readscreenbrightness() / 255
    writered(screenbrightnesscoef * utilisation)
    writeblue(screenbrightnesscoef * (255 - utilisation))
    commit()
    sleep(0.1)
