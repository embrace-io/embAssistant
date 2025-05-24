from typing import Optional, Dict, Any, List
import ollama
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManagerForLLMRun
from config.settings import settings

class OllamaClient:
    """Enhanced Ollama client with connection pooling and error handling."""
    
    def __init__(self, model: str = None, base_url: str = None):
        self.model = model or settings.OLLAMA_MODEL
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.client = ollama.Client(host=self.base_url)
        
        # Initialize LangChain Ollama instance
        self.llm = Ollama(
            model=self.model,
            base_url=self.base_url,
            temperature=0.7
        )
    
    async def chat(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """Send a chat message and get response."""
        try:
            messages = context or []
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            return response['message']['content']
        
        except Exception as e:
            raise Exception(f"Ollama chat error: {str(e)}")
    
    def generate(self, prompt: str) -> str:
        """Generate response using LangChain interface."""
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            raise Exception(f"Ollama generation error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Ollama server is available."""
        try:
            self.client.list()
            return True
        except:
            return False
    
    def list_models(self) -> List[str]:
        """List available models."""
        try:
            models = self.client.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

