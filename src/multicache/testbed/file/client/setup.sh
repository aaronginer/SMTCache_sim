# https://kongll.github.io/2015/04/24/dbench/
# https://zoomadmin.com/HowToInstall/UbuntuPackage/libsmbclient

# loadfiles:
# https://dbench.samba.org/web/smb-loadfiles.html

echo "Starting file client setup..."

#apt-get install gcc make libsmbclient libsmbclient-dev libpopt-dev autoconf
#git clone git://git.samba.org/sahlberg/dbench.git dbench
#cd dbench
#./autogen.sh
# manually fix include paths for libsmbclient.h /usr/include/... in both configure and smb.c
# the standard include does not work for some reason, try to fix later
# this is not ideal!
#sed -i "s/<libsmbclient.h>/\"\/usr\/include\/samba-4.0\/libsmbclient.h\"/g" smb.c
#sed -i "s/<libsmbclient.h>/\"\/usr\/include\/samba-4.0\/libsmbclient.h\"/g" configure
#./configure
#add stdint.h include to libnfs.c
#sed -i '/<fcntl.h>/a #include "stdint.h"' libnfs.c

#make -j

apt-get install libsmbclient-dev

cp file/client/dbench_bin /usr/bin/dbench


#NOTE: loadfiles need newline at end of file!

echo "Finished file client setup"
