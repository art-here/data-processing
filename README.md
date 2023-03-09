### gatherData.py

---
실행 화면

```
지역:
서울
페이지
시작:
1
페이지
끝:
3
```

지역 종류

```
서울, 세종, 부산, 대구, 인천, 광주, 대전, 울산, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주
```

1. 실행 후 실행 화면에 원하는 지역과 수집하고 싶은 데이터의 페이지 번호를 입력
2. 요청 후 가공된 데이터는 구글 스프레드시트에 저장

반환 데이터

```
[category, image, art_name, author_name, address, latitude, longitude, start_date]
```

구글 API 요금 관련으로 분당 요청 페이지수 크기를 4로 제한

데이터 출처: [공공 미술 포털](https://www.publicart.or.kr/search/total_list.do?menuId=15)

### gatherDateBySeoulismuseum.py

---

데이터 구성

```
[content, 작품 이름, 상세 내용, 유형, 연도 / 기간, 위치/공간, 아티스트]
```

출력

```
--- process count: 19
--- process count: 20
--- more page: 9
--- process count: 1
--- process count: 2
--- process count: 3
--- no data
--- save data
```

1. main() 함수에 있는 page 와 end 를 수정해 원하는 데이터 요청
2. 요청 후 가공된 데이터는 구글 스프레드시트에 저장

반환 데이터

```
['작품구현', '2019', '서울 중랑구 용마산로 250-12', '정지현', 'https://player.vimeo.com/external/606560220.hd.mp4?s=f98f4963bff16eb8b86e38d243ca3eb7743a92cc&amp;profile_id=175', '타원본부, 2017', "시민이 간직한 소중한 추억이 작품이 되다\n<타원 본부>는2018~2019년까지 2년에 걸쳐 진행된공공미술 시민 아이디어 구현 사업으로 시민이 직접 작품 제작에 참여하는 프로젝트였습니다."']
```

구글 API 요금 관련으로 분당 요청 60 제한

데이터 출처: [서울은 미술관](https://seoulismuseum.kr/seoul/index.do?content=main)

### changeSql.py

---

구글 스프레드시트에 저장돼있는 데이터를 읽어와 SQL문으로 변환 후 sql.txt에 저장