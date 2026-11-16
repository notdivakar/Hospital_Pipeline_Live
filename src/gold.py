import os
import pandas as pd

def detect_anomalies(df: pd.DataFrame, output_path: str = "gold/anomalies.csv") -> pd.DataFrame:
    """
    Filters a patient vitals DataFrame for anomalous readings and saves them to a CSV.
    """
    # Define anomaly conditions
    condition = (
        (df["hr"] > 120) |
        (df["ox"] < 92) |
        (df["sys"] > 160) |
        (df["dia"] > 100)
    )
    
    # Filter the dataframe
    anomalies_df = df[condition].copy()
    
    # Ensure the target directory exists before saving
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save flagged rows to CSV
    anomalies_df.to_csv(output_path, index=False)
    
    print("Anomalies detected")
    return anomalies_df


# --- Test Logic with Dummy DataFrame ---
if __name__ == "__main__":
    dummy_data = {
        "patient_id": ["P001", "P002", "P003", "P004", "P005"],
        "hr": [75, 130, 88, 95, 70],       # P002 triggers hr > 120
        "ox": [98, 96, 89, 97, 95],        # P003 triggers ox < 92
        "sys": [120, 135, 118, 175, 122],  # P004 triggers sys > 160
        "dia": [80, 85, 76, 90, 105]       # P005 triggers dia > 100
    }
    
    test_df = pd.DataFrame(dummy_data)
    
    # Run the function
    flagged_patients = detect_anomalies(test_df)
    print("\nFlagged Rows:")
    print(flagged_patients)
