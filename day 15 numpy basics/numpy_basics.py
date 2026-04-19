"""
NumPy Basics - Data Analysis on AI Predictions
"""

import numpy as np


def main() -> None:
    # 1️⃣ Create random predictions (100 values between 0 and 1)
    predictions: np.ndarray = np.random.rand(100)

    print("Predictions:")
    print(predictions)

    # 2️⃣ Statistical calculations
    mean_value: float = np.mean(predictions)
    std_dev: float = np.std(predictions)
    variance: float = np.var(predictions)

    print("\nStatistics:")
    print(f"Mean: {mean_value}")
    print(f"Standard Deviation: {std_dev}")
    print(f"Variance: {variance}")

    # 3️⃣ Vectorized operation (no loops)
    scaled_predictions: np.ndarray = (predictions * 100).astype(int)

    print("\nScaled Predictions (0-100):")
    print(scaled_predictions)

    # 4️⃣ Filtering using boolean indexing
    filtered_predictions: np.ndarray = scaled_predictions[scaled_predictions > 50]

    print("\nFiltered Predictions (>50):")
    print(filtered_predictions)

    # 5️⃣ Reshape to 10x10 matrix (Bonus)
    matrix: np.ndarray = predictions.reshape(10, 10)

    print("\n10x10 Matrix:")
    print(matrix)


if __name__ == "__main__":
    main()