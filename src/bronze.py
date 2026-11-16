from pathlib import Path
import shutil

import pandas as pd


def ingest_raw_data():
    project_dir = Path(__file__).resolve().parent.parent
    data_dir = project_dir / "data"
    bronze_dir = project_dir / "bronze"
    bronze_dir.mkdir(parents=True, exist_ok=True)

    for filename in ("ehr.csv", "vitals.csv", "labs.csv"):
        source = data_dir / filename
        pd.read_csv(source)
        shutil.copyfile(source, bronze_dir / filename)
    print("Bronze layer complete")


if __name__ == "__main__":
    ingest_raw_data()