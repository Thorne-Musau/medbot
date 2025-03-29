import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from sklearn.metrics import top_k_accuracy_score

def load_model_and_data():
    model_path = Path('models/saved_models/disease_predictor.joblib')
    model = joblib.load(model_path)
    
    X_test = pd.read_csv(Path('data/processed/X_test.csv')).values
    y_test = pd.read_csv(Path('data/processed/y_test.csv')).values.ravel()
    
    le = joblib.load(Path('data/processed/label_encoder.joblib'))
    
    return model, X_test, y_test, le

def evaluate_model(model, X_test, y_test, le):
    metrics = {}
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Create docs directory if it doesn't exist
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(docs_dir / 'confusion_matrix.png')
    plt.close()
    
    # Classification report
    report = classification_report(y_test, y_pred, target_names=le.classes_)
    print("\nClassification Report:")
    print(report)
    
    # Save probabilities for XAI
    np.save(Path('data/processed/y_proba.npy'), y_proba)

    # Top-3 accuracy
    y_proba = model.predict_proba(X_test)
    top3_acc = top_k_accuracy_score(y_test, y_proba, k=3)
    print(f"Top-3 Accuracy: {top3_acc:.4f}")
    
    # Per-class metrics
    class_report = classification_report(
        y_test, 
        y_pred, 
        target_names=le.classes_,
        output_dict=True
    )

    # Save detailed report
    report_df = pd.DataFrame(class_report).transpose()
    report_df.to_csv(docs_dir / 'classification_report.csv')
    
    metrics.update({
        'top3_accuracy': top3_acc,
        'class_report': class_report
    })
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'classification_report': report
    }

def main():
    model, X_test, y_test, le = load_model_and_data()
    metrics = evaluate_model(model, X_test, y_test, le)
    
    # Save metrics
    joblib.dump(metrics, Path('models/saved_models/metrics.joblib'))

if __name__ == '__main__':
    main()