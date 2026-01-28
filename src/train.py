import pandas as pd
import numpy as np
import joblib
import optuna
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score
import os

# --- 1. Data Ingestion & Engineering ---
def load_and_preprocess(path):
    df = pd.read_csv(path)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    df = df.dropna()
    
    # Feature Engineering: Creating 'Lag' features if time-series data exists
    # In production, you'd pull this from a Feature Store or SQL DB
    return df

# --- 2. Objective Function for Hyperparameter Tuning ---
def objective(trial, X_train, y_train):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
    }
    
    model = XGBRegressor(**params, random_state=42)
    model.fit(X_train, y_train)
    return mean_absolute_error(y_train, model.predict(X_train))

# --- 3. Full Training Workflow ---
def train_model():
    data = load_and_preprocess(r"F:\Downloads\AQI-and-Lat-Long-of-Countries.csv")
    
    # Define features
    features = ['co_aqi_value', 'ozone_aqi_value', 'no2_aqi_value', 'pm2.5_aqi_value']
    target = 'aqi_value'
    
    X = data[features]
    y = data[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Optimization Step
    study = optuna.create_study(direction='minimize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=20)
    
    # Build Pipeline with Best Params
    preprocessor = ColumnTransformer(
        transformers=[('num', RobustScaler(), features)]
    )
    
    final_model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', XGBRegressor(**study.best_params))
    ])
    
    final_model.fit(X_train, y_train)
    
    # Metrics
    preds = final_model.predict(X_test)
    print(f"Final Model MAE: {mean_absolute_error(y_test, preds):.4f}")
    print(f"R2 Score: {r2_score(y_test, preds):.4f}")
    
    # Save Artifact in the root directory
    model_path = os.path.join(os.path.dirname(__file__), '..', 'aqi_pipeline_v1.pkl')
    joblib.dump(final_model, model_path)
    print(f"Model saved as {model_path}")

if __name__ == "__main__":
    train_model()


#pip install -r requirements.txt
#python src/train.py
#uvicorn src.main:app --reload
#http://127.0.0.1:8000
#Model is Correct now it's time to see the Dataset and 
#Build a best UI in fast api according to project, dataset and model