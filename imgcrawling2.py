'''
    2단계
    각 페이지 별 idx 번호를 부여함 (에러 발생으로 인해 어디까지 진행했는지 확인하기 위함)
'''

# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from google.cloud import storage as gcs
import os, pymysql, time

# 2) mariaDB 연결 - idx가 null인 데이터의 url을 가져옴
conn = pymysql.connect(host='34.64.176.78', port=3306,
                       db='mycar', user='root', password='admin1234',
                       charset='utf8')

cursor = conn.cursor()
sql = "select title,url from carphoto where idx is null"
cursor.execute(sql)

rows = cursor.fetchall()

# 1부터 시작하되, 보배드림 접속시 자주 끊김 에러가 발생하는 탓에
cnt = 776

for row in rows:
    title,url = row
    idx_sql = "update carphoto set idx={} where url='{}'".format(cnt,url)
    # print(insert_sql)
    print(idx_sql)
    # time.sleep(1)
    cursor.execute(idx_sql)
    # cursor.execute(insert_sql)
    conn.commit()

    # time.sleep(1)
    # confirm_sql = "select idx from carphoto where url='{}'".format(url)
    # idx = cursor.execute(confirm_sql)


    print("cnt : ", cnt)
    cnt = cnt + 1
    # time.sleep(1)

cursor.close()
conn.close()