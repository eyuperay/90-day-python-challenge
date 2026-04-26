import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw transaction dataset.
    """

    # Remove duplicates
    df = df.drop_duplicates(subset="transaction_id")

    # Convert date
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    # Fill missing amounts with department median
    df["amount"] = df.groupby("department_id")["amount"].transform(
        lambda x: x.fillna(x.median())
    )

    return df


def merge_with_departments(
    transactions: pd.DataFrame,
    departments: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge transactions with department metadata using left join.
    """

    return transactions.merge(departments, on="department_id", how="left")


def add_budget_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mark departments as Over Budget if spending exceeds limit.
    """

    total_spending = df.groupby("department_id")["amount"].sum().to_dict()

    df["budget_status"] = df["department_id"].apply(
        lambda x: "Over Budget" if total_spending.get(x, 0) > df.loc[df["department_id"] == x, "budget_limit"].iloc[0]
        else "Within Budget"
    )

    return df


def add_rolling_average(df: pd.DataFrame) -> pd.DataFrame:
    """
    7-day rolling average of transaction amounts.
    """

    df = df.sort_values("transaction_date")

    df["rolling_avg_7d"] = df["amount"].rolling(window=7).mean()

    return df