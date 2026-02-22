import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # GUI 에러 방지
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Monte Carlo 샘플 데이터 생성 (데이터가 없을 경우를 대비)
def generate_mc_data():
    np.random.seed(42)
    # 1.25V 기준, 표준편차 10mV의 가우시안 분포 생성 (1000개 샘플)
    mc_data = np.random.normal(loc=1.250, scale=0.010, size=1000)
    df_mc = pd.DataFrame({'Iteration': range(1, 1001), 'Vref': mc_data})
    df_mc.to_csv('mc_summary.txt', index=False)
    print("--- Monte Carlo 샘플 데이터(mc_summary.txt) 생성 완료 ---")

generate_mc_data() # 테스트용 데이터 생성

# 2. 데이터 로드 및 통계 계산
df = pd.read_csv('mc_summary.txt')
vref = df['Vref']

mean = np.mean(vref)
std = np.std(vref)
usl = 1.250 + 0.030 # Upper Spec Limit (1.28V)
lsl = 1.250 - 0.030 # Lower Spec Limit (1.22V)

# 수율(Yield) 계산: Spec 내에 들어오는 샘플 비율
yield_count = len(df[(df['Vref'] >= lsl) & (df['Vref'] <= usl)])
yield_pct = (yield_count / len(df)) * 100

# 3. 히스토그램 및 정규분포 곡선 시각화
plt.figure(figsize=(10, 6))
sns.histplot(vref, kde=True, color='skyblue', stat='density', label='MC Samples')

# Spec 라인 및 통계 지표 표시
plt.axvline(lsl, color='red', linestyle='--', linewidth=2, label=f'LSL ({lsl}V)')
plt.axvline(usl, color='red', linestyle='--', linewidth=2, label=f'USL ({usl}V)')
plt.axvline(mean, color='green', linestyle='-', linewidth=2, label=f'Mean ({mean:.3f}V)')

# 텍스트 박스에 통계 결과 표시
stats_text = f'Mean: {mean:.4f}V\nStd Dev: {std:.4f}V\nYield: {yield_pct:.1f}%\nTarget: 1.250V'
plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

plt.title('180nm BCD IP: Monte Carlo Yield Analysis (Vref)', fontsize=15)
plt.xlabel('Reference Voltage (Vref) [V]')
plt.ylabel('Density')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# 그래프 저장
plt.savefig('mc_analysis_plot.png', dpi=300)
print(f"--- 분석 완료: Yield = {yield_pct:.1f}%, 결과가 'mc_analysis_plot.png'에 저장되었습니다. ---")
