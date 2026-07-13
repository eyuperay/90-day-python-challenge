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

## day 21 Capstone Project

Project: Automated Financial & Operational Health Report

Description:

This project builds an end-to-end data pipeline that processes raw transaction data, cleans inconsistencies, merges department metadata, and generates a financial health report.

Steps Performed:

1. Data Loading:
   Transactions loaded from CSV and department metadata from JSON.

2. Data Cleaning:
   - Removed duplicate transaction IDs
   - Converted transaction_date to datetime
   - Filled missing values using department median

3. Data Merging:
   Left join used to attach department metadata to transactions

4. Feature Engineering:
   - Budget status calculated based on department limits
   - 7-day rolling average of transaction amounts computed

5. Output:
   Final cleaned dataset exported as CSV
   Processing logs stored in process.log

Tools Used:
- Pandas
- Python datetime
- Custom decorators
- Modular Python design

## Day 22 - Introduction to Data Visualization (Matplotlib & Seaborn)

### Project: Model Performance Visualization

### Description:
In this project, we explore data visualization using Matplotlib and Seaborn. The goal is to visually compare model performance over training epochs and analyze relationships in real-world datasets.

---

### What This Project Does:

#### 1. Matplotlib Visualization
- Simulates training accuracy for two models (Model A and Model B)
- Plots accuracy over 10 epochs
- Adds:
  - Title: Model Training Progress
  - X-axis: Epochs
  - Y-axis: Accuracy
  - Legend for comparison

#### 2. Seaborn Visualization
- Uses built-in `tips` dataset
- Creates a scatter plot showing relationship between:
  - Total bill
  - Tip amount
- Uses:
  - color grouping by day
  - whitegrid style for better readability

---

### Technologies Used:
- Python
- NumPy
- Matplotlib
- Seaborn

---

### Key Learning Objectives:
- Understanding basic plotting with Matplotlib
- Creating statistical visualizations with Seaborn
- Comparing model performance visually
- Working with real-world datasets
- Improving data storytelling skills

---



## Day 23 - Statistical Distributions and Outlier Detection

### Project: AI Inference Latency Analysis

### Description:
This project analyzes the distribution of AI model inference latency values and detects abnormal values (outliers) using statistical methods. It combines data visualization with mathematical anomaly detection.

---

### What This Project Does:

#### 1. Data Generation
- Creates 1000 synthetic latency values using a normal distribution
- Adds artificial extreme values (outliers)

---

#### 2. Data Visualization

##### Histogram + KDE Plot:
- Shows the distribution of latency values
- Includes a smooth density curve (KDE)
- Helps identify skewness and spread of data

##### Box Plot:
- Visualizes median, quartiles, and outliers
- Clearly highlights abnormal values

---

#### 3. Outlier Detection (IQR Method)

The Interquartile Range (IQR) method is used:

- Q1 = 25th percentile
- Q3 = 75th percentile
- IQR = Q3 - Q1

Outliers are defined as:
- Values below Q1 - 1.5 * IQR
- Values above Q3 + 1.5 * IQR

---

### Technologies Used:
- Python
- NumPy
- Matplotlib
- Seaborn

---

### Key Learning Objectives:
- Understanding statistical distributions
- Identifying skewed data patterns
- Detecting outliers using IQR method
- Visualizing distributions with histograms and box plots
- Applying basic statistical reasoning in AI monitoring

---

### How to Run:
bash
pip install numpy matplotlib seaborn  

## Day 24 - Categorical Relationships and Correlation Heatmaps

### Project: AI Treasury Process Analysis

### Description:
This project analyzes relationships between system performance metrics and identifies patterns between categorical and numerical variables using correlation analysis and visualization techniques.

---

### What This Project Does:

#### 1. Synthetic Dataset Creation
The dataset includes:
- Processing_Time
- Error_Rate
- Token_Usage
- Cost
- Success_Rate
- Model_Type (categorical)

---

#### 2. Correlation Analysis
- Computes Pearson correlation between numerical features using `.corr()`
- Measures relationships between variables:
  - Positive correlation (close to +1)
  - Negative correlation (close to -1)
  - No correlation (close to 0)

---

#### 3. Heatmap Visualization
- Uses `sns.heatmap()`
- Displays correlation matrix visually
- Includes numeric annotations for clarity
- Uses `coolwarm` color palette

---

#### 4. Categorical Analysis
- Uses `sns.barplot()`
- Shows average Error Rate per Model Type
- Helps compare performance across models

