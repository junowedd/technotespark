; file: my_rect_pcell.il

; Minimal ROD-based rectangle with stretch handles + pin
; Assumes tech layers "DIFF" and "MET1"; adapt to your PDK.
; Load once to (re)define the PCell:
; load("my_rect_pcell.il")

pcDefinePCell(
 list(ddGetObj("MY_LIB") "rect_pcell" "layout")
 ( (w float 2.0) ; width (X)
 (h float 1.0) ; height (Y)
 (pinName string "P") ; a single metal pin
 )

 let( (rect rodR met net tfId minMetalW minMetalExt pinR)

 ;-- tech lookups (guard against nils in older PDKs)
 tfId = techGetTechFile(pcCellView~>lib)
 minMetalW = max(0.06 car(techGetSpacingRule(tfId "minWidth" "MET1")||list(0.06)))
 minMetalExt = max(0.06 car(techGetSpacingRule(tfId "minExtension" "MET1")||list(0.06)))

 ;-- main rectangle on DIFF
 rect = rodCreateRect(
 ?cvId pcCellView
 ?layer "DIFF"
 ?bBox list( 0:0 w:h )
 ?name "body"
 )

 ;-- expose stretch handles bound to parameters
 rodAssignHandleToParameter(
 ?parameter "w"
 ?rodObj rect
 ?handleName list("centerRight" "centerLeft")
 ?displayName "w" ?stretchDir "x" ?stretchType "relative" ?moveOrigin t
 )
 rodAssignHandleToParameter(
 ?parameter "h"
 ?rodObj rect
 ?handleName list("upperCenter" "lowerCenter")
 ?displayName "h" ?stretchDir "y" ?stretchType "relative" ?moveOrigin t
 )

 ;-- simple pin on MET1 centered at top edge (respect min widths)
 rodR = rodCreateRect(
 ?cvId pcCellView ?layer "MET1"
 ?bBox list( (w/2 - minMetalW/2) : (h - minMetalExt)
 (w/2 + minMetalW/2) : (h + minMetalExt) )
 ?name "pinMetal"
 )
 pinR = dbCreatePin(
 pcCellView pinName "MET1"
 list( rodR~>bBox ) "terminal"
 )

 ;-- label for the pin
 dbCreateLabel(pcCellView "MET1" list(w/2 : (h + minMetalExt))
 pinName "centerLeft" "stick" 0.12)

 t
 ) ; let
) ; pcDefinePCell