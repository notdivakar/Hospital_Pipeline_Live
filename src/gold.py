import pandas as pd
import os

def detect_anomalies():
    # Read the real file created by the Silver layer
    df = pd.read_csv('silver/patient_master.csv')
    
    # Apply the anomaly logic
    anomalies = df[(df['hr'] > 120) | (df['ox'] < 92) | (df['sys'] > 160) | (df['dia'] > 100)]
    
    # Save the output
    os.makedirs('gold', exist_ok=True)
    anomalies.to_csv('gold/anomalies.csv', index=False)
    print("Gold layer anomalies detected and saved.")
