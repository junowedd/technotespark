;============================================================
; finfet_pcell.il
;
; Reference FinFET PCell (12nm-class)
; ----------------------------------
; This file demonstrates FinFET PCell architecture:
; topology-driven design, technology abstraction,
; and DFM/OPC-aware constraints.
;
; NOT intended for tape-out or direct foundry use.
;============================================================

;------------------------------------------------------------
; Technology rule abstraction (PDK-dependent layer)
;------------------------------------------------------------
procedure(loadTechRules(cv)
  let((rules)
    rules = makeTable('techRules nil)

    ; Abstract technology parameters
    rules->finPitch       = 0.04
    rules->finWidth       = 0.01
    rules->finHeight      = 0.06
    rules->minGateLength  = 0.016
    rules->gatePitch      = 0.05

    rules
  )
)

;------------------------------------------------------------
; Generate discrete fin grid (NO continuous width)
;------------------------------------------------------------
procedure(generateFinGrid(nFin finPitch)
  let((fins i)
    fins = nil
    for(i 0 nFin-1
      fins = cons(i * finPitch fins)
    )
    reverse(fins)
  )
)

;------------------------------------------------------------
; DFM / OPC guard checks
;------------------------------------------------------------
procedure(checkDFMConstraints(nFin gateLength pcmMode rules)
  when(nFin < 2 && !pcmMode
    error("Single-fin devices forbidden in product mode")
  )
  when(gateLength < rules->minGateLength
    error("Gate length below technology minimum")
  )
)

;------------------------------------------------------------
; Geometry creation (simplified 2D top view)
;------------------------------------------------------------
procedure(createFinFETGeometry(cv fins gateLength rules)
  let((x)

    ; Create fins
    foreach(x fins
      dbCreateRect(
        cv "FIN"
        list(
          x:0
          x + rules->finWidth : rules->finHeight
        )
      )
    )

    ; Create gate stripe
    dbCreateRect(
      cv "POLY"
      list(
        -rules->gatePitch/2 : rules->finHeight/2
        (last(fins) + rules->finPitch)
        : rules->finHeight/2 + gateLength
      )
    )
  )
)

;------------------------------------------------------------
; Top-level PCell definition
;------------------------------------------------------------
pcDefinePCell(
  list(ddGetObj("ReferenceLib") "finfet_pcell" "layout")

  (
    (deviceType "NMOS")
    (nFin 3)
    (gateLength 0.016)
    (pcmMode nil)
  )

  let((cv rules fins)

    cv = pcCellView
    rules = loadTechRules(cv)

    checkDFMConstraints(nFin gateLength pcmMode rules)
    fins = generateFinGrid(nFin rules->finPitch)

    createFinFETGeometry(cv fins gateLength rules)
  )
)
