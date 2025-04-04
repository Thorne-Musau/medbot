from typing import Dict, Any
from pathlib import Path
import json
import sys
import os

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from nlp.diagnosis_integration import DiagnosisIntegrator
except ImportError:
    print("Warning: nlp module not found. Please ensure it's installed and in the Python path.")
    DiagnosisIntegrator = None

class MedicalChatbot:
    def __init__(self):
        if DiagnosisIntegrator is None:
            raise ImportError("Required module 'nlp' not found. Please install it first.")
            
        self.diagnosis_integrator = DiagnosisIntegrator()
        self.conversation_state = {
            'symptoms': [],
            'current_step': 'greeting'
        }
        
        # Load conversation flow
        try:
            flow_path = Path('chatbot/data/conversation_flow.json')
            if not flow_path.exists():
                raise FileNotFoundError(f"Conversation flow file not found at {flow_path}")
            with open(flow_path) as f:
                self.flow = json.load(f)
        except Exception as e:
            print(f"Error loading conversation flow: {str(e)}")
            raise

    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input and return response"""
        current_step = self.conversation_state['current_step']
        
        if current_step == 'greeting':
            self.conversation_state['current_step'] = 'symptom_collection'
            return {'text': self.flow['greeting']}
            
        elif current_step == 'symptom_collection':
            # Extract symptoms from user input
            extraction = self.diagnosis_integrator.text_to_features(user_input)
            self.conversation_state['symptoms'].extend(extraction['exact_matches'])
            
            if len(self.conversation_state['symptoms']) >= 3:
                self.conversation_state['current_step'] = 'diagnosis'
                return {'text': self.flow['enough_symptoms']}
            else:
                remaining = 3 - len(self.conversation_state['symptoms'])
                return {'text': self.flow['more_symptoms_needed'].format(remaining=remaining)}
                
        elif current_step == 'diagnosis':
            diagnosis = self.diagnosis_integrator.predict_disease(
                self.conversation_state['symptoms']
            )
            self.conversation_state['current_step'] = 'followup'
            return {'text': self._format_diagnosis(diagnosis)}
            
        elif current_step == 'followup':
            self.conversation_state = {'current_step': 'greeting'}  # Reset
            return {'text': self.flow['goodbye']}

    def _format_diagnosis(self, diagnosis: Dict) -> str:
        """Format diagnosis results for user"""
        top3 = diagnosis['predictions'][:3]
        formatted = [f"{disease} ({prob:.1%})" for disease, prob in top3]
        return self.flow['diagnosis_response'].format(
            conditions=", ".join(formatted)
        )