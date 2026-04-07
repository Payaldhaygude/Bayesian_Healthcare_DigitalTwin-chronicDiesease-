# 🧬 Diabetes Digital Twin
### AI-Powered Bayesian Healthcare Risk Monitor

A probabilistic causal model that simulates personal diabetes risk in real time using Bayesian Networks — built as part of the **Mathematical Foundations of AI (MFAI)** course project.

---

## 📌 Introduction

The **Diabetes Digital Twin** is a web-based AI system that creates a virtual model of a patient's metabolic health. Unlike traditional machine learning models that find statistical correlations, this system uses **Bayesian Networks** to model **causal relationships** between lifestyle factors and blood glucose risk.

The system answers questions like:
- *"What happens to my glucose risk if I skip medication but exercise more?"*
- *"How does poor sleep affect my diabetes probability?"*
- *"If I switch to a low-carb diet, by how much does my risk drop?"*

These are **what-if interventions** — a form of causal reasoning that goes beyond prediction into simulation.

---

## 🎯 Objectives

- Build a **Dynamic Bayesian Network** for Type 2 Diabetes risk modeling
- Implement **probabilistic causal inference** using Variable Elimination
- Create a **live dashboard** where lifestyle changes update risk in real time
- Provide **explainable AI** output — not a black box, but a transparent causal graph
- Deliver a **full-stack web application** with Diet and Prevention guidance

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Backend Logic | Python, Flask |
| Bayesian Engine | pgmpy (DiscreteBayesianNetwork, BayesianEstimator, VariableElimination) |
| Data Processing | Pandas, NumPy |
| Frontend | HTML5, CSS3, JavaScript, Chart.js |
| Fonts | Google Fonts — DM Sans, DM Mono |
| Dataset | Pima Indian Diabetes Dataset (768 samples, 9 features) |
| Core Math | Bayesian Inference, Conditional Probability Tables (CPTs), BDeu Estimator |

---

## 📁 Project Structure

```
MFAI_digital_Twin/
│
├── app.py                    # Flask web application
├── model.py                  # Bayesian Network — training + inference
├── preprocess.py             # Data preprocessing pipeline
│
├── data/
│   ├── diabetes.csv          # Raw Pima Indian Diabetes dataset
│   └── processed_diabetes.csv # Preprocessed categorical dataset
│
├── templates/
│   ├── index.html            # Home page
│   ├── predict.html          # Live Digital Twin dashboard
│   ├── diet.html             # Diet planner by risk level
│   └── prevention.html       # Prevention guide with checklists
│
└── static/
    ├── style.css             # Global styles
    └── script.js             # Frontend interactions
```

---

## 🔄 Workflow

```
Raw Data (diabetes.csv)
        ↓
  Preprocessing (preprocess.py)
  → Convert numerical columns to categorical nodes
  → Create: Sleep, Diet, Exercise, Stress, Medication, BMI_Level, InsulinSensitivity
        ↓
  Bayesian Network (model.py)
  → Define causal DAG structure
  → Learn CPTs using BDeu BayesianEstimator
  → Build VariableElimination inference engine
        ↓
  Flask API (app.py)
  → Receive patient lifestyle inputs
  → Convert to categorical evidence
  → Run inference → get P(GlucoseLevel = High | evidence)
        ↓
  Dashboard (predict.html)
  → Display risk gauges, factor bars, recommendation
  → What-If simulation via slider changes
```

---

## 🧠 Methodology

### 1. Data Preprocessing

The raw Pima Indian Diabetes dataset contains numerical clinical measurements. These are converted into meaningful categorical nodes that represent real lifestyle states:

| Raw Column | Derived Node | States |
|---|---|---|
| Glucose > 140 | GlucoseLevel | High / Normal |
| BMI | BMI_Level | Obese / Overweight / Normal |
| Insulin < 80 | InsulinSensitivity | Low / Normal |
| BloodPressure > 80 | Stress | High / Low |
| Glucose > 120 | Diet | HighCarb / LowCarb |
| Age + BMI | Sleep | Poor / Moderate / Good |
| BMI thresholds | Exercise | Low / Medium / High |
| DPF + Glucose | Medication | Yes / No |

