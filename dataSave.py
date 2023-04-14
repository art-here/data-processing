import gspread
import os
import requests
import uuid


def renameImage(name):  # 이미지 이름 변경

    url = str(uuid.uuid4())  # 4버전 사용
    os.rename("./image/" + name + ".jpg", "./image/" + url + ".jpg")

    return "image/" + url + ".jpg"


# API 요청
def requestAPI(name, image, latitude, longitude, address, category, author, agency, info, start, end):
    url = 'https://dev.art-here.site/api/admin/art'
    token = ""

    data = {
        "artName": name,
        "imageURL": image,
        "latitude": latitude,
        "longitude": longitude,
        "roadAddress": address,
        "category": category,
        "authorName": author,
        "agency": agency,
        "info": info,
        "startDate": start,
        "endDate": end
    }
    auth = {
        "Authorization": "Bearer " + token
    }

    response = requests.post(url, json=data, headers=auth)

    print(response.text)
    print(response.status_code)


# 작품 데이터 저장
def processData():
    # gspread read
    gc = gspread.service_account(filename="./art-here.json")
    sh = gc.open("art-here").worksheet("시트1")
    table = sh.get_all_values()
    f = open("sql.txt", 'r', encoding="UTF-8")

    for i in range(1, len(table)):
        # get Image URL
        url = renameImage(table[i][0])  # image

        # save data
        # name, image, latitude, longitude, address, category, author, agency, info, start, end
        requestAPI(table[i][5], url, table[i][10], table[i][11], table[i][9], table[i][1], table[i][3],
                   table[i][7], table[i][6], table[i][2], table[i][8])


if __name__ == '__main__':
    processData()
