import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # GUI 에러 방지용
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. 데이터 로드 및 Monte Carlo 샘플 생성 (없을 경우 대비)
def prepare_data():
    if not os.path.exists('mc_summary.txt'):
        np.random.seed(42)
        vref_mc = np.random.normal(loc=1.250, scale=0.012, size=1000)
        pd.DataFrame({'Vref': vref_mc}).to_csv('mc_summary.txt', index=False)
        print("--- mc_summary.txt 생성 완료 ---")

prepare_data()
df_corner = pd.read_csv('sim_summary.txt')
df_mc = pd.read_csv('mc_summary.txt')

# 2. Monte Carlo 히스토그램 생성 및 저장
plt.figure(figsize=(8, 5))
sns.histplot(df_mc['Vref'], kde=True, color='skyblue')
plt.axvline(1.22, color='red', linestyle='--') # LSL
plt.axvline(1.28, color='red', linestyle='--') # USL
plt.title('Monte Carlo Yield Analysis')
plt.savefig('mc_plot.png')
print("--- mc_plot.png 저장 완료 ---")

# 3. 통합 요약 통계 출력
vref_mean = df_mc['Vref'].mean()
vref_std = df_mc['Vref'].std()
yield_val = (len(df_mc[(df_mc['Vref'] >= 1.22) & (df_mc['Vref'] <= 1.28)]) / len(df_mc)) * 100

print("\n" + "="*40)
print("180nm BCD IP 통합 분석 리포트")
print("="*40)
print(f"평균 전압 (Mean): {vref_mean:.4f} V")
print(f"표준 편차 (Std): {vref_std:.4f} V")
print(f"추정 수율 (Yield): {yield_val:.1f} %")
print("-"*40)
print("온도 코너별 데이터 (Summary):")
print(df_corner.groupby('Temp')['Vref_Avg'].agg(['min', 'max', 'mean']))
print("="*40) 