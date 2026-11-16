"""Generate small, reproducible synthetic hospital data files."""

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROW_COUNT = 50
RANDOM_SEED = 42
OUTPUT_DIR = Path(__file__).resolve().parent
START_TIME = datetime(2024, 1, 1, tzinfo=timezone.utc)


def random_timestamp(rng: random.Random) -> int:
    """Return a Unix timestamp within the two years starting January 2024."""
    timestamp = START_TIME + timedelta(
        days=rng.randint(0, 730),
        seconds=rng.randint(0, 86_399),
    )
    return int(timestamp.timestamp())


def write_csv(filename: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    """Write rows to a UTF-8 CSV next to this script."""
    with (OUTPUT_DIR / filename).open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_ehr(rng: random.Random) -> list[dict[str, object]]:
    diagnoses = [
        "hypertension",
        "Type 2 diabetes",
        "asthma",
        "URI",
        "hypertenison",
        "  migraine ",
        "N/A",
        "",
    ]
    medications = [
        "metformin",
        "Lisinopril 10 mg",
        "albuterol",
        "none",
        "UNKNOWN",
        "",
    ]
    allergies = ["none", "penicillin", "NKDA", "unknown", "  latex", ""]
    notes = [
        "follow-up scheduled",
        "pt reports feeling better",
        "History imported from legacy system",
        "check spelling",
        "N/A",
        "",
    ]
    ages: list[object] = [24, 37, 52, 68, " 45 ", "unknown", "N/A", ""]
    sexes = ["F", "female", "M", "Male", "unknown", ""]

    return [
        {
            "patient_id": f"P{rng.randint(1, 25):04d}",
            "encounter_id": f"E{index:05d}",
            "timestamp": random_timestamp(rng),
            "age": rng.choice(ages),
            "sex": rng.choice(sexes),
            "diagnosis": rng.choice(diagnoses),
            "medication": rng.choice(medications),
            "allergies": rng.choice(allergies),
            "notes": rng.choice(notes),
        }
        for index in range(1, ROW_COUNT + 1)
    ]


def generate_vitals(rng: random.Random) -> list[dict[str, object]]:
    heart_rates: list[object] = [62, 74, 88, 102, "72 bpm", " 81 ", "N/A", ""]
    systolic_values: list[object] = [108, 120, 139, 158, "120 mmHg", "unknown", ""]
    diastolic_values: list[object] = [66, 78, 89, 96, "80 mmHg", "N/A", ""]
    temperatures: list[object] = [36.7, 37.1, 38.2, "98.6 F", " 37 C ", "N/A", ""]
    oxygen_values: list[object] = [95, 97, 99, "98%", "0.96", "N/A", ""]
    respiratory_rates: list[object] = [12, 16, 20, "18 /min", "unknown", ""]

    return [
        {
            "patient_id": f"P{rng.randint(1, 25):04d}",
            "timestamp": random_timestamp(rng),
            "heart_rate": rng.choice(heart_rates),
            "systolic_bp": rng.choice(systolic_values),
            "diastolic_bp": rng.choice(diastolic_values),
            "temperature": rng.choice(temperatures),
            "oxygen_saturation": rng.choice(oxygen_values),
            "respiratory_rate": rng.choice(respiratory_rates),
        }
        for _ in range(ROW_COUNT)
    ]


def generate_labs(rng: random.Random) -> list[dict[str, object]]:
    lab_results = [
        ("glucose", ["88", "5.6", " 102 ", "<70", "N/A", ""], ["mg/dL", "mmol/L", "mg/dl", ""]),
        ("hemoglobin", ["12.8", "14.1", "16", "10.2", "unknown", ""], ["g/dL", "g/dl", ""]),
        ("sodium", ["138", "140", "132", "4.2", "N/A", ""], ["mmol/L", "mEq/L", ""]),
        ("creatinine", ["0.9", "1.1", "2.0", "88 umol/L", "N/A", ""], ["mg/dL", "mg/dl", ""]),
        ("WBC", ["6.4", "8.1", "12.5", " 5.2 ", "?", ""], ["10^3/uL", "K/uL", ""]),
    ]
    flags = ["normal", "HIGH", "low", "H", "L", "N/A", ""]

    rows = []
    for _ in range(ROW_COUNT):
        test_name, results, units = rng.choice(lab_results)
        rows.append(
            {
                "patient_id": f"P{rng.randint(1, 25):04d}",
                "timestamp": random_timestamp(rng),
                "test_name": rng.choice([test_name, test_name.upper(), f" {test_name} "]),
                "result": rng.choice(results),
                "unit": rng.choice(units),
                "reference_range": rng.choice(["70-99", "4.0-10.0", "135-145", "0.6-1.2", "see notes", ""]),
                "flag": rng.choice(flags),
            }
        )
    return rows


def main() -> None:
    rng = random.Random(RANDOM_SEED)
    datasets = [
        (
            "ehr.csv",
            ["patient_id", "encounter_id", "timestamp", "age", "sex", "diagnosis", "medication", "allergies", "notes"],
            generate_ehr(rng),
        ),
        (
            "vitals.csv",
            ["patient_id", "timestamp", "heart_rate", "systolic_bp", "diastolic_bp", "temperature", "oxygen_saturation", "respiratory_rate"],
            generate_vitals(rng),
        ),
        (
            "labs.csv",
            ["patient_id", "timestamp", "test_name", "result", "unit", "reference_range", "flag"],
            generate_labs(rng),
        ),
    ]

    for filename, fieldnames, rows in datasets:
        write_csv(filename, fieldnames, rows)
        print(f"Wrote {len(rows)} rows to {OUTPUT_DIR / filename}")


if __name__ == "__main__":
    main()