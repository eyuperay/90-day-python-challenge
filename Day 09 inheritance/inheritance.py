"""
Purpose of this script:
This script demonstrates the concept of inheritance in Python by creating
a base model class and extending it into specialized AI model classes.
Each derived class customizes the training behavior.
"""


class BaseModel:
    """
    Base class for all AI models.
    """

    def __init__(self, model_name: str, version: str) -> None:
        self.model_name = model_name
        self.version = version

    def train(self) -> None:
        """
        Simulates training process.
        """
        print("Model is being trained...")


class NLPModel(BaseModel):
    """
    NLP model class inheriting from BaseModel.
    """

    def __init__(self, model_name: str, version: str, language: str) -> None:
        super().__init__(model_name, version)
        self.language = language

    def train(self) -> None:
        """
        Overridden training method for NLP models.
        """
        print(f"NLP model is being trained for {self.language}...")


class VisionModel(BaseModel):
    """
    Vision model class inheriting from BaseModel.
    """

    def __init__(self, model_name: str, version: str, resolution: str) -> None:
        super().__init__(model_name, version)
        self.resolution = resolution


# Example usage
if __name__ == "__main__":
    nlp_model = NLPModel("TextAnalyzer", "1.0", "English")
    vision_model = VisionModel("ImageClassifier", "2.1", "1080p")

    print("NLP Model:")
    print(nlp_model.model_name, nlp_model.version, nlp_model.language)
    nlp_model.train()

    print("\nVision Model:")
    print(vision_model.model_name, vision_model.version, vision_model.resolution)
    vision_model.train()