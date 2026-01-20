1. 전체 워크플로우 (Flow)
이 방식의 핵심은 **"좌표 수동 입력 배제"**입니다.

Calibre QS (Tcl): LVS 결과에서 문제가 된 Net이나 Short 좌표를 텍스트 파일로 추출.

SKILL Script: 생성된 텍스트 파일을 읽어 Virtuoso 레이아웃 창에 Highlighting Shape를 생성.

Result: 디자이너는 버튼 하나로 Short 지점으로 즉시 이동(Zoom) 및 확인.


2. 단계별 상세 명령어 및 코드
Step 1: Calibre Query Server에서 좌표 추출 (Tcl/QS)
대화형 모드(-qs) 혹은 배치 스크립트에서 특정 Net의 좌표를 파일로 저장합니다.

Tcl > extract.tcl 
# Calibre QS 환경 (qs.tcl)
LAYOUT SYSTEM GDS
LAYOUT PATH "top_design.gds"
LAYOUT PRIMARY "TOP_CELL"
LVS REPORT "lvs_result.rep"

# Net 12번(예: VDD)의 모든 Metal Shape 좌표를 "vdd_shapes.txt"로 저장
set  net_idx    [NET NAME "VDD" LAYOUT]
set  file_id    [open  "vdd_shapes.txt"  w]
puts  $file_id  [LAYOUT  NET  LIST  $net_idx]
close  $file_id

Bash:
$ calibre -qs -cmd extract.tcl 

데이터 양: 만약 VDD 같은 전원 넷을 추출하면 좌표 데이터가 수십만 줄이 될 수 있습니다. 이 경우 파일 쓰기 속도가 느려질 수 있으므로, 특정 영역(LAYOUT BBOX)으로 한정해서 추출하는 로직을 추가하는 것이 실무적입니다.


Step 2: SKILL 스크립트와 연동 (Highlighting)
위에서 만든 "vdd_shapes.txt" 를 읽어서 Virtuoso 화면에 노란색 박스를 그려주는 SKILL 예시입니다.

procedure(MyHighlightNet(fileName)
  let((fp line coords cv)
    cv = geGetEditCellView() ; 현재 열려있는 레이아웃 창 (CellView) 가져오기
/**    fp = infile(fileName)
    if(cv && (fp = infile(fileName)) then
      printf("Starting Highlight from file: %s\n" fileName)

    
    while(gets(line fp)
      ; 텍스트에서 좌표(x1 y1 x2 y2)를 파싱 (간단 예시), 파일의 각 라인을 읽음
      ; 문자열을 리스트로 변환 (예: "10 2500 5000 2800 12000" -> ("10" "2500" ...))

      coords = parseString(line)

      ; Calibre 출력 형식에 따라 좌표 인덱스 설정 (보통 1~4번 인덱스가 x1 y1 x2 y2)
      if(length(coords) >= 5 then
        ; 레이아웃에 Highlighting 목적의 Rect 생성 (y0 layer 등 사용)
        dbCreateRect(cv list("y0" "drawing") 
          list(atof(nth(0 coords)):atof(nth(1 coords))   ; Lower-Left (x:y)
               atof(nth(2 coords)):atof(nth(3 coords)))  ; Upper-Right (x:y)
        )

        ; 3. 하이라이트 레이어로 사각형 생성 (y0 layer, drawing purpose)
          dbCreateRect(cv list("y0" "drawing") rectCoords)
      )
    )
    close(fp)  
    ; 4. 화면 갱신
    hiRedraw()
    printf("Highlighting process finished.\n")
    else
      warn("Cannot open file or no layout window found!\n")
    )
  )
)

; 사용법: CIW 창에 TrHighlightFromFile("vdd_shapes.txt") 입력

; Coordinate Precision (atof): "Calibre Query Server에서 나온 텍스트 데이터는 문자열 형태이므로, 이를 atof()(ASCII to Float) 함수를 통해 부동 소수점 좌표로 정확히 변환하여 미세 공정의 정밀도를 유지했습니다."

;Layer Selection (y0): "실제 설계 데이터(Metal1, Metal2 등)를 건드리지 않고, 검증용 임시 레이어인 **y0나 y1 (Highlight layer)**을 사용하여 설계를 오염시키지 않으면서 디버깅 시인성을 높였습니다."

;Efficiency: "수천 개의 좌표가 있을 경우 dbCreateRect 대신 **dbCreateHierElement**나 Overlay 기능을 사용하여 툴의 부하(Lag)를 줄이는 방향으로도 고도화가 가능합니다."