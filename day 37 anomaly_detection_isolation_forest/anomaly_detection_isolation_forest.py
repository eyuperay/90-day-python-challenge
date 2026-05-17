import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# LOGGING FUNCTION
# -----------------------------
def log(message: str):
    print(f"[LOG] {message}")


# -----------------------------
# DATA GENERATION
# -----------------------------
def create_dataset() -> pd.DataFrame:
    log("Generating dataset...")

    # Normal transactions
    normal = pd.DataFrame({
        "Amount": np.random.randint(20, 150, 500),
        "Days_Since_Last": np.random.randint(1, 6, 500)
    })

    # Anomalies
    anomaly = pd.DataFrame({
        "Amount": np.random.randint(1500, 3000, 10),
        "Days_Since_Last": np.random.randint(20, 31, 10)
    })

    df = pd.concat([normal, anomaly], ignore_index=True)

    return df


# -----------------------------
# MODEL TRAINING
# -----------------------------
def train_model(df: pd.DataFrame):
    log("Training Isolation Forest model...")

    model = IsolationForest(
        contamination=0.02,
        random_state=42
    )

    features = df[["Amount", "Days_Since_Last"]]
    model.fit(features)

    return model


# -----------------------------
# APPLY MODEL SAFELY
# -----------------------------
def flag_high_risk_transactions(df: pd.DataFrame, model) -> pd.DataFrame:
    log("Applying anomaly detection...")

    df = df.copy()

    # IMPORTANT: use only training features
    features = df[["Amount", "Days_Since_Last"]]

    df["Prediction"] = model.predict(features)
    df["Anomaly_Score"] = model.decision_function(features)
    df["Is_Suspicious"] = df["Prediction"] == -1

    return df


# -----------------------------
# VISUALIZATION
# -----------------------------
def visualize(df: pd.DataFrame):
    log("Plotting results...")

    plt.figure(figsize=(10, 5))

    sns.scatterplot(
        data=df,
        x="Amount",
        y="Days_Since_Last",
        hue="Is_Suspicious"
    )

    plt.title("Isolation Forest - Suspicious Transaction Detection")
    plt.show()


# -----------------------------
# MAIN PIPELINE
# -----------------------------
if __name__ == "__main__":

    df = create_dataset()

    model = train_model(df)

    result_df = flag_high_risk_transactions(df, model)

    print(result_df.head())

    visualize(result_df)