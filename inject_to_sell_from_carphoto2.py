'''
    배기량,보증기간,연료,변속기,판매자,사진폴더까지url 정보를 sell 테이블에 입력
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

sell_sql = "select sell_id,image from sell"
cursor.execute(sell_sql)
idxurl = cursor.fetchall()

cnt = 1
for idx,url in idxurl:
    carphoto_sql = "SELECT baeki,guarantee,fuel,gear,seller,photourl FROM carphoto WHERE photourl='{}'".format(url)
    cursor.execute(carphoto_sql)
    datas = cursor.fetchall()
    print(cnt)

    for baeki,guarantee,fuel,gear,seller,photourl in datas:
        inject_sql = "UPDATE sell SET baeki='{}',guarantee='{}',fuel='{}',gear='{}',seller='{}' WHERE image='{}'".format(baeki,guarantee,fuel,gear,seller,url)
        cursor.execute(inject_sql)
        conn.commit()
    cnt = cnt + 1

cursor.close()
conn.close()
print('완료')

