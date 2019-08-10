#! /bin/sh

SERVER=10.53.53.53
ZONE="example.com"

name="${1}"
record_data="${2}"

nsupdate <<EOF
server ${SERVER}
zone ${ZONE}
update add ${name} 300 IN TXT ${record_data}
send
EOF
