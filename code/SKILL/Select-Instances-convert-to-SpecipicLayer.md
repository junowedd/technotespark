만약 "선택한 모든 인스턴스의 이름을 출력하고, 특정 레이어로 변경하라"는 문제가 나온다면?

procedure(MySimpleChallenge()
  let((cv selectedShapes)
    cv = geGetEditCellView()
    selectedShapes = geGetSelSet() ; 현재 선택된 객체들 가져오기
    
    foreach(shape selectedShapes
      if(shape~>objType == "rect" then
        printf("Found a rect at: %L\n" shape~>bBox)
        ; 레이어를 Metal2로 변경 예시
        shape~>lpp = list("M2" "drawing")
      )
    )
  )
)


4. 인터뷰 팁 (Infineon 스타일)
Logic First: 코드가 완벽하지 않아도 됩니다. "먼저 CellView ID를 얻고, 반복문을 통해 레이어를 필터링한 뒤, 좌표를 계산해서 새로운 도형을 만들겠습니다"라고 로직을 먼저 설명하세요.

Error Handling: "만약 셀이 Read-only라면 오류가 날 테니, dbIsId(cv) 같은 체크가 필요할 것 같습니다"라고 덧붙이면 시니어급 엔지니어로 보입니다.
    unless( cv
      error("No editable cellview found.\n")
    )


Virtuoso 통합: SKILL이 단순히 언어가 아니라, Virtuoso 환경(CIW, Layout Editor)과 어떻게 상호작용하는지 이해하고 있음을 보여주세요.