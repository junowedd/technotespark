1. Metal-to-Via Enclosure & Grid 체크 스크립트
이 스크립트는 Via가 Metal1 내부에 안전하게 들어와 있는지, 그리고 그 여유 공간(Enclosure)이 정해진 그리드 배수인지 확인합니다.

Code snippet

procedure(CheckViaEnclosure(@optional (grid 0.005))
  let((cv selectedVias metals enclosure_x enclosure_y)
    cv = geGetEditCellView()
    ; 1. Metal1-Via1 연결 부위에서 Via1들만 선택
    selectedVias = setof(x geGetSelSet() x~>lpp == list("VIA1" "drawing"))

    foreach(via selectedVias
        ; 2. Via가 위치한 좌표의 Metal1을 검색
        metals = dbGetOverlaps(cv via~>bBox list("M1" "drawing") 0)

        if(metals then
            let((vBBox mBBox)
                vBBox = via~>bBox
                mBBox = car(metals)~>bBox ; 가장 첫 번째 겹치는 Metal 기준

                ; 3. Enclosure 계산 (Metal 가장자리 - Via 가장자리)
                ; Left-side enclosure 예시
                enclosure_x = abs(car(car(mBBox)) - car(car(vBBox)))
                enclosure_y = abs(cadar(mBBox) - cadar(vBBox))

                ; 4. Grid 체크 (예: Enclosure는 5nm Grid X times 배수여야 함)
                if( abs(remainder(enclosure_x grid)) > 0.001 || abs(remainder(enclosure_y grid)) > 0.001 then
                    printf("--- [Enclosure Error] Off-Grid: X=%g, Y=%g ---\n" enclosure_x enclosure_y)
                    geAddHilightRectangle(geGetEditRep() list("y0" "drawing") via~>bBox)
                else
                    printf("--- [Pass] Via Enclosure is Grid-Clean ---\n")
                )
            )
        else
            printf("--- [LVS Error] Floating Via: No Metal1 found! ---\n")
        )
    )
  )
)

2. 왜 Metal-to-Via 마진이 중요한가? (인터뷰 답변 포인트)
이 스크립트를 설명하면서 아래 두 가지 제조 이슈를 언급하면 면접관들이 당신의 깊이에 감탄할 것입니다.

Electromigration (EM): "Via가 Metal의 정중앙에서 벗어나 한쪽 Enclosure가 너무 좁아지면, 그 부분에 전류 밀도가 집중되어 배선이 끊어지는 EM 문제가 발생할 수 있습니다."

Via Misalignment (Overlay): "제조 과정에서 마스크가 미세하게 틀어질 수 있는데, Enclosure 마진이 그리드에 맞지 않고 너무 작으면 Via가 Metal 밖으로 삐져나가는 'Unlanded Via'가 되어 저항이 급격히 증가합니다."

3. 복잡한 좌표 계산 루틴: BBox 중심 맞추기
만약 면접관이 **"Via를 Metal의 정중앙에 자동으로 위치시키는 코드를 짤 수 있나요?"**라고 챌린지를 준다면, 이 '중심점 계산' 로직을 보여주세요.

Code snippet
; 두 객체의 중심점을 일치시키는 핵심 수식
procedure(CenterViaOnMetal(via metal)
    let((mCenter vCenter offset)
        ; 1. Metal의 중심점 구하기
        mCenter = list(
            (car(car(metal~>bBox)) + car(cadadr(metal~>bBox))) / 2.0
            (cadar(metal~>bBox) + cadadr(metal~>bBox)) / 2.0
        )
        ; 2. Via의 이동 (dbMoveFig 사용)
        ; Via의 현재 중심과 Metal 중심 사이의 거리를 계산하여 이동
        dbMoveFig(via nil list(mCenter "R0")) 
        printf("Via centered on Metal at %L\n" mCenter)
    )
)


4. 

Challenge를 받으면: 바로 코딩하지 말고, "입력값(Via ID), 검색 범위(Metal), 판단 기준(Grid/Enclosure)"을 먼저 말로 정의하세요.

화이트보드 코딩 시: dbGetOverlaps와 ~>bBox 이 두 가지만 정확히 써도 "SKILL을 실제로 써본 사람"이라는 확신을 줍니다.

마무리 발언: "이러한 자동화 스크립트는 DRC/LVS를 돌리기 전에 설계 단계에서 에러를 90% 이상 차단하여 전체 프로젝트 일정을 단축시키는 데 핵심적인 역할을 합니다."

