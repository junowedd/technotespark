# TVS Diode Lab Characterization 경험 정리

## 1. Controlled Snapback Behavior 유지 방법

### 1) Snapback 주요 파라미터

-   **Vt1 (Trigger Voltage)**
-   **Vh (Holding Voltage)**
-   **It2 (Failure Current)**

Snapback은 Breakdown 이후 전압이 감소하면서 전류가 증가하는 영역이며,
Parasitic BJT Turn-on과 Self-heating 효과가 핵심 메커니즘이다.

------------------------------------------------------------------------

### 2) Layout & Geometry Control

-   Guard ring 최적화
-   Well spacing control
-   Ballasting resistance 균일화
-   Finger width 균일성 유지
-   Current crowding 방지 → Local thermal runaway 방지

------------------------------------------------------------------------

### 3) Process Variation Control

-   Junction depth uniformity
-   Implant dose 균일성
-   Silicide block 영역 관리
-   공정 편차 최소화 → Vt1 / Vh 변동 억제

------------------------------------------------------------------------

### 4) Thermal Stability 확보

-   Electro-thermal TCAD simulation 수행
-   Lattice temperature peak 분석
-   TLP pulse width 조건 비교 (100ns vs 1µs 등)
-   Heat spreading metal 확보
-   Thermal runaway margin 확보

------------------------------------------------------------------------

### 5) TLP 기반 Characterization

-   Transmission Line Pulse (TLP)
-   VF-TLP

확인 항목: - Vt1 variation - Vh collapse 여부 - Multi-trigger 현상 - It2
extraction

------------------------------------------------------------------------

## 2. Leakage Limit 유지 방법

### 1) Leakage 발생 원인

-   Surface leakage
-   Junction leakage
-   Trap-assisted tunneling
-   Silicide spiking
-   Edge electric field crowding

------------------------------------------------------------------------

### 2) Surface Trap Control

Surface trap은 Si--SiO₂ interface에서 발생하는 interface states(Dit)로,
Trap-assisted generation 및 leakage 증가의 원인이 된다.

#### 개선 방법

-   고품질 Passivation (SiO₂ / SiN)
-   Plasma damage 최소화
-   Field plate 적용 → Edge field 완화
-   Multi guard ring 구조 적용
-   Silicide block edge control
-   TCAD에서 Dit sweep 분석

------------------------------------------------------------------------

### 3) 신뢰성 시험 기반 관리

-   HTOL (High Temp Operating Life)
-   HTRB (High Temp Reverse Bias)
-   온도별 Leakage 측정 (25°C / 85°C / 125°C)

Leakage는 온도 의존성이 매우 큼.

------------------------------------------------------------------------

## 3. DUT에 DC Pulse 인가 방법 및 사용 툴

### 1) 장비 기반 방법

-   SMU Pulse Mode (Keysight B1500, Keithley 4200 등)
-   Curve Tracer
-   TLP 장비

------------------------------------------------------------------------

### 2) EDA / Simulation Tool

#### 1) TCAD (Electro-thermal Simulation)

-   Snapback 물리 해석
-   Lattice temperature 분포 분석
-   Thermal runaway 예측

#### 2) Layout & Verification Tool

-   Schematic / PEX / LVS
-   DRC 및 ESD rule check

------------------------------------------------------------------------

## 4. Repetitive Surge Stress 시험

### 1) 시험 목적

-   Degradation 확인
-   Soft failure 검출
-   Lifetime 예측
-   Wear-out mechanism 분석

------------------------------------------------------------------------

### 2) 대표 파형

-   IEC 61000-4-5 (8/20 µs)
-   10/1000 µs Surge

------------------------------------------------------------------------

### 3) 시험 조건 예시

-   10 \~ 1000 shots 반복 인가
-   Shot 간 10\~60 sec interval
-   온도 안정화 시간 확보

------------------------------------------------------------------------

### 4) 평가 항목

-   Vbr shift
-   Leakage 증가 여부
-   Clamping voltage 상승
-   Dynamic resistance 변화
-   It2 감소 여부

------------------------------------------------------------------------

## 5. 추가 심화 질문 정리

### 1) Self-heating Simulation Tool 종류

-   Synopsys Sentaurus (Electro-thermal coupling)
-   Silvaco Atlas
-   COMSOL Multiphysics (Package 포함 Multiphysics 해석)

------------------------------------------------------------------------

### 2) Thermal Runaway 메커니즘

-   Joule heating 증가
-   Temperature 상승 → Carrier mobility 감소
-   Impact ionization 증가
-   Local hot spot 형성 → Snapback collapse

------------------------------------------------------------------------

### 3) TLP vs DC Self-heating 차이

-   DC: Steady-state heating
-   TLP: Short pulse transient heating
-   VF-TLP: 매우 빠른 rise time → 실제 ESD 상황에 근접

------------------------------------------------------------------------

### 4) Automotive Grade 고려사항

-   AEC-Q101 기준 충족
-   더 엄격한 Leakage spec
-   더 높은 반복 surge 요구 조건
-   고온 환경에서의 안정성 확보

------------------------------------------------------------------------

# 면접용 핵심 정리 문장

> Snapback은 Parasitic BJT와 Self-heating에 의해 결정되며,
> Electro-thermal TCAD와 TLP characterization을 통해 안정성을
> 확보합니다.\
> Leakage는 주로 Junction edge 및 Surface trap에 의해 지배되므로 Guard
> ring, Passivation, Interface trap density 제어가 핵심입니다.\
> Repetitive surge stress는 Degradation margin 및 장기 신뢰성 확보를
> 위한 필수 시험입니다.