---

#### 5. Output Export
- Saves correlation matrix as `correlation_matrix.csv` for documentation and analysis

---

### Technologies Used:
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

---

### Key Learning Objectives:
- Understanding feature correlation
- Interpreting heatmaps
- Comparing categorical groups statistically
- Combining visualization + data analysis
- Preparing data for AI model evaluation

---

### How to Run:
bash
pip install pandas numpy matplotlib seaborn

## Day 25 - Interactive Data Visualization with Plotly

### Project: Treasury Operational Dashboard

### Description:
This project introduces interactive data visualization using Plotly. It simulates a financial monitoring dashboard for analyzing transaction behavior across different regions.

---

### What This Project Does:

#### 1. Dataset Creation
- Simulates 200 financial transactions
- Includes:
  - Date
  - Amount
  - Region
  - Transaction Fee

---

#### 2. Interactive Scatter Plot
- Uses `plotly.express.scatter`
- Shows relationship between:
  - Transaction Amount
  - Transaction Fee
- Features:
  - Color-coded regions
  - Hover tooltips showing date
  - Fully interactive zoom and pan

---

#### 3. Interactive Bar Chart
- Aggregates total transaction amount by region
- Displays comparative regional performance

---

#### 4. HTML Export
- Saves interactive chart as:
  - `transaction_report.html`
- Can be opened in any browser without Python

---

### Technologies Used:
- Python
- Pandas
- NumPy
- Plotly

---

### Key Learning Objectives:
- Building interactive charts
- Using hover and color dimensions
- Creating browser-based dashboards
- Exporting visualizations to HTML
- Understanding modern BI tools (like Power BI / Tableau logic)

---

### How to Run:
pip install plotly pandas numpy

## Day 26 - EDA Part 1: Investigation & Hypothesis Building

### Project: Automated Invoice Processing Analysis

---

## Description
This project performs the first stage of Exploratory Data Analysis (EDA) on an invoice dataset. The goal is to understand structure, detect missing values, and explore relationships between variables.

---

## Dataset Features
- Invoice_ID: Unique identifier for invoices
- Vendor_Category: Type of vendor
- Invoice_Amount: Payment amount (contains missing values)
- Days_to_Pay: Payment delay in days
- Approval_Status: Invoice approval state

---

## EDA Workflow

### 1. Data Overview
- `.info()` for structure
- `.describe()` for statistical summary

---

### 2. Missing Value Analysis
- Heatmap visualization of missing data
- Helps identify data quality issues

---

### 3. Univariate Analysis
- Distribution of Invoice Amount
- KDE + histogram to detect skewness

---

### 4. Bivariate Analysis
- Vendor Category vs Invoice Amount
- Boxplot used for comparison

---

## Key Insight Goals
- Identify missing data patterns
- Detect skewed financial distributions
- Compare vendor pricing behavior
- Build hypotheses for further analysis

---

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

---

## How to Run
bash
pip install pandas numpy matplotlib seaborn

## Day 27 -eda_part2_cleaning- Feature Engineering & Data Transformation

### Project: Treasury Risk Model Feature Optimization

---

## Description
This project focuses on transforming raw financial transaction data into machine learning-ready features using feature engineering techniques.

---

## Dataset Features
- Transaction_ID: Unique identifier
- Amount: Transaction value
- Category: Type of transaction (Travel, Tech, Legal, Rent)
- Days_Since_Last_Audit: Time since last audit

---

## Feature Engineering Steps

### 1. Log Transformation
- Reduces skewness in Amount
- Creates: Log_Amount

---

### 2. Binning (Discretization)
- Converts Days_Since_Last_Audit into categories:
  - Low
  - Medium
  - High
- Creates: Audit_Urgency

---

### 3. One-Hot Encoding
- Converts Category into binary columns
- Example:
  - Category_Travel
  - Category_Tech
  - Category_Legal
  - Category_Rent

---

### 4. Derived Feature (Risk Score)
A weighted score combining:

- Log_Amount (importance: 70%)
- Normalized audit time (importance: 30%)

This helps identify high-risk transactions.

---

## Technologies Used
- Python
- Pandas
- NumPy

---

## How to Run
bash
pip install pandas numpy


# Day 28 - eda part 3 - Comprehensive EDA Report

## Project: Treasury Operations Analytics (Adidas Simulation)

---

## Objective
To perform a full Exploratory Data Analysis (EDA) pipeline including:
- Data cleaning
- Visualization
- Feature engineering
- Insight generation

