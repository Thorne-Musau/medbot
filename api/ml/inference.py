import joblib
from pathlib import Path
import numpy as np
from typing import List, Dict, Tuple

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.symptom_names = None
        self.label_encoder = None
        self.load_model()

    def load_model(self):
        """Load the trained model and necessary components."""
        try:
            model_path = Path("models/saved_models/disease_predictor.joblib")
            symptom_path = Path("data/processed/symptom_names.joblib")
            encoder_path = Path("data/processed/label_encoder.joblib")

            self.model = joblib.load(model_path)
            self.symptom_names = joblib.load(symptom_path)
            self.label_encoder = joblib.load(encoder_path)
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

    def preprocess_symptoms(self, symptoms: List[str]) -> np.ndarray:
        """Convert symptoms list to model input format."""
        # Create a binary vector for symptoms
        symptom_vector = np.zeros(len(self.symptom_names))
        for symptom in symptoms:
            if symptom in self.symptom_names:
                idx = self.symptom_names.index(symptom)
                symptom_vector[idx] = 1
        return symptom_vector.reshape(1, -1)

    def predict(self, symptoms: List[str]) -> Tuple[List[Dict[str, float]], str, float]:
        """
        Make predictions for given symptoms.
        Returns:
            - List of disease predictions with probabilities
            - Primary diagnosis
            - Confidence score
        """
        if not self.model or not self.symptom_names or not self.label_encoder:
            raise RuntimeError("Model not loaded")

        # Preprocess symptoms
        X = self.preprocess_symptoms(symptoms)

        # Get probability predictions
        probabilities = self.model.predict_proba(X)[0]

        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        predictions = []
        for idx in top_indices:
            disease = self.label_encoder.inverse_transform([idx])[0]
            probability = float(probabilities[idx])
            predictions.append({
                "disease": disease,
                "probability": probability
            })

        # Get primary diagnosis and confidence
        primary_diagnosis = predictions[0]["disease"]
        confidence = predictions[0]["probability"]

        return predictions, primary_diagnosis, confidence

# Create a singleton instance
predictor = DiseasePredictor()

def get_predictor() -> DiseasePredictor:
    """Get the singleton predictor instance."""
    return predictor 