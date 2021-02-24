import pymysql
from selenium import webdriver
import time, os, csv
from bs4 import BeautifulSoup

# 데이터를 mariaDB에 저장하는 함수
def saveDB(result):

    # 통로 연결
    conn = pymysql.connect(host='34.64.176.78', port=3306,
                           db='mycar', user='root', password='admin1234',
                           charset='utf8')
    print('연결성공')
    cursor = conn.cursor()
    # 필요한 수량만큼 수정 ##############
    sql = "INSERT INTO news VALUES (nextval(news_w_id_sq),'{}','{}', 0, 0,'{}')".format(result[0], result[1], result[2])
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

driver = webdriver.Chrome('./webdriver/chromedriver')
driver.implicitly_wait(1)
driver2 = webdriver.Chrome('./webdriver/chromedriver')
driver2.implicitly_wait(1)
for i in range(1,13):
    driver.get('https://www.bobaedream.co.kr/list?code=nnews&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&s_select=&s_key=&level_no=&vdate=&type=list&page={}'.format(i))
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    alls = soup.select('.bsubject')
    alls = alls[5:]
    for all in alls:
        num = str(all).split('No=')[1].split('&')[0]
        driver2.get('https://www.bobaedream.co.kr/view?code=nnews&No={}&bm=1'.format(num))
        time.sleep(1)

        html = driver2.page_source
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.select_one('.content02')

        title = soup.select_one('.writerProfile strong')

        day = soup.select_one('.countGroup').text.split(' ')

        result = [title.text.split("[")[0], day[-2].split('\xa0')[0] + " " + day[-1],
                  str(div).replace('\t', '').replace('\n', '').replace("'", '"').replace('\xa0', '')]
        #saveDB(result)