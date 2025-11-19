echo "Starting mail server setup..."

yes | apt-get install postfix
echo "resolve_numeric_domain = yes" >> /etc/postfix/main.cf
/etc/init.d/postfix start

echo "Finished mail server setup"
