# Parasitic Inductance (L) – Fundamentals

## Definition

Inductance is a physical property that resists changes in current.

\[
V = L \frac{dI}{dt}
\]

- Unit: Henry (H)
- Energy stored:
\[
E = \frac{1}{2} L I^2
\]

---

## Why It Matters in ESD

ESD has very high current slew rate:

- IEC rise time ≈ 1 ns
- dI/dt can reach 10–30 A/ns

Example:

L = 5 nH  
dI/dt = 10 A/ns  

\[
V = 50V
\]

Even small inductance creates large overshoot.

---

## Typical Values

| Structure | Approx. L |
|------------|----------|
| Bond wire | 1 nH/mm |
| PCB via | 0.5–1 nH |
| Package loop | 5–20 nH |
