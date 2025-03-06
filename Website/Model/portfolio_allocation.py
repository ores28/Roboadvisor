import pandas as pd

def optimize_portfolio(user_risk_tolerance, desired_savings_per_month):
    # Load the CSV containing the weights and asset information
    df = pd.read_csv("Model\Data\Thresholds.csv")

    # Initialize variables for the assets
    df['Adjusted_Weight'] = 0.0  # Initialize a column for adjusted weights
    
    # Exclude assets based on the user's risk tolerance and threshold
    df['Selected'] = df['Optimized_Threshold'] >= user_risk_tolerance
    
    # Filter out assets that do not meet the risk tolerance - create an explicit copy
    selected_assets = df[df['Selected'] == True].copy()
    
    if selected_assets.empty:
        print("No assets meet the risk tolerance. Please lower the risk tolerance.")
        return None
    
    # Calculate the adjusted weights using .loc accessor
    total_ip_value = selected_assets['Optimized_Threshold'].sum()
    selected_assets.loc[:, 'Adjusted_Weight'] = selected_assets['Optimized_Threshold'] / total_ip_value
    
    # Normalize the weights using .loc
    selected_assets.loc[:, 'Adjusted_Weight'] = selected_assets['Adjusted_Weight'] / selected_assets['Adjusted_Weight'].sum()
    
    # Calculate investment amount using .loc
    selected_assets.loc[:, 'Investment_Amount'] = selected_assets['Adjusted_Weight'] * desired_savings_per_month
    
    # Convert DataFrame to list of dictionaries
    optimized_portfolio = selected_assets[['Asset_Class', 'Source', 'Optimized_Threshold', 'Adjusted_Weight', 'Investment_Amount']]
    
    optimized_portfolio = optimized_portfolio.to_dict(orient="records")
    return optimized_portfolio