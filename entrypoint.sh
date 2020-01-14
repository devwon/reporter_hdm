#!/bin/bash

# cron 시작
cron
# container 시작시 문구 STDOUT으로 노출(docker logs로 노출)
echo container is started!!: `date` > /proc/1/fd/1 2>/proc/1/fd/2
# container 상태 계속 유지
while : ; do
    sleep 3
done