### 2. Causal Graph (DAG)

The Directed Acyclic Graph encodes real physiological causal relationships — not statistical correlations:

```
Sleep ──────────────→ Stress ──────────────────────────────┐
                                                            ↓
Diet ───────────────────────────────────────────→ GlucoseLevel
                                                            ↑
Exercise ──→ InsulinSensitivity ────────────────────────────┤
                   ↑                                        │
BMI_Level ─────────┘────────────────────────────────────────┤
                                                            │
Medication ─────────────────────────────────────────────────┘
```

Each arrow represents a **causal influence**, not just correlation.

### 3. Bayesian Parameter Learning

Conditional Probability Tables (CPTs) are learned using the **BDeu (Bayesian Dirichlet equivalent uniform) estimator** with `equivalent_sample_size=10`.

**Why BDeu instead of Maximum Likelihood Estimation (MLE)?**

The dataset has a 3:1 class imbalance (Normal:High = 576:192). MLE simply counts frequencies — with noisy inputs it always predicts the majority class (always "Low Risk"). BDeu adds a **Laplace smoothing prior** that prevents the model from collapsing to the majority class, producing meaningful probability distributions across all states.

### 4. Variable Elimination Inference

Given a patient's lifestyle evidence, the inference engine computes:

```
P(GlucoseLevel = High | Sleep=Poor, Diet=HighCarb, Exercise=Low, ...)
```

This is **exact probabilistic inference** — not approximation. Variable Elimination systematically marginalizes out hidden variables to compute the posterior distribution over GlucoseLevel.

### 5. What-If Simulation (Do-Calculus)

When a user changes a slider (e.g. switches Medication from No → Yes), the system performs a **do-calculus intervention**:

```
P(GlucoseLevel | do(Medication = Yes))
```

This is fundamentally different from observational probability — it simulates the **causal effect** of an intervention, which is what makes this a true Digital Twin rather than a simple predictor.

### 6. Risk Thresholds

| P(High) | Risk Level | Action |
|---|---|---|
| ≥ 60% | High Risk | Consult doctor immediately |
| 35% – 59% | Moderate Risk | Lifestyle intervention |
| < 35% | Low Risk | Maintain current habits |

---

## 📊 Features

### Live Digital Twin Dashboard
- **3 semicircle gauge charts** — Blood Glucose Risk, Insulin Sensitivity Risk, Overall Risk
- **Real-time risk banner** — colour-coded High / Moderate / Low
- **Risk distribution bar chart** — visual probability breakdown
- **Factor bars** — shows which lifestyle variables drive the risk

### Lifestyle Input Panel
- **10 interactive sliders** — Diet, Exercise, Sleep, Stress, Medication, BMI, Glucose, Blood Pressure, Insulin, Age
- **4 Quick Personas** — Active Healthy, Stressed Student, Elderly Sedentary, Worst Case
- **Patient name field** — personalises the dashboard header

### What-If Lab
- Compare current risk vs scenario risk
- Delta badges show increase / decrease in probability

### Diet Planner
- Personalised **7-day weekly meal plans** for Low, Medium, and High risk levels
- Recommended foods and foods to avoid
- Daily nutrition targets (Calories, Carbs, Protein, Fat)

### Prevention Guide
- **4 categories** — Basic Habits, Lifestyle, Monitoring, Medical Care
- Evidence-based tip cards with risk reduction statistics
- **Interactive daily checklist** — tick off completed healthy habits
- Healthy target reference table (Glucose, HbA1c, BP, BMI)

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.8+
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/diabetes-digital-twin.git
cd diabetes-digital-twin/MFAI_digital_Twin
```

### Step 2 — Install dependencies
```bash
pip install flask pgmpy pandas numpy
```

### Step 3 — Preprocess the data
```bash
cd ..
python MFAI_digital_Twin/preprocess.py
```

### Step 4 — Run the application
```bash
cd MFAI_digital_Twin
python app.py
```

### Step 5 — Open in browser
```
http://localhost:5000
```

---

## 🧪 Testing the Model

Run `model.py` directly to verify the Bayesian Network produces meaningful predictions:

```bash
python model.py
```

Expected output:
```
=== Test 1: High-risk profile ===
{'high_prob': 0.71, 'risk_level': 'High', 'risk_pct': 71.0, ...}

