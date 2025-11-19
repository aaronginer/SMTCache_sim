echo "Starting web server setup..."

yes | apt-get install apache2
service apache2 start

echo "Finished web server setup"