# 학독만 관련 뉴스 안내봇
> 네이버 기사내 학독만 관련 뉴스 크롤링
 
-- 소스코드는 gitlab에 /lyn/reporter_hdm/

-- 개발자=린(lyn)**

**1. 개요**
----------

학독만 관련 기사를 올리는 **#뉴스_학독만** 채널을 자동화하기 위한 **뉴스안내봇**

**2. 기능**
----------
매일 오후 11시 59분에 학독만 관련 기사가 올라옴
- ✅서비스 프로세스
	(오후 11시 59분)
	1.  네이버 기사 내 오늘자 기사 검색(검색어: "학생독립만세" -학생독립만세운동)
	2.  크롤링 후 기사 링크와 제목 가져옴
	3.  기사 제목이 중복되지 않으면 담음
	4.  담긴 내용이 있으면 메시지 하나에 링크|기사제목 형식으로 하나씩 메시지 보냄(최대 10개)

- 예시
	(링크 미리보기 되는 경우)
	노션에 정리

**3. TEST**
----------

매일 11시로 테스트

```
0 11 * * * ~/reporter_hdm/start_crawling.sh >> ~/reporter_hdm/crontab_log.txt 2>&1

```

11시에 정상적으로 알림

노션에 정리

**4. 이슈**
----------

1.  링크 미리보기 지원 관련
    
    -   이슈 내용 : 링크 미리보기가 안되는 경우가 왕왕 있음.
        
    -   해결법 :
        **When previews don't display**

		Here are some reasons your link may not expand to show a preview:
		- **The link contains no preview data.** If the web page doesn't include the necessary [embedded data](https://medium.com/slack-developer-blog/everything-you-ever-wanted-to-know-about-unfurling-but-were-afraid-to-ask-or-how-to-make-your-e64b4bb9254), the preview won't expand.
		    - **해결법** : 메타데이터가 존재하지 않는 경우가 있으므로, 기사 제목에 바로가기 형식으로 노출
		-  **You linked to a private page or file.** For example, you won't see a preview of password-protected YouTube or Vimeo videos.
		    -   발생할 가능성 X(∵ 네이버 기사 크롤링이므로)
		-   **It was recently posted by another member of your workspace.** No attachment will expand if that link was shared in the same conversation within the past hour.
			    -   발생할 가능성 X(∵ 매일 오전 8시에 크롤링하므로, 다른 날짜에 같은 제목의 기사를 올릴 가능성 없음 but 워낙 복붙 기사가 많아서..확실하진 않음)
		-  **You haven’t added the Twitter app yet.** If Twitter URLs don’t expand to show the full tweet, add the Twitter app to your workspace.
			    -   발생할 가능성 X(∵ 네이버 기사 크롤링이므로)
		-   **The link was to video or audio hosted by a service we've yet to whitelist.** We're working to whitelist more services in future!
		-   **http:// was not included.** Try adding http:// and your link should expand.
		-   **Your message contains more than four links.** If your message has five or more links included, they won't expand.
			    -   **해결법**: 리스트에 담긴 링크들을 한 메시지씩 보낸다.(메시지 하나에 링크 하나)
	    
        
2.  Crontab 관련
    -   이슈 내용 : PC off 또는 asleep일때 Crontab이 시행 안됨
	    ♻️crontab이 매일 오전 8시에 돌아야하는데, 평일 오전 9시에 출근하는 개발자의 PC는 보통 asleep..
    
    -   해결법: 노션에 따로 정리
