
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.llm.ollama_service import OllamaService

async def test_ollama():
    print("Testing Ollama connection...")
    service = OllamaService()
    
    try:
        connected = await service.check_connection()
        print(f"Ollama connected: {connected}")
        
        if connected:
            print("\nTesting text generation...")
            response = await service.generate("Hello, test", temperature=0.1)
            print(f"Ollama response: {response}")
            print("\n✅ Ollama test passed!")
    except Exception as e:
        print(f"Ollama test failed: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_ollama())
