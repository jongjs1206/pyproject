'''
    3단계
    각 페이지에서 제목/연식/배기량/주행거리/색상/변속기/보증정보/연료/ 정보를 DB에 입력
'''

# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from google.cloud import storage as gcs
import os, pymysql, time

conn = pymysql.connect(host='34.64.176.78', port=3306,
                       db='mycar', user='root', password='admin1234',
                       charset='utf8')

cursor = conn.cursor()
# sql = "select idx, url from carphoto"
sql = "select idx,url from intercar where old is null"
cursor.execute(sql)
urls = cursor.fetchall()

for idxurl in urls:
    # 차량 각 상세페이지 열기
    idx,url = idxurl
    print(idx)
    html = urlopen(url)
    # time.sleep(1)
    soup = bs(html, "html.parser")
    # time.sleep(1)
    tds = soup.select('div.info-basic div.tbl-01 tr>td')

    update_sql = "update intercar set old='{}',baeki='{}',mile='{}',color='{}',gear='{}',guarantee='{}',fuel='{}' where url='{}'".format(
        tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, url)
    cursor.execute(update_sql)
    time.sleep(1)
    conn.commit()


cursor.close()
conn.close()
print('완료')


