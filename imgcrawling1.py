'''
    1단계
    보배드림 국산차 페이지에서 각 상품별 제목 / url 가져와서 DB의 carphoto 테이블에 저장
'''

# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from google.cloud import storage as gcs
import os, pymysql

# 2) 보배드림 사이트에서 차량 목록 페이지 주소 가져오기
for i in range(180, 191):
    url = "https://www.bobaedream.co.kr/mycar/mycar_list.php?gubun=K&page={}&order=S11&view_size=20".format(str(i))
    print(i)
    # 3) url 열고 bs4로 파싱 및 이미지 주소 얻기
    html = urlopen(url)
    soup = bs(html, "html.parser")
    a_lists = soup.select('p.tit a')    # 제목, url

    # 4) 페이지 내의 이미지 주소로부터 다운로드
    for list in a_lists:
        title = list.text  # title
        url = "https://www.bobaedream.co.kr" + list.attrs["href"]

        # 5) mariaDB 연결 - 제목/url 저장
        conn = pymysql.connect(host='34.64.176.78', port=3306,
                               db='mycar', user='root', password='admin1234',
                               charset='utf8')

        cursor = conn.cursor()
        sql = "insert into carphoto (title, url) values ('{}', '{}')".format(title, url)
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()