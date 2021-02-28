'''
    4단계
    각 페이지에서 사진 파일을 스토리지 버킷에 입력
'''

# 1) 필요한 라이브러리 import
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from google.cloud import storage as gcs
import os, pymysql, time


# 2) 다운받은 json파일로 인증키 설정
gcs_client = gcs.Client.from_service_account_json(json_credentials_path='./gcs/sachawon-2d1766dc97cd.json')
# 3) 사용할 버킷 지정
bucket = gcs_client.get_bucket('car_image_for_analysis')

# 4) 보배드림 사이트에서 차량 상세페이지 주소 가져오기
conn = pymysql.connect(host='34.64.176.78', port=3306,
                       db='mycar', user='root', password='admin1234',
                       charset='utf8')

cursor = conn.cursor()
sql = "select idx,url from carphoto where photourl is null"
cursor.execute(sql)
urls = cursor.fetchall()

bucket_url = ''

# 5) url 열고 bs4로 파싱 및 이미지 주소 얻기
for idxurl in urls:
    idx,url = idxurl
    print("idx : ", idx)
    # print(url)
    html = urlopen(url)
    soup = bs(html, "html.parser")
    imgs = soup.select('ul#imgPos a')

    # 6) 페이지 내의 이미지 주소로부터 다운로드
    carnum = 1        # 파일명에 사용할 변수 img1.png
    for i in imgs:
        href = i.attrs['href']
        img = href.replace('//','https://')
        # 완성되는 이미지파일의 주소 형식
        # https://file2.bobaedream.co.kr/pds/CyberCar/6/737606/img_737606_0.jpg

        # 7) 파일을 저장할 폴더 생성 (url의 no에 해당하는 숫자로 생성)
        # ex) https://www.bobaedream.co.kr/mycar/mycar_view.php?no=2096317&gubun=K 의 경우
        # 폴더명 : 2096317
        dirname = './bobaeC/'+url[-15:-8]+'/'
        # print(dirname)
        savedir = os.path.dirname(dirname)
        if not os.path.exists(savedir):
            os.makedirs(savedir)

        # 8) 특정 이름으로 이미지 저장 (사진이 404일 경우 저장하지 않고 다음장으로 넘어감)
        try:
            with urlopen(img) as f:
                f.read()
        except:
            print('에러발생 : ', img)
        else:
            with urlopen(img) as f:
                with open(dirname + 'img' + str(carnum) + '.png', 'wb' ) as h:
                    car = f.read()
                    h.write(car)

            # 9) gcs 버킷에 저장될 객체명
            file_name = url[-15:-8]+'/img{}.png'.format(carnum)
            # print('버킷에 저장될 객체명 : ', file_name)
            object_name = bucket.blob(file_name)
            # print(file_name)

            # 10) 버킷에 저장될 로컬 파일 (8에서 지정했음)
            upload_file = '{}img{}.png'.format(dirname, carnum)
            # print(upload_file)
            object_name.upload_from_filename(upload_file)

        # 11) 버킷에 저장된 파일의 url
        bucket_url = "https://storage.googleapis.com/car_image_for_analysis/" + url[-15:-8]+'/'

        carnum += 1

    # 12) DB의 carphoto 테이블에 photourl을 저장
    print(bucket_url)
    update_sql = "UPDATE carphoto SET photourl='{}' where idx={}".format(bucket_url,idx)
    cursor.execute(update_sql)
    conn.commit()



cursor.close()
conn.close()
print('완료')
