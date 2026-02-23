// Predict function called when button is clicked
async function predict() {

    // Get result element
    const result = document.getElementById("result");

    // Read input values
    const data = {

        Pregnancies: parseFloat(document.getElementById("Pregnancies").value),
        Glucose: parseFloat(document.getElementById("Glucose").value),
        BloodPressure: parseFloat(document.getElementById("BloodPressure").value),
        SkinThickness: parseFloat(document.getElementById("SkinThickness").value),
        Insulin: parseFloat(document.getElementById("Insulin").value),
        BMI: parseFloat(document.getElementById("BMI").value),
        DiabetesPedigreeFunction: parseFloat(document.getElementById("DPF").value),
        Age: parseFloat(document.getElementById("Age").value)

    };

    // Validate inputs
    for (let key in data) {

        if (isNaN(data[key])) {

            result.innerHTML = "⚠ Please fill all fields correctly";
            result.style.color = "orange";
            return;

        }

    }

    try {

        // Show loading
        result.innerHTML = "Predicting...";
        result.style.color = "#333";

        // Send POST request to Flask backend
        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

        const output = await response.json();

        // Show result
        if (output.prediction == 1) {

            result.innerHTML = "⚠ High Risk of Diabetes";
            result.style.color = "red";

        } else {

            result.innerHTML = "✅ Low Risk of Diabetes";
            result.style.color = "green";

        }

    } catch (error) {

        console.error(error);

        result.innerHTML = "❌ Server Error";
        result.style.color = "red";

    }

}