dpkg -i linux-headers-5.13.0+_5.13.0+-3_amd64.deb
dpkg -i linux-image-5.13.0+_5.13.0+-3_amd64.deb
dpkg -i linux-libc-dev_5.13.0+-3_amd64.deb
sed -i 's/GRUB_DEFAULT=[0-9]*/GRUB_DEFAULT="1>2"/g' /etc/default/grub
update-grub
reboot

# https://unix.stackexchange.com/questions/198003/set-default-kernel-in-grub