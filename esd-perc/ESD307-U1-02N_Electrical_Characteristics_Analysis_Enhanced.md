# Infineon ESD307-U1-02N Electrical Characteristics 심화 분석

(면접 대비 + 회로적 의미까지 정리)

------------------------------------------------------------------------

# 1. Reverse Leakage 그래프 깊이 해석

### 그래프 의미 (IR vs VR)

데이터시트 Figure 4-1 기준:

-   0V \~ 10V 구간에서 IR은 약 10\^-11 \~ 10\^-10 A 수준
-   10V 근처에서도 급격히 증가하지 않음

### 물리적 의미

Reverse leakage는 다음에 의해 결정됩니다:

-   Depletion region thermal generation
-   Junction area
-   온도 의존성 (Arrhenius 특성)

IR은 대략:

    IR ≈ IS * exp(-qV/kT)

이 값이 매우 작다는 것은:

✔ 공정 품질이 좋음\
✔ Junction defect density 낮음\
✔ 배터리 소모 거의 없음

------------------------------------------------------------------------

# 2. Capacitance (CL) 그래프 깊이 해석

### Figure 4-2 (CL vs VR)

-   VR = 0V → 약 270 pF
-   VR 증가 시 → 약 100 pF까지 감소

이는 전형적인 PN junction depletion capacitance 특성입니다.

공식:

    Cj = Cj0 / sqrt(1 + VR / Φ)

즉,

-   Reverse bias 증가 → depletion width 증가
-   C 감소

### 회로적 의미

270 pF는 상당히 큰 값입니다.

신호 라인에서:

    Zc = 1 / (2π f C)

예를 들어 100 MHz에서:

    Zc ≈ 1 / (2π × 10^8 × 270×10^-12)
       ≈ 5.9 Ω

즉, 고속 신호에서는 거의 단락처럼 동작

👉 그래서 USB VBUS 전원 보호용이지\
👉 USB 3.x 데이터 라인용은 아님

------------------------------------------------------------------------

# 3. TLP Curve (Figure 4-7) 깊이 해석

TLP는 quasi-static I-V 곡선입니다.

그래프 특징:

-   약 12V 부근에서 breakdown 시작
-   Snapback 없이 monotonic 증가
-   기울기 일정 → RDYN ≈ 0.05Ω

이는 avalanche-diode 기반 TVS 구조임을 의미

### 수식적으로 보면

Clamping 영역에서:

    VCL = VBR + I × RDYN

예:

I = 30A RDYN = 0.05Ω

전압 상승분:

    ΔV = I × RDYN
       = 30 × 0.05
       = 1.5V

즉,

전류가 30A 증가해도 전압은 1.5V만 증가

→ 매우 우수한 클램핑 성능

------------------------------------------------------------------------

# 4. Dynamic Resistance 0.05Ω의 회로적 의미

## 정의

    RDYN = dV/dI

이는 ESD 중 TVS의 등가 직렬 저항과 유사

## 실제 회로에서 의미

회로 모델:

    TVS ≈ Ideal Clamp Voltage + RDYN

즉,

    Vprotected = VBR + I_ESD × RDYN

만약 RDYN이 1Ω이라면:

30A × 1Ω = 30V 상승

하지만 0.05Ω이면:

30A × 0.05Ω = 1.5V 상승

차이:

30V vs 1.5V

👉 downstream IC 보호에 결정적 차이

------------------------------------------------------------------------

# 5. Surge 8/20µs 곡선 해석

Figure 4-8:

-   34A에서 VCL ≈ 24V

즉,

    24V = 12V + (34A × RDYN_effective)

이 값은 TLP보다 높음

왜?

-   펄스 폭이 더 길어 열 효과 존재
-   Transient thermal impedance 영향

------------------------------------------------------------------------

# 6. Overshoot 파형 해석 (8kV / 15kV IEC)

초기 피크:

-   8kV → 35V
-   15kV → 64V

이는:

-   패키지 기생 인덕턴스
-   측정 fixture 영향
-   di/dt × L 효과

수식:

    V_overshoot = L × di/dt

rise time이 빠를수록 overshoot 증가

------------------------------------------------------------------------

# 7. 전체 종합 해석

이 제품은:

✔ Avalanche 기반 구조\
✔ 낮은 RDYN (0.05Ω) → 강력한 클램핑\
✔ 비교적 큰 C (270pF) → 전원 라인 전용\
✔ IEC ±30kV 대응

즉,

"고속 데이터 보호용"이 아니라\
"전원 rail 보호용 high-current TVS"

------------------------------------------------------------------------

# 8. 면접용 고급 정리 멘트

"ESD307-U1-02N은 avalanche 기반 TVS로, TLP 기준 dynamic resistance가
0.05Ω로 매우 낮아 대전류 인가 시에도 전압 상승이 거의 없다는 점이
핵심입니다. 반면 270pF의 비교적 높은 junction capacitance를 가지므로
고속 신호 라인보다는 USB VBUS와 같은 전원 라인 보호에 적합합니다."

------------------------------------------------------------------------

작성 목적: TVS 제품 물리적 이해 및 회로적 해석 심화 정리
