import sqlite3

conn = sqlite3.connect("explainx.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    gender INTEGER,
    married INTEGER,
    dependents INTEGER,
    education INTEGER,
    self_employed INTEGER,

    applicant_income REAL,
    coapplicant_income REAL,

    loan_amount REAL,
    loan_term REAL,

    credit_history REAL,

    property_area INTEGER,

    prediction TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

conn.close()

print("Database Created Successfully")