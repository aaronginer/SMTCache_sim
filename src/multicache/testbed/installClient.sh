#!/bin/bash

#requirements
#gcc, autoconf, make, automake, libpopt-dev

apt update
apt-get install dialog msr-tools
git@extgit.iaik.tugraz.at:coresec_students/2021_bachelor_giner_cachesim.git
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
            chmod 700 ./app/client/setup.sh
            ./app/client/setup.sh
            ;;
        2)
            chmod 700 ./db/client/setup.sh
            ./db/client/setup.sh
            ;;
        3)
            chmod 700 ./file/client/setup.sh
            ./file/client/setup.sh
            ;;
        4)
            chmod 700 ./mail/client/setup.sh
            ./mail/client/setup.sh
            ;;
        5)
            chmod 700 ./stream/client/setup.sh
            ./stream/client/setup.sh
            ;;
        6)
            chmod 700 ./web/client/setup.sh
            ./web/client/setup.sh
            ;;
    esac
done