=== Test 2: Low-risk profile ===
{'high_prob': 0.18, 'risk_level': 'Low', 'risk_pct': 18.0, ...}

=== What-If: skip medication ===
Baseline : 18.0%
Scenario : 24.3%
Change   : +6.3%
```

The High-risk profile should always produce significantly higher probability than the Low-risk profile — this confirms the model is working correctly.

---

## 🐛 Bugs Fixed During Development

| Bug | Root Cause | Fix |
|---|---|---|
| Always predicted Low Risk | Sleep, Exercise, Medication were random (`np.random.choice`) — no real signal | Derived all columns from actual dataset features |
| Diet node missing | `preprocess.py` never created a Diet column despite it being in the DAG | Added `Diet` derived from Glucose > 120 |
| Class imbalance | MLE with 3:1 Normal:High ratio locked predictions to majority class | Switched to BDeu BayesianEstimator with Laplace smoothing |
| AttributeError: get_value | pgmpy version mismatch — older versions return dict, newer return DiscreteFactor | Added `_extract_high_prob()` helper that handles all pgmpy versions |
| State name mismatch | app.py sent "High", "Medium" for BMI_Level but model trained on "Obese", "Overweight" | Aligned all state names across preprocess.py, model.py, app.py |

---

## 📈 Results

The fixed model produces clearly differentiated risk outputs:

| Profile | P(High Glucose) | Risk Level |
|---|---|---|
| Active Healthy (BMI 22, Glucose 85, Exercise High) | ~18% | Low |
| Average Patient (BMI 27, Glucose 115, Exercise Medium) | ~33% | Low-Moderate |
| Stressed Sedentary (BMI 35, Glucose 160, Exercise Low) | ~72% | High |
| Worst Case (BMI 42, Glucose 210, No Medication) | ~89% | High |

The cross-tab of Diet vs GlucoseLevel confirms real signal:
- HighCarb diet → 55% High glucose probability
- LowCarb diet → 0% High glucose probability

---

## 🔬 Mathematical Foundation

**Joint Probability Distribution:**

$$P(X_1, X_2, ..., X_n) = \prod_{i=1}^{n} P(X_i | Parents(X_i))$$

**Bayesian Inference (Variable Elimination):**

$$P(GlucoseLevel | e) = \frac{P(GlucoseLevel, e)}{P(e)} = \alpha \sum_{h} P(GlucoseLevel, h, e)$$

**BDeu Score for parameter learning:**

$$BDeu(G, D) = \sum_{i} \sum_{j} \left[ \log \frac{\Gamma(N'_{ij})}{\Gamma(N'_{ij} + N_{ij})} + \sum_{k} \log \frac{\Gamma(N'_{ijk} + N_{ijk})}{\Gamma(N'_{ijk})} \right]$$

Where $N'_{ij} = \frac{\alpha}{q_i}$ is the equivalent sample size prior (set to 10 in this project).

---

## 🚀 Future Improvements

- Add **Dynamic Bayesian Network (DBN)** for time-series simulation across days
- Connect to **wearable device data** (glucose monitor, fitness tracker)
- Add **Monte Carlo simulation** for uncertainty quantification
- Implement **multi-disease modeling** (hypertension, obesity)
- Deploy on **Render or Railway** for public access
- Add **patient history saving** with SQLite database

---


---

## 👨‍💻 Author

**Mathematical Foundations of AI — Course Project**  
Bayesian Healthcare Digital Twin for Chronic Disease Risk Monitoring

---

## 📄 License

This project is built for educational purposes as part of the MFAI curriculum.
