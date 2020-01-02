#!/bin/bash
source ~/reporter_hdm/botvenv/bin/activate
curl https://hakdokman.slack.com/api/auth.test\?token\=xoxb-325351176550-888847745232-ahkVBaVUVO2kyKSCBRL25kPU
export SLACK_BOT_TOKEN="xoxb-325351176550-888847745232-ahkVBaVUVO2kyKSCBRL25kPU"
export BOT_ID='US4QXMX6U'
python3 ~/reporter_hdm/news_crawling.py >> ~/reporter_hdm/crontab_log2.txt 2>&1