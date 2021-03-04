'''
    6단계
    최조등록 날짜, 사고이력, 옵션, 내용
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
sql = "select idx,url from intercar where option is null"
cursor.execute(sql)
urls = cursor.fetchall()

for idxurl in urls:
    # 차량 각 상세페이지 열기
    idx,url = idxurl
    print("idx : ", idx)
    html = urlopen(url)
    soup = bs(html, "html.parser")

    datas = soup.select('div.gallery-data dd')
    w_date = ''
    try:
        write_data = datas[2].text
    except:
        delete_sql = "delete from intercar where idx='{}'".format(idx)
        cursor.execute(delete_sql)
        conn.commit()
        print(idx, '삭제')
    else:
        w_date = write_data.split('최초등록 ')[1]   # 21/01/05  -- 최초등록날짜

    thtd_tmp = ''
    try:
        insnum = soup.select_one('div.info-insurance b').text  # 보험처리 횟수 n회
    except:
        print('idx {} 보험처리 횟수 인식 불가')
    else:
        ths = soup.select('div.info-insurance th')
        tds = soup.select('div.info-insurance td')
        thtd_tmp = "보험처리=" + insnum + "회"
        for th,td in zip(ths,tds):
            thtd_tmp = thtd_tmp + '+' + th.text + '=' + td.text
    # print(thtd_tmp)

    txt = ''
    try:
        txt = soup.select_one('div.explanation-box').text   # 내용
    except:
        print(idx, '에서 txt에러 발생')
    else:
        txt = soup.select_one('div.explanation-box').text.replace("'","/")  # 내용

    options = soup.select('.radioBox')
    option_num_string = ""

    for option in zip(options):
        if 'checked' in str(option):
            option_num_string += "1"
        else:
            option_num_string += "0"

    op1 = option_num_string[:14]
    op2 = option_num_string[14:31]
    op3 = option_num_string[31:49]
    op4 = option_num_string[49:66]
    op5 = option_num_string[66:78]

    option_i = op1 + "/" + op2 + "/" + op3 + "/" + op4 + "/" + op5

    insert_sql = "UPDATE intercar SET accident='{}', w_date='{}', option='{}', content='{}' WHERE idx='{}'".format(thtd_tmp,w_date,option_i,txt,idx)
    # print(insert_sql2)
    cursor.execute(insert_sql)
    conn.commit()

cursor.close()
conn.close()
print('완료')
