# ExplainX - Loan Prediction with Explainable AI

<div align="center">

![ExplainX](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-brightgreen)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

**A web-based loan prediction system powered by Machine Learning and Explainable AI (XAI) using SHAP values and NLP-driven explanations.**

[Getting Started](#getting-started) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

ExplainX is an advanced loan prediction system that combines machine learning with explainable AI (XAI) to provide transparent and interpretable loan approval/rejection decisions. Unlike traditional black-box models, ExplainX uses **SHAP (SHapley Additive exPlanations)** values and **Natural Language Processing** to explain why a loan application was approved or rejected.

### Key Problem Statement
Traditional loan prediction systems often act as "black boxes," making decisions without explaining the reasoning. This creates trust issues and regulatory compliance challenges. ExplainX solves this by providing:
- Clear, human-readable explanations for every prediction
- SHAP-based visual interpretations showing feature contributions
- Actionable coaching tips for rejected applicants
- Complete prediction history and analytics dashboard

---

## ✨ Features

### 🤖 Core Prediction Engine
- **ML-Based Loan Classification**: Uses trained ensemble models for accurate predictions
- **Confidence Scoring**: Provides probability estimates for each prediction
- **Real-time Processing**: Instant predictions on user input

### 📊 Explainability Features
- **SHAP Waterfall Plots**: Visual representation of feature contributions
- **Feature Impact Analysis**: Shows positive and negative drivers of decisions
- **Natural Language Explanations**: Human-readable explanations generated using spaCy and NLTK
- **Coaching Tips**: Actionable recommendations for improvement

### 💾 Data Management
- **SQLite Database**: Persistent storage of all predictions and user interactions
- **Prediction History**: Track all past predictions and their outcomes
- **Analytics Dashboard**: Real-time statistics and trends

### 🎨 User Interface
- **Intuitive Web Dashboard**: Clean, responsive Flask-based web application
- **Interactive Forms**: User-friendly input forms for loan applications
- **Visual Analytics**: Charts and graphs for performance metrics
- **Mobile-Responsive Design**: Works seamlessly on desktop and mobile devices

### 📈 Analytics & Monitoring
- **Approval Rate Tracking**: Real-time statistics on approval/rejection ratios
- **Prediction Metrics**: Total predictions, approved, and rejected counts
- **Recent Activity Feed**: Latest predictions displayed with details
- **Performance Insights**: Actionable insights from prediction data

---

## 🛠️ Tech Stack

### Backend
- **Flask 2.0+**: Web framework for Python
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning models
- **SHAP**: Explainable AI library
- **Joblib**: Model serialization and persistence

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive styling
- **JavaScript**: Interactive features
- **Bootstrap/CSS Framework**: UI components (implied)

### NLP & Data Processing
- **spaCy**: Natural language processing
- **NLTK**: Text tokenization and processing
- **Matplotlib**: Data visualization

### Database
- **SQLite3**: Lightweight relational database

### Development Tools
- **Python 3.8+**: Core programming language
- **Git**: Version control

---

## 📁 Project Structure

```
ExplainX_final_PAI/
├── app.py                          # Main Flask application
├── db.py                           # Database initialization and schema
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── best_model.pkl                  # Trained ML model
├── loan_data.csv                   # Original loan dataset
├── preprocessed_loan_data.csv      # Cleaned and preprocessed data
├── eda.ipynb                       # Exploratory Data Analysis notebook
├── explainx.db                     # SQLite database
│
├── explain/
│   └── shap_engine.py             # SHAP-based explanation generation
│
├── nlp/
│   └── explanation_engine.py      # NLP-based text explanations
│
├── static/
│   ├── shap/                      # SHAP plot storage
│   └── css/                       # Stylesheet files (implied)
│
└── templates/
    ├── base.html                  # Base template (navigation, layout)
    ├── index.html                 # Home page
    ├── dashboard.html             # Analytics dashboard
    ├── result.html                # Prediction results page
    ├── history.html               # Prediction history page
    ├── metrics.html               # Metrics and statistics
    └── settings.html              # Configuration page
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- 500MB disk space for dependencies and models

### Quick Start (5 minutes)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ExplainX_final_PAI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the web interface**
   - Open your browser and navigate to `http://localhost:5000`

---

## 📚 Installation

### Detailed Installation Guide

For detailed installation instructions including troubleshooting, see [INSTALLATION.md](INSTALLATION.md).

### System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows, macOS, Linux |
| **Python** | 3.8 - 3.11 |
| **RAM** | Minimum 2GB (Recommended 4GB+) |
| **Storage** | 500MB available space |
| **Browser** | Modern browser (Chrome, Firefox, Safari, Edge) |

---

## 💻 Usage

### Using the Web Interface

#### 1. **Home Page**
- Navigate to the home page to view the application overview
- Click "Make a Prediction" to start a new loan assessment

#### 2. **Making a Prediction**
- Fill in the loan application form with the following details:
  - **Personal Information**: Gender, Marital Status, Dependents, Education
  - **Employment**: Self-Employment Status
  - **Financial**: Applicant Income, Co-applicant Income
  - **Loan Details**: Loan Amount, Loan Term
  - **Credit**: Credit History
  - **Property**: Property Area (Urban, Semi-Urban, Rural)

- Click "Submit" to get an instant prediction with explanation

#### 3. **Understanding the Result**
- **Prediction**: APPROVED or REJECTED status
- **Confidence Score**: Probability of the prediction
- **SHAP Plot**: Visual representation of feature contributions
- **Explanation**: Natural language explanation of the decision
- **Coaching Tips**: Actionable recommendations (especially for rejections)

#### 4. **Dashboard**
- View real-time statistics on predictions
- Monitor approval rates and trends
- Check recent prediction activity
- Track total approved/rejected applications

#### 5. **Prediction History**
- Browse all past predictions
- Filter and search through history
- Export prediction data

---

## 🔌 API Documentation

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/` | Home page |
| **GET** | `/dashboard` | Analytics dashboard |
| **POST** | `/predict` | Make a prediction |
| **GET** | `/history` | View prediction history |
| **GET** | `/metrics` | Get metrics data |

### Example Request

```bash
curl -X POST http://localhost:5000/predict \
  -d "Gender=1&Married=1&Dependents=0&Education=1&Self_Employed=0&ApplicantIncome=5000&CoapplicantIncome=0&LoanAmount=150&Loan_Amount_Term=360&Credit_History=1&Property_Area=2"
```

---

## ⚙️ Configuration

### Environment Configuration

Create a `.env` file in the project root (optional):

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_PATH=explainx.db
MODEL_PATH=best_model.pkl
```

### Model Configuration

- **Model Type**: Trained ensemble classifier
- **Model File**: `best_model.pkl`
- **Input Features**: 11 features (see Database Schema)
- **Output**: Binary classification (0=REJECTED, 1=APPROVED)

### Database Configuration

- **Type**: SQLite3
- **Location**: `explainx.db`
- **Auto-initialization**: Yes (runs on first start)

---

## 🗄️ Database Schema

### Predictions Table

```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender INTEGER,                 -- 0: Female, 1: Male
    married INTEGER,               -- 0: No, 1: Yes
    dependents INTEGER,            -- 0-3+
    education INTEGER,             -- 0: Graduate, 1: Undergraduate
    self_employed INTEGER,         -- 0: No, 1: Yes
    applicant_income REAL,         -- Monthly income in rupees
    coapplicant_income REAL,       -- Co-applicant income in rupees
    loan_amount REAL,              -- Loan amount in thousands
    loan_term REAL,                -- Loan term in months
    credit_history REAL,           -- 0: No, 1: Yes
    property_area INTEGER,         -- 0: Urban, 1: Semi-Urban, 2: Rural
    prediction TEXT,               -- APPROVED or REJECTED
    created_at TIMESTAMP           -- Prediction timestamp
);
```

---

## 🏗️ Architecture

For detailed technical architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Web Browser                            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Flask Web Application                       │
│  (app.py - Route Handling, Session Management)          │
└────────────┬──────────────────────┬────────────────────┘
             │                      │
             ▼                      ▼
┌─────────────────────┐   ┌──────────────────────┐
│ Prediction Engine   │   │  Database Layer      │
│  - Model Loading    │   │  (SQLite3)           │
│  - Input Processing │   │  (db.py)             │
│  - SHAP Explainer   │   │  - Store Predictions │
│  (explain/)         │   │  - Retrieve History  │
└────────┬────────────┘   └──────────────────────┘
         │
         ├──────────────┬──────────────────┐
         │              │                  │
         ▼              ▼                  ▼
    ┌─────────┐   ┌──────────┐   ┌──────────────┐
    │ SHAP    │   │  Model   │   │ NLP Engine   │
    │ Engine  │   │  Joblib  │   │ (spaCy,NLTK) │
    │(explain)│   │(pkl file)│   │ (nlp/)       │
    └─────────┘   └──────────┘   └──────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
                        ▼
         ┌──────────────────────────┐
         │  Explainability Output   │
         │ - SHAP Plots (PNG)       │
         │ - Text Explanations      │
         │ - Coaching Tips          │
         └──────────────────────────┘
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
   ```bash
   git clone <your-fork-url>
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 coding standards
   - Add comments for complex logic
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python app.py  # Test locally
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues

### Contribution Guidelines

- **Code Style**: Follow PEP 8
- **Documentation**: Update README and docs for new features
- **Testing**: Test thoroughly before submitting PR
- **Commits**: Use clear, descriptive commit messages
- **Issues**: Check existing issues before creating new ones

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Contact

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for feature requests
- **Documentation**: Check [ARCHITECTURE.md](ARCHITECTURE.md) and [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🙏 Acknowledgments

- **SHAP Library**: For explainability visualizations
- **Flask**: For the web framework
- **Scikit-learn**: For machine learning tools
- **spaCy & NLTK**: For NLP capabilities

---

## 📊 Project Stats

- **Language**: Python 3.8+
- **Total Dependencies**: 7
- **Database**: SQLite3
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Type**: Machine Learning + Web Application

---

<div align="center">

**Built with ❤️ for Explainable AI**

[⬆ back to top](#explainx---loan-prediction-with-explainable-ai)

</div>
