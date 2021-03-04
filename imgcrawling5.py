'''
    5단계
    각 페이지에서 제목/가격/판매자명을 DB에 저장
    한글은 int 타입 컬럼에 입력불가한 관계로,
    판매완료는 0, 계약은 1로 저장함
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
sql = "select idx,url from intercar where price is null"
cursor.execute(sql)
urls = cursor.fetchall()

for idxurl in urls:
    # 차량 각 상세페이지 열기
    idx,url = idxurl
    print("idx : ", idx)
    html = urlopen(url)
    soup = bs(html, "html.parser")
    title = soup.select_one('div.title-area h3.tit').text
    price = soup.select_one('div.price-area b').text.replace(',','')
    seller = soup.select_one('div.seller-data div.seller-state b').text

    if price=='[판매완료]':
        update_sql = "UPDATE intercar SET title='{}',price=0,seller='{}' where idx={}".format(title, seller,idx)
    elif price=='[계약]':
        update_sql = "UPDATE intercar SET title='{}',price=1,seller='{}' where idx={}".format(title, seller, idx)
    elif price=='[가격상담]':
        update_sql = "UPDATE intercar SET title='{}',price=2,seller='{}' where idx={}".format(title, seller, idx)
    elif price=='[보류]':
        update_sql = "UPDATE intercar SET title='{}',price=3,seller='{}' where idx={}".format(title, seller, idx)
    else:
        update_sql = "UPDATE intercar SET title='{}',price={},seller='{}' where idx={}".format(title,price,seller,idx)
    print(update_sql)
    cursor.execute(update_sql)
    conn.commit()

cursor.close()
conn.close()
print('완료')


