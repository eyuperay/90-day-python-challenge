import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# -----------------------------
# DATA GENERATION
# -----------------------------
np.random.seed(42)

df = pd.DataFrame({
    "Amount": np.random.uniform(100, 10000, 500),
    "Vendor_Age": np.random.randint(1, 30, 500),
    "Country_Risk_Score": np.random.uniform(0, 1, 500),
    "Time_of_Day": np.random.randint(0, 24, 500),
    "User_History_Score": np.random.uniform(0, 100, 500),
    "Is_Manual_Entry": np.random.randint(0, 2, 500)
})

# Target variable (synthetic fraud logic)
df["Fraud"] = (
    (df["Amount"] > 8000) |
    (df["Country_Risk_Score"] > 0.7) |
    (df["Is_Manual_Entry"] == 1)
).astype(int)


# -----------------------------
# FEATURES / TARGET
# -----------------------------
X = df.drop("Fraud", axis=1)
y = df["Fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -----------------------------
# DECISION TREE (BASELINE)
# -----------------------------
tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)
tree_model.fit(X_train, y_train)
tree_pred = tree_model.predict(X_test)
tree_acc = accuracy_score(y_test, tree_pred)


# -----------------------------
# RANDOM FOREST MODEL
# -----------------------------
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)


# -----------------------------
# RESULTS
# -----------------------------
print("\nMODEL COMPARISON:")
print(f"Decision Tree Accuracy: {tree_acc:.4f}")
print(f"Random Forest Accuracy: {rf_acc:.4f}")


# -----------------------------
# FEATURE IMPORTANCE
# -----------------------------
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf_model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:")
print(feature_importance)


# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(10, 5))
sns.barplot(data=feature_importance, x="Importance", y="Feature")
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.show()