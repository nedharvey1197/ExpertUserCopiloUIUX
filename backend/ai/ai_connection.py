import os
from dotenv import load_dotenv
import openai

# 🔄 Load environment variables from .env
load_dotenv()

# 🧠 OpenAI Configuration
def init_openai():
    # First check OS environment
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    source = "OS environment"
    
    # If not in OS env, check .env file
    if not openai_api_key:
        load_dotenv()  # Load .env file
        openai_api_key = os.getenv("OPENAI_API_KEY")
        source = ".env file"
    
    if not openai_api_key:
        raise ValueError("OpenAI API Key is missing from both OS environment and .env file!")
    
    print(f"Using OpenAI API key from: {source}")
    openai.api_key = openai_api_key
    return openai

# 🤖 Custom Assistant Configuration
def get_assistant_client():
    # Initialize the OpenAI client for assistants API
    client = openai.OpenAI()
    return client

# Example assistant ID (replace with your actual ID)
ASSISTANT_ID = "asst_gBino8HQs7HoxblezP4eKrQw"

# ✅ Optional: test the connection when run directly
if __name__ == "__main__":
    try:
        # Test standard API
        openai_client = init_openai()
        print("✅ OpenAI API configured!")
        
        # Test assistants API
        assistant_client = get_assistant_client()
        print("✅ Assistants API configured!")
    except Exception as e:
        print("❌ OpenAI configuration failed:", e)
