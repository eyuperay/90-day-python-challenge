# 90-Day Python Challenge

This repository contains my daily Python learning journey.  
The goal of this challenge is to build a strong foundation in Python programming through hands-on exercises covering variables, data types, lists, dictionaries, loops, functions, and more.

---

## Day 01
**Project:** 01_variable_types.py  
**Description:**  
Collected user personal information (first name, last name, birth year, height) and calculated age dynamically using the `datetime` module.  
Displayed a polished message using f-strings and used type hints for clarity.

---

## Day 02
**Project:** 02_data_structures.py  
**Description:**  
Created a product inventory list and managed it using list operations.  
Removed and added products, sliced the list to get popular products.  
Stored stock information in a dictionary and calculated total stock using a loop.  
Applied list comprehension to filter products with names longer than 5 characters.

## Day 03
**Project:** 03_control_flow_break.py  
**Description:**  
Analyzed a list of customer transactions using control flow statements.  
Skipped invalid transactions (zero or negative values) using `continue`.  
Stopped execution early when a suspicious transaction (999.99) was detected using `break`.  
Identified premium transactions (amount > 1000) before termination.  
Calculated total and average of processed transactions only.

## Day 03
**Project:** 03_control_flow_continue.py  
**Description:**  
Analyzed a list of customer transactions using control flow statements.  
Skipped invalid transactions (zero or negative values) using `continue`.  
Detected suspicious transactions (999.99) and logged them without stopping execution.  
Identified premium transactions (amount > 1000) and stored them in a list.  
Calculated total and average of all valid transactions.

## Day 04
**Project:** 04_functions_and_scope.py  
**Description:**

The goal of this task is to implement basic Python functions and understand variable scope.

####  Requirements

- `clean_text(text: str) -> str`  
  Write a function that takes a string, removes leading and trailing whitespace, and converts all characters to lowercase.

- `calculate_tax(price: float, tax_rate: float = 0.18) -> float`  
  Write a function that takes a price and a tax rate, and returns the total price including tax.  
  If no tax rate is provided, use a default value of `0.18`.

- `is_outlier(value: float, threshold: float = 100.0) -> bool`  
  Write a function that takes a numeric value and returns `True` if it exceeds the given threshold.

#### Scope Experiment

- Define a global variable named `global_counter` outside of any function.
- Inside a function, print this variable without modifying it.
- Create a local variable inside the function.
- Explain (using comments) why this local variable causes an error when accessed outside the function.

#### Clean Code

- Add a short docstring to each function explaining its purpose.

## Day 05
**Projects:** 05_error_handling_and_modules.py, utils.py  
**Description:**

The goal of this task is to implement basic error handling in Python and understand modular programming.

#### Requirements

- `safe_divide(a: float, b: float) -> float`  
  Write a function that performs division.  
  If `b` is zero, handle the error and return `0.0` with a warning message.

- `validate_age(age: int) -> bool`  
  Write a function that checks if the age is valid.  
  If the age is less than 0, raise a `ValueError`.

#### Main Program

- Import functions from `utils.py`.
- Take two numbers from the user and safely divide them.
- Take an age input from the user.
- Use a `try-except` block to handle possible errors during validation.

#### Clean Code

- Add a short docstring to each function explaining its purpose.
- Use clear and readable structure in the main script.

## Day 06

Project: 06_file_management.py
Description:

The goal of this task is to practice file handling in Python, including reading, writing, and filtering data in different formats.

Requirements
Raw Data Handling
Create a file named raw_data.txt containing some random names and ages.
Read the file and store the data in a Python list or dictionary.
JSON Export
Create a file named data.json and save the collected data in a professional JSON format.
CSV Challenge
Create a file named students.csv containing two columns: Name and Grade.
Read this file and select students with a grade above 70.
Save these students in a new file named passed_students.csv.
Try-Except Blocks
Handle file reading/writing errors gracefully.
Provide informative messages if a file is missing or cannot be written.

Notes

This task emphasizes practical file operations and error handling in Python.

## Day 07

Project: Sales Analysis and Reporting System (S.A.R.S)

Description:

The goal of this task is to practice data processing, cleaning, and analysis using Python by building a modular system that handles real-world sales data.

