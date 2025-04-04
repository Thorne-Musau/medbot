from chatbot import MedicalChatbot
from nlp.diagnosis_integration import DiagnosisIntegrator

def test_real_symptoms():
    print("Testing MedBot with Real-World Symptom Inputs")
    print("-" * 50)
    
    # Test cases with various symptom descriptions
    test_cases = [
        {
            "description": "Common Cold Symptoms",
            "inputs": [
                "I have a runny nose and sore throat",
                "I'm sneezing a lot and my head feels heavy",
                "I feel tired and have a mild fever"
            ]
        },
        {
            "description": "Flu-like Symptoms",
            "inputs": [
                "I have a high fever and body aches",
                "I feel extremely tired and have chills",
                "My head hurts and I'm coughing"
            ]
        },
        {
            "description": "Gastrointestinal Issues",
            "inputs": [
                "I have stomach pain and feel nauseous",
                "I've been vomiting and have diarrhea",
                "I feel bloated and have no appetite"
            ]
        },
        {
            "description": "Respiratory Symptoms",
            "inputs": [
                "I'm having trouble breathing",
                "My chest feels tight and I'm wheezing",
                "I have a persistent cough with phlegm"
            ]
        },
        {
            "description": "Mixed Symptoms",
            "inputs": [
                "I have a headache and feel dizzy",
                "I'm sweating a lot and feel weak",
                "My muscles ache and I feel tired"
            ]
        }
    ]
    
    try:
        # Initialize chatbot
        chatbot = MedicalChatbot()
        print("✓ Chatbot initialized successfully")
        
        # Run each test case
        for case in test_cases:
            print(f"\nTesting Case: {case['description']}")
            print("-" * 30)
            
            # Reset chatbot state
            chatbot.conversation_state = {
                'symptoms': [],
                'current_step': 'greeting'
            }
            
            # Process each input
            for input_text in case['inputs']:
                print(f"\nInput: {input_text}")
                try:
                    # Test symptom extraction
                    extraction = chatbot.diagnosis_integrator.text_to_features(input_text)
                    print(f"Extracted symptoms: {extraction['exact_matches']}")
                    
                    # Process through chatbot
                    response = chatbot.process_input(input_text)
                    print(f"Chatbot response: {response['text']}")
                    print(f"Current symptoms: {chatbot.conversation_state['symptoms']}")
                    
                except Exception as e:
                    print(f"Error processing input: {str(e)}")
                    continue
            
            # Get final diagnosis
            if len(chatbot.conversation_state['symptoms']) >= 3:
                print("\nFinal Diagnosis:")
                try:
                    response = chatbot.process_input("")
                    print(f"Diagnosis: {response['text']}")
                except Exception as e:
                    print(f"Error in diagnosis: {str(e)}")
            
            print("\n" + "="*50)
        
        print("\nAll test cases completed!")
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        print("Please ensure all required files and dependencies are installed.")

if __name__ == "__main__":
    test_real_symptoms() 