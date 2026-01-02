from pycursor_agent import Client
import os
import shutil

def test_sdk():
    # Set the folder where test results will be stored
    sdk_root = os.path.dirname(os.path.abspath(__file__))
    test_results_dir = os.path.join(sdk_root, "test_results")
    
    # Clean and create the test results directory
    if os.path.exists(test_results_dir):
        # ask if user wants to delete the directory
        if input(f"Do you want to delete the test results directory {test_results_dir} to start a new test? (y/n): ") == "y":
            shutil.rmtree(test_results_dir)
        else:
            print("Test results directory not deleted. Please delete it manually before running the test.")
            return

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

    # --- PART 1: CONTEXT TESTS ---
    log("=== PART 1: CONTEXT TESTS ===")
    
    # 1.1 Testing Multi-turn Chat using Chat ID
    log("--- 1.1 Testing Chat Session Resumption ---")
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

    # 1.2 Testing 'agent' mode (with file-based context)
    log("--- 1.2 Testing File-based Context ---")
    try:
        res = client.agent("Write 'Context test: Step 1 passed' into context_file.txt", model=model)
        log(f"Step 1: {res}")
        
        res = client.agent("Read context_file.txt and summarize the context", model=model)
        log(f"Step 2: {res}\n")
    except Exception as e:
        log(f"Error in file-based context test: {e}\n")

    # --- PART 2: FUNCTIONALITY TESTS (4 MODES) ---
    log("\n=== PART 2: FUNCTIONALITY TESTS ===")

    # 2.1 Agent Mode (Standard)
    log("--- 2.1 Testing 'agent' mode (standard) ---")
    try:
        res = client.agent("Create a file 'mode_test.txt' with the current date and time", model=model)
        log(f"Result: {res}\n")
    except Exception as e:
        log(f"Error in 'agent': {e}\n")

    # 2.2 Ask Mode
    log("--- 2.2 Testing 'ask' mode ---")
    try:
        res = client.ask("What is the capital of France?", model=model)
        log(f"Result: {res}\n")
    except Exception as e:
        log(f"Error in 'ask': {e}\n")

    # 2.3 Planner Mode
    log("--- 2.3 Testing 'planner' mode ---")
    try:
        res = client.plan("I want to build a simple Todo app, please provide a plan", model=model)
        log(f"Result: {res}\n")
    except Exception as e:
        log(f"Error in 'planner': {e}\n")

    # 2.4 Debug Mode
    log("--- 2.4 Testing 'debug' mode ---")
    try:
        # Create a buggy file for debugging
        buggy_file = os.path.join(test_results_dir, "buggy.py")
        with open(buggy_file, "w") as f:
            f.write("def power(a, b):\n    return a + b  # Wrong logic, should be a ** b")
        
        res = client.debug("The logic of the power function in buggy.py is wrong. Please check and fix it for me.", model=model)
        log(f"Result: {res}\n")
    except Exception as e:
        log(f"Error in 'debug': {e}\n")

    log("=== All Tests Complete ===")

if __name__ == "__main__":
    test_sdk()
