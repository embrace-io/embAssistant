from typing import List, Dict, Any, Optional
from datetime import datetime
from config.settings import settings
import json

class ConversationMemory:
    """Simple in-memory conversation storage with context window management."""
    
    def __init__(self, max_tokens: int = None, window_size: int = None):
        self.max_tokens = max_tokens or settings.MAX_MEMORY_TOKENS
        self.window_size = window_size or settings.MEMORY_WINDOW_SIZE
        self.messages: List[Dict[str, Any]] = []
        self.session_id = None
        self.created_at = datetime.now()
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to memory."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        self._manage_memory()
    
    def get_context(self, include_system: bool = True) -> List[Dict[str, str]]:
        """Get conversation context for the LLM."""
        context = []
        
        if include_system and self.messages:
            # Add system message if we have conversation history
            context.append({
                "role": "system",
                "content": "You are a helpful AI assistant. Continue the conversation naturally based on the context provided."
            })
        
        # Return recent messages within window
        recent_messages = self.messages[-self.window_size:]
        for msg in recent_messages:
            context.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return context
    
    def get_summary(self) -> str:
        """Get a summary of the conversation."""
        if not self.messages:
            return "No conversation history."
        
        total_messages = len(self.messages)
        user_messages = len([m for m in self.messages if m["role"] == "user"])
        assistant_messages = len([m for m in self.messages if m["role"] == "assistant"])
        
        return f"Conversation: {total_messages} messages ({user_messages} user, {assistant_messages} assistant)"
    
    def _manage_memory(self):
        """Manage memory by removing old messages if needed."""
        # Simple token estimation (rough)
        total_tokens = sum(len(msg["content"].split()) for msg in self.messages)
        
        # Remove oldest messages if we exceed token limit
        while total_tokens > self.max_tokens and len(self.messages) > 2:
            removed = self.messages.pop(0)
            total_tokens -= len(removed["content"].split())
    
    def clear(self):
        """Clear all conversation history."""
        self.messages.clear()
    
    def export_history(self) -> str:
        """Export conversation history as JSON."""
        return json.dumps({
            "session_info": {
                "created_at": self.created_at.isoformat(),
                "total_messages": len(self.messages),
                "summary": self.get_summary()
            },
            "messages": self.messages
        }, indent=2)
