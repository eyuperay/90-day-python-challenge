import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# -----------------------------
# BASE DIRECTORY (IMPORTANT FIX)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent


# -----------------------------
# CREATE DATASET
# -----------------------------
np.random.seed(42)

df = pd.DataFrame({
    "Processing_Time": np.random.normal(200, 50, 100),
    "Error_Rate": np.random.uniform(0, 10, 100),
    "Token_Usage": np.random.normal(1000, 200, 100),
    "Cost": np.random.normal(50, 10, 100),
    "Success_Rate": np.random.uniform(80, 100, 100),
    "Model_Type": np.random.choice(["GPT", "Claude", "Llama"], 100)
})


# -----------------------------
# CORRELATION MATRIX
# -----------------------------
corr_matrix = df[[
    "Processing_Time",
    "Error_Rate",
    "Token_Usage",
    "Cost",
    "Success_Rate"
]].corr()


# -----------------------------
# SAVE OUTPUT (FIXED PATH)
# -----------------------------
output_file = BASE_DIR / "correlation_matrix.csv"
corr_matrix.to_csv(output_file)


# -----------------------------
# PLOT SETUP
# -----------------------------
plt.figure(figsize=(14, 5))


# -----------------------------
# HEATMAP
# -----------------------------
plt.subplot(1, 2, 1)
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")


# -----------------------------
# BAR PLOT (ERROR RATE BY MODEL)
# -----------------------------
plt.subplot(1, 2, 2)
sns.barplot(
    data=df,
    x="Model_Type",
    y="Error_Rate",
    estimator=np.mean,
    errorbar=None
)

plt.title("Average Error Rate by Model Type")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()