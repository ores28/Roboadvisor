from sklearn.linear_model import LinearRegression
import torch
import numpy as np
import pandas as pd

# Load the trained model parameters
loaded_params = torch.load('Model\linear_regression_model.pth', weights_only=False)
loaded_model = LinearRegression()
loaded_model.coef_ = np.array(loaded_params['coef_'])
loaded_model.intercept_ = np.array(loaded_params['intercept_'])

# New input data
new_data = pd.DataFrame({
    'Income_per_month': [50000],
    'Age': [30],
    'Rent_per_month': [10000],
    'Loan_Repayment_per_month': [5000],
    'Insurance_premium': [2000],
    'Healthcare_cost_per_month': [3000],
    'Education_cost_per_month': [4000],
    'Desired_Savings_per_month': [7000],
    'Dependents_0': [0],
    'Dependents_1': [1],
    'Dependents_2': [0],
    'Dependents_3': [0],
    'Dependents_4': [0],
    'Occupation_Professional': [1],
    'Occupation_Retired': [0],
    'Occupation_Self_Employed': [0],
    'Occupation_Student': [0],
})

# Convert new_data to a NumPy array before prediction
new_risk_tolerance = loaded_model.predict(new_data.to_numpy())

print(f'Predicted Risk Tolerance for new data: {new_risk_tolerance[0]}')
