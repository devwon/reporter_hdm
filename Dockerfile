FROM python:3.7.2

MAINTAINER HAKDOKMAN

# 홈 디렉토리
ENV APP_HOME /reporter_hdm 

# apt-get 업그레이드 & crontab 설치
RUN apt-get update && apt-get -y install cron

# python venv 실행
#RUN python3 -m venv botvenv

# pip 업그레이드
RUN pip install --upgrade pip

# 현재 디렉토리 전체 복사
COPY ./ $APP_HOME

# 경로 잡아주기
WORKDIR $APP_HOME

# requirements 설치
RUN pip install -r requirements.txt

# 크론탭 설정&실행(매일 오후 11시59분)
#RUN (crontab -l ; echo "* * * * * /reporter_hdm/start_crawling.sh >> /reporter_hdm/reporter_hdm.log 2>&1") | crontab
RUN (crontab -l ; echo "59 23 * * * /reporter_hdm/start_crawling.sh >> /reporter_hdm/reporter_hdm.log 2>&1") | crontab

ENTRYPOINT cron start $$ tail -f /reporter_hdm/reporter_hdm.log
