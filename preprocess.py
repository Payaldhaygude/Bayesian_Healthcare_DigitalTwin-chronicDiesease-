import pandas as pd
import numpy as np

def preprocess_data(input_path="../data/diabetes.csv",
                    output_path="../data/processed_diabetes.csv"):

    df = pd.read_csv(input_path)
    print("Loaded:", df.shape)

    # ── Outcome node ──────────────────────────────────────────────────────────
    df["GlucoseLevel"] = df["Glucose"].apply(
        lambda x: "High" if x > 140 else "Normal"
    )

    # ── BMI Level (3 states) ──────────────────────────────────────────────────
    df["BMI_Level"] = df["BMI"].apply(
        lambda x: "Obese" if x > 30 else ("Overweight" if x > 25 else "Normal")
    )

    # ── Insulin Sensitivity (2 states) ───────────────────────────────────────
    df["InsulinSensitivity"] = df["Insulin"].apply(
        lambda x: "Low" if x < 80 else "Normal"
    )

    # ── Stress — derived from BloodPressure (real physiological proxy) ────────
    df["Stress"] = df["BloodPressure"].apply(
        lambda x: "High" if x > 80 else "Low"
    )

    # ── Diet — derived from Glucose (real causal link) ────────────────────────
    df["Diet"] = df["Glucose"].apply(
        lambda x: "HighCarb" if x > 120 else "LowCarb"
    )

    # ── Sleep — derived from Age + BMI ───────────────────────────────────────
    df["Sleep"] = df.apply(
        lambda r: "Poor"     if (r["Age"] > 45 or r["BMI"] > 32)
        else      "Moderate" if r["Age"] > 30
        else      "Good",
        axis=1
    )

    # ── Exercise — derived from BMI (inverse proxy) ──────────────────────────
    df["Exercise"] = df["BMI"].apply(
        lambda x: "Low"    if x > 30
        else      "Medium" if x > 25
        else      "High"
    )

    # ── Medication — derived from DPF + Glucose ──────────────────────────────
    df["Medication"] = df.apply(
        lambda r: "Yes" if (r["DiabetesPedigreeFunction"] > 0.5
                            and r["Glucose"] > 140)
        else "No",
        axis=1
    )

    cols = ["Sleep", "Diet", "Exercise", "Stress", "Medication",
            "BMI_Level", "InsulinSensitivity", "GlucoseLevel"]

    out = df[cols].copy()
    out.to_csv(output_path, index=False)

    print("\n── Distributions ──")
    for c in cols:
        print(f"  {c}: {dict(out[c].value_counts())}")

    print(f"\nSaved → {output_path}")
    return out


if __name__ == "__main__":
    preprocess_data()