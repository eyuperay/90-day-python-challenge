"""
Purpose of this script:
Demonstrates polymorphism using a base metric class and multiple derived classes
that override the same method with different behaviors.
"""


class Metric:
    """
    Base metric class.
    """

    def calculate(self) -> None:
        """
        Default calculation method.
        """
        print("Metric is being calculated...")


class AccuracyMetric(Metric):
    """
    Accuracy metric implementation.
    """

    def calculate(self) -> None:
        """
        Calculates accuracy metric.
        """
        print("Accuracy is being calculated...")


class PrecisionMetric(Metric):
    """
    Precision metric implementation.
    """

    def calculate(self) -> None:
        """
        Calculates precision metric.
        """
        print("Precision is being calculated...")


if __name__ == "__main__":
    metrics_list = [
        AccuracyMetric(),
        PrecisionMetric(),
        Metric()
    ]

    for metric in metrics_list:
        metric.calculate()