# Planar MOS PCell – Technology-Agnostic Structure

Planar MOS PCells have historically been effective
for testchip and PCM applications,
especially in mature technology nodes.

Their strength lies in parameterized geometry generation
that allows rapid sweep of width, length, and spacing.

## Typical Structure

User Parameters → Geometry Generation → DRC Check


## Strengths

- Simple parameter model (W/L)
- Easy automation
- Suitable for PCM and early characterization

## Fundamental Limitations

- Continuous width is assumed
- Heavy reliance on OPC to fix geometry
- Limited scalability below 14nm

In planar technologies, OPC can often compensate for poor layout choices.
This assumption no longer holds for FinFET and beyond.

## Key Takeaway

> Planar PCells are geometry-driven.
> Advanced-node PCells must be topology-driven.

This realization motivates the transition
from planar MOS PCells to FinFET-aware PCell architectures.

