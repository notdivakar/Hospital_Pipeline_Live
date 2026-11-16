from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SILVER_DIR = PROJECT_ROOT / "silver"


def clean_vitals():
    """Clean vital-sign observations and save them to the silver layer."""
    vitals = pd.read_csv(DATA_DIR / "vitals.csv")
    vitals = vitals.rename(columns={"patientId": "patient_id"})
    vitals["timestamp"] = pd.to_datetime(vitals["timestamp"], unit="s")

    for column in ["hr", "ox", "sys", "dia"]:
        vitals[column] = pd.to_numeric(vitals[column], errors="coerce")

    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    vitals.to_csv(SILVER_DIR / "clean_vitals.csv", index=False)
    return vitals


def clean_labs():
    """Clean laboratory observations and save them to the silver layer."""
    labs = pd.read_csv(DATA_DIR / "labs.csv")
    labs = labs.rename(
        columns={
            "patientId": "patient_id",
            "test": "lab_test",
            "value": "lab_value",
        }
    )
    labs["timestamp"] = pd.to_datetime(labs["timestamp"], unit="s")
    labs["lab_value"] = pd.to_numeric(labs["lab_value"], errors="coerce")

    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    labs.to_csv(SILVER_DIR / "clean_labs.csv", index=False)
    return labs


def create_patient_master():
    """Create a one-record-per-patient master dataset from cleaned sources."""
    vitals = pd.read_csv(SILVER_DIR / "clean_vitals.csv",
                         parse_dates=["timestamp"])
    vitals = (
        vitals.sort_values("timestamp")
        .groupby("patient_id", as_index=False)
        .tail(1)
    )

    labs = pd.read_csv(SILVER_DIR / "clean_labs.csv",
                       parse_dates=["timestamp"])
    labs = (
        labs.sort_values("timestamp")
        .groupby("patient_id", as_index=False)
        .tail(1)
    )

    ehr = pd.read_csv(DATA_DIR / "ehr.csv")
    ehr = ehr.rename(columns={"patientId": "patient_id"})

    patient_master = ehr.merge(vitals, on="patient_id", how="outer")
    patient_master = patient_master.merge(labs, on="patient_id", how="outer")

    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    patient_master.to_csv(SILVER_DIR / "patient_master.csv", index=False)

    return patient_master
