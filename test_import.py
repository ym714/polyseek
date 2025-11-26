# Test if imports work
import sys
print("Python path:", sys.path)

try:
    from src.polyseek_sentient.main import app
    print("✅ Import successful!")
    print("App:", app)
except Exception as e:
    print("❌ Import failed:", e)
    import traceback
    traceback.print_exc()
