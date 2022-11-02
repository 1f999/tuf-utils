#### [Linux only]
## Use Asus TUF Gaming laptop keyboard backlight as a CPU/GPU utilization indicator with cool gradient effect from blue(both 0%) to red(CPU 100%) and green(GPU 100%)

#### Requires [hackbnw/faustus](https://github.com/hackbnw/faustus) driver to be installed and functioning! If your Asus TUF laptop is unsupported by the driver try building dkms module anyway and put following to your kernel parameters:
```
faustus.let_it_burn=1
```

### Installation
```
cd /tmp  
git clone https://github.com/digitalmadness/tuf-rgb-cpu/  
cd tuf-rgb-cpu  
sudo cp tuf-rgb-cpu.py /usr/local/share  
sudo cp tuf-rgb-cpu.service /etc/systemd/system  
```
### Usage
```
sudo systemctl start tuf-rgb-cpu.service  
sudo systemctl stop tuf-rgb-cpu.service  
```

### Autostart
```
sudo systemctl enable tuf-rgb-cpu.service  
```
