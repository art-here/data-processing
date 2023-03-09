import gspread

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()  # 옵션 생성
options.add_argument("headless")  # 창 숨기는 옵션 추가
driver = webdriver.Chrome(executable_path='chromedriver', options=options)

dic = {'유형': 1, '연도 / 기간': 2, '위치/공간': 3, '아티스트': 4}


# 분당 60 제한

def main():
    page = 1  # 페이지 시작 1~9 까지
    end = 10  # 마지막 페이지
    i = 1  # 1~20 까지
    driver.implicitly_wait(time_to_wait=5)
    driver.get("https://seoulismuseum.kr/seoul/search.do?page=" + str(page))
    data = []

    while end > page:
        posting = get_element('//*[@id="list_archive"]/div[' + str(i) + ']')  # 요소 지정

        if posting:  # 해당 요소 게시물이 있음
            posting.click()
            driver.switch_to.window(driver.window_handles[-1])  # 새 창 전환

            # 값 들고 오기
            # 이미지, 영상
            element = driver.find_element(By.XPATH, '//*[@id="cn-top-image"]|//*[@id="cn-top-video"]/source')

            # 정보
            title = get_element('/html/body/main/article/section[2]/div/div/div/header/h2')
            detail = driver.find_element(By.XPATH, '/html/body/main/article/section[2]/div/div/div/div/div[1]/ul')
            info = get_element('/html/body/main/article/section[2]/div/div/div[1]/div/div[2]')

            # 데이터 임시 저장
            data.append([None, None, None, None, element.get_attribute('src'), title.text, info.text])

            details = detail.text.split('\n')

            for k in range(len(details) - 1):
                key = details[k]
                if dic.get(key):
                    data[len(data) - 1][dic[key] - 1] = details[k + 1]

            print("--- process count: " + str(i))

            driver.close()  # 팝업창 닫기
            driver.switch_to.window(driver.window_handles[0])  # 기존 창 전환

            i += 1  # 요소 위치

        else:  # 게시물이 없음, more 버튼으로 게시물을 더 불러옴
            if i < 20:  # 더이상 데이터가 없음 종료
                print("--- no data")
                break
            else:
                page += 1
                i = 1
                driver.get("https://seoulismuseum.kr/seoul/search.do?page=" + str(page))  # 다음 페이지 이동
                print("--- more page: " + str(page))

    driver.quit()  # driver 종료

    save(data)  # 저장


def get_element(xpath):
    try:
        result = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return None
    return result


def save(data):
    print("--- save data")
    gc = gspread.service_account(filename="./art-here.json")
    sh = gc.open("art-here").worksheet("시트1")

    for d in data:
        sh.append_row(d)


if __name__ == '__main__':
    main()
