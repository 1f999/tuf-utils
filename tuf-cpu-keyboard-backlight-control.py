from time import sleep

with open('/sys/devices/platform/faustus/kbbl/kbbl_green', "w") as green:
    green.write("00")
with open('/sys/devices/platform/faustus/kbbl/kbbl_mode', "w") as mode:
    mode.write("0")
with open('/sys/devices/platform/faustus/kbbl/kbbl_speed', "w") as speed:
    speed.write("0")
with open('/sys/devices/platform/faustus/kbbl/kbbl_flags', "w") as flags:
    flags.write("ff")
last_idle = last_total = 0

while True:
    with open('/proc/stat') as cpu:
        fields = [float(column) for column in cpu.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    utilisation = 255 * (1.0 - idle_delta / total_delta)
    with open('/sys/devices/platform/faustus/kbbl/kbbl_red', "w") as red:
        red.write(str(hex(int((utilisation)))))
    with open('/sys/devices/platform/faustus/kbbl/kbbl_blue', "w") as blue:
        blue.write(str(hex(int((255 - utilisation)))))
    with open('/sys/devices/platform/faustus/kbbl/kbbl_set', "w") as commit:
        commit.write("2")
    sleep(0.1)