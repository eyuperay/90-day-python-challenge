"""
DAY 34 - Decision Tree: Vendor Risk Assessment

Scenario:
Predict whether a vendor is HIGH RISK using interpretable AI.

Goal:
Understand decision paths, feature importance, and tree visualization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree


# -----------------------------
# DATA GENERATION
# -----------------------------
def generate_data(n_samples: int = 300) -> pd.DataFrame:
    np.random.seed(42)

    years_in_business = np.random.randint(1, 30, n_samples)
    late_payments = np.random.randint(0, 10, n_samples)
    contract_value = np.random.uniform(1000, 100000, n_samples)

    # Risk logic (hidden rule)
    risk_score = (
        (late_payments * 2)
        - (years_in_business * 0.3)
        + (contract_value / 50000)
    )

    high_risk = (risk_score > 3).astype(int)

    return pd.DataFrame({
        "Years_in_Business": years_in_business,
        "Late_Payments": late_payments,
        "Contract_Value": contract_value,
        "High_Risk": high_risk
    })


# -----------------------------
# TREE PREDICTION PATH FUNCTION
# -----------------------------
def explain_decision(model, feature_names, sample):
    node = 0

    tree = model.tree_

    print("\nDecision Path Explanation:")

    while tree.children_left[node] != tree.children_right[node]:

        feature = tree.feature[node]
        threshold = tree.threshold[node]

        feature_name = feature_names[feature]
        value = sample[feature]

        print(f"IF {feature_name} <= {threshold:.2f} (value={value:.2f})")

        if value <= threshold:
            node = tree.children_left[node]
        else:
            node = tree.children_right[node]


    print("→ FINAL DECISION (Leaf Node)")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main() -> None:
    print("Generating dataset...")
    df = generate_data()

    X = df[["Years_in_Business", "Late_Payments", "Contract_Value"]]
    y = df["High_Risk"]

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training Decision Tree (max_depth=3)...")
    model = DecisionTreeClassifier(max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    # -----------------------------
    # TREE VISUALIZATION
    # -----------------------------
    print("Visualizing Decision Tree...")

    plt.figure(figsize=(14, 8))
    plot_tree(
        model,
        feature_names=X.columns,
        class_names=["Low Risk", "High Risk"],
        filled=True
    )
    plt.title("Vendor Risk Decision Tree")
    plt.show()

    # -----------------------------
    # FEATURE IMPORTANCE
    # -----------------------------
    print("\nFeature Importance:")
    for name, importance in zip(X.columns, model.feature_importances_):
        print(f"{name}: {importance:.4f}")

    # -----------------------------
    # EXPLAIN SINGLE PREDICTION
    # -----------------------------
    sample = X_test.iloc[0].values
    prediction = model.predict([sample])[0]

    print("\nSample Prediction:", prediction)
    explain_decision(model, X.columns.tolist(), sample)


if __name__ == "__main__":
    main()