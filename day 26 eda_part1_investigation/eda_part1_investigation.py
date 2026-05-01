import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# -----------------------------
# DATA GENERATION
# -----------------------------
np.random.seed(42)

df = pd.DataFrame({
    "Invoice_ID": range(1, 501),
    "Vendor_Category": np.random.choice(
        ["IT Services", "Logistics", "Consulting", "Office Supplies"],
        500
    ),
    "Invoice_Amount": np.random.normal(1000, 300, 500),
    "Days_to_Pay": np.random.randint(1, 60, 500),
    "Approval_Status": np.random.choice(["Approved", "Pending", "Rejected"], 500)
})

# Introduce missing values (real-world EDA condition)
df.loc[np.random.choice(df.index, 30), "Invoice_Amount"] = np.nan
df.loc[np.random.choice(df.index, 20), "Days_to_Pay"] = np.nan


# -----------------------------
# DATA INVESTIGATOR CLASS
# -----------------------------
class DataInvestigator:
    def __init__(self, data: pd.DataFrame):
        self.df = data

    # -------------------------
    # SUMMARY STATISTICS
    # -------------------------
    def get_summary(self):
        print("\nDATA INFO:")
        print(self.df.info())

        print("\nDATA DESCRIPTION:")
        print(self.df.describe())

    # -------------------------
    # MISSING VALUE HEATMAP
    # -------------------------
    def check_missing(self):
        plt.figure(figsize=(8, 4))
        sns.heatmap(self.df.isnull(), cbar=False, cmap="viridis")
        plt.title("Missing Value Map")
        plt.show()

    # -------------------------
    # DISTRIBUTION PLOT
    # -------------------------
    def plot_distributions(self):
        plt.figure(figsize=(10, 5))
        sns.histplot(self.df["Invoice_Amount"], kde=True, bins=30)
        plt.title("Invoice Amount Distribution")
        plt.xlabel("Invoice Amount")
        plt.ylabel("Frequency")
        plt.show()

    # -------------------------
    # CATEGORY ANALYSIS
    # -------------------------
    def vendor_analysis(self):
        plt.figure(figsize=(10, 5))
        sns.boxplot(
            data=self.df,
            x="Vendor_Category",
            y="Invoice_Amount"
        )
        plt.title("Vendor Category vs Invoice Amount")
        plt.xticks(rotation=45)
        plt.show()


# -----------------------------
# RUN ANALYSIS
# -----------------------------
investigator = DataInvestigator(df)

investigator.get_summary()
investigator.check_missing()
investigator.plot_distributions()
investigator.vendor_analysis()