Requirements

Raw Data Handling
Create a file named sales_data.csv containing customer, product, category, and price information.
Read the CSV file and store the data in a suitable Python structure (list of dictionaries).

Data Cleaning
Remove rows with invalid or non-numeric prices.
Remove rows with negative price values.
Standardize customer names (capitalize first letter).
Log all invalid records into a file named errors.log.

Data Analysis
Calculate the total sales amount.
Find the best-performing category based on total sales.
Identify and list "premium" sales (sales above a certain threshold, e.g., 1000).

JSON Export
Create a file named report.json.
Store the analysis results in a structured and readable JSON format.

Modular Structure
Split the project into at least two files:

data_utils.py → data cleaning and analysis functions
main.py → main execution flow

Error Handling
Use try-except blocks to handle:

File not found errors
Data conversion errors
Ensure the program does not crash and provides meaningful messages.

Professional Standards
Use type hinting for all functions.
Write clear and descriptive docstrings.
Follow PEP8 naming and formatting conventions.

Notes

This task simulates a real-world data analyst workflow, focusing on data cleaning, analysis, modular coding, and professional software development practices.

## Day 08

Project: 08_classes_and_objects.py
Description:

The goal of this task is to practice Object-Oriented Programming (OOP) in Python by designing a simple data source management system.

Requirements

Class Definition
Create a class named DataSource.

Constructor (init)
The class should initialize with the following attributes:

source_name (string)
file_type (string)
row_count (integer)

Methods
Implement the following methods inside the class:

describe() → Display the data source information in a formatted way.
update_row_count(new_count) → Update the row count value.

Object Creation
Create at least two objects:

Customer List (CSV)
Sales Data (JSON)

Method Usage
Call the methods to:

Display initial data
Update row counts
Display updated data

Notes

This task focuses on understanding classes, objects, attributes, and methods, which are fundamental concepts in Object-Oriented Programming.

## Day 09

Project: 09_inheritance.py

Description:

The goal of this task is to understand and implement object-oriented programming concepts in Python, specifically inheritance and method overriding.

Requirements

Base Class
Create a class named `BaseModel`.
Define an `__init__` method that takes `model_name` and `version` as parameters.
Add a method named `train()` that prints "Model is being trained...".

NLP Model
Create a class named `NLPModel` that inherits from `BaseModel`.
Add an extra attribute called `language`.
Override the `train()` method to print a customized message like:
"NLP model is being trained for [language]...".

Vision Model
Create a class named `VisionModel` that inherits from `BaseModel`.
Add an extra attribute called `resolution`.

Usage
Create one object from each class (`NLPModel` and `VisionModel`).
Assign appropriate values to their attributes.
Call their `train()` methods to observe the difference in behavior.

Concepts Covered

* Inheritance
* Method overriding
* Use of `super()`
* Class structure and object creation

Notes

This task focuses on understanding how base classes can be extended and customized through inheritance, a key concept in object-oriented programming.

## Day 10

Project: 10_encapsulation.py  

Description:

The goal of this task is to understand and implement the concept of encapsulation in Python by controlling access to class attributes using private and protected variables.

Requirements

Database Connector Class  
Create a class named `DatabaseConnector`.

Initialization  
Define a constructor (`__init__`) that takes a `connection_string` parameter.  
Store it as a private attribute (`__connection_string`).  
Define a protected attribute (`_status`) to track connection status.

Getter Method  
Create a getter method for `connection_string`.  
It should return a masked version of the string:  
- Show only the first 10 characters  
- Replace the rest with `*`

Setter Method  
Create a setter method for `connection_string`.  
It should validate the input:  
- If the new string does not start with `"http"`, raise a `ValueError`.

Encapsulation Test  
Try to access the private attribute directly from outside the class and observe the error.  
Then use the getter and setter methods to access and modify the value safely.

Notes

This task demonstrates how encapsulation improves data security and control in object-oriented programming.

## Day 11

Project: 11_polymorphism.py  

Description:

The goal of this task is to understand and implement polymorphism in Python by creating a flexible metric evaluation system where different classes share the same method name but produce different outputs.

Requirements

Base Class  
Create a class named `Metric`.  
Define a method called `calculate()` that prints:  
"Metric is being calculated..."

