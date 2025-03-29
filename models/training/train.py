import pandas as pd
import joblib
import yaml
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
from sklearn.svm import SVC
import numpy as np
from sklearn.utils.class_weight import compute_class_weight

def load_config():
    with open(Path('config/model_config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def load_data():
    processed_dir = Path('data/processed')
    X_train = pd.read_csv(processed_dir / 'X_train.csv').values
    X_test = pd.read_csv(processed_dir / 'X_test.csv').values
    y_train = pd.read_csv(processed_dir / 'y_train.csv').values.ravel()
    y_test = pd.read_csv(processed_dir / 'y_test.csv').values.ravel()
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    config = load_config()
    model_type = config['model']['type']
    
    # Calculate class weights for imbalanced data
    classes = np.unique(y_train)
    weights = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weights = dict(zip(classes, weights))
    
    if model_type == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=config['model']['n_estimators'],
            max_depth=config['model']['max_depth'],
            random_state=config['data']['random_state'],
            class_weight=class_weights,  # Add class weighting
            n_jobs=-1  # Use all cores
        )
    elif model_type == 'xgboost':
        model = XGBClassifier(
            n_estimators=config['model']['n_estimators'],
            max_depth=config['model']['max_depth'],
            learning_rate=config['model']['learning_rate'],
            random_state=config['data']['random_state'],
            scale_pos_weight=1,  # Adjust if severe imbalance
            use_label_encoder=False,
            eval_metric='logloss'
        )
    elif model_type == 'svm':
        model = SVC(
            C=config['model']['C'],
            kernel=config['model']['kernel'],
            probability=True,
            random_state=config['data']['random_state']
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(report)
    
    return accuracy, y_proba

def save_model(model):
    saved_models_dir = Path('models/saved_models')
    saved_models_dir.mkdir(exist_ok=True)
    joblib.dump(model, saved_models_dir / 'disease_predictor.joblib')
    print("Model saved successfully!")

def main():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)
    accuracy, y_proba = evaluate_model(model, X_test, y_test)
    save_model(model)

if __name__ == '__main__':
    main()