# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib.request as req
from selenium import webdriver
import os, time
import pymysql
#------------------------함수들---------------------------------
# 데이터를 mariaDB에 저장하는 함수
def saveDB(sql):

    # 통로 연결
    conn = pymysql.connect(host='34.64.176.78', port=3306,
                           db='mycar', user='root', password='admin1234',
                           charset='utf8')
    print('연결성공')
    cursor = conn.cursor()
    # 필요한 수량만큼 수정 ##############
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

# 최종적으로 들어갈 데이터를 list 형태로 담아서 저장함
#--------------------------------------------------------------
# txt 파일을 읽어오는 함수 (중복 확인하는 mulit()에서 호출 예정)
def readTXT1():
    with open('./searchoption/category.txt', 'r', encoding='utf-8') as f:
        lines = f.read()
    return lines

#--------------------------------------------------------------
# 중복 확인하는 함수
def multi(tel):
    lines = readTXT1()
    if tel in lines:
        flag = True
    else:
        flag = False
    return flag

#--------------------------------------------------------------
# txt 파일로 저장하는 함수
def saveTXT1(result):
    with open('./searchoption/category.txt', 'a', encoding='utf-8') as f:
        for i in range(4):
            if i < 3:
                f.write(result[i])
                f.write(',')
            if i == 3:
                f.write(result[i])
        f.write('\n')
def saveTXT2(result):
    with open('./searchoption/detail.txt', 'a', encoding='utf-8') as f:
        for i in range(3):
            if i < 2:
                f.write(result[i])
                f.write(',')
            if i == 2:
                f.write(result[i])
        f.write('\n')
def saveTXT3(result):
    with open('./searchoption/grade.txt', 'a', encoding='utf-8') as f:
        for i in range(4):
            if i < 3:
                f.write(result[i])
                f.write(',')
            if i == 3:
                f.write(result[i])
        f.write('\n')
#--------------------------------------------------------------
# 파일을 저장할 폴더 생성
savedir = os.path.dirname('./searchoption/')
if not os.path.exists(savedir):
    os.makedirs(savedir)
    # 데이터 저장 전 txt 파일을 읽어 중복확인을 하므로 에러 발생을 막고자 첫 라인을 입력
    column_name1 = ['car_num','jejosa','model','abroad']
    column_name2 = ['d_id','car_num','detail']
    column_name3 = ['g_id','d_id','grade1','grade2']
    saveTXT1(column_name1)
    saveTXT2(column_name2)
    saveTXT3(column_name3)


#--------------------------------------------------------------
#--------------------------------------------------------------
#--------------------------------------------------------------


# 2) webdriver 객체 생성
driver = webdriver.Chrome('./webdriver/chromedriver')
driver.implicitly_wait(3)

# 3) 보배드림 사이트에서 차량 상세페이지 주소 가져오기
url = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=I"
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


    i = 0
    # 5) 모델 클릭
    # 모델에 해당하는 button 태그들의 리스트
    model_list = driver.find_elements_by_tag_name('div.area-model > div > dl > dd > button')
    for model in model_list:
        # 반복문에서 순서대로 모델에 해당하는 태그를 한 번씩 클릭
        model.find_element_by_css_selector('button span.t1').click()
        time.sleep(1)
        # 현재의 모델명을 변수에 지정
        model_name = model.find_element_by_css_selector('button span.t1').text


        #####################중복검사 추가##################
        result1 = [i, jejosa_name, model_name, '국내']
        # 중복 여부를 확인 (중복:True / 값없을때:False)
        flag = multi(result1[2])
        ##################### DB 입력 #####################
        # 중복 데이터가 없을 경우 TXT,DB에 데이터 저장
        if(flag):
            pass
        else:
            sql = "INSERT INTO category (car_num, jejosa, model, abroad) VALUES ('{}','{}','{}','{}')".format(i, jejosa_name, model_name, '국내')
            saveTXT1()
            saveDB(sql)

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
        for onedd,detail in zip(alldd,details):
            # dd태그 안에 none이 없을 경우 = display:none이 아닐 경우에만 화면에 출력됨
            if not('none' in str(onedd)):
                # 현재의 세부모델명을 변수에 지정
                detail_name = detail.text
                # 세부모델명 출력
                # print(detail_name)

                # 세부모델명 체크(클릭)
                check_boxes[i].click()
                time.sleep(3)

                ##################### DB 입력 #####################
                sql = "INSERT INTO detail (d_id, car_num, detail) VALUES ('{}',i,'{}')".format(str(i)+'-1',detail_name)
                # saveDB(sql)
                ##################### DB 입력 #####################


                # 7) 등급 클릭
                # 선택자로 클릭할 수 없어 webdriver로 현재 url 다시 열어야 함
                driver3 = webdriver.Chrome('./webdriver/chromedriver')
                driver3.implicitly_wait(3)  # 이미지 파일 때문에 여유시간 필요
                # 새로 열린 창에서 기존 창의 url로 접속
                driver3.get(driver2.current_url)


                # 현재 url 얻은 뒤 bs로 파싱하기
                html2 = urlopen(driver2.current_url)
                soup2 = bs(html2, "html.parser")

                # 숨겨져있는 등급(display:none)을 모두 포함하는 dd 태그들
                alldd2 = soup2.select('.area-grade dd')


                # 화면에 출력되는 등급이 작성되어 있는 label 태그들
                grade2 = soup2.select('.area-grade dd label')
                for detail2 in grade2:
                    grade1 = detail2.text
                    print(grade1)
                    break

                    # 새로 열린 창에서 체크박스에 해당하는 input 태그들
                    check_boxes2 = driver2.find_elements_by_tag_name('div.area-grade dd input')
                    for check_box2 in check_boxes2:
                        print(check_box2)
                        check_box2.click()
                        break

                # # 세부모델명 체크해제(클릭)
                # check_boxes[i].click()
                break
            i+=1
        time.sleep(1)
        break
    break




