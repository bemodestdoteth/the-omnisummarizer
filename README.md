# The Omnisummaizer

## 소개

모든 것을 간편하게 요약

## 요약 범위
- **1. 유튜브 동영상**
    - 유튜브 동영상 링크 → Transcript → 요약문
    - 1시간 정도의 긴 동영상은 Segment를 이용해 요약
    - [참고 링크](https://www.reddit.com/r/ChatGPT/comments/10m3bwd/a_very_cool_and_useful_script_i_wrote_with_the/)
- **2. 글**
    - 웹사이트 → 본문 → 요약문
    - 자주 쓰이는 웹사이트 위주로
        - 네이버 블로그
        - 티스토리
        - 미디엄
        - 서브스택
        - 미러
        - 트위터 스레드
    - 4,000자 이상의 긴 글은 Segment를 이용해 요약
- **3. 팟캐스트, 트위터 스페이스**
    - 팟캐스트/트위터 스페이스 → Transcript → 요약문
- **4. 커뮤니티 채팅 등 cacual conversation (예정)**
    - 텔레그램, 디스코드
    - 필요시 워드클라우드 기능도 구현
- **5. 요약문 번역 기능**

## 방법론

- **사용 언어**
    - 파이썬
- **1. 유튜브 동영상**
    - 자막 있는 영상은 자막, 자막 없는 영상은 음성 인식 이용
    - 특정 시간(5분) 기준으로 Segment를 나눈 다음 Segment별로 1차 요약 진행
    - 1차 요약 결과물 생성
    - Segmentation 참고: [유튜브 동영상을 Segmented Transcript로 만들어주는 라이브러라](https://pypi.org/project/youtube-transcript-api/)
- **2. 글**
    - 각 링크에 맞는 scraper code 제작
    - beautlfulsoup4 또는 selenium 라이브러리 사용
    - 4,000자를 기준으로 Segment를 나눈 다음 Segment별로 1차 요약 진행
    - 1차 요약 결과물 생성
- **3. 팟캐스트, 트위터 스페이스 요약**
    - 음성인식 이용
    - [트위터 스페이스 라이브러리](https://github.com/adwisatya/TwitterSpaces2Text)
    - 특정 시간(5분?)을 기준으로 Segment를 나눈 다음 Segment별로 1차 요약 진행
    - 1차 요약 결과물 생성
- **4. 요약문 생성**
    - [OpenAI 라이브러리 이용](https://pypi.org/project/openai/)
    - 1차 요약문 Segment 개수에 따라 요약문의 크기를 자동으로 조절하는 기능 추가 ex) 1차 요약의 Segment가 5개가 넘으면 2개의 문단으로 요약
- **5. 번역**
    - [DeepL 라이브러리 이용 (가능하다면)](https://pypi.org/project/deepl/)
    - DeepL이 불가능하다면 Plan B로 구글 번역 라이브러리 이용
    - 번역은 최종 요약문 대상으로 진행
- **6. 링크 input을 넣는 플랫폼**
    - 텔레그램 사용 예정
    - python-telegram-bot 라이브러리 이용. CommandHandler 사용해서 링크를 받고 4번의 최종 요약문을 답장
- **기타 세부 방법론**
    - Segmentation 기준 (5분, 4,000자)는 유저가 링그 Input을 넣을 때 Parameter로 같이 넣을 수 있어야 함
    - 텔레그램 그룹을 만들어 그룹 참여자들끼리 요약 결과를 공유할 수 있으면 좋겠음

## 타임라인

이 프로젝트는 최대한 빠른 시간 내에 완료될 것이며 다음의 중간 결과물을 가질 것입니다:

- 1 ~ 3번까지 각자 맡아서 진행
- 4번 요약문을 만들기 위해 1 ~ 3번의 
- 6번은 제가 만들 예정

## 예산

이 프로젝트의 예산은 {예산}으로 다음과 같은 항목이 필요합니다.

1. 시간
2. 커피
3. 노오오오력
4. 열정
5. 악
6. 깡

## 결론

이 프로젝트 제안서는 제안된 프로젝트의 목표, 범위, 방법론, 타임라인 및 예산을 개요하고 설명합니다. 이 프로젝트가 세상의 모든 것을 요약하고 빠르게 섭취할 수 있게 함으로써 생산성의 대단햔 향상을 제공할 것으로 믿습니다.