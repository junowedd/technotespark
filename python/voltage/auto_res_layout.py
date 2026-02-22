from cni.drc import *
from cni.pycell.util import *
from cni.pycell.wrapper import *
import pandas as pd

class AutoAdjustResistor(PyCell):
    @classmethod
    def defineParam(cls, specs):
        # 기본 파라미터 설정
        specs.add('target_res', 10000.0)  # 목표 저항 10kOhm
        specs.add('w', 2.0)               # 너비 2um固定
        specs.add('sheet_res', 50.0)      # 공정 시트 저항 (Ohm/sq)

    def display(self):
        # 1. 시뮬레이션 리포트 분석 데이터 읽기
        try:
            df = pd.read_csv('sim_summary.txt')
            # 분석 결과 Vref가 목표보다 낮으면 저항을 줄이고, 높으면 늘리는 보정 로직
            # 예: 보정 계수 = (평균 측정값 / 목표값)
            cal_factor = df['Vref_Avg'].mean() / 1.250
        except:
            cal_factor = 1.0  # 파일이 없으면 기본값 사용
            print("Warning: Simulation report not found. Using default scaling.")

        # 2. 보정된 길이(L) 계산
        # R = Rs * (L/W) -> L = (R * W) / Rs
        base_l = (self.target_res * self.w) / self.sheet_res
        adjusted_l = base_l * cal_factor  # 분석 결과 반영

        # 3. 레이아웃 생성 (180nm BCD Poly Layer)
        poly_layer = Layer('POLY', 'drawing')
        res_body = Box(0, 0, self.w, adjusted_l)
        self.addRect(poly_layer, res_body)

        # 4. 컨택(Contact) 및 메탈 연결 자동 생성
        cont_layer = Layer('CONT', 'drawing')
        metal_layer = Layer('MET1', 'drawing')
        
        # 상단/하단 컨택 배치 루틴 (생략 가능)
        self.addRect(metal_layer, Box(0, -1, self.w, 0)) # Bottom Port
        self.addRect(metal_layer, Box(0, adjusted_l, self.w, adjusted_l + 1)) # Top Port

        print(f"Layout Generated: Target Res with Cal Factor {cal_factor:.3f}, Final L={adjusted_l:.2f}um")

# 이 클래스는 OpenAccess 환경에서 컴파일되어 Virtuoso/Custom Compiler에서 호출됩니다.