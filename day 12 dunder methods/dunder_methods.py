"""
Purpose of this script:
This script demonstrates the use of special (dunder) methods in Python
by creating a custom Dataset class with enhanced behavior.
"""


class Dataset:
    """
    Custom dataset class for handling collections of data.
    """

    def __init__(self, data: list, name: str) -> None:
        self.data = data
        self.name = name

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the dataset.
        """
        return f"Dataset: {self.name} ({len(self.data)} records)"

    def __len__(self) -> int:
        """
        Returns the number of records in the dataset.
        """
        return len(self.data)

    def __add__(self, other: "Dataset") -> "Dataset":
        """
        Combines two datasets into a new dataset.
        """
        combined_data = self.data + other.data
        combined_name = f"{self.name} + {other.name}"
        return Dataset(combined_data, combined_name)


# Example usage
if __name__ == "__main__":
    dataset1 = Dataset([1, 2, 3], "Dataset A")
    dataset2 = Dataset([4, 5, 6, 7], "Dataset B")

    combined_dataset = dataset1 + dataset2

    print(dataset1)
    print(dataset2)
    print(combined_dataset)

    print("Total records in combined dataset:", len(combined_dataset))