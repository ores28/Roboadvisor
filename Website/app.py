from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from Model.model_run import predict_risk_tolerance
from Model.portfolio_allocation import optimize_portfolio
import os

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_finances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # For session management
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not logged in

class FinancialDatabase(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    income_per_month = db.Column(db.Float)
    rent_per_month = db.Column(db.Float)
    loan_repayment_per_month = db.Column(db.Float)
    insurance_premium = db.Column(db.Float)
    healthcare_cost_per_month = db.Column(db.Float)
    education_cost_per_month = db.Column(db.Float)
    desired_saving_per_month = db.Column(db.Float)
    no_of_dependents = db.Column(db.String(10))
    occupation = db.Column(db.String(50))
    risk_tolerance = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.now)
    cmf2 = db.Column(db.Float)
    nb2 = db.Column(db.Float)
    nb3 = db.Column(db.Float)
    gibf1 = db.Column(db.Float)
    cmf1 = db.Column(db.Float)
    kef = db.Column(db.Float)
    lvf = db.Column(db.Float)
    mmf1 = db.Column(db.Float)
    niblstf = db.Column(db.Float)
    rmf1 = db.Column(db.Float)
    sfmf = db.Column(db.Float)

    def __repr__(self):
        return f'<Entry {self.id}>'
    
with app.app_context():
    db.create_all()

# Helper function to encode categorical values
def encode_dependents(no_of_dependents):
    return {f"dependents_{i}": int(no_of_dependents == str(i)) for i in range(5)}

def encode_occupation(occupation):
    occupations = ["Professional", "Retired", "Self Employed", "Student"]
    return {f"occupation_{o.lower().replace(' ', '_')}": int(occupation == o) for o in occupations}

# Login Manager
@login_manager.user_loader
def load_user(user_id):
    return FinancialDatabase.query.get(int(user_id))

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = FinancialDatabase.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):  # Password hash check
            login_user(user)
            flash('Login Successful!', 'success')
            return render_template("index.html" if user.risk_tolerance is None else "user.html", entries=user)
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if FinancialDatabase.query.filter_by(email=email).first():
            flash('Email already exists! Please login.', 'danger')
            return redirect(url_for('register'))
        
        # Hash the password before saving
        hashed_password = generate_password_hash(password)
        new_user = FinancialDatabase(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration Successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error occurred: {e}', 'danger')
            
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        form_data = {key: request.form[key] for key in request.form}
        
        # Update the current user with the form data
        for key, value in form_data.items():
            setattr(current_user, key, value)
        
        dependents_encoded = encode_dependents(form_data["no_of_dependents"])
        occupation_encoded = encode_occupation(form_data["occupation"])
        
        # Prepare DataFrame for prediction
        df_data = {**form_data, **dependents_encoded, **occupation_encoded}
        df_data.pop("no_of_dependents")
        df_data.pop("occupation")
        df = pd.DataFrame(df_data, index=[0])

        # Predict risk tolerance
        risk_tolerance_cal = predict_risk_tolerance(df)
        risk_tolerance = risk_tolerance_cal * 20
        current_user.risk_tolerance = max(risk_tolerance, 0)
        print(f"Risk Tolerance: {current_user.risk_tolerance}")

        saving = float(form_data['income_per_month']) - float(form_data['rent_per_month']) - float(form_data['loan_repayment_per_month']) - float(form_data['insurance_premium']) - float(form_data['healthcare_cost_per_month']) - float(form_data['education_cost_per_month'])
        # Optimize portfolio
        optimized_portfolio = optimize_portfolio(risk_tolerance, saving)

        # Update the portfolio data
        if optimized_portfolio:
            for entry in optimized_portfolio:
                source_value = entry['Source']
                investment_value = entry['Investment_Amount']
                if source_value in ['cmf2', 'nb2', 'nb3', 'gibf1', 'cmf1', 'kef', 'lvf', 'mmf1', 'niblstf', 'rmf1', 'sfmf']:
                    setattr(current_user, source_value, investment_value)
        db.session.commit()
        return render_template("user.html", entries=current_user)
    return render_template('index.html')

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    entry_to_delete = FinancialDatabase.query.get_or_404(id)
    try:
        db.session.delete(entry_to_delete)
        db.session.commit()
        flash('Entry deleted successfully', 'info')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error deleting entry: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)