import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# -----------------------------
# DATA GENERATION
# -----------------------------
np.random.seed(42)

df = pd.DataFrame({
    "Invoice_Frequency": np.random.randint(1, 20, 300),
    "Average_Value": np.random.randint(100, 5000, 300)
})

print("Sample Data:")
print(df.head())


# -----------------------------
# FEATURE SCALING
# -----------------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)


# -----------------------------
# ELBOW METHOD FUNCTION
# -----------------------------
def find_optimal_k(data):
    inertia_values = []

    for k in range(1, 11):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(data)
        inertia_values.append(model.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 11), inertia_values, marker="o")
    plt.title("Elbow Method - Optimal K Selection")
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Inertia")
    plt.show()


# Run elbow method
find_optimal_k(scaled_data)


# -----------------------------
# FINAL MODEL (K = 3)
# -----------------------------
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(scaled_data)

centers = kmeans.cluster_centers_


# -----------------------------
# VISUALIZATION
# -----------------------------
plt.figure(figsize=(8, 6))

sns.scatterplot(
    x=df["Invoice_Frequency"],
    y=df["Average_Value"],
    hue=df["Cluster"],
    palette="Set2"
)

# Convert cluster centers back to original scale
centers_original = scaler.inverse_transform(centers)

plt.scatter(
    centers_original[:, 0],
    centers_original[:, 1],
    s=200,
    c="black",
    marker="X",
    label="Centroids"
)

plt.title("Vendor Segmentation (K-Means Clustering)")
plt.xlabel("Invoice Frequency")
plt.ylabel("Average Invoice Value")
plt.legend()
plt.show()