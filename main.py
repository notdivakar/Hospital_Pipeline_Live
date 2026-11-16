from src import bronze, silver, gold, visualize

def main():
    print("--- Running Bronze Layer ---")
    bronze.ingest_raw_data()
    
    print("--- Running Silver Layer ---")
    silver.clean_vitals()
    silver.clean_labs()
    silver.create_patient_master()
    
    print("--- Running Gold Layer ---")
    gold.detect_anomalies()
    
    print("--- Generating Visualizations ---")
    visualize.generate_hr_trend()
    
    print("Pipeline Execution Complete!")

if __name__ == "__main__":
    main()