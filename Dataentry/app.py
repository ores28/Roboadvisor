from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finances.db'  # Database name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the model
class FinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    income_per_month = db.Column(db.Float, nullable=False)
    rent_per_month = db.Column(db.Float, nullable=False)
    loan_repayment_per_month = db.Column(db.Float, nullable=False)
    insurance_premium = db.Column(db.Float, nullable=False)
    healthcare_cost_per_month = db.Column(db.Float, nullable=False)
    education_cost_per_month = db.Column(db.Float, nullable=False)
    desired_saving_per_month = db.Column(db.Float, nullable=False)
    no_of_dependents = db.Column(db.String(10), nullable=False)
    occupation = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Entry {self.id}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve data from the form
        age = request.form['age']
        income_per_month = request.form['income_per_month']
        rent_per_month = request.form['rent_per_month']
        loan_repayment_per_month = request.form['loan_repayment_per_month']
        insurance_premium = request.form['insurance_premium']
        healthcare_cost_per_month = request.form['healthcare_cost_per_month']
        education_cost_per_month = request.form['education_cost_per_month']
        desired_saving_per_month = request.form['desired_saving_per_month']
        no_of_dependents = request.form['no_of_dependents']
        occupation = request.form['occupation']

        # Create a new database entry
        new_entry = FinancialData(
            age=age,
            income_per_month=income_per_month,
            rent_per_month=rent_per_month,
            loan_repayment_per_month=loan_repayment_per_month,
            insurance_premium=insurance_premium,
            healthcare_cost_per_month=healthcare_cost_per_month,
            education_cost_per_month=education_cost_per_month,
            desired_saving_per_month=desired_saving_per_month,
            no_of_dependents=no_of_dependents,
            occupation=occupation,
        )

        try:
            db.session.add(new_entry)
            db.session.commit()
            # Redirect to the table view
            return redirect(url_for('index', submitted='true'))
        except Exception as e:
            return f'There was an issue adding the entry: {str(e)}'

    # Handle GET requests
    submitted = request.args.get('submitted', 'false').lower() == 'true'
    entries = FinancialData.query.order_by(FinancialData.date_created).all() if submitted else []
    return render_template('index.html', entries=entries, submitted=submitted)

@app.route('/delete/<int:id>')
def delete(id):
    entry_to_delete = FinancialData.query.get_or_404(id)
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        # Stay on the table view after deleting
        return redirect(url_for('index', submitted='true'))
    except Exception as e:
        return f'There was a problem deleting the entry: {str(e)}'

if __name__ == "__main__":
    app.run(debug=True)
