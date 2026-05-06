"""
DAY 30 - Month 2 Blueprint (Treasury AI Roadmap)

This project does not perform data analysis.
It defines the transition from EDA to Machine Learning systems.

Goal:
To document the learning path toward building predictive AI systems for treasury operations.
"""


def print_month2_blueprint() -> None:
    """Prints structured Month 2 roadmap for ML transition."""

    roadmap = {
        "Week 5 - ML Foundations": [
            "Introduction to Scikit-Learn",
            "Regression Models (Linear Regression)",
            "Classification Models (Logistic Regression)",
            "fit() and predict() workflow"
        ],
        "Week 6 - Advanced ML": [
            "Random Forests",
            "Gradient Boosting (XGBoost concept)",
            "Hyperparameter Tuning",
            "Feature Importance Analysis"
        ],
        "Week 7 - NLP & LLMs": [
            "Text preprocessing (tokenization, cleaning)",
            "TF-IDF and Word Embeddings basics",
            "Introduction to Large Language Models (LLMs)",
            "Retrieval-Augmented Generation (RAG concept)"
        ],
        "Week 8 - Model Evaluation": [
            "Confusion Matrix",
            "Precision, Recall, F1 Score",
            "ROC-AUC",
            "Business impact evaluation (risk vs cost)"
        ]
    }

    print("\nMONTH 2: TREASURY AI ROADMAP\n")
    print("=" * 50)

    for week, topics in roadmap.items():
        print(f"\n{week}")
        print("-" * len(week))
        for topic in topics:
            print(f"• {topic}")

    print("\n" + "=" * 50)
    print("\nVision: Transition from Data Analyst → AI Treasury Engineer")


if __name__ == "__main__":
    print_month2_blueprint()