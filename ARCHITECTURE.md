# Technical Architecture

Comprehensive technical documentation of ExplainX system architecture, design patterns, and implementation details.

## Table of Contents

- [System Architecture](#system-architecture)
- [Component Overview](#component-overview)
- [Data Flow](#data-flow)
- [Module Details](#module-details)
- [Database Architecture](#database-architecture)
- [Explainability Engine](#explainability-engine)
- [Design Patterns](#design-patterns)
- [Performance Considerations](#performance-considerations)
- [Security Considerations](#security-considerations)
- [Deployment Architecture](#deployment-architecture)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│              (Web Browser - HTML/CSS/JS)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                              │
│                  (Flask Routes)                             │
│  ├── / (home)          ├── /dashboard                       │
│  ├── /predict          ├── /history                        │
│  └── /metrics          └── Static files                    │
└────────┬──────────────────────┬──────────────────────────────┘
         │                      │
    ┌────▼──────────┐      ┌────▼──────────────┐
    │ Business      │      │ Data Access       │
    │ Logic Layer   │      │ Layer             │
    │               │      │                   │
    │ ├── app.py    │      │ ├── db.py        │
    │ │  - Route    │      │ │  - SQLite      │
    │ │    handlers │      │ │  - Queries     │
    │ │  - Request  │      │ │  - Inserts     │
    │ │    process. │      │ └────────────────┘
    │ │              │      │
    │ └── Prediction │      └────────────────────┐
    │     Engine     │                           │
    └────┬────────┬──┘                           │
         │        │                               │
    ┌────▼──┐ ┌───▼─────────┐          ┌─────────▼───┐
    │ Model │ │ Explainability        │  Database   │
    │ Layer │ │ Engine                 │ (SQLite3)   │
    │       │ │                        │             │
    │ ├── Load          │ ├── SHAP      │ ├── predictions
    │ │  Model          │ │  Engine     │ │  table
    │ │  (joblib)       │ │  (explain/) │ │
    │ │                 │ │             │ │
    │ ├── Make          │ ├── NLP Engine│ └─────────┬─┘
    │ │  Predictions    │ │  (nlp/)     │           │
    │ │                 │ │             │           │
    │ └── Get           │ └── Generate  │           │
    │    Probabilities  │    Text       │           │
    │                   │    Explanations           │
    └───────────────────┴─────────────────┘         │
                                                     │
    ┌────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│  ├── best_model.pkl      ├── preprocessed_loan_data.csv    │
│  ├── loan_data.csv       └── SHAP plots (PNG files)         │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Layers

| Layer | Components | Responsibility |
|-------|-----------|-----------------|
| **Presentation** | Flask routes, Templates | Handle HTTP requests, render HTML |
| **Business Logic** | app.py, Prediction engine | Process requests, coordinate flow |
| **Explainability** | SHAP engine, NLP engine | Generate explanations |
| **Data Access** | db.py | Database operations |
| **Model** | best_model.pkl | ML predictions |
| **Data** | CSV files, SQLite DB | Persist data |

---

## Component Overview

### 1. **Flask Application (app.py)**

**Responsibilities**:
- Route handling and request processing
- Session management
- Template rendering
- Business logic orchestration

**Key Functions**:
```python
@app.route("/")                  # Home page
@app.route("/dashboard")         # Analytics dashboard
@app.route("/predict", POST)     # Make predictions
@app.route("/history")           # Prediction history
@app.route("/metrics")           # Performance metrics
```

**Key Variables**:
- `df`: Preprocessed data for SHAP baseline
- `model`: Trained ML model
- `explainer`: SHAP explainer instance

### 2. **Database Layer (db.py)**

**Responsibilities**:
- Database schema initialization
- Connection management
- Query execution

**Schema**:
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender, married, dependents, education, self_employed INTEGER,
    applicant_income, coapplicant_income, loan_amount, loan_term REAL,
    credit_history REAL,
    property_area INTEGER,
    prediction TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. **SHAP Engine (explain/shap_engine.py)**

**Responsibilities**:
- Generate SHAP values
- Create waterfall plots
- Visualize feature contributions

**Key Function**:
```python
def generate_shap_plot(shap_values):
    """
    Generate SHAP waterfall plot
    
    Args:
        shap_values: SHAP explainer output
        
    Output:
        PNG file saved to static/shap/shap_plot.png
    """
```

### 4. **NLP Engine (nlp/explanation_engine.py)**

**Responsibilities**:
- Generate natural language explanations
- Create coaching tips
- Identify positive/negative drivers

**Key Function**:
```python
def generate_explanation(shap_values, feature_names, prediction_result):
    """
    Generate human-readable explanation
    
    Returns:
        {
            'reason_text': str,           # Main explanation
            'coaching_tips': list[str],   # Improvement suggestions
            'positive_drivers': list,     # Approval factors
            'negative_drivers': list      # Rejection factors
        }
    """
```

---

## Data Flow

### Prediction Flow

```
┌─────────────────┐
│  User Input     │
│  (Web Form)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 1. Input Validation                 │
│    - Check required fields          │
│    - Validate data types            │
│    - Check value ranges             │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 2. Data Preparation                 │
│    - Convert to DataFrame           │
│    - Scale/normalize if needed      │
│    - Match model input format       │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 3. ML Prediction                    │
│    - Load model                     │
│    - Make prediction                │
│    - Get probabilities              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 4. SHAP Explanation                 │
│    - Calculate SHAP values          │
│    - Generate waterfall plot        │
│    - Extract feature impacts        │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 5. NLP Explanation                  │
│    - Generate text explanation      │
│    - Create coaching tips           │
│    - Identify top drivers           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 6. Database Storage                 │
│    - Save prediction record         │
│    - Store all features             │
│    - Log timestamp                  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 7. Response Generation              │
│    - Format JSON response           │
│    - Include all explanations       │
│    - Return to user                 │
└────────┬────────────────────────────┘
         │
         ▼
    ┌────────────────┐
    │  User sees:    │
    │ - Prediction   │
    │ - SHAP Plot    │
    │ - Explanation  │
    │ - Tips         │
    └────────────────┘
```

### Dashboard Data Flow

```
┌──────────────────┐
│  User visits     │
│  /dashboard      │
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Query Database:                 │
│ - COUNT(*) FROM predictions     │
│ - WHERE prediction='APPROVED'   │
│ - WHERE prediction='REJECTED'   │
│ - ORDER BY created_at DESC      │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Calculate Metrics:              │
│ - Total count                   │
│ - Approval rate (%)             │
│ - Recent activity               │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ Render Dashboard Template       │
│ - Display stats                 │
│ - Show recent activity          │
│ - Render charts                 │
└────────┬────────────────────────┘
         │
         ▼
    ┌─────────────────┐
    │  User sees:     │
    │ - Statistics    │
    │ - Activity Feed │
    │ - Charts        │
    └─────────────────┘
```

---

## Module Details

### app.py Structure

```python
# Imports
from flask import Flask, render_template, request
import pandas as pd, joblib, shap, sqlite3
from nlp.explanation_engine import generate_explanation
from explain.shap_engine import generate_shap_plot

# Initialize Flask app
app = Flask(__name__)

# Load data and models at startup
df = pd.read_csv("preprocessed_loan_data.csv")
X = df.drop("Loan_Status", axis=1)
model = joblib.load("best_model.pkl")
explainer = shap.Explainer(model, X)

# Route: Home
@app.route("/")
def home():
    return render_template("index.html")

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    # Query stats from DB
    # Calculate metrics
    # Return rendered template

# Route: Predict
@app.route("/predict", methods=["POST"])
def predict():
    # Extract form data
    # Validate input
    # Make prediction
    # Generate SHAP explanation
    # Generate NLP explanation
    # Save to database
    # Return JSON response

# Run application
if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### explain/shap_engine.py

```python
import shap
import matplotlib.pyplot as plt

plt.switch_backend('Agg')  # Headless mode

def generate_shap_plot(shap_values):
    """
    Generate and save SHAP waterfall plot
    
    Workflow:
    1. Create waterfall plot from SHAP values
    2. Save as PNG to static/shap/
    3. Close figure to free memory
    """
    shap.plots.waterfall(shap_values[0], show=False)
    plt.savefig(
        "static/shap/shap_plot.png",
        bbox_inches='tight'
    )
    plt.close()
```

### nlp/explanation_engine.py

```python
import spacy
import nltk
from nltk.tokenize import sent_tokenize

nlp = spacy.load("en_core_web_sm")

def generate_explanation(shap_values, feature_names, prediction_result):
    """
    Generate natural language explanation
    
    Process:
    1. Extract SHAP values for each feature
    2. Sort by magnitude
    3. Identify top positive/negative drivers
    4. Generate explanation text based on result
    5. Create coaching tips for improvement
    
    Returns:
        Dictionary with explanation components
    """
    # Implementation details...
```

---

## Database Architecture

### Schema Design

```
┌─────────────────────────────────────────┐
│         predictions table               │
├─────────────────────────────────────────┤
│ PK: id (INTEGER)                        │
├─────────────────────────────────────────┤
│ Applicant Info:                         │
│  - gender INTEGER (0/1)                 │
│  - married INTEGER (0/1)                │
│  - dependents INTEGER (0-3)             │
│  - education INTEGER (0/1)              │
│  - self_employed INTEGER (0/1)          │
├─────────────────────────────────────────┤
│ Financial Info:                         │
│  - applicant_income REAL                │
│  - coapplicant_income REAL              │
│  - loan_amount REAL                     │
│  - loan_term REAL                       │
│  - credit_history REAL (0/1)            │
│  - property_area INTEGER (0-2)          │
├─────────────────────────────────────────┤
│ Result:                                 │
│  - prediction TEXT (APPROVED/REJECTED)  │
│  - created_at TIMESTAMP                 │
└─────────────────────────────────────────┘
```

### Indexing Strategy

```sql
-- Recommended indexes for performance
CREATE INDEX idx_prediction ON predictions(prediction);
CREATE INDEX idx_created_at ON predictions(created_at);
CREATE INDEX idx_applicant_income ON predictions(applicant_income);
```

### Query Examples

```sql
-- Get statistics
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN prediction='APPROVED' THEN 1 ELSE 0 END) as approved,
    SUM(CASE WHEN prediction='REJECTED' THEN 1 ELSE 0 END) as rejected
FROM predictions;

-- Get recent predictions
SELECT * FROM predictions 
ORDER BY created_at DESC 
LIMIT 10;

-- Approval rate by property area
SELECT property_area, 
       COUNT(*) as total,
       SUM(CASE WHEN prediction='APPROVED' THEN 1 ELSE 0 END) as approved,
       (SUM(CASE WHEN prediction='APPROVED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as approval_rate
FROM predictions
GROUP BY property_area;
```

---

## Explainability Engine

### SHAP Value Calculation

```
Feature Importance Calculation:
┌─────────────────────────────────────────┐
│ Input: New applicant data               │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ SHAP Explainer (initialized with data)  │
│ - Baseline: Average prediction from X   │
│ - Model: Trained ML model               │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Calculate Shapley Values                │
│ - Contribution of each feature          │
│ - Additive: Sum of values = prediction  │
│ - Fair allocation of credit             │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Output: SHAP values for each feature    │
│ - Positive values: Push to APPROVED     │
│ - Negative values: Push to REJECTED     │
└─────────────────────────────────────────┘
```

### NLP Explanation Generation

```
┌──────────────────────────────┐
│ Extract top drivers          │
│ (positive & negative)        │
└────────────┬─────────────────┘
             │
    ┌────────┴─────────┐
    │                  │
    ▼                  ▼
┌──────────────┐  ┌──────────────────┐
│ If APPROVED  │  │ If REJECTED      │
│ - Highlight │  │ - Highlight      │
│   positive   │  │   negative       │
│   factors    │  │   factors        │
└──────────────┘  └──────────────────┘
    │                  │
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────┐
    │ Generate Tips   │
    │ - Specific to   │
    │   weak areas    │
    │ - Actionable    │
    │   advice        │
    └─────────────────┘
             │
             ▼
    ┌──────────────────────┐
    │ Return explanation:  │
    │ - Reason text        │
    │ - Coaching tips      │
    │ - Driver lists       │
    └──────────────────────┘
```

---

## Design Patterns

### 1. **MVC Pattern**

```
Model: best_model.pkl, Data layer
View: Templates (HTML)
Controller: app.py routes
```

### 2. **Factory Pattern**

```python
class ModelFactory:
    @staticmethod
    def create_explainer(model, data):
        return shap.Explainer(model, data)
```

### 3. **Singleton Pattern**

```python
# Model and explainer loaded once
model = joblib.load("best_model.pkl")
explainer = shap.Explainer(model, X)
```

### 4. **Pipeline Pattern**

```
Input → Validation → Processing → Prediction → 
    Explanation → Storage → Response
```

---

## Performance Considerations

### Optimization Strategies

| Issue | Solution |
|-------|----------|
| **Slow SHAP plots** | Cache plots, generate async |
| **Model loading time** | Load once at startup |
| **Database queries** | Add indexes, use SELECT efficiently |
| **Memory usage** | Limit SHAP baseline size |
| **Network latency** | Serve static files via CDN |

### Performance Monitoring

```python
import time

def measure_performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

@measure_performance
def predict():
    # Prediction logic
    pass
```

### Benchmarks (Typical)

| Operation | Time |
|-----------|------|
| Model prediction | 50-100ms |
| SHAP calculation | 200-500ms |
| SHAP plot generation | 300-800ms |
| NLP explanation | 100-200ms |
| Database save | 50-100ms |
| **Total per prediction** | **800ms - 1.8s** |

---

## Security Considerations

### Input Validation

```python
def validate_input(data):
    """Comprehensive input validation"""
    # Type checking
    # Range checking
    # SQL injection prevention
    # XSS prevention
```

### Database Security

```python
# Use parameterized queries
cursor.execute(
    "INSERT INTO predictions (...) VALUES (?, ?, ...)",
    (value1, value2, ...)
)
```

### Model Security

```python
# Verify model integrity
import hashlib

def verify_model_hash(filepath, expected_hash):
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_hash
```

---

## Deployment Architecture

### Development Deployment

```
Local Machine
├── Python 3.10
├── Flask development server
├── SQLite database
└── All files in project directory
```

### Production Deployment

```
Production Server
├── Python 3.10 environment
├── Gunicorn/uWSGI application server
├── Nginx reverse proxy
├── SQLite or PostgreSQL
├── Static file server
└── SSL/TLS certificates
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
COPY . .
CMD ["gunicorn", "-w", "4", "app:app"]
```

---

<div align="center">

**Architecture Documentation v1.0**

[⬆ back to top](#technical-architecture)

</div>
