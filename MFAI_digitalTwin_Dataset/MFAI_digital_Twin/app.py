from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Prediction API
@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()

    # Example logic (replace later with Bayesian model)
    glucose = data['Glucose']
    bmi = data['BMI']
    age = data['Age']

    risk_score = (glucose * 0.5) + (bmi * 0.3) + (age * 0.2)

    if risk_score > 100:
        prediction = 1
    else:
        prediction = 0

    return jsonify({
        'prediction': prediction
    })


if __name__ == '__main__':
    app.run(debug=True)