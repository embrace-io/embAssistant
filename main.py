"""
Command-line chat interface for the Ollama Agent
"""

import sys
import os
import signal
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.core.agent import ChatAgent
from config.settings import settings

class ChatCLI:
    def __init__(self):
        self.agent = None
        self.running = True
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print("\n\n👋 Goodbye!")
        self.running = False
        sys.exit(0)
    
    def print_welcome(self):
        """Print welcome message."""
        print("Embrace Assistant")
        print("=" * 50)
        print(f"Model: {settings.OLLAMA_MODEL}")
        print(f"Server: {settings.OLLAMA_BASE_URL}")
        print("\nCommands:")
        print("  /help     - Show this help")
        print("  /clear    - Clear conversation memory")
        print("  /memory   - Show memory summary")
        print("  /export   - Export conversation")
        print("  /models   - List available models")
        print("  /quit     - Exit the chat")
        print("\nType your message and press Enter to chat!")
        print("=" * 50)
    
    def handle_command(self, command: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        command = command.lower().strip()
        
        if command == "/help":
            self.print_welcome()
            return True
        
        elif command == "/clear":
            self.agent.clear_memory()
            return True
        
        elif command == "/memory":
            summary = self.agent.get_memory_summary()
            print(f"🧠 {summary}")
            return True
        
        elif command == "/export":
            history = self.agent.export_conversation()
            filename = f"conversation_{settings.OLLAMA_MODEL.replace(':', '_')}.json"
            with open(filename, 'w') as f:
                f.write(history)
            print(f"💾 Conversation exported to {filename}")
            return True
        
        elif command == "/models":
            models = self.agent.llm_client.list_models()
            if models:
                print("📋 Available models:")
                for model in models:
                    current = " (current)" if model == settings.OLLAMA_MODEL else ""
                    print(f"  - {model}{current}")
            else:
                print("❌ Could not fetch models list")
            return True
        
        elif command in ["/quit", "/exit", "/q"]:
            print("👋 Goodbye!")
            self.running = False
            return True
        
        return False
    
    def run(self):
        """Run the chat CLI."""
        try:
            # Initialize agent
            print("🚀 Initializing Ollama Chat Agent...")
            self.agent = ChatAgent()
            
            # Check if Ollama is available
            if not self.agent.is_ready():
                print("❌ Error: Cannot connect to Ollama server.")
                print(f"   Make sure Ollama is running at {settings.OLLAMA_BASE_URL}")
                print("   You can start Ollama with: ollama serve")
                return
            
            print("✅ Connected to Ollama!")
            self.print_welcome()
            
            # Main chat loop
            while self.running:
                try:
                    # Get user input
                    user_input = input("\n🤔 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle commands
                    if user_input.startswith('/'):
                        self.handle_command(user_input)
                        continue
                    
                    # Process chat message
                    print("🤖 Assistant: ", end="", flush=True)
                    response = self.agent.chat(user_input)
                    print(response)
                    
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        except Exception as e:
            print(f"❌ Fatal error: {e}")
        
        finally:
            if self.agent:
                print(f"\n📊 Final memory summary: {self.agent.get_memory_summary()}")

def main():
    """Main entry point."""
    cli = ChatCLI()
    cli.run()

if __name__ == "__main__":
    main()
