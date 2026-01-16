# FinFET PCell Architecture for 12nm and Below

FinFET devices fundamentally break planar assumptions.
There is no continuous transistor width.
Electrical strength is defined by a **discrete number of fins**.

Any PCell that exposes continuous width parameters
is architecturally incompatible with FinFET technologies.

## Why Planar Thinking Fails

- Width does not physically exist
- Fin pitch is fixed by the process
- Gate length is defined by cut patterns
- OPC freedom is extremely limited

## Architectural Shift

Planar PCell:
Parameters → Rectangles

FinFET PCell:
Parameters → Topology → Constraints → Geometry


## User-Visible Parameters

Only parameters that map to real physical degrees of freedom
should be exposed:

- `nFin` – number of fins (discrete)
- `gateLength` – grid-locked
- `deviceType` – NMOS / PMOS
- `pcmMode` – exploration vs production

## Skeleton Concept

The FinFET PCell is structured as:

User Params
↓
Fin / Gate Topology
↓
Technology Rule Queries
↓
DFM / OPC Guards
↓
Layout Shapes


Topology is portable across nodes.
Rules and layer mappings are not.

## Design Philosophy

> The goal of a FinFET PCell is not flexibility,
> but predictability and silicon relevance.

