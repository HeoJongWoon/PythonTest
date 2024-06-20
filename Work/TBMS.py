from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# 전 영업일 구하기
today = datetime.today()
previous_date = today - timedelta(1)
while True :
    if previous_date.weekday() < 5 :
        break
    else:
        previous_date = previous_date - timedelta(1)
previous_date = previous_date.strftime("%Y-%m-%d")
# 계정정보 할당
id = "rpa.emailbot@inzisoft.com"
pw = "rpaemail1942"
#브라우저 옵션 설정
#options = webdriver.ChromeOptions()



options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
# TBMS 접속
driver = webdriver.Chrome(options)
driver.get("https://tbms.mobileleader.com:8010/login")
driver.implicitly_wait(5)
#로그인
driver.find_element(By.ID, 'plainUserId').send_keys(id)
driver.find_element(By.ID, 'plainUserPw').send_keys(pw)
driver.find_element(By.ID, 'plainUserPw').send_keys(Keys.ENTER)
#전 영업일 조회
driver.find_element(By.ID, 'wrkDd').send_keys(previous_date)
driver.find_element(By.ID, 'wrkDd').send_keys(Keys.ENTER)
driver.find_element(By.ID, 'wrkDd').send_keys(Keys.ENTER)
#조회 결과 테이블 수집
soup = BeautifulSoup(driver.page_source, 'html.parser') #현재 페이지 소스 수집
columns = soup.find_all(class_ = 'hdrcell') #컬럼 수집
column_list = []
for column in columns :
    column_list.append(column.text.strip())
print(column_list)
table = soup.find_all(class_ = 'objbox')