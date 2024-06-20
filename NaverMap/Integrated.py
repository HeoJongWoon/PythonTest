from selenium import webdriver  # Selenium WebDriver를 사용하기 위해 import
from bs4 import BeautifulSoup  # BeautifulSoup을 사용하여 HTML을 파싱하기 위해 import
import pandas as pd  # Pandas를 사용하여 Excel 파일을 처리하기 위해 import
from os.path import expanduser  # 사용자 홈 디렉토리를 찾기 위해 expanduser를 import
from selenium.webdriver.common.by import By  # Selenium에서 요소를 찾기 위해 By를 import
from selenium.webdriver.chrome.service import Service as ChromeService  # ChromeDriver 서비스를 사용하기 위해 import
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriver를 자동으로 설치하기 위해 import
from selenium.webdriver.chrome.options import Options  # Chrome 옵션을 설정하기 위해 import

def FindRoadName():
    # 사용자 홈 디렉토리에서 엑셀 파일 경로 설정
    FilePath = f"{expanduser('~')}\\Desktop\\회사명 리스트.xlsx"
    
    # 엑셀 파일에서 검색어 읽기
    Df = pd.read_excel(FilePath, sheet_name='Sheet1')
    CompanyNameList = Df['회사명'].tolist()  # '회사명' 열의 모든 값을 리스트로 변환
    
    # 도로명 주소 리스트 초기화
    RoadNameList = []

    # Chrome WebDriver 인스턴스 생성
    options = Options()
    options.add_argument("--headless=new")  # 브라우저를 표시하지 않음 (New headless mode)
    options.add_argument("--disable-gpu")  # GPU 가속 사용 중지
    options.add_argument("--no-sandbox")  # 샌드박스 사용 중지
    options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 중지
    options.add_argument("--disable-software-rasterizer")  # 소프트웨어 래스터라이저 사용 중지
    options.add_argument("window-size=1920x1080")  # 화면 크기 설정
    options.add_argument("--log-level=3")  # 로그 레벨 설정 (경고 및 오류만 표시)
    
    # ChromeDriver 인스턴스를 생성하고 설정된 옵션을 적용
    Driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # 각 회사명을 순회하면서 주소를 검색
    for CompanyName in CompanyNameList:
        try:
            # 네이버 지도에서 회사명 검색
            Url = f"https://pcmap.place.naver.com/place/list?query={CompanyName}"

            # 웹 페이지 열기
            Driver.get(Url)

            # 페이지 로딩을 위해 5초 대기
            Driver.implicitly_wait(5)

            # 도로명 주소 펼치기 (첫 번째 검색 결과의 도로명 주소를 클릭)
            Driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/div/div/div/span[2]/a/span[1]').click()

            # 페이지 소스 가져오기
            Soup = BeautifulSoup(Driver.page_source, 'html.parser')

            # 도로명 주소 요소 찾기
            RoadNameElements = Soup.select_one('span.MN3sj')
            RoadName = RoadNameElements.find_next_sibling(text=True).get_text(strip=True) if RoadNameElements else '검색결과가 없습니다.'

            # 도로명 주소를 리스트에 추가
            RoadNameList.append(RoadName.strip() if RoadName else '검색결과가 없습니다.')
        except Exception as e:
            print(f"오류 발생: {e}")
            RoadNameList.append('검색결과가 없습니다.')
    
    # WebDriver 종료
    Driver.quit()

    # 결과를 DataFrame에 추가
    Df['도로명 주소'] = RoadNameList

    # 수정된 DataFrame을 새로운 Excel 파일로 저장
    Df.to_excel(FilePath, index=False)

    print("성공")

# 함수 실행
FindRoadName()