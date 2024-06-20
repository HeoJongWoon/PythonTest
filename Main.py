from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import ContentParsing

def Main():
      options = Options()
      options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
      options.add_argument('--disable-gpu')  # GPU 비활성화

      # ChromeDriver 인스턴스를 생성하고 설정된 옵션을 적용
      Driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

      Url = "https://www.ddm.go.kr/www/selectBbsNttView.do?key=208&bbsNo=42&nttNo=149003&searchCtgry=&searchCnd=SJ&searchKrwd=%eb%aa%a8%ec%a7%91&integrDeptCode=&pageIndex=1"

      Driver.get(Url)

      # 페이지 로딩을 위해 5초 대기
      Driver.implicitly_wait(5)

      # 페이지 내용을 가져옴
      ContentElement = Driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[2]/table/tbody')
      Content = ContentElement.text  # WebElement에서 텍스트 추출

      Value = ContentParsing.ContentParse(Content, '신청기간')
      print(Value)

Main()