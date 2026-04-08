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