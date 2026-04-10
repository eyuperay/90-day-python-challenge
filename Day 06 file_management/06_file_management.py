"""
Day 06: File Management

This script demonstrates:
- Creating and reading text files
- Saving data in JSON format
- Working with CSV files
- Handling errors with try-except blocks

For detailed explanations, please refer to the README file.
"""

import os
import json
import csv

# Script'in bulunduğu klasörü al
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_raw_data_file():
    """Create raw_data.txt only if it does not exist."""
    file_path = os.path.join(BASE_DIR, "raw_data.txt")

    if not os.path.exists(file_path):
        try:
            with open(file_path, "w") as file:
                file.write("Alice,25\nBob,30\nCharlie,22\nDiana,28\n")
            print("raw_data.txt created.")
        except Exception as e:
            print(f"Error creating raw_data.txt: {e}")
    else:
        print("raw_data.txt already exists.")


def read_raw_data():
    """Read raw_data.txt and return structured data."""
    file_path = os.path.join(BASE_DIR, "raw_data.txt")
    data = []

    try:
        with open(file_path, "r") as file:
            for line in file:
                name, age = line.strip().split(",")
                data.append({"name": name, "age": int(age)})
    except FileNotFoundError:
        print("raw_data.txt not found.")
    except Exception as e:
        print(f"Error reading raw_data.txt: {e}")

    return data


def save_to_json(data):
    """Save data.json only if it does not exist."""
    file_path = os.path.join(BASE_DIR, "data.json")

    if not os.path.exists(file_path):
        try:
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print("data.json created.")
        except Exception as e:
            print(f"Error writing data.json: {e}")
    else:
        print("data.json already exists.")


def create_students_csv():
    """Create students.csv only if it does not exist."""
    file_path = os.path.join(BASE_DIR, "students.csv")

    if not os.path.exists(file_path):
        try:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Grade"])
                writer.writerow(["Alice", 85])
                writer.writerow(["Bob", 60])
                writer.writerow(["Charlie", 90])
                writer.writerow(["Diana", 72])
            print("students.csv created.")
        except Exception as e:
            print(f"Error creating students.csv: {e}")
    else:
        print("students.csv already exists.")


def filter_passed_students():
    """Create passed_students.csv from students.csv (only if not exists)."""
    input_path = os.path.join(BASE_DIR, "students.csv")
    output_path = os.path.join(BASE_DIR, "passed_students.csv")

    if os.path.exists(output_path):
        print("passed_students.csv already exists.")
        return

    try:
        passed_students = []

        with open(input_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["Grade"]) > 70:
                    passed_students.append(row)

        with open(output_path, "w", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=["Name", "Grade"])
            writer.writeheader()
            writer.writerows(passed_students)

        print("passed_students.csv created.")

    except FileNotFoundError:
        print("students.csv not found.")
    except Exception as e:
        print(f"Error processing CSV: {e}")


if __name__ == "__main__":
    create_raw_data_file()
    data = read_raw_data()
    save_to_json(data)
    create_students_csv()
    filter_passed_students()