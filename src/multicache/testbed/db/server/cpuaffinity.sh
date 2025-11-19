FOLDER="/lib/systemd/system/"
SERVICE="mysql"
aff_cnt=$(cat ${FOLDER}${SERVICE}.service | grep "CPUAffinity" | wc -l)

if [ "$aff_cnt" -eq "0" ]; then
    sed -i "s/\[Service\]/\[Service\]\nCPUAffinity=$1/g" ${FOLDER}${SERVICE}.service
else
    sed -i "s/$(cat ${FOLDER}${SERVICE}.service | grep "CPUAffinity=")/CPUAffinity=$1/g" ${FOLDER}${SERVICE}.service
fi

systemctl daemon-reload
service $SERVICE restart