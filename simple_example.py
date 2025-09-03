"""
Simple Example: Programming Language Debate
==========================================

This is a simple example showing how to modify the conversation topic.
Perfect for beginners who want to try different discussion topics.

Just run: python simple_example.py
"""

import ollama

llama_model = "llama3.2"
deepseek_model = "deepseek-r1:1.5b" 

# Different topic - programming languages
llama_messages = ["What's the best programming language for beginners?"]
deepseek_messages = ["I think Python is great for beginners because of its readable syntax."]

def call_ollama(model, history, system=None):
    messages = [{"role": "system", "content": system}] if system else []
    messages += history
    response = ollama.chat(model=model, messages=messages)
    return response['message']['content']

print("🚀 Programming Language Debate")
print("=" * 40)
print("Topic: What's the best programming language for beginners?")
print("=" * 40)

# Only 3 rounds for this simple example
for _ in range(3):
    # llama3 回答
    llama_history = []
    for u, a in zip(llama_messages, deepseek_messages):
        llama_history.append({"role": "user", "content": u})
        llama_history.append({"role": "assistant", "content": a})
    llama_history.append({"role": "user", "content": llama_messages[-1]})
    llama_reply = call_ollama(llama_model, llama_history)
    print(f"\n🦙 llama3:\n{llama_reply}\n")
    llama_messages.append(llama_reply)

    # deepseek 回答
    deepseek_history = []
    for u, a in zip(deepseek_messages, llama_messages[1:]):  # skip the first llama message
        deepseek_history.append({"role": "user", "content": u})
        deepseek_history.append({"role": "assistant", "content": a})
    deepseek_history.append({"role": "user", "content": deepseek_messages[-1]})
    deepseek_reply = call_ollama(deepseek_model, deepseek_history)
    print(f"\n🤖 deepseek-coder:\n{deepseek_reply}\n")
    deepseek_messages.append(deepseek_reply)

print("✅ Conversation complete!")
print("💡 Try changing the initial topic and messages to explore different discussions!")
