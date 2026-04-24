"""
Day 20 - Time Series and Advanced Transformations
AI Server Log Monitoring System
"""

import pandas as pd


def main() -> None:
    # -----------------------------
    # Create dataset
    # -----------------------------
    data = {
        "timestamp": [
            "2026-04-01 10:00",
            "2026-04-01 11:00",
            "2026-04-02 12:00",
            "2026-04-03 13:00",
            "2026-04-04 14:00",
            "2026-04-05 15:00",
            "2026-04-06 16:00",
            "2026-04-07 17:00"
        ],
        "response_time": [
            320.5, 610.2, 450.0, 700.3,
            250.0, 800.0, 400.0, 550.0
        ]
    }

    df = pd.DataFrame(data)

    print("Original DataFrame:")
    print(df)

    # -----------------------------
    # Convert to datetime
    # -----------------------------
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    except Exception as e:
        print("Datetime conversion error:", e)

    print("\nAfter datetime conversion:")
    print(df)

    # -----------------------------
    # Create weekend flag
    # -----------------------------
    df["is_weekend"] = df["timestamp"].dt.dayofweek.apply(
        lambda x: x >= 5
    )

    print("\nWeekend Flag Added:")
    print(df)

    # -----------------------------
    # Status column using apply()
    # -----------------------------
    def latency_status(value: float) -> str:
        return "High Latency" if value > 500 else "Optimal"

    df["status"] = df["response_time"].apply(latency_status)

    print("\nStatus Column Added:")
    print(df)

    # -----------------------------
    # Resample (daily average response time)
    # -----------------------------
    df.set_index("timestamp", inplace=True)

    daily_avg = df["response_time"].resample("D").mean()

    print("\nDaily Average Response Time:")
    print(daily_avg)


if __name__ == "__main__":
    main()