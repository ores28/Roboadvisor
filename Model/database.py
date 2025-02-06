import pandas as pd
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mutual_funds.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the database model
class MutualFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(200), nullable=False)
    min_sip = db.Column(db.Float, nullable=False)
    min_lumpsum = db.Column(db.Float, nullable=False)
    expense_ratio = db.Column(db.Float, nullable=False)
    fund_size_cr = db.Column(db.Float, nullable=False)
    fund_age_yr = db.Column(db.Float, nullable=False)
    fund_manager = db.Column(db.String(100), nullable=False)
    sortino = db.Column(db.Float, nullable=True)
    alpha = db.Column(db.Float, nullable=True)
    sd = db.Column(db.Float, nullable=True)
    beta = db.Column(db.Float, nullable=True)
    sharpe = db.Column(db.Float, nullable=True)
    risk_level = db.Column(db.String(50), nullable=False)
    amc_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    sub_category = db.Column(db.String(100), nullable=False)
    returns_1yr = db.Column(db.Float, nullable=True)
    returns_3yr = db.Column(db.Float, nullable=True)
    returns_5yr = db.Column(db.Float, nullable=True)

# Create the database
with app.app_context():
    db.create_all()



# Function to load Kaggle dataset into the database
def load_data():
    try:
        df = pd.read_csv('comprehensive_mutual_funds_data.csv')  # Ensure dataset is in the same directory
        
        if MutualFund.query.first() is None:
            for _, row in df.iterrows():
                fund = MutualFund(
                    scheme_name=row['scheme_name'],
                    min_sip=row['min_sip'],
                    min_lumpsum=row['min_lumpsum'],
                    expense_ratio=row['expense_ratio'],
                    fund_size_cr=row['fund_size_cr'],
                    fund_age_yr=row['fund_age_yr'],
                    fund_manager=row['fund_manager'],
                    sortino=row.get('sortino', None),
                    alpha=row.get('alpha', None),
                    sd=row.get('sd', None),
                    beta=row.get('beta', None),
                    sharpe=row.get('sharpe', None),
                    risk_level=row['risk_level'],
                    amc_name=row['amc_name'],
                    rating=row['rating'],
                    category=row['category'],
                    sub_category=row['sub_category'],
                    returns_1yr=row.get('returns_1yr', None),
                    returns_3yr=row.get('returns_3yr', None),
                    returns_5yr=row.get('returns_5yr', None)
                )
                db.session.add(fund)
            db.session.commit()
            print("Dataset imported successfully!")
        else:
            print("Dataset already exists in the database. Skipping import.")
    
    except Exception as e:
        print(f"Error loading dataset: {e}")

# API Endpoint to retrieve all mutual funds
@app.route('/funds', methods=['GET'])
def get_funds():
    funds = MutualFund.query.all()
    return jsonify([
        {
            'id': fund.id,
            'scheme_name': fund.scheme_name,
            'min_sip': fund.min_sip,
            'min_lumpsum': fund.min_lumpsum,
            'expense_ratio': fund.expense_ratio,
            'fund_size_cr': fund.fund_size_cr,
            'fund_age_yr': fund.fund_age_yr,
            'fund_manager': fund.fund_manager,
            'sortino': fund.sortino,
            'alpha': fund.alpha,
            'sd': fund.sd,
            'beta': fund.beta,
            'sharpe': fund.sharpe,
            'risk_level': fund.risk_level,
            'amc_name': fund.amc_name,
            'rating': fund.rating,
            'category': fund.category,
            'sub_category': fund.sub_category,
            'returns_1yr': fund.returns_1yr,
            'returns_3yr': fund.returns_3yr,
            'returns_5yr': fund.returns_5yr
        }
        for fund in funds
    ])

if __name__ == '__main__':
    with app.app_context():
        if not MutualFund.query.first():  # Only load data if the database is empty
            load_data()
    app.run(debug=True)
