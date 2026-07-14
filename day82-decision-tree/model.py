"""
Decision Tree Model Module
Builds and visualizes decision tree models
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine, make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    precision_score, recall_score, f1_score
)
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime

# ==================== GRAPHVIZ PATH (MANUAL) ====================
import os
import sys

# Graphviz bin dizinini ekle
GRAPHVIZ_PATH = r"C:\Program Files\Graphviz\bin"
if os.path.exists(GRAPHVIZ_PATH):
    os.environ["PATH"] = GRAPHVIZ_PATH + os.pathsep + os.environ.get("PATH", "")
    print(f"[INFO] Graphviz path added: {GRAPHVIZ_PATH}")
else:
    print(f"[WARNING] Graphviz not found at: {GRAPHVIZ_PATH}")
# ================================================================

try:
    import graphviz
    HAS_GRAPHVIZ = True
    print("[INFO] Graphviz module loaded successfully")
except ImportError as e:
    HAS_GRAPHVIZ = False
    print(f"[INFO] Graphviz not installed: {e}")


class DecisionTreeModel:
    """Decision Tree model wrapper with visualization"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
        self.results = {}
        self.feature_names = None
        self.target_names = None
        
        os.makedirs("output", exist_ok=True)
    
    def load_dataset(self, dataset: str = 'iris'):
        """Load dataset"""
        if dataset == 'iris':
            data = load_iris()
            self.X = data.data
            self.y = data.target
            self.feature_names = data.feature_names
            self.target_names = data.target_names
            print(f"[OK] Loaded Iris dataset")
            print(f"  Samples: {len(self.X)}, Features: {self.X.shape[1]}")
            print(f"  Classes: {self.target_names}")
            
        elif dataset == 'wine':
            data = load_wine()
            self.X = data.data
            self.y = data.target
            self.feature_names = data.feature_names
            self.target_names = data.target_names
            print(f"[OK] Loaded Wine dataset")
            print(f"  Samples: {len(self.X)}, Features: {self.X.shape[1]}")
            print(f"  Classes: {self.target_names}")
            
        else:
            self.X, self.y = make_classification(
                n_samples=500,
                n_features=4,
                n_informative=3,
                n_redundant=0,
                n_classes=3,
                random_state=self.random_state
            )
            self.feature_names = [f'feature_{i+1}' for i in range(4)]
            self.target_names = [f'Class_{i}' for i in range(3)]
            print(f"[OK] Generated synthetic dataset")
            print(f"  Samples: 500, Features: 4, Classes: 3")
        
        return self.X, self.y
    
    def split_data(self, test_size: float = 0.2):
        """Split data"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=self.random_state, stratify=self.y
        )
        print(f"\n[OK] Data split:")
        print(f"  Train: {len(self.X_train)} samples")
        print(f"  Test: {len(self.X_test)} samples")
    
    def train(self, max_depth: int = 5, min_samples_split: int = 2,
              min_samples_leaf: int = 1, criterion: str = 'gini'):
        """Train decision tree"""
        self.model = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            criterion=criterion,
            random_state=self.random_state
        )
        
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)
        
        print(f"\n[OK] Model trained:")
        print(f"  max_depth: {max_depth}")
        print(f"  min_samples_split: {min_samples_split}")
        print(f"  min_samples_leaf: {min_samples_leaf}")
        print(f"  criterion: {criterion}")
        print(f"  Training accuracy: {self.model.score(self.X_train, self.y_train):.4f}")
        
        self.results['model_params'] = {
            'max_depth': max_depth,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf,
            'criterion': criterion,
            'feature_importances': self.model.feature_importances_.tolist()
        }
        
        return self.model
    
    def evaluate(self):
        """Evaluate model"""
        accuracy = accuracy_score(self.y_test, self.y_pred)
        precision = precision_score(self.y_test, self.y_pred, average='weighted')
        recall = recall_score(self.y_test, self.y_pred, average='weighted')
        f1 = f1_score(self.y_test, self.y_pred, average='weighted')
        
        cm = confusion_matrix(self.y_test, self.y_pred)
        report = classification_report(self.y_test, self.y_pred, 
                                       target_names=self.target_names, 
                                       output_dict=True)
        
        self.results['metrics'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        self.results['confusion_matrix'] = cm.tolist()
        self.results['classification_report'] = report
        
        print("\n[OK] Model Evaluation:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        
        return self.results
    
    def cross_validate(self, cv: int = 5):
        """Cross-validation"""
        scores = cross_val_score(self.model, self.X_train, self.y_train, cv=cv)
        
        self.results['cross_validation'] = {
            'cv_scores': scores.tolist(),
            'cv_mean': scores.mean(),
            'cv_std': scores.std()
        }
        
        print(f"\n[OK] Cross-Validation ({cv}-fold):")
        print(f"  Scores: {scores}")
        print(f"  Mean: {scores.mean():.4f}")
        print(f"  Std: {scores.std():.4f}")
        
        return scores
    
    def plot_tree(self, filename: str = "decision_tree.png", 
                  max_depth: int = 5, figsize: tuple = (20, 12)):
        """Plot decision tree"""
        plt.figure(figsize=figsize)
        plot_tree(
            self.model,
            feature_names=self.feature_names,
            class_names=self.target_names,
            filled=True,
            rounded=True,
            fontsize=8,
            max_depth=max_depth,
            proportion=True,
            impurity=False
        )
        plt.title(f'Decision Tree (max_depth={max_depth})')
        plt.tight_layout()
        plt.savefig(f'output/{filename}', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"[OK] Decision tree saved to: output/{filename}")
    
    def plot_tree_graphviz(self, filename: str = "decision_tree"):
        """Export tree to Graphviz format"""
        if not HAS_GRAPHVIZ:
            print("[INFO] Graphviz not available. Skipping Graphviz export.")
            return None
        
        try:
            dot_data = export_graphviz(
                self.model,
                feature_names=self.feature_names,
                class_names=self.target_names,
                filled=True,
                rounded=True,
                special_characters=True,
                proportion=True,
                impurity=False,
                max_depth=5
            )
            
            # Önce PATH'i kontrol et
            import subprocess
            try:
                subprocess.run(['dot', '-V'], capture_output=True, check=True)
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                print(f"[WARNING] Graphviz 'dot' executable not found: {e}")
                print("[INFO] Skipping Graphviz export.")
                return None
            
            graph = graphviz.Source(dot_data)
            graph.render(f'output/{filename}', format='png', cleanup=True)
            print(f"[OK] Graphviz tree saved to: output/{filename}.png")
            return graph
        except Exception as e:
            print(f"[INFO] Graphviz export failed: {e}")
            return None
    
    def plot_feature_importance(self, filename: str = "feature_importance.png"):
        """Plot feature importance"""
        importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 8))
        plt.barh(importance['feature'], importance['importance'], color='teal')
        plt.xlabel('Importance')
        plt.title('Feature Importance')
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Feature importance saved to: output/{filename}")
        
        return importance
    
    def plot_confusion_matrix(self, filename: str = "confusion_matrix.png"):
        """Plot confusion matrix"""
        cm = confusion_matrix(self.y_test, self.y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.target_names,
                    yticklabels=self.target_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Confusion matrix saved to: output/{filename}")
    
    def compare_depths(self, depths: list = [1, 3, 5, 7, 10]):
        """Compare different tree depths"""
        print("\n[OK] Comparing different tree depths:")
        print("-"*50)
        
        results = []
        for depth in depths:
            self.train(max_depth=depth)
            train_acc = self.model.score(self.X_train, self.y_train)
            test_acc = self.model.score(self.X_test, self.y_test)
            results.append({
                'depth': depth,
                'train_accuracy': train_acc,
                'test_accuracy': test_acc
            })
            print(f"  Depth {depth:2d}: Train={train_acc:.4f}, Test={test_acc:.4f}")
        
        # Plot comparison
        plt.figure(figsize=(10, 6))
        plt.plot(depths, [r['train_accuracy'] for r in results], 'b-o', label='Train')
        plt.plot(depths, [r['test_accuracy'] for r in results], 'r-o', label='Test')
        plt.xlabel('Tree Depth')
        plt.ylabel('Accuracy')
        plt.title('Accuracy vs Tree Depth')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('output/depth_comparison.png')
        plt.close()
        print(f"[OK] Depth comparison saved to: output/depth_comparison.png")
        
        return results
    
    def save_results(self, filename: str = "results.json"):
        """Save results"""
        self.results['timestamp'] = datetime.now().isoformat()
        self.results['features'] = self.feature_names
        self.results['target_names'] = self.target_names
        
        def convert(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        with open(f"output/{filename}", 'w') as f:
            json.dump(self.results, f, indent=2, default=convert)
        
        print(f"[OK] Results saved to: output/{filename}")
    
    def print_summary(self):
        """Print summary"""
        print("\n" + "="*50)
        print("MODEL SUMMARY")
        print("="*50)
        
        print(f"\nDataset: {self.X.shape[0]} samples, {self.X.shape[1]} features")
        print(f"Classes: {self.target_names}")
        
        print("\nFeature Importance:")
        for name, imp in zip(self.feature_names, self.model.feature_importances_):
            print(f"  {name}: {imp:.4f}")
        
        if 'metrics' in self.results:
            print("\nPerformance Metrics:")
            for key, value in self.results['metrics'].items():
                print(f"  {key}: {value:.4f}")
        
        if 'cross_validation' in self.results:
            print(f"\nCross-Validation: {self.results['cross_validation']['cv_mean']:.4f} (±{self.results['cross_validation']['cv_std']:.4f})")
        
        print("="*50)
