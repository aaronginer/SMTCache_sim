echo "Starting app server setup..."

yes | apt-get install tomcat9 tomcat9-admin tomcat9-docs tomcat9-examples
yes | apt-get install ant
yes | apt-get install cvs

systemctl start tomcat9.service

echo "Finished app server setup"
