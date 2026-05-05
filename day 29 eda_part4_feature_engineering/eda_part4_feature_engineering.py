import pandas as pd
import numpy as np
from shared_tools import timer, log_step


@timer
def feature_engineering() -> pd.DataFrame:
    log_step("Creating dataset...")

    df = pd.DataFrame({
        "Transaction_ID": range(1, 11),
        "Amount": np.random.randint(100, 5000, 10),
        "Category": ["Travel", "Tech", "Legal", "Rent", "Travel",
                     "Tech", "Legal", "Rent", "Travel", "Tech"],
        "Days_Since_Last_Audit": np.random.randint(1, 300, 10)
    })

    log_step("Applying log transformation...")
    df["Log_Amount"] = np.log(df["Amount"])

    log_step("Creating bins...")
    df["Audit_Urgency"] = pd.cut(
        df["Days_Since_Last_Audit"],
        bins=[0, 90, 180, 999],
        labels=["Low", "Medium", "High"]
    )

    log_step("One-hot encoding...")
    df = pd.get_dummies(df, columns=["Category"])

    log_step("Creating Risk Score...")
    df["Risk_Score"] = (
        df["Log_Amount"] * 0.6 +
        df["Days_Since_Last_Audit"] * 0.4
    )

    log_step("Feature engineering completed.")

    return df


if __name__ == "__main__":
    result = feature_engineering()
    print(result)