---

## Dataset Features
- Request_ID
- Employee_Level
- Process_Time
- Cost
- Error_Found
- Region

---

## Workflow

### Phase 1: Data Integrity
- Missing values handled using median imputation
- Negative values removed

---

### Phase 2: Visualization
- Violin plot: Employee Level vs Process Time
- Heatmap: Cost vs Process Time correlation
- Bar plot: Error rate by region

---

### Phase 3: Feature Engineering
- Cost_Efficiency ratio created
- Region encoded using one-hot encoding

---

### Phase 4: Insights
Automated business insights:
- Highest error region
- Highest cost region
- Fastest employee level

---

## Tools Used
- Python
- Pandas
- NumPy
- Seaborn
- Matplotlib

---

## Output
- Cleaned dataset
- Visual dashboard
- Feature-enhanced dataset
- Final report summary

# Day 29
## Project Overview
This repository contains a structured 90-day learning journey focused on Python, Data Engineering, and AI-ready data pipelines for treasury and financial operations.

---

## Week 1–2: Core Engineering
- Python fundamentals
- OOP principles
- Decorators & generators
- File handling automation

---

## Week 3–4: Data Engineering & EDA
- Pandas data manipulation
- Data cleaning techniques
- Feature engineering
- Data visualization (Matplotlib, Seaborn, Plotly)
- Exploratory Data Analysis (EDA)

---

## Week 5: EDA Pipeline (Structured Workflow)
This project simulates a real-world data pipeline:

- Data investigation
- Data cleaning
- Visualization
- Feature engineering
- Final reporting

---

## Business Impact
This project simulates real treasury workflows:

- Automated financial data cleaning
- Detection of anomalies in transaction logs
- Feature engineering for AI risk models
- Visualization of operational inefficiencies
- Reporting for decision-makers

---

## Tools Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly

---

## Goal
To build a production-style data pipeline that mirrors real-world data engineering and analytics systems used in finance departments.

# Day 30: Month 2 Blueprint - Treasury AI Roadmap

## Objective
This milestone marks the transition from **Exploratory Data Analysis (EDA)** to **Machine Learning and Predictive AI systems**.

Instead of analyzing past data, the focus now shifts to:

- Predicting financial risk
- Automating decision-making
- Building AI-driven treasury systems

---

## Month 2 Learning Roadmap

### Week 5 - Machine Learning Foundations
- Scikit-Learn basics
- Regression (Linear Regression)
- Classification (Logistic Regression)
- Model training workflow: fit() → predict()

---

### Week 6 - Advanced Machine Learning
- Random Forests
- Gradient Boosting models (XGBoost concept)
- Hyperparameter tuning
- Feature importance analysis

---

### Week 7 - NLP & Large Language Models
- Text preprocessing
- TF-IDF & embeddings
- Introduction to LLMs
- Retrieval-Augmented Generation (RAG)

---

### Week 8 - Model Evaluation
- Confusion Matrix
- Precision / Recall / F1 Score
- ROC-AUC
- Business impact evaluation (cost vs risk)

---

## Strategic Vision

This roadmap shifts the role from:

> Data Analyst → AI Treasury Systems Engineer

The goal is to move from descriptive analytics to predictive and intelligent decision systems.

---

## Output

Running `30_month2_blueprint.py` prints a structured roadmap of Month 2 learning objectives.

# Day 31: Introduction to Machine Learning (Scikit-Learn)

## Objective
This project introduces the fundamentals of Machine Learning using Scikit-Learn.

The goal is to understand how models learn patterns from data and make predictions.

---

## Scenario
A "Predictive Budget Estimator" is built to estimate how many hours a project will require based on its complexity.

---

## Machine Learning Workflow

1. Instantiate the model
2. Train the model using `.fit()`
3. Make predictions using `.predict()`

---

## Dataset

Synthetic dataset generated using:

- Feature: Project_Complexity (1–10)
- Target: Required_Hours

Formula used:

Required_Hours = 5 × Complexity + Noise

---

## Key Concepts

- Train/Test Split (to prevent overfitting)
- Linear Regression
- Model Coefficient (slope)
- Model Intercept

---

## Output

- Learned coefficient (should be close to 5)
- Learned intercept
- Predicted hours for a new project

---

## Business Impact

This model simulates how treasury teams can:

- Estimate project costs
- Predict resource allocation
- Automate budgeting decisions

---

## Learning Outcome

Transition from:

Rule-based logic → Data-driven prediction

