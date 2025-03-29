import unittest
import numpy as np
from explainable_ai.pipeline import XAIPipeline

class TestXAI(unittest.TestCase):
    def setUp(self):
        self.pipeline = XAIPipeline()
        # Sample symptom vector (fever + cough)
        self.sample_input = np.zeros(132)
        self.sample_input[0] = 1  # fever
        self.sample_input[1] = 1  # cough

    def test_shap_calculation(self):
        result = self.pipeline.explain(self.sample_input)
        self.assertIn('shap_values', result)
        self.assertEqual(len(result['shap_values']), 
                        len(self.pipeline.shap.label_encoder.classes_))

    def test_explanation_generation(self):
        result = self.pipeline.explain(self.sample_input)
        self.assertIn('Primary diagnosis', result['text_explanation'])
        self.assertIn('favored', result['contrastive_explanation'])

if __name__ == '__main__':
    unittest.main()