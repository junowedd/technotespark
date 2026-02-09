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
