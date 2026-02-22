import pandas as pd

# 180nm BCD IP 분석을 위한 표준 테스트 데이터
data = {
    'Corner': ['TT_27', 'FF_125', 'SS_-40', 'TT_27', 'FF_125', 'SS_-40'],
    'Temp': [27, 125, -40, 27, 125, -40],
    'Vdd': [1.62, 1.62, 1.62, 1.98, 1.98, 1.98],
    'Vref_Avg': [1.245, 1.230, 1.260, 1.255, 1.240, 1.270],
    'Current_nA': [100, 120, 90, 110, 130, 95],
    'SOA_Status': ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS']
}

df = pd.DataFrame(data)
# index=False 옵션으로 불필요한 열을 제거하고 저장
df.to_csv('sim_summary.txt', index=False)
print("성공: 표준 형식의 sim_summary.txt 파일이 재생성되었습니다.")