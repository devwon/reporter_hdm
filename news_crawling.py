# hakdokman news web crawler 만들기
import os
import time
import sys
import logging
# 모듈 import하기 전에 pip 모듈 install된 경로 지정(하드코딩)
sys.path.append('/usr/local/lib/python3.7/site-packages/')
from slackclient import SlackClient

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict  # 순서가 있는 OrderedDict 불러오기
from datetime import datetime


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "뉴스"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

form = '<{link}|{title}>'
error_config = {
    'username': '학독만 뉴스봇',
    'channel': '#newsbot_hdm',  # 기사 업로드할 채널명
    'text': 'error',  # 에러 메시지 노출
}

# logging 관련 셋팅
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG
                    )


# hakdokman news web crawler
# 당일 날짜의 학독만 관련 뉴스 링크를 크롤링해서 가져온다.
def news_crawler():
    url = 'https://search.naver.com/search.naver'
    post_dict = OrderedDict()
    today = datetime.today().strftime("%Y.%m.%d")  # YYYY.mm.dd 형태의 시간 출력

    params = {
        # 'query': '%22%ED%95%99%EC%83%9D%EB%8F%85%EB%A6%BD%EB%A7%8C%EC%84%B8%22-%ED%95%99%EC%83%9D%EB%8F%85%EB%A6%BD%EB%A7%8C%EC%84%B8%EC%9A%B4%EB%8F%99',
        'query': '"학생독립만세"-학생독립만세운동',   #검색어: '학생독립만세'('학생독립만세운동'은 제외)
        'where': 'news',    # 뉴스 카테고리 검색
        'sm': 'tab_opt',    # 옵션으로 검색
        # 'sm': 'tab_pge', # pagination 사용시 주석 풀기
        # 'start': '22', # pagination 사용시 주석 풀기
        'sort': '1',    # 옵션 - 최신순 정렬
        'pd': '3',  # 옵션 - 기간 직접입력
        'ds': today,  # 오늘 날짜
        'de': today,  # 오늘 날짜
    }

    # 오늘자 네이버 뉴스 '학생독립만세'('학생독립만세운동'은 제외) 검색요청 객체 생성
    res = requests.get(url, params=params)
    # full url 예시는 아래와 같다
    # https://search.naver.com/search.naver?where=news&query=%22%ED%95%99%EC%83%9D%EB%8F%85%EB%A6%BD%EB%A7%8C%EC%84%B8%22-%ED%95%99%EC%83%9D%EB%8F%85%EB%A6%BD%EB%A7%8C%EC%84%B8%EC%9A%B4%EB%8F%99&sm=tab_opt&sort=1&pd=3&ds=2019.12.27&de=2019.12.27

    # 검색 후 소스코드 추출
    html = res.text

    # html -> python object
    soup = BeautifulSoup(html, 'html.parser')

    # 태그에서 제목과 링크주소 추출
    sp_tags = soup.select('._sp_each_title')

    if sp_tags:

        for tag in sp_tags:
            if tag['title'] not in post_dict:
                post_dict[tag['title']] = tag['href']   #title 중복아닌 경우에만 링크를 post_dict에 할당

        print(len(post_dict), "news in "+today)
        return post_dict
    else:
        print("There is no news about hakdokman in "+today)


def hakdokman_noti(**api_conf):
    response = news_crawler()    # 크롤러 호출
    if response:                 # 학독만 관련 새로운 뉴스가 있을 경우에만 메시지 보냄.
        for title, link in response.items():
            api_conf['text'] = form.format(link=link, title=title)   # 링크 바로가기 형식으로 메시지 노출
            slack_client.api_call('chat.postMessage', **api_conf)


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]

        initial_config = {
            'username': '학독만 뉴스봇',
            'channel': '#뉴스_학독만',     # 기사 업로드할 채널명
            'text': form,    # 링크 바로가기 형식으로 메시지 노출
            'unfurl_links': True           # 링크 미리보기 true로 해놓고 메타데이터 있는 경우에도 미리보기 노출 안되는 케이스 존재..
        }

        while True:
            try:
                hakdokman_noti(**initial_config)
                time.sleep(RTM_READ_DELAY)
            except Exception as error:
                logging.exception(error)
                error_config['text'] = "[ERROR OCCURRED] "+str(error)
                slack_client.api_call('chat.postMessage', **error_config)   # 에러 내용 SLACK 전송
            break
    else:
        print("Connection failed. Exception traceback printed above.")
