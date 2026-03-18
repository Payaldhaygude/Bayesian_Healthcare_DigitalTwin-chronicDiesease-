from flask import Flask, render_template, request
from model import DiabetesDigitalTwin

app = Flask(__name__)
twin = DiabetesDigitalTwin()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/prediction")
def prediction():
    return render_template("predict.html")


@app.route("/predict", methods=["POST"])
def predict():

    # ── Read raw form values ──────────────────────────────────────────────────
    glucose       = float(request.form["Glucose"])
    bloodpressure = float(request.form["BloodPressure"])
    insulin       = float(request.form["Insulin"])
    bmi           = float(request.form["BMI"])
    dpf           = float(request.form["DPF"])
    age           = float(request.form["Age"])

    # ── Convert to categorical states (must match preprocess.py exactly) ──────
    sleep       = "Poor"     if (age > 45 or bmi > 32) else ("Moderate" if age > 30 else "Good")
    exercise    = "Low"      if bmi > 30               else ("Medium"   if bmi > 25 else "High")
    stress      = "High"     if bloodpressure > 80     else "Low"
    medication  = "Yes"      if (dpf > 0.5 and glucose > 140) else "No"
    diet        = "HighCarb" if glucose > 120          else "LowCarb"
    bmi_level   = "Obese"    if bmi > 30               else ("Overweight" if bmi > 25 else "Normal")
    insulin_sen = "Low"      if insulin < 80           else "Normal"

    evidence = {
        "Sleep":              sleep,
        "Diet":               diet,
        "Exercise":           exercise,
        "Stress":             stress,
        "Medication":         medication,
        "BMI_Level":          bmi_level,
        "InsulinSensitivity": insulin_sen,
    }

    print("Evidence sent to model:", evidence)

    # ── Run inference ─────────────────────────────────────────────────────────
    result = twin.predict_risk(evidence)

    if result is None:
        return render_template("predict.html",
                               result_text="Prediction failed. Check server logs.",
                               risk_class="low", icon="X", headline="Error",
                               advice="Please try again.",
                               bar_glucose="0%", bar_bmi="0%",
                               bar_insulin="0%", bar_bp="0%",
                               bar_color="green")

    # ── Read from the dict that predict_risk now returns ──────────────────────
    risk_level  = result["risk_level"]
    risk_pct    = result["risk_pct"]
    print(f"Risk level: {risk_level} ({risk_pct}%)")

    # ── Build display variables ───────────────────────────────────────────────
    if risk_level == "High":
        risk_class  = "high"
        icon        = "!!"
        headline    = "High Risk of Diabetes"
        result_text = f"High Risk — Probability: {risk_pct}%"
        advice      = ("Your profile suggests elevated glucose risk. "
                       "Please consult a doctor soon. Focus on reducing "
                       "carbohydrate intake, increasing physical activity, "
                       "and monitoring blood sugar regularly.")
        bar_glucose = "85%"
        bar_bmi     = "75%"
        bar_insulin = "80%"
        bar_bp      = "60%"
        bar_color   = "red"

    elif risk_level == "Moderate":
        risk_class  = "medium"
        icon        = "~~"
        headline    = "Moderate Risk of Diabetes"
        result_text = f"Moderate Risk — Probability: {risk_pct}%"
        advice      = ("There are some risk factors present. Improving diet, "
                       "sleeping 7-8 hours per night, and light daily exercise "
                       "can significantly reduce your risk over time.")
        bar_glucose = "55%"
        bar_bmi     = "50%"
        bar_insulin = "45%"
        bar_bp      = "40%"
        bar_color   = "orange"

    else:
        risk_class  = "low"
        icon        = "OK"
        headline    = "Low Risk of Diabetes"
        result_text = f"Low Risk — Probability: {risk_pct}%"
        advice      = ("Your indicators look healthy. Maintain your current "
                       "lifestyle — regular exercise, a balanced diet, and "
                       "routine checkups every 1-2 years are recommended.")
        bar_glucose = "22%"
        bar_bmi     = "18%"
        bar_insulin = "15%"
        bar_bp      = "20%"
        bar_color   = "green"

    return render_template("predict.html",
                           result_text=result_text,
                           risk_class=risk_class,
                           icon=icon,
                           headline=headline,
                           advice=advice,
                           bar_glucose=bar_glucose,
                           bar_bmi=bar_bmi,
                           bar_insulin=bar_insulin,
                           bar_bp=bar_bp,
                           bar_color=bar_color)


@app.route("/diet")
def diet():
    return render_template("diet.html")


@app.route("/prevention")
def prevention():
    return render_template("prevention.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)