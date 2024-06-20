import pandas as pd  # Pandas를 사용하여 Excel 파일을 처리하기 위해 import
from os.path import expanduser  # 사용자 홈 디렉토리를 찾기 위해 expanduser를 import

def WriteExcel(RoadNameList):
    # 사용자 홈 디렉토리에서 엑셀 파일 경로 설정
    FilePath = f"{expanduser('~')}\\Desktop\\회사명 리스트.xlsx"
    
    # 엑셀 파일에서 검색어 읽기
    Df = pd.read_excel(FilePath, sheet_name='Sheet1')  # 엑셀 파일의 'Sheet1'에서 데이터 읽기
    
    # 결과를 DataFrame에 추가
    Df['도로명 주소'] = RoadNameList  # DataFrame에 '도로명 주소' 열 추가 또는 업데이트

    # 수정된 DataFrame을 새로운 Excel 파일로 저장
    Df.to_excel(FilePath, index=False)  # 변경된 DataFrame을 원래 파일 경로에 저장

    return '성공'  # 작업 완료 메시지 반환

# 메인 실행 블록
if __name__ == "__main__":
    WriteExcel()  # 함수 실행, 단 RoadNameList 매개변수가 필요함