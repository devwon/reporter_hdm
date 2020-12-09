FROM python:3.7.2

MAINTAINER HAKDOKMAN

# 기본 셋팅
ENV APP_HOME /reporter_hdm 
ENV PYTHONIOENCODING UTF-8
# set display port to avoid crash
ENV DISPLAY=:99

# apt 업그레이드
RUN apt update && apt install -y gnupg wget curl apt-utils
# google chrome key 다운로드 후 이 key를 키링에 추가하여 패키지 관리자가 Chrome deb의 무결성 확인 가능
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# chrome, crontab 설치
RUN apt update && apt install -y google-chrome-stable cron

# chromedriver 설치
RUN apt install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin

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

# cron pam 설정 변경 - pam_loginuid.so 주석 처리 inside /etc/pam.d/cron
RUN sed -i '/session    required     pam_loginuid.so/c\#session    required   pam_loginuid.so' /etc/pam.d/cron

# 컨테이너 작동 확인 & cron 실행하는 shell 파일 호출
ENTRYPOINT ["/reporter_hdm/entrypoint.sh"]
