import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.chat.chat_assistant import ChatAssistant
from app.utils.logger import get_logger

logger = get_logger(__name__)

def run_chat_demo():
    """
    Script to run the ChatAssistant interactively for testing queries.
    """
    assistant = ChatAssistant()
    
    print("\n--- Supply Chain Chat Assistant Demo ---")
    print("Type 'exit' or 'quit' to stop.\n")
    
    try:
        while True:
            question = input("User: ")
            if question.lower() in ["exit", "quit"]:
                break
            
            response = assistant.ask(question)
            print(f"Assistant: {response.get('answer')}")
            # print(f"DEBUG - Data: {response.get('data')[:2]}...") # Optional debug
            
    except Exception as e:
        logger.error(f"Error running chat assistant: {e}")
    finally:
        assistant.close()
        print("\nConnection closed. Goodbye!")

if __name__ == "__main__":
    run_chat_demo()
