#### [Linux only]
## Use Asus TUF Gaming laptop ⌨ backlight as a colorful CPU/GPU utilization indicator with gradients from 🟦 (indicating both idle) to 🟥 (CPU 100% load) and 🟩 (GPU 100% load) 

#### Requires [hackbnw/faustus](https://github.com/hackbnw/faustus) driver to be installed and functioning! If your Asus TUF laptop is unsupported by the driver try building dkms module anyway and put following to your kernel parameters🫠
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
