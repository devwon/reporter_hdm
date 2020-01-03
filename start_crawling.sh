#!/bin/bash
source ~/reporter_hdm/venv/bin/activate    #botvenv 가상환경실행
export SLACK_BOT_TOKEN="xoxb-325351176550-888847745232-ahkVBaVUVO2kyKSCBRL25kPU"  # 토큰
export BOT_ID='US4QXMX6U'   #BOT ID
curl -sS https://hakdokman.slack.com/api/auth.test\?token\=\{$SLACK_BOT_TOKEN\}    #api 서버와 통신
python3 ~/reporter_hdm/news_crawling.py   #python 크롤링 파일 실행

