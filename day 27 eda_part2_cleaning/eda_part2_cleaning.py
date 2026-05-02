import pandas as pd
import numpy as np


# -----------------------------
# DATA CREATION
# -----------------------------
np.random.seed(42)

df = pd.DataFrame({
    "Transaction_ID": range(1, 101),
    "Amount": np.random.uniform(100, 10000, 100),
    "Category": np.random.choice(["Travel", "Tech", "Legal", "Rent"], 100),
    "Days_Since_Last_Audit": np.random.randint(1, 365, 100)
})


# -----------------------------
# FEATURE ENGINEERING FUNCTION
# -----------------------------
def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies feature engineering steps to improve model readiness.

    Risk_Score logic:
    Combines:
    - Log-transformed transaction amount (reduces impact of outliers)
    - Days since last audit (higher = higher risk)

    Formula:
    Risk_Score = (0.7 * Log_Amount) + (0.3 * Days_Since_Last_Audit_normalized)

    Returns:
        Transformed pandas DataFrame
    """

    df = df.copy()

    # -------------------------
    # TRANSFORMATION 1: LOG SCALE
    # -------------------------
    df["Log_Amount"] = np.log1p(df["Amount"])

    # -------------------------
    # TRANSFORMATION 2: BINNING
    # -------------------------
    df["Audit_Urgency"] = pd.cut(
        df["Days_Since_Last_Audit"],
        bins=[0, 90, 180, 365],
        labels=["Low", "Medium", "High"]
    )

    # -------------------------
    # TRANSFORMATION 3: ONE-HOT ENCODING
    # -------------------------
    category_dummies = pd.get_dummies(df["Category"], prefix="Category")
    df = pd.concat([df, category_dummies], axis=1)

    # -------------------------
    # TRANSFORMATION 4: DERIVED FEATURE (RISK SCORE)
    # -------------------------
    max_days = df["Days_Since_Last_Audit"].max()
    min_days = df["Days_Since_Last_Audit"].min()

    # Normalize Days_Since_Last_Audit
    df["Days_Normalized"] = (
        (df["Days_Since_Last_Audit"] - min_days) /
        (max_days - min_days)
    )

    df["Risk_Score"] = (
        0.7 * df["Log_Amount"] +
        0.3 * df["Days_Normalized"]
    )

    return df


# -----------------------------
# RUN PIPELINE
# -----------------------------
transformed_df = apply_feature_engineering(df)

print("Original Data:")
print(df.head())

print("\nTransformed Data:")
print(transformed_df.head())