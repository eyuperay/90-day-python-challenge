from processors import CSVProcessor, JSONProcessor
from decorators import time_logger


@time_logger
def process_pipeline(processor) -> None:
    for item in processor.read_data():
        print("Processing:", item)


if __name__ == "__main__":

    csv_processor = CSVProcessor("input.csv")
    json_processor = JSONProcessor("input.json")

    print(csv_processor)
    process_pipeline(csv_processor)
    print("Processed records:", len(csv_processor))

    print("\n-------------------\n")

    print(json_processor)
    process_pipeline(json_processor)
    print("Processed records:", len(json_processor))