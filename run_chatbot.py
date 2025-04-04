from chatbot import MedicalChatbot
import sys

def main():
    print("Welcome to MedBot - Medical Diagnosis Assistant")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    try:
        chatbot = MedicalChatbot()
        print("MedBot initialized successfully!")
        print("-" * 50)
        
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for quit command
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nThank you for using MedBot. Take care!")
                break
            
            # Process input
            response = chatbot.process_input(user_input)
            
            # Print response
            print("\nMedBot:", response['text'])
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please ensure all required files and dependencies are installed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 