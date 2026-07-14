#!/usr/bin/env python3
"""
Day 83 - Neural Network
Deep Learning with TensorFlow/Keras
"""

import os
from model import NeuralNetworkModel


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_digits():
    """Demonstrate on Digits dataset (10 classes)"""
    print_section("1. DIGITS DATASET (10 CLASSES)")
    
    model = NeuralNetworkModel(random_state=42)
    model.load_dataset('digits')
    model.split_data(test_size=0.2)
    model.scale_data()
    
    # Build and train
    model.build_model(layers_list=[128, 64, 32], activation='relu')
    model.train(epochs=100, early_stopping=True, patience=10)
    
    # Evaluate
    model.evaluate_model()
    
    # Visualizations
    model.plot_training_history('digits_training_history.png')
    model.plot_confusion_matrix('digits_confusion_matrix.png')
    
    # Compare architectures
    architectures = [
        [64, 32],
        [128, 64, 32],
        [128, 64, 32, 16]
    ]
    model.compare_architectures(architectures)
    
    model.save_results('digits_results.json')
    model.print_summary()
    
    return model


def demo_synthetic():
    """Demonstrate on synthetic dataset (2 classes)"""
    print_section("2. SYNTHETIC DATASET (2 CLASSES)")
    
    model = NeuralNetworkModel(random_state=42)
    model.load_dataset('synthetic', n_samples=2000, n_features=10, n_classes=2)
    model.split_data(test_size=0.2)
    model.scale_data()
    
    # Build and train
    model.build_model(layers_list=[64, 32], activation='relu')
    model.train(epochs=50, early_stopping=True, patience=5)
    
    # Evaluate
    model.evaluate_model()
    
    # Visualizations
    model.plot_training_history('synthetic_training_history.png')
    model.plot_confusion_matrix('synthetic_confusion_matrix.png')
    
    # Compare architectures
    architectures = [
        [32, 16],
        [64, 32],
        [128, 64]
    ]
    model.compare_architectures(architectures)
    
    model.save_results('synthetic_results.json')
    model.print_summary()
    
    return model


def demo_multiclass():
    """Demonstrate on multiclass synthetic dataset (3 classes)"""
    print_section("3. MULTICLASS SYNTHETIC DATASET (3 CLASSES)")
    
    model = NeuralNetworkModel(random_state=42)
    model.load_dataset('synthetic', n_samples=1500, n_features=8, n_classes=3)
    model.split_data(test_size=0.2)
    model.scale_data()
    
    # Build and train
    model.build_model(layers_list=[64, 32, 16], activation='relu')
    model.train(epochs=50, early_stopping=True, patience=5)
    
    # Evaluate
    model.evaluate_model()
    
    # Visualizations
    model.plot_training_history('multiclass_training_history.png')
    model.plot_confusion_matrix('multiclass_confusion_matrix.png')
    
    model.save_results('multiclass_results.json')
    model.print_summary()
    
    return model


def main():
    print("=" * 60)
    print("DAY 83 - NEURAL NETWORK")
    print("=" * 60 + "\n")
    
    print("This demo shows neural networks on different datasets.\n")
    print("[WARNING] TensorFlow installation may take a few minutes.\n")
    
    # Run demos
    demo_digits()
    demo_synthetic()
    demo_multiclass()
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for results and plots")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
