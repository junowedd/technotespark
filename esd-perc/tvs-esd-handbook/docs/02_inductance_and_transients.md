# 2. Parasitic Inductance & Transient Overshoot

## Inductance Definition

\[
V = L \frac{dI}{dt}
\]

Energy:

\[
E = \frac{1}{2} L I^2
\]

---

## ESD Slew Rate

IEC 61000-4-2:

- Rise time ≈ 1 ns
- High \( dI/dt \)

Example:

L = 5 nH  
dI/dt = 15 A/ns  

\[
V = 75V
\]

---

## Practical Sources of L

| Source | Typical Value |
|--------|---------------|
| Bond wire | 1 nH/mm |
| Package loop | 5–20 nH |
| PCB trace | 0.8–1 nH/mm |
