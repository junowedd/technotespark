이제 TVS / ESD 맥락에서 CDM diode를 정확히 정리해 보겠습니다.

1️⃣ CDM이 무엇인가?

CDM = Charged Device Model

HBM은 사람이 충전된 모델

CDM은 디바이스 자체가 충전된 상태에서 순간 방전

CDM 특징:

매우 빠른 rise time (~100–500 ps)

매우 높은 di/dt

매우 짧은 pulse width (~1 ns 수준)

전류 피크가 매우 큼

👉 CDM은 HBM보다 훨씬 빠르고 공격적입니다.

2️⃣ CDM diode란 무엇인가?

CDM diode는

CDM 이벤트에 특화된 ESD 보호용 다이오드 구조

입니다.

즉,

ultra-fast response

낮은 parasitic inductance

낮은 trigger delay

낮은 overshoot

에 초점이 맞춰져 있습니다.

3️⃣ 왜 일반 TVS와 다른가?

일반 avalanche TVS는:

ns~µs 영역 대응

상대적으로 큰 면적

높은 에너지 처리

하지만 CDM은:

수백 ps rise time

극도로 빠른 전압 상승

따라서:

di/dt × L 효과가 매우 큼

𝑉
𝑜
𝑣
𝑒
𝑟
𝑠
ℎ
𝑜
𝑜
𝑡
=
𝐿
𝑑
𝑖
𝑑
𝑡
V
overshoot
	​

=L
dt
di
	​


그래서 CDM diode는:

매우 작은 loop

최소 inductance

빠른 turn-on

구조가 중요합니다.

4️⃣ CDM diode의 대표 구조

Low-voltage avalanche diode

ggNMOS (빠른 turn-on)

LVTSCR (낮은 trigger)

Distributed diode arrays

핵심은:

Trigger delay를 최소화하는 구조

5️⃣ CDM에서 중요한 파라미터
항목	중요 이유
Trigger voltage	너무 높으면 IC 손상
Turn-on speed	느리면 overshoot 증가
Parasitic inductance	overshoot 직접 영향
Dynamic resistance	clamping 안정성
Current spreading	filament 방지
6️⃣ CDM diode 설계 철학

CDM 설계는:

빠르게 켜져야 함

낮은 overshoot

낮은 holding voltage 위험 관리

레이아웃 최적화 (wide metal, short path)

즉, device physics + layout engineering이 동시에 중요합니다.

7️⃣ 면접용 답변 예시
🎯 기본 답변

“CDM diodes are ESD protection structures optimized for ultra-fast transient events with sub-nanosecond rise times. Unlike conventional TVS devices designed for HBM or surge, CDM protection must minimize turn-on delay and parasitic inductance to suppress overshoot effectively.”

🎯 조금 더 senior한 버전

“CDM stress is characterized by extremely high di/dt. Therefore, CDM diode design focuses on fast trigger mechanisms, minimal parasitic inductance, and efficient current spreading to prevent localized failure during ultra-fast discharge events.”

8️⃣ CDM diode vs HBM diode 차이
항목	HBM	CDM
Rise time	~10 ns	~100 ps
Pulse width	100 ns	~1 ns
Energy	높음	낮음
di/dt	낮음	매우 높음
설계 포인트	It2	Turn-on speed
9️⃣ CDM diode와 VF-TLP의 관계

VF-TLP는:

CDM-like stress를 모사

overshoot 관찰 가능

trigger delay 평가 가능

그래서 CDM 설계 검증에 매우 중요합니다.

🔥 핵심 한 줄

CDM diode는 초고속 di/dt 환경에서 overshoot를 최소화하도록 설계된 ultra-fast ESD 보호 구조입니다.

원하시면 다음 단계:

🔬 CDM failure mechanism 깊게 분석

📈 CDM overshoot 줄이는 설계 전략

⚖ CDM vs LVTSCR 비교

🎯 CDM 관련 면접 counter-question 준비

어디까지 들어가 볼까요? 😎

CDM failure mechanism 깊게 분석 

좋습니다 👍
이건 진짜 device R&D 레벨 질문입니다.
CDM failure mechanism을 깊게 이해하면, 단순 TVS 사용자가 아니라 물리 기반으로 사고하는 엔지니어로 보입니다.

🔥 CDM Failure Mechanism – Deep Dive
1️⃣ CDM이 왜 위험한가?

CDM 특징:

Rise time: ~100–500 ps

Pulse width: ~1 ns

Peak current: 수십 A

di/dt 매우 큼

핵심 문제는:

