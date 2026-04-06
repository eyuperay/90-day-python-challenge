# Create a list of products
products: list[str] = ["Laptop", "Mouse", "Keyboard", "Monitor", "Tablet"]

# Add a new product to the end of the list
products.append("Headphones")

# Remove the second item from the list (index 1)
del products[1]

# Print the updated product list
print("Updated Products List:", products)

# Use slicing to get the first 3 products
popular_products: list[str] = products[:3]

print("Popular Products:", popular_products)

# Create a dictionary for stock information
# Keys represent product names, values represent stock quantities
stock_info: dict[str, int] = {
    "Laptop": 10,
    "Keyboard": 25,
    "Monitor": 8,
    "Tablet": 15,
    "Headphones": 20
}

# Calculate total stock using a loop
total_stock: int = 0

for product in stock_info:
    total_stock += stock_info[product]

print("Total Stock:", total_stock)

# Use list comprehension to filter products
# Select products with names longer than 5 characters
long_name_products: list[str] = [p for p in products if len(p) > 5]

print("Products with name longer than 5 characters:", long_name_products)