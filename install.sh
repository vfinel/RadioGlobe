#! /usr/bin/sh
# Install all dependencies and setup radioglobe service to run under default user
sudo apt install vlc pulseaudio python3-pip python3-smbus python3-dev python3-rpi-lgpio
pip3 install https://github.com/pl31/python-liquidcrystal_i2c/archive/master.zip
pip3 install python-vlc
pip3 install spidev
pip install librosa 
pip install pandas

# autorize execution of utility scripts 
sudo chmod +x poweroff_globe.sh  reboot_globe.sh  restart_main.sh 

# Set paths according to username
sed -i "s/USER/${USER}/g" services/*.service
sudo cp services/*.service /etc/systemd/system
nano
