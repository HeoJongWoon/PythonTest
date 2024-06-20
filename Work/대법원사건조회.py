import requests
from urllib.request import urlretrieve # 이미지 저장하는 라이브러리
import cv2 #이미지 불러오는 라이브러리
import time # 딜레이 라이브러리
from selenium import webdriver
import pandas as pd
import os
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By # 셀레니움 4.3 이상부터 동작 방식이 변경됨에 따라 By 사용법 숙지 필수
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup  # 지금은 안씀
import OCR
options = ChromeOptions()
""" 
백그라운드에서 열리는 크롬 설정
options = webdriver.ChromeOptions() 
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
"""
#options.add_experimental_option("detach", True) # 해당 옵션이 없으면 업무 종료 후 바로 꺼짐 주석 처리 추천. 테스트 할땐 주석 풀기

class Scrap :
    def __init__(self):
        self.index = 1
        self.df = self.read_df_file()
        self.page_inform = []
        for item in range(len(self.df)): 
            GroupResult = self.url_setting(item)
            if GroupResult == "사건없음":
                continue
            self.make_df_file()
        
    def temp(self):
        return("성공")
    
    
    def url_setting(self, item) : #페이지를 열고 그 후에 make_법원_dict()함수를 호출 
        while True: #캡챠 인식률이 낮기 때문에 만든 로직    
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            self.driver.implicitly_wait(3) # 암시적 대기 / 무작정 sleep 하는거보다 효율이 좋다   
            url = "https://www.scourt.go.kr/portal/information/events/search/search.jsp"  # 대법원 사이트 접속
            #driver = webdriver.Chrome(r"C:\Users\chromedriver.exe")  셀레니움 자체적으로 크롬드라이버를 지원해 준다. 이제 필요없는 코드
            self.driver.get(url)        
            #html = self.driver.page_source # 현재 페이지 내 Xpath 및 요소를 전부 가져온다. -> 그냥 iauto 쓰듯이 쓸 수 있어진다고 생각하면 됨 / 없어도 Xpath 사용가능 , BeautifulSoup용 코드
            #self.soup = BeautifulSoup(html, 'html.parser') # -> 마찬가지
            GroupResult = self.make_법원_dict(item)
            if GroupResult == "성공":
                break
            elif GroupResult == "사건없음":
                break
            else:
                #self.driver.quit()
                print(self.GroupResult)

        if GroupResult == "사건없음":
            return("사건없음")


    def make_법원_dict(self,item): # Xpath로 타이틀,회사,url를 수집
            #변수 선언
            사건번호 = self.df['사건번호1'][item]
            법원명 = self.df['법원명'][item]

            #iframe 요소로 변경 / 동작 확인
            content = self.driver.find_element(By.TAG_NAME,'iframe')
            self.driver.switch_to.frame(content)

            #사건번호입력모드 체크
            self.driver.find_element(By.XPATH,f'//*[@id="inputsano_ch"]').click()

            #for i in range(3): # 예외처리 안해도 되는거 같지만, 혹시 모르니 구현
            #    self.driver.find_element(By.XPATH,f'//*[@id="inputsano_ch"]').click()
            #    #time.sleep(1)                 
            #    GetText = self.driver.find_element(By.XPATH, f'//*[@id="div_sa_year"]').get_attribute("style") # 사건번호입력모드 체크되면 요소값이 사라짐
            #    if "none" in GetText: # GetText 내 'none'이란 글자 있는지 확인
            #        break
            #    else:
            #        time.sleep(1)

            # 법원명 선택
            Select(self.driver.find_element(By.XPATH, "//*[@id='sch_bub_nm']")).select_by_visible_text(법원명) #법원명 선택
            

            
            # 사건번호 입력
            self.driver.find_element(By.XPATH,f'//*[@id="div_input_sano"]/input').send_keys(사건번호) # 사건번호 입력
            #GetText = self.driver.find_element(By.XPATH, f'//*[@id="div_input_sano"]/input').text
            #GetText = self.soup.select_one('#tbody > tr > td > div:nth-child(5) > input').get

            #당사자명 입력(광주)
            self.driver.find_element(By.XPATH,f'//*[@id="ds_nm"]').send_keys("광주") # 사건번호 입력

            #캡챠 후 검색 클릭
            while True:                
                #캡챠 이미지 저장                
                try: # 너무 빨라서 요소 에러 나는듯?
                    captchaImage_element = self.driver.find_element(By.XPATH, f'//*[@id="captcha"]/img') # 캡챠할 요소를 변수에 담기
                    captchaImage = captchaImage_element.screenshot_as_png # 요소를 스크린샷하기
                    captchText = OCR.ReadImage(captchaImage)
                except:
                    print("너무 빠름")
                    time.sleep(1)
                    continue
                captchText = captchText.strip() # 개행 및 공백 제거
                print(captchText)
                #캡챠 입력
                self.driver.find_element(By.XPATH,f'//*[@id="answer"]').send_keys(captchText)
                #검색 버튼 클릭
                self.driver.find_element(By.XPATH,f'//*[@id="tab1"]/form[1]/table/tbody/tr/td/div[12]/a').click()
                try:
                    #캡챠 입력 실패시 타는 곳 / 그전까지 실패는 없다고 가정 -> 원래 예외 처리 있었는데 귀찮아서 다 뺌 ㅎ (return "성공", "실패" 구조로 만들었음)
                    alert = self.driver.switch_to.alert
                    
                    print(alert.text)
                    if "올바른" in alert.text:
                        return("사건없음")
                    alert.dismiss()
                    #캡챠 새로고침 클릭
                    self.driver.find_element(By.XPATH,f'//*[@id="tab1"]/form[1]/table/tbody/tr/td/div[9]/a').click()
                    #캡챠 입력란에 있는 값 삭제
                    self.driver.find_element(By.XPATH,f'//*[@id="answer"]').clear()
                    #return("실패")
                except:
                    print("성공")
                    #return("실패")
                    break

            #테이블 수집
            table = self.driver.find_element(By.XPATH, f'//*[@id="subTab1"]/table[1]')
            heads = table.find_elements(By.TAG_NAME,"th")
            body = table.find_elements(By.TAG_NAME,"td")
            법원_dict = {name.text:value.text for name,value in zip(heads,body)}
            [법원_dict.pop(key) for key in ['사건명','재판부','회생위원','채권이의마감일','보존여부','송달료,보관금 종결에 따른 잔액조회']] # 필요없는 컬럼(키) 삭제
            print(법원_dict)
            self.page_inform.append(법원_dict)
            return("성공")


    def make_df_file(self): # 수집된 정보들을 엑셀에 추가
        tempcolumns=['사건번호', '접수일', '채무자', '개시결정일', '변제계획인가일', '면책결정일', '절차폐지결정일', '종국결과']
        tempdf = pd.DataFrame(self.page_inform) # 엑셀 컬럼명 수정 금지  columns = tempcolumns
        print("df","="*50,"\n",self.df)
        print("tempdf","="*50,"\n",tempdf)
        
        totaldf = pd.concat([self.df,tempdf],axis=1)
        print(totaldf)

        totaldf.to_excel('./개인회생_사건번호_기초데이터.xlsx')
        totaldf.to_csv('./개인회생_사건번호_기초데이터.csv')
        self.index += 1

    def read_df_file(self):
        tempusecols=['사건번호1','법원명','사건번호', '접수일', '채무자', '개시결정일', '변제계획인가일', '면책결정일', '절차폐지결정일', '종국결과']
        df= pd.read_excel('./개인회생_사건번호_기초데이터.xlsx',usecols=['사건번호1','법원명']) # 안되면 추가하기 usecols=tempusecols
        return df


if __name__ == "__main__" :
    print("웹크롤링 작업을 시작합니다.")
    News = Scrap()
    print("웹크롤링 작업을 종료합니다.")


 