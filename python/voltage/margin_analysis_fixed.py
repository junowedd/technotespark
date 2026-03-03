# margin_analysis_fixed.py
# Purpose: Load sim_summary.txt and generate a Vref margin plot without GUI popups.
# Fixes:
#  - Removes duplicated imports / duplicated savefig calls
#  - Keeps a non-interactive backend (Agg) to avoid plt.show() warnings
#  - Replaces "℃" with "°C" to avoid missing glyph warnings
#  - Avoids incorrect plt.xlabel("Temperature ...") (x-axis is Vdd)
#  - Adds robust checks and clearer messages

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for scripts/CI/headless runs

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Seaborn is optional; script will fall back to matplotlib if missing.
try:
    import seaborn as sns
    _HAVE_SEABORN = True
except ImportError:
    _HAVE_SEABORN = False


def main():
    data_path = Path("sim_summary.txt")
    if not data_path.exists():
        print("ERROR: 'sim_summary.txt' not found. Run the simulation summary export first.")
        sys.exit(1)

    df = pd.read_csv(data_path)

    # Basic column validation (adjust names here if your file differs)
    required_cols = {"Vdd", "Temp", "Vref_Avg"}
    missing = required_cols - set(df.columns)
    if missing:
        print(f"ERROR: Missing required columns in sim_summary.txt: {sorted(missing)}")
        print(f"Found columns: {list(df.columns)}")
        sys.exit(1)

    # Spec setup
    target_vref = 1.25
    spec_limit = 0.05  # ±5%

    upper = target_vref * (1 + spec_limit)
    lower = target_vref * (1 - spec_limit)

    # Derived columns (optional)
    df["Vref_Error"] = df["Vref_Avg"] - target_vref
    df["Upper_Limit"] = upper
    df["Lower_Limit"] = lower

    # Plot
    plt.figure(figsize=(10, 6))

    if _HAVE_SEABORN:
        sns.set_style("whitegrid")
        sns.lineplot(
            data=df,
            x="Vdd",
            y="Vref_Avg",
            hue="Temp",
            marker="o",
        )
    else:
        for temp, g in df.groupby("Temp"):
            g_sorted = g.sort_values("Vdd")
            plt.plot(g_sorted["Vdd"], g_sorted["Vref_Avg"], marker="o", label=f"{temp}")
        plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)

    # Spec lines
    plt.axhline(upper, linestyle="--", linewidth=1, label="Upper Spec (±5%)")
    plt.axhline(lower, linestyle="--", linewidth=1, label="Lower Spec (±5%)")
    plt.axhline(target_vref, linestyle="-", linewidth=1, alpha=0.5, label="Target")

    plt.title("180nm BCD IP: Vref Voltage Margin Analysis", fontsize=15)
    plt.xlabel("Supply Voltage Vdd [V]", fontsize=12)
    plt.ylabel("Reference Voltage Vref [V]", fontsize=12)

    # Legend title: use °C (degree sign + C) to avoid missing glyph warnings
    plt.legend(title="Temperature [°C]", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()

    out_png = Path("voltage_margin_plot.png")
    plt.savefig(out_png, dpi=300)
    print(f"OK: Plot saved to '{out_png.resolve()}'")

    # Summary stats
    summary = df.groupby("Temp")["Vref_Avg"].agg(["min", "max", "mean"])
    print("\n--- Temperature Corner Summary (Vref_Avg) ---")
    print(summary)


if __name__ == "__main__":
    main()
