from .xai_methods import SHAPExplainer
from .interpret_results import ExplanationGenerator
import numpy as np

class XAIPipeline:
    def __init__(self):
        self.shap = SHAPExplainer()
        self.interpreter = ExplanationGenerator()
    
    def explain(self, symptom_vector):
        # Get SHAP values
        shap_values = self.shap.explain_prediction(symptom_vector)
        
        # Get top prediction
        pred_proba = self.shap.model.predict_proba([symptom_vector])[0]
        top_class = np.argmax(pred_proba)
        
        # Generate explanations
        return {
            'shap_values': shap_values,
            'text_explanation': self.interpreter.generate_explanation(
                shap_values, symptom_vector, top_class),
            'contrastive_explanation': self.interpreter.generate_contrastive_explanation(
                shap_values, [top_class, np.argsort(pred_proba)[-2]])
        }