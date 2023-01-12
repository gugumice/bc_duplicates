#!/bin/bash

raspi-config nonint do_memory_16
systemctl disable bluetooth.service
systemctl disable hciuart.service
apt-get update && apt-get -y upgrade

ln /opt/dupl/dupl.service /lib/systemd/system/dupl.service
ln /opt/dupl/firstboot.service /lib/systemd/system/firstboot.service
ln /opt/dupl/config.ini /home/pi/config.ini
systemctl enable firstboot.service

sed -i '/^# Additional overlays.*/a dtoverlay=pi3-disable-wifi\ndtoverlay=pi3-disable-bt' /boot/config.txt

addgroup watchdog
usermod -a -G watchdog pi
apt-get --yes install python3-pip
pip3 --no-input install pyserial
#apt-get --yes --allow-downgrades --allow-remove-essential --allow-change-held-packages install python3-pip
echo 'KERNEL=="watchdog", MODE="0660", GROUP="watchdog"' > /etc/udev/rules.d/60-watchdog.rules
sed -i '/^#NTP=.*/a FallbackNTP=laiks.egl.local' /etc/systemd/timesyncd.conf
chattr -i /etc/hosts
echo '10.100.20.104   laiks.egl.local' >> /etc/hosts
chattr +i /etc/hosts
#Get sound effects
wget https://www.freespecialeffects.co.uk/soundfx/computers/pop3.wav
wget https://www.freespecialeffects.co.uk/soundfx/bleep_02.wav
wget https://www.freespecialeffects.co.uk/soundfx/glass/glassbreak_2.wav
chown pi:pi *.*
#/usr/sbin/shutdown -r now
