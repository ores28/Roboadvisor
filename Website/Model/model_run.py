from sklearn.linear_model import LinearRegression
import torch
import numpy as np

def predict_risk_tolerance(data):
    # Load the trained model parameters
    loaded_params = torch.load('Roboadvisor\Website\Model\linear_regression_model.pth', weights_only=False)
    loaded_model = LinearRegression()
    loaded_model.coef_ = np.array(loaded_params['coef_'])
    loaded_model.intercept_ = np.array(loaded_params['intercept_'])

    # Convert data to a NumPy array before prediction
    risk_tolerance = loaded_model.predict(data.to_numpy())
    return risk_tolerance[0]