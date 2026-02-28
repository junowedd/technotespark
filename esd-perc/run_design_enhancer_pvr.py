import json

# [Step 1] 데이터 로드: Calibre 또는 전력 분석 툴에서 추출된 Raw 데이터
# 각 항목은 위치(coordinate), 전압 강하량(drop_mv), 문제 유형(type)을 포함합니다.
analysis_data = [
    {"id": 1, "coordinate": (120.5, 450.2), "drop_mv": 45, "type": "IR_DROP", "net": "VDD"},
    {"id": 2, "coordinate": (340.1, 120.8), "drop_mv": 12, "type": "IR_DROP", "net": "VSS"},
    {"id": 3, "coordinate": (500.0, 500.0), "drop_mv": 85, "type": "IR_DROP", "net": "VDD"},
    {"id": 4, "coordinate": (150.2, 300.5), "drop_mv": 0, "type": "SINGLE_VIA", "net": "SIGNAL_A"},
    {"id": 5, "coordinate": (600.7, 850.1), "drop_mv": 60, "type": "IR_DROP", "net": "VDD"}
]

def run_design_enhancer_pvr(data, threshold_mv=40):
    """
    가상의 Design Enhancer PVR 로직:
    - 전압 강하(IR-drop)가 설정값 이상인 지점과 신뢰성이 낮은 Single Via를 탐지합니다.
    """
    print(f"--- DFM Design Enhancer PVR 자동화 실행 (임계치: {threshold_mv}mV) ---")
    
    correction_commands = []
    
    for entry in data:
        # [Step 2] Hotspot 탐지 (Filtering)
        # 1. IR-drop이 심각한 지점 (예: 40mV 이상)
        if entry['type'] == "IR_DROP" and entry['drop_mv'] > threshold_mv:
            print(f"[알람] {entry['net']} Net 전압 강하 과다: {entry['drop_mv']}mV (위치: {entry['coordinate']})")
            
            # [Step 3] 자동 보정 명령 생성 (Metal Widening)
            # 배선 저항을 낮추기 위해 해당 좌표의 Metal 폭을 넓히는 명령
            fix = {
                "action": "WIDEN_METAL",
                "target_net": entry['net'],
                "coord": entry['coordinate'],
                "params": {"add_width": "0.2um", "layer": "M1"}
            }
            correction_commands.append(fix)
            
        # 2. 신뢰성이 낮은 Single Via 탐지
        elif entry['type'] == "SINGLE_VIA":
            print(f"[주의] Single Via 발견 (위치: {entry['coordinate']})")
            
            # [Step 3] 자동 보정 명령 생성 (Redundant Via Insertion)
            # 단일 비아를 이중 비아(Double Via)로 보강하여 저항 감소 및 수율 향상
            fix = {
                "action": "ADD_REDUNDANT_VIA",
                "target_net": entry['net'],
                "coord": entry['coordinate'],
                "params": {"via_type": "VIA12_DOUBLE"}
            }
            correction_commands.append(fix)
            
    return correction_commands

# 스크립트 실행
fix_list = run_design_enhancer_pvr(analysis_data)

# [Step 4] 결과 요약 및 레이아웃 수정 리포트 생성
print("\n--- 자동 보정 리스트 (Layout Fix List) ---")
for i, f in enumerate(fix_list, 1):
    print(f"{i}. {f['action']} 수행 -> 좌표: {f['coord']} | 상세: {f['params']}")

# 결과를 JSON 파일로 저장 (실제 레이아웃 툴에 입력값으로 활용 가능)
with open('dfm_pvr_fix_report.json', 'w') as f:
    json.dump(fix_list, f, indent=4)