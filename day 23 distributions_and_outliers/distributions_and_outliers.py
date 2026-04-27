import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# -----------------------------
# OUTLIER DETECTION (IQR METHOD)
# -----------------------------
def detect_outliers_iqr(data: np.ndarray):
    """
    Detect outliers using the IQR (Interquartile Range) method.
    Returns a list of outlier values.
    """

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = data[(data < lower_bound) | (data > upper_bound)]

    return outliers


# -----------------------------
# DATA GENERATION
# -----------------------------
np.random.seed(42)

# Normal latency distribution (ms)
latency = np.random.normal(loc=200, scale=30, size=1000)

# Add artificial outliers
outliers = np.array([400, 420, 450, 500, 600, 700, 800])
latency = np.concatenate([latency, outliers])


# -----------------------------
# PLOTS (Histogram + Boxplot)
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogram with KDE
sns.histplot(latency, bins=30, kde=True, ax=axes[0])
axes[0].set_title("Latency Distribution (Histogram + KDE)")
axes[0].set_xlabel("Latency (ms)")

# Box plot
sns.boxplot(x=latency, ax=axes[1])
axes[1].set_title("Latency Outliers (Box Plot)")
axes[1].set_xlabel("Latency (ms)")

plt.tight_layout()
plt.show()


# -----------------------------
# OUTLIER DETECTION OUTPUT
# -----------------------------
detected_outliers = detect_outliers_iqr(latency)

print("\nDetected Outliers (IQR Method):")
print(detected_outliers)