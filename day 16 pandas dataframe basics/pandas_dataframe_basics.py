"""
Pandas DataFrame Basics - Employee Data Analysis
"""

import pandas as pd


def main() -> None:
    # Create data dictionary
    data = {
        "Name": ["Ahmet", "Can", "Derya", "Eren", "Fatma"],
        "Department": ["Accounting", "Software", "Software", "HR", "Accounting"],
        "Experience": [16, 2, 5, 8, 10],
        "Salary": [85000, 45000, 60000, 55000, 70000]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    print("Full DataFrame:")
    print(df)

    # First 3 rows
    print("\nFirst 3 rows:")
    print(df.head(3))

    # Filter Software department
    software_employees = df[df["Department"] == "Software"]

    print("\nSoftware Department Employees:")
    print(software_employees)

    # Statistics
    avg_salary = df["Salary"].mean()
    total_experience = df["Experience"].sum()

    print("\nStatistics:")
    print(f"Average Salary: {avg_salary}")
    print(f"Total Experience: {total_experience}")

    # Bonus: Sort by Experience (descending)
    sorted_df = df.sort_values(by="Experience", ascending=False)

    print("\nSorted by Experience (Descending):")
    print(sorted_df)


if __name__ == "__main__":
    main()