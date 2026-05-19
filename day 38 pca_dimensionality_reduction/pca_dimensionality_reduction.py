import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# -----------------------------
# LOGGING
# -----------------------------
def log(message: str):
    print(f"[LOG] {message}")


# -----------------------------
# DATA GENERATION
# -----------------------------
def create_dataset() -> pd.DataFrame:
    log("Generating dataset...")

    np.random.seed(42)

    data = {
        f"Ratio_{i}": np.random.rand(200) * (i + 1) * 10
        for i in range(1, 11)
    }

    return pd.DataFrame(data)


# -----------------------------
# PCA PROCESS
# -----------------------------
def apply_pca(df: pd.DataFrame):
    log("Standardizing data...")

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    log("Applying PCA...")

    pca = PCA(n_components=2)
    components = pca.fit_transform(scaled_data)

    pca_df = pd.DataFrame(
        components,
        columns=["PC1", "PC2"]
    )

    return pca_df, pca


# -----------------------------
# VISUALIZATION
# -----------------------------
def visualize(pca_df: pd.DataFrame):
    log("Plotting PCA result...")

    plt.figure(figsize=(8, 6))

    sns.scatterplot(
        data=pca_df,
        x="PC1",
        y="PC2"
    )

    plt.title("PCA - Dimensionality Reduction (2 Components)")
    plt.show()


# -----------------------------
# MAIN PIPELINE
# -----------------------------
if __name__ == "__main__":

    df = create_dataset()

    pca_df, pca_model = apply_pca(df)

    visualize(pca_df)

    variance_ratio = pca_model.explained_variance_ratio_
    total_variance = variance_ratio.sum() * 100

    print("\nExplained Variance Ratio:", variance_ratio)
    print(f"Total Variance Captured: {total_variance:.2f}%")

    print(
        f"\nReduced 10 features to 2 components while retaining "
        f"{total_variance:.2f}% of the original data variance."
    )