#!/usr/bin/env python3
"""
Day 81 - Logistic Regression
Machine Learning with Logistic Regression
"""

import os
import numpy as np
import pandas as pd
from model import LogisticRegressionModel


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_breast_cancer():
    """Demonstrate logistic regression on breast cancer dataset"""
    print_section("1. BREAST CANCER DATASET")
    
    # Create model
    model = LogisticRegressionModel(random_state=42)
    
    # Load data
    model.load_dataset('breast_cancer')
    
    # Split data
    model.split_data(test_size=0.2)
    
    # Scale data
    model.scale_data()
    
    # Train model
    model.train(C=1.0, solver='lbfgs')
    
    # Evaluate
    model.evaluate()
    
    # Cross-validate
    model.cross_validate(cv=5)
    
    # Plots
    model.plot_confusion_matrix()
    model.plot_roc_curve()
    model.plot_feature_importance(top_n=10)
    
    # Save results
    model.save_results('breast_cancer_results.json')
    
    # Summary
    model.print_summary()
    
    return model


def demo_synthetic_data():
    """Demonstrate logistic regression on synthetic data"""
    print_section("2. SYNTHETIC DATASET")
    
    # Create model
    model = LogisticRegressionModel(random_state=42)
    
    # Load data
    model.load_dataset('synthetic', n_samples=1000, n_features=10, n_classes=2)
    
    # Split data
    model.split_data(test_size=0.2)
    
    # Scale data
    model.scale_data()
    
    # Train model (try different C)
    print("\nTrying different C values...")
    for C in [0.01, 0.1, 1.0, 10.0, 100.0]:
        model.train(C=C, solver='lbfgs', max_iter=1000)
        accuracy = model.model.score(model.X_test_scaled, model.y_test)
        print(f"  C={C:.2f}: Test accuracy = {accuracy:.4f}")
    
    # Train with best C
    model.train(C=1.0, solver='lbfgs')
    
    # Evaluate
    model.evaluate()
    
    # Cross-validate
    model.cross_validate(cv=5)
    
    # Plots
    model.plot_confusion_matrix()
    model.plot_roc_curve()
    model.plot_feature_importance(top_n=10)
    
    # Save results
    model.save_results('synthetic_results.json')
    
    # Summary
    model.print_summary()
    
    return model


def demo_multiclass():
    """Demonstrate logistic regression on multiclass data"""
    print_section("3. MULTICLASS CLASSIFICATION")
    
    # Create model
    model = LogisticRegressionModel(random_state=42)
    
    # Load data
    model.load_dataset('synthetic', n_samples=1000, n_features=10, n_classes=3)
    
    # Split data
    model.split_data(test_size=0.2)
    
    # Scale data
    model.scale_data()
    
    # Train model
    model.train(C=1.0, solver='lbfgs', max_iter=1000)
    
    # Evaluate
    model.evaluate()
    
    # Cross-validate
    model.cross_validate(cv=5)
    
    # Plots
    model.plot_confusion_matrix()
    model.plot_feature_importance(top_n=10)
    
    # Save results
    model.save_results('multiclass_results.json')
    
    # Summary
    model.print_summary()
    
    return model


def main():
    print("=" * 60)
    print("DAY 81 - LOGISTIC REGRESSION")
    print("=" * 60 + "\n")
    
    print("This demo shows logistic regression on different datasets.\n")
    
    # Run demos
    demo_breast_cancer()
    demo_synthetic_data()
    demo_multiclass()
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for results and plots")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