# Day 32: Classification with Logistic Regression

## Objective
Build a classification model to predict whether a transaction will be approved.

---

## Scenario
An automated "Treasury Approval Gate" system predicts:

- Approved (1)
- Denied (0)

based on:
- Transaction Amount
- User Seniority

---

## Machine Learning Workflow

1. Generate synthetic dataset
2. Split into training and testing sets
3. Scale features using StandardScaler
4. Train Logistic Regression model
5. Evaluate predictions

---

## Key Concepts

- Classification vs Regression
- Logistic Regression
- Feature Scaling
- Decision Threshold (0.5)
- Evaluation Metrics:
  - Precision
  - Recall
  - F1-score

---

## Output

- Classification report showing model performance
- Accuracy typically around 80–90%

---

## Business Impact

This system simulates:

- Automated approval pipelines
- Risk-based decision making
- Reduction of manual review workload

---

## Learning Outcome

Transition from:

Predicting values → Predicting decisions

# Day 33: Confusion Matrix & Model Evaluation

## Objective
This project evaluates a classification model using a Confusion Matrix and translates prediction errors into real business costs.

---

## Scenario
A Treasury Approval model is analyzed to determine:

- How many fraud cases are correctly detected
- How many legitimate transactions are incorrectly flagged
- The financial impact of model errors

---

## Machine Learning Workflow

1. Generate synthetic financial dataset
2. Train Logistic Regression model
3. Predict approval outcomes
4. Evaluate results using Confusion Matrix
5. Convert errors into business cost

---

## Confusion Matrix Explained

| Term | Meaning |
|------|--------|
| True Positive (TP) | Fraud correctly detected |
| True Negative (TN) | Legitimate transaction correctly accepted |
| False Positive (FP) | Legitimate transaction flagged as fraud |
| False Negative (FN) | Fraud missed by model |

---

## Business Cost Assumptions

- False Positive (FP): $50 cost (manual review effort)
- False Negative (FN): $500 cost (financial loss)

---

## Key Outputs

- Confusion Matrix (numerical)
- Visual Confusion Matrix plot
- Total operational cost of model errors
- Summary statement of financial risk

---

## Example Insight

"Our model missed X fraud cases, resulting in a potential loss of $Y."

---

## Business Impact

This system demonstrates how machine learning is used in financial systems to:

- Reduce fraud risk
- Optimize approval pipelines
- Quantify cost of prediction errors
- Support decision-making in Treasury operations

---

## Learning Outcome

You learned that:

- Accuracy alone is not enough
- Different errors have different costs
- ML models must be evaluated using business logic, not just statistics

---

## Tools Used

- Python
- Scikit-learn
- Logistic Regression
- Confusion Matrix
- Matplotlib

---

## Next Step

Move toward:
- Decision Trees
- Random Forests
- Explainable AI models

# Day 34: Decision Trees - Vendor Risk Assessment

## Objective
Build an interpretable AI model to classify vendors as HIGH RISK or LOW RISK.

---

## Scenario
We analyze vendor behavior using:

- Years in Business
- Late Payments
- Contract Value

The model predicts whether a vendor is risky for Treasury operations.

---

## Machine Learning Workflow

1. Generate synthetic vendor dataset
2. Train Decision Tree Classifier (max_depth=3)
3. Visualize decision logic as a tree
4. Extract feature importance
5. Explain prediction path step-by-step

---

## Key Concepts

### Decision Tree Structure
- Root Node: First decision split
- Branches: Conditions (True/False paths)
- Leaves: Final prediction

---

## Why max_depth=3?

To prevent overfitting and ensure generalization.

---

## Feature Importance

The model automatically calculates which features influence decisions the most.

---

## Business Impact

Decision Trees help Treasury teams:

- Understand why a vendor is marked risky
- Reduce manual audit workload
- Improve transparency in AI decisions

---

## Learning Outcome

You learned:

- How AI makes rule-based decisions
- How splits are determined (Gini/Entropy conceptually)
- How to interpret AI decisions step-by-step

---

## Output

- Decision Tree visualization
- Feature importance ranking
- Step-by-step decision explanation


# Day 35 - Random Forest Fraud Detection

## Objective
Build a Random Forest model to detect fraudulent transactions and compare it with a Decision Tree.

---

## Models Used
- Decision Tree (Baseline)
- Random Forest (Ensemble Model)

---

## Key Concepts

### Random Forest
An ensemble of multiple decision trees that vote on the final prediction.

