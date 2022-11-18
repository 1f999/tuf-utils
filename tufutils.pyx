import cython
from time import sleep
from os import system,path,chmod
from ProcessMappingScanner import scanAllProcessesForMapping
from multiprocessing import Process
@cython.cclass
class utils:
    def __init__(self) -> cython.int:
        with open('/sys/devices/platform/faustus/kbbl/kbbl_mode', "w") as f:
            f.write("0")
        with open('/sys/devices/platform/faustus/kbbl/kbbl_speed', "w") as f:
            f.write("0")
        with open('/sys/devices/platform/faustus/kbbl/kbbl_flags', "w") as f:
            f.write("ff")
        with open('/run/nvidiautilization', "w") as f:
            f.write("")
        with open('/run/gamemode', 'w') as f:
            f.write('0')
        chmod('/run/gamemode',0o0777)
        self.main()
    
    @cython.cfunc
    def isonbattery(self) -> cython.bint:
        with open('/sys/class/power_supply/BAT1/status') as f:
            if 'Discharging' in f.read():
                return True
            else:
                return False
    
    @cython.cfunc
    def readbrightness(self,brightnessdev) -> cython.int:
        with open(brightnessdev,'r') as f:
            return int((f.read()))
    
    @cython.cfunc
    def readgpuutilization(self) -> cython.int:
        system('/usr/bin/nvidia-smi -f=/run/nvidiautilization -q -d UTILIZATION,TEMPERATURE,MEMORY')
        with open('/run/nvidiautilization','r') as f:
            return int(f.readlines()[19].strip(' Gpu:%\n'))
    
    @cython.cfunc
    def readgamemode(self) -> cython.int : #temporary solution - !requires setting these lines in /etc/gamemode.ini: start=echo "1" > /run/gamemode 
                        #                                                                         end=echo "0" > /run/gamemode
                        #!todo - develop gamemode controller service
        with open('/run/gamemode', 'r') as f:
            return int(f.read())
    
    @cython.cfunc
    def readthermalthrottlepolicy(self) -> cython.int:
        with open('/sys/devices/platform/faustus/throttle_thermal_policy', 'r') as f:
            return int(f.read())
    
    @cython.cfunc
    def setled(self,color:cython.p_char,value:cython.float,faustusdev:cython.p_char="/sys/devices/platform/faustus/kbbl/kbbl_"):
        with open(faustusdev + color, "w") as f:
            f.write(str(hex(int(value))))
    
    @cython.cfunc
    def commitled(self):
        with open('/sys/devices/platform/faustus/kbbl/kbbl_set', "w") as f:
            f.write("2")
    
    @cython.cfunc  
    def setthermalthrottlepolicy(self,mode:cython.int):
        with open('/sys/devices/platform/faustus/throttle_thermal_policy', 'w') as f:
            f.write(str(mode))
    
    
    @cython.ccall
    def controlkeyboardled(self,lastgpuutilization:cython.float=0.0,is2tick:cython.bint=True,brightnessdev:cython.p_char="",brightnessinit:cython.p_char="",lastcpuidle:cython.float=0.0,lastcputotal:cython.float=0.0):
        while True:
            if brightnessdev == brightnessinit:
                if path.isfile('/sys/class/backlight/amdgpu_bl0/brightness'):
                    brightnessdev = "/sys/class/backlight/amdgpu_bl0/brightness"
                else:
                    brightnessdev = "/sys/class/backlight/amdgpu_bl1/brightness"
            with open('/proc/stat') as f:
                fields:cython.array = [float(column) for column in f.readline().strip().split()[1:]]
            cpuidle:cython.float = fields[3] # calculating cpu utilization 
            cputotal:cython.float = sum(fields) 
            cpuidledelta:cython.float = cpuidle - lastcpuidle
            cputotaldelta:cython.float = cputotal - lastcputotal
            lastcpuidle = cpuidle 
            lastcputotal = cputotal
            cpuutilization:cython.float = 255 * (1.0 - cpuidledelta / cputotaldelta)
            if is2tick:
                gpuutilization:cython.float = 2.55 * self.readgpuutilization()
                lastgpuutilization = gpuutilization
            else:
                gpuutilization:cython.float = lastgpuutilization
            brightnesscoef:cython.float = self.readbrightness(brightnessdev) / 255
            self.setled("red", brightnesscoef * cpuutilization)
            self.setled("green", brightnesscoef * gpuutilization)
            if cpuutilization >= gpuutilization:
                self.setled("blue", brightnesscoef * (255 - cpuutilization) )
            else:
                self.setled("blue", brightnesscoef * (255 - gpuutilization) )
            self.commitled()
            is2tick = not is2tick
            if self.isonbattery():
                sleep(1)
            else:
                sleep(0.1)
    
    @cython.ccall
    def controlthermalthrottle(self):
        while True:
            onbattery:cython.bint=self.isonbattery()
            thermalthrottlepolicy:cython.int = self.readthermalthrottlepolicy()
            if onbattery:
                if thermalthrottlepolicy != 2:
                    self.setthermalthrottlepolicy(2)
                    system("sysctl kernel.sched_tt_balancer_opt=3")
            else:
                gamemode:cython.int = self.readgamemode()
                if gamemode == 1:
                    if thermalthrottlepolicy != 1:
                        self.setthermalthrottlepolicy(1)
                        system("sysctl kernel.sched_tt_balancer_opt=1")
                elif scanAllProcessesForMapping("clang") != {}:
                        self.setthermalthrottlepolicy(1)
                elif thermalthrottlepolicy != 0:
                    self.setthermalthrottlepolicy(0)
                    system("sysctl kernel.sched_tt_balancer_opt=1")
            if self.isonbattery():
                sleep(5)
            else:
                sleep(2.5)
    
    
    @cython.ccall
    def main(self):
        if cython.compiled:
            print("maca paca performance optimized - running compiled")
        else:
            print("performance reduced! runnning interpreted!")
        Process(target=self.controlthermalthrottle).start()
        Process(target=self.controlkeyboardled).start()

