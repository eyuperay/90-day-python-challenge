"""
DAY 31 - Introduction to Machine Learning (Scikit-Learn)

Scenario:
Predict Required Hours based on Project Complexity using Linear Regression.

Goal:
Learn the sklearn workflow: Instantiate → Fit → Predict
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def generate_data(n_samples: int = 100) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates synthetic linear data.

    y = 5x + noise
    """
    np.random.seed(42)

    X = np.random.uniform(1, 10, n_samples).reshape(-1, 1)
    noise = np.random.normal(0, 2, n_samples)
    y = 5 * X.flatten() + noise

    return X, y


def train_model(X: np.ndarray, y: np.ndarray) -> LinearRegression:
    """
    Trains Linear Regression model.
    """
    model = LinearRegression()
    model.fit(X, y)
    return model


def main() -> None:
    print("Generating data...")

    X, y = generate_data()

    print("Splitting data (80% train / 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training Linear Regression model...")
    model = train_model(X_train, y_train)

    print("\nModel Parameters:")
    print(f"Coefficient (Slope): {model.coef_[0]:.4f}")
    print(f"Intercept: {model.intercept_:.4f}")

    print("\nMaking prediction for Project Complexity = 8.5...")
    prediction = model.predict([[8.5]])

    print(f"Predicted Required Hours: {prediction[0]:.2f}")


if __name__ == "__main__":
    main()