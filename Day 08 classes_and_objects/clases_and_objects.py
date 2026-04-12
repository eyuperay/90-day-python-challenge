# Day 08 - Classes and Objects

class DataSource:
    def __init__(self, source_name: str, file_type: str, row_count: int):
        self.source_name = source_name
        self.file_type = file_type
        self.row_count = row_count

    def describe(self):
        print("\nData Source Information")
        print("----------------------------")
        print(f"Source Name : {self.source_name}")
        print(f"File Type   : {self.file_type}")
        print(f"Row Count   : {self.row_count}")
        print("----------------------------")

    def update_row_count(self, new_count: int):
        print(f"\nUpdating row count for {self.source_name}...")
        print(f"Old Row Count: {self.row_count}")
        self.row_count = new_count
        print(f"New Row Count: {self.row_count}")


# Create objects
customer_data = DataSource("Customer List", "CSV", 1500)
sales_data = DataSource("Sales Data", "JSON", 3200)


# Display initial information
customer_data.describe()
sales_data.describe()

# Update row counts
customer_data.update_row_count(1550)
sales_data.update_row_count(3300)

# Display updated information
customer_data.describe()
sales_data.describe()