import time
import pandas as pd
from os.path import expanduser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_roadname():
    # 사용자 홈 디렉토리에서 엑셀 파일 경로 설정
    file_path = f"{expanduser('~')}\\Desktop\\회사명 리스트.xlsx"
    
    # 엑셀 파일에서 검색어 읽기
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    companynamelist = df['회사명'].tolist()
    
    # 도로명 주소 리스트 초기화
    roadnamelist = []

    # Selenium WebDriver 설정
    options = Options()
    options.add_argument("--headless=new")  # 브라우저를 표시하지 않음 (New headless mode)
    options.add_argument("--disable-gpu")  # GPU 가속 사용 중지
    options.add_argument("--no-sandbox")  # 샌드박스 사용 중지
    options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 중지
    options.add_argument("--disable-software-rasterizer")  # 소프트웨어 래스터라이저 사용 중지
    options.add_argument("window-size=1920x1080")  # 화면 크기 설정
    options.add_argument("--log-level=3")  # 로그 레벨 설정 (경고 및 오류만 표시)
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    for companyname in companynamelist:
        # 네이버 지도에서 회사명 검색
        url = f"https://map.naver.com/v5/search/{companyname}"
        driver.get(url)
        
        try:
            # 검색 결과 iframe으로 전환
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe"))
            )
            
            # 도로명 주소 요소 찾기
            roadname_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span.Pb4bU'))
            )
            roadname_text = roadname_element.text
            roadnamelist.append(roadname_text)
        except Exception as e:
            print(f"오류 발생: {e}")
            roadnamelist.append('검색결과가 없습니다.')
        
        # 기본 콘텐츠로 돌아가기
        driver.switch_to.default_content()
        time.sleep(1)

    driver.quit()

    # 도로명 주소 리스트 출력
    print(*roadnamelist, sep='\n')
    
    # 결과를 DataFrame에 추가
    df['도로명 주소'] = roadnamelist

    # 수정된 DataFrame을 저장
    df.to_excel(file_path, index=False)

    print("성공")

find_roadname()