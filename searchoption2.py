# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib.request as req
from selenium import webdriver
import os, time
import pymysql

def saveDB1(result):

    # 통로 연결
    conn = pymysql.connect(host='34.64.176.78', port=3306,
                           db='mycar', user='root', password='admin1234',
                           charset='utf8')
    print('연결성공')
    cursor = conn.cursor()
    # 필요한 수량만큼 수정 ##############
    sql = "INSERT INTO category VALUES ('{}','{}','{}','{}')".format(result[0], result[1], result[2], result[3])
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

def saveDB2(result):

    # 통로 연결
    conn = pymysql.connect(host='34.64.176.78', port=3306,
                           db='mycar', user='root', password='admin1234',
                           charset='utf8')
    print('연결성공')
    cursor = conn.cursor()
    # 필요한 수량만큼 수정 ##############
    sql = "INSERT INTO detail VALUES ('{}','{}','{}')".format(result[0], result[1], result[2])
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

def saveDB3(result):

    # 통로 연결
    conn = pymysql.connect(host='34.64.176.78', port=3306,
                           db='mycar', user='root', password='admin1234',
                           charset='utf8')
    print('연결성공')
    cursor = conn.cursor()
    # 필요한 수량만큼 수정 ##############
    sql = "INSERT INTO grade VALUES ('{}','{}','{}','{}')".format(result[0], result[1], result[2], result[3])
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

sq1 = 38
sq2 = 38122
sq3 = 3802551

# 2) webdriver 객체 생성
driver = webdriver.Chrome('./webdriver/chromedriver')
driver.implicitly_wait(3)
driver2 = webdriver.Chrome('./webdriver/chromedriver')
driver2.implicitly_wait(1)
driver3 = webdriver.Chrome('./webdriver/chromedriver')
driver3.implicitly_wait(1)
driver4 = webdriver.Chrome('./webdriver/chromedriver')
driver4.implicitly_wait(1)

url = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=K"
driver.get(url)

html = urlopen(url)
soup = bs(html, "html.parser")

# 4) 제조사 클릭
# 제조사에 해당하는 button 태그들의 리스트
jejosa_list = driver.find_elements_by_tag_name('div.area-maker > div > dl > dd > button')

count = 0
for jejosa in jejosa_list:

    # 반복문에서 순서대로 제조사에 해당하는 태그를 한 번씩 클릭
    jejosa.find_element_by_css_selector('button span.t1').click()
    time.sleep(1)

    # 현재의 제조사명을 변수에 지정
    jejosa_name = jejosa.find_element_by_css_selector('button span.t1').text

    # 5) 모델 클릭
    # 모델에 해당하는 button 태그들의 리스트
    templists = []
    model_list = driver.find_elements_by_tag_name('div.area-model > div > dl > dd > button')
    for model in model_list:
        ck=0
        # 반복문에서 순서대로 모델에 해당하는 태그를 한 번씩 클릭
        model.find_element_by_css_selector('button span.t1').click()
        time.sleep(1)
        # 현재의 모델명을 변수에 지정
        model_name = model.find_element_by_css_selector('button span.t1').text
        for templist in templists:
            if templist == model_name:
                ck=1
                break
        if ck == 1:
            continue
        templists.append(model_name)
        count += 1
        if count < 38:
            continue
        result1=[sq1, jejosa_name, model_name, '국내차']
        saveDB1(result1)

        driver2.get(driver.current_url)

        html2 = urlopen(driver.current_url)
        soup2 = bs(html2, "html.parser")

        # 숨겨져있는 세부모델(display:none)을 모두 포함하는 dd 태그들
        alldd = soup2.select('.area-detail dd')
        # 화면에 출력되는 세부모델이 작성되어 있는 label 태그들
        details = soup2.select('.area-detail dd label')
        # 새로 열린 창에서 체크박스에 해당하는 input 태그들
        check_boxes = driver2.find_elements_by_css_selector('.area-detail input')
        check_temp = driver2.find_elements_by_css_selector('.area-grade input')


        # dd태그와 label태그를 zip으로 묶는다.
        i = 0
        for onedd, detail in zip(alldd, details):
            # dd태그 안에 none이 없을 경우 = display:none이 아닐 경우에만 화면에 출력됨
            if 'none' not in str(onedd):
                # 현재의 세부모델명을 변수에 지정

                detail_name = detail.text
                # 세부모델명 출력

                result2 = [sq2, sq1, detail_name.replace('\xa0','')]
                saveDB2(result2)

                if len(check_temp) == 0:
                    check_boxes[i].click()
                    time.sleep(1)

                driver3.get(driver2.current_url)
                check_boxes[i].click()

                html3 = urlopen(driver2.current_url)
                soup3 = bs(html3, "html.parser")

                gradedds = soup3.select('.area-grade label')
                checks = driver3.find_elements_by_css_selector('.area-grade input')

                for gradedd, check in zip(gradedds,checks):
                    check.click()
                    time.sleep(1)

                    driver4.get(driver3.current_url)

                    html4 = urlopen(driver3.current_url)
                    soup4 = bs(html4, "html.parser")

                    check.click()

                    grade_details = soup4.select('.area-grade>div>dl>dd dd label')
                    if len(grade_details) == 0:
                        result3 = [sq3, sq2, gradedd.text, '0']
                        saveDB3(result3)
                        sq3 += 1
                    else:
                        for grade_detail in grade_details:
                            result3 = [sq3, sq2, gradedd.text, grade_detail.text]
                            saveDB3(result3)
                            sq3 += 1
                sq2 += 1
            i += 1
        sq1 += 1
        sq2 += 1000
        sq3 += 100000