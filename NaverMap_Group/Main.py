import ReadExcel  # ReadExcel 모듈을 import
import WriteExcel  # WriteExcel 모듈을 import

import time  # 시간 관련 기능을 사용하기 위해 import
import pandas as pd  # Pandas를 사용하여 Excel 파일을 처리하기 위해 import
from os.path import expanduser  # 사용자 홈 디렉토리를 찾기 위해 expanduser를 import
import requests  # HTTP 요청을 보내기 위해 import
from bs4 import BeautifulSoup  # BeautifulSoup을 사용하여 HTML을 파싱하기 위해 import


def Main():
    # 사용자 홈 디렉토리에서 엑셀 파일 경로 설정
    FilePath = f"{expanduser('~')}\\Desktop\\회사명 리스트.xlsx"
    # 엑셀 파일에서 회사명 리스트 읽기
    Df = ReadExcel.ReadExcel(FilePath)  # ReadExcel 모듈의 ReadExcel 함수를 호출하여 회사명 리스트를 읽어옴
    CompanyNameList = Df['회사명'].tolist()  # '회사명' 열의 모든 값을 리스트로 변환
    RoadAddressList = Df['도로명 주소'].tolist() # '도로명 주소' 열의 모든 값을 리스트로 변환
    
    # 도로명 주소 리스트 초기화
    RoadNameList = []

    # HTTP 요청 시 사용할 헤더 설정
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 각 회사명과 도로명 주소를 순회하면서 주소를 검색
    for idx, (CompanyName, RoadAddress) in enumerate(zip(CompanyNameList, RoadAddressList)):
        StripCompanyName = str(CompanyName).strip()  # 회사명의 앞뒤 공백 제거
        StripRoadAddress = str(RoadAddress).strip()  # 도로명 주소의 앞뒤 공백 제거
        Num = idx + 1  # 인덱스 번호 1부터 시작

        # 인덱스와 함께 회사명 출력
        print("\n" + "-"*75)
        print(f"[{Num}번째] 회사명: {StripCompanyName}")
        print("-"*75+"\n")

        # 회사명이 비어있는 경우 또는 NaN인 경우 '검색결과가 없습니다.' 추가 후 다음 검색어로 넘어감
        if pd.isna(CompanyName) or StripCompanyName == '':
            RoadNameList.append('검색결과가 없습니다.')
            print(f"[{Num}번째] 회사명이 없으므로 다음 검색어로 넘어갑니다.")
            continue

        # 이미 도로명 주소가 있는 경우 해당 값을 리스트에 추가 후 다음 검색어로 넘어감
        if not pd.isna(RoadAddress) and StripRoadAddress != '':
            if StripRoadAddress != '검색결과가 없습니다.':
                RoadNameList.append(RoadAddress)
                print(f"[{Num}번째] 도로명 주소 값이 이미 있으므로 다음 검색어로 넘어갑니다.")
                continue

        # 네이버 지도에서 회사명 검색
        Url = f"https://pcmap.place.naver.com/place/list?query={CompanyName}"
        
        try:
            # 페이지 HTML 가져오기
            Response = requests.get(Url, headers=Headers)  # HTTP GET 요청 보내기
            Response.raise_for_status()  # 요청이 성공했는지 확인

            # BeautifulSoup으로 HTML 파싱
            Soup = BeautifulSoup(Response.content, 'html.parser')

            # 도로명 주소 찾기
            RoadNameElement = Soup.select_one('span.Pb4bU')  # 도로명 주소가 포함된 요소 선택

            if RoadNameElement:
                RoadNameText = RoadNameElement.text.strip()  # 공백 제거 및 텍스트 가져오기
                RoadNameList.append(RoadNameText)  # 도로명 주소 리스트에 추가
                print(f"[{Num}번째] 도로명 주소: {RoadNameText}")
            else:
                RoadNameList.append('검색결과가 없습니다.')  # 도로명 주소를 찾지 못한 경우
                print(f"[{Num}번째] 검색결과가 없습니다.")
        except Exception as e:
            print(f"[{Num}번째] 오류 발생: {e}")
            RoadNameList.append('검색결과가 없습니다.')  # 오류 발생 시 '검색결과가 없습니다.' 추가
    
    # 수집한 도로명 주소 엑셀 파일에 저장
    Result = WriteExcel.WriteExcel(RoadNameList)  # WriteExcel 모듈의 WriteExcel 함수를 호출하여 수집한 도로명 주소를 엑셀 파일에 저장
    print(Result)  # 저장 결과를 출력

    return Result  # 저장 결과를 반환

# 시작 시간 저장
start = time.time()

# 메인 실행 블록
if __name__ == "__main__":
    Main()  # Main 함수 실행

# 실행 시간 출력
print(f"업무 실행 시간: {int(time.time() - start)} 초")