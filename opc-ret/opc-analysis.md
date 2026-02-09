# OPC Bottlenecks in FinFET Layout

In advanced nodes, OPC challenges are rarely isolated.
They arise from **interacting constraints** that amplify variability.

## 1. Gate Cut × Gate × Fin Interaction

Gate cuts define effective gate length.
Their interaction with fins is one of the most difficult
patterns for OPC to stabilize.

- Gate-end pullback
- CD non-uniformity across fins
- Vt and leakage variation

## 2. Fin Pitch Quantization

Fin pitch is fixed and discrete.
OPC loses most of its corrective freedom.

- Edge fin thinning
- Pitch walking
- Limited assist feature placement

## 3. Fin Termination at Active Edges

Fin ends near active boundaries create strong line-end effects.

- Asymmetric etch behavior
- Source/drain resistance variation

## 4. Contact and Via Density Effects

Contacts interact with local fin density.
OPC behavior becomes density-driven rather than local.

## 5. PCM Structures vs Product Structures

PCM patterns intentionally stress the process.
If not isolated, they destabilize OPC models.

## Core Insight

> In advanced nodes, OPC difficulty is usually a design problem,
> not a tool problem.

Well-designed PCells reduce OPC complexity
by removing problematic degrees of freedom.

