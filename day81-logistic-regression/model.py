"""
Logistic Regression Model Module
Builds and evaluates logistic regression models
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    roc_auc_score, roc_curve, precision_score, recall_score, f1_score
)
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime


class LogisticRegressionModel:
    """Logistic Regression model wrapper"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
        self.y_pred_proba = None
        self.results = {}
        
        os.makedirs("output", exist_ok=True)
    
    def load_dataset(self, dataset: str = 'breast_cancer', n_samples: int = 1000, 
                     n_features: int = 20, n_classes: int = 2):
        """Load dataset"""
        if dataset == 'breast_cancer':
            data = load_breast_cancer()
            self.X = data.data
            self.y = data.target
            self.feature_names = data.feature_names
            self.target_names = data.target_names
            print(f"[OK] Loaded Breast Cancer dataset")
            print(f"  Samples: {len(self.X)}, Features: {self.X.shape[1]}")
            print(f"  Classes: {self.target_names}")
            
        else:
            self.X, self.y = make_classification(
                n_samples=n_samples,
                n_features=n_features,
                n_informative=n_features // 2,
                n_redundant=0,
                n_classes=n_classes,
                random_state=self.random_state
            )
            self.feature_names = [f'feature_{i+1}' for i in range(n_features)]
            self.target_names = [f'Class_{i}' for i in range(n_classes)]
            print(f"[OK] Generated synthetic dataset")
            print(f"  Samples: {n_samples}, Features: {n_features}, Classes: {n_classes}")
        
        return self.X, self.y
    
    def split_data(self, test_size: float = 0.2):
        """Split data into train and test sets"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=self.random_state, stratify=self.y
        )
        print(f"\n[OK] Data split:")
        print(f"  Train: {len(self.X_train)} samples")
        print(f"  Test: {len(self.X_test)} samples")
        
        self.results['data_split'] = {
            'train_size': len(self.X_train),
            'test_size': len(self.X_test),
            'total_samples': len(self.X)
        }
    
    def scale_data(self):
        """Scale features using StandardScaler"""
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        print("[OK] Data scaled using StandardScaler")
        
        return self.X_train_scaled, self.X_test_scaled
    
    def train(self, C: float = 1.0, max_iter: int = 1000, 
              solver: str = 'lbfgs', penalty: str = 'l2'):
        """Train logistic regression model"""
        self.model = LogisticRegression(
            C=C,
            max_iter=max_iter,
            solver=solver,
            penalty=penalty,
            random_state=self.random_state
        )
        
        self.model.fit(self.X_train_scaled, self.y_train)
        self.y_pred = self.model.predict(self.X_test_scaled)
        self.y_pred_proba = self.model.predict_proba(self.X_test_scaled)
        
        print(f"[OK] Model trained:")
        print(f"  C: {C}, solver: {solver}, penalty: {penalty}")
        print(f"  Training accuracy: {self.model.score(self.X_train_scaled, self.y_train):.4f}")
        
        self.results['model_params'] = {
            'C': C,
            'max_iter': max_iter,
            'solver': solver,
            'penalty': penalty,
            'coef': self.model.coef_.tolist(),
            'intercept': self.model.intercept_.tolist()
        }
        
        return self.model
    
    def evaluate(self):
        """Evaluate model performance"""
        accuracy = accuracy_score(self.y_test, self.y_pred)
        precision = precision_score(self.y_test, self.y_pred, average='weighted')
        recall = recall_score(self.y_test, self.y_pred, average='weighted')
        f1 = f1_score(self.y_test, self.y_pred, average='weighted')
        
        cm = confusion_matrix(self.y_test, self.y_pred)
        
        if len(np.unique(self.y)) == 2:
            roc_auc = roc_auc_score(self.y_test, self.y_pred_proba[:, 1])
        else:
            roc_auc = roc_auc_score(self.y_test, self.y_pred_proba, multi_class='ovr')
        
        report = classification_report(self.y_test, self.y_pred, 
                                       target_names=self.target_names, 
                                       output_dict=True)
        
        self.results['metrics'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc
        }
        
        self.results['confusion_matrix'] = cm.tolist()
        self.results['classification_report'] = report
        
        print("\n[OK] Model Evaluation:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        print(f"  ROC AUC: {roc_auc:.4f}")
        
        return self.results
    
    def cross_validate(self, cv: int = 5):
        """Perform cross-validation"""
        scores = cross_val_score(self.model, self.X_train_scaled, self.y_train, cv=cv)
        
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
    
    def plot_confusion_matrix(self):
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
        plt.savefig('output/confusion_matrix.png')
        plt.close()
        print("[OK] Confusion matrix saved to: output/confusion_matrix.png")
    
    def plot_feature_importance(self, top_n: int = 10):
        """Plot feature importance (coefficients)"""
        if hasattr(self.model, 'coef_'):
            if len(self.model.coef_) == 1 or self.model.coef_.shape[0] == 1:
                coefficients = self.model.coef_[0]
            else:
                # For multiclass, use mean absolute coefficients
                coefficients = np.mean(np.abs(self.model.coef_), axis=0)
            
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'coefficient': coefficients
            }).sort_values('coefficient', key=abs, ascending=False)
            
            plt.figure(figsize=(10, 8))
            top_features = feature_importance.head(top_n)
            colors = ['red' if x < 0 else 'green' for x in top_features['coefficient']]
            plt.barh(top_features['feature'], top_features['coefficient'], color=colors)
            plt.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
            plt.xlabel('Coefficient')
            plt.title(f'Top {top_n} Feature Coefficients')
            plt.tight_layout()
            plt.savefig('output/feature_importance.png')
            plt.close()
            print(f"[OK] Feature importance saved to: output/feature_importance.png")
            
            self.results['feature_importance'] = feature_importance.head(top_n).to_dict()
    
    def plot_roc_curve(self):
        """Plot ROC curve (binary classification only)"""
        if len(np.unique(self.y)) != 2:
            print("[INFO] ROC curve only for binary classification")
            return
        
        fpr, tpr, _ = roc_curve(self.y_test, self.y_pred_proba[:, 1])
        roc_auc = roc_auc_score(self.y_test, self.y_pred_proba[:, 1])
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('output/roc_curve.png')
        plt.close()
        print(f"[OK] ROC curve saved to: output/roc_curve.png")
    
    def save_results(self, filename: str = "results.json"):
        """Save results to JSON file"""
        self.results['timestamp'] = datetime.now().isoformat()
        self.results['features'] = self.feature_names
        self.results['target_names'] = self.target_names
        
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        with open(f"output/{filename}", 'w') as f:
            json.dump(self.results, f, indent=2, default=convert_to_serializable)
        
        print(f"[OK] Results saved to: output/{filename}")
    
    def print_summary(self):
        """Print model summary"""
        print("\n" + "="*50)
        print("MODEL SUMMARY")
        print("="*50)
        
        print(f"\nDataset: {self.X.shape[0]} samples, {self.X.shape[1]} features")
        print(f"Classes: {self.target_names}")
        
        if 'metrics' in self.results:
            print("\nPerformance Metrics:")
            for key, value in self.results['metrics'].items():
                print(f"  {key}: {value:.4f}")
        
        if 'cross_validation' in self.results:
            print(f"\nCross-Validation: {self.results['cross_validation']['cv_mean']:.4f} (±{self.results['cross_validation']['cv_std']:.4f})")
        
        print("="*50)
