'''
    재상이가 짜준 option 가져오는 함수 (imgcrawling6.py에서 가져다 사용했음)
'''


from selenium import webdriver
import time, os, csv
from bs4 import BeautifulSoup

driver = webdriver.Chrome('./webdriver/chromedriver')
driver.implicitly_wait(1)

driver.get('https://www.bobaedream.co.kr/mycar/mycar_view.php?no=2041523&gubun=I')
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
options = soup.select('.radioBox')

option_num_string = ""

for option in zip(options):
    if 'checked' in str(option):
        option_num_string += "1"
    else:
        option_num_string += "0"

print(option_num_string[:14])
print(option_num_string[14:31])
print(option_num_string[31:49])
print(option_num_string[49:66])
print(option_num_string[66:78])

