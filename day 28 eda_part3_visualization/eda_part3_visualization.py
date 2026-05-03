import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time


# -----------------------------
# TIMER DECORATOR
# -----------------------------
def time_logger(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print("\n[START] EDA Process")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[END] EDA Process | Duration: {end - start:.4f} seconds\n")
        return result
    return wrapper


# -----------------------------
# DATA GENERATION
# -----------------------------
np.random.seed(42)

df = pd.DataFrame({
    "Request_ID": range(1, 1001),
    "Employee_Level": np.random.choice(["Junior", "Mid", "Senior"], 1000),
    "Process_Time": np.random.normal(300, 80, 1000),
    "Cost": np.random.normal(1000, 250, 1000),
    "Error_Found": np.random.choice([True, False], 1000, p=[0.2, 0.8]),
    "Region": np.random.choice(["North America", "Europe", "Asia"], 1000)
})


# Introduce missing values (real-world noise)
df.loc[np.random.choice(df.index, 20), "Cost"] = np.nan


# -----------------------------
# EDA CLASS
# -----------------------------
class DataInvestigator:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    # -------------------------
    # PHASE 1: CLEANING
    # -------------------------
    def clean_data(self):
        print("Cleaning data...")

        # Missing values
        self.df["Cost"].fillna(self.df["Cost"].median(), inplace=True)

        # Remove negative values
        self.df = self.df[self.df["Cost"] > 0]
        self.df = self.df[self.df["Process_Time"] > 0]

    # -------------------------
    # PHASE 2: VISUALIZATION
    # -------------------------
    def visualize(self):
        print("Generating visualizations...")

        plt.figure(figsize=(15, 5))

        # Violin Plot
        plt.subplot(1, 3, 1)
        sns.violinplot(data=self.df, x="Employee_Level", y="Process_Time")
        plt.title("Process Time by Employee Level")

        # Heatmap
        plt.subplot(1, 3, 2)
        sns.heatmap(self.df[["Process_Time", "Cost"]].corr(),
                    annot=True, cmap="coolwarm")
        plt.title("Cost vs Process Time Correlation")

        # Error rate per region
        plt.subplot(1, 3, 3)
        sns.barplot(data=self.df, x="Region", y="Error_Found", estimator=np.mean)
        plt.title("Error Rate by Region")

        plt.tight_layout()
        plt.show()

    # -------------------------
    # PHASE 3: FEATURE ENGINEERING
    # -------------------------
    def feature_engineering(self):
        print("Creating features...")

        self.df["Cost_Efficiency"] = self.df["Cost"] / self.df["Process_Time"]

        region_dummies = pd.get_dummies(self.df["Region"], prefix="Region")
        self.df = pd.concat([self.df, region_dummies], axis=1)

    # -------------------------
    # PHASE 4: REPORT
    # -------------------------
    def summary_report(self):
        print("\n===== FINAL INSIGHTS REPORT =====")

        highest_error_region = (
            self.df.groupby("Region")["Error_Found"].mean().idxmax()
        )

        highest_cost_region = (
            self.df.groupby("Region")["Cost"].mean().idxmax()
        )

        fastest_level = (
            self.df.groupby("Employee_Level")["Process_Time"].mean().idxmin()
        )

        print(f"1. Region with highest error rate: {highest_error_region}")
        print(f"2. Region with highest cost: {highest_cost_region}")
        print(f"3. Fastest employee level: {fastest_level}")


# -----------------------------
# PIPELINE
# -----------------------------
@time_logger
def run_eda():
    investigator = DataInvestigator(df)

    print("Loading dataset...")
    print("Initial shape:", df.shape)

    investigator.clean_data()
    investigator.visualize()
    investigator.feature_engineering()
    investigator.summary_report()

    print("\nEDA completed successfully.")


# RUN
run_eda()