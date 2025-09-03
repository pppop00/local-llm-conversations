"""
Local LLM Conversation System
============================

This creates conversations between different local AI models using Ollama.
Two AI models (Llama 3.2 and DeepSeek-R1) discuss topics back and forth.

Features:
- Zero API costs (completely local)
- Privacy-focused (no data sent to external servers)  
- Educational tool for understanding AI model differences
- Simple code that's easy to understand and modify

Models Used: Llama 3.2 & DeepSeek-R1 (via Ollama)
Cost: $0 per conversation
"""

import ollama

llama_model = "llama3.2"
deepseek_model = "deepseek-r1:1.5b" 

llama_messages = ["Do you think AI will help or hurt humanity in the long run?"]
deepseek_messages = ["That's a great question. I think it depends on how we build and use it."]

def call_ollama(model, history, system=None):
    messages = [{"role": "system", "content": system}] if system else []
    messages += history
    response = ollama.chat(model=model, messages=messages)
    return response['message']['content']

for _ in range(5):
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
