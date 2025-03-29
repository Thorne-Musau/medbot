import joblib
from pathlib import Path
import numpy as np
from .symptom_extraction import ComprehensiveSymptomExtractor

class DiagnosisIntegrator:
    def __init__(self):
        self.extractor = ComprehensiveSymptomExtractor()
        self.symptom_names = joblib.load(Path('data/processed/symptom_names.joblib'))
        self.model = joblib.load(Path('models/saved_models/disease_predictor.joblib'))
        self.label_encoder = joblib.load(Path('data/processed/label_encoder.joblib'))
    
    def text_to_features(self, text):
        """Convert user text to binary symptom vector"""
        extraction = self.extractor.extract(text)
        symptom_vector = np.zeros(len(self.symptom_names), dtype=int)
        
        for i, symptom in enumerate(self.symptom_names):
            if symptom in extraction['exact_matches']:
                symptom_vector[i] = 1
                
        return {
            'symptom_vector': symptom_vector,
            'extraction_result': extraction
        }
    
    def predict_disease(self, text):
        """Full pipeline: text -> symptoms -> diagnosis"""
        features = self.text_to_features(text)
        proba = self.model.predict_proba([features['symptom_vector']])[0]
        
        diseases = self.label_encoder.classes_
        predictions = sorted(zip(diseases, proba), 
                           key=lambda x: x[1], 
                           reverse=True)
        
        return {
            'symptoms': features['extraction_result'],
            'predictions': predictions[:3],  # Top 3 diagnoses
            'primary_diagnosis': predictions[0]
        }