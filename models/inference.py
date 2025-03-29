import joblib
import numpy as np
from pathlib import Path

class DiseasePredictor:
    def __init__(self):
        # Load model, encoder, and symptom names
        self.model = joblib.load(Path('models/saved_models/disease_predictor.joblib'))
        self.le = joblib.load(Path('data/processed/label_encoder.joblib'))
        self.symptom_names = joblib.load(Path('data/processed/symptom_names.joblib'))
        
    def predict_from_symptoms(self, symptom_list):
        """
        Predict from list of symptom names
        
        Args:
            symptom_list: List of symptom names present (e.g., ['itching', 'skin_rash'])
            
        Returns:
            dict: Prediction results
        """
        # Create binary vector
        input_vector = [1 if symptom in symptom_list else 0 
                       for symptom in self.symptom_names]
        return self.predict(input_vector)
    
    def predict(self, symptoms):
        """
        Predict disease based on binary symptom vector
        
        Args:
            symptoms: Binary list/array matching symptom_names
            
        Returns:
            dict: {
                'disease': str,
                'probability': float,
                'all_predictions': list of (disease, probability) tuples,
                'matched_symptoms': list of matched symptom names
            }
        """
        symptoms = np.array(symptoms)
        if len(symptoms.shape) == 1:
            symptoms = symptoms.reshape(1, -1)
            
        probabilities = self.model.predict_proba(symptoms)[0]
        top_class_idx = np.argmax(probabilities)
        
        # Get matched symptoms
        matched_symptoms = [self.symptom_names[i] 
                          for i, val in enumerate(symptoms[0]) 
                          if val == 1]
        
        all_predictions = sorted(
            zip(self.le.classes_, probabilities),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'disease': self.le.classes_[top_class_idx],
            'probability': probabilities[top_class_idx],
            'all_predictions': all_predictions,
            'matched_symptoms': matched_symptoms
        }

if __name__ == '__main__':
    # Example usage
    predictor = DiseasePredictor()
    # Example symptoms vector (should match your model's input features)
    example_symptoms = [1, 0, 1, 0, 0, 1, 0, 0, 1, 0]  # This is just an example
    prediction = predictor.predict(example_symptoms)
    print("Top Prediction:", prediction['disease'], f"(Probability: {prediction['probability']:.2f})")
    print("\nAll Predictions:")
    for disease, prob in prediction['all_predictions']:
        print(f"- {disease}: {prob:.4f}")