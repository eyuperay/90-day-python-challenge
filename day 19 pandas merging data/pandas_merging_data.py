"""
Pandas Merging, Joining, and Concatenation - User Activity Analysis
"""

import pandas as pd


def main() -> None:
    # -----------------------------
    # DataFrame A: Users
    # -----------------------------
    users = pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5],
        "name": ["John", "Michael", "Sarah", "Emma", "David"],
        "email": [
            "john@mail.com",
            "michael@mail.com",
            "sarah@mail.com",
            "emma@mail.com",
            "david@mail.com"
        ]
    })

    print("Users DataFrame:")
    print(users)

    # -----------------------------
    # DataFrame B: Activity
    # (Note: user_id = 6 does NOT exist in users → to test join behavior)
    # -----------------------------
    activity = pd.DataFrame({
        "user_id": [1, 2, 2, 3, 6],
        "last_login": [
            "2024-01-10",
            "2024-01-12",
            "2024-01-15",
            "2024-01-20",
            "2024-01-22"
        ],
        "total_spend": [120, 250, 300, 180, 500]
    })

    print("\nActivity DataFrame:")
    print(activity)

    # -----------------------------
    # INNER JOIN
    # Only matching users in both tables
    # -----------------------------
    inner_merge = pd.merge(users, activity, on="user_id", how="inner")

    print("\nInner Join Result (Active Users Only):")
    print(inner_merge)

    # -----------------------------
    # LEFT JOIN
    # All users + activity if exists
    # -----------------------------
    left_merge = pd.merge(users, activity, on="user_id", how="left")

    print("\nLeft Join Result (All Users):")
    print(left_merge)

    # -----------------------------
    # CONCATENATION
    # New users added to original dataset
    # -----------------------------
    new_users = pd.DataFrame({
        "user_id": [6, 7],
        "name": ["Alice", "Robert"],
        "email": ["alice@mail.com", "robert@mail.com"]
    })

    combined_users = pd.concat([users, new_users], ignore_index=True)

    print("\nConcatenated Users DataFrame:")
    print(combined_users)


if __name__ == "__main__":
    main()