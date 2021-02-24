# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib.request as req
from selenium import webdriver
import os, time

# 2) webdriver 객체 생성
driver = webdriver.Chrome('./webdriver/chromedriver')
driver.implicitly_wait(3)

# 3) 보배드림 사이트에서 차량 상세페이지 주소 가져오기
url = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=K"
driver.get(url)

# 4) url 열고 bs4로 파싱 및 이미지 주소 얻기
html = urlopen(url)
soup = bs(html, "html.parser")

# 4) 제조사 클릭
# 제조사에 해당하는 button 태그들의 리스트
jejosa_list = driver.find_elements_by_tag_name('div.area-maker > div > dl > dd > button')
for jejosa in jejosa_list:
    # 반복문에서 순서대로 제조사에 해당하는 태그를 한 번씩 클릭
    jejosa.find_element_by_css_selector('button span.t1').click()
    time.sleep(1)
    # 현재의 제조사명을 변수에 지정
    jejosa_name = jejosa.find_element_by_css_selector('button span.t1').text

    ##################### DB 입력 #####################

    # 5) 모델 클릭
    # 모델에 해당하는 button 태그들의 리스트
    model_list = driver.find_elements_by_tag_name('div.area-model > div > dl > dd > button')
    for model in model_list:
        # 반복문에서 순서대로 모델에 해당하는 태그를 한 번씩 클릭
        model.find_element_by_css_selector('button span.t1').click()
        time.sleep(1)
        # 현재의 모델명을 변수에 지정
        model_name = model.find_element_by_css_selector('button span.t1').text
        print(jejosa_name, model_name)

        ##################### DB 입력 #####################

        # 6) 세부모델 클릭
        # 선택자로 클릭할 수 없어 webdriver로 현재 url 다시 열어야 함
        driver2 = webdriver.Chrome('./webdriver/chromedriver')
        driver2.implicitly_wait(3)     # 이미지 파일 때문에 여유시간 필요
        # 새로 열린 창에서 기존 창의 url로 접속
        driver2.get(driver.current_url)

        # 현재 url 얻은 뒤 bs로 파싱하기
        html = urlopen(driver.current_url)
        soup = bs(html, "html.parser")

        # 숨겨져있는 세부모델(display:none)을 모두 포함하는 dd 태그들
        alldd = soup.select('.area-detail dd')
        # 화면에 출력되는 세부모델이 작성되어 있는 label 태그들
        details = soup.select('.area-detail dd label')

        # 새로 열린 창에서 체크박스에 해당하는 input 태그들
        check_boxes = driver2.find_elements_by_css_selector('.area-detail input')

        # dd태그와 label태그를 zip으로 묶는다.
        i = 0
        for onedd,detail in zip(alldd,details):
            # dd태그 안에 none이 없을 경우 = display:none이 아닐 경우에만 화면에 출력됨
            if not('none' in str(onedd)):
                # 현재의 세부모델명을 변수에 지정
                detail_name = detail.text
                # 세부모델명 출력
                print(detail_name)

                ##################### DB 입력 #####################

                # 세부모델명 체크(클릭)
                check_boxes[i].click()
                time.sleep(3)

                # 7) 등급 클릭
                # 선택자로 클릭할 수 없어 webdriver로 현재 url 다시 열어야 함
                driver3 = webdriver.Chrome('./webdriver/chromedriver')
                driver3.implicitly_wait(3)  # 이미지 파일 때문에 여유시간 필요
                # 새로 열린 창에서 기존 창의 url로 접속
                driver3.get(driver.current_url)

                check_boxes[i].click()

                # 현재 url 얻은 뒤 bs로 파싱하기
                html = urlopen(driver.current_url)
                soup = bs(html, "html.parser")

                # 숨겨져있는 등급(display:none)을 모두 포함하는 dd 태그들
                alldd = soup.select('.area-grade dd')
                # 화면에 출력되는 등급이 작성되어 있는 label 태그들
                details = soup.select('.area-grade dd label')

                # 새로 열린 창에서 체크박스에 해당하는 input 태그들
                check_boxes = driver2.find_elements_by_css_selector('.area-grade input')

                # dd태그와 label태그를 zip으로 묶는다.




                # 세부모델명 체크해제(클릭)
                check_boxes[i].click()
                # break
            i+=1
        time.sleep(1)
        break
    break