Accuracy Metric  
Create a class named `AccuracyMetric` that inherits from `Metric`.  
Override the `calculate()` method to print:  
"Accuracy is being calculated..."

Precision Metric  
Create a class named `PrecisionMetric` that inherits from `Metric`.  
Override the `calculate()` method to print:  
"Precision is being calculated..."

Polymorphism Demonstration  
Create a list called `metrics_list` and store objects of the above classes.  
Loop through the list and call the `calculate()` method on each object.  
Observe how the same method name produces different outputs depending on the object type.

Notes

This task demonstrates polymorphism, a core concept of object-oriented programming where the same interface behaves differently based on the object implementation.

## Day 12

Project: 12_dunder_methods.py  

Description:

The goal of this task is to understand and implement special (dunder) methods in Python by creating a custom Dataset class that behaves like built-in data structures.

Requirements

Dataset Class  
Create a class named `Dataset`.  
Define an `__init__` method that takes `data` (list) and `name` (string).

String Representation  
Implement the `__str__` method.  
When the object is printed, it should display:  
"Dataset: [name] ([number] records)"

Length Support  
Implement the `__len__` method.  
It should return the number of elements in the dataset.

Addition Operator  
Implement the `__add__` method.  
When two Dataset objects are added using `+`, their data should be combined.  
Return a new Dataset object containing the merged data.

Testing  
Create two dataset objects.  
Combine them using the `+` operator.  
Use `len()` to verify the total number of records and print the result.

Notes

This task demonstrates how Python's special methods allow custom objects to behave like built-in types, improving usability and readability.


## Day 13

Project: 13_advanced_python_tools.py  

Description:

The goal of this task is to explore advanced Python tools such as decorators, generators, and type hinting by simulating a simple data processing pipeline.

Requirements

Decorator  
Create a decorator named `log_execution`.  
It should print when a function starts and when it finishes execution.

Generator  
Create a generator function named `data_streamer`.  
It should yield items from a given list one by one.  
Before yielding each item, print a message indicating that the data is being processed.

Application  
Create a large dataset (e.g., using `range(100)`).  
Iterate over the dataset using the generator.  
Process each item using a function decorated with `log_execution`.

Clean Code  
Use type hints such as `Callable` and `Iterator` from the `typing` module.  
Write clear and readable code with proper structure.

Notes

This task demonstrates how decorators and generators can be combined to build efficient and traceable data processing workflows in Python.


## Day 14

Project: Smart Data Processing and Analysis Pipeline

Description:

The goal of this project is to build a modular and scalable data processing pipeline that handles multiple data sources (CSV, JSON, and lists) using object-oriented programming, generators, and decorators. The system is designed to be memory efficient and suitable for large-scale data processing.

Requirements

Base Processor (OOP & Inheritance)  
Create a base class named `BaseProcessor`.  
This class defines common behavior for all data processors.

CSV Processor  
Create a class named `CSVProcessor` that inherits from `BaseProcessor`.  
It should read CSV files and process data line by line.

JSON Processor  
Create a class named `JSONProcessor` that inherits from `BaseProcessor`.  
It should read JSON files and process data accordingly.

Generators (Memory Efficiency)  
Use generator functions to yield data line by line instead of loading the entire dataset into memory.  
This simulates processing large-scale datasets efficiently.

Decorator (Performance Tracking)  
Create a decorator named `time_logger`.  
It should measure and print the execution time of data processing functions.

Dunder Methods  
Implement `__len__` to return the total number of processed records.  
Implement `__str__` to return information about the processor.

Encapsulation & Error Handling  
Store file paths as protected attributes (`_file_path`).  
Use try-except blocks to handle invalid file formats or missing files.

Notes
This project demonstrates real-world data pipeline architecture using Python.  
It combines object-oriented programming, generators, decorators, and error handling to create a scalable and memory-efficient system.

## Day 15

Project: 15_numpy_basics.py

Description:

The goal of this task is to practice NumPy operations for analyzing AI model prediction data. This includes statistical analysis, vectorized operations, filtering, and matrix reshaping.

Requirements

Random Data Generation
Create a NumPy array named `predictions` containing 100 random floating-point numbers between 0 and 1.

Statistical Analysis
Calculate the mean, standard deviation, and variance of the predictions.

Vectorized Operations
Multiply all prediction values by 100 and convert them to integers without using loops.

Filtering
Select prediction values greater than 50 using boolean indexing and store them in a new array.

Matrix Transformation (Bonus)
Reshape the 100-element array into a 10x10 matrix.

Notes

This task emphasizes efficient numerical computation using NumPy and introduces key concepts used in data analysis and machine learning workflows.

## Day 16

Project: 16_pandas_dataframe_basics.py

Description:

The goal of this task is to practice basic data analysis using Pandas DataFrames. It includes data creation, filtering, statistical analysis, and sorting operations.

Requirements

Data Creation
Create a dictionary containing employee information such as Name, Department, Experience, and Salary.

DataFrame Conversion
Convert the dictionary into a Pandas DataFrame.

Data Exploration
Display the first 3 rows of the DataFrame.

Filtering
Filter and display employees who work in the Software department.

Statistical Analysis
Calculate the average salary and total years of experience.

Sorting (Bonus)
Sort the DataFrame by Experience in descending order.

Notes

This task introduces fundamental Pandas operations used in real-world data analysis workflows.

## Day 17

Project: 17_data_cleaning.py

Description:

The goal of this task is to practice data cleaning techniques on a raw e-commerce dataset. This includes handling missing values, removing duplicates, correcting invalid data, and standardizing categorical values.

Requirements

Data Preparation
Create a raw dataset containing order information such as Order ID, Customer, Amount, and City.

Duplicate Handling
Identify duplicate rows using .duplicated() and remove them using .drop_duplicates().

Missing Data Handling
Fill missing Customer values with "Unknown Customer".
Fill missing Amount values with the column mean.

Data Correction
Fix invalid values such as negative amounts.

Data Standardization
Ensure consistency in City names using replacement techniques.

Notes

This task focuses on real-world data cleaning processes commonly used in data analysis and machine learning pipelines.

## Day 18

Project: 18_pandas_groupby_analysis.py

Description:

The goal of this task is to practice grouping and aggregation techniques using Pandas. This includes summarizing data by categories, calculating statistics, and analyzing sales performance.

Requirements

Data Creation
Create a DataFrame containing sales representative, region, sales amount, and units sold.

GroupBy Analysis
Calculate total sales amount by region.

Sorting
Find the average units sold per sales representative and sort the results in descending order.

Multiple Aggregations
Use the .agg() method to calculate multiple statistics (total sales and maximum units sold) for each region.

Filtering + Grouping
Filter records where sales amount is greater than 5000 and count them by region.

Notes

This task introduces the core concept of "split-apply-combine", which is fundamental in data analysis and real-world data pipelines.

## Day 19

Project: 19_pandas_merging_data.py

Description:

The goal of this task is to practice combining multiple datasets using Pandas. In real-world applications, data is often split across multiple sources, and merging them correctly is essential for analysis and machine learning workflows.

Requirements

DataFrames Creation
Create a Users DataFrame containing user information (user_id, name, email).
Create an Activity DataFrame containing user activity logs (user_id, last_login, total_spend).

Inner Join
Perform an inner merge to return only users who have matching activity records.

Left Join
Perform a left merge to keep all users, including those without activity data.

Concatenation
Create a new DataFrame with additional users and append it to the original dataset using concatenation.

Notes

This task demonstrates the core concepts of relational data handling in Pandas, similar to SQL join operations used in databases.

## Day 20

Project: 20_time_series_and_transforms.py

Description:

The goal of this task is to learn how to work with time-series data in Pandas. Time-based data is essential for monitoring systems, financial analysis, and AI service performance tracking.

Requirements

Datetime Conversion
Convert string timestamps into proper datetime objects using pd.to_datetime().

Feature Engineering
Create a new column that identifies whether a timestamp falls on a weekend.

Custom Transformations
Use the .apply() method to classify response times as "High Latency" or "Optimal".

Time-Based Aggregation
Resample the data to calculate the average response time per day.

Error Handling
Handle potential datetime conversion errors using try-except blocks.

Notes

This project introduces time-series fundamentals used in real-world monitoring and analytics systems.


