# Junction Capacitance vs Breakdown Voltage  
## 왜 반비례 관계가 되는가? (물리적 설명)

---

# 1. 문제 정의

PN 접합에서

- **Junction Capacitance (Cj, 접합 커패시턴스)**
- **Breakdown Voltage (Vbr, 항복 전압)**

는 실험적으로 서로 반비례 관계(정확히는 제곱근 반비례)를 가진다.

즉,

Cj ↑ → Vbr ↓  
Cj ↓ → Vbr ↑  

왜 이런 관계가 나타나는지 반도체 물리 관점에서 유도한다.

---

# 2. 공핍층(Depletion Region) 물리

역바이어스 PN 접합에서 공핍층 두께 W는 Poisson 방정식을 풀면 다음과 같이 주어진다.

\[
W = \sqrt{\frac{2\varepsilon_s}{q} \cdot \frac{(V_{bi}+V_R)}{N_{eff}}}
\]

where:

- εs : 반도체 유전율
- q : 전자 전하
- Vbi : Built-in potential
- VR : 역바이어스 전압
- Neff : 유효 도핑 농도

핵심 관계:

\[
W \propto \sqrt{\frac{V}{N}}
\]

즉,

- 도핑 농도 N ↑ → W ↓
- 전압 V ↑ → W ↑

---

# 3. Junction Capacitance 유도

접합 커패시턴스는 평행판 커패시터와 동일하게 정의된다.

\[
C_j = \frac{\varepsilon_s A}{W}
\]

W 식을 대입하면:

\[
C_j = A \sqrt{\frac{q\varepsilon_s N_{eff}}{2(V_{bi}+V_R)}}
\]

정리하면:

\[
C_j \propto \sqrt{\frac{N}{V}}
\]

즉,

- 도핑 ↑ → Cj ↑
- 전압 ↑ → Cj ↓

---

# 4. Breakdown Voltage 유도

Avalanche breakdown 조건:

최대 전기장이 임계 전기장 Ecrit에 도달할 때 항복이 발생한다.

최대 전기장:

\[
E_{max} = \frac{q N W}{\varepsilon_s}
\]

Breakdown 조건:

\[
E_{max} = E_{crit}
\]

이를 정리하면:

\[
V_{br} \propto \frac{E_{crit}^2 \varepsilon_s}{q N}
\]

즉,

\[
V_{br} \propto \frac{1}{N}
\]

결론:

- 도핑 ↑ → Vbr ↓
- 도핑 ↓ → Vbr ↑

---

# 5. 두 식을 결합

이미 얻은 관계:

\[
C_j \propto \sqrt{N}
\]

\[
V_{br} \propto \frac{1}{N}
\]

N을 제거하면:

\[
C_j \propto \frac{1}{\sqrt{V_{br}}}
\]

따라서,

**Junction Capacitance는 Breakdown Voltage에 대해 제곱근 반비례 관계를 가진다.**
Junction capacitance is inversely proportional to the square root of the breakdown voltage.

---

# 6. 물리적 직관

## 도핑이 높은 경우 (Low Vbr 소자)

- 공핍층 얇음
- 전기장 강함
- 낮은 전압에서 항복
- 정전용량 큼

→ Low breakdown, High capacitance

---

## 도핑이 낮은 경우 (High Vbr 소자)

- 공핍층 두꺼움
- 전기장 분산
- 높은 전압에서 항복
- 정전용량 작음

→ High breakdown, Low capacitance

---

# 7. 핵심 요약

모든 것은 **도핑 농도 N** 이 결정한다.

- Cj ∝ √N
- Vbr ∝ 1/N

따라서

\[
C_j \propto \frac{1}{\sqrt{V_{br}}}
\]

즉,

**Breakdown Voltage가 증가하면 Junction Capacitance는 감소한다.**

---

# 8. 엔지니어링 의미

- 전원 보호용 TVS → 낮은 Vbr, 높은 Cj
- 고속 데이터 보호 → 높은 Vbr, 매우 낮은 Cj
- RF 보호 → 극저 Cj (< 1 pF)

설계자는 도핑과 공핍층 구조를 조절하여 이 트레이드오프를 설계한다.

---

# END