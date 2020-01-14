#!/bin/bash

#path 지정
export DIR_NAME=`dirname "$0"`
export DIR_HOME=`cd $DIR_NAME; cd ..; pwd`

echo 'dir home: '$DIR_HOME
echo 'dir name: '$DIR_NAME

#source $DIR_HOME/reporter_hdm/botvenv/bin/activate    #botvenv 가상환경실행
export SLACK_BOT_TOKEN="xoxb-325351176550-888847745232-ahkVBaVUVO2kyKSCBRL25kPU"  # 토큰
export BOT_ID='US4QXMX6U'   #BOT ID
curl -sS https://hakdokman.slack.com/api/auth.test\?token\=\{$SLACK_BOT_TOKEN\}    #api 서버와 통신
#python3 $DIR_HOME/reporter_hdm/news_crawling.py   #python 크롤링 파일 실행
python3 $DIR_NAME/news_crawling.py   #python 크롤링 파일 실행
