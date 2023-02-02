### gatherData.py

---
실행 화면

```python
지역:
서울
페이지 시작:
1
페이지 끝:
3
```

지역 종류

```python
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

### changeSql.py

---

구글 스프레드시트에 저장돼있는 데이터를 읽어와 SQL문으로 변환 후 sql.txt에 저장