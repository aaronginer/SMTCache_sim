# file source: https://github.com/tianweiz07/Benchmarks/tree/master/PALMScloud/Video

echo "Starting streaming server setup..."

#install gcc
#install yasm
#install make
#unzip tarball
#./configure
#make -j
#cpy config file to /etc
#cpy video and sound file to /home
#sudo ./ffserver

## place binary and config file
cp stream/server/bin/ffserver /usr/bin
cp stream/server/ffserver.conf /etc/

## create default data location
mkdir /home/stream
cp stream/server/test1.mkv /home/stream
cp stream/server/test2.mp3 /home/stream
cp stream/server/test3.mp4 /home/stream

## create service and enable / start it
cp stream/server/ffserver.service /lib/systemd/system
systemctl daemon-reload
systemctl enable ffserver
service ffserver start

echo "Finished streaming server setup"
