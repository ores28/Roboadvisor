import pyodbc
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

# Database Connection Function
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-H50EB6O\SQLEXPRESS;'  # Change to your server name if necessary
        'DATABASE=UserInfoDB;'
        'Trusted_Connection=yes;'
    )
    return conn

# Convert number of dependents into binary values for up to 4 dependents
def get_dependency_status(num_dependents):
    return [1 if i < num_dependents else 0 for i in range(4)]

# Insert User Data into Database
def insert_user_data(name, occupation, income, age, rent, loan, insurance, healthcare, education, savings, dependents):
    dep_status = get_dependency_status(dependents)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Users (name, occupation, income_per_month, age, rent_per_month, loan_repayment_per_month, 
                           insurance_premium, healthcare_cost_per_month, education_cost_per_month, 
                           desired_savings_per_month, dependent_1, dependent_2, dependent_3, dependent_4)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, occupation, income, age, rent, loan, insurance, healthcare, education, savings, *dep_status))

    conn.commit()
    conn.close()

# Home route (renders form)
@app.route('/')
def home():
    return render_template('thank_you.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            name = request.form['name']
            occupation = request.form['occupation']
            income = float(request.form['income'])
            age = int(request.form['age'])
            rent = float(request.form['rent'])
            loan = float(request.form['loan'])
            insurance = float(request.form['insurance'])
            healthcare = float(request.form['healthcare'])
            education = float(request.form['education'])
            savings = float(request.form['savings'])
            dependents = int(request.form['dependents'])

            # Insert data into the database
            insert_user_data(name, occupation, income, age, rent, loan, insurance, healthcare, education, savings, dependents)
            
            return redirect(url_for('thank_you'))

        except Exception as e:
            return f"Error: {e}"

# Thank You Page
@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting your information!"

if __name__ == '__main__':
    app.run(debug=True)

   
