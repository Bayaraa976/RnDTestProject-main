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
    
    # Headers matching the request more closely
    summary_report = "# NASM Overhead Squat Assessment Results\n\n"
    summary_report += "| Subject | Knee Rotation (L/R Deg) | Waist Bending (Deg) | Upper Body Bending (Deg) | Assessment |\n"
    summary_report += "|---|---|---|---|---|\n"
    
    metrics_calc = NASMMetrics()
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        print(f"Processing {filename}...")
        
        try:
            # 1. Load
            df_raw = load_data(filepath)
            
            # 2. Preprocess (Interpolate gaps)
            df_interp = preprocess_data(df_raw)
            
            # 3. Filter (Median Despike + BW Low-pass)
            # Using 6Hz cutoff typical for human movement
            df_filtered = filter_dataframe(df_interp, cutoff=6.0, fs=100.0)
            
            # 4. Calculate Metrics
            metrics_df = metrics_calc.process_subject(df_filtered)
            
            # 5. Analyze Results
            # Strategies for "Max Deviation":
            # For simple assessment, we look at the peak values during the squat.
            # Usually, the squat phase is the middle part. 
            # Assuming the file contains one rep or we just look at extrema.
            
            # Knee Valgus (+Inward) / Varus (-Outward)
            l_valgus_max = metrics_df['l_knee_angle'].max()
            l_varus_min = metrics_df['l_knee_angle'].min() # if negative
            r_valgus_max = metrics_df['r_knee_angle'].max()
            r_varus_min = metrics_df['r_knee_angle'].min()
            
            # Select the most significant deviation for reporting
            # E.g. if Valgus is 15 and Varus is -2, report 15.
            # If Valgus is 2 and Varus is -15, report -15.
            def get_max_abs(pos, neg):
                if abs(neg) > abs(pos):
                    return neg
                return pos
                
            l_knee_dev = get_max_abs(l_valgus_max, l_varus_min)
            r_knee_dev = get_max_abs(r_valgus_max, r_varus_min)
            
            # Waist Bending (Lumbar Extension/Arch)
            lumbar_max = metrics_df['lumbar_extension'].max() # Arch
            
            # Upper Body Bending (Torso Lean)
            lean_max = metrics_df['torso_lean'].max()
            
            # Assessment Logic (Thresholds need tuning, using heuristics)
            assessment_notes = []
            
            # Knees
            if l_knee_dev > 10 or r_knee_dev > 10:
                assessment_notes.append("Knees Move Inward")
            if l_knee_dev < -10 or r_knee_dev < -10:
                assessment_notes.append("Knees Move Outward")
                
            # Lumbar
            if lumbar_max > 15: 
                assessment_notes.append("Low Back Arch")
            
            # Torso
            if lean_max > 30:
                assessment_notes.append("Torso Lean Forward") # aka Excessive Lean
                
            assessment_str = ", ".join(assessment_notes) if assessment_notes else "Normal"
            
            summary_report += f"| {filename} | L:{l_knee_dev:.1f}, R:{r_knee_dev:.1f} | {lumbar_max:.1f} | {lean_max:.1f} | {assessment_str} |\n"
            
            # Save individual results
            # Flattening to requested columns mapping
            # "Knee Rotation" -> using Computed Valgus Angle
            metrics_df['l_knee_rotation'] = metrics_df['l_knee_angle']
            metrics_df['r_knee_rotation'] = metrics_df['r_knee_angle']
            metrics_df['waist_bending'] = metrics_df['lumbar_extension']
            metrics_df['upper_body_bending'] = metrics_df['torso_lean']
            
            out_df = metrics_df[['l_knee_rotation', 'r_knee_rotation', 'waist_bending', 'upper_body_bending']]
            
            result_path = os.path.join(output_dir, f"results_{filename.replace('.xlsx', '.csv')}")
            out_df.to_csv(result_path, index=False)
            
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
            import traceback
            traceback.print_exc()
            summary_report += f"| {filename} | ERROR | ERROR | ERROR | {e} |\n"

    # Write Report
    report_path = os.path.join(output_dir, 'results_report.md')
    with open(report_path, 'w') as f:
        f.write(summary_report)
    
    print(f"\nAnalysis complete. Report saved to {report_path}")
    print(summary_report)

if __name__ == "__main__":
    main()
