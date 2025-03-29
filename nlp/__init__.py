from pathlib import Path
import joblib
from .entity_recognition import MedicalNER
from .intent_classification import IntentClassifier

# Create models directory if it doesn't exist
models_dir = Path('models/saved_models')
models_dir.mkdir(parents=True, exist_ok=True)

# Initialize NLP components when module loads
if not (models_dir / 'intent_classifier.joblib').exists():
    # Sample training data
    train_texts = [
        "I have a headache and fever",
        "What causes diabetes?",
        "How is pneumonia treated?",
        "Hello doctor",
        "My stomach hurts after eating"
    ]
    train_labels = [
        'symptom_description',
        'disease_inquiry',
        'treatment_inquiry',
        'greeting',
        'symptom_description'
    ]
    
    # Train and save the classifier
    classifier = IntentClassifier()
    classifier.train(train_texts, train_labels)
    classifier.save(models_dir / 'intent_classifier.joblib')

# Initialize NLP components
ner_model = MedicalNER()

def process_text(text):
    """Main interface for NLP processing"""
    return ner_model.process_input(text)