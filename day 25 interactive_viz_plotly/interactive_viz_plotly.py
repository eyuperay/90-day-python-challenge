import pandas as pd
import numpy as np
import plotly.express as px


# -----------------------------
# DATA GENERATION
# -----------------------------
np.random.seed(42)

regions = ["North", "South", "East", "West"]

df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=200),
    "Amount": np.random.normal(1000, 300, 200).round(2),
    "Region": np.random.choice(regions, 200),
    "Transaction_Fee": np.random.normal(25, 5, 200).round(2),
})

df["Month"] = df["Date"].dt.month.astype(str)


# -----------------------------
# LABELS
# -----------------------------
labels = {
    "Amount": "Transaction Amount (USD)",
    "Transaction_Fee": "Transaction Fee (USD)",
    "Region": "Region",
    "Date": "Date"
}


# -----------------------------
# INTERACTIVE SCATTER PLOT
# -----------------------------
scatter_fig = px.scatter(
    df,
    x="Amount",
    y="Transaction_Fee",
    color="Region",
    hover_data=["Date"],
    title="Transaction Fee vs Amount Analysis",
    labels=labels
)

scatter_fig.write_html("transaction_report.html")
scatter_fig.show()


# -----------------------------
# INTERACTIVE BAR CHART
# -----------------------------
region_summary = df.groupby("Region")["Amount"].sum().reset_index()

bar_fig = px.bar(
    region_summary,
    x="Region",
    y="Amount",
    color="Region",
    title="Total Transaction Amount by Region",
    labels=labels
)

bar_fig.show()