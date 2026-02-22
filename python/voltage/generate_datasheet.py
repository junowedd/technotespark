import pandas as pd
import numpy as np
from datetime import datetime

def create_html_report():
    # 1. Load data from previous analysis steps
    try:
        df_corner = pd.read_csv('sim_summary.txt')
        df_mc = pd.read_csv('mc_summary.txt')
    except FileNotFoundError:
        print("Error: Required data files (sim_summary.txt or mc_summary.txt) not found.")
        return

    # 2. Calculate Key Performance Indicators (KPIs)
    vref_typ = df_mc['Vref'].mean()
    vref_std = df_mc['Vref'].std()
    vref_min = df_corner['Vref_Avg'].min()
    vref_max = df_corner['Vref_Avg'].max()
    
    # Yield Calculation based on +/- 30mV spec
    lsl, usl = 1.220, 1.280
    yield_val = (len(df_mc[(df_mc['Vref'] >= lsl) & (df_mc['Vref'] <= usl)]) / len(df_mc)) * 100
    
    # 3. Define HTML Content with CSS for Professional Look
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>180nm BCD IP Datasheet</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: auto; padding: 40px; background-color: #f0f2f5; }}
            .container {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            header {{ border-bottom: 3px solid #0056b3; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
            h1 {{ color: #0056b3; margin: 0; }}
            .status-tag {{ background: #28a745; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
            .summary-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
            .card {{ background: #e9ecef; padding: 20px; border-radius: 8px; text-align: center; }}
            .card-val {{ font-size: 22px; font-weight: bold; color: #0056b3; }}
            table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
            th, td {{ padding: 12px; border: 1px solid #dee2e6; text-align: left; }}
            th {{ background-color: #0056b3; color: white; }}
            .image-section {{ display: flex; gap: 20px; margin-top: 40px; }}
            .image-box {{ flex: 1; text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }}
            img {{ max-width: 100%; height: auto; }}
            footer {{ margin-top: 50px; font-size: 0.8em; color: #777; border-top: 1px solid #ccc; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div>
                    <h1>ams OSRAM 180nm BCD IP</h1>
                    <p>Bandgap Reference Block (BGR01)</p>
                </div>
                <div class="status-tag">Foundry Ready</div>
            </header>

            <section class="summary-grid">
                <div class="card"><div class="card-val">{yield_val:.1f}%</div>Estimated Yield</div>
                <div class="card"><div class="card-val">{vref_typ:.3f}V</div>Typical Vout</div>
                <div class="card"><div class="card-val">{(vref_max - vref_min)*1000:.1f}mV</div>Total Margin</div>
                <div class="card"><div class="card-val">{vref_std*1000:.2f}mV</div>Std. Deviation</div>
            </section>

            <h2>1. Electrical Performance Summary</h2>
            <table>
                <tr><th>Parameter</th><th>Symbol</th><th>Min</th><th>Typ</th><th>Max</th><th>Unit</th><th>Note</th></tr>
                <tr><td>Supply Voltage</td><td>Vdd</td><td>1.62</td><td>1.80</td><td>1.98</td><td>V</td><td>+/- 10% Range</td></tr>
                <tr><td>Reference Voltage</td><td>Vref</td><td>{vref_min:.3f}</td><td>{vref_typ:.3f}</td><td>{vref_max:.3f}</td><td>V</td><td>Full PVT Range</td></tr>
                <tr><td>Temperature Range</td><td>Tj</td><td>-40</td><td>27</td><td>125</td><td>&deg;C</td><td>Automotive Grade 1</td></tr>
                <tr><td>Current Consumption</td><td>Idd</td><td>-</td><td>110</td><td>135</td><td>nA</td><td>Static Current</td></tr>
            </table>

            <h2>2. Verification Analysis</h2>
            <div class="image-section">
                <div class="image-box">
                    <img src="voltage_margin_plot.png" alt="Corner Analysis">
                    <p><strong>Figure 1:</strong> Voltage Margin vs. Temperature</p>
                </div>
                <div class="image-box">
                    <img src="mc_analysis_report.png" alt="Yield Analysis">
                    <p><strong>Figure 2:</strong> Monte Carlo Statistical Distribution</p>
                </div>
            </div>

            <footer>
                <p>Confidential Proprietary Information - ams OSRAM Foundry Services</p>
                <p>Report Generated: {now} | Engineering Revision: 1.0.2</p>
            </footer>
        </div>
    </body>
    </html>
    """

    with open("IP_Technical_Datasheet.html", "w") as f:
        f.write(html_content)
    print("--- Success: 'IP_Technical_Datasheet.html' has been generated. ---")

if __name__ == "__main__":
    create_html_report()