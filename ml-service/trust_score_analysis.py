"""
Trust Score Prediction Analysis
Project: Behavioral Activity Trust Scoring
--------------------------------------------------
This script performs exploration, preprocessing, and model training
for predicting trust scores based on synthetic behavioral data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio
import joblib
import warnings

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# --- Configuration & Settings ---
warnings.simplefilter(action="ignore")
pio.templates.default = "plotly_dark"
plt.style.use('ggplot')

# --- 1. Data Generation ---
def generate_data(n_samples=10000):
    """Generates synthetic behavioral data for analysis."""
    np.random.seed(42)
    data = {
        'totalInteractions': np.random.poisson(50, n_samples),
        'totalSessions': np.random.poisson(10, n_samples),
        'avgTimeBetweenEvents': np.random.exponential(5, n_samples),
        'uniquePages': np.random.poisson(8, n_samples),
        'avgSessionDuration': np.random.exponential(200, n_samples),
        'totalSessionsCount': np.random.poisson(10, n_samples),
    }
    df = pd.DataFrame(data)
    
    # Custom Logic: High activity = Higher Score, Fast Clicks = Lower Score
    score = 50 
    score += (df['totalInteractions'] / 10).clip(0, 20)
    score += (df['uniquePages'] / 2).clip(0, 15)
    score -= (df['avgTimeBetweenEvents'] < 1).astype(int) * 20
    score -= (df['totalSessionsCount'] > 100).astype(int) * 10
    df['trust_score'] = score.clip(0, 100)
    return df

print("Generating synthetic dataset...")
df = generate_data(10000)

# --- 2. Data Profiling ---
print("\n--- Data Information ---")
df.info()

print("\nMissing Values Check:")
print(df.isna().sum())

print("\nDuplicate Rows Check:", df.duplicated().sum())

# --- 3. Exploratory Data Analysis (EDA) ---

# Distribution of Target Variable
plt.figure(figsize=(10, 5)) 
sns.histplot(df['trust_score'], bins=20, kde=True, color="blue") 
plt.title('Distribution of Trust Scores') 
plt.xlabel('Trust Score (0-100)') 
plt.ylabel('Frequency') 
plt.show() 

# Boxplot for Interactions
plt.figure(figsize=(10, 5))
sns.boxplot(x=df['totalInteractions']) 
plt.title('Interactions Distribution') 
plt.show() 

# Risk Level Categorization
df['risk_level'] = pd.cut(df['trust_score'], bins=[0, 40, 70, 100], labels=['High', 'Medium', 'Low'])
risk_counts = df['risk_level'].value_counts() 

# Risk Level Pie Chart
fig = px.pie(values=risk_counts.values, names=risk_counts.index, title='Risk Level Distribution')
fig.update_traces(textinfo='label+percent') 
fig.show() 

# Interactions vs Trust Score Scatter Plot
plt.figure(figsize=(10, 5)) 
sns.scatterplot(data=df, x='totalInteractions', y='trust_score', hue='risk_level')
plt.title('Interactions vs Trust Score') 
plt.show() 

# --- 4. Outlier Handling ---
def outliers_handler(real_data: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Handles outliers using the IQR method."""
    data = real_data.copy() 
    q1 = np.percentile(data[col_name], 25) 
    q3 = np.percentile(data[col_name], 75) 
    iqr = q3 - q1 
    upper_bound = q3 + (1.5 * iqr) 
    lower_bound = q1 - (1.5 * iqr) 
     
    outliers = (data[col_name] > upper_bound) | (data[col_name] < lower_bound) 
    num_of_outliers = len(data[outliers]) 
    
    # If outliers are less than 10%, remove them, otherwise cap them
    if num_of_outliers <= len(data) * 0.1: 
        data = data[~outliers] 
    else: 
        data.loc[data[col_name] > upper_bound, col_name] = upper_bound 
        data.loc[data[col_name] < lower_bound, col_name] = lower_bound 
    return data 

numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

for col in numeric_columns: 
    if col == 'trust_score': 
        continue 
    df = outliers_handler(df, col) 

# --- 5. Feature Engineering & Preprocessing ---

# Encoding Label for Analysis (Risk Level)
le = LabelEncoder() 
df['risk_level_encoded'] = le.fit_transform(df['risk_level']) 

# Splitting Features and Target
X = df.drop(columns=['trust_score', 'risk_level', 'risk_level_encoded'])  
y = df['trust_score'] 

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 

# Correlation Analysis
plt.figure(figsize=(10, 8))
combined = pd.concat([X_train, y_train], axis=1) 
sns.heatmap(combined.corr(), annot=True, fmt='.2f', cmap='coolwarm') 
plt.title('Feature Correlation Matrix')
plt.show() 

# Standard Scaling
sc = StandardScaler() 
X_train = sc.fit_transform(X_train) 
X_test = sc.transform(X_test) 

# --- 6. Model Training (XGBoost) ---
print("\nStarting Model Training...")
model = XGBRegressor( 
    n_estimators=200, 
    learning_rate=0.05, 
    max_depth=6, 
    random_state=42 
) 

model.fit(X_train, y_train) 

# Predictions
y_pred = model.predict(X_test) 

# --- 7. Evaluation ---
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n--- Model Performance ---")
print(f"Mean Squared Error: {mse:.2f}") 
print(f"R2 Score (Variance Explained): {r2:.4f}")

# --- 8. Model Persistence ---
joblib.dump(model, 'model.pkl')
print("\nSuccess: Model stored as 'model.pkl'")
