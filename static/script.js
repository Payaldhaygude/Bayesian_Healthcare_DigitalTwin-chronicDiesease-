function predict() {
    const result = document.getElementById("result");
    result.innerHTML = "🔄 Analyzing patient data...";

    // Gather input values
    const data = {
        Pregnancies: document.getElementById("Pregnancies").value,
        Glucose: document.getElementById("Glucose").value,
        BloodPressure: document.getElementById("BloodPressure").value,
        SkinThickness: document.getElementById("SkinThickness").value,
        Insulin: document.getElementById("Insulin").value,
        BMI: document.getElementById("BMI").value,
        DPF: document.getElementById("DPF").value, // Matches your HTML ID
        Age: document.getElementById("Age").value
    };

    // Validate that all fields are filled
    for (const key in data) {
        if (!data[key]) {
            result.innerHTML = `⚠ Please fill in the "${key}" field`;
            return;
        }
    }

    // Send data to Flask backend
    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Check for expected 'prediction' field in response
        if (data.prediction === 1) {
            result.innerHTML = "⚠ High Risk of Diabetes";
        } else if (data.prediction === 0) {
            result.innerHTML = "✔ Low Risk of Diabetes";
        } else {
            result.innerHTML = "❌ Unexpected response from server";
            console.error("Unexpected response:", data);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        result.innerHTML = "❌ Error communicating with server";
    });
}