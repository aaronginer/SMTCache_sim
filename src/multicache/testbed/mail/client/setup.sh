echo "Starting mail client setup..."

apt-get install postfix
echo "resolve_numeric_domain = yes" >> /etc/postfix/main.cf
/etc/init.d/postfix start

echo "Finished mail client setup"