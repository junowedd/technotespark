import json
import argparse
import os


class DFMPVREnhancer:
    def __init__(self, threshold_mv=40):
        self.threshold_mv = threshold_mv
        self.data = []
        self.fix_plan = []

    # -----------------------------
    # Step 1: Load JSON Input
    # -----------------------------
    def load_data(self, input_file):
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        with open(input_file, 'r') as f:
            self.data = json.load(f)

        print(f"[INFO] Loaded {len(self.data)} entries from {input_file}")

    # -----------------------------
    # Step 2: Analyze Hotspots
    # -----------------------------
        # -----------------------------
    # Step 2: Analyze Hotspots
    # -----------------------------
    def analyze(self):
        print(f"[INFO] Running analysis (Threshold: {self.threshold_mv} mV)")

        for entry in self.data:

            if not isinstance(entry, dict):
                print(f"[WARNING] Skipping non-dict entry: {entry}")
                continue

            if "type" not in entry:
                print(f"[WARNING] Skipping entry (missing 'type'): {entry}")
                continue

            if entry["type"] == "IR_DROP":
                if "drop_mv" not in entry or "net" not in entry:
                    print(f"[WARNING] Incomplete IR_DROP entry: {entry}")
                    continue
                self._handle_ir_drop(entry)

            elif entry["type"] == "SINGLE_VIA":
                if "net" not in entry:
                    print(f"[WARNING] Incomplete SINGLE_VIA entry: {entry}")
                    continue
                self._handle_single_via(entry)

            else:
                print(f"[INFO] Unknown type skipped: {entry['type']}")
    
    

    # -----------------------------
    # IR Drop Handling
    # -----------------------------
    def _handle_ir_drop(self, entry):
        if entry["drop_mv"] > self.threshold_mv:
            fix = {
                "action": "WIDEN_METAL",
                "target_net": entry["net"],
                "coord": entry["coordinate"],
                "params": {
                    "add_width": "0.2um",
                    "reason": f"IR drop {entry['drop_mv']}mV > {self.threshold_mv}mV"
                }
            }
            self.fix_plan.append(fix)

    # -----------------------------
    # Single Via Handling
    # -----------------------------
    def _handle_single_via(self, entry):
        fix = {
            "action": "ADD_REDUNDANT_VIA",
            "target_net": entry["net"],
            "coord": entry["coordinate"],
            "params": {
                "via_type": "DOUBLE",
                "reason": "Single Via Reliability"
            }
        }
        self.fix_plan.append(fix)

    # -----------------------------
    # Step 3: Export JSON Report
    # -----------------------------
    def export_json(self, output_file):
        with open(output_file, 'w') as f:
            json.dump(self.fix_plan, f, indent=4)

        print(f"[INFO] Fix report saved to {output_file}")

    # -----------------------------
    # Step 4: Export TCL Script
    # -----------------------------
    def export_tcl(self, tcl_file):
        with open(tcl_file, 'w') as f:
            for fix in self.fix_plan:
                if fix["action"] == "WIDEN_METAL":
                    cmd = (
                        f"# {fix['params']['reason']}\n"
                        f"db_enhance_metal -net {fix['target_net']} "
                        f"-coord {fix['coord'][0]} {fix['coord'][1]} "
                        f"-add_width 0.2\n\n"
                    )
                elif fix["action"] == "ADD_REDUNDANT_VIA":
                    cmd = (
                        f"# {fix['params']['reason']}\n"
                        f"db_insert_via -net {fix['target_net']} "
                        f"-coord {fix['coord'][0]} {fix['coord'][1]} "
                        f"-type DOUBLE\n\n"
                    )
                f.write(cmd)

        print(f"[INFO] TCL script saved to {tcl_file}")


# =====================================
# CLI Entry
# =====================================
def main():
    parser = argparse.ArgumentParser(description="DFM PVR Enhancer Automation Tool")

    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--threshold", type=int, default=40, help="IR drop threshold (mV)")
    parser.add_argument("--output", default="dfm_pvr_fix_report.json", help="Output JSON report")
    parser.add_argument("--export-tcl", help="Export TCL script file")

    args = parser.parse_args()

    enhancer = DFMPVREnhancer(threshold_mv=args.threshold)
    enhancer.load_data(args.input)
    enhancer.analyze()
    enhancer.export_json(args.output)

    if args.export_tcl:
        enhancer.export_tcl(args.export_tcl)

    print("[STATUS] DFM PVR Optimization Completed.")


if __name__ == "__main__":
    main()