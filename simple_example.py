"""
Simple Example: Quick Start Guide
================================

This is the most basic example of how to use the Local LLM Conversation system.
Perfect for beginners or quick testing.

Just run: python simple_example.py
"""

from llm_conversation import LocalLLMConversation

def main():
    print("🚀 Simple LLM Conversation Example")
    print("=" * 40)
    
    # Create the conversation system
    # This uses the default models: Llama 3.2 and DeepSeek-R1
    chat = LocalLLMConversation()
    
    # Start a simple 2-round conversation
    print("\n💬 Starting a quick debate about programming languages...")
    
    chat.start_conversation(
        initial_topic="What's the best programming language for beginners?",
        initial_response="I think Python is great for beginners because of its readable syntax.",
        rounds=2  # Keep it short for this example
    )
    
    # Save the conversation
    chat.save_conversation("beginner_programming_debate.json")
    
    print("\n✅ Done! Check the generated JSON file for the full conversation.")
    print("💡 Try editing this file to explore different topics!")

if __name__ == "__main__":
    main()
