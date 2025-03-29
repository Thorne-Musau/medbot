from collections import defaultdict
import numpy as np
import joblib
from pathlib import Path

class ExplanationGenerator:
    def __init__(self):
        self.symptom_impact = defaultdict(list)
        self.symptom_names = joblib.load(Path('data/processed/symptom_names.joblib'))
        self.label_encoder = joblib.load(Path('data/processed/label_encoder.joblib'))
        
    def generate_explanation(self, shap_values, symptom_vector):
        """Generate human-readable explanation from SHAP values"""
        # Get top predicted disease
        pred_probs = self.model.predict_proba(symptom_vector.reshape(1, -1))[0]
        top_disease_idx = np.argmax(pred_probs)
        top_disease = self.label_encoder.classes_[top_disease_idx]
        
        # Get contributing symptoms
        contributing_symptoms = []
        for i in np.where(shap_values[top_disease_idx][0] != 0)[0]:
            symptom_name = self.symptom_names[i]
            contribution = shap_values[top_disease_idx][0][i]
            contributing_symptoms.append((symptom_name, contribution))
        
        # Sort by absolute contribution
        contributing_symptoms.sort(key=lambda x: abs(x[1]), reverse=True)
        
        # Generate explanation
        explanation = f"The model predicts {top_disease} with {pred_probs[top_disease_idx]:.2%} confidence.\n"
        explanation += "Key contributing symptoms:\n"
        for symptom, contribution in contributing_symptoms[:5]:  # Top 5 symptoms
            direction = "increases" if contribution > 0 else "decreases"
            explanation += f"- {symptom} {direction} the likelihood by {abs(contribution):.2%}\n"
        
        return explanation

    def generate_contrastive_explanation(self, shap_values, top_diseases):
        """Explain why one disease was chosen over another"""
        primary = top_diseases[0]
        secondary = top_diseases[1]
        
        diff = shap_values[primary] - shap_values[secondary]
        
        return (
            f"The system favored {primary} over {secondary} because:\n"
            f"- Higher weight given to: {', '.join(self._top_features(diff, 3))}\n"
            f"- Lower weight given to: {', '.join(self._bottom_features(diff, 3))}"
        )
    
    def _top_features(self, values, n=3):
        return [self.symptom_names[i] for i in np.argsort(values)[-n:][::-1]]
    
    def _bottom_features(self, values, n=3):
        return [self.symptom_names[i] for i in np.argsort(values)[:n]]