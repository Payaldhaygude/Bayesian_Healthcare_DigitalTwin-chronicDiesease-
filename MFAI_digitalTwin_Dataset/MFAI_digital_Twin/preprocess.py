import pandas as pd
import numpy as np

def preprocess_data():

    # Load dataset from parent folder
    df = pd.read_csv("../data/diabetes.csv")

    print("Original Columns:")
    print(df.columns)

    # Convert Glucose → Category
    df["GlucoseLevel"] = df["Glucose"].apply(
        lambda x: "High" if x > 140 else "Normal"
    )

    # Convert BMI → Category
    df["BMI_Level"] = df["BMI"].apply(
        lambda x: "High" if x > 30 else "Normal"
    )

    # Age → Stress proxy
    df["Stress"] = df["Age"].apply(
        lambda x: "High" if x > 50 else "Low"
    )

    # Insulin → Insulin Sensitivity
    df["InsulinSensitivity"] = df["Insulin"].apply(
        lambda x: "Low" if x < 50 else "Normal"
    )

    # Add simulated lifestyle variables
    df["Sleep"] = np.random.choice(
        ["Poor", "Moderate", "Good"], size=len(df)
    )

    df["Exercise"] = np.random.choice(
        ["Low", "Medium", "High"], size=len(df)
    )

    df["Medication"] = np.random.choice(
        ["Yes", "No"], size=len(df)
    )

    # Select required columns
    processed_df = df[[
        "Sleep",
        "Exercise",
        "Medication",
        "Stress",
        "BMI_Level",
        "InsulinSensitivity",
        "GlucoseLevel"
    ]]

    # Save processed file to data folder
    processed_df.to_csv("../data/processed_diabetes.csv", index=False)

    print("\nProcessed dataset saved successfully!")
    print("Location: data/processed_diabetes.csv")

    return processed_df


if __name__ == "__main__":
    preprocess_data()