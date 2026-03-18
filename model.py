import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination


class DiabetesDigitalTwin:

    HIGH_THRESHOLD   = 0.60
    MEDIUM_THRESHOLD = 0.35

    def __init__(self, data_path="../data/processed_diabetes.csv"):

        # ── Load processed data ───────────────────────────────────────────────
        try:
            self.data = pd.read_csv(data_path)
            print(f"Data loaded: {self.data.shape}")
        except FileNotFoundError:
            print(f"ERROR: File not found at {data_path}")
            self.data      = None
            self.inference = None
            return

        # ── Bayesian Network structure ────────────────────────────────────────
        # All causal edges including Diet (was missing in original)
        self.model = DiscreteBayesianNetwork([
            ("Sleep",              "Stress"),
            ("Diet",               "GlucoseLevel"),
            ("Exercise",           "InsulinSensitivity"),
            ("BMI_Level",          "InsulinSensitivity"),
            ("InsulinSensitivity", "GlucoseLevel"),
            ("Medication",         "GlucoseLevel"),
            ("Stress",             "GlucoseLevel"),
            ("BMI_Level",          "GlucoseLevel"),
        ])

        # ── Fit with BayesianEstimator (handles class imbalance better) ───────
        self.model.fit(
            data=self.data,
            estimator=BayesianEstimator,
            prior_type="BDeu",
            equivalent_sample_size=10
        )
        print("Bayesian Network trained successfully!")

        self.inference = VariableElimination(self.model)

    # ── Safe probability extraction (works on ALL pgmpy versions) ────────────
    def _extract_high_prob(self, result):
        """
        pgmpy returns different types depending on version:
          Older  -> plain dict  {"High": 0.6, "Normal": 0.4}
          Middle -> DiscreteFactor with .values + .state_names
          Newer  -> DiscreteFactor with .get_value()
        This method handles all three cases.
        """
        if isinstance(result, dict):
            # Older pgmpy
            return float(result.get("High", 0.0)), float(result.get("Normal", 1.0))

        if hasattr(result, "get_value"):
            # Newer pgmpy
            return (float(result.get_value(GlucoseLevel="High")),
                    float(result.get_value(GlucoseLevel="Normal")))

        if hasattr(result, "values") and hasattr(result, "state_names"):
            # Middle pgmpy
            states      = list(result.state_names["GlucoseLevel"])
            high_prob   = float(result.values[states.index("High")])
            normal_prob = float(result.values[states.index("Normal")])
            return high_prob, normal_prob

        raise ValueError(f"Unknown pgmpy result type: {type(result)}")

    # ── Main prediction method ────────────────────────────────────────────────
    def predict_risk(self, evidence: dict):
        """
        Run inference and return a result dict:
        {
          "high_prob"  : float,   P(GlucoseLevel=High)
          "normal_prob": float,   P(GlucoseLevel=Normal)
          "risk_level" : str,     "High" | "Moderate" | "Low"
          "risk_pct"   : float,   percentage 0-100
          "message"    : str,
        }
        Returns None if inference fails.
        """
        if self.inference is None:
            print("Inference engine not initialized.")
            return None

        try:
            raw = self.inference.query(
                variables=["GlucoseLevel"],
                evidence=evidence,
                show_progress=False
            )

            high_prob, normal_prob = self._extract_high_prob(raw)
            risk_pct = round(high_prob * 100, 1)

            if high_prob >= self.HIGH_THRESHOLD:
                risk_level = "High"
                message    = f"High Risk of Diabetes ({risk_pct}%)"
            elif high_prob >= self.MEDIUM_THRESHOLD:
                risk_level = "Moderate"
                message    = f"Moderate Risk of Diabetes ({risk_pct}%)"
            else:
                risk_level = "Low"
                message    = f"Low Risk of Diabetes ({risk_pct}%)"

            return {
                "high_prob"  : high_prob,
                "normal_prob": normal_prob,
                "risk_level" : risk_level,
                "risk_pct"   : risk_pct,
                "message"    : message,
            }

        except Exception as e:
            print("Error during prediction:", e)
            return None

    # ── What-if simulation ────────────────────────────────────────────────────
    def what_if(self, base_evidence: dict, changed_evidence: dict):
        """
        Compares baseline risk vs scenario risk.
        Returns delta (positive = risk increased, negative = risk decreased).
        """
        base = self.predict_risk(base_evidence)
        new  = self.predict_risk(changed_evidence)
        if base is None or new is None:
            return None

        delta = new["high_prob"] - base["high_prob"]
        print(f"\n── What-If Analysis ──")
        print(f"Baseline : {base['risk_pct']}%")
        print(f"Scenario : {new['risk_pct']}%")
        print(f"Change   : {'+' if delta >= 0 else ''}{round(delta * 100, 1)}%")
        return {
            "baseline": base["high_prob"],
            "scenario": new["high_prob"],
            "delta"   : delta
        }


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    twin = DiabetesDigitalTwin()

    print("\n=== Test 1: High-risk profile ===")
    high_risk = {
        "Sleep":              "Poor",
        "Diet":               "HighCarb",
        "Exercise":           "Low",
        "Stress":             "High",
        "Medication":         "No",
        "BMI_Level":          "Obese",
        "InsulinSensitivity": "Low",
    }
    print(twin.predict_risk(high_risk))

    print("\n=== Test 2: Low-risk profile ===")
    low_risk = {
        "Sleep":              "Good",
        "Diet":               "LowCarb",
        "Exercise":           "High",
        "Stress":             "Low",
        "Medication":         "Yes",
        "BMI_Level":          "Normal",
        "InsulinSensitivity": "Normal",
    }
    print(twin.predict_risk(low_risk))

    print("\n=== What-If: skip medication ===")
    scenario = {**low_risk, "Medication": "No"}
    twin.what_if(low_risk, scenario)