import os
from dotenv import load_dotenv

def test_env():
    # Load environment variables from .env file
    load_dotenv()
    
    # List of required environment variables
    required_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    optional_vars = ['AGENTOPS_API_KEY']
    
    # Check required variables
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    # Check optional variables
    missing_optional = []
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    # Print results
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
    else:
        print("✅ All required environment variables are set")
    
    if missing_optional:
        print("\nℹ️ Missing optional environment variables:")
        for var in missing_optional:
            print(f"  - {var}")
    else:
        print("✅ All optional environment variables are set")

if __name__ == "__main__":
    test_env() 