import joblib
from pathlib import Path
import numpy as np
import sys
import os

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

class IntentClassifier:
    def __init__(self):
        # Load trained model
        try:
            model_path = Path('models/saved_models/intent_classifier.joblib')
            vectorizer_path = Path('models/saved_models/intent_vectorizer.joblib')
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found at {model_path}")
            if not vectorizer_path.exists():
                raise FileNotFoundError(f"Vectorizer file not found at {vectorizer_path}")
                
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            
        except Exception as e:
            print(f"Error loading model files: {str(e)}")
            raise
        
        self.classes = [
            'symptom_description',
            'treatment_inquiry',
            'emergency',
            'greeting',
            'goodbye'
        ]

    def classify(self, text: str) -> str:
        """Classify user intent"""
        features = self.vectorizer.transform([text])
        proba = self.model.predict_proba(features)[0]
        return self.classes[np.argmax(proba)]
    
    def is_emergency(self, text: str) -> bool:
        """Check for emergency keywords"""
        emergency_terms = {
            'chest pain', 'difficulty breathing', 'unconscious',
            'severe pain', 'bleeding heavily'
        }
        return any(term in text.lower() for term in emergency_terms)