"""
Local LLM Conversation System
============================

A system that creates conversations between different local AI models using Ollama.
This demonstrates how different AI models can have back-and-forth discussions
on various topics, all running locally on your computer.

Features:
- Zero API costs (completely local)
- Privacy-focused (no data sent to external servers)
- Customizable models and conversation topics
- Educational tool for understanding AI model differences

Author: Your Name
Models Used: Llama 3.2 & DeepSeek-R1 (via Ollama)
Cost: $0 per conversation
"""

import ollama
import time
import json
from datetime import datetime
from typing import List, Dict, Optional


class LocalLLMConversation:
    """
    Manages conversations between different local LLM models.
    
    This class orchestrates discussions between AI models, allowing them to
    respond to each other in a natural conversation flow.
    """
    
    def __init__(self, model1: str = "llama3.2", model2: str = "deepseek-r1:1.5b"):
        """
        Initialize the conversation system with two models.
        
        Args:
            model1 (str): First AI model name (default: llama3.2)
            model2 (str): Second AI model name (default: deepseek-r1:1.5b)
        """
        self.model1 = model1
        self.model2 = model2
        self.model1_name = "🦙 Llama"
        self.model2_name = "🤖 DeepSeek"
        
        # Conversation history
        self.model1_messages = []
        self.model2_messages = []
        
        # Verify models are available
        self._check_models()
        
        print(f"🚀 Conversation System Initialized")
        print(f"Model 1: {self.model1_name} ({self.model1})")
        print(f"Model 2: {self.model2_name} ({self.model2})")
        print("=" * 50)
    
    def _check_models(self):
        """Check if required models are available in Ollama."""
        try:
            available_models = ollama.list()
            model_names = [model['name'] for model in available_models['models']]
            
            if self.model1 not in model_names:
                print(f"⚠️  Model {self.model1} not found!")
                print(f"To install: ollama pull {self.model1}")
            
            if self.model2 not in model_names:
                print(f"⚠️  Model {self.model2} not found!")
                print(f"To install: ollama pull {self.model2}")
                
        except Exception as e:
            print(f"❌ Error checking models: {e}")
            print("Make sure Ollama is running: ollama serve")
    
    def call_ollama(self, model: str, history: List[Dict], system: Optional[str] = None) -> str:
        """
        Make a call to an Ollama model with conversation history.
        
        Args:
            model (str): Model name to use
            history (List[Dict]): Conversation history in OpenAI format
            system (Optional[str]): System prompt to guide the model
            
        Returns:
            str: Model's response
        """
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.extend(history)
            
            response = ollama.chat(model=model, messages=messages)
            return response['message']['content']
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def start_conversation(self, 
                         initial_topic: str,
                         initial_response: str,
                         rounds: int = 5,
                         system_prompt1: Optional[str] = None,
                         system_prompt2: Optional[str] = None):
        """
        Start a conversation between the two models.
        
        Args:
            initial_topic (str): The opening question/topic
            initial_response (str): Initial response to start the conversation
            rounds (int): Number of conversation rounds
            system_prompt1 (Optional[str]): System prompt for model 1
            system_prompt2 (Optional[str]): System prompt for model 2
        """
        print(f"🎬 Starting Conversation: {rounds} rounds")
        print(f"📝 Topic: {initial_topic}")
        print("=" * 70)
        
        # Initialize conversation
        self.model1_messages = [initial_topic]
        self.model2_messages = [initial_response]
        
        # Print initial exchange
        print(f"\n💭 Initial Topic:")
        print(f"{initial_topic}")
        print(f"\n{self.model2_name} Initial Response:")
        print(f"{initial_response}")
        
        # Conversation loop
        for round_num in range(1, rounds + 1):
            print(f"\n" + "="*20 + f" ROUND {round_num} " + "="*20)
            
            # Model 1 responds
            model1_history = self._build_history_for_model1()
            model1_reply = self.call_ollama(self.model1, model1_history, system_prompt1)
            
            print(f"\n{self.model1_name}:")
            print(f"{model1_reply}")
            
            self.model1_messages.append(model1_reply)
            
            # Small delay for readability
            time.sleep(1)
            
            # Model 2 responds
            model2_history = self._build_history_for_model2()
            model2_reply = self.call_ollama(self.model2, model2_history, system_prompt2)
            
            print(f"\n{self.model2_name}:")
            print(f"{model2_reply}")
            
            self.model2_messages.append(model2_reply)
            
            # Small delay between rounds
            time.sleep(1)
        
        print(f"\n🎉 Conversation Complete! ({rounds} rounds finished)")
        print("=" * 70)
    
    def _build_history_for_model1(self) -> List[Dict]:
        """Build conversation history from Model 1's perspective."""
        history = []
        
        # Add alternating messages (Model 1 sees Model 2's messages as user input)
        for i, (user_msg, assistant_msg) in enumerate(zip(self.model1_messages, self.model2_messages)):
            history.append({"role": "user", "content": user_msg})
            history.append({"role": "assistant", "content": assistant_msg})
        
        # Add the last user message if exists
        if len(self.model1_messages) > len(self.model2_messages):
            history.append({"role": "user", "content": self.model1_messages[-1]})
        
        return history
    
    def _build_history_for_model2(self) -> List[Dict]:
        """Build conversation history from Model 2's perspective."""
        history = []
        
        # Add alternating messages (Model 2 sees Model 1's messages as user input)
        for i, (user_msg, assistant_msg) in enumerate(zip(self.model2_messages, self.model1_messages[1:])):
            history.append({"role": "user", "content": user_msg})
            history.append({"role": "assistant", "content": assistant_msg})
        
        # Add the last user message if exists
        if len(self.model2_messages) > len(self.model1_messages) - 1:
            history.append({"role": "user", "content": self.model2_messages[-1]})
        
        return history
    
    def save_conversation(self, filename: Optional[str] = None):
        """Save the conversation to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "model1": self.model1,
            "model2": self.model2,
            "model1_messages": self.model1_messages,
            "model2_messages": self.model2_messages,
            "total_rounds": len(self.model1_messages) - 1
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Conversation saved to: {filename}")


def main():
    """
    Main function demonstrating different conversation scenarios.
    """
    print("🤖 LOCAL LLM CONVERSATION SYSTEM")
    print("=" * 50)
    print("This system creates conversations between different AI models")
    print("All processing happens locally - no internet required after setup!")
    print("Cost: $0 per conversation")
    print()
    
    # Initialize conversation system
    conversation = LocalLLMConversation()
    
    # Example 1: Philosophy Discussion
    print("\n🧠 EXAMPLE 1: PHILOSOPHY DISCUSSION")
    conversation.start_conversation(
        initial_topic="Do you think AI will help or hurt humanity in the long run?",
        initial_response="That's a great question. I think it depends on how we build and use it.",
        rounds=3,
        system_prompt1="You are a thoughtful philosopher who considers multiple perspectives.",
        system_prompt2="You are a pragmatic technologist focused on practical implications."
    )
    
    # Save this conversation
    conversation.save_conversation("philosophy_discussion.json")
    
    print("\n" + "="*70)
    print("💡 Try modifying the code to explore different topics!")
    print("💡 Change the models, system prompts, or conversation length")
    print("💡 All conversations are saved as JSON files for later review")


def demo_quick_conversation():
    """Quick demo for testing purposes."""
    conversation = LocalLLMConversation()
    
    conversation.start_conversation(
        initial_topic="What's the most important skill for a programmer?",
        initial_response="I believe problem-solving is fundamental - code is just the tool.",
        rounds=2
    )


if __name__ == "__main__":
    # Run the main demo
    main()
    
    # Uncomment for quick testing:
    # demo_quick_conversation()
