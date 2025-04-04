from explainable_ai.pipeline import XAIPipeline
import joblib
from pathlib import Path
import numpy as np
from .symptom_extraction import ComprehensiveSymptomExtractor

class DiagnosisIntegrator:
    def __init__(self):
        # Expanded symptom mapping
        self.symptom_mapping = {
            # Respiratory symptoms
            'cough': ['cough', 'coughing', 'hacking cough'],
            'sore throat': ['sore throat', 'throat pain', 'scratchy throat'],
            'runny nose': ['runny nose', 'nasal discharge', 'rhinorrhea'],
            'breathing difficulty': ['trouble breathing', 'shortness of breath', 'breathlessness', 'wheezing'],
            'chest tightness': ['chest tightness', 'chest pressure', 'chest discomfort'],
            
            # General symptoms
            'fever': ['fever', 'feverish', 'high temperature', 'chills'],
            'fatigue': ['fatigue', 'tired', 'exhausted', 'weakness'],
            'headache': ['headache', 'head pain', 'cephalgia', 'migraine'],
            'body aches': ['body aches', 'muscle pain', 'myalgia', 'joint pain'],
            
            # Gastrointestinal symptoms
            'nausea': ['nausea', 'nauseous', 'feeling sick', 'queasy'],
            'vomiting': ['vomiting', 'throwing up', 'emesis'],
            'diarrhea': ['diarrhea', 'loose stools', 'bowel movement'],
            'stomach pain': ['stomach pain', 'abdominal pain', 'belly ache'],
            'loss of appetite': ['loss of appetite', 'no appetite', 'not hungry'],
            
            # Other symptoms
            'dizziness': ['dizziness', 'lightheaded', 'vertigo'],
            'sweating': ['sweating', 'perspiration', 'sweat'],
            'sneezing': ['sneezing', 'sneezes'],
            'congestion': ['congestion', 'stuffy nose', 'nasal congestion']
        }
        
    def text_to_features(self, text: str) -> dict:
        """Extract symptoms from text"""
        text = text.lower()
        exact_matches = []
        
        # Check for each symptom and its variations
        for symptom, variations in self.symptom_mapping.items():
            if any(variation in text for variation in variations):
                exact_matches.append(symptom)
        
        return {
            'exact_matches': exact_matches,
            'text': text
        }
    
    def predict_disease(self, symptoms: list) -> dict:
        """Predict disease based on symptoms"""
        # Define symptom patterns for different diseases
        disease_patterns = {
            'Common Cold': ['cough', 'sore throat', 'runny nose', 'sneezing', 'congestion'],
            'Influenza': ['fever', 'cough', 'body aches', 'fatigue', 'headache'],
            'Gastroenteritis': ['nausea', 'vomiting', 'diarrhea', 'stomach pain', 'loss of appetite'],
            'Bronchitis': ['cough', 'breathing difficulty', 'chest tightness', 'fatigue'],
            'Sinusitis': ['headache', 'congestion', 'runny nose', 'facial pain'],
            'Migraine': ['headache', 'nausea', 'dizziness', 'sensitivity to light'],
            'Pneumonia': ['cough', 'fever', 'breathing difficulty', 'chest pain', 'fatigue'],
            'Allergic Rhinitis': ['sneezing', 'runny nose', 'congestion', 'itchy eyes']
        }
        
        # Calculate match scores for each disease
        predictions = []
        for disease, pattern in disease_patterns.items():
            # Count matching symptoms
            matches = sum(1 for symptom in symptoms if symptom in pattern)
            # Calculate probability (simple scoring)
            probability = matches / len(pattern)
            predictions.append((disease, probability))
        
        # Sort by probability
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'predictions': predictions[:5],  # Top 5 predictions
            'symptoms_used': symptoms
        }
    
    def predict_with_explanation(text):
        """Enhanced prediction with explainable AI"""
        integrator = DiagnosisIntegrator()
        xai = XAIPipeline()  # Make sure to import at top: from explainable_ai.pipeline import XAIPipeline
        
        # Get features
        features = integrator.text_to_features(text)
        
        # Get prediction and explanation
        diagnosis = integrator.predict_disease(features['exact_matches'])
        explanation = xai.explain(features['exact_matches'])
        
        return {
            'diagnosis': diagnosis,
            'explanation': explanation
        }
    