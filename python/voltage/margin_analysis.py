import matplotlib
matplotlib.use('Agg') # 화면을 띄우지 않는 백엔드 설정 (TclError 방지)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ... 기존 코드 ...

# plt.show() 대신 저장만 수행
plt.savefig('voltage_margin_plot.png', dpi=300)
print("성공: 그래프가 'voltage_margin_plot.png'로 저장되었습니다.")


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드 (이전 단계에서 생성된 데이터)
try:
    df = pd.read_csv('sim_summary.txt')
except FileNotFoundError:
    print("데이터 파일이 없습니다. 먼저 시뮬레이션을 실행하세요.")
    exit()

# 2. 성능 지표 분석 (예: 목표 전압 대비 마진 계산)
target_vref = 1.25
spec_limit = 0.05  # +/- 5% 허용 오차
df['Vref_Error'] = df['Vref_Avg'] - target_vref
df['Upper_Limit'] = target_vref * (1 + spec_limit)
df['Lower_Limit'] = target_vref * (1 - spec_limit)

# 3. 전압 마진 시각화 (Schmoo Plot 스타일 또는 Line Plot)
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")

# 온도별로 색상을 나누어 전압 변화에 따른 Vref 추이 시각화
plot = sns.lineplot(data=df, x='Vdd', y='Vref_Avg', hue='Temp', marker='o', palette='viridis')

# Spec Limit 가이드라인 추가 (빨간 점선)
plt.axhline(target_vref * 1.05, color='red', linestyle='--', label='Upper Spec (5%)')
plt.axhline(target_vref * 0.95, color='red', linestyle='--', label='Lower Spec (5%)')
plt.axhline(target_vref, color='blue', linestyle='-', alpha=0.3, label='Target')

# 그래프 디테일 설정
plt.title('180nm BCD IP: Vref Voltage Margin Analysis', fontsize=15)
plt.xlabel('Supply Voltage (Vdd) [V]', fontsize=12)
plt.ylabel('Reference Voltage (Vref) [V]', fontsize=12)
plt.legend(title='Temperature [℃]', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()


# 그래프 저장 및 출력
plt.savefig('voltage_margin_plot.png', dpi=300)
print("그래프가 'voltage_margin_plot.png'로 저장되었습니다.")

plt.savefig("margin_plot.png", dpi=300)

# 4. 분석 요약 통계 출력
summary = df.groupby('Temp')['Vref_Avg'].agg(['min', 'max', 'mean'])
print("\n--- Temperature Corner Summary ---")
print(summary)