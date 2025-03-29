import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import yaml
from pathlib import Path

def load_config():
    with open(Path('config/model_config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def preprocess_data():
    config = load_config()
    
    # Load raw data
    raw_data_path = Path('data/raw') / config['data']['raw_filename']
    df = pd.read_csv(raw_data_path)
    
    # Basic cleaning
    df = df.dropna()
    df = df.drop_duplicates()
    
    # Separate features (symptoms) and target (prognosis)
    X = df.drop('prognosis', axis=1).values
    y = df['prognosis'].values
    
    # Encode target variable
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config['data']['test_size'], 
        random_state=config['data']['random_state'],
        stratify=y  # Important for imbalanced classes
    )
    
    # Save processed data and encoder
    processed_dir = Path('data/processed')
    processed_dir.mkdir(exist_ok=True)
    
    # Save symptom names for later reference
    symptom_names = df.drop('prognosis', axis=1).columns.tolist()
    joblib.dump(symptom_names, processed_dir / 'symptom_names.joblib')
    
    pd.DataFrame(X_train).to_csv(processed_dir / 'X_train.csv', index=False)
    pd.DataFrame(X_test).to_csv(processed_dir / 'X_test.csv', index=False)
    pd.DataFrame(y_train).to_csv(processed_dir / 'y_train.csv', index=False)
    pd.DataFrame(y_test).to_csv(processed_dir / 'y_test.csv', index=False)
    
    joblib.dump(le, processed_dir / 'label_encoder.joblib')
    
    print("Data preprocessing completed successfully!")
    print(f"Total symptoms: {len(symptom_names)}")
    print(f"Total diseases: {len(le.classes_)}")
    
if __name__ == '__main__':
    preprocess_data()