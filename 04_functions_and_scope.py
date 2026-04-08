

# Global variable
global_counter = 0


def clean_text(text: str) -> str:
    """Remove leading/trailing spaces and convert text to lowercase."""
    return text.strip().lower()


def calculate_tax(price: float, tax_rate: float = 0.18) -> float:
    """Calculate total price including tax."""
    return price * (1 + tax_rate)


def is_outlier(value: float, threshold: float = 100.0) -> bool:
    """Return True if value exceeds the given threshold."""
    return value > threshold


def scope_demo():
    """Demonstrate global vs local variable behavior."""
    local_variable = "I am local"

    print("Global counter:", global_counter)
    print("Local variable inside function:", local_variable)


# TEST / USAGE 

# 1. clean_text
text = "   Hello World   "
cleaned = clean_text(text)
print("Cleaned text:", cleaned)

# 2. calculate_tax
price_with_tax = calculate_tax(100)
print("Price with tax:", price_with_tax)

# 3. is_outlier
value = 150
print("Is outlier:", is_outlier(value))

# 4. scope demo
scope_demo()

# print(local_variable)
# ❌ This will raise an error because:
# local_variable is defined inside the function (local scope)
# and cannot be accessed outside the function.
