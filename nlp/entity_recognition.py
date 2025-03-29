from .symptom_extraction import ComprehensiveSymptomExtractor
from .intent_classification import IntentClassifier
from typing import Dict, Any
import joblib
from pathlib import Path

class MedicalNER:
    def __init__(self):
        self.symptom_extractor = ComprehensiveSymptomExtractor()
        self.intent_classifier = IntentClassifier.load(
            Path('models/saved_models/intent_classifier.joblib')
        )
        
    def process_input(self, text: str) -> Dict[str, Any]:
        """Process user input and extract medical entities"""
        # Step 1: Classify intent
        intent = self.intent_classifier.predict(text)
        
        # Step 2: Extract symptoms if relevant
        symptoms = {}
        if intent['intent'] in ['symptom_description', 'disease_inquiry']:
            symptoms = self.symptom_extractor.extract_symptoms(text)
        
        return {
            'text': text,
            'intent': intent,
            'symptoms': symptoms,
            'is_emergency': self._check_emergency(text, symptoms)
        }
    
    def _check_emergency(self, text: str, symptoms: Dict) -> bool:
        """Check for emergency keywords or critical symptoms"""
        emergency_keywords = {
            'chest pain', 'difficulty breathing', 'severe pain',
            'unconscious', 'bleeding heavily', 'sudden numbness'
        }
        
        critical_symptoms = {
            'chest_pain', 'breathlessness', 'acute_liver_failure',
            'coma', 'stomach_bleeding'
        }
        
        # Check text for keywords
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in emergency_keywords):
            return True
        
        # Check extracted symptoms
        if any(symptom in critical_symptoms 
               for symptom in symptoms.get('exact_matches', [])):
            return True
            
        return False