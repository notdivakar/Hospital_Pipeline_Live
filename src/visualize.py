import os
import matplotlib.pyplot as plt
import pandas as pd


def generate_hr_trend(output_path: str = "visualizations/hr_trend.png") -> None:
  """Creates a dummy patient vitals DataFrame and generates a multi-line heart rate trend plot,

  saving it to the specified path without displaying it.
  """
  # Create dummy dataframe
  data = {
      "patient_id": [
          "P001",
          "P001",
          "P001",
          "P002",
          "P002",
          "P002",
          "P003",
          "P003",
          "P003",
      ],
      "timestamp": pd.to_datetime([
          "2026-11-16 08:00:00",
          "2026-11-16 12:00:00",
          "2026-11-16 16:00:00",
          "2026-11-16 08:00:00",
          "2026-11-16 12:00:00",
          "2026-11-16 16:00:00",
          "2026-11-16 08:00:00",
          "2026-11-16 12:00:00",
          "2026-11-16 16:00:00",
      ]),
      "hr": [74, 82, 79, 88, 95, 91, 112, 125, 118],
  }
  df = pd.DataFrame(data)

  # Ensure target directory exists
  os.makedirs(os.path.dirname(output_path), exist_ok=True)

  # Initialize plot
  plt.figure(figsize=(10, 6))

  # Plot a separate colored line for each unique patient_id
  for patient_id, group in df.groupby("patient_id"):
    plt.plot(
        group["timestamp"],
        group["hr"],
        marker="o",
        linestyle="-",
        linewidth=2,
        label=f"Patient {patient_id}",
    )

  # Format plot
  plt.title("Heart Rate (HR) Trend Over Time", fontsize=14, fontweight="bold")
  plt.xlabel("Timestamp", fontsize=12)
  plt.ylabel("Heart Rate (hr)", fontsize=12)
  plt.legend(title="Patient ID")
  plt.grid(True, linestyle="--", alpha=0.5)
  plt.xticks(rotation=45)
  plt.tight_layout()

  # Save to disk and close figure (no plt.show())
  plt.savefig(output_path, dpi=300)
  plt.close()

  print(f"Plot successfully saved to {output_path}")


if __name__ == "__main__":
  generate_hr_trend()