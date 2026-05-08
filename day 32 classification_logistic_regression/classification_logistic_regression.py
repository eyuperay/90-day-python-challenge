"""
DAY 32 - Classification with Logistic Regression

Scenario:
Predict whether a transaction will be APPROVED (1) or DENIED (0)
based on Amount and User Seniority.

Goal:
Learn classification workflow + evaluation metrics
"""

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


def generate_data(n_samples: int = 200) -> pd.DataFrame:
    """
    Generate synthetic classification dataset.

    Logic:
    - Higher seniority → more approval
    - Higher amount → less approval
    """
    np.random.seed(42)

    amount = np.random.uniform(100, 10000, n_samples)
    seniority = np.random.randint(1, 11, n_samples)

    # Probability logic
    prob = (seniority / 10) - (amount / 20000)

    # Convert to binary (Approved: 1 / Denied: 0)
    approved = (prob > 0.3).astype(int)

    df = pd.DataFrame({
        "Amount": amount,
        "Seniority": seniority,
        "Approved": approved
    })

    return df


def main() -> None:
    print("Generating dataset...")

    df = generate_data()

    X = df[["Amount", "Seniority"]]
    y = df["Approved"]

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    print("Making predictions...")
    y_pred = model.predict(X_test_scaled)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()