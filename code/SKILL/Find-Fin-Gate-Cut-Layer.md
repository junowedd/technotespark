특정 영역 내에서 FIN이나 GATE 레이어만 찾아내어 그 개수를 세거나 속성을 변경하는 로직입니다

procedure(AnalyzeFinLayers(cv areaBox)
    let((allShapes finCount cutCount)
        finCount = 0
        cutCount = 0
        
        ; 지정된 영역(areaBox) 내의 모든 도형을 검색
        allShapes = dbGetOverlaps(cv areaBox list("FIN" "drawing") 0)
        
        foreach(shape allShapes
            ; dbGetOverlaps는 리스트 형태(id or list)로 반환할 수 있으므로 처리
            case(car(shape~>lpp)
                ("FIN"     finCount++)
                ("GATE"    printf("Gate found at %L\n" shape~>bBox))
                ("FINCUT"  cutCount++)
            )
        )
        printf("Summary: Fins(%d), Cut Layers(%d)\n" finCount cutCount)
    )
)