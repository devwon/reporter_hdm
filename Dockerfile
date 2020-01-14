FROM python:3.7.2

MAINTAINER HAKDOKMAN

# 기본 셋팅
ENV APP_HOME /reporter_hdm 
ENV PYTHONIOENCODING UTF-8

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

# Timezone Asia/Seoul로 설정
RUN echo "Asia/Seoul" > /etc/timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# 크론탭 설정&실행(매일 오후 11시59분)
RUN (crontab -l ; echo "59 23 * * * $APP_HOME/start_crawling.sh > /proc/1/fd/1 2>/proc/1/fd/2") | crontab -

# 파일 권한 +x 설정
RUN chmod +x $APP_HOME/entrypoint.sh

# 컨테이너 작동 확인 & cron 실행하는 shell 파일 호출
ENTRYPOINT ["/reporter_hdm/entrypoint.sh"]
