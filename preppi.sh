#!/bin/bash

raspi-config nonint do_memory_16
systemctl disable bluetooth.service
systemctl disable hciuart.service
apt-get update && apt-get -y upgrade

ln /opt/dupl/dupl.service /lib/systemd/system/dupl.service
ln /opt/dupl/firstboot.service /lib/systemd/system/firstboot.service
ln /opt/dupl/config.ini /home/pi/kiosk.ini
systemctl enable firstboot.service

sed -i '/^# Additional overlays.*/a dtoverlay=pi3-disable-wifi\ndtoverlay=pi3-disable-bt' /boot/config.txt
apt-get --yes install libcups2-dev cups cups-bsd

addgroup watchdog
usermod -a -G watchdog pi
apt-get --yes install python3-pip

#apt-get --yes --allow-downgrades --allow-remove-essential --allow-change-held-packages install python3-pip
echo 'KERNEL=="watchdog", MODE="0660", GROUP="watchdog"' > /etc/udev/rules.d/60-watchdog.rules
sed -i '/^#NTP=.*/a FallbackNTP=laiks.egl.local' /etc/systemd/timesyncd.conf
chattr -i /etc/hosts
echo '10.100.20.104   laiks.egl.local' >> /etc/hosts
chattr +i /etc/hosts

#/usr/sbin/shutdown -r now
