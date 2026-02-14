# Low-Impedance State vs Inductance

## Low-Impedance State

Occurs when a protection device (SCR, BJT) turns on.

\[
Z = \frac{V}{I}
\]

After snapback:
- Voltage decreases
- Current increases
- Impedance becomes small

---

## Inductance

\[
V = L \frac{dI}{dt}
\]

Inductance generates voltage when current changes rapidly.

---

## Key Difference

| Low-Impedance | Inductance |
|--------------|------------|
| Device state | Physical parameter |
| Nonlinear | Linear (in most cases) |
| Controls conduction | Controls transient voltage |

---

## Interaction

\[
V_{total} = V_{device} + L \frac{dI}{dt}
\]

Even if device is in low-impedance state, inductance adds overshoot.
