'''
    7단계
    차종에 따른 grade 테이블 상의 g_id 확인 및 carphoto 테이블에 입력(car_num 컬럼)
'''

import pymysql,time

def selectDB(name):

    # 통로 연결
    # conn = pymysql.connect(host='34.64.176.78', port=3306,
    #                        db='mycar', user='root', password='admin1234',
    #                        charset='utf8')
    # print('연결성공')
    # cursor = conn.cursor()

    nameslice = name.split(' ')
    jejosa = nameslice[0]
    if jejosa == 'GM대우':
        jejosa = '쉐보레/대우'
    elif jejosa == '쉐보레':
        jejosa = '쉐보레/대우'

    sql = "select g.g_id,c.model, d.detail, g.grade1, g.grade2 from detail d inner join  (select * from category where jejosa='{}') c, grade g where c.car_num=d.car_num and  d.d_id=g.d_id".format(jejosa)
    cursor.execute(sql)

    nameslice = nameslice[1:]
    rows = cursor.fetchall()
    # print(nameslice)

    temps = []
    for row in rows:
        temp = []
        # print('row', row)
        for word in row:
            word_temp = str(word).split('(')[0]
            temp.append(word_temp)
        temps.append(temp)

    result = []
    for oneslice in nameslice:
        re_temp = []
        for tp in temps:
            for t in tp[1:]:
                if oneslice in t:
                    re_temp.append(tp)
                    break
        result = re_temp
        if len(re_temp) > 1:
            temps = re_temp
        if len(re_temp) == 1:
            break
    # print(result)

    # cursor.close()
    # conn.close()
    return result[0][0]
    # return 0
###############

conn = pymysql.connect(host='34.64.176.78', port=3306,
                       db='mycar', user='root', password='admin1234',
                       charset='utf8')
cursor = conn.cursor()
name_sql = "select title from carphoto where car_num is null"
cursor.execute(name_sql)
names = cursor.fetchall()

cnt = 1
for carname in names:
    print(carname[0])
    try:
        numnum = selectDB(carname[0])
    except:
        delete_sql = "delete from carphoto where title='{}'".format(carname[0])
        cursor.execute(delete_sql)
        conn.commit()
        print(carname[0], '삭제')
    else:
        numnum = selectDB(carname[0])
        print(numnum)
        insert_carnum_sql = "UPDATE carphoto SET car_num='{}' WHERE title='{}'".format(numnum,carname[0])
        cursor.execute(insert_carnum_sql)
        conn.commit()
    print('cnt : ', cnt)
    cnt = cnt+1

# name = "기아 더 뉴 K9 3.3 GDI 이그제큐티브"
# name = "GM대우 윈스톰 맥스 HDLX 5인승 4WD 최고급형"
# name = "쉐보레 더 넥스트 스파크 1.0 LT 플러스"
# name = "르노삼성 QM6 2.0 GDe 2WD RE 시그니처"
# num = selectDB(name)
# print(num)

cursor.close()
conn.close()

print('완료')