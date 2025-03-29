import unittest
from nlp.diagnosis_integration import DiagnosisIntegrator

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.integrator = DiagnosisIntegrator()
    
    def test_common_conditions(self):
        test_cases = [
            ("I have fever and cough", ['Bronchial Asthma', 'GERD']),
            ("Headache with nausea and vomiting", ['Gastroenteritis', 'Paralysis (brain hemorrhage)']),
            ("Chest pain and dizziness", ['Heart attack', 'Hypertension'])
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = self.integrator.predict_disease(text)
                predicted_diseases = [d[0] for d in result['predictions']]
                matches = [d for d in predicted_diseases if d in expected]
                self.assertTrue(len(matches) > 0, 
                               f"No expected diseases in {predicted_diseases}")

    def test_symptom_mapping(self):
        text = "I have cephalgia and emesis"
        result = self.integrator.text_to_features(text)
        self.assertIn('headache', result['extraction_result']['exact_matches'])
        self.assertIn('vomiting', result['extraction_result']['exact_matches'])

if __name__ == "__main__":
    unittest.main()