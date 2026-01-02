from pycursor_agent import Client
import os
import shutil

def test_sdk():
    # Set the folder where test results will be stored
    sdk_root = os.path.dirname(os.path.abspath(__file__))
    test_results_dir = os.path.join(sdk_root, "test_results")
    
    # Clean and create the test results directory
    if os.path.exists(test_results_dir):
        shutil.rmtree(test_results_dir)
    os.makedirs(test_results_dir)
    
    print(f"Testing SDK. Results will be saved in: {test_results_dir}")
    
    client = Client(workspace=test_results_dir)
    model = "gemini-3-flash"
    
    # Log file path
    log_path = os.path.join(test_results_dir, "test_log.txt")
    
    def log(msg):
        print(msg)
        with open(log_path, "a") as f:
            f.write(msg + "\n")

    log("=== Cursor Agent SDK Test Report ===\n")

    # 1. Testing Multi-turn Chat using Chat ID
    log("--- 1. Testing Chat Session Resumption ---")
    try:
        chat_id = client.create_chat()
        log(f"Created new chat session: {chat_id}")
        
        # Turn 1: Introduce
        client.agent("My name is Cursor Explorer.", model=model, chat_id=chat_id)
        log("Sent: My name is Cursor Explorer.")
        
        # Turn 2: Ask about the name
        res = client.agent("What is my name?", model=model, chat_id=chat_id)
        log(f"Sent: What is my name?\nResult: {res}\n")
    except Exception as e:
        log(f"Error in multi-turn chat: {e}\n")

    # 2. Testing 'agent' mode
    log("--- 2. Testing 'agent' mode (with file-based context) ---")
    try:
        res = client.agent("Write '1 + 1 = 2' into context_test.txt", model=model)
        log(f"Turn 1: {res}")
        
        res = client.agent("Read context_test.txt and tell me what the result was", model=model)
        log(f"Turn 2 (File-based context): {res}\n")
    except Exception as e:
        log(f"Error in 'agent': {e}\n")

    log("=== Test Complete ===")

if __name__ == "__main__":
    test_sdk()
