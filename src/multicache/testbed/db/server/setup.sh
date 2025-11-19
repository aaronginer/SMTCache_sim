echo "Starting database server setup..."

USERNAME="mysql_test_user"
PASSWORD="mysql_test_pw"
DATABASE="mysql_test_db"

#install mysql server

yes | apt install mysql-server
service mysql start

# create user and database

mysql -e "CREATE USER '$USERNAME'@localhost IDENTIFIED BY '$PASSWORD';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO $USERNAME@localhost;"
mysql -e "CREATE USER '$USERNAME'@'%' IDENTIFIED BY '$PASSWORD';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO '$USERNAME'@'%';"
mysql -e "FLUSH PRIVILEGES"
mysql -e "CREATE DATABASE $DATABASE;"

#change bind-addr @ /etc/mysql/mysql.conf.d/mysqld.conf to 0.0.0.0
# this way its possible to connect to the database from the outside

sed -i -E 's/bind-address(\t){2}=\s([0-9])+(.[0-9])+/bind-address\t\t= 0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf
echo 'skip-name-resolve' >> /etc/mysql/mysql.conf.d/mysqld.cnf
# sudo mysql -e "SET GLOBAL max_connections = 2000;"

service mysql restart

echo "Finished database server setup"
