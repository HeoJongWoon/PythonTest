import os

windows_user_name = os.path.expanduser('~')

import pandas as pd

# 변수 지정
department = 'iauto'
name = '허종운'

# 엑셀 파일 읽기
file_path = (f'{windows_user_name}//Desktop//리스트.xlsx')
df = pd.read_excel(file_path)

# 행 개수 확인
row_count = len(df)

# '부서'와 '이름' 컬럼에 값 입력
df.loc[row_count, '부서'] = department
df.loc[row_count, '성명'] = name

# 수정된 데이터를 엑셀 파일로 저장
df.to_excel(file_path, index=False)