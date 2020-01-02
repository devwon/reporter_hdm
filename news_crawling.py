#!~/reporter_hdm/botvenv/bin/python     #가상환경내 파이썬사용

# hakdokman news web crawler 만들기
import os
import time
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

# hakdokman news web crawler
# 당일 날짜의 학독만 관련 뉴스 링크를 크롤링해서 가져온다.
def news_crawler():
    url = 'https://search.naver.com/search.naver'
    post_dict = OrderedDict()
    title_text = []
    link_text = []
    today = datetime.today().strftime("%Y.%m.%d")  # YYYY.mm.dd 형태의 시간 출력

    params = {
        # 'query': '%22%ED%95%99%EC%83%9D%EB%8F%85%EB%A6%BD%EB%A7%8C%EC%84%B8%22-%ED%95%99%EC%83%9D%EB%8F%85%EB%A6%BD%EB%A7%8C%EC%84%B8%EC%9A%B4%EB%8F%99',
        'query': '"학생독립만세"-학생독립만세운동',   #검색어: '학생독립만세'('학생독립만세운동'은 제외)
        'where': 'news',
        'sm': 'tab_opt',
        # 'sm': 'tab_pge', # pagination 사용시 주석 풀기
        # 'start': '22', # pagination 사용시 주석 풀기
        'sort': '1',
        'pd': '3',
        #'ds': '2020.01.02',  # 오늘 날짜 변수 넣기
        #'de': '2020.01.02',  # 오늘 날짜 변수 넣기
        'ds': today,  # 오늘 날짜 변수 넣기
        'de': today,  # 오늘 날짜 변수 넣기
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
                #post_dict[tag['title']] = tag['href'].replace("http://", "https://")  # http->https 바꿔주고, post_dict에 할당

        print(len(post_dict), "news")
        return post_dict
    else:
        print("오늘 날짜("+today+")의 학독만 관련 뉴스가 없습니다ㅠㅠ")


def hakdokman_noti():
    response = news_crawler()    # 크롤러 호출
    if response:                 # 학독만 관련 새로운 뉴스가 있을 경우에만 메시지 보냄.
        #for link_text in response:
        for title, link in response.items():

            slack_client.api_call(
                "chat.postMessage",
                channel='#newsbot_hdm',  #newsbot_hdm 채널에 기사 알림
                text='<'+link+'|'+title+'>',    #링크 바로가기 형식으로 메시지 노출
                #attachments=[{"pretext": link, "text": title}],
                unfurl_links=True       # 링크 미리보기 true로 해놓고 메타데이터 있는 경우에도 미리보기 노출 안되는 케이스 존재..
            )


if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            hakdokman_noti()
            time.sleep(RTM_READ_DELAY)
            break
    else:
        print("Connection failed. Exception traceback printed above.")
