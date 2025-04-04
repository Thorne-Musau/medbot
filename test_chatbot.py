from chatbot import MedicalChatbot
from nlp.diagnosis_integration import DiagnosisIntegrator

def test_chatbot():
    print("Testing MedBot - Basic Functionality")
    print("-" * 50)
    
    try:
        # Initialize chatbot
        chatbot = MedicalChatbot()
        print("✓ Chatbot initialized successfully")
        
        # Test greeting
        response = chatbot.process_input("")
        print("\nGreeting Test:")
        print(f"Expected: Greeting message")
        print(f"Actual: {response['text']}")
        
        # Test symptom collection
        print("\nSymptom Collection Test:")
        symptoms = [
            "I have a headache",
            "I feel feverish",
            "I'm feeling nauseous"
        ]
        
        for symptom in symptoms:
            print(f"\nProcessing: {symptom}")
            try:
                # Test symptom extraction directly
                extraction = chatbot.diagnosis_integrator.text_to_features(symptom)
                print(f"Extracted symptoms: {extraction['exact_matches']}")
                
                # Process through chatbot
                response = chatbot.process_input(symptom)
                print(f"Chatbot response: {response['text']}")
                print(f"Current symptoms: {chatbot.conversation_state['symptoms']}")
                
            except Exception as e:
                print(f"Error processing symptom: {str(e)}")
                raise
        
        # Test diagnosis
        print("\nDiagnosis Test:")
        try:
            response = chatbot.process_input("")
            print(f"Response: {response['text']}")
        except Exception as e:
            print(f"Error in diagnosis: {str(e)}")
            raise
        
        # Test reset
        print("\nReset Test:")
        try:
            response = chatbot.process_input("")
            print(f"Response: {response['text']}")
        except Exception as e:
            print(f"Error in reset: {str(e)}")
            raise
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        print("Please ensure all required files and dependencies are installed.")

if __name__ == "__main__":
    test_chatbot() 