### Why it works better
- Reduces overfitting
- Uses multiple random samples of data (bootstrapping)
- Uses random feature selection

---

## Output

- Model accuracy comparison
- Feature importance ranking
- Visualization of most important fraud indicators

---

## Business Value
This model helps Treasury teams:
- Detect fraud more accurately
- Reduce false alarms
- Improve decision consistency

# Day 36 - K-Means Clustering Analysis

## Objective
This project applies **unsupervised machine learning (K-Means clustering)** to segment vendors based on their invoice behavior.

---

## Business Scenario
In Treasury operations, vendors behave differently:
- Some invoice frequently with small amounts
- Others invoice rarely but with high amounts

We use clustering to automatically group them.

---

## Dataset Features

- Invoice_Frequency → How often vendors send invoices
- Average_Value → Average invoice amount

---

## Workflow

### 1. Data Generation
Synthetic vendor dataset is created for simulation purposes.

### 2. Feature Scaling
StandardScaler is used because K-Means relies on distance calculations.

---

### 3. Elbow Method
We test K values from 1 to 10 and measure inertia.

Purpose:
- Helps find optimal number of clusters

---

### 4. K-Means Model
We train the final model with:
- K = 3 clusters

---

### 5. Visualization
Two key visual outputs:

#### Elbow Curve
- Shows optimal cluster count

#### Cluster Plot
- Vendors grouped into clusters
- Cluster centers marked with black X

---

## Key Learnings

- How K-Means groups data without labels
- Why scaling is essential for distance-based models
- How to interpret clusters for business segmentation

---

## Business Value

This model helps Treasury teams:
- Identify vendor behavior patterns
- Optimize payment strategies
- Detect unusual vendor activity

---

## Output

- Elbow method graph
- Cluster visualization
- Vendor segmentation results

# Day 37 - Anomaly Detection with Isolation Forest

##  Project Overview
This project demonstrates how to detect unusual (suspicious) financial transactions using an **Isolation Forest** machine learning model.

The goal is to automatically identify abnormal expense patterns that may indicate fraud, errors, or policy violations in Treasury operations.

---

##  Key Concept

Isolation Forest is an **unsupervised anomaly detection algorithm** that works on the idea that:

> Anomalies are rare and easier to isolate than normal data points.

- Normal transactions require many splits to isolate
- Anomalies require fewer splits

---

##  Dataset Description

The dataset is synthetically generated:

### Normal Transactions:
- Amount: 20 – 150
- Days Since Last Transaction: 1 – 5
- Count: 500 records

### Anomalous Transactions:
- Amount: 1500 – 3000
- Days Since Last Transaction: 20 – 30
- Count: 10 records

---

##  Model Configuration

python
IsolationForest(
    contamination=0.02,
    random_state=42
)


# Day 38 - PCA Dimensionality Reduction

##  Objective
Reduce high-dimensional financial data into 2 principal components for visualization and pattern discovery.

---

##  Concept

Principal Component Analysis (PCA) transforms many correlated variables into fewer uncorrelated components.

- PC1 → captures most variance
- PC2 → captures remaining variance

---

##  Workflow

### 1. Data Generation
- 10 financial ratio features
- 200 samples

### 2. Standardization
- All features scaled using StandardScaler
- Prevents dominance of large-value features

### 3. PCA Transformation
- Reduced 10 features → 2 components
- Fit + transform applied

---

##  Visualization

- Scatter plot of PC1 vs PC2
- Each point represents a data sample in reduced space

---

##  Explained Variance

The model prints:

- Individual variance per component
- Total variance retained

Example:

Total Variance Captured: 93.45%


---

##  Business Value

PCA is used in Treasury & Finance for:

- Risk grouping of departments
- Fraud pattern simplification
- Visualization of complex financial ratios
- Noise reduction in financial signals

---

##  Learning Outcome

You learned how to:

- Reduce dimensionality safely
- Preserve information using variance
- Visualize high-dimensional financial data
- Apply PCA in real-world business analytics

# Day 39 - Model Selection & Hyperparameter Tuning

## Objective
Improve model performance by automatically selecting the best hyperparameters using GridSearchCV.

---

## Concept

Hyperparameters are configuration settings defined before training.

Examples:
- Number of trees in a Random Forest
- Maximum tree depth
- Minimum samples required for splitting

---

## Key Techniques

### Cross-Validation (CV)
- Data is split into multiple folds
- Model is trained and validated multiple times
- Reduces risk of overfitting

---

### Grid Search
- Tests all combinations of hyperparameters
- Finds the best-performing configuration

---

## Workflow

### 1. Dataset
- Synthetic fraud detection dataset
- Features: Amount, Seniority, Frequency, Risk Score
- Target: Fraud (0/1)

---

### 2. Model Tuning
- Algorithm: Random Forest
- Tool: GridSearchCV
- CV: 5-fold cross-validation

---

### 3. Output
- Best hyperparameters
- Best cross-validation score
- Final test accuracy

---

## Business Value

Hyperparameter tuning is used in:

- Fraud detection systems
- Credit risk modeling
- Financial forecasting
- AI optimization pipelines

---

## Learning Outcome

You learned how to:

- Automatically optimize ML models
- Avoid manual trial-and-error tuning
- Use cross-validation for reliable evaluation
- Select production-ready models


# Day 40 - E-Commerce Inventory Management API

## Description

A production-ready RESTful API for managing e-commerce inventory, products, orders, and user authentication. Built with FastAPI, PostgreSQL, Redis, and Docker. This project demonstrates real-world backend development practices including JWT authentication, role-based access control, caching, and containerization.

## Features

- **User Authentication** - Register, login, and JWT-based authorization
- **Product Management** - Full CRUD operations with filtering and search
- **Category Management** - Organize products with categories
- **Order Management** - Create and track customer orders
- **Inventory Management** - Track stock levels and reorder points
- **Role-Based Access** - Admin and Employee roles with different permissions
- **Redis Caching** - Performance optimization for frequently accessed data
- **Docker Support** - Containerized application for easy deployment
- **API Documentation** - Auto-generated Swagger UI and ReDoc

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **PostgreSQL** | Primary database |
| **SQLAlchemy** | ORM |
| **Redis** | Caching |
| **Docker** | Containerization |
| **JWT** | Authentication |
| **Pytest** | Testing |

## Requirements

### Prerequisites

- **Python 3.11+**
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Git** (optional)

### Python Packages

All dependencies are listed in `requirements.txt`:
- FastAPI
- SQLAlchemy
- Pydantic
- Python-JOSE
- Passlib
- Redis
- Pytest

## Installation

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/day40-ecommerce-inventory-api.git
cd day40-ecommerce-inventory-api

# 2. Start all services with Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# 3. Seed the database with sample data
docker exec -it day40_app python scripts/seed_data.py

# 4. Access the API
curl http://localhost:8000

# Day 41 - CRM API

## Description

A production-ready CRM (Customer Relationship Management) REST API for managing customers, leads, interactions, deals, and tasks. Built with FastAPI, PostgreSQL, Redis, and Docker.

## Features

- **User Management** - Multi-role authentication (Admin, Sales, Support, Viewer)
- **Customer Management** - Full CRUD with status tracking (Active, VIP, Potential)
- **Lead Management** - Track leads through sales pipeline with scoring
- **Interaction Tracking** - Log calls, emails, meetings, and notes
- **Deal Management** - Track sales deals through stages
- **Task Management** - Assign and track tasks with priorities
- **Redis Caching** - Performance optimization
- **Docker Support** - Easy deployment

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **PostgreSQL** | Primary database |
| **SQLAlchemy** | ORM |
| **Redis** | Caching |
| **Docker** | Containerization |
| **JWT** | Authentication |
| **Pytest** | Testing |

## Quick Start

```bash
# Start services
docker-compose -f docker/docker-compose.yml up -d

# Seed database
docker exec -it day41_app python scripts/seed_data.py

# Access API
curl http://localhost:8000

# Swagger UI
http://localhost:8000/docs

# Day42 Task Management API

A modern, fast and secure task management backend built with **FastAPI**.

## Features

- JWT Authentication (Register & Login)
- Project Management (Create, List, View)
- Task Management (Create, List, View with status & priority)
- Comments System on Tasks
- Inventory Management
- Async SQLAlchemy with PostgreSQL support
- Redis caching ready
- CORS configured for frontend integration
- Docker & Docker Compose support
- Comprehensive test coverage

## Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Database**: SQLAlchemy (Async) + PostgreSQL (SQLite for development)
- **Cache**: Redis
- **Authentication**: JWT + bcrypt
- **Validation**: Pydantic v2
- **Container**: Docker

## Quick Start

### 1. Local Setup

```bash
# 1. Clone the project
git clone <your-repo-url>
cd day42-task-management-api

# 2. Copy environment file
cp .env.example .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload

# Day 43 - Booking System API

## Objective

Build a RESTful Booking System API using FastAPI with JWT authentication, allowing users to manage service providers, bookings, availability schedules, and reviews.

---

## Concept

A Booking System API enables customers to schedule appointments with service providers while preventing scheduling conflicts through availability management.

The project follows a layered FastAPI architecture using routers, services, models, and schemas.

---

## Key Features

### Authentication

* User Registration
* User Login
* JWT Access Token
* Protected Endpoints

---

### Booking Management

* Create bookings
* Update bookings
* Cancel bookings
* View booking history

---

### Provider Management

* Create service providers
* Manage provider profiles
* Define available working hours
* Block unavailable dates

---

### Review System

* Leave customer reviews
* Rate service providers
* Retrieve provider reviews

---

## Workflow

### 1. Authentication

* Register a new user
* Login to receive a JWT access token
* Authorize protected endpoints

---

### 2. Provider Setup

* Create provider profiles
* Configure availability schedule
* Define unavailable dates

---

### 3. Booking Process

* Search provider availability
* Create a booking
* Update or cancel reservations

---

### 4. Reviews

* Submit customer reviews
* Store ratings
* Display provider feedback

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Uvicorn
* Docker
* Pytest

---

## API Documentation

Run the server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Business Value

Booking APIs are widely used in:

* Healthcare appointment systems
* Salon and beauty services
* Hotel reservation platforms
* Restaurant booking systems
* Fitness and personal training
* Consulting services
* Equipment rental platforms

---

## Learning Outcome

You learned how to:

* Build a RESTful API with FastAPI
* Structure a scalable backend project
* Implement JWT authentication
* Design relational database models
* Manage bookings and provider availability
* Protect endpoints using access tokens
* Document APIs with Swagger


# Day 44 - Web Scraping: Real Estate Prices

## About This Project
This project collects apartment listings from a specified city and neighborhood, allowing you to analyze real estate prices in your area.

## Features
- Fetches listings from specified city/neighborhood
- Cleans and extracts price, square meters, room count data
- Saves data in CSV format
- Provides basic statistics (average price, price per sqm, etc.)

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Enter requested information
- City name (e.g., Istanbul)
- Neighborhood name (e.g., Kadikoy)
- Number of pages to scrape (default: 3)

## Important Note
This project is demonstration only. For real website integration:

1. Update base_url in realestate_scraper.py
2. Modify URL structure in the scrape() method
3. Update HTML selectors (CSS classes) in the scrape() method

## Output
Scraped data is saved in the data/ folder with format:
realestate_Istanbul_Kadikoy_20260113_153045.csv

## Example Output
SUMMARY STATISTICS
----------------------------------------
Total Listings: 45
Average Price: 3,250,000 TRY
Lowest Price: 1,150,000 TRY
Highest Price: 8,900,000 TRY
Average SQM: 95.0 m²
Price per SQM: 34,211 TRY/m²

## Libraries Used
- requests - HTTP requests
- beautifulsoup4 - HTML parsing
- pandas - Data processing and CSV export
- fake-useragent - Random User-Agent generation

## Learning Objectives
- Web scraping fundamentals
- BeautifulSoup HTML parsing
- Data cleaning techniques
- CSV data storage
- Error handling and polite scraping strategies


# Day 45 - Data Visualization Dashboard

## About This Project
This project creates comprehensive sales dashboards using synthetic data with both static and interactive visualizations.

## Features
- Generates synthetic sales and customer data
- Creates static charts using Matplotlib and Seaborn
- Creates interactive dashboards using Plotly
- Includes correlation analysis
- Shows distribution patterns

## Visualizations Generated

### Static Charts (PNG)
1. Monthly Sales Trend
2. Sales Distribution by Region (Pie Chart)
3. Top 10 Products by Revenue
4. Price vs Quantity Scatter Plot
5. Correlation Heatmap
6. Distribution Charts

### Interactive Dashboard (HTML)
- Monthly sales trend with line chart
- Category distribution with pie chart
- Regional performance with bar chart
- Product performance comparison

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Check outputs
- Static charts: output/ folder (PNG files)
- Interactive dashboard: output/interactive_dashboard.html
- Raw data: data/ folder (CSV files)

## Output Files
- static_dashboard.png - Static dashboard with 4 subplots
- interactive_dashboard.html - Interactive Plotly dashboard
- correlation_heatmap.png - Correlation matrix
- distribution_charts.png - Sales distribution visualizations
- sales_data.csv - Generated sales data
- customer_data.csv - Generated customer data

## Libraries Used
- pandas - Data manipulation
- numpy - Numerical operations
- matplotlib - Static visualizations
- seaborn - Statistical visualizations
- plotly - Interactive visualizations

## Learning Objectives
- Creating dashboards with multiple chart types
- Static vs interactive visualization techniques
- Data summarization and aggregation
- Correlation analysis
- Professional data presentation


# Day 46 - SQLite Database

## About This Project
This project demonstrates SQLite database operations with a product management system. It includes CRUD operations, relationships, and data reporting.

## Database Schema
- **products**: Product information (name, category, price, stock)
- **customers**: Customer information (name, email, phone, city)
- **orders**: Order headers (customer, total, status)
- **order_items**: Order details (product, quantity, price)

## Features
- Complete CRUD operations
- Foreign key relationships
- Data export to CSV
- Visual reports
- Sample data generation

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Check outputs
- Database: data/products.db
- CSV exports: output/*.csv
- Charts: output/*.png

## Generated Reports

### CSV Exports
- products_export.csv - All products
- customers_export.csv - All customers
- orders_export.csv - All orders

### Visualizations (PNG)
- products_by_category.png - Bar chart
- price_distribution.png - Histogram
- orders_by_status.png - Pie chart

## Sample Data
The program automatically creates sample data including:
- 10 products in 5 categories
- 8 customers in 8 cities
- 4 sample orders with items
- Various order statuses

## Database Operations Demonstrated
- CREATE TABLE with constraints
- INSERT with foreign keys
- SELECT with JOIN
- UPDATE with conditions
- DELETE with WHERE clauses
- Aggregate functions (COUNT, SUM, AVG)
- GROUP BY and ORDER BY

## Libraries Used
- sqlite3 - Database operations
- pandas - Data processing and export
- matplotlib - Visualization
- seaborn - Styling

## Learning Objectives
- SQLite database operations
- CRUD operations in Python
- Foreign key relationships
- Data export and reporting
- Database visualization

# Day 47 - REST API Consumer

## About This Project
This project demonstrates consuming REST APIs in Python. It fetches real-time exchange rates from ExchangeRate-API and simulates weather data retrieval.

## Features
- Fetch real-time exchange rates
- Extract rates for specific currencies
- Perform currency conversions
- Save data to CSV and JSON
- Display formatted reports

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Check outputs
- CSV reports: output/exchange_rates_*.csv
- JSON data: data/*.json

## API Endpoints Used

### ExchangeRate-API (Free)
- Endpoint: https://api.exchangerate-api.com/v4/latest/{BASE}
- Method: GET
- Response: Exchange rates for all currencies

## Output Files

### CSV Reports
- exchange_rates_USD_*.csv - USD base rates
- exchange_rates_EUR_*.csv - EUR base rates

### JSON Data
- usd_exchange_rates.json - Raw API response
- eur_exchange_rates.json - Raw API response
- weather_demo.json - Demo weather data

## Features Demonstrated
- GET requests with requests library
- JSON response parsing
- Error handling for API calls
- Data extraction and transformation
- CSV and JSON export

## Libraries Used
- requests - HTTP client
- pandas - Data processing and CSV export

## API Documentation
- ExchangeRate-API: https://exchangerate-api.com/documentation
- OpenWeatherMap: https://openweathermap.org/api

## Learning Objectives
- REST API concepts
- Making HTTP requests in Python
- Handling JSON responses
- Error handling for APIs
- Data export and reporting

# Day 48 - Multithreading Image Downloader

## About This Project
This project demonstrates multithreading in Python by downloading images from URLs simultaneously. It compares sequential vs multithreaded performance.

## Features
- Download multiple images from URLs
- Sequential and multithreaded modes
- Performance comparison
- Thread-safe operations
- Error handling

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Select download method
- 1: Sequential (no threading)
- 2: Multithreaded (fast)
- 3: Compare performance

## Image Sources
Images are downloaded from picsum.photos - free placeholder images:
- https://picsum.photos/200/300?random=1

## Threading Concepts Demonstrated
- Creating and starting threads
- Thread synchronization with locks
- Thread-safe data collection
- Performance comparison

## Learning Objectives
- Understanding multithreading in Python
- Parallel vs sequential execution
- Thread safety
- Performance optimization
- Real-world application of threading

## Performance Benefits
Multithreading significantly speeds up I/O-bound operations like downloading images, as the program can download multiple images simultaneously while waiting for network responses.