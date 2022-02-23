#### [Linux only]
## Make your Asus TUF Gaming laptop keyboard backlight reflect CPU utilization with cool gradient effect from blue to red! 

Requires [hackbnw/faustus](https://github.com/hackbnw/faustus) to be installed and functioning!

### Installation
cd /tmp  
git clone https://github.com/digitalmadness/tuf-rgb-cpu/  
cd tuf-rgb-cpu  
sudo cp tuf-rgb-cpu.py /usr/local/share  
sudo cp tuf-rgb-cpu.service /etc/systemd/system  

### Usage
sudo systemctl start tuf-rgb-cpu.service  
sudo systemctl stop tuf-rgb-cpu.service  

### Autostart
sudo systemctl enable tuf-rgb-cpu.service  

### Removing from autostart
sudo systemctl disable tuf-rgb-cpu.service  
