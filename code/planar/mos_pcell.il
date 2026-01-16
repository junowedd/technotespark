; mos_pcell.il — Simple NMOS/PMOS PCell (planar)
; Author: (you)
; License: For internal/educational use only
; --------------------------------------------------------------

(procedure (mosSnapToGrid x grid)
 (let ((g (or grid 0.001)))
 (* g (round (/ x g)))
 )
)

(procedure (mosResolveLP tech name purp)
 (let ((lp (techGetLP tech name purp)))
 (when (null lp)
 (error "Layer-purpose %L %L not found in tech file.\n" name purp)
 )
 lp
 )
)

; --------------------------------------------------------------
; pcDefinePCell: MOSFET with multiple fingers
; Parameters in microns (unless noted). Uses current lib's tech.
; --------------------------------------------------------------
(pcDefinePCell
 (list 'layout
 "mos_simple"
 (list
 (cons 'type "n") ; "n" or "p"
 (cons 'w 1.00) ; channel width (µm), per finger
 (cons 'l 0.18) ; gate length (µm)
 (cons 'nf 1) ; number of fingers (int)
 (cons 'sdExt 0.20) ; S/D diffusion extension beyond gate edge (µm)
 (cons 'gateExt 0.10) ; poly extension beyond diffusion (µm)
 (cons 'polySpace 0.20) ; poly-to-poly space between fingers (µm)
 (cons 'contSize 0.14) ; contact size (square) (µm)
 (cons 'contSp 0.14) ; contact-to-contact space (µm)
 (cons 'contEncOD 0.03) ; contact enclosure by OD (µm)
 (cons 'contEncM1 0.03) ; contact enclosure by M1 (µm)
 (cons 'm1OverCont 0.06) ; extra M1 beyond contact (µm)
 (cons 'impEncOD 0.10) ; implant enclosure over OD (µm)
 (cons 'nwellEnc 0.40) ; nwell enclosure over P-diff (µm)
 (cons 'addNwell t) ; add N-well for PMOS
 (cons 'addPins t) ; create metal pins
 )
 )

👏
👍
😊



;; PCell body

(let* (

(cvId (geGetEditCellView))

(tech (if cvId (techGetTechFile cvId) (error "No edit cellView.")))



;; Resolve layer-purpose pairs (adapt names to your PDK if needed)

(lpOD (mosResolveLP tech "OD" "drawing"))

(lpPOLY (mosResolveLP tech "POLY" "drawing"))

(lpNIMP (mosResolveLP tech "NIMP" "drawing"))

(lpPIMP (mosResolveLP tech "PIMP" "drawing"))

(lpNWELL (mosResolveLP tech "NWELL" "drawing"))

(lpCONT (mosResolveLP tech "CONT" "drawing"))

(lpM1 (mosResolveLP tech "MET1" "drawing"))

(lpPIN (mosResolveLP tech "MET1" "pin"))



;; Parameters

(type (if (equal type "p") "p" "n"))

(w (max 0.05 w))

(l (max 0.05 l))

(nf (max 1 (fix nf)))

(sdExt (max 0.0 sdExt))

(gateExt (max 0.0 gateExt))

(polySpace (max 0.0 polySpace))

(contSize (max 0.05 contSize))

(contSp (max 0.05 contSp))

(contEncOD (max 0.0 contEncOD))

(contEncM1 (max 0.0 contEncM1))

(m1OverCont (max 0.0 m1OverCont))

(impEncOD (max 0.0 impEncOD))

(nwellEnc (max 0.0 nwellEnc))

(addNwell addNwell)

(addPins addPins)



;; Derived geometry

(gatePitch (+ l polySpace 2*gateExt))

(activeLen (+ (* nf l) (* (max 0 (- nf 1)) polySpace) (* 2 gateExt)))

(odLen (+ activeLen (* 2 sdExt)))

(odWid w)



;; Coordinate frame: center at origin

(x0 (- (/ odLen 2.0)))

(y0 (- (/ odWid 2.0)))

(x1 (+ (/ odLen 2.0)))

(y1 (+ (/ odWid 2.0)))



;; Contact rows (S and D) inside OD

(contRowYclear (- (/ odWid 2.0) contEncOD))

(contYmin (- contRowYclear contSize))

(contYmax contRowYclear)



;; M1 strap over contacts

(m1Ymin (- contYmin m1OverCont))

(m1Ymax (+ contYmax m1OverCont))

)



(rodSetEnv(nil)) ; ensure ROD initialized



;; 1) OD rectangle

(setq odRect (rodCreateRect

?layer lpOD

?bBox (list x0 y0 x1 y1)

))



;; 2) Poly fingers

(setq polyList nil)

(for i 0 (sub1 nf)

(let* ( (gx (+ x0 sdExt gateExt (* i gatePitch)))

(polyX0 gx)

(polyX1 (+ gx l))

(polyY0 (- (/ w 2.0) gateExt))

(polyY1 (+ (/ w 2.0) gateExt)) )

(setq pg (rodCreateRect ?layer lpPOLY ?bBox (list polyX0 polyY0 polyX1 polyY1)))

(setq polyList (cons pg polyList))

)

)



;; 3) Implants

(let* ( (impX0 (- x0 impEncOD))

(impY0 (- y0 impEncOD))

(impX1 (+ x1 impEncOD))

(impY1 (+ y1 impEncOD))

(impLP (if (equal type "n") lpNIMP lpPIMP)) )

(setq impRect (rodCreateRect ?layer impLP ?bBox (list impX0 impY0 impX1 impY1)))

)



;; 4) N-well for PMOS (optional)

(when (and addNwell (equal type "p"))

(let* ( (nwX0 (- x0 nwellEnc))

(nwY0 (- y0 nwellEnc))

(nwX1 (+ x1 nwellEnc))

(nwY1 (+ y1 nwellEnc)) )

(setq nwRect (rodCreateRect ?layer lpNWELL ?bBox (list nwX0 nwY0 nwX1 nwY1)))

)

)



;; 5) Contacts in S/D regions and M1 over them

;; Determine source side: left of first gate, drain side: right of last gate.

(let* ( (firstGateX (+ x0 sdExt))

(lastGateX (- x1 sdExt))

(srcXmax (- firstGateX contEncOD))

(drnXmin (+ lastGateX contEncOD))

(srcXmin (+ x0 contEncOD))

(drnXmax (- x1 contEncOD))



;; Fill contact arrays in available windows

(function createContRow (lambda (xmin xmax)

(let* ( (winW (- xmax xmin))

(nx (max 1 (fix (/ (+ winW contSp) (+ contSize contSp)))))

(totalW (+ (* nx contSize) (* (sub1 nx) contSp)))

(xStart (+ xmin (/ (- winW totalW) 2.0)))

(conts '()))

(for j 0 (sub1 nx)

(let* ( (cx0 (+ xStart (* j (+ contSize contSp))))

(cx1 (+ cx0 contSize)) )

(setq c (rodCreateRect ?layer lpCONT ?bBox (list cx0 contYmin cx1 contYmax)))

(setq conts (cons c conts))

)

)

conts

)))

)



(setq srcConts (createContRow srcXmin srcXmax))

(setq drnConts (createContRow drnXmin drnXmax))



;; M1 straps over contacts

(when srcConts

(setq sMin (car (apply 'min (foreach mapcar c srcConts (list (car (geGetBBox c)))))))

(setq sMax (car (apply 'max (foreach mapcar c srcConts (list (cadr (geGetBBox c)))))))

(setq sM1 (rodCreateRect ?layer lpM1 ?bBox (list (- sMin contEncM1) m1Ymin (+ sMax contEncM1) m1Ymax)))

)

(when drnConts

(setq dMin (car (apply 'min (foreach mapcar c drnConts (list (car (geGetBBox c)))))))

(setq dMax (car (apply 'max (foreach mapcar c drnConts (list (cadr (geGetBBox c)))))))

(setq dM1 (rodCreateRect ?layer lpM1 ?bBox (list (- dMin contEncM1) m1Ymin (+ dMax contEncM1) m1Ymax)))

)

)



;; 6) Gate M1 strap (optional slim M1 over poly centerline for easy pinning)

(let* ( (gxCenter (/ (+ x0 x1) 2.0)) ) )



;; 7) Create pins (M1) for S/D/G

(when addPins

;; Source pin over left S region M1

(when sM1

(dbCreatePin cvId "S" lpPIN (dbCreateRect cvId lpPIN (geGetBBox sM1))))

;; Drain pin over right D region M1

(when dM1

(dbCreatePin cvId "D" lpPIN (dbCreateRect cvId lpPIN (geGetBBox dM1))))

;; Gate pin: use a slim M1 rectangle spanning all fingers at y=0

(let* ( (gX0 (+ x0 sdExt))

(gX1 (- x1 sdExt))

(gW (max contSize 0.12))

(gY0 (- 0 (/ gW 2.0)))

(gY1 (+ 0 (/ gW 2.0)))

(gM1 (rodCreateRect ?layer lpM1 ?bBox (list gX0 gY0 gX1 gY1))) )

(dbCreatePin cvId "G" lpPIN (dbCreateRect cvId lpPIN (geGetBBox gM1)))

)

)



;; 8) Stretch handles (for Virtuoso stretch UI)

(rodAssignHandle odRect "w" "height" nil) ; vertical stretch changes W

(rodAssignHandle odRect "l" "width" nil) ; horizontal stretch changes L



t

)

); mos_pcell.il — Simple NMOS/PMOS PCell (planar)
; Author: (you)
; License: For internal/educational use only
; --------------------------------------------------------------

(procedure (mosSnapToGrid x grid)
 (let ((g (or grid 0.001)))
 (* g (round (/ x g)))
 )
)

(procedure (mosResolveLP tech name purp)
 (let ((lp (techGetLP tech name purp)))
 (when (null lp)
 (error "Layer-purpose %L %L not found in tech file.\n" name purp)
 )
 lp
 )
)

; --------------------------------------------------------------
; pcDefinePCell: MOSFET with multiple fingers
; Parameters in microns (unless noted). Uses current lib's tech.
; --------------------------------------------------------------
(pcDefinePCell
 (list 'layout
 "mos_simple"
 (list
 (cons 'type "n") ; "n" or "p"
 (cons 'w 1.00) ; channel width (µm), per finger
 (cons 'l 0.18) ; gate length (µm)
 (cons 'nf 1) ; number of fingers (int)
 (cons 'sdExt 0.20) ; S/D diffusion extension beyond gate edge (µm)
 (cons 'gateExt 0.10) ; poly extension beyond diffusion (µm)
 (cons 'polySpace 0.20) ; poly-to-poly space between fingers (µm)
 (cons 'contSize 0.14) ; contact size (square) (µm)
 (cons 'contSp 0.14) ; contact-to-contact space (µm)
 (cons 'contEncOD 0.03) ; contact enclosure by OD (µm)
 (cons 'contEncM1 0.03) ; contact enclosure by M1 (µm)
 (cons 'm1OverCont 0.06) ; extra M1 beyond contact (µm)
 (cons 'impEncOD 0.10) ; implant enclosure over OD (µm)
 (cons 'nwellEnc 0.40) ; nwell enclosure over P-diff (µm)
 (cons 'addNwell t) ; add N-well for PMOS
 (cons 'addPins t) ; create metal pins
 )
 )

👏
👍
😊



;; PCell body

(let* (

(cvId (geGetEditCellView))

(tech (if cvId (techGetTechFile cvId) (error "No edit cellView.")))



;; Resolve layer-purpose pairs (adapt names to your PDK if needed)

(lpOD (mosResolveLP tech "OD" "drawing"))

(lpPOLY (mosResolveLP tech "POLY" "drawing"))

(lpNIMP (mosResolveLP tech "NIMP" "drawing"))

(lpPIMP (mosResolveLP tech "PIMP" "drawing"))

(lpNWELL (mosResolveLP tech "NWELL" "drawing"))

(lpCONT (mosResolveLP tech "CONT" "drawing"))

(lpM1 (mosResolveLP tech "MET1" "drawing"))

(lpPIN (mosResolveLP tech "MET1" "pin"))



;; Parameters

(type (if (equal type "p") "p" "n"))

(w (max 0.05 w))

(l (max 0.05 l))

(nf (max 1 (fix nf)))

(sdExt (max 0.0 sdExt))

(gateExt (max 0.0 gateExt))

(polySpace (max 0.0 polySpace))

(contSize (max 0.05 contSize))

(contSp (max 0.05 contSp))

(contEncOD (max 0.0 contEncOD))

(contEncM1 (max 0.0 contEncM1))

(m1OverCont (max 0.0 m1OverCont))

(impEncOD (max 0.0 impEncOD))

(nwellEnc (max 0.0 nwellEnc))

(addNwell addNwell)

(addPins addPins)



;; Derived geometry

(gatePitch (+ l polySpace 2*gateExt))

(activeLen (+ (* nf l) (* (max 0 (- nf 1)) polySpace) (* 2 gateExt)))

(odLen (+ activeLen (* 2 sdExt)))

(odWid w)



;; Coordinate frame: center at origin

(x0 (- (/ odLen 2.0)))

(y0 (- (/ odWid 2.0)))

(x1 (+ (/ odLen 2.0)))

(y1 (+ (/ odWid 2.0)))



;; Contact rows (S and D) inside OD

(contRowYclear (- (/ odWid 2.0) contEncOD))

(contYmin (- contRowYclear contSize))

(contYmax contRowYclear)



;; M1 strap over contacts

(m1Ymin (- contYmin m1OverCont))

(m1Ymax (+ contYmax m1OverCont))

)



(rodSetEnv(nil)) ; ensure ROD initialized



;; 1) OD rectangle

(setq odRect (rodCreateRect

?layer lpOD

?bBox (list x0 y0 x1 y1)

))



;; 2) Poly fingers

(setq polyList nil)

(for i 0 (sub1 nf)

(let* ( (gx (+ x0 sdExt gateExt (* i gatePitch)))

(polyX0 gx)

(polyX1 (+ gx l))

(polyY0 (- (/ w 2.0) gateExt))

(polyY1 (+ (/ w 2.0) gateExt)) )

(setq pg (rodCreateRect ?layer lpPOLY ?bBox (list polyX0 polyY0 polyX1 polyY1)))

(setq polyList (cons pg polyList))

)

)



;; 3) Implants

(let* ( (impX0 (- x0 impEncOD))

(impY0 (- y0 impEncOD))

(impX1 (+ x1 impEncOD))

(impY1 (+ y1 impEncOD))

(impLP (if (equal type "n") lpNIMP lpPIMP)) )

(setq impRect (rodCreateRect ?layer impLP ?bBox (list impX0 impY0 impX1 impY1)))

)



;; 4) N-well for PMOS (optional)

(when (and addNwell (equal type "p"))

(let* ( (nwX0 (- x0 nwellEnc))

(nwY0 (- y0 nwellEnc))

(nwX1 (+ x1 nwellEnc))

(nwY1 (+ y1 nwellEnc)) )

(setq nwRect (rodCreateRect ?layer lpNWELL ?bBox (list nwX0 nwY0 nwX1 nwY1)))

)

)



;; 5) Contacts in S/D regions and M1 over them

;; Determine source side: left of first gate, drain side: right of last gate.

(let* ( (firstGateX (+ x0 sdExt))

(lastGateX (- x1 sdExt))

(srcXmax (- firstGateX contEncOD))

(drnXmin (+ lastGateX contEncOD))

(srcXmin (+ x0 contEncOD))

(drnXmax (- x1 contEncOD))



;; Fill contact arrays in available windows

(function createContRow (lambda (xmin xmax)

(let* ( (winW (- xmax xmin))

(nx (max 1 (fix (/ (+ winW contSp) (+ contSize contSp)))))

(totalW (+ (* nx contSize) (* (sub1 nx) contSp)))

(xStart (+ xmin (/ (- winW totalW) 2.0)))

(conts '()))

(for j 0 (sub1 nx)

(let* ( (cx0 (+ xStart (* j (+ contSize contSp))))

(cx1 (+ cx0 contSize)) )

(setq c (rodCreateRect ?layer lpCONT ?bBox (list cx0 contYmin cx1 contYmax)))

(setq conts (cons c conts))

)

)

conts

)))

)



(setq srcConts (createContRow srcXmin srcXmax))

(setq drnConts (createContRow drnXmin drnXmax))



;; M1 straps over contacts

(when srcConts

(setq sMin (car (apply 'min (foreach mapcar c srcConts (list (car (geGetBBox c)))))))

(setq sMax (car (apply 'max (foreach mapcar c srcConts (list (cadr (geGetBBox c)))))))

(setq sM1 (rodCreateRect ?layer lpM1 ?bBox (list (- sMin contEncM1) m1Ymin (+ sMax contEncM1) m1Ymax)))

)

(when drnConts

(setq dMin (car (apply 'min (foreach mapcar c drnConts (list (car (geGetBBox c)))))))

(setq dMax (car (apply 'max (foreach mapcar c drnConts (list (cadr (geGetBBox c)))))))

(setq dM1 (rodCreateRect ?layer lpM1 ?bBox (list (- dMin contEncM1) m1Ymin (+ dMax contEncM1) m1Ymax)))

)

)



;; 6) Gate M1 strap (optional slim M1 over poly centerline for easy pinning)

(let* ( (gxCenter (/ (+ x0 x1) 2.0)) ) )



;; 7) Create pins (M1) for S/D/G

(when addPins

;; Source pin over left S region M1

(when sM1

(dbCreatePin cvId "S" lpPIN (dbCreateRect cvId lpPIN (geGetBBox sM1))))

;; Drain pin over right D region M1

(when dM1

(dbCreatePin cvId "D" lpPIN (dbCreateRect cvId lpPIN (geGetBBox dM1))))

;; Gate pin: use a slim M1 rectangle spanning all fingers at y=0

(let* ( (gX0 (+ x0 sdExt))

(gX1 (- x1 sdExt))

(gW (max contSize 0.12))

(gY0 (- 0 (/ gW 2.0)))

(gY1 (+ 0 (/ gW 2.0)))

(gM1 (rodCreateRect ?layer lpM1 ?bBox (list gX0 gY0 gX1 gY1))) )

(dbCreatePin cvId "G" lpPIN (dbCreateRect cvId lpPIN (geGetBBox gM1)))

)

)



;; 8) Stretch handles (for Virtuoso stretch UI)

(rodAssignHandle odRect "w" "height" nil) ; vertical stretch changes W

(rodAssignHandle odRect "l" "width" nil) ; horizontal stretch changes L



t

)

)