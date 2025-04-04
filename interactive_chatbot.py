from chatbot import MedicalChatbot
import sys

def run_interactive_chatbot():
    print("=" * 50)
    print("MedBot - Interactive Medical Diagnosis Assistant")
    print("=" * 50)
    print("Type 'quit' to exit, 'reset' to start a new conversation")
    print("-" * 50)
    
    try:
        # Initialize chatbot
        chatbot = MedicalChatbot()
        print("✓ MedBot initialized successfully")
        print("-" * 50)
        
        # Start conversation
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for commands
            if user_input.lower() == 'quit':
                print("\nThank you for using MedBot. Take care!")
                break
                
            elif user_input.lower() == 'reset':
                chatbot.conversation_state = {
                    'symptoms': [],
                    'current_step': 'greeting'
                }
                print("\nConversation reset. Starting new session...")
                continue
            
            # Process input
            try:
                response = chatbot.process_input(user_input)
                print("\nMedBot:", response['text'])
                
                # Show current symptoms if in symptom collection mode
                if chatbot.conversation_state['current_step'] == 'symptom_collection':
                    if chatbot.conversation_state['symptoms']:
                        print("\nCurrent symptoms:", ", ".join(chatbot.conversation_state['symptoms']))
                
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Please try again or type 'reset' to start over.")
    
    except Exception as e:
        print(f"\nError initializing MedBot: {str(e)}")
        print("Please ensure all required files and dependencies are installed.")
        sys.exit(1)

if __name__ == "__main__":
    run_interactive_chatbot() 