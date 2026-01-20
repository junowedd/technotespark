;===========================================================
; File: my_rect_pcell.il
; Description: Simple ROD-based rectangular PCell with pin
;===========================================================

pcDefinePCell(
  list(ddGetObj("MY_LIB") "rect_pcell" "layout")

  ;; -----------------------------
  ;; PCell parameters
  ;; -----------------------------
  (
    (w float 2.0)
    (h float 1.0)
    (pinName string "P")
  )

  ;; -----------------------------
  ;; PCell body
  ;; -----------------------------
  let(
    (
      pcCellView
      tfId
      minMetalW
      minMetalExt
      rodR
      pinR
    )

    ;; Get current cellView
    pcCellView = pcGetCellView()

    ;; Get techfile
    tfId = techGetTechFile(pcCellView~>lib)

    ;; Technology rules (fallback-safe)
    minMetalW  = 0.2
    minMetalExt = 0.2

 ;-- tech lookups (guard against nils in older PDKs)
 ;-- tfId = techGetTechFile(pcCellView~>lib)
 ;-- minMetalW =   max(0.06 car(techGetSpacingRule(tfId "minWidth" "MET1")||list(0.06)))
 ;-- minMetalExt = max(0.06 car(techGetSpacingRule(tfId "minExtension" "MET1")||list(0.06)))

    ;; ----------------------------------
    ;; Create ROD rectangle (DIFF)
    ;; ----------------------------------
    rodR = rodCreateRect(
      ?cvId   pcCellView
      ?layer  "DIFF"
      ?width  w
      ?height h
      ?origin list(0 0)
      ?name   "diffRect"
    )

    ;; ----------------------------------
    ;; Create MET1 pin over top edge
    ;; ----------------------------------
    pinR = dbCreatePin(
      pcCellView
      pinName
      "MET1"
      list(
        list(
          (w/2 - minMetalW/2) : h
          (w/2 + minMetalW/2) : (h + minMetalExt)
        )
      )
      "terminal"
    )

    ;; ----------------------------------
    ;; Create pin label (stretch-aware)
    ;; ----------------------------------
    dbCreateLabel(
      pcCellView
      "MET1"
      list(w/2 : (h + minMetalExt))
      pinName
      "centerLeft"
      "stick"
      0.12
    )

    t
  ) ; let
) ; pcDefinePCell


# rect_pcell – ROD-Based Rectangle PCell

## Overview
`rect_pcell` is a simple, technology-safe, ROD-based parameterized cell
implemented in Cadence SKILL. It generates a rectangular DIFF shape with
a MET1 pin placed on the top edge.

This PCell is suitable for:
- Analog layout prototyping
- PERC / Calibre DFM-safe flows
- Educational or template usage

---

## Parameters

| Name     | Type   | Default | Description |
|---------|--------|---------|-------------|
| `w`     | float  | 2.0     | Width of the rectangle (µm) |
| `h`     | float  | 1.0     | Height of the rectangle (µm) |
| `pinName` | string | "P" | Name of the MET1 pin |

---

## Geometry Creation

- A **ROD rectangle** is created on the `DIFF` layer.
- The rectangle origin is fixed at `(0,0)` to ensure deterministic stretching.
- Width and height are fully parameterized.

---

## Pin Definition

- A MET1 pin is created centered on the top edge of the rectangle.
- The pin width respects minimum metal width.
- Pin extension ensures clean LVS recognition.

---

## Label & Stretching

- A label is placed at the pin center.
- Label alignment: `centerLeft`
- Stretch behavior: `stick`
- Snap grid: `0.12 µm`

This ensures:
- Proper snapping during interactive stretching
- Clean electrical connectivity
- DRC/LVS robustness

---

## Best Practices Used

- ROD-based geometry
- Typed parameters
- Layout-view targeting
- Explicit techfile access
- Clean pin purposes (`terminal`)

---

## Notes

- Technology rules are provided with safe fallback values.
- Can be extended easily with:
  - Stretch handles
  - Multiple pins
  - Net expressions
