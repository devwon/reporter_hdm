#!/bin/bash

# container 시작시 문구 STDOUT으로 노출(docker logs로 노출)
echo container is started!!: `date` > /proc/1/fd/1 2>/proc/1/fd/2

# cron foreground 모드로 시작(default는 background)
cron -f
