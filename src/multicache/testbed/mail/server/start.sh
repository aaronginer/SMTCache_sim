service postfix start

sleep 5

VAR=$(ps aux | grep -v "grep" | grep "postfix" | tr -s ' ' | cut -d' ' -f2)
array=($(echo $VAR | tr ' ' '\n'))

for tgid in "${array[@]}"
do
  taskset -p 0x8 $tgid
done


rm /var/mail/root
