'''
    차량명에 해당하는 차량제원 정보를 grade 테이블 default_info에 입력
'''

# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib.request
from selenium import webdriver
from google.cloud import storage as gcs
import os, pymysql, time

driver = webdriver.Chrome('./webdriver/chromedriver.exe')
driver2 = driver
driver.implicitly_wait(2)
conn = pymysql.connect(host='34.64.176.78', port=3306,
                       db='mycar', user='root', password='admin1234',
                       charset='utf8')

cursor = conn.cursor()

sell_sql = "SELECT sell_id,g_id,title FROM sell WHERE default_info is null"
cursor.execute(sell_sql)
g_ids = cursor.fetchall()

cnt = 114
for sell_id,g_id,title in g_ids:
    print(sell_id, ' : ', g_id, ' : ', title)
    url = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=I"
    driver.get(url)
    q = driver.find_element_by_id('inp-search')
    q.send_keys(title)
    driver.find_element_by_css_selector('#frm_search > div.wrap-finder-option.js-options-container > div > div > button').click()
    time.sleep(2)

    driver2.get(driver.current_url)
    html = urlopen(driver2.current_url)
    soup = bs(html, "html.parser")
    time.sleep(1)

    car_info = ''
    dds = soup.select('dl.is-list dd')
    for dd in dds:
        if dd.text == "성능기록":
            break
        elif dd.text == "보험이력":
            break
        elif dd.text in car_info:
            break
        else:
            car_info = car_info + '/' + dd.text
    sell_default_info = "UPDATE sell SET default_info='{}' WHERE title='{}'".format(car_info,title)
    cursor.execute(sell_default_info)
    conn.commit()
    # print(sell_default_info)
    grade_default_info = "UPDATE grade SET default_info='{}' WHERE g_id='{}'".format(car_info,g_id)
    cursor.execute(grade_default_info)
    # print(grade_default_info)
    conn.commit()
    cnt = cnt + 1

cursor.close()
conn.close()
print('완료')




