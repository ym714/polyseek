import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from polyseek_sentient.config import load_settings

def check_config():
    try:
        settings = load_settings()
        print(f"Offline Mode: {settings.app.offline_mode}")
        print(f"Model: {settings.llm.model}")
        
        api_key = settings.llm.api_key
        if api_key:
            masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "****"
            print(f"API Key found: {masked}")
        else:
            print("API Key: NOT FOUND")
            
        print(f"Polymarket Base: {settings.apis.polymarket_base}")
        
        try:
            import litellm
            print(f"LiteLLM version: {litellm.__version__}")
        except ImportError:
            print("LiteLLM not installed")
            
    except Exception as e:
        print(f"Error loading settings: {e}")

if __name__ == "__main__":
    check_config()
