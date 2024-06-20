import re

def ContentParse(ContentData, NotFoundValue):
    print('시작')

    # 조건들을 동적으로 설정
    if NotFoundValue == '신청기간':
        conditions = ["접수기간", "신청기간", "근로기간", "원서접수", "공고기간", "모집기간", "접수일시", "접수기간 :", "원서접수 기간 :", "채용공고 기간 :", "제출 마감기한 :", "서류접수:", "공고(접수)기간", "기 간"]
    elif NotFoundValue == '사업명':
        conditions = ["사업명"]
    elif NotFoundValue == '근무지':
        conditions = ["근무지", "근무장소", "근 무 처 :", "근 무 지"]
    elif NotFoundValue == '임금조건':
        conditions = ["임금조건(보수)", "급여:", "보수", "일 급", "보수수준 :", "보 수 :", "급여내용:", "인부임", "보 수:"]
    elif NotFoundValue == '등록일':
        conditions = ["등록일"]
    elif NotFoundValue == '문의처':
        conditions = ["전화", "문 의 처", "☎", "문의", "문의처", "문 의 :", "문의 :", "기타 문의사항 :", "문의전화 :", "연 락 처:", "문의사항:"]
    else:
        return None  # 처리할 수 없는 값이 들어왔을 경우 None 반환

    # 선택된 조건에 따라 패턴 생성
    pattern = r'(' + r'|'.join([re.escape(cond) for cond in conditions]) + r')\s*[:：]?\s*(.*)'

    # 텍스트를 엔터 기준으로 자름
    lines = ContentData.split('\n')

    result = None

    # 각 라인을 패턴에 맞게 검사하여 값 추출
    for line in lines:
        match = re.match(pattern, line)
        if match:
            value = match.group(2).strip()
            result = value
            break  # 첫 번째 매칭된 값만 사용하므로 루프 종료

    return result
