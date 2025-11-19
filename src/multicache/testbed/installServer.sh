#!/bin/bash
apt update
apt upgrade
apt-get install dialog openssh-server libdw1

cp servers.sh /usr/bin
cp trace.sh /usr/bin
cp pmc_setup.sh /usr/bin

cmd=(dialog --separate-output --checklist "Select options:" 22 76 16)
options=(1 "App" off    # any option can be set to default to "on"
         2 "Database" off
         3 "File" off
         4 "Mail" off
         5 "Stream" off
         6 "Web" off)
choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
clear
for choice in $choices
do
    case $choice in
        1)
            chmod 700 ./app/server/setup.sh
            ./app/server/setup.sh
            ;;
        2)
            chmod 700 ./db/server/setup.sh
            ./db/server/setup.sh
            ;;
        3)
            chmod 700 ./file/server/setup.sh
            ./file/server/setup.sh
            ;;
        4)
            chmod 700 ./mail/server/setup.sh
            ./mail/server/setup.sh
            ;;
        5)
            chmod 700 ./stream/server/setup.sh
            ./stream/server/setup.sh
            ;;
        6)
            chmod 700 ./web/server/setup.sh
            ./web/server/setup.sh
            ;;
    esac
done

sed -i 's/#SystemMaxUse=/SystemMaxUse=50M/g' /etc/systemd/journald.cnf
systemctl restart systemd-journald
