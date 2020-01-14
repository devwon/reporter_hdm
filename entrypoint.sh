#!/bin/bash

# cron 시작
cron
# container 시작 문구
echo container is started!!: `date` > /proc/1/fd/1 2>/proc/1/fd/2
# container 상태 계속 유지
while : ; do
    sleep 3
done

