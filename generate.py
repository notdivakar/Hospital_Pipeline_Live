import pandas as pd
import numpy as np
import time
import os

def generate_dummy_data():
    os.makedirs('data', exist_ok=True)
    patient_ids = [f"P{i:03d}" for i in range(1, 51)]
    
    # 1. EHR Data
    ehr = pd.DataFrame({'patientId': patient_ids, 'age': np.random.randint(20, 80, 50)})
    ehr.to_csv('data/ehr.csv', index=False)
    
    # 2. Vitals Data (Forcing exact column names: hr, ox, sys, dia)
    vitals = pd.DataFrame({
        'patientId': np.random.choice(patient_ids, 50),
        'timestamp': [int(time.time()) - np.random.randint(0, 10000) for _ in range(50)],
        'hr': np.random.randint(60, 130, 50),
        'ox': np.random.randint(85, 100, 50),
        'sys': np.random.randint(90, 180, 50),
        'dia': np.random.randint(60, 120, 50)
    })
    vitals.to_csv('data/vitals.csv', index=False)
    
    # 3. Labs Data
    labs = pd.DataFrame({
        'patientId': np.random.choice(patient_ids, 50),
        'timestamp': [int(time.time()) - np.random.randint(0, 10000) for _ in range(50)],
        'test': np.random.choice(['blood_sugar', 'cholesterol'], 50),
        'value': np.random.uniform(50.0, 200.0, 50)
    })
    labs.to_csv('data/labs.csv', index=False)
    
    print("Fixed dummy data generated successfully with correct columns.")

if __name__ == "__main__":
    generate_dummy_data()