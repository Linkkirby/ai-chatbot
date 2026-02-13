import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

def run_house_prediction():
    # 1. Load Dataset (Standard dataset similar to real estate data)
    data = fetch_california_housing()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['PRICE'] = data.target  # The target variable we want to predict
    
    print("--- Data Snapshot ---")
    print(df.head())

    # 2. Feature Selection (X) and Target (y)
    X = df.drop('PRICE', axis=1)
    y = df['PRICE']

    # 3. Split Data (80% for training, 20% for testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Train Model (Using Random Forest for better accuracy than simple Linear Regression)
    print("\nTraining the model... (this may take a moment)")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Make Predictions
    y_pred = model.predict(X_test)

    # 6. Evaluate
    score = r2_score(y_test, y_pred)
    print(f"\nModel Accuracy (R² Score): {score:.2f}")

    # Optional: Plot Actual vs Predicted prices
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.xlabel("Actual Prices")
    plt.ylabel("Predicted Prices")
    plt.title("Actual vs Predicted House Prices")
    plt.show()

if __name__ == "__main__":
    run_house_prediction()