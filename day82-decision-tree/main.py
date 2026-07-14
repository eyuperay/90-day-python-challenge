#!/usr/bin/env python3
"""
Day 82 - Decision Tree Visualization
Machine Learning with Decision Trees
"""

import os
from model import DecisionTreeModel


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_iris():
    """Demonstrate on Iris dataset"""
    print_section("1. IRIS DATASET")
    
    model = DecisionTreeModel(random_state=42)
    model.load_dataset('iris')
    model.split_data(test_size=0.2)
    model.train(max_depth=4, criterion='gini')
    model.evaluate()
    model.cross_validate(cv=5)
    
    # Visualizations
    model.plot_tree('iris_tree.png', max_depth=4)
    model.plot_tree_graphviz('iris_tree')
    model.plot_feature_importance('iris_feature_importance.png')
    model.plot_confusion_matrix('iris_confusion_matrix.png')
    
    # Compare depths
    model.compare_depths([1, 2, 3, 4, 5, 7, 10])
    
    model.save_results('iris_results.json')
    model.print_summary()
    
    return model


def demo_wine():
    """Demonstrate on Wine dataset"""
    print_section("2. WINE DATASET")
    
    model = DecisionTreeModel(random_state=42)
    model.load_dataset('wine')
    model.split_data(test_size=0.2)
    model.train(max_depth=5, criterion='gini')
    model.evaluate()
    model.cross_validate(cv=5)
    
    # Visualizations
    model.plot_tree('wine_tree.png', max_depth=5)
    model.plot_tree_graphviz('wine_tree')
    model.plot_feature_importance('wine_feature_importance.png')
    model.plot_confusion_matrix('wine_confusion_matrix.png')
    
    # Compare depths
    model.compare_depths([1, 2, 3, 4, 5, 7, 10])
    
    model.save_results('wine_results.json')
    model.print_summary()
    
    return model


def demo_synthetic():
    """Demonstrate on synthetic data"""
    print_section("3. SYNTHETIC DATASET")
    
    model = DecisionTreeModel(random_state=42)
    model.load_dataset('synthetic')
    model.split_data(test_size=0.2)
    model.train(max_depth=4, criterion='gini')
    model.evaluate()
    model.cross_validate(cv=5)
    
    # Visualizations
    model.plot_tree('synthetic_tree.png', max_depth=4)
    model.plot_tree_graphviz('synthetic_tree')
    model.plot_feature_importance('synthetic_feature_importance.png')
    model.plot_confusion_matrix('synthetic_confusion_matrix.png')
    
    # Compare depths
    model.compare_depths([1, 2, 3, 4, 5, 7, 10])
    
    model.save_results('synthetic_results.json')
    model.print_summary()
    
    return model


def main():
    print("=" * 60)
    print("DAY 82 - DECISION TREE VISUALIZATION")
    print("=" * 60 + "\n")
    
    print("This demo shows decision tree models on different datasets.\n")
    
    # Run demos
    demo_iris()
    demo_wine()
    demo_synthetic()
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for visualizations")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
