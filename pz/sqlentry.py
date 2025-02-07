import pyodbc
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')


# Connect to the SQL Server
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost;'
        'DATABASE=UserInfoDB;'
        'Trusted_Connection=yes;'
    )
    return conn

# Function to determine dependency status (0 or 1) for up to 4 individuals
def get_dependency_status(num_dependents):
    return [1 if i < num_dependents else 0 for i in range(4)]  # Returns list of 4 values (0 or 1)

# Insert data into SQL Server
def insert_user_data(income, age, rent, loan_repayment, insurance, healthcare, education, savings, occupation, dependents):
    dep_status = get_dependency_status(dependents)  # Convert dependency count to binary values

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
    INSERT INTO Users (income_per_month, age, rent_per_month, loan_repayment_per_month, 
                       insurance_premium, healthcare_cost_per_month, education_cost_per_month, 
                       desired_savings_per_month, occupation, dependent_1, dependent_2, dependent_3, dependent_4)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (income, age, rent, loan_repayment, insurance, healthcare, education, savings, occupation, *dep_status))
    
    conn.commit()
    conn.close()

# Home route (GET)
@app.route('/')
def home():
    return render_template('final2.html')  # Show the form

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get data from the form
        income = float(request.form['income'])
        age = int(request.form['age'])
        rent = float(request.form['rent'])
        loan_repayment = float(request.form['loan_repayment'])
        insurance = float(request.form['insurance'])
        healthcare = float(request.form['healthcare'])
        education = float(request.form['education'])
        savings = float(request.form['savings'])
        occupation = request.form['occupation']  # Get occupation from form
        dependents = int(request.form['dependents'])  # Number of dependents (0-4)

        # Insert the data into the database
        insert_user_data(income, age, rent, loan_repayment, insurance, healthcare, education, savings, occupation, dependents)
        return redirect(url_for('thank_you'))

# Thank you page after submission
@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting your information!"

if __name__ == '__main__':
    app.run(debug=True)
