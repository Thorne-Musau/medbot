import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nlp.utils import tokenize_text
import joblib
from pathlib import Path

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            tokenizer=tokenize_text,
            ngram_range=(1, 2),
            max_features=5000
        )
        self.model = LogisticRegression(multi_class='multinomial', max_iter=1000)
        self.classes = [
            'symptom_description', 
            'treatment_inquiry',
            'disease_inquiry',
            'greeting',
            'other'
        ]
        
    def train(self, texts, labels):
        """Train the intent classifier"""
        X = self.vectorizer.fit_transform(texts)
        y = np.array([self.classes.index(label) for label in labels])
        self.model.fit(X, y)
        
    def predict(self, text):
        """Predict intent of user input"""
        X = self.vectorizer.transform([text])
        proba = self.model.predict_proba(X)[0]
        intent_idx = np.argmax(proba)
        return {
            'intent': self.classes[intent_idx],
            'confidence': float(proba[intent_idx]),
            'all_intents': list(zip(self.classes, proba))
        }
    
    def save(self, path):
        """Save trained model"""
        joblib.dump({
            'vectorizer': self.vectorizer,
            'model': self.model,
            'classes': self.classes
        }, path)
    
    @classmethod
    def load(cls, path):
        """Load trained model"""
        data = joblib.load(path)
        classifier = cls()
        classifier.vectorizer = data['vectorizer']
        classifier.model = data['model']
        classifier.classes = data['classes']
        return classifier