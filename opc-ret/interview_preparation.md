
FinFET의 Fin Grid가 $0.030\mu m (30nm)$라고 가정하고, 선택한 객체들을 가장 가까운 그리드로 옮겨주는 "Check-and-Fix" 자동화 스크립트 예시입니다.

'Find Off-grid' → 'Calculate Offset' → 'Move to Grid' Oder

1. SKILL 기반 자동 Snap 루틴 (Auto-Fixer)
이 코드는 크게 세 부분으로 나뉩니다: 현재 좌표 확인 → 오프셋 계산 → 위치 수정.

procedure(FixFinGridAlignment(@optional (pitch 0.030))
  let((cv selectedObjs offset_x offset_y newBBox)
    cv = geGetEditCellView()
    selectedObjs = geGetSelSet() ; 사용자가 선택한 객체들

    if(selectedObjs == nil then
        printf("--- Warning: 선택된 객체가 없습니다. ---\n")
    else
        foreach(obj selectedObjs
            ; 1. 현재 좌표 가져오기 (Lower-Left based)
            let((ll_x ll_y ur_x ur_y width height)
                ll_x = car(car(obj~>bBox))
                ll_y = cadar(obj~>bBox)
                ur_x = caadr(obj~>bBox)
                ur_y = cadadr(obj~>bBox)
                
                width = ur_x - ll_x
                height = ur_y - ll_y

                ; 2. caculate the most closed Grid-offset (round applied)
                ; Example: 0.031 -> 0.030 (offset -0.001) / 0.029 -> 0.030 (offset +0.001)
                new_ll_x = round(ll_x / pitch) * pitch
                new_ll_y = round(ll_y / pitch) * pitch

                ; 3. setting up new BBox (keeping the size of objects)
                newBBox = list(
                    list(new_ll_x new_ll_y)
                    list(new_ll_x + width new_ll_y + height)
                )

                ; 4. update to the Real DB (Move to Grid)
                obj~>bBox = newBBox
                
                printf("Fixed: %s at %L moved to %L\n" obj~>objType list(ll_x ll_y) list(new_ll_x new_ll_y))
            )
        )
        printf("--- Grid Alignment 완료 (%g pitch) ---\n" pitch)
    )
  )
)

2. 코드의 논리적 흐름 (인터뷰 답변용 설명)
매니저 앞에서 화이트보드에 코드를 적거나 설명할 때 다음 단계를 강조하세요:

Selection (geGetSelSet): 모든 객체를 건드리는 것은 위험하므로, 설계자가 수정을 원하는 대상만 선택해서 처리하도록 안전장치를 둡니다.

Quantization Logic (round): 현재 좌표를 pitch로 나누고 반올림한 뒤 다시 pitch를 곱하는 것이 핵심입니다. 이것이 수학적으로 가장 가까운 그리드 지점을 찾는 방법입니다.

Preserve Dimensions: 객체의 전체 크기(Width, Height)가 변하면 안 되므로, 왼쪽 하단(LL) 좌표만 그리드에 맞춘 뒤 원래 크기를 더해 우측 상단(UR) 좌표를 재계산합니다.

