# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from google.cloud import storage as gcs
import os, pymysql, time


conn = pymysql.connect(host='34.64.176.78', port=3306,
                       db='mycar', user='root', password='admin1234',
                       charset='utf8')

cursor = conn.cursor()
carphoto_sql = "select idx, car_num, title, w_date, old, mile, color, accident, price, photourl, content, url from carphoto"
cursor.execute(carphoto_sql)
datas = cursor.fetchall()

for idx, car_num, title, w_date, old, mile, color, accident, price, photourl, content, url in datas:
    print(idx)
    sell_sql = """insert into sell (sell_id, g_id, m_id, 
                    title, w_date, old, mile, color, 
                    accident, price, image, content, url) 
                    values (nextval(sell_sell_id_sq), '{}', 'user2', 
                    '{}', '{}', '{}', '{}', '{}',
                    '{}', '{}', '{}', '{}', '{}' )""".format(int(car_num), title, w_date, old, mile, color,
                                                             accident, int(price), photourl, content,url)
    try:
        cursor.execute(sell_sql)
    except:
        print('에러발생 : ', idx, '열 삭제처리')
        delete_sql = "delete from carphoto where idx='{}'".format(idx)
        # cursor.execute(delete_sql)
        # conn.commit()
    else:
        conn.commit()



cursor.close()
conn.close()
print('완료')
