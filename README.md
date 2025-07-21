# RoboAdvisor

A comprehensive AI-powered financial advisory system that provides personalized investment recommendations and portfolio optimization using machine learning algorithms.

## Overview

RoboAdvisor is an intelligent financial advisory platform that combines multiple machine learning approaches to deliver personalized investment advice. The system analyzes user financial data, risk tolerance, and investment preferences to generate optimized portfolio allocations and investment strategies.

## Features

### 🤖 AI-Powered Risk Assessment
- **Machine Learning Models**: Multiple algorithms for risk tolerance prediction
- **Genetic Algorithm Optimization**: Advanced portfolio optimization techniques
- **Linear Regression Models**: Traditional statistical approaches for baseline comparisons

### 💼 Portfolio Management
- **Automated Portfolio Allocation**: AI-driven asset distribution recommendations
- **Risk-Adjusted Returns**: Optimization based on user risk profile
- **Diversification Strategies**: Multi-asset class portfolio construction

### 🌐 Web Interface
- **User-Friendly Dashboard**: Interactive web application built with Flask
- **User Authentication**: Secure login and registration system
- **Real-time Recommendations**: Dynamic portfolio suggestions
- **Financial Data Visualization**: Charts and graphs for portfolio analysis

### 📊 Data Analytics
- **Historical Data Analysis**: Comprehensive financial market data processing
- **Performance Metrics**: R² scores, MSE, and other evaluation metrics
- **Backtesting Capabilities**: Historical performance validation

## Project Structure

```
Roboadvisor/
├── Website/                 # Flask web application
│   ├── app.py              # Main Flask application
│   ├── Model/              # ML models and algorithms
│   ├── static/             # CSS, JavaScript, images
│   ├── templates/          # HTML templates
│   └── instance/           # Database files
├── Genetic_train/          # Genetic algorithm training
│   ├── bankdata/           # Financial datasets
│   ├── results/            # Training results and outputs
│   └── train_notebooks/    # Jupyter notebooks for GA training
├── Linear_reg_train/       # Linear regression models
│   ├── model_train.ipynb   # Linear regression training notebook
│   └── Data/               # Training datasets
└── README.md               # This file
```

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **SQLite** - Database

### Frontend
- **HTML5/CSS3**
- **JavaScript**
- **Bootstrap** - UI framework
- **Chart.js** - Data visualization

### Machine Learning
- **Genetic Algorithms** - Portfolio optimization
- **Linear Regression** - Risk assessment
- **Neural Networks** - Advanced prediction models
- **Cross-validation** - Model validation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Roboadvisor
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-login pandas numpy scikit-learn werkzeug
   ```

3. **Set up the database**
   ```bash
   cd Website
   python -c "from app import db; db.create_all()"
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Usage

### Web Application
1. **Register/Login**: Create an account or log in to existing account
2. **Profile Setup**: Enter your financial information and investment preferences
3. **Risk Assessment**: Complete the risk tolerance questionnaire
4. **Portfolio Generation**: Receive AI-generated portfolio recommendations
5. **Monitor Performance**: Track your portfolio's performance over time

### Training Models
1. **Genetic Algorithm Training**:
   ```bash
   cd Genetic_train/train_notebooks
   jupyter notebook GA.ipynb
   ```

2. **Linear Regression Training**:
   ```bash
   cd Linear_reg_train
   jupyter notebook model_train.ipynb
   ```

## Model Performance

### Evaluation Metrics
- **R² Score**: Measures the proportion of variance explained by the model
- **Mean Squared Error (MSE)**: Average squared difference between predicted and actual values
- **Cross-Validation Scores**: Model generalization performance

### Why These Metrics?
- **R² Score**: Indicates how well the model explains the variability in the data (0-1 scale)
- **MSE**: Provides a measure of prediction accuracy (lower is better)
- **Combined Analysis**: Using both metrics gives a comprehensive view of model performance

## API Endpoints

### User Management
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /logout` - User logout

### Portfolio Management
- `GET /dashboard` - User dashboard
- `POST /update_profile` - Update user financial profile
- `GET /portfolio` - Get portfolio recommendations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Data Sources

- **Financial Market Data**: Historical stock prices, bonds, ETFs
- **Economic Indicators**: Interest rates, inflation data, GDP growth
- **Risk Metrics**: Volatility measures, correlation matrices

## Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Session Management**: Flask-Login for user session handling
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CSRF Protection**: Cross-site request forgery prevention

## Future Enhancements

- [ ] Real-time market data integration
- [ ] Advanced ML models (LSTM, Transformer networks)
- [ ] Mobile application development
- [ ] API for third-party integrations
- [ ] Advanced risk analytics
- [ ] ESG (Environmental, Social, Governance) investing options

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please open an issue on the GitHub repository or contact the development team.

## Acknowledgments

- Financial data providers
- Open-source machine learning libraries
- Flask and Python communities
- Academic research in quantitative finance

---

**Disclaimer**: This software is for educational and research purposes. It does not constitute financial advice. Always consult with qualified financial advisors before making investment decisions.