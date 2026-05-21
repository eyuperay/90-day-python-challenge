import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# -----------------------------
# LOGGING
# -----------------------------
def log(message: str):
    print(f"[LOG] {message}")


# -----------------------------
# DATA GENERATION
# (Reused fraud-style dataset)
# -----------------------------
def create_dataset():
    log("Generating dataset...")

    np.random.seed(42)

    df = pd.DataFrame({
        "Amount": np.random.randint(100, 10000, 500),
        "Seniority": np.random.randint(1, 11, 500),
        "Frequency": np.random.randint(1, 20, 500),
        "Risk_Score": np.random.rand(500) * 100
    })

    # synthetic target (fraud logic)
    df["Fraud"] = (
        (df["Amount"] > 7000) |
        (df["Risk_Score"] > 80) |
        (df["Seniority"] < 3)
    ).astype(int)

    return df


# -----------------------------
# MODEL TUNING
# -----------------------------
def tune_model(X_train, y_train):

    log("Starting GridSearchCV...")

    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5]
    }

    model = RandomForestClassifier(random_state=42)

    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        scoring="accuracy"
    )

    grid_search.fit(X_train, y_train)

    print("\nBest Parameters:", grid_search.best_params_)
    print("Best Cross-Validation Score:", grid_search.best_score_)

    return grid_search.best_estimator_


# -----------------------------
# MAIN PIPELINE
# -----------------------------
if __name__ == "__main__":

    df = create_dataset()

    features = ["Amount", "Seniority", "Frequency", "Risk_Score"]
    X = df[features]
    y = df["Fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    best_model = tune_model(X_train, y_train)

    log("Evaluating best model on test set...")

    y_pred = best_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\nFinal Test Accuracy:", accuracy)