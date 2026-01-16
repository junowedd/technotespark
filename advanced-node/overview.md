# Advanced-Node Layout Architecture

Below 14nm, layout design is no longer about drawing shapes.
It is about **constraining degrees of freedom** to ensure
manufacturability, yield, and predictable OPC convergence.

In advanced technology nodes, many geometries that are DRC-clean
are fundamentally non-manufacturable.
Therefore, the role of layout automation and PCells
must shift from geometry generation
to **encoding manufacturing intent**.

## Architectural View

User Parameters
↓
Topology Definition
↓
Technology Rules (PDK)
↓
DFM / OPC Guards
↓
Layout Geometry


A well-designed PCell does not rely on post-layout fixes.
Instead, it prevents invalid structures from being generated in the first place.

> **Good layout architecture removes freedom, not adds it.**
