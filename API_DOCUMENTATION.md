# API Documentation

Complete reference for ExplainX API endpoints and usage.

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Response Format](#response-format)
- [Endpoints](#endpoints)
  - [Home](#home)
  - [Dashboard](#dashboard)
  - [Predict](#predict)
  - [History](#history)
  - [Metrics](#metrics)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## Overview

ExplainX provides a RESTful API for loan prediction and explainability. The API is built with Flask and returns JSON responses for data endpoints.

### Key Features
- **Real-time Predictions**: Get loan decisions instantly
- **Explainability Data**: SHAP values and explanations included
- **History Tracking**: Access all past predictions
- **Performance Metrics**: Real-time statistics

---

## Authentication

**Current Version**: No authentication required (development mode)

**For Production**: Implement JWT tokens or API keys

```python
# Suggested implementation for app.py
from functools import wraps
from flask import request

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not api_key or api_key != 'your-secret-key':
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/predict', methods=['POST'])
@require_auth
def predict():
    # Implementation
    pass
```

---

## Base URL

```
http://localhost:5000
```

### Production URLs
```
https://yourdomain.com/api/v1
```

---

## Response Format

All responses use JSON format (except HTML for web pages).

### Success Response

```json
{
    "status": "success",
    "data": {
        "prediction": "APPROVED",
        "confidence": 0.85
    }
}
```

### Error Response

```json
{
    "status": "error",
    "message": "Invalid input parameters",
    "errors": {
        "ApplicantIncome": "Must be a positive number"
    }
}
```

---

## Endpoints

### Home

#### GET /

**Description**: Render home page

**Request**
```bash
GET /
```

**Response**
- **Status**: 200 OK
- **Content-Type**: text/html
- **Body**: HTML home page

**Example**
```bash
curl http://localhost:5000/
```

---

### Dashboard

#### GET /dashboard

**Description**: Render analytics dashboard with statistics

**Request**
```bash
GET /dashboard
```

**Response**
- **Status**: 200 OK
- **Content-Type**: text/html
- **Body**: Dashboard HTML with embedded statistics

**Response Data Structure**
```python
{
    "stats": {
        "total": 42,                    # Total predictions
        "approved": 28,                 # Approved count
        "rejected": 14,                 # Rejected count
        "approval_rate": 66.7           # Approval percentage
    },
    "activity": [
        {
            "id": 1,
            "prediction": "APPROVED",
            "confidence": 0.92,
            "created_at": "2024-01-15 10:30:45"
        },
        # ... more records
    ]
}
```

**Example**
```bash
curl http://localhost:5000/dashboard
```

---

### Predict

#### POST /predict

**Description**: Make a loan prediction with explanation

**Request**

```bash
POST /predict
Content-Type: application/x-www-form-urlencoded
```

**Parameters**

| Parameter | Type | Required | Description | Range |
|-----------|------|----------|-------------|-------|
| `Gender` | Integer | Yes | Gender (0=Female, 1=Male) | 0-1 |
| `Married` | Integer | Yes | Marital status (0=No, 1=Yes) | 0-1 |
| `Dependents` | Integer | Yes | Number of dependents | 0-3 |
| `Education` | Integer | Yes | Education level (0=Graduate, 1=Undergraduate) | 0-1 |
| `Self_Employed` | Integer | Yes | Self-employment status (0=No, 1=Yes) | 0-1 |
| `ApplicantIncome` | Float | Yes | Monthly income in rupees | > 0 |
| `CoapplicantIncome` | Float | Yes | Co-applicant income | >= 0 |
| `LoanAmount` | Float | Yes | Loan amount in thousands | > 0 |
| `Loan_Amount_Term` | Float | Yes | Loan term in months | > 0 |
| `Credit_History` | Float | Yes | Credit history (0=No, 1=Yes) | 0-1 |
| `Property_Area` | Integer | Yes | Property area (0=Urban, 1=Semi-Urban, 2=Rural) | 0-2 |

**Response**

```json
{
    "status": "success",
    "prediction": "APPROVED",
    "confidence": 0.87,
    "explanation": "Primary Approval Reason: Your ApplicantIncome demonstrates strong loan eligibility. This was the key factor supporting your approval (impact: +0.45).",
    "shap_plot": "static/shap/shap_plot.png",
    "coaching_tips": [
        "💡 Maintain your strong income level for future loan applications",
        "💡 Keep your credit history clean and payments on time"
    ],
    "positive_drivers": [
        ["ApplicantIncome", 0.45],
        ["Credit_History", 0.32]
    ],
    "negative_drivers": [
        ["Loan_Amount_Term", -0.15]
    ]
}
```

**Error Response**

```json
{
    "status": "error",
    "message": "Missing required parameters",
    "errors": {
        "ApplicantIncome": "This field is required",
        "Gender": "Must be 0 or 1"
    }
}
```

**Example**

Using cURL:
```bash
curl -X POST http://localhost:5000/predict \
  -d "Gender=1&Married=1&Dependents=0&Education=1&Self_Employed=0&ApplicantIncome=5000&CoapplicantIncome=1000&LoanAmount=150&Loan_Amount_Term=360&Credit_History=1&Property_Area=1"
```

Using Python:
```python
import requests

data = {
    "Gender": 1,
    "Married": 1,
    "Dependents": 0,
    "Education": 1,
    "Self_Employed": 0,
    "ApplicantIncome": 5000,
    "CoapplicantIncome": 1000,
    "LoanAmount": 150,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": 1
}

response = requests.post('http://localhost:5000/predict', data=data)
print(response.json())
```

Using JavaScript:
```javascript
fetch('/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
        Gender: '1',
        Married: '1',
        Dependents: '0',
        Education: '1',
        Self_Employed: '0',
        ApplicantIncome: '5000',
        CoapplicantIncome: '1000',
        LoanAmount: '150',
        Loan_Amount_Term: '360',
        Credit_History: '1',
        Property_Area: '1'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### History

#### GET /history

**Description**: View prediction history

**Request**
```bash
GET /history
```

**Response**
- **Status**: 200 OK
- **Content-Type**: text/html
- **Body**: HTML page with prediction history table

**Response Data**
```python
{
    "history": [
        {
            "id": 1,
            "gender": 1,
            "married": 1,
            "dependents": 0,
            "education": 1,
            "self_employed": 0,
            "applicant_income": 5000,
            "coapplicant_income": 1000,
            "loan_amount": 150,
            "loan_term": 360,
            "credit_history": 1,
            "property_area": 1,
            "prediction": "APPROVED",
            "created_at": "2024-01-15 10:30:45"
        }
    ],
    "total_records": 42
}
```

**Example**
```bash
curl http://localhost:5000/history
```

---

### Metrics

#### GET /metrics

**Description**: Get performance metrics and statistics

**Request**
```bash
GET /metrics
```

**Response**
- **Status**: 200 OK
- **Content-Type**: text/html or application/json
- **Body**: Metrics page or JSON data

**Response Data**
```json
{
    "total_predictions": 42,
    "approved_count": 28,
    "rejected_count": 14,
    "approval_rate": 66.7,
    "average_confidence": 0.82,
    "predictions_today": 5,
    "predictions_this_week": 23,
    "predictions_this_month": 42,
    "top_approval_factors": [
        ["ApplicantIncome", 0.35],
        ["Credit_History", 0.28]
    ],
    "top_rejection_factors": [
        ["Loan_Amount_Term", -0.22],
        ["LoanAmount", -0.18]
    ]
}
```

**Example**
```bash
curl http://localhost:5000/metrics
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful prediction |
| 400 | Bad Request | Missing required parameters |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Server Error | Database connection failed |
| 503 | Service Unavailable | Model loading failed |

### Common Error Scenarios

#### 1. Missing Required Parameter

```json
{
    "status": "error",
    "message": "Missing required parameter: ApplicantIncome",
    "errors": {
        "ApplicantIncome": "This field is required"
    }
}
```

#### 2. Invalid Parameter Type

```json
{
    "status": "error",
    "message": "Invalid parameter type",
    "errors": {
        "Gender": "Expected integer (0 or 1), got 'invalid'"
    }
}
```

#### 3. Out of Range Parameter

```json
{
    "status": "error",
    "message": "Parameter out of valid range",
    "errors": {
        "Property_Area": "Expected value between 0-2, got 5"
    }
}
```

#### 4. Database Error

```json
{
    "status": "error",
    "message": "Database error occurred",
    "code": "DB_ERROR",
    "details": "Could not save prediction"
}
```

---

## Rate Limiting

**Current**: No rate limiting (development mode)

**Recommended Production Settings**:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/predict', methods=['POST'])
@limiter.limit("100 per hour")
def predict():
    pass
```

---

## Examples

### Example 1: Simple Prediction Request

**Scenario**: Check if a standard applicant gets approved

```bash
curl -X POST http://localhost:5000/predict \
  -d "Gender=1" \
  -d "Married=1" \
  -d "Dependents=1" \
  -d "Education=1" \
  -d "Self_Employed=0" \
  -d "ApplicantIncome=4500" \
  -d "CoapplicantIncome=800" \
  -d "LoanAmount=120" \
  -d "Loan_Amount_Term=360" \
  -d "Credit_History=1" \
  -d "Property_Area=0"
```

### Example 2: Python Integration

```python
import requests
import json

def get_loan_prediction(applicant_data):
    """
    Make a prediction for a loan applicant
    
    Args:
        applicant_data (dict): Dictionary with applicant information
        
    Returns:
        dict: Prediction result with explanation
    """
    url = 'http://localhost:5000/predict'
    
    try:
        response = requests.post(url, data=applicant_data)
        result = response.json()
        
        if result['status'] == 'success':
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Explanation: {result['explanation']}")
            return result
        else:
            print(f"Error: {result['message']}")
            return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# Usage
applicant = {
    "Gender": 1,
    "Married": 1,
    "Dependents": 0,
    "Education": 1,
    "Self_Employed": 0,
    "ApplicantIncome": 5500,
    "CoapplicantIncome": 1200,
    "LoanAmount": 140,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": 1
}

result = get_loan_prediction(applicant)
```

### Example 3: Batch Predictions

```python
import requests
import pandas as pd

def batch_predict(csv_file):
    """Process multiple predictions from CSV"""
    df = pd.read_csv(csv_file)
    results = []
    
    for idx, row in df.iterrows():
        data = row.to_dict()
        response = requests.post('http://localhost:5000/predict', data=data)
        result = response.json()
        results.append(result)
        
    return pd.DataFrame(results)

# Usage
predictions_df = batch_predict('applicants.csv')
predictions_df.to_csv('predictions_output.csv', index=False)
```

### Example 4: JavaScript Fetch

```javascript
async function makePrediction(applicantData) {
    const formData = new URLSearchParams();
    
    for (const [key, value] of Object.entries(applicantData)) {
        formData.append(key, value);
    }
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log(`Result: ${result.prediction}`);
            console.log(`Explanation: ${result.explanation}`);
            displayResult(result);
        } else {
            console.error('Prediction failed:', result.message);
        }
    } catch (error) {
        console.error('Request error:', error);
    }
}

// Usage
const applicant = {
    Gender: '1',
    Married: '1',
    Dependents: '0',
    Education: '1',
    Self_Employed: '0',
    ApplicantIncome: '5000',
    CoapplicantIncome: '1000',
    LoanAmount: '150',
    Loan_Amount_Term: '360',
    Credit_History: '1',
    Property_Area: '1'
};

makePrediction(applicant);
```

---

## Best Practices

### 1. Input Validation

```python
def validate_prediction_input(data):
    """Validate input parameters"""
    required_fields = [
        'Gender', 'Married', 'Dependents', 'Education',
        'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome',
        'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'
    ]
    
    # Check all required fields present
    for field in required_fields:
        if field not in data:
            return False, f"Missing {field}"
    
    # Validate ranges
    if not (0 <= int(data['Gender']) <= 1):
        return False, "Gender must be 0 or 1"
    
    return True, "Valid"
```

### 2. Error Handling

```python
try:
    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.Timeout:
    print("Request timeout")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except ValueError:
    print("Invalid JSON response")
```

### 3. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_prediction_cached(gender, married, dependents, ...):
    """Cache predictions to reduce computation"""
    pass
```

---

<div align="center">

**API Documentation v1.0**

[⬆ back to top](#api-documentation)

</div>
