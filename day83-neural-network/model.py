"""
Neural Network Model Module
Builds and trains neural networks using TensorFlow/Keras
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers, Sequential
from tensorflow.keras.callbacks import EarlyStopping
import json
import os
from datetime import datetime


class NeuralNetworkModel:
    """Neural Network model wrapper using TensorFlow/Keras"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.history = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
        self.y_pred_proba = None
        self.results = {}
        
        os.makedirs("output", exist_ok=True)
        np.random.seed(random_state)
    
    def load_dataset(self, dataset: str = 'digits', n_samples: int = 1000,
                     n_features: int = 10, n_classes: int = 2):
        """Load dataset"""
        if dataset == 'digits':
            data = load_digits()
            self.X = data.data
            self.y = data.target
            self.n_classes = 10
            self.feature_names = [f'pixel_{i}' for i in range(self.X.shape[1])]
            self.target_names = [str(i) for i in range(10)]
            print(f"[OK] Loaded Digits dataset")
            print(f"  Samples: {len(self.X)}, Features: {self.X.shape[1]}")
            print(f"  Classes: 10 (digits 0-9)")
            
        else:  # synthetic
            self.X, self.y = make_classification(
                n_samples=n_samples,
                n_features=n_features,
                n_informative=n_features - 2,
                n_redundant=0,
                n_classes=n_classes,
                random_state=self.random_state
            )
            self.n_classes = n_classes
            self.feature_names = [f'feature_{i+1}' for i in range(n_features)]
            self.target_names = [f'Class_{i}' for i in range(n_classes)]
            print(f"[OK] Generated synthetic dataset")
            print(f"  Samples: {n_samples}, Features: {n_features}, Classes: {n_classes}")
        
        return self.X, self.y
    
    def split_data(self, test_size: float = 0.2):
        """Split data"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=self.random_state, stratify=self.y
        )
        print(f"\n[OK] Data split:")
        print(f"  Train: {len(self.X_train)} samples")
        print(f"  Test: {len(self.X_test)} samples")
    
    def scale_data(self):
        """Scale features"""
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        print("[OK] Data scaled using StandardScaler")
    
    def build_model(self, layers_list: list = None, activation: str = 'relu',
                    dropout_rate: float = 0.2):
        """Build neural network model"""
        if layers_list is None:
            layers_list = [64, 32]
        
        model = Sequential()
        
        # Input layer
        model.add(layers.Dense(layers_list[0], activation=activation, 
                               input_shape=(self.X_train.shape[1],)))
        model.add(layers.Dropout(dropout_rate))
        
        # Hidden layers
        for units in layers_list[1:]:
            model.add(layers.Dense(units, activation=activation))
            model.add(layers.Dropout(dropout_rate))
        
        # Output layer
        if self.n_classes == 2:
            model.add(layers.Dense(1, activation='sigmoid'))
            loss = 'binary_crossentropy'
        else:
            model.add(layers.Dense(self.n_classes, activation='softmax'))
            loss = 'sparse_categorical_crossentropy'
        
        model.compile(
            optimizer='adam',
            loss=loss,
            metrics=['accuracy']
        )
        
        self.model = model
        self.model.summary()
        
        self.results['model_architecture'] = {
            'layers': layers_list,
            'activation': activation,
            'dropout_rate': dropout_rate,
            'n_classes': self.n_classes
        }
        
        return model
    
    def train(self, epochs: int = 100, batch_size: int = 32,
              validation_split: float = 0.2, early_stopping: bool = True,
              patience: int = 10):
        """Train the model"""
        callbacks = []
        
        if early_stopping:
            callbacks.append(
                EarlyStopping(
                    monitor='val_loss',
                    patience=patience,
                    restore_best_weights=True,
                    verbose=1
                )
            )
        
        self.history = self.model.fit(
            self.X_train, self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate
        train_loss, train_acc = self.model.evaluate(self.X_train, self.y_train, verbose=0)
        test_loss, test_acc = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        
        self.y_pred = self.model.predict(self.X_test)
        if self.n_classes == 2:
            self.y_pred_class = (self.y_pred > 0.5).astype(int).flatten()
            self.y_pred_proba = self.y_pred
        else:
            self.y_pred_class = np.argmax(self.y_pred, axis=1)
            self.y_pred_proba = self.y_pred
        
        self.results['training'] = {
            'train_loss': float(train_loss),
            'train_accuracy': float(train_acc),
            'test_loss': float(test_loss),
            'test_accuracy': float(test_acc),
            'epochs_trained': len(self.history.history['loss'])
        }
        
        print(f"\n[OK] Model trained:")
        print(f"  Train Accuracy: {train_acc:.4f}")
        print(f"  Test Accuracy: {test_acc:.4f}")
        
        return self.history
    
    def plot_training_history(self, filename: str = "training_history.png"):
        """Plot training history"""
        if self.history is None:
            print("[ERROR] Model not trained yet")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Loss
        ax1.plot(self.history.history['loss'], label='Train Loss')
        ax1.plot(self.history.history['val_loss'], label='Validation Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.set_title('Training and Validation Loss')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Accuracy
        ax2.plot(self.history.history['accuracy'], label='Train Accuracy')
        ax2.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.set_title('Training and Validation Accuracy')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Training history saved to: output/{filename}")
    
    def plot_confusion_matrix(self, filename: str = "confusion_matrix.png"):
        """Plot confusion matrix"""
        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
        
        cm = confusion_matrix(self.y_test, self.y_pred_class)
        
        plt.figure(figsize=(10, 8))
        disp = ConfusionMatrixDisplay(cm, display_labels=self.target_names)
        disp.plot(cmap='Blues', values_format='d')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Confusion matrix saved to: output/{filename}")
    
    def evaluate_model(self):
        """Evaluate model and print metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
        
        accuracy = accuracy_score(self.y_test, self.y_pred_class)
        precision = precision_score(self.y_test, self.y_pred_class, average='weighted')
        recall = recall_score(self.y_test, self.y_pred_class, average='weighted')
        f1 = f1_score(self.y_test, self.y_pred_class, average='weighted')
        
        report = classification_report(self.y_test, self.y_pred_class, 
                                       target_names=self.target_names, 
                                       output_dict=True)
        
        self.results['metrics'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        self.results['classification_report'] = report
        
        print("\n[OK] Model Evaluation:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1 Score: {f1:.4f}")
        
        return self.results
    
    def compare_architectures(self, architectures: list):
        """Compare different model architectures"""
        print("\n[OK] Comparing different architectures:")
        print("-"*60)
        
        results = []
        original_model = self.model
        original_history = self.history
        
        for layers in architectures:
            print(f"\nTesting: {layers}")
            self.build_model(layers_list=layers)
            self.train(epochs=50, early_stopping=True, patience=5)
            
            train_acc = self.model.evaluate(self.X_train, self.y_train, verbose=0)[1]
            test_acc = self.model.evaluate(self.X_test, self.y_test, verbose=0)[1]
            
            results.append({
                'layers': layers,
                'train_accuracy': train_acc,
                'test_accuracy': test_acc
            })
            
            print(f"  Train: {train_acc:.4f}, Test: {test_acc:.4f}")
        
        # Restore original model
        self.model = original_model
        self.history = original_history
        
        return results
    
    def save_results(self, filename: str = "results.json"):
        """Save results"""
        self.results['timestamp'] = datetime.now().isoformat()
        self.results['features'] = self.feature_names
        self.results['target_names'] = self.target_names
        
        if self.history:
            self.results['history'] = {
                'loss': self.history.history['loss'],
                'val_loss': self.history.history['val_loss'],
                'accuracy': self.history.history['accuracy'],
                'val_accuracy': self.history.history['val_accuracy']
            }
        
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
        print(f"Classes: {len(self.target_names)}")
        
        if 'metrics' in self.results:
            print("\nPerformance Metrics:")
            for key, value in self.results['metrics'].items():
                print(f"  {key}: {value:.4f}")
        
        if 'training' in self.results:
            print(f"\nTraining: {self.results['training']['epochs_trained']} epochs")
            print(f"  Train Accuracy: {self.results['training']['train_accuracy']:.4f}")
            print(f"  Test Accuracy: {self.results['training']['test_accuracy']:.4f}")
        
        if self.model:
            self.model.summary()
        
        print("="*50)
