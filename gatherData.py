import gspread
import requests
from bs4 import BeautifulSoup

kinds = {'사진': 'PICTURE', '벽화': 'MURAL', '공예': 'CRAFT', '조각': 'SCULPTURE', '회화': 'CONVERSATION',
         '서예': 'CALLIGRAPHY', '미디어': 'MEDIA', '기타': 'OTHER'}

areas = {'서울': '11', '세종': '12', '부산': '26', '대구': '27', '인천': '28', '광주': '29', '대전': '30', '울산': '31',
         '경기': '41', '강원': '42', '충북': '43', '충남': '44', '전북': '45', '전남': '46', '경북': '47', '경남': '48',
         '제주': '50'}


# 분당 4회 이하 요청하기

def main():
    print("지역:")
    area = areas[input()]  # 지역

    print("페이지 시작:")
    start = int(input())  # 시작 페이지
    print("페이지 끝:")
    end = int(input())  # 끝 페이지

    if (abs(start - end) > 4):
        print("총 개수 4 페이지 이하 요청 가능")
        return

    gc = gspread.service_account(filename="./art-here.json")
    sh = gc.open("art-here").worksheet("시트1")

    for page in range(start, end + 1):
        data = gather(str(page), area)
        save(data, sh)


def gather(page, area):
    base = 'https://www.publicart.or.kr'
    time = ' 0:00:00'

    raw = requests.get(base + '/search/total_list.do?pagenum=' + page + '&menuId=15&search_sido_cd=' + area)
    html = BeautifulSoup(raw.text, 'html.parser')

    data = []

    for linke in html.find_all('h5'):  # 해당 태그 탐색
        url = linke.find('a').get('href')  # a 태그에 href 얻기
        raw = requests.get(base + url);
        html = BeautifulSoup(raw.text, 'html.parser')

        # 이미지
        image = base + html.select_one('#showhide').get('src')

        infoList = html.select_one('#content_sec > div > div > div.col-lg-5.col-md-6.col-sm-6 > dl').find_all('dd')
        art_name = infoList[0].text  # 작품 이름
        author_name = infoList[1].text  # 작가 이름
        category = getCategory(infoList[4].text)  # 카테고리
        start_date = infoList[5].text + time  # 작품 시작일
        address = infoList[6].text  # 주소

        # 위도, 경도
        sc = html.select_one('#content_sec > div > div > script')
        latitude, longitude = getPosition(sc)

        data.append(
            [category, image, art_name, author_name, '', '', '', address, latitude, longitude,
             start_date, '', ''])

    return data


def getPosition(sc):
    position = sc.text.replace('(', ' ').replace(')', ' ').split()[12:14]
    return format(float(position[0][:-1]), ".6f"), format(float(position[1]), ".6f")


def getCategory(kind):
    if kinds.get(kind):
        return kinds[kind]
    else:
        return 'OTHER'


def save(data, sh):
    for d in data:
        sh.append_row(d)


if __name__ == '__main__':
    main()
