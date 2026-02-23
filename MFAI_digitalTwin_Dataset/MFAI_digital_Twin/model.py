import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination


class DiabetesDigitalTwin:

    def __init__(self):

        # Load processed data
        self.data = pd.read_csv("../data/processed_diabetes.csv")

        print("Processed data loaded successfully")

        # Define Bayesian Network Structure
        self.model = BayesianNetwork([

            ("Sleep", "Stress"),

            ("Exercise", "InsulinSensitivity"),

            ("InsulinSensitivity", "GlucoseLevel"),

            ("Medication", "GlucoseLevel"),

            ("Stress", "GlucoseLevel"),

            ("BMI_Level", "GlucoseLevel")

        ])

        # Train model (learn probabilities)
        self.model.fit(
            self.data,
            estimator=MaximumLikelihoodEstimator
        )

        print("Bayesian Network trained successfully")

        # Create inference engine
        self.inference = VariableElimination(self.model)


    # Risk prediction function
    def predict_risk(self, evidence):

        result = self.inference.query(
            variables=["GlucoseLevel"],
            evidence=evidence
        )

        return result


# Test the model
if __name__ == "__main__":

    twin = DiabetesDigitalTwin()

    # Example scenario
    evidence = {
        "Sleep": "Poor",
        "Exercise": "Low",
        "Medication": "No",
        "Stress": "High",
        "BMI_Level": "High",
        "InsulinSensitivity": "Low"
    }

    result = twin.predict_risk(evidence)

    print("\nRisk Prediction:")
    print(result)