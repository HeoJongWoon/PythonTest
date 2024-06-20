import pandas as pd  # Pandas를 사용하여 Excel 파일을 처리하기 위해 import

def ReadExcel(FilePath):
    # 엑셀 파일에서 검색어 읽기
    Df = pd.read_excel(FilePath, sheet_name='Sheet1')  # 엑셀 파일의 'Sheet1'에서 데이터 읽기

    return Df  # 데이터 반환

# 메인 실행 블록
if __name__ == "__main__":
    ReadExcel()  # 함수 실행, 반환된 값은 사용하지 않음