import os

windows_user_name = os.path.expanduser('~')

import pandas as pd

# 엑셀 파일의 두 번째 시트 읽기
file_path = (f'{windows_user_name}//Desktop//리스트.xlsx')
sheet_name = 'Sheet2'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# '값' 컬럼의 데이터를 변수에 저장
values = df['값'].tolist()

# '값' 컬럼의 첫 번째 데이터 할당
value = values[0]

# 입력한 층 수의 피라미드 출력
for i in range(1, int(value) + 1):
    print(' ' * (int(value) - i) + '*' * (2 * i - 1))