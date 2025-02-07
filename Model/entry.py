from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Dictionary to hold occupation weightage and remarks
occupation_data = {
    "Student": {"weightage": 0.8, "remarks": "Higher risk tolerance due to fewer financial responsibilities and long-term earning potential."},
    "Retired": {"weightage": 0.2, "remarks": "Very low risk tolerance; focus on preserving savings for stability and healthcare."},
    "Professional": {"weightage": 0.6, "remarks": "Moderate to high risk tolerance depending on income stability and career progression."},
    "Self-Employed": {"weightage": 0.35, "remarks": "Lower risk tolerance due to inconsistent incomes and limited safety nets."},
    "Other": {"weightage": 0.35, "remarks": "Varies based on personal and career circumstances."}
}

# Create DB function
def create_db():
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        income_per_month REAL,
        age INTEGER,
        dependents INTEGER,
        rent_per_month REAL,
        loan_repayment_per_month REAL,
        insurance_premium REAL,
        healthcare_cost_per_month REAL,
        education_cost_per_month REAL,
        desired_savings_per_month REAL,
        occupation TEXT,
        weightage REAL,
        remarks TEXT
    );
    ''')
    conn.commit()
    conn.close()

# Insert user data function
def insert_user_data(income, age, dependents, rent, loan_repayment, insurance, healthcare, education, savings, occupation):
    weightage = occupation_data.get(occupation, {}).get("weightage", 0.35)  # Default to 0.5 if not found
    remarks = occupation_data.get(occupation, {}).get("remarks", "Varies based on personal and career circumstances.")
    
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (
        income_per_month, age, dependents, rent_per_month, 
        loan_repayment_per_month, insurance_premium, 
        healthcare_cost_per_month, education_cost_per_month, 
        desired_savings_per_month, occupation, weightage, remarks
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (income, age, dependents, rent, loan_repayment, insurance, healthcare, education, savings, occupation, weightage, remarks))
    
    conn.commit()
    conn.close()

# Route to show form and handle submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Getting user input from the form
        income = float(request.form['income'])
        age = int(request.form['age'])
        dependents = int(request.form['dependents'])
        rent = float(request.form['rent'])
        loan_repayment = float(request.form['loan_repayment'])
        insurance = float(request.form['insurance'])
        healthcare = float(request.form['healthcare'])
        education = float(request.form['education'])
        savings = float(request.form['savings'])
        occupation = request.form['occupation']

        # Insert user data into the database
        insert_user_data(income, age, dependents, rent, loan_repayment, insurance, healthcare, education, savings, occupation)

        return redirect(url_for('thank_you'))

    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting your information!"

if __name__ == '__main__':
    create_db()  # Ensure the DB is created on app startup
    app.run(debug=True)
