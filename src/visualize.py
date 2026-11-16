import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_hr_trend():
    # Read the cleaned vitals from the Silver layer
    df = pd.read_csv('silver/clean_vitals.csv')
    
    plt.figure(figsize=(10, 6))
    for patient_id, group in df.groupby('patient_id'):
        plt.plot(group['timestamp'], group['hr'], marker='o', label=patient_id)
        
    plt.title('Heart Rate Trend by Patient')
    plt.xlabel('Time')
    plt.ylabel('Heart Rate (bpm)')
    
    os.makedirs('visualizations', exist_ok=True)
    plt.savefig('visualizations/hr_trend.png')
    plt.close()
    print("Visualization saved to visualizations/hr_trend.png")