#### [Linux only]
## some useful tools for your Asus Tuf laptop

### use keyboard⌨ backlight as an CPU/GPU load indicator with gradients from 🟦 (indicating both idle) to 🟥 (CPU 100% load) and 🟩 (GPU 100% load)

### activate powersave thermal throttle mode based on if running on battery🔋 or boost mode if 🎮 [FeralInteractive/gamemode](https://github.com/FeralInteractive/gamemode) is activated and running on charger🔌

#### Requires [hackbnw/faustus](https://github.com/hackbnw/faustus) driver to be installed and functioning! If your Asus TUF laptop is unsupported by the driver try building dkms module anyway and put following to your kernel parameters🫠, worked for me!
```
faustus.let_it_burn=1
```

### 🔨installation🔧
```
git clone https://github.com/digitaimadness/tuf-utils /tmp/tuf-utils
cd /tmp/tuf-utils  
python setup.py build_ext --inplace
sudo mkdir /opt/tuf-utils
sudo mv tufutils.pyx tufutilsstarter.py tufutils.cpython-310-x86_64-linux-gnu.so /opt/tuf-utils
sudo mv tuf-rgb-cpu.service /etc/systemd/system

```
### ✨usage✨
```
sudo systemctl start tuf-rgb-cpu.service  
sudo systemctl stop tuf-rgb-cpu.service  
```

### 🌄autostart🌄
```
sudo systemctl enable tuf-rgb-cpu.service  
```
