# TVS Diode Internal Physics During 8kV ESD Event
## (What Actually Happens Inside the Silicon)

---

# 1. Introduction

This document explains what physically happens inside a TVS (Transient Voltage Suppressor) diode
when an 8kV ESD pulse is applied.

The explanation follows:

- IEC 61000-4-2 standard
- 8kV contact discharge model
- Nanosecond-level time sequence
- Semiconductor physics perspective

---

# 2. 8kV ESD Pulse Characteristics

According to IEC 61000-4-2 (Contact Discharge):

- Peak Current ≈ 30A
- Rise Time ≈ 0.7 ~ 1ns
- Pulse Duration ≈ 30 ~ 60ns

This means:

A very high current (tens of amperes) is injected within 1 nanosecond.

---

# 3. Time-Sequence of Internal Events

---

## t = 0 ~ 0.5ns
### Electric Field Build-Up

- 8kV appears across the TVS terminals.
- Electric field inside the depletion region increases rapidly.
- The peak electric field approaches the critical field (Ecrit).

At this moment, current is still minimal.

---

## t ≈ 1ns
### Avalanche Breakdown Initiation

When the electric field reaches Ecrit:

- Free electrons accelerate.
- High-energy electrons collide with lattice atoms.
- Impact ionization occurs.
- Electron-hole pairs multiply rapidly.

This process is called:

Carrier Avalanche Multiplication.

Current increases exponentially.

---

## t = 1 ~ 5ns
### High Current Conduction Mode

The TVS enters low dynamic resistance mode.

- Tens of amperes flow.
- Voltage across the device clamps near the clamp voltage (Vc).

Clamp voltage relationship:

V_clamp = V_BR + I_PP × R_d

Where:

- V_BR = Breakdown voltage
- I_PP = Peak pulse current
- R_d = Dynamic resistance

The protected IC now sees a limited voltage
instead of the original 8kV.

---

## t = 5 ~ 50ns
### Heat Generation Phase

Instantaneous power:

P = V × I

Example:

20V × 30A = 600W

Although 600W is extremely high,
the pulse duration is very short.

Energy absorbed:

Energy = Power × Time

600W × 30ns = 18µJ

This energy is small enough to be absorbed
by the silicon junction without destruction.

---

## t > 50ns
### Recovery Phase

- The surge current decays.
- Avalanche multiplication stops.
- The device returns to high impedance state.

If within rating limits,
the TVS fully recovers without damage.

---

# 4. What Physically Happens Inside the Silicon

During conduction:

1. Avalanche carrier multiplication occurs.
2. A plasma-like high carrier density region forms.
3. The depletion region temporarily collapses.
4. The junction behaves almost like a low-resistance conductor.
5. Local heating occurs in the active region.

TVS devices are designed to survive this repeatedly.

---

# 5. Why TVS Survives but Regular Diode Fails

TVS Structure Advantages:

- Large junction area
- Optimized doping profile
- Thick epi layer
- Guard ring structure
- Improved thermal spreading
- Low dynamic resistance

Regular diodes:

- Small junction
- Not optimized for surge
- Severe current crowding
- Hotspot formation
- Thermal runaway
- Junction melting

Breakdown in regular diodes = Failure

Breakdown in TVS = Normal operation mode

---

# 6. Energy Perspective

Even though current is very high:

Energy is what determines damage.

ESD event energy (tens of µJ)
is much lower than:

- 10/1000µs surge pulses
- Lightning surge events

TVS is designed to absorb
short high-current spikes safely.

---

# 7. Key Engineering Parameters

When selecting a TVS:

- V_BR (Breakdown voltage)
- V_C (Clamp voltage)
- I_PP (Peak pulse current)
- P_PP (Peak pulse power)
- TLP curve data
- Dynamic resistance

---

# 8. Final Summary

When 8kV ESD hits a TVS:

1. Electric field rises rapidly.
2. Avalanche breakdown starts.
3. Tens of amperes conduct within nanoseconds.
4. Voltage is clamped to safe level.
5. Energy is absorbed as heat.
6. Device returns to normal state.

TVS is essentially:

"A silicon shield designed to absorb nanosecond lightning strikes."

---

END