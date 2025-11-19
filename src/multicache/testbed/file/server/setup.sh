
#https://ieeexplore.ieee.org/ielaam/10208/7951066/7530858-aam.pdf
#https://ubuntu.com/tutorials/install-and-configure-samba#1-overview

echo "Starting file server setup..."

username=${SUDO_USER:-${USER}}
# follow this guide -> also sudo -R 777 sambashare folder for user access
yes | apt-get install samba
mkdir /home/$username/sambashare
sudo chmod -R 777 /home/$username/sambashare

cp file/server/config.txt file/server/config_temp.x

sed -i "s/#USER#/${username}/g" file/server/config_temp.x

cat file/server/config_temp.x >> /etc/samba/smb.conf

sudo service smbd restart
sudo ufw allow samba

sudo smbpasswd -a $username
# enter pw

echo "Finished file server setup"
