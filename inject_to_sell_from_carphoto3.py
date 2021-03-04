'''
    옵션 정보와 차량번호(임의생성함)를 sell 테이블에 입력

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

sell_sql = "select sell_id,image from sell where option is null"
cursor.execute(sell_sql)
conn.commit()
idxurl = cursor.fetchall()

cha = 3000
cnt = 1
for idx,url in idxurl:
    carphoto_sql = "SELECT idx,option,photourl FROM intercar WHERE photourl='{}'".format(url)
    cursor.execute(carphoto_sql)
    conn.commit()
    datas = cursor.fetchall()
    # print(cnt)

    for idx2,option,photourl in datas:
        cha = int(cha) + int(idx2)
        chanum = str(cha)[1:3] + '가' + str(cha)[:4]  # 임의의 차량번호 생성
        inject_sql = "UPDATE sell SET option='{}', vehicle_num='{}' WHERE image='{}'".format(option,chanum,photourl)
        cursor.execute(inject_sql)
        conn.commit()
        print(inject_sql)
    cnt = cnt + 1

cursor.close()
conn.close()
print('완료')

