from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from Model.model_run import predict_risk_tolerance
from Model.portfolio_allocation import optimize_portfolio

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Database Model
class FinancialDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
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
    risk_tolerance = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    cmf2 = db.Column(db.Float)
    nb2 = db.Column(db.Float)
    nb3 = db.Column(db.Float)
    gibf1 = db.Column(db.Float)

    def __repr__(self):
        return f'<Entry {self.id}>'
    
with app.app_context():
    db.create_all()
# Helper function to encode categorical values
def encode_dependents(no_of_dependents):
    dependents = {f"dependents_{i}": int(no_of_dependents == str(i)) for i in range(5)}
    return dependents

def encode_occupation(occupation):
    occupations = ["Professional", "Retired", "Self Employed", "Student"]
    return {f"occupation_{o.lower().replace(' ', '_')}": int(occupation == o) for o in occupations}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        form_data = {key: request.form[key] for key in request.form}
        
        # Encode categorical features
        dependents_encoded = encode_dependents(form_data["no_of_dependents"])
        occupation_encoded = encode_occupation(form_data["occupation"])
        
        # Prepare DataFrame for prediction
        df_data = {**form_data, **dependents_encoded, **occupation_encoded}
        df_data.pop("no_of_dependents")
        df_data.pop("occupation")
        df_data.pop("name")
        df = pd.DataFrame(df_data, index=[0])

        # Predict risk tolerance
        risk_tolerance = predict_risk_tolerance(df)
        risk_tolerance = risk_tolerance*10
        if risk_tolerance < 0:
            risk_tolerance = 0
        print(f"Risk Tolerance: {risk_tolerance}")
        optimized_portfolio = optimize_portfolio(risk_tolerance, float(form_data["desired_saving_per_month"]))

        if optimized_portfolio is not None:
            for i in range(len(optimized_portfolio['Source'])):
                source_value = optimized_portfolio['Source'][i]
                investment_value = optimized_portfolio['Investment_Amount'][i]

                if source_value == "cmf2":
                    form_data["cmf2"] = int(investment_value)
                elif source_value == "nb2":
                    form_data["nb2"] = int(investment_value)
                elif source_value == "nb3":
                    form_data["nb3"] = int(investment_value)
                elif source_value == "gibf1":
                    form_data["gibf1"] = int(investment_value)

        # Create & save new database entry
        new_entry = FinancialDatabase(
            **form_data,  # Unpacking form data
            risk_tolerance=risk_tolerance
        )

        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('index', submitted='true'))
        except Exception as e:
            return f'Error adding entry: {str(e)}'

    # Fetch database records if submitted
    submitted = request.args.get('submitted', 'false').lower() == 'true'
    entries = FinancialDatabase.query.order_by(FinancialDatabase.date_created).all() if submitted else []
    return render_template('index.html', entries=entries, submitted=submitted)

@app.route("/user/", methods=["POST"])
def get_user_data():
    requested_user_id = request.form.get("user-id")  # Retrieves the entered user ID
    if requested_user_id:
        try:
            user_id = int(requested_user_id)  # Convert user ID from string to integer
            entry = FinancialDatabase.query.filter(FinancialDatabase.id == user_id).first()  
        except ValueError:
            print("Invalid user ID received")  
        return render_template("user.html", entries=entry, user_id=requested_user_id)


@app.route('/delete/<int:id>')
def delete(id):
    entry_to_delete = FinancialDatabase.query.get_or_404(id)
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        return redirect(url_for('index', submitted='false'))
    except Exception as e:
        return f'Error deleting entry: {str(e)}'

if __name__ == "__main__":
    app.run(debug=True)