"""
DAY 33 - Confusion Matrix & Error Analysis

Scenario:
Evaluate a Treasury Approval model and calculate business cost of errors.

Goal:
Understand FP / FN impact and visualize Confusion Matrix.
"""

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# -----------------------------
# DATA GENERATION
# -----------------------------
def generate_data(n_samples: int = 200) -> pd.DataFrame:
    np.random.seed(42)

    amount = np.random.uniform(100, 10000, n_samples)
    seniority = np.random.randint(1, 11, n_samples)

    prob = (seniority / 10) - (amount / 20000)
    noise = np.random.normal(0, 0.1, n_samples)

    approved = ((prob + noise) > 0.3).astype(int)

    return pd.DataFrame({
        "Amount": amount,
        "Seniority": seniority,
        "Approved": approved
    })


# -----------------------------
# MODEL TRAINING
# -----------------------------
def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main() -> None:
    print("Generating dataset...")
    df = generate_data()

    X = df[["Amount", "Seniority"]]
    y = df["Approved"]

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Scaling data...")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print("Training model...")
    model = train_model(X_train, y_train)

    print("Generating predictions...")
    y_pred = model.predict(X_test)

    # -----------------------------
    # CONFUSION MATRIX
    # -----------------------------
    cm = confusion_matrix(y_test, y_pred)

    tn, fp, fn, tp = cm.ravel()

    print("\nConfusion Matrix:")
    print(cm)

    print("\nPlotting Confusion Matrix...")
    ConfusionMatrixDisplay(confusion_matrix=cm).plot()

    # -----------------------------
    # BUSINESS COST CALCULATION
    # -----------------------------
    fp_cost = fp * 50
    fn_cost = fn * 500
    total_cost = fp_cost + fn_cost

    print("\nBusiness Impact Analysis:")
    print(f"False Positives (FP): {fp} → Cost: ${fp_cost}")
    print(f"False Negatives (FN): {fn} → Cost: ${fn_cost}")
    print(f"Total Operational Cost: ${total_cost}")

    print(
        f"\nOur model missed {fn} fraud cases, "
        f"resulting in a potential loss of ${fn_cost}."
    )


if __name__ == "__main__":
    main()