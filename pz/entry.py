from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Dictionary to hold occupation weightage and remarks


# Create DB function
def create_db():
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        income_per_month REAL,
        age INTEGER,
        rent_per_month REAL,
        loan_repayment_per_month REAL,
        insurance_premium REAL,
        healthcare_cost_per_month REAL,
        education_cost_per_month REAL,
        desired_savings_per_month REAL,
        
    );
    ''')
    conn.commit()
    conn.close()

# Insert user data function
def insert_user_data(income, age, rent, loan_repayment, insurance, healthcare, education, savings):
    
    
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (
        income_per_month, age, rent_per_month, 
        loan_repayment_per_month, insurance_premium, 
        healthcare_cost_per_month, education_cost_per_month, 
        desired_savings_per_month, remarks
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (income, age,  rent, loan_repayment, insurance, healthcare, education, savings))
    
    conn.commit()
    conn.close()

# Route to show form and handle submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Getting user input from the form
        income = float(request.form['income'])
        age = int(request.form['age'])
        
        rent = float(request.form['rent'])
        loan_repayment = float(request.form['loan_repayment'])
        insurance = float(request.form['insurance'])
        healthcare = float(request.form['healthcare'])
        education = float(request.form['education'])
        savings = float(request.form['savings'])
       

        # Insert user data into the database
        insert_user_data(income, age,  rent, loan_repayment, insurance, healthcare, education, savings)

        return redirect(url_for('thank_you'))

    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting your information!"

if __name__ == '__main__':
    create_db()  # Ensure the DB is created on app startup
    app.run(debug=True)
