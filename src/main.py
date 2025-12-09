import os
import pandas as pd
import numpy as np
from src.data_loader import load_data, preprocess_data
from src.filters import filter_dataframe
from src.nasm_metrics import NASMMetrics

def main():
    data_dir = 'data'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('.xlsx')])
    
    summary_report = "# NASM Overhead Squat Assessment Results\n\n"
    summary_report += "| Subject | L.Knee Valgus (Deg) | R.Knee Valgus (Deg) | Max Lumbar Arch (Deg) | Max Torso Lean (Deg) | Assessment |\n"
    summary_report += "|---|---|---|---|---|---|\n"
    
    metrics_calc = NASMMetrics()
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        print(f"Processing {filename}...")
        
        try:
            # 1. Load
            df_raw = load_data(filepath)
            
            # 2. Preprocess (Interpolate gaps)
            df_interp = preprocess_data(df_raw)
            
            # 3. Filter (Low-pass)
            # Filter all coordinate columns
            df_filtered = filter_dataframe(df_interp, cutoff=6.0, fs=100.0)
            
            # 4. Calculate Metrics
            metrics_df = metrics_calc.process_subject(df_filtered)
            
            # 5. Analyze Results (Simple Stats)
            # Knee Valgus: Max inward deviation? 
            # Our angle is 0 for straight. Larger angle = more deviation.
            # Let's take the 95th percentile to avoid outliers, or just Max.
            l_knee_max = metrics_df['l_knee_angle'].max()
            r_knee_max = metrics_df['r_knee_angle'].max()
            lumbar_max = metrics_df['lumbar_angle'].max()
            lean_max = metrics_df['torso_lean'].max()
            
            # Assessment Logic (Heuristic thresholds)
            assessment_notes = []
            if l_knee_max > 10 or r_knee_max > 10:
                assessment_notes.append("Knees Move Inward")
            if lumbar_max > 15: # Arbitrary threshold for "Excessive"
                assessment_notes.append("Low Back Arch")
            if lean_max > 30: # Arbitrary threshold
                assessment_notes.append("Excessive Lean")
                
            assessment_str = ", ".join(assessment_notes) if assessment_notes else "Normal"
            
            summary_report += f"| {filename} | {l_knee_max:.2f} | {r_knee_max:.2f} | {lumbar_max:.2f} | {lean_max:.2f} | {assessment_str} |\n"
            
            # Save individual results
            result_path = os.path.join(output_dir, f"results_{filename.replace('.xlsx', '.csv')}")
            metrics_df.to_csv(result_path, index=False)
            
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            summary_report += f"| {filename} | ERROR | ERROR | ERROR | ERROR | {e} |\n"

    # Write Report
    report_path = os.path.join(output_dir, 'results_report.md')
    with open(report_path, 'w') as f:
        f.write(summary_report)
    
    print(f"\nAnalysis complete. Report saved to {report_path}")
    print(summary_report)

if __name__ == "__main__":
    main()
