from sklearn.linear_model import LinearRegression
import torch
import numpy as np
import pandas as pd

loaded_params = torch.load('Roboadvisor\Model\linear_regression_model.pth', weights_only=False)
loaded_model = LinearRegression()
loaded_model.coef_ = np.array(loaded_params['coef_'])
loaded_model.intercept_ = np.array(loaded_params['intercept_'])


new_data = pd.DataFrame({
    'Income_per_month': [50000],
    'Age': [30],
    'Dependents': [1],
    'Rent_per_month': [10000],
    'Loan_Repayment_per_month': [5000],
    'Insurance_premium': [2000],
    'Healthcare_cost_per_month': [3000],
    'Education_cost_per_month': [4000],
    'Desired_Savings_per_month': [7000],
    'Occupation_Weight': [0.6]
})

new_risk_tolerance = loaded_model.predict(new_data)
print(f'Predicted Risk Tolerance for new data: {new_risk_tolerance[0]}')