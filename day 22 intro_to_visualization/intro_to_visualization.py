import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def plot_performance_comparison(epochs, model_a, model_b):
    """
    Plots training accuracy comparison between two models.
    """

    plt.figure(figsize=(10, 5))

    plt.plot(epochs, model_a, marker="o", label="Model A")
    plt.plot(epochs, model_b, marker="o", label="Model B")

    plt.title("Model Training Progress")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")

    plt.legend()
    plt.grid(True)

    plt.show()


def seaborn_scatter_plot():
    """
    Creates a Seaborn scatter plot using tips dataset.
    """

    sns.set_style("whitegrid")

    data = sns.load_dataset("tips")

    plt.figure(figsize=(10, 5))

    sns.scatterplot(
        data=data,
        x="total_bill",
        y="tip",
        hue="day",
        palette="viridis"
    )

    plt.title("Total Bill vs Tip Relationship")

    plt.show()


if __name__ == "__main__":

    # -----------------------------
    # Matplotlib Data
    # -----------------------------
    epochs = np.arange(1, 11)

    model_a_accuracy = np.array([0.55, 0.60, 0.65, 0.70, 0.72, 0.75, 0.78, 0.80, 0.82, 0.85])
    model_b_accuracy = np.array([0.50, 0.58, 0.63, 0.67, 0.71, 0.74, 0.77, 0.79, 0.83, 0.88])

    plot_performance_comparison(epochs, model_a_accuracy, model_b_accuracy)

    # -----------------------------
    # Seaborn Plot
    # -----------------------------
    seaborn_scatter_plot()