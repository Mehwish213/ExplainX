from flask import Flask, render_template, request

import pandas as pd
import joblib
import shap
import sqlite3


from nlp.explanation_engine import generate_explanation
from explain.shap_engine import generate_shap_plot

app = Flask(__name__)

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("preprocessed_loan_data.csv")

X = df.drop("Loan_Status", axis=1)

# =========================
# LOAD TRAINED MODEL
# =========================

model = joblib.load("best_model.pkl")

# =========================
# CREATE SHAP EXPLAINER
# =========================

explainer = shap.Explainer(model, X)

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# DASHBOARD PAGE
# =========================

@app.route("/dashboard")
def dashboard():
    try:
        conn = sqlite3.connect("explainx.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Stats
        cursor.execute("SELECT COUNT(*) as total FROM predictions")
        total_count = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as approved FROM predictions WHERE prediction='APPROVED'")
        approved_count = cursor.fetchone()['approved']
        
        cursor.execute("SELECT COUNT(*) as rejected FROM predictions WHERE prediction='REJECTED'")
        rejected_count = cursor.fetchone()['rejected']
        
        # Recent Activity
        cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC LIMIT 5")
        recent_activity = cursor.fetchall()
        
        conn.close()
        
        stats = {
            "total": total_count,
            "approved": approved_count,
            "rejected": rejected_count,
            "approval_rate": round((approved_count / total_count * 100), 1) if total_count > 0 else 0
        }
    except Exception as e:
        print("Dashboard error:", e)
        stats = {"total": 0, "approved": 0, "rejected": 0, "approval_rate": 0}
        recent_activity = []
        
    return render_template("dashboard.html", stats=stats, activity=recent_activity)

# =========================
# PREDICTION ROUTE
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    # =====================
    # GET USER INPUT
    # =====================

    data = {

        "Gender": int(request.form["Gender"]),
        "Married": int(request.form["Married"]),
        "Dependents": int(request.form["Dependents"]),
        "Education": int(request.form["Education"]),
        "Self_Employed": int(request.form["Self_Employed"]),
        "ApplicantIncome": float(request.form["ApplicantIncome"]),
        "CoapplicantIncome": float(request.form["CoapplicantIncome"]),
        "LoanAmount": float(request.form["LoanAmount"]),
        "Loan_Amount_Term": float(request.form["Loan_Amount_Term"]),
        "Credit_History": float(request.form["Credit_History"]),
        "Property_Area": int(request.form["Property_Area"])

    }

    # =====================
    # CONVERT TO DATAFRAME
    # =====================

    input_df = pd.DataFrame([data])

    # =====================
    # MAKE PREDICTION
    # =====================

    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]
    confidence = float(max(prediction_proba))
    
    result = "APPROVED" if prediction == 1 else "REJECTED"

    # =====================
    # SHAP VALUES
    # =====================

    shap_values = explainer(input_df)

    # =====================
    # GENERATE SHAP GRAPH
    # =====================

    generate_shap_plot(shap_values)

    # =====================
    # NLP EXPLANATION
    # =====================

    explanation_data = generate_explanation(
        shap_values,
        X.columns,
        prediction_result=result
    )

    # =====================
    # SAVE TO DATABASE
    # =====================

    try:
        conn = sqlite3.connect("explainx.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (
                gender, married, dependents, education, self_employed,
                applicant_income, coapplicant_income, loan_amount, loan_term,
                credit_history, property_area, prediction
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["Gender"], data["Married"], data["Dependents"], data["Education"], data["Self_Employed"],
            data["ApplicantIncome"], data["CoapplicantIncome"], data["LoanAmount"], data["Loan_Amount_Term"],
            data["Credit_History"], data["Property_Area"], result
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database error:", e)

    # =====================
    # SEND TO RESULT PAGE
    # =====================

    # =====================
    # PREPARE DATA FOR CHARTS
    # =====================
    shap_data = []
    for feature, value in zip(X.columns, shap_values.values[0]):
        shap_data.append({
            "feature": feature,
            "impact": round(float(value), 4)
        })
    
    # Sort by absolute impact for better visualization
    shap_data.sort(key=lambda x: abs(x["impact"]), reverse=True)

    return render_template(
        "result.html",
        prediction=result,
        confidence=round(confidence * 100, 1),
        reason=explanation_data["reason"],
        coaching=explanation_data["coaching"],
        summary=explanation_data["summary"],
        keywords=explanation_data["keywords"],
        full_text=explanation_data["full_text"],
        shap_data=shap_data
    )

# =========================
# HISTORY PAGE
# =========================

@app.route("/history")
def history():
    try:
        conn = sqlite3.connect("explainx.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC")
        predictions = cursor.fetchall()
        conn.close()
    except Exception as e:
        print("Database error:", e)
        predictions = []
    
    return render_template("history.html", predictions=predictions)

@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        conn = sqlite3.connect("explainx.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database error:", e)
    
    return history()

# =========================
# METRICS PAGE
# =========================

@app.route("/metrics")
def metrics():
    return render_template("metrics.html")

# =========================
# SETTINGS PAGE
# =========================

@app.route("/settings")
def settings():
    return render_template("settings.html")

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=5001)
