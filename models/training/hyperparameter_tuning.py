import pandas as pd
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from pathlib import Path
import yaml
from train import load_data, train_model

def load_config():
    with open(Path('config/model_config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def tune_hyperparameters(X_train, y_train):
    config = load_config()
    model_type = config['model']['type']
    
    if model_type == 'random_forest':
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
        base_model = RandomForestClassifier(random_state=config['data']['random_state'])
    elif model_type == 'xgboost':
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 6, 9],
            'learning_rate': [0.01, 0.1, 0.2]
        }
        base_model = XGBClassifier(random_state=config['data']['random_state'])
    else:
        print("Hyperparameter tuning not implemented for this model type")
        return None
    
    grid_search = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        scoring='accuracy'
    )
    
    grid_search.fit(X_train, y_train)
    
    print("Best parameters found:")
    print(grid_search.best_params_)
    print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_

def main():
    X_train, X_test, y_train, y_test = load_data()
    best_model = tune_hyperparameters(X_train, y_train)
    
    if best_model:
        # Save the best model
        saved_models_dir = Path('models/saved_models')
        saved_models_dir.mkdir(exist_ok=True)
        joblib.dump(best_model, saved_models_dir / 'tuned_disease_predictor.joblib')
        print("Tuned model saved successfully!")

if __name__ == '__main__':
    main()