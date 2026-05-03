---
title: "How to Add Memory to LangChain Prompt Templates for Stateful Conversations"
description: "Unlock truly stateful AI. Discover how to enhance LangChain prompt templates memory, adding continuous context for smarter, more human-like interactions."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain prompt templates memory]
featured: false
image: '/assets/images/langchain-prompt-templates-memory-stateful-conversations.webp'
---

## Giving Your AI Brains: Adding Memory to LangChain Prompt Templates for Smart Conversations

Imagine talking to someone who forgets everything you said a moment ago. That would be a very confusing conversation, right? Large Language Models (LLMs), which are the brains behind many AI tools, are a bit like that by default. They usually don't remember past messages.

This is where **LangChain prompt templates memory** comes in handy! It helps your AI remember what you've talked about, making conversations much smoother and more natural. You can build powerful, **stateful LLM** applications that truly understand context.

### Why Your AI Needs a Good Memory

When you chat with an AI, each question you ask is often treated like a brand new conversation. The AI doesn't automatically know what you mentioned just before. Without a good **conversation memory**, the AI might repeat itself or give answers that don't make sense with your previous questions.

Think of it like reading a story where every page is a new beginning. You wouldn't know what happened to the characters or the plot. To have a continuous story, or a meaningful chat, you need to remember the **chat history**.

This is why giving your AI memory is super important. It lets the AI build on past information, leading to much smarter and more helpful responses. LangChain makes adding this memory surprisingly easy.

### What are LangChain Prompt Templates?

Before we add memory, let's quickly understand prompt templates. A prompt template is like a fill-in-the-blanks form that you use to talk to an AI. It's a set of instructions and questions designed to get the best response from the AI.

For example, a simple template might be: "Translate the following English text to Spanish: '{text}'". You just fill in the `{text}` part. However, these templates usually don't have a spot for remembering old conversations.

They are perfect for one-off questions but struggle with ongoing dialogue. To create a **stateful LLM**, we need to teach these templates to remember.

### How LangChain Adds Memory to Your AI Conversations

LangChain has special tools to give your AI a memory. These tools let the AI keep track of the **chat history** so it can refer back to it. This means your AI can understand the context of your conversation, just like a human would.

The core idea is to put the conversation history directly into the prompt you send to the AI. LangChain helps you manage this history automatically. This is a game-changer for building truly interactive AI applications.

One of the coolest parts is using something called `MessagesPlaceholder`. This is like a special slot in your prompt template where all the past messages will go. It's how you inject **conversation memory** seamlessly.

### Introducing `MessagesPlaceholder`: The Memory Slot

The `MessagesPlaceholder` is a key ingredient when you want to use **LangChain prompt templates memory**. It’s a special instruction you put inside your `ChatPromptTemplate` that tells LangChain, "Hey, put all the past conversation messages right here!" This makes it simple to include the **chat history** without manually adding each message.

Without `MessagesPlaceholder`, you'd have to gather all the old messages yourself and add them to your prompt string. This would be a lot of work and prone to errors. `MessagesPlaceholder` automates this entire process for you, making your life much easier.

It's particularly powerful because it allows LangChain to manage different types of memory and inject them correctly. It makes your prompts flexible and ready for **stateful LLM** interactions.

### Simple Memory: Conversation Buffer

Let's start with a very common and easy-to-use type of **LangChain memory**: `ConversationBufferMemory`. This memory simply stores all the messages in your conversation in a list. It's like keeping a notepad with everything said so far.

This type of memory is great for shorter conversations where you want the AI to remember everything. It's straightforward to set up and perfect for learning how **LangChain prompt templates memory** works. You just tell LangChain to use this buffer, and it handles the rest.

We can link this memory to our prompt template using the `MessagesPlaceholder` we talked about. This combination is how your AI gets its working memory.

### Practical Example 1: Making a Simple AI Remember

Let's see how to make an AI remember using `ConversationBufferMemory` and `MessagesPlaceholder`. First, we need to import some tools from LangChain. We'll use a basic language model for our AI.

{% raw %}
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOllama # Or any other ChatModel
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Set up our AI model
llm = ChatOllama(model="llama2") # You can use "gpt-3.5-turbo" if you have an OpenAI API key
```
{% endraw %}

Now, let's create our prompt template. Notice the `MessagesPlaceholder` named "chat_history". This is where all the previous messages will go.

{% raw %}
```python
# 2. Create a prompt template with a placeholder for memory
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a friendly chatbot that loves to talk about hobbies."),
        MessagesPlaceholder(variable_name="chat_history"), # This is our memory slot!
        ("human", "{input}"),
    ]
)
```
{% endraw %}

Next, we'll create our memory system. We'll use a dictionary to store memory for different session IDs, as `RunnableWithMessageHistory` expects to manage separate conversations. This makes sure each user's chat history is unique.

{% raw %}
```python
# 3. Set up a store for session specific memories
# In a real application, this store might be a database.
store = {}
def get_session_history_for_setup(session_id: str):
    if session_id not in store:
        store[session_id] = ConversationBufferMemory(return_messages=True)
    return store[session_id]

# 4. Create the chain with the LLM and prompt
chain = prompt | llm

# 5. Add memory to the chain using RunnableWithMessageHistory
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history_for_setup, # Function to retrieve or create memory for a session
    input_messages_key="input", # Key for the current user's input
    history_messages_key="chat_history", # Key for the memory placeholder in the prompt
)
```
{% endraw %}

Now let's try it out! You'll see how the AI remembers what we talked about.

{% raw %}
```python
# 6. Have a conversation!
session_id_example = "user_hobby_chat_1"

print(f"User (Session: {session_id_example}): Hi there!")
response1 = chain_with_history.invoke({"input": "Hi there!"}, config={"configurable": {"session_id": session_id_example}})
print(f"AI: {response1.content}\n")

print(f"User (Session: {session_id_example}): My favorite hobby is playing guitar. What do you think about that?")
response2 = chain_with_history.invoke({"input": "My favorite hobby is playing guitar. What do you think about that?"}, config={"configurable": {"session_id": session_id_example}})
print(f"AI: {response2.content}\n")

print(f"User (Session: {session_id_example}): Do you know what my hobby is?")
response3 = chain_with_history.invoke({"input": "Do you know what my hobby is?"}, config={"configurable": {"session_id": session_id_example}})
print(f"AI: {response3.content}\n")

# Let's inspect the memory to see the chat history for this session
print(f"\n--- Current Chat History for '{session_id_example}' ---")
if session_id_example in store:
    for message in store[session_id_example].chat_memory.messages:
        print(f"{message.type}: {message.content}")
else:
    print("No memory found for this session ID.")
```
{% endraw %}

In the example above, you'll notice the AI actually remembered your hobby! This is the power of **LangChain prompt templates memory** at work. The `MessagesPlaceholder` created a dynamic spot for the `chat_history` to be injected into the prompt.

This makes your AI feel much more alive and intelligent. It's a fundamental step towards building truly **stateful LLM** applications.

### Deep Dive: `MessagesPlaceholder` and Its Superpowers

The `MessagesPlaceholder` isn't just a simple tag; it's a powerful feature that makes your prompts much more flexible. When LangChain sees `MessagesPlaceholder`, it knows to grab the current **conversation memory** and insert it there. This happens automatically before the prompt is sent to the LLM.

This is different from just putting a variable like `{history}` in your prompt. If you used `{history}`, you would have to manually format all your past messages into a single string. `MessagesPlaceholder` handles the correct formatting and message types (like `HumanMessage` and `AIMessage`) for you.

It's especially useful when dealing with `ChatPromptTemplate` which expects a list of message objects. This ensures that the AI receives the **chat history** in a format it best understands.

### Practical Example 2: `MessagesPlaceholder` with a `ChatPromptTemplate`

Let's refine our understanding with another clear example using `ChatPromptTemplate` directly. This is often the preferred way to work with chat models in LangChain. We'll explicitly show the role of different message types.

{% raw %}
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessage, HumanMessage, AIMessage
from langchain_community.chat_models import ChatOllama # Or your preferred ChatModel
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Set up our AI model again
llm = ChatOllama(model="llama2")

# Define the ChatPromptTemplate
# Notice how we combine SystemMessage, MessagesPlaceholder, and HumanMessage
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are a helpful assistant who is good at remembering details about the user."),
        MessagesPlaceholder(variable_name="chat_history"), # The crucial memory slot
        HumanMessage(content="{input}"),
    ]
)

# Initialize memory for the conversation
# We'll use a dictionary to store memory for different session IDs
session_store_chat = {}
def get_session_history_chat_func(session_id: str):
    if session_id not in session_store_chat:
        session_store_chat[session_id] = ConversationBufferMemory(return_messages=True)
    return session_store_chat[session_id]

# Create the chain with memory
chain_with_memory = RunnableWithMessageHistory(
    chat_prompt_template | llm,
    get_session_history_chat_func,
    input_messages_key="input",
    history_messages_key="chat_history",
)

print("Starting a new conversation session 'user123'.")

# First turn
user_input_1 = "My name is Alex and I live in New York."
print(f"User: {user_input_1}")
response_1 = chain_with_memory.invoke(
    {"input": user_input_1},
    config={"configurable": {"session_id": "user123"}}
)
print(f"AI: {response_1.content}\n")

# Second turn
user_input_2 = "What city do I live in?"
print(f"User: {user_input_2}")
response_2 = chain_with_memory.invoke(
    {"input": user_input_2},
    config={"configurable": {"session_id": "user123"}}
)
print(f"AI: {response_2.content}\n")

# Third turn - new session to show separation
print("\nStarting a new conversation session 'user456'.")
user_input_3 = "What is my name?"
print(f"User: {user_input_3}")
response_3 = chain_with_memory.invoke(
    {"input": user_input_3},
    config={"configurable": {"session_id": "user456"}}
)
print(f"AI: {response_3.content}\n") # AI should not know the name "Alex" in this new session.

print("\n--- Reviewing Chat History for 'user123' ---")
if "user123" in session_store_chat:
    for message in session_store_chat["user123"].chat_memory.messages:
        print(f"{message.type}: {message.content}")

print("\n--- Reviewing Chat History for 'user456' ---")
if "user456" in session_store_chat:
    for message in session_store_chat["user456"].chat_memory.messages:
        print(f"{message.type}: {message.content}")
else:
    print("Memory for 'user456' is empty or not yet committed, which is expected if the AI didn't respond or if only input was processed without an AI turn yet.")
```
{% endraw %}

In this example, the AI correctly remembers Alex's city in the `user123` session. But when we switch to `user456`, it doesn't know Alex's name because it's a fresh **conversation memory**. This highlights how `RunnableWithMessageHistory` helps manage separate chat sessions, each with its own **LangChain prompt templates memory**.

You can see how easily you can make your AI remember past interactions. This is a crucial step towards building complex AI applications, like agents that can perform multi-step tasks. For more on building such agents, you might want to read about [LangChain Google Gemini Function Calling Agent with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}) or explore [LangGraph StateGraph for Multi-step AI Agent Development]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

### Managing Conversation Memory and State

The `ConversationBufferMemory` we used stores the **chat history** right in your computer's memory. This is great for simple uses and testing. However, for a real application with many users, you wouldn't want to lose all your `conversation memory` if your program restarts.

LangChain offers other types of memory that can save information more permanently. For instance, you could store the history in a database or a file. This ensures that your **stateful LLM** can pick up right where it left off, even after a break.

For now, understanding how `ConversationBufferMemory` works is a perfect start. It teaches you the core concept of bringing **chat history** into your prompts.

### Other Cool LangChain Memory Types

While `ConversationBufferMemory` is simple, LangChain has other clever ways to manage **conversation memory**. Some types summarize the conversation to keep the memory from getting too long. Imagine a very long book; you might only remember the main points, not every single word.

*   **`ConversationSummaryMemory`**: This memory summarizes the conversation as it goes along. It helps keep the prompt short, which is useful for very long chats. The AI creates a summary of the past messages.
*   **`ConversationKMemory`**: This memory only keeps the last "K" number of messages. It's like remembering only the most recent few sentences, letting go of the really old stuff.

Choosing the right `LangChain memory` type depends on your needs. For most simple conversations, `ConversationBufferMemory` is a fantastic start. But for complex applications, these other types become very valuable for managing the **chat history** efficiently.

### When Memory Matters Most

Adding memory to your **LangChain prompt templates memory** isn't just for simple chats. It's vital for many advanced AI applications. Any time you need the AI to carry on a discussion, answer follow-up questions, or build on previous information, memory is a must.

This includes things like personalized customer service bots, interactive storytellers, or smart assistants. If your AI needs to act like it's having a real conversation, it needs to remember. It truly transforms a basic LLM into a **stateful LLM**.

For example, imagine an AI assistant helping you plan a trip. If it remembers your destination and dates, it can answer follow-up questions about hotels or activities much better. This kind of application heavily relies on good **conversation memory**. When building sophisticated applications like RAG (Retrieval Augmented Generation) where context from a knowledge base is combined with chat history, effective memory management is key. You can learn more about RAG applications with LangChain in this post: [Build RAG Applications with LangChain Vector Store]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

### Tips for Using LangChain Memory Effectively

Here are some friendly tips to make the most of **LangChain prompt templates memory**:

*   **Keep your system message clear:** Tell your AI what kind of personality it should have and what its main job is. This helps guide its responses even with memory.
*   **Be mindful of token limits:** If your `conversation memory` gets too long, it might exceed the AI model's "thinking capacity" (called token limit). This can make conversations slow or expensive. Use summary memory for very long chats.
*   **Choose the right memory type:** Start with `ConversationBufferMemory` for simplicity. As your needs grow, explore `ConversationSummaryMemory` or `ConversationKMemory` for better management of **chat history**.
*   **Test different session IDs:** If you're building an app for multiple users, make sure each user's `conversation memory` is separate. `RunnableWithMessageHistory` helps with this, as shown in our example.
*   **Understand `MessagesPlaceholder`:** This is your best friend for inserting memory into `ChatPromptTemplate`. Make sure its `variable_name` matches what you set in your `RunnableWithMessageHistory` (e.g., `history_messages_key`).

By following these tips, you'll be well on your way to building robust and intelligent **stateful LLM** applications.

### Conclusion: Empowering Your AI with Lasting Memories

You've learned how to give your AI a brain that remembers! By using **LangChain prompt templates memory**, especially with the powerful `MessagesPlaceholder` and `ConversationBufferMemory`, you can create **stateful LLM** applications. No more AI forgetting what you just said!

This ability to manage **chat history** and integrate **conversation memory** into your AI's thinking process is a cornerstone of modern AI development. It makes interactions much more natural, helpful, and engaging. LangChain makes this complex task surprisingly approachable.

Now you have the tools to build AIs that truly engage in continuous conversations. Start experimenting, and see the amazing difference memory makes in your AI projects! If you're curious about other ways to enhance LangChain applications, you might be interested in how to handle [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}) or compare LangChain with [Top LangChain Alternatives in 2026]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}). Happy building!