from typing import Optional, Dict, Any
import asyncio
from src.core.llm_client import OllamaClient
from src.memory.converstaion_memory import ConversationMemory
from config.settings import settings

class ChatAgent:
    """Main chat agent with memory and Ollama integration."""
    
    def __init__(self, model: str = None):
        self.llm_client = OllamaClient(model=model)
        self.memory = ConversationMemory()
        self.model = model or settings.OLLAMA_MODEL
        
    def chat(self, message: str) -> str:
        """Process a chat message and return response."""
        # Add user message to memory
        self.memory.add_message("user", message)
        
        # Get conversation context
        context = self.memory.get_context()
        
        try:
            # Generate response using context
            if len(context) > 1:  # If we have context beyond system message
                response = asyncio.run(self.llm_client.chat(message, context[:-1]))  # Exclude the last user message since it's already in the chat call
            else:
                response = self.llm_client.generate(message)
            
            # Add assistant response to memory
            self.memory.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.memory.add_message("assistant", error_msg, {"error": True})
            return error_msg
    
    def get_memory_summary(self) -> str:
        """Get a summary of the conversation memory."""
        return self.memory.get_summary()
    
    def clear_memory(self):
        """Clear conversation memory."""
        self.memory.clear()
        print("🧠 Memory cleared!")
    
    def export_conversation(self) -> str:
        """Export the conversation history."""
        return self.memory.export_history()
    
    def is_ready(self) -> bool:
        """Check if the agent is ready to chat."""
        return self.llm_client.is_available()
