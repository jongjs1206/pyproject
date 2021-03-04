'''
    차량명에 해당하는 옵션 정보(op1,op2,op3,op4,op5를 option 테이블에 입력
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

sell_sql = "select sell_id, option from sell where default_info is null"
cursor.execute(sell_sql)
idxoption = cursor.fetchall()

for idx,option in idxoption:
    print(idx)
    options = option.split('/')
    option_sql = "INSERT INTO option VALUES ({},'{}','{}','{}','{}','{}')".format(idx,options[0],options[1],options[2],options[3],options[4])
    try:
        print(option_sql)
        cursor.execute(option_sql)
    except:
        print('옵션X로 해당행 생략')
        option_sql2 = "INSERT INTO option (sell_id) VALUES '{}'".format(idx)
        cursor.execute(option_sql2)
        conn.commit()
    else:
        conn.commit()

cursor.close()
conn.close()
print('완료')