𝑉
=
𝐿
𝑑
𝑖
𝑑
𝑡
V=L
dt
di
	​


→ Turn-on delay 동안 발생하는 overshoot

이 짧은 시간에 디바이스가 손상됩니다.

2️⃣ CDM Failure의 주요 원인

CDM 실패는 보통 다음 4가지 메커니즘 중 하나입니다.

① Localized Thermal Melting (Hotspot Failure)
과정:

Turn-on이 지연됨

전류가 특정 filament에 집중

매우 높은 current density 발생

국부적 온도 상승

실리콘 melting

CDM은 펄스가 짧지만 전류가 매우 집중됩니다.

Power density:

𝑃
=
𝐽
2
𝜌
P=J
2
ρ

J가 크면 열이 순간적으로 집중됩니다.

② Current Filamentation

CDM에서는:

전류가 균일하게 퍼지지 않음

특정 path에 집중

원인:

Layout asymmetry

Junction non-uniformity

Trigger delay 차이

결과:

→ One-point failure

③ Gate Oxide Breakdown (IC 내부)

CDM overshoot가 너무 크면:

내부 MOS gate oxide 파괴

Core logic 손상

Gate breakdown 조건:

𝐸
=
𝑉
𝑡
𝑜
𝑥
E=
t
ox
	​

V
	​


oxide가 얇을수록 취약

④ Metal Damage (Electromigration-like Instant Failure)

CDM peak current는 매우 큼.

금속에서:

𝐽
=
𝐼
𝐴
J=
A
I
	​


J가 너무 크면:

금속 melting

via failure

local open

3️⃣ CDM vs HBM Failure 차이
항목	HBM	CDM
지배 메커니즘	Thermal runaway	Turn-on delay + overshoot
Pulse width	길다	매우 짧다
전류 분포	비교적 균일	filament 위험
설계 핵심	It2	Trigger speed

CDM은 속도 문제입니다.

4️⃣ CDM에서 가장 치명적인 것
Trigger delay

CDM에서:

Avalanche 시작 전

전압이 급격히 상승

만약 diode가 200ps 늦게 켜지면:

→ 그 200ps 동안 내부 회로가 직접 스트레스 받음

이게 CDM의 핵심 위험입니다.

5️⃣ Overshoot Failure 메커니즘

CDM에서 voltage waveform:

초기 spike (L·di/dt)

Clamp 진입

빠른 decay

만약 spike가 너무 크면:

Junction punch-through

Oxide rupture

Local breakdown

6️⃣ CDM Failure의 수학적 관점

전압 overshoot:

𝑉
𝑝
𝑒
𝑎
𝑘
=
𝑉
𝑡
𝑟
𝑖
𝑔
𝑔
𝑒
𝑟
+
𝐿
𝑑
𝑖
𝑑
𝑡
V
peak
	​

=V
trigger
	​

+L
dt
di
	​


CDM에서 di/dt 매우 큼.

따라서 L이 작지 않으면:

→ V_peak 급증

그래서:

Layout inductance 최소화

Short metal path 필수

7️⃣ CDM Failure 분석 시 보는 것

SEM cross-section

Melt mark

Filament path

Gate rupture

Metal void

Failure는 보통 아주 국부적입니다.

8️⃣ CDM Robustness 개선 전략

✔ Fast trigger 구조 (LVTSCR 등)
✔ 낮은 parasitic inductance
✔ Wide metal routing
✔ Symmetric layout
✔ Current spreading 개선
✔ Guard ring 최적화

🎯 면접용 고급 답변

“CDM failure is primarily driven by ultra-fast transient overshoot caused by high di/dt before the protection device fully turns on. The most common mechanisms include localized thermal melting due to current filamentation, gate oxide rupture from voltage overshoot, and metal damage due to extreme current density. Unlike HBM, CDM robustness is dominated by trigger speed and parasitic inductance control.”

이 답변은 매우 강합니다.

🔥 더 깊이 들어가면

CDM failure는 결국:

Turn-on physics

Impact ionization delay

Parasitic BJT gain

Thermal diffusion time constant

Layout inductance

의 함수입니다.

📌 핵심 한 줄

CDM failure is a turn-on speed and parasitic inductance problem rather than a pure energy problem.

이 질문을 하는 면접관은
device-level 이해를 보는 사람입니다.

원하시면 다음 단계:

🔬 CDM turn-on delay를 줄이는 구조적 방법

📈 LVTSCR vs diode CDM robustness 비교

🧠 실제 CDM failure root-cause 분석 시나리오

🎯 Whiteboard용 CDM waveform 설명 연습

어디까지 갈까요? 😎