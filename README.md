# The Omnisummaizer

## 소개

이 제안서의 목적은 모든 것의 요악을 목표로하는 프로젝트를 개요하고 설명하는 것입니다.

## 목표

이 프로젝트의 목표는 다음과 같습니다:

- 모든 것을 요약하는 프로그램

## 범위

이 프로젝트의 범위에는 다음이 포함됩니다:

- **유튜브 동영상 요약**
    - 유튜브 동영상 링크 → Transcript → 요약문
    - Segment를 이용해 1시간 이상의 긴 동영상도 요약할 수 있도록
    - [참고 링크](https://www.reddit.com/r/ChatGPT/comments/10m3bwd/a_very_cool_and_useful_script_i_wrote_with_the/)
- **문서 요약**
    - 문서 링크를 넣으면 요약문을 뱉어줌
    - 웹사이트마다 문서 포맷이 다양하므로 자주 쓰이는 사이트 위주로 문서 요약 지원을 추가해야 할 필요 있음
        - 네이버 블로그
        - 티스토리
        - 미디움
        - 서브스택
        - mirror.xyz
- **팟캐스트, 트위터 스페이스 요약**
- **커뮤니티 채팅 등 cacual conversation도 요약 (예정)**
    - 트위터 스레드
    - 텔레그램 메시지
    - 디스코드 메시지
- **모든 요약에는 번역 기능 추가**
- **링크를 넣고 요약을 받는 플랫폼은 텔레그램 사용**
    - CommandHandler 사용해서 링크를 받고 요약문을 reply하는 방식으로

## 방법론

이 프로젝트는 다음 방법론을 사용하여 실행됩니다:

- **파이썬 사용**
- **유튜브 동영상 대본 따오기**
    - [Transcript 따오는 API](https://pypi.org/project/youtube-transcript-api/)
- **게시글 링크에 있는 글 따오기**
    - 각 링크에 맞는 scraper code 만들어야 함
    - beautlfulsoup4 또는 selenium 사용
    - 4,000 자가 넘을 경우
- **팟캐스트, 트위터 스페이스 요약**
    - https://github.com/adwisatya/TwitterSpaces2Text << 트위터 스페이스 대본 가져오는 라이브러리
- **요약문 생성**
    - [OpenAI 라이브러리 이용](https://pypi.org/project/openai/)
    - 요약 대상의 길이에 따라 요약문의 크기를 자동으로 조절하는 기능도 있었으면
- **번역**
    - [DeepL 라이브러리 이용 (가능하다면)](https://pypi.org/project/deepl/)
    - 안되면 구글 번역 라이브러리 이용
- **텔레그램 메시지**
    - python-telegram-bot 라이브러리 이용

## 타임라인

이 프로젝트는 최대한 빠른 시간 내에 완료될 것이며 다음의 중간 결과물을 가질 것입니다:

- 유튜브 동영상 segment를 이용한 요약
- 게시글 링크 (segment를 이용한) 요약
    - 네이버 블로그, 미디엄, 서브스택, mirror.xyz, 티스토리, 브런치 등
- 트위터 스레드 요약
- 위의 요약 프로그램을 텔레그램 서버에 올리기

## 예산

이 프로젝트의 예산은 {예산}으로 예산 항목

1. 시간
2. 커피
3. 노오오오력
4. 열정
5. 악
6. 깡

## 결론

이 프로젝트 제안서는 제안된 프로젝트의 목표, 범위, 방법론, 타임라인 및 예산을 개요하고 설명합니다. 이 프로젝트가 세상의 모든 것을 요약하고 빠르게 섭취할 수 있게 함으로써 생산성의 대단햔 향상을 제공할 것으로 믿습니다.