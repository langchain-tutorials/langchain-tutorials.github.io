---
title: "Implement Conversation Memory in LangGraph: Checkpointer Tutorial with Code"
description: "Unlock persistent AI conversations. Our tutorial shows you how to implement langgraph conversation memory checkpointer functionality with clear code examples..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [langgraph conversation memory checkpointer]
featured: false
image: '/assets/images/implement-conversation-memory-langgraph-checkpointer.webp'
---

### Welcome to the World of Persistent Conversations with LangGraph!

Imagine talking to a friend, but every time you pause, they forget everything you've said. That would be frustrating, right? In the world of AI chatbots and complex agents, this "forgetfulness" is a big problem. We need our AI to remember what happened before.

This is where "conversation memory" comes in handy. It lets your AI remember previous turns, context, and even specific details from your chat. Today, we're diving deep into a super important tool in LangGraph that makes this possible: the `langgraph conversation memory checkpointer`.

It's like giving your AI a magical notepad that saves everything important. This tutorial will show you exactly how to use it, step-by-step, with clear examples. You'll learn how to keep your AI conversations flowing smoothly, even if you stop and come back later.

### Understanding LangGraph and Why Memory Matters

LangGraph is a fantastic library that helps you build powerful AI applications. It allows you to design your AI agent as a "graph" of interconnected steps. Each step can do something specific, like understanding a question or looking up information.

Think of it as building a complex machine with different gears and levers. You can define how information flows between these parts. This structured approach helps in building reliable and intelligent systems.

But what if your conversation needs to span across many interactions? What if your AI needs to recall a user's preference mentioned days ago? This is where standard LangGraph, without memory, falls short.

Without memory, each time you interact with your LangGraph agent, it's like starting a brand new conversation. It doesn't remember anything from the past. This makes it impossible for the AI to build on previous exchanges or maintain context, which is essential for natural and effective interactions.

Conversation memory gives your AI the ability to retain context and past information. It's crucial for personalizing experiences, handling multi-turn dialogues, and ensuring continuity. For more on the basics of LangGraph, you might want to check out our [Introduction to LangGraph](internal-link-to-langgraph-basics.md) post.

### The Checkpointer: Your Conversation's Memory Keeper

At the heart of LangGraph's memory system is something called a `Checkpointer`. You can think of a checkpointer as a diligent librarian for your conversations. Its job is to save snapshots of your conversation's current state.

These snapshots, called "checkpoints," contain all the important information about where your conversation is right now. If your application crashes or if you close it and come back later, the checkpointer helps you pick up exactly where you left off. It's a key part of implementing robust `langgraph conversation memory checkpointer` functionality.

This means your AI won't forget what you were talking about. It can seamlessly continue the dialogue, remembering everything from previous turns. It is particularly useful for long-running processes or complex multi-step interactions, ensuring no progress is lost.

#### How Checkpoints Work

A checkpoint is essentially a saved state of your LangGraph. It captures the values of all variables within your graph at a specific moment. When you restart or resume a conversation, the checkpointer loads the latest checkpoint, restoring your graph to that exact state.

This makes your AI applications much more user-friendly and reliable. Users don't have to repeat themselves, and the AI can maintain a consistent understanding of the ongoing dialogue. It transforms ephemeral interactions into persistent, meaningful conversations.

The checkpointer works by taking these snapshots automatically or on demand. Every time your graph progresses through a significant step, a new checkpoint can be created. This detailed saving ensures that even subtle changes in your conversation state are recorded and retrievable.

### Checkpointer Interface Explained

Every checkpointer in LangGraph follows a specific set of rules, much like a job description. This set of rules is called the "Checkpointer interface." It defines exactly what actions any checkpointer must be able to perform.

By having this common interface, LangGraph can work with any type of checkpointer, whether it saves to memory, a database, or even a fancy cloud storage. You don't have to worry about the underlying details; you just know it can save and load. This standard approach makes `langgraph conversation memory checkpointer` implementations flexible.

This interface ensures that all checkpointers behave predictably. It specifies methods like `get` to retrieve a checkpoint and `put` to save one. Knowing this interface is helpful if you ever want to create your own custom checkpointer later on.

The main methods you'll find in the `BaseCheckpointer` interface are:

-   `get(thread_id: str, thread_ts: Optional[str])`: This method is used to fetch a specific checkpoint. You tell it which conversation (`thread_id`) you're interested in, and optionally, a specific moment in time (`thread_ts`).
-   `put(config: RunnableConfig, checkpoint: Checkpoint)`: This is how a checkpointer saves a new snapshot of the conversation. It takes the current configuration and the actual `Checkpoint` data.
-   `list(config: RunnableConfig, filter: Optional[Mapping[str, Any]])`: This method helps you see all the checkpoints available for a particular conversation or based on other filters. It's like looking through your librarian's index cards.
-   `delete(config: RunnableConfig)`: As the name suggests, this method allows you to remove one or more checkpoints. This is important for managing storage and privacy.

Understanding these methods is key to grasping how `langgraph conversation memory checkpointer` operates internally. They provide the framework for all memory operations.

### Built-in Checkpointer Types

LangGraph gives you a couple of ready-to-use checkpointers right out of the box. These are perfect for getting started quickly, and each serves a different purpose. We'll look at `MemorySaver` and `SQLSaver`.

These built-in options cover most common scenarios you'll encounter. They demonstrate how the `Checkpointer` interface works in practice. Choosing the right one depends on your application's needs for persistence and scalability.

#### Using MemorySaver (Ephemeral Memory)

`MemorySaver` is the simplest type of checkpointer. It keeps all the conversation checkpoints in your computer's memory while your program is running. This is great for testing and development because it's fast and easy to set up.

However, once your program stops, all the memory is cleared. It's like writing notes on a whiteboard that gets erased every time you leave the room. So, it's not suitable for applications that need to remember things permanently.

Here's how you can use `MemorySaver` with a simple LangGraph. First, let's define a basic graph that just greets you and asks a question.

```python
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator

# Define the state for our graph
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_name: str

# Define a simple node that processes messages
def greet_and_ask(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None
    
    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content
        if "hello" in user_input.lower():
            response = AIMessage(content=f"Hello there! What's your name?")
        else:
            response = AIMessage(content="I didn't quite catch that. Can you say hello?")
        return {"messages": [response]}
    else:
        # Initial greeting if no user message yet
        return {"messages": [AIMessage(content="Welcome! How can I help you today?")]}

def store_name(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None

    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content
        if "my name is" in user_input.lower():
            name_start_index = user_input.lower().find("my name is") + len("my name is")
            name = user_input[name_start_index:].strip().split(' ')[0]
            if name:
                print(f"DEBUG: Storing name: {name}")
                return {"messages": [AIMessage(content=f"Nice to meet you, {name}! How can I help you further?")], "user_name": name}
        else:
            return {"messages": [AIMessage(content="Could you tell me your name again?")]}
    return {"messages": [AIMessage(content="Waiting for your name.")]}

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("greeter", greet_and_ask)
workflow.add_node("name_collector", store_name)

workflow.add_edge(START, "greeter")
workflow.add_edge("greeter", "name_collector")
workflow.add_edge("name_collector", END) # For simplicity, end here after name

app = workflow.compile()

# Using MemorySaver
memory = MemorySaver()
config = {"configurable": {"thread_id": "user123"}}

# First run: Start a new conversation
print("--- First Run (initial interaction) ---")
inputs1 = {"messages": [HumanMessage(content="Hello")]}
output1 = app.invoke(inputs1, config=config, checkpoint=memory)
print(output1["messages"][-1].content)
print(f"Current state after first run: {app.get_state(config, checkpoint=memory).values}")

# Second run: Continue the conversation with the same thread_id
print("\n--- Second Run (continuing with name) ---")
inputs2 = {"messages": [HumanMessage(content="My name is Alice")]}
output2 = app.invoke(inputs2, config=config, checkpoint=memory)
print(output2["messages"][-1].content)
print(f"Current state after second run: {app.get_state(config, checkpoint=memory).values}")

# Third run: Ask for name again if not provided correctly
print("\n--- Third Run (asking again) ---")
inputs3 = {"messages": [HumanMessage(content="Just Alice")]}
output3 = app.invoke(inputs3, config=config, checkpoint=memory)
print(output3["messages"][-1].content)
print(f"Current state after third run: {app.get_state(config, checkpoint=memory).values}")

# Fourth run: Provide name correctly again
print("\n--- Fourth Run (Alice confirms) ---")
inputs4 = {"messages": [HumanMessage(content="My name is Alice again")]}
output4 = app.invoke(inputs4, config=config, checkpoint=memory)
print(output4["messages"][-1].content)
print(f"Current state after fourth run: {app.get_state(config, checkpoint=memory).values}")
print(f"Final user_name after all runs: {output4.get('user_name', 'Not set')}")
```

In this example, the `MemorySaver` keeps track of the `messages` and `user_name` for "user123". If you were to restart your Python script, all this memory would be gone. This makes it perfect for quick tests, but not for your final application that needs `langgraph conversation memory checkpointer` persistence.

You can see how the state evolves across different `invoke` calls for the same `thread_id`. The `checkpoint=memory` argument tells LangGraph to use our `MemorySaver` instance. This implicitly saves the state after each step and loads it before the next step.

#### Using SQLSaver (Persistent Memory)

`SQLSaver` is a much more robust option for storing your conversation memory. It saves checkpoints into a database, usually a SQLite file for simplicity, or a more powerful database like PostgreSQL for large applications. This means the memory persists even if your program stops or crashes.

It's like writing your notes in a permanent notebook that you can always come back to. This is the checkpointer you'll typically use for production-ready `langgraph conversation memory checkpointer` applications. It ensures your users' conversation history is always available.

To use `SQLSaver`, you need to set up a database connection. For this example, we'll use SQLite, which stores everything in a single file. You usually specify a connection string to tell `SQLSaver` where your database is.

```python
import sqlite3
import os
from langgraph.checkpoint import SQLSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator

# Redefine the AgentState and graph nodes for clarity, or assume they are the same as above
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_name: str
    item_requested: str
    order_id: str

def greet_customer(state: AgentState):
    messages = state['messages']
    if not messages:
        return {"messages": [AIMessage(content="Hello! How can I help you today?")]}
    return {} # No change if already greeted

def process_request(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None
    
    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content.lower()
        if "coffee" in user_input or "tea" in user_input:
            item = "coffee" if "coffee" in user_input else "tea"
            return {"messages": [AIMessage(content=f"Sure, I can help you with {item}. Any specific type?")], "item_requested": item}
        elif "my name is" in user_input:
            # Re-process name if not caught before or if user repeats
            name_start_index = user_input.find("my name is") + len("my name is")
            name = user_input[name_start_index:].strip().split(' ')[0]
            if name:
                return {"messages": [AIMessage(content=f"Got it, your name is {name}. How can I help you?"),
                                     HumanMessage(content=user_input)], # Add user message back
                        "user_name": name}
        elif state.get("user_name"):
            return {"messages": [AIMessage(content=f"Okay, {state['user_name']}, what else can I do for you?")]}
        else:
            return {"messages": [AIMessage(content="I'm not sure what you mean. Can you ask me for something?")]}
    return {}

def finalize_order(state: AgentState):
    item = state.get("item_requested")
    name = state.get("user_name", "customer")
    if item:
        order_id = "ORD" + str(hash(item + name))[:5] # Simple unique ID
        return {"messages": [AIMessage(content=f"Alright, {name}! Your {item} order is placed. Your order ID is {order_id}.")],
                "order_id": order_id}
    return {"messages": [AIMessage(content="I need to know what you want to order first.")]}


# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("greeter", greet_customer)
workflow.add_node("request_processor", process_request)
workflow.add_node("order_finalizer", finalize_order)

workflow.add_edge(START, "greeter")
workflow.add_edge("greeter", "request_processor")
workflow.add_conditional_edges(
    "request_processor",
    lambda state: "order_finalizer" if state.get("item_requested") else END,
    {
        "order_finalizer": "order_finalizer",
        END: END
    }
)
workflow.add_edge("order_finalizer", END)

app_sql = workflow.compile()

# Define the path for our SQLite database
DB_FILE = "langgraph_checkpoints.sqlite"
if os.path.exists(DB_FILE):
    os.remove(DB_FILE) # Clean up previous run for fresh start

# Using SQLSaver
# Ensure the database file exists, or it will be created
try:
    conn = sqlite3.connect(DB_FILE)
    conn.close()
except sqlite3.Error as e:
    print(f"Error connecting to SQLite: {e}")
    exit()

memory_sql = SQLSaver.from_conn_string(f"sqlite:///{DB_FILE}")

thread_id_user = "customer_alice_1"
config_sql = {"configurable": {"thread_id": thread_id_user}}

print("--- First Session (ordering coffee) ---")
# User says hello and provides name
inputs_s1_1 = {"messages": [HumanMessage(content="Hello, my name is Alice")]}
output_s1_1 = app_sql.invoke(inputs_s1_1, config=config_sql, checkpoint=memory_sql)
print(f"AI: {output_s1_1['messages'][-1].content}")
print(f"Current state: {app_sql.get_state(config_sql, checkpoint=memory_sql).values}")

# User requests coffee
inputs_s1_2 = {"messages": [HumanMessage(content="I'd like a coffee")]}
output_s1_2 = app_sql.invoke(inputs_s1_2, config=config_sql, checkpoint=memory_sql)
print(f"AI: {output_s1_2['messages'][-1].content}")
print(f"Current state: {app_sql.get_state(config_sql, checkpoint=memory_sql).values}")

print("\n--- Simulating Application Restart ---")
# In a real app, you would close and reopen.
# Here, we just create a new app instance or re-initialize parts to show persistence
# The `memory_sql` object is already connected to the file, so it retains state.
# Let's verify by checking the state directly from the checkpointer
reloaded_state = app_sql.get_state(config_sql, checkpoint=memory_sql).values
print(f"Reloaded state shows name: {reloaded_state.get('user_name')}, item: {reloaded_state.get('item_requested')}")

print("\n--- Second Session (continuing the order) ---")
# Continue the conversation with the same thread_id
inputs_s2_1 = {"messages": [HumanMessage(content="Yes, a latte please")]} # This input is ignored by 'finalize_order'
output_s2_1 = app_sql.invoke(inputs_s2_1, config=config_sql, checkpoint=memory_sql)
print(f"AI: {output_s2_1['messages'][-1].content}")
print(f"Current state: {app_sql.get_state(config_sql, checkpoint=memory_sql).values}")

print(f"\nFinal state for {thread_id_user}: {app_sql.get_state(config_sql, checkpoint=memory_sql).values}")

# Clean up the database file
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"\nCleaned up {DB_FILE}")
```
In this `SQLSaver` example, the `thread_id` "customer_alice_1" keeps the conversation state safe in the `langgraph_checkpoints.sqlite` file. Even if you completely restart your Python script, as long as you connect to the same database file, the conversation will be loaded from where it left off. This is the power of persistent `langgraph conversation memory checkpointer`.

### Checkpoint Data Structure

When a `langgraph conversation memory checkpointer` saves a snapshot, what exactly does it put into that snapshot? It's not just a single piece of information. A checkpoint is a carefully organized bundle of data that captures the complete state of your graph at a specific moment.

Think of it like a complete backup of your game save file. It needs to know your score, your inventory, your location, and everything else needed to jump right back into the game. The same applies to your LangGraph's conversation memory.

The core of a checkpoint is the `values` dictionary. This dictionary holds the current state of your graph, which corresponds to the `AgentState` you defined. For instance, in our examples, this would include the `messages` list, `user_name`, `item_requested`, and `order_id`.

Beyond the `values`, a checkpoint also contains metadata. This metadata includes `thread_id` (which conversation it belongs to), `thread_ts` (the timestamp when it was saved), and potentially `parent_ts` (if it branched off an earlier state). These pieces of information are vital for loading previous states and understanding the history of a conversation. It's how `langgraph conversation memory checkpointer` keeps track of everything.

Here's a simplified look at what a checkpoint might contain:

```json
{
  "thread_id": "customer_alice_1",
  "thread_ts": "2023-10-27T10:30:00.123456Z",
  "parent_ts": null, // Or an earlier thread_ts if branching
  "values": {
    "messages": [
      {
        "type": "human",
        "content": "Hello, my name is Alice"
      },
      {
        "type": "ai",
        "content": "Hello Alice! How can I help you today?"
      },
      {
        "type": "human",
        "content": "I'd like a coffee"
      },
      {
        "type": "ai",
        "content": "Sure, I can help you with coffee. Any specific type?"
      }
    ],
    "user_name": "Alice",
    "item_requested": "coffee",
    "order_id": null
  },
  "versions_seen": {
    "greeter": "2023-10-27T10:29:58.000000Z",
    "request_processor": "2023-10-27T10:29:59.000000Z"
  }
}
```

This structure allows LangGraph to precisely restore the graph's execution flow. It captures not just the data, but also the historical path taken through the graph's nodes. This detailed record is essential for the robust `langgraph conversation memory checkpointer` functionality.

### Saving Checkpoints

You might be wondering when and how these checkpoints get saved. The good news is that LangGraph handles much of this automatically when you use a checkpointer. Every time you invoke your compiled graph with a `checkpoint` object and a `thread_id`, LangGraph takes care of saving the state.

Specifically, after each node in your graph finishes its work, LangGraph will typically save a new checkpoint. This means your conversation progress is continuously being backed up. This automatic saving ensures that you don't lose much progress if an error occurs.

The `thread_id` in your configuration is key here. It tells the `langgraph conversation memory checkpointer` which specific conversation to save or load. Without it, the checkpointer wouldn't know which memory to use, or it would treat every interaction as a new conversation.

Let's illustrate with a simple example. We'll reuse our `app_sql` and `memory_sql` from before, but pay closer attention to the `thread_ts` values. Each invocation will generate a new checkpoint, marked by a unique timestamp.

```python
import os
from langgraph.checkpoint import SQLSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator
import datetime

# Assume AgentState and graph workflow are defined as in the SQLSaver example

# Define the path for our SQLite database
DB_FILE_SAVE = "langgraph_save_checkpoints.sqlite"
if os.path.exists(DB_FILE_SAVE):
    os.remove(DB_FILE_SAVE) # Clean up previous run for fresh start

memory_sql_save = SQLSaver.from_conn_string(f"sqlite:///{DB_FILE_SAVE}")

# Rebuild the app for this example if it wasn't global or imported
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_name: str
    item_requested: str
    order_id: str

def greet_customer(state: AgentState):
    messages = state['messages']
    if not messages:
        return {"messages": [AIMessage(content="Hello! How can I help you today?")]}
    # No changes if already greeted, just pass through
    return {"messages": messages} 

def process_request(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None
    
    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content.lower()
        if "coffee" in user_input or "tea" in user_input:
            item = "coffee" if "coffee" in user_input else "tea"
            return {"messages": [AIMessage(content=f"Sure, I can help you with {item}. Any specific type?")], "item_requested": item}
        elif "my name is" in user_input and not state.get("user_name"): # Only set if not already set
            name_start_index = user_input.find("my name is") + len("my name is")
            name = user_input[name_start_index:].strip().split(' ')[0]
            if name:
                return {"messages": [AIMessage(content=f"Got it, your name is {name}. How can I help you?")] , "user_name": name}
        elif state.get("user_name"):
            return {"messages": [AIMessage(content=f"Okay, {state['user_name']}, what else can I do for you?")]}
        else:
            return {"messages": [AIMessage(content="I'm not sure what you mean. Can you ask me for something?")]}
    return {} # No changes if no new human message

def finalize_order(state: AgentState):
    item = state.get("item_requested")
    name = state.get("user_name", "customer")
    if item:
        order_id = "ORD" + str(hash(item + name))[:5] # Simple unique ID
        return {"messages": [AIMessage(content=f"Alright, {name}! Your {item} order is placed. Your order ID is {order_id}.")],
                "order_id": order_id}
    return {"messages": [AIMessage(content="I need to know what you want to order first.")]}

# Build the graph
workflow_save = StateGraph(AgentState)
workflow_save.add_node("greeter", greet_customer)
workflow_save.add_node("request_processor", process_request)
workflow_save.add_node("order_finalizer", finalize_order)

workflow_save.add_edge(START, "greeter")
workflow_save.add_edge("greeter", "request_processor")
workflow_save.add_conditional_edges(
    "request_processor",
    lambda state: "order_finalizer" if state.get("item_requested") else END,
    {
        "order_finalizer": "order_finalizer",
        END: END
    }
)
workflow_save.add_edge("order_finalizer", END)

app_save = workflow_save.compile()

# Thread ID for this example
thread_id_save = "user_saving_demo"
config_save = {"configurable": {"thread_id": thread_id_save}}

print("--- Saving Checkpoints Demo ---")

# Step 1: Initial greeting and name
print("\nStep 1: User says hello and name")
inputs1 = {"messages": [HumanMessage(content="Hi, my name is Bob")]}
output1 = app_save.invoke(inputs1, config=config_save, checkpoint=memory_sql_save)
print(f"AI: {output1['messages'][-1].content}")
# Check the latest checkpoint
latest_checkpoint1 = memory_sql_save.get(thread_id_save, None) # None gets the latest
print(f"Latest checkpoint after Step 1 (thread_ts): {latest_checkpoint1['thread_ts']}")
print(f"User name in state: {latest_checkpoint1['values'].get('user_name')}")


# Step 2: User requests an item
print("\nStep 2: User requests an item")
inputs2 = {"messages": [HumanMessage(content="I want tea please")]}
output2 = app_save.invoke(inputs2, config=config_save, checkpoint=memory_sql_save)
print(f"AI: {output2['messages'][-1].content}")
# Check the latest checkpoint
latest_checkpoint2 = memory_sql_save.get(thread_id_save, None)
print(f"Latest checkpoint after Step 2 (thread_ts): {latest_checkpoint2['thread_ts']}")
print(f"Item requested in state: {latest_checkpoint2['values'].get('item_requested')}")

# Step 3: Finalize order
print("\nStep 3: Finalize order (automatic continuation)")
# No new user input, the graph automatically finalizes based on previous state
# Note: In this specific graph, the 'finalize_order' is reached after 'request_processor' 
# if 'item_requested' is present.
# To demonstrate a separate 'invoke' that *continues* and reaches a new state,
# we need a more complex graph or ensure 'finalize_order' isn't reached immediately.
# Let's adjust the graph to pause after request, asking for confirmation.

# For now, let's just invoke with an empty message to trigger subsequent nodes if they were reachable
# This will likely finalize the order based on the previous state.
inputs3 = {"messages": [HumanMessage(content="Ok")]} # User acknowledges
output3 = app_save.invoke(inputs3, config=config_save, checkpoint=memory_sql_save)
print(f"AI: {output3['messages'][-1].content}")
# Check the latest checkpoint
latest_checkpoint3 = memory_sql_save.get(thread_id_save, None)
print(f"Latest checkpoint after Step 3 (thread_ts): {latest_checkpoint3['thread_ts']}")
print(f"Order ID in state: {latest_checkpoint3['values'].get('order_id')}")

print("\n--- Listing all checkpoints for this thread ---")
all_checkpoints = memory_sql_save.list({"configurable": {"thread_id": thread_id_save}})
for cp in all_checkpoints:
    print(f"  Thread TS: {cp['thread_ts']}, User Name: {cp['values'].get('user_name')}, Item: {cp['values'].get('item_requested')}, Order ID: {cp['values'].get('order_id')}")

# Clean up the database file
if os.path.exists(DB_FILE_SAVE):
    os.remove(DB_FILE_SAVE)
    print(f"\nCleaned up {DB_FILE_SAVE}")
```
As you run this code, you'll see different `thread_ts` values for each step. Each `thread_ts` represents a distinct snapshot of your conversation. This automatic saving mechanism is a core feature of `langgraph conversation memory checkpointer`, providing a robust backbone for your AI.

### Loading Previous States

The ability to save checkpoints wouldn't be very useful if you couldn't load them back later! This is where the magic of `langgraph conversation memory checkpointer` truly shines. You can instruct LangGraph to start a new interaction not from scratch, but from a specific saved point in time.

To load a previous state, you simply provide the `thread_id` to your graph's `invoke` or `stream` methods. LangGraph will then look up the latest checkpoint associated with that `thread_id` and restore your graph to that state. It's like pressing "continue game" in a video game.

If you want to load an even older state (for example, to explore a different conversation path), you can also specify a `thread_ts`. This is very powerful for debugging or for implementing features like "undo" or "revert" in your AI. You'll learn more about this in the "Checkpoint Versioning" section.

Let's see how loading previous states works in practice. We'll simulate restarting our application and continuing a conversation from where we left off, using the `SQLSaver`.

```python
import os
from langgraph.checkpoint import SQLSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator
import datetime

# Assume AgentState and graph workflow are defined as in the SQLSaver example (same as previous section)

# Define the path for our SQLite database
DB_FILE_LOAD = "langgraph_load_checkpoints.sqlite"
if os.path.exists(DB_FILE_LOAD):
    os.remove(DB_FILE_LOAD) # Clean up previous run for fresh start

memory_sql_load = SQLSaver.from_conn_string(f"sqlite:///{DB_FILE_LOAD}")

# Rebuild the app if necessary
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_name: str
    item_requested: str
    order_id: str

def greet_customer(state: AgentState):
    messages = state['messages']
    if not messages:
        return {"messages": [AIMessage(content="Hello! How can I help you today?")]}
    return {} 

def process_request(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None
    
    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content.lower()
        if "coffee" in user_input or "tea" in user_input:
            item = "coffee" if "coffee" in user_input else "tea"
            return {"messages": [AIMessage(content=f"Sure, I can help you with {item}. Any specific type?")], "item_requested": item}
        elif "my name is" in user_input and not state.get("user_name"):
            name_start_index = user_input.find("my name is") + len("my name is")
            name = user_input[name_start_index:].strip().split(' ')[0]
            if name:
                return {"messages": [AIMessage(content=f"Got it, your name is {name}. How can I help you?")] , "user_name": name}
        elif state.get("user_name"):
            return {"messages": [AIMessage(content=f"Okay, {state['user_name']}, what else can I do for you?")]}
        else:
            return {"messages": [AIMessage(content="I'm not sure what you mean. Can you ask me for something?")]}
    return {}

def finalize_order(state: AgentState):
    item = state.get("item_requested")
    name = state.get("user_name", "customer")
    if item:
        order_id = "ORD" + str(hash(item + name))[:5]
        return {"messages": [AIMessage(content=f"Alright, {name}! Your {item} order is placed. Your order ID is {order_id}.")],
                "order_id": order_id}
    return {"messages": [AIMessage(content="I need to know what you want to order first.")]}

# Build the graph
workflow_load = StateGraph(AgentState)
workflow_load.add_node("greeter", greet_customer)
workflow_load.add_node("request_processor", process_request)
workflow_load.add_node("order_finalizer", finalize_order)

workflow_load.add_edge(START, "greeter")
workflow_load.add_edge("greeter", "request_processor")
workflow_load.add_conditional_edges(
    "request_processor",
    lambda state: "order_finalizer" if state.get("item_requested") else END,
    {
        "order_finalizer": "order_finalizer",
        END: END
    }
)
workflow_load.add_edge("order_finalizer", END)

app_load = workflow_load.compile()

# Thread ID for this example
thread_id_load = "user_loading_demo"
config_load = {"configurable": {"thread_id": thread_id_load}}

print("--- Initial Session (creating checkpoints) ---")
# Part 1: Initial conversation
inputs_l1_1 = {"messages": [HumanMessage(content="Hello, my name is Carol")]}
app_load.invoke(inputs_l1_1, config=config_load, checkpoint=memory_sql_load)
print(f"State after name: {app_load.get_state(config_load, checkpoint=memory_sql_load).values.get('user_name')}")

inputs_l1_2 = {"messages": [HumanMessage(content="I'd like a tea")]}
app_load.invoke(inputs_l1_2, config=config_load, checkpoint=memory_sql_load)
print(f"State after item request: {app_load.get_state(config_load, checkpoint=memory_sql_load).values.get('item_requested')}")

inputs_l1_3 = {"messages": [HumanMessage(content="Yes, please finalize")]}
output_l1_3 = app_load.invoke(inputs_l1_3, config=config_load, checkpoint=memory_sql_load)
print(f"AI: {output_l1_3['messages'][-1].content}")
print(f"State after finalization: {app_load.get_state(config_load, checkpoint=memory_sql_load).values.get('order_id')}")

print("\n--- Simulating Application Restart and Loading ---")
# Here, you would normally restart your script.
# We'll just create a new `app_load_restarted` instance to emphasize loading from disk.
# The memory_sql_load object already points to the persistent database.

# Load the latest state for 'user_loading_demo'
current_state = app_load.get_state(config_load, checkpoint=memory_sql_load).values
print(f"Current state loaded: User Name: {current_state.get('user_name')}, Item: {current_state.get('item_requested')}, Order ID: {current_state.get('order_id')}")

print("\n--- Continuing the conversation ---")
inputs_l2_1 = {"messages": [HumanMessage(content="Can I also get a receipt?")]}
output_l2_1 = app_load.invoke(inputs_l2_1, config=config_load, checkpoint=memory_sql_load)
print(f"AI: {output_l2_1['messages'][-1].content}")
print(f"State after new input: {app_load.get_state(config_load, checkpoint=memory_sql_load).values.get('messages')[-1].content}")


# Clean up the database file
if os.path.exists(DB_FILE_LOAD):
    os.remove(DB_FILE_LOAD)
    print(f"\nCleaned up {DB_FILE_LOAD}")
```
Notice how the second "session" automatically knows "Carol" and "tea" and "ORD..." without those details being explicitly passed as input. This demonstrates the seamless loading capability of the `langgraph conversation memory checkpointer`. You simply pass the `thread_id`, and LangGraph does the rest, fetching the latest state.

### Checkpoint Versioning

Every checkpoint saved by the `langgraph conversation memory checkpointer` comes with a unique timestamp called `thread_ts`. This timestamp is more than just a label; it's a version marker. It tells you exactly when that specific state of your conversation was saved.

Why is this important? Because it allows you to travel back in time! Instead of always loading the *latest* state, you can specify an older `thread_ts` to revert your conversation to an earlier point. This is incredibly powerful for several advanced use cases.

Imagine a scenario where a user makes a mistake or changes their mind halfway through a complex process. With checkpoint versioning, you can offer them an "undo" feature. You simply load the checkpoint from before their mistake and let them try again. This flexibility is a hallmark of a robust `langgraph conversation memory checkpointer` system.

#### Branching Conversations

Checkpoint versioning also enables something called "branching conversations." This means you can take a conversation up to a certain point, save it, and then explore different paths from that same point. Each new path would generate new checkpoints, but they would all trace back to that original shared checkpoint.

This is invaluable for A/B testing different agent behaviors or for allowing users to explore "what if" scenarios. You can save a checkpoint, try one answer, then go back to the saved point and try a different answer, creating parallel timelines for the same original conversation.

Let's demonstrate loading an older checkpoint.

```python
import os
from langgraph.checkpoint import SQLSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator
import time # For slight delays to ensure distinct thread_ts

# Assume AgentState and graph workflow are defined as before

# Define the path for our SQLite database
DB_FILE_VERSION = "langgraph_version_checkpoints.sqlite"
if os.path.exists(DB_FILE_VERSION):
    os.remove(DB_FILE_VERSION) # Clean up previous run for fresh start

memory_sql_version = SQLSaver.from_conn_string(f"sqlite:///{DB_FILE_VERSION}")

# Rebuild the app for this example if needed (same as previous sections)
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_name: str
    item_requested: str
    order_id: str

def greet_customer(state: AgentState):
    messages = state['messages']
    if not messages:
        return {"messages": [AIMessage(content="Hello! How can I help you today?")]}
    return {} 

def process_request(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None
    
    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content.lower()
        if "coffee" in user_input or "tea" in user_input:
            item = "coffee" if "coffee" in user_input else "tea"
            return {"messages": [AIMessage(content=f"Sure, I can help you with {item}. Any specific type?")], "item_requested": item}
        elif "my name is" in user_input and not state.get("user_name"):
            name_start_index = user_input.find("my name is") + len("my name is")
            name = user_input[name_start_index:].strip().split(' ')[0]
            if name:
                return {"messages": [AIMessage(content=f"Got it, your name is {name}. How can I help you?")] , "user_name": name}
        elif state.get("user_name"):
            return {"messages": [AIMessage(content=f"Okay, {state['user_name']}, what else can I do for you?")]}
        else:
            return {"messages": [AIMessage(content="I'm not sure what you mean. Can you ask me for something?")]}
    return {}

def finalize_order(state: AgentState):
    item = state.get("item_requested")
    name = state.get("user_name", "customer")
    if item:
        order_id = "ORD" + str(hash(item + name))[:5]
        return {"messages": [AIMessage(content=f"Alright, {name}! Your {item} order is placed. Your order ID is {order_id}.")],
                "order_id": order_id}
    return {"messages": [AIMessage(content="I need to know what you want to order first.")]}

# Build the graph
workflow_version = StateGraph(AgentState)
workflow_version.add_node("greeter", greet_customer)
workflow_version.add_node("request_processor", process_request)
workflow_version.add_node("order_finalizer", finalize_order)

workflow_version.add_edge(START, "greeter")
workflow_version.add_edge("greeter", "request_processor")
workflow_version.add_conditional_edges(
    "request_processor",
    lambda state: "order_finalizer" if state.get("item_requested") else END,
    {
        "order_finalizer": "order_finalizer",
        END: END
    }
)
workflow_version.add_edge("order_finalizer", END)

app_version = workflow_version.compile()

thread_id_version = "user_versioning_demo"
config_version = {"configurable": {"thread_id": thread_id_version}}

print("--- Initial conversation path ---")
# Step 1: User introduces self
inputs_v1_1 = {"messages": [HumanMessage(content="Hi, I'm David")]}
app_version.invoke(inputs_v1_1, config=config_version, checkpoint=memory_sql_version)
time.sleep(0.1) # Ensure distinct timestamps

# Step 2: User asks for coffee
inputs_v1_2 = {"messages": [HumanMessage(content="I'd like a coffee")]}
app_version.invoke(inputs_v1_2, config=config_version, checkpoint=memory_sql_version)
time.sleep(0.1)

# Save the thread_ts of this checkpoint (after item request but before finalization)
checkpoints = memory_sql_version.list(config_version)
coffee_request_ts = None
for cp in checkpoints:
    if cp['values'].get('item_requested') == 'coffee':
        coffee_request_ts = cp['thread_ts']
        break
print(f"Checkpoint 'coffee_request_ts' captured: {coffee_request_ts}")


# Step 3: User confirms coffee order (path 1)
inputs_v1_3 = {"messages": [HumanMessage(content="Yes, a black coffee")]}
app_version.invoke(inputs_v1_3, config=config_version, checkpoint=memory_sql_version)
output_path1 = app_version.get_state(config_version, checkpoint=memory_sql_version).values
print(f"Path 1 (Coffee) final order ID: {output_path1.get('order_id')}")
print(f"Path 1 final state: {output_path1}")

print("\n--- Branching to an earlier point (Tea order) ---")
# To branch, we need to invoke with an older thread_ts.
# This means we'll explicitly load the state *before* the coffee request and then provide a different input.
# The 'thread_ts' for the state before coffee request is usually the one where the name was set.
# Let's get the checkpoint before 'coffee_request_ts'
name_set_ts = None
for cp in checkpoints:
    if cp['values'].get('user_name') == 'David' and not cp['values'].get('item_requested'):
        name_set_ts = cp['thread_ts']
        break
print(f"Checkpoint 'name_set_ts' captured: {name_set_ts}")

if name_set_ts:
    # Set the config to load the state from 'name_set_ts'
    config_branch = {"configurable": {"thread_id": thread_id_version, "thread_ts": name_set_ts}}
    
    # Check loaded state
    loaded_state_for_branch = app_version.get_state(config_branch, checkpoint=memory_sql_version).values
    print(f"State loaded for branching (ts={name_set_ts}): {loaded_state_for_branch.get('user_name')}, {loaded_state_for_branch.get('item_requested')}")

    # Now, invoke with a *different* request: "tea"
    inputs_v2_1 = {"messages": [HumanMessage(content="Actually, I'd prefer a tea")]}
    output_path2 = app_version.invoke(inputs_v2_1, config=config_branch, checkpoint=memory_sql_version)
    print(f"Path 2 (Tea) final order ID: {output_path2.get('order_id')}")
    print(f"Path 2 final state: {output_path2}")

    # Verify that a new branch was created - the coffee path and tea path should both exist
    print("\n--- Verifying both branches exist ---")
    all_final_checkpoints = memory_sql_version.list(config_version)
    for cp in all_final_checkpoints:
        print(f"  Thread TS: {cp['thread_ts']}, User Name: {cp['values'].get('user_name')}, Item: {cp['values'].get('item_requested')}, Order ID: {cp['values'].get('order_id')}, Parent TS: {cp.get('parent_ts')}")

else:
    print("Could not find suitable checkpoint for branching.")


# Clean up the database file
if os.path.exists(DB_FILE_VERSION):
    os.remove(DB_FILE_VERSION)
    print(f"\nCleaned up {DB_FILE_VERSION}")
```
This example clearly shows how you can load an older state using `thread_ts` and then continue the conversation from there. This creates a new "branch" of the conversation, effectively giving you multiple histories for the same `thread_id`. This is incredibly powerful for complex `langgraph conversation memory checkpointer` designs.

### Custom Checkpointer Creation

While LangGraph's built-in `MemorySaver` and `SQLSaver` are great, you might find yourself in a situation where you need something different. Perhaps your application uses a specific NoSQL database, a cloud storage service like S3, or you have unique security requirements. In these cases, you'll want to create a "custom checkpointer."

Creating a custom `langgraph conversation memory checkpointer` allows you to integrate LangGraph's memory system with virtually any data storage solution. It means you have complete control over how and where your conversation history is stored. It's like building your own custom librarian system tailored to your specific needs.

To build a custom checkpointer, you need to follow the `Checkpointer` interface we discussed earlier. This means your custom class must implement the `get`, `put`, `list`, and `delete` methods. LangGraph expects these methods to be present and to function correctly. This is a powerful feature for extending the `langgraph conversation memory checkpointer` capabilities.

#### Understanding the `BaseCheckpointer` Abstract Methods

Before diving into code, let's briefly recap the methods you *must* implement when inheriting from `BaseCheckpointer`:

-   `get(thread_id: str, thread_ts: Optional[str]) -> Optional[Checkpoint]`: This method should retrieve a single checkpoint. If `thread_ts` is `None`, it should return the latest checkpoint for the given `thread_id`. Otherwise, it returns the specific checkpoint for that `thread_id` and `thread_ts`. If no checkpoint is found, it returns `None`.
-   `put(config: RunnableConfig, checkpoint: Checkpoint) -> RunnableConfig`: This method is responsible for saving a `Checkpoint` object. It receives the `RunnableConfig` (which includes the `thread_id`) and the `Checkpoint` itself. It should store this checkpoint persistently. It returns the updated `RunnableConfig` which might include the `thread_ts` of the newly saved checkpoint.
-   `list(config: RunnableConfig, filter: Optional[Mapping[str, Any]] = None) -> List[Checkpoint]`: This method should return a list of checkpoints. It takes a `RunnableConfig` (primarily for `thread_id`) and an optional `filter` dictionary. You should use these to retrieve relevant checkpoints, often for a specific `thread_id`.
-   `delete(config: RunnableConfig) -> None`: This method deletes checkpoints. It receives a `RunnableConfig`, which will typically contain the `thread_id` and optionally a `thread_ts` to delete a specific checkpoint or all checkpoints for a thread.

These methods form the backbone of any `langgraph conversation memory checkpointer` implementation. Ensuring they are correctly implemented is crucial for the stability and functionality of your custom memory system.

#### A Simple File-Based Custom Checkpointer

Let's create a custom checkpointer that saves each checkpoint as a separate JSON file in a directory. This is simpler than a database but demonstrates the principles of custom checkpointer creation.

```python
import json
import os
import datetime
from typing import Any, Optional, Mapping, List, Dict
from langgraph.checkpoint import BaseCheckpointSaver, Checkpoint
from langchain_core.runnables import RunnableConfig

# Define the directory where checkpoints will be saved
CHECKPOINT_DIR = "custom_checkpoints"

class FileCheckpointSaver(BaseCheckpointSaver):
    def __init__(self, checkpoint_dir: str = CHECKPOINT_DIR):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        print(f"FileCheckpointSaver initialized. Checkpoints will be saved in: {self.checkpoint_dir}")

    def _get_file_path(self, thread_id: str, thread_ts: str) -> str:
        return os.path.join(self.checkpoint_dir, f"{thread_id}_{thread_ts}.json")

    def get(self, thread_id: str, thread_ts: Optional[str] = None) -> Optional[Checkpoint]:
        # print(f"FileCheckpointSaver.get called for thread_id={thread_id}, thread_ts={thread_ts}")
        checkpoints_for_thread = self.list({"configurable": {"thread_id": thread_id}})

        if not checkpoints_for_thread:
            # print(f"No checkpoints found for thread_id={thread_id}")
            return None

        if thread_ts is None:
            # Return the latest checkpoint for the thread
            latest_cp = max(checkpoints_for_thread, key=lambda cp: cp["thread_ts"])
            # print(f"Returning latest checkpoint for {thread_id}: {latest_cp['thread_ts']}")
            return latest_cp
        else:
            # Return a specific checkpoint
            for cp in checkpoints_for_thread:
                if cp["thread_ts"] == thread_ts:
                    # print(f"Returning specific checkpoint for {thread_id} at {thread_ts}")
                    return cp
            # print(f"Specific checkpoint not found for {thread_id} at {thread_ts}")
            return None

    def put(self, config: RunnableConfig, checkpoint: Checkpoint) -> RunnableConfig:
        thread_id = config["configurable"]["thread_id"]
        # LangGraph automatically adds thread_ts to the checkpoint object
        # but we might need to ensure it's there or generate if missing for some reason.
        if "thread_ts" not in checkpoint:
            checkpoint["thread_ts"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        file_path = self._get_file_path(thread_id, checkpoint["thread_ts"])
        
        # Ensure 'values' is serializable (e.g., convert BaseMessage to dict)
        serializable_checkpoint = checkpoint.copy()
        if 'values' in serializable_checkpoint and 'messages' in serializable_checkpoint['values']:
            serializable_checkpoint['values']['messages'] = [
                msg.dict() if hasattr(msg, 'dict') else msg for msg in serializable_checkpoint['values']['messages']
            ]
        
        with open(file_path, "w") as f:
            json.dump(serializable_checkpoint, f, indent=2)
        # print(f"Checkpoint saved for {thread_id} at {checkpoint['thread_ts']} to {file_path}")
        
        # Update config with the new thread_ts if it wasn't already there or for confirmation
        config["configurable"]["thread_ts"] = checkpoint["thread_ts"]
        return config

    def list(self, config: RunnableConfig, filter: Optional[Mapping[str, Any]] = None) -> List[Checkpoint]:
        thread_id = config["configurable"]["thread_id"]
        # print(f"FileCheckpointSaver.list called for thread_id={thread_id}, filter={filter}")
        checkpoints = []
        for filename in os.listdir(self.checkpoint_dir):
            if filename.startswith(f"{thread_id}_") and filename.endswith(".json"):
                file_path = os.path.join(self.checkpoint_dir, filename)
                try:
                    with open(file_path, "r") as f:
                        cp_data = json.load(f)
                        # Re-hydrate messages if they were stored as dicts
                        if 'values' in cp_data and 'messages' in cp_data['values']:
                            new_messages = []
                            for msg_data in cp_data['values']['messages']:
                                if isinstance(msg_data, dict):
                                    if msg_data.get('type') == 'human':
                                        new_messages.append(HumanMessage(**msg_data))
                                    elif msg_data.get('type') == 'ai':
                                        new_messages.append(AIMessage(**msg_data))
                                    else: # Fallback for other message types or if 'type' is missing
                                        new_messages.append(msg_data)
                                else:
                                    new_messages.append(msg_data)
                            cp_data['values']['messages'] = new_messages
                        checkpoints.append(cp_data)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON from {file_path}")
                    continue
        
        # Apply filter if provided (basic implementation, can be extended)
        if filter:
            filtered_checkpoints = []
            for cp in checkpoints:
                match = True
                for key, value in filter.items():
                    if key == "thread_id": continue # Already filtered by filename
                    if key == "thread_ts" and cp.get("thread_ts") != value:
                        match = False
                        break
                    # Add more filter conditions as needed
                if match:
                    filtered_checkpoints.append(cp)
            return filtered_checkpoints
        
        # Sort by thread_ts to ensure latest is easily identifiable
        return sorted(checkpoints, key=lambda cp: cp["thread_ts"])

    def delete(self, config: RunnableConfig) -> None:
        thread_id = config["configurable"]["thread_id"]
        thread_ts = config["configurable"].get("thread_ts")

        if thread_ts:
            # Delete a specific checkpoint
            file_path = self._get_file_path(thread_id, thread_ts)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted specific checkpoint: {file_path}")
            else:
                print(f"Checkpoint not found for deletion: {file_path}")
        else:
            # Delete all checkpoints for a given thread_id
            for filename in os.listdir(self.checkpoint_dir):
                if filename.startswith(f"{thread_id}_") and filename.endswith(".json"):
                    file_path = os.path.join(self.checkpoint_dir, filename)
                    os.remove(file_path)
            print(f"Deleted all checkpoints for thread_id: {thread_id}")

# Now, let's use our custom checkpointer with LangGraph
from langgraph.graph import StateGraph, START, END
import operator

# Assume AgentState and graph workflow are defined as before

# Build the graph (using the same structure as previous examples)
workflow_custom = StateGraph(AgentState)
workflow_custom.add_node("greeter", greet_customer)
workflow_custom.add_node("request_processor", process_request)
workflow_custom.add_node("order_finalizer", finalize_order)

workflow_custom.add_edge(START, "greeter")
workflow_custom.add_edge("greeter", "request_processor")
workflow_custom.add_conditional_edges(
    "request_processor",
    lambda state: "order_finalizer" if state.get("item_requested") else END,
    {
        "order_finalizer": "order_finalizer",
        END: END
    }
)
workflow_custom.add_edge("order_finalizer", END)

app_custom = workflow_custom.compile()

# Initialize our custom checkpointer
custom_memory = FileCheckpointSaver()

thread_id_custom = "user_custom_demo"
config_custom = {"configurable": {"thread_id": thread_id_custom}}

# Clean up previous custom checkpoints if they exist
if os.path.exists(CHECKPOINT_DIR):
    for f in os.listdir(CHECKPOINT_DIR):
        if f.startswith(f"{thread_id_custom}_"):
            os.remove(os.path.join(CHECKPOINT_DIR, f))

print("\n--- Using Custom FileCheckpointSaver ---")

# Step 1
inputs_c1_1 = {"messages": [HumanMessage(content="Hello, my name is Frank")]}
app_custom.invoke(inputs_c1_1, config=config_custom, checkpoint=custom_memory)
print(f"State after name (from custom): {app_custom.get_state(config_custom, checkpoint=custom_memory).values.get('user_name')}")

# Step 2
inputs_c1_2 = {"messages": [HumanMessage(content="I want a latte")]}
app_custom.invoke(inputs_c1_2, config=config_custom, checkpoint=custom_memory)
print(f"State after item (from custom): {app_custom.get_state(config_custom, checkpoint=custom_memory).values.get('item_requested')}")

# Step 3
inputs_c1_3 = {"messages": [HumanMessage(content="Yes, please")]}
output_c1_3 = app_custom.invoke(inputs_c1_3, config=config_custom, checkpoint=custom_memory)
print(f"AI: {output_c1_3['messages'][-1].content}")
print(f"State after finalization (from custom): {app_custom.get_state(config_custom, checkpoint=custom_memory).values.get('order_id')}")

# List all checkpoints for verification
print("\n--- Listing checkpoints from custom saver ---")
all_custom_cps = custom_memory.list(config_custom)
for cp in all_custom_cps:
    print(f"  TS: {cp['thread_ts']}, User: {cp['values'].get('user_name')}, Item: {cp['values'].get('item_requested')}, Order: {cp['values'].get('order_id')}")

# Delete all checkpoints for this thread
print(f"\n--- Deleting all checkpoints for {thread_id_custom} ---")
custom_memory.delete(config_custom)
print(f"Remaining checkpoints for {thread_id_custom}: {custom_memory.list(config_custom)}")

# Clean up the directory
if os.path.exists(CHECKPOINT_DIR):
    os.rmdir(CHECKPOINT_DIR)
    print(f"\nCleaned up directory: {CHECKPOINT_DIR}")
```
This custom `FileCheckpointSaver` fully implements the `BaseCheckpointSaver` interface. It stores each checkpoint as a JSON file, named with the `thread_id` and `thread_ts`. This demonstrates how you can extend `langgraph conversation memory checkpointer` functionality to suit your specific storage requirements. You'll see JSON files appearing and disappearing in the `custom_checkpoints` directory as the script runs.

### Checkpoint Cleanup

As your LangGraph applications run and conversations accumulate, your `langgraph conversation memory checkpointer` will save many checkpoints. Over time, this can consume significant storage space, especially with `SQLSaver` or a custom persistent checkpointer. It's also important for data privacy to manage old or irrelevant conversation data.

"Checkpoint cleanup" refers to the process of removing old or unnecessary checkpoints. This is an essential maintenance task for any long-running application. You don't want your database or file system to be overloaded with outdated conversation states.

LangGraph's `BaseCheckpointSaver` interface includes a `delete` method for this very purpose. You can use it to remove specific checkpoints or all checkpoints associated with a particular `thread_id`. Implementing a cleanup strategy is crucial for efficient and compliant `langgraph conversation memory checkpointer` management.

#### Strategies for Cleanup

-   **Delete oldest:** Keep only the `N` most recent checkpoints for each thread.
-   **Delete after X days:** Automatically remove checkpoints older than a certain age.
-   **Delete on user request:** Allow users to clear their conversation history.
-   **Delete specific branches:** If you're using branching conversations, you might want to delete a specific "what if" branch.

Let's look at an example using `SQLSaver` to delete checkpoints.

```python
import os
import sqlite3
from langgraph.checkpoint import SQLSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator
import time

# Assume AgentState and graph workflow are defined as before

# Define the path for our SQLite database
DB_FILE_CLEANUP = "langgraph_cleanup_checkpoints.sqlite"
if os.path.exists(DB_FILE_CLEANUP):
    os.remove(DB_FILE_CLEANUP) 

memory_sql_cleanup = SQLSaver.from_conn_string(f"sqlite:///{DB_FILE_CLEANUP}")

# Rebuild the app if necessary (same as previous sections)
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_name: str
    item_requested: str
    order_id: str

def greet_customer(state: AgentState):
    messages = state['messages']
    if not messages:
        return {"messages": [AIMessage(content="Hello! How can I help you today?")]}
    return {} 

def process_request(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None
    
    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content.lower()
        if "coffee" in user_input or "tea" in user_input:
            item = "coffee" if "coffee" in user_input else "tea"
            return {"messages": [AIMessage(content=f"Sure, I can help you with {item}. Any specific type?")], "item_requested": item}
        elif "my name is" in user_input and not state.get("user_name"):
            name_start_index = user_input.find("my name is") + len("my name is")
            name = user_input[name_start_index:].strip().split(' ')[0]
            if name:
                return {"messages": [AIMessage(content=f"Got it, your name is {name}. How can I help you?")] , "user_name": name}
        elif state.get("user_name"):
            return {"messages": [AIMessage(content=f"Okay, {state['user_name']}, what else can I do for you?")]}
        else:
            return {"messages": [AIMessage(content="I'm not sure what you mean. Can you ask me for something?")]}
    return {}

def finalize_order(state: AgentState):
    item = state.get("item_requested")
    name = state.get("user_name", "customer")
    if item:
        order_id = "ORD" + str(hash(item + name))[:5]
        return {"messages": [AIMessage(content=f"Alright, {name}! Your {item} order is placed. Your order ID is {order_id}.")],
                "order_id": order_id}
    return {"messages": [AIMessage(content="I need to know what you want to order first.")]}

# Build the graph
workflow_cleanup = StateGraph(AgentState)
workflow_cleanup.add_node("greeter", greet_customer)
workflow_cleanup.add_node("request_processor", process_request)
workflow_cleanup.add_node("order_finalizer", finalize_order)

workflow_cleanup.add_edge(START, "greeter")
workflow_cleanup.add_edge("greeter", "request_processor")
workflow_cleanup.add_conditional_edges(
    "request_processor",
    lambda state: "order_finalizer" if state.get("item_requested") else END,
    {
        "order_finalizer": "order_finalizer",
        END: END
    }
)
workflow_cleanup.add_edge("order_finalizer", END)

app_cleanup = workflow_cleanup.compile()

thread_id_cleanup = "user_cleanup_demo"
config_cleanup = {"configurable": {"thread_id": thread_id_cleanup}}

print("--- Creating multiple checkpoints for cleanup demo ---")
app_cleanup.invoke({"messages": [HumanMessage(content="Hello")]}, config=config_cleanup, checkpoint=memory_sql_cleanup)
time.sleep(0.1)
app_cleanup.invoke({"messages": [HumanMessage(content="My name is Grace")]}, config=config_cleanup, checkpoint=memory_sql_cleanup)
time.sleep(0.1)
app_cleanup.invoke({"messages": [HumanMessage(content="I'd like a pastry")]}, config=config_cleanup, checkpoint=memory_sql_cleanup) # This might not finalize based on current graph
time.sleep(0.1)
app_cleanup.invoke({"messages": [HumanMessage(content="A croissant, please")]}, config=config_cleanup, checkpoint=memory_sql_cleanup)

print("\n--- Listing checkpoints before cleanup ---")
all_cps_before = memory_sql_cleanup.list(config_cleanup)
print(f"Total checkpoints for '{thread_id_cleanup}': {len(all_cps_before)}")
for cp in all_cps_before:
    print(f"  TS: {cp['thread_ts']}, User: {cp['values'].get('user_name')}, Item: {cp['values'].get('item_requested')}")

# Get an old thread_ts to delete specifically
if len(all_cps_before) > 1:
    oldest_ts_to_delete = all_cps_before[0]['thread_ts']
    print(f"\n--- Deleting specific oldest checkpoint: {oldest_ts_to_delete} ---")
    memory_sql_cleanup.delete({"configurable": {"thread_id": thread_id_cleanup, "thread_ts": oldest_ts_to_delete}})

    print("\n--- Listing checkpoints after specific deletion ---")
    all_cps_after_specific = memory_sql_cleanup.list(config_cleanup)
    print(f"Total checkpoints for '{thread_id_cleanup}': {len(all_cps_after_specific)}")
    for cp in all_cps_after_specific:
        print(f"  TS: {cp['thread_ts']}, User: {cp['values'].get('user_name')}, Item: {cp['values'].get('item_requested')}")

print(f"\n--- Deleting ALL checkpoints for '{thread_id_cleanup}' ---")
memory_sql_cleanup.delete(config_cleanup) # No thread_ts means delete all for thread_id

print("\n--- Listing checkpoints after ALL deletion ---")
all_cps_after_all = memory_sql_cleanup.list(config_cleanup)
print(f"Total checkpoints for '{thread_id_cleanup}': {len(all_cps_after_all)}")

# Clean up the database file
if os.path.exists(DB_FILE_CLEANUP):
    os.remove(DB_FILE_CLEANUP)
    print(f"\nCleaned up {DB_FILE_CLEANUP}")
```
This example shows how to list checkpoints, then delete a specific old checkpoint using its `thread_ts`, and finally delete all checkpoints for a given `thread_id`. Proper `langgraph conversation memory checkpointer` cleanup is vital for maintaining the health and efficiency of your AI system.

### Error Recovery with Checkpoints

One of the most valuable benefits of using a `langgraph conversation memory checkpointer` is its role in error recovery. Imagine your complex AI application is running, processing a user's request that involves multiple steps, and suddenly something goes wrong. Maybe an external API call fails, or your code encounters an unexpected error. Without checkpoints, the entire conversation progress could be lost.

With checkpoints, you have built-in "save points." If an error occurs, you don't have to start the whole interaction from the beginning. You can simply reload the last known good checkpoint and restart the process from that stable state. This prevents data loss and significantly improves the robustness of your AI applications.

It's like having an "undo" button for your entire application flow. This capability is crucial for providing a seamless user experience, even when unforeseen issues arise. It's a fundamental aspect of building resilient `langgraph conversation memory checkpointer` systems.

Consider a scenario where your agent needs to gather several pieces of information from a user before fulfilling a request. If the user provides half the information, and then a backend service goes down, you don't want the user to have to re-enter everything when the service is back up. The `langgraph conversation memory checkpointer` ensures that data is preserved.

Let's simulate an error and then recover from it.

```python
import os
import sqlite3
from langgraph.checkpoint import SQLSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import operator
import time

# Assume AgentState and graph workflow are defined as before

# Define the path for our SQLite database
DB_FILE_ERROR = "langgraph_error_checkpoints.sqlite"
if os.path.exists(DB_FILE_ERROR):
    os.remove(DB_FILE_ERROR) 

memory_sql_error = SQLSaver.from_conn_string(f"sqlite:///{DB_FILE_ERROR}")

# Rebuild the app if necessary
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_name: str
    item_requested: str
    order_id: str
    error_occurred: bool # New field for error simulation

def greet_customer_error(state: AgentState):
    messages = state['messages']
    if not messages:
        return {"messages": [AIMessage(content="Hello! How can I help you today?")]}
    return {} 

def process_request_error(state: AgentState):
    messages = state['messages']
    last_message = messages[-1] if messages else None
    
    if last_message and isinstance(last_message, HumanMessage):
        user_input = last_message.content.lower()
        if "coffee" in user_input or "tea" in user_input:
            item = "coffee" if "coffee" in user_input else "tea"
            return {"messages": [AIMessage(content=f"Sure, I can help you with {item}. Any specific type?")], "item_requested": item}
        elif "my name is" in user_input and not state.get("user_name"):
            name_start_index = user_input.find("my name is") + len("my name is")
            name = user_input[name_start_index:].strip().split(' ')[0]
            if name:
                return {"messages": [AIMessage(content=f"Got it, your name is {name}. How can I help you?")] , "user_name": name}
        elif state.get("user_name"):
            return {"messages": [AIMessage(content=f"Okay, {state['user_name']}, what else can I do for you?")]}
        else:
            return {"messages": [AIMessage(content="I'm not sure what you mean. Can you ask me for something?")]}
    return {}

def risky_step(state: AgentState):
    print("\n--- Running risky_step ---")
    if state.get("error_occurred"):
        raise ValueError("Simulated critical error!")
    
    messages = state['messages']
    if not state.get("order_id"):
        return {"messages": [AIMessage(content=f"Just confirming, you wanted {state.get('item_requested')}?")]}
    return {"messages": messages}

def finalize_order_error(state: AgentState):
    item = state.get("item_requested")
    name = state.get("user_name", "customer")
    if item:
        order_id = "ORD" + str(hash(item + name))[:5]
        return {"messages": [AIMessage(content=f"Alright, {name}! Your {item} order is placed. Your order ID is {order_id}.")],
                "order_id": order_id}
    return {"messages": [AIMessage(content="I need to know what you want to order first.")]}

# Build the graph
workflow_error = StateGraph(AgentState)
workflow_error.add_node("greeter", greet_customer_error)
workflow_error.add_node("request_processor", process_request_error)
workflow_error.add_node("risky_operation", risky_step)
workflow_error.add_node("order_finalizer", finalize_order_error)


workflow_error.add_edge(START, "greeter")
workflow_error.add_edge("greeter", "request_processor")
workflow_error.add_edge("request_processor", "risky_operation")
workflow_error.add_conditional_edges(
    "risky_operation",
    lambda state: "order_finalizer" if state.get("item_requested") else END,
    {
        "order_finalizer": "order_finalizer",
        END: END
    }
)
workflow_error.add_edge("order_finalizer", END)

app_error = workflow_error.compile()

thread_id_error = "user_error_recovery_demo"
config_error = {"configurable": {"thread_id": thread_id_error}}

print("--- Step 1: User provides name and requests item ---")
app_error.invoke({"messages": [HumanMessage(content="Hello, my name is Hannah. I want a pizza.")], "error_occurred": False}, 
                 config=config_error, 
                 checkpoint=memory_sql_error)

current_state_after_request = app_error.get_state(config_error, checkpoint=memory_sql_error).values
print(f"State after request: Name='{current_state_after_request.get('user_name')}', Item='{current_state_after_request.get('item_requested')}'")

print("\n--- Step 2: Simulating an error in the risky step ---")
try:
    # We set error_occurred to True to simulate a failure in the risky_step
    app_error.invoke({"messages": [HumanMessage(content="Proceed with pizza order.")], "error_occurred": True}, 
                     config=config_error, 
                     checkpoint=memory_sql_error)
except ValueError as e:
    print(f"Caught expected error: {e}")
    # The error means the 'risky_step' failed and did not complete.
    # The checkpoint *before* this risky step should still be valid.

print("\n--- Attempting recovery: Restarting from previous valid state ---")
# To recover, we don't pass the "error_occurred: True" flag anymore.
# The `thread_id` will automatically load the LATEST VALID checkpoint,
# which is the one *before* the risky_step attempt.
# We then provide a new input to proceed.
recovered_state = app_error.get_state(config_error, checkpoint=memory_sql_error).values
print(f"Recovered state before proceeding: Name='{recovered_state.get('user_name')}', Item='{recovered_state.get('item_requested')}'")

print("\n--- Retrying the operation after recovery ---")
output_recovered = app_error.invoke({"messages": [HumanMessage(content="Yes, please finalize the pizza order.")], "error_occurred": False}, 
                                  config=config_error, 
                                  checkpoint=memory_sql_error)
print(f"AI: {output_recovered['messages'][-1].content}")
print(f"Final state after recovery: Order ID='{output_recovered.get('order_id')}'")


# Clean up the database file
if os.path.exists(DB_FILE_ERROR):
    os.remove(DB_FILE_ERROR)
    print(f"\nCleaned up {DB_FILE_ERROR}")
```
In this example, the `risky_step` simulates a failure. When we `invoke` the graph again, the `langgraph conversation memory checkpointer` automatically loads the state *before* the failure occurred. This means "Hannah" and "pizza" were remembered, and the process could continue without starting over. This powerful feature makes your LangGraph agents much more resilient.

### Best Practices for Using Checkpointers

Using `langgraph conversation memory checkpointer` effectively can greatly improve your AI applications. Here are some best practices to keep in mind:

#### When to Use `MemorySaver` vs. `SQLSaver`

-   **`MemorySaver`**: Use this for quick experiments, local development, or temporary conversations that don't need to last beyond the current session. It's fast and simple, but not persistent.
-   **`SQLSaver`**: This is your go-to for production applications or any scenario requiring persistent memory. It ensures conversations are remembered even if your application restarts. For larger deployments, consider using a dedicated SQL database like PostgreSQL instead of SQLite.

#### Considerations for Custom Checkpointers

-   **Scalability**: If you're building a high-traffic application, choose a storage solution that can handle many reads and writes (e.g., a NoSQL database or cloud storage).
-   **Security**: Ensure your custom checkpointer encrypts sensitive conversation data, especially if it's storing personal information. Access control to the storage should also be carefully managed.
-   **Reliability**: Your custom checkpointer should be robust against failures. Implement error handling and consider redundancy if your storage system allows it.

#### Naming Conventions for `thread_id`

-   Choose `thread_id` values that are unique and meaningful. Using user IDs, session IDs, or a combination can be good.
-   Avoid using easily guessable or sequential IDs if they could expose user data. Use UUIDs (Universally Unique Identifiers) for maximum uniqueness and security.

#### Regularly Review and Clean Up Checkpoints

-   Implement a strategy for regularly deleting old or irrelevant checkpoints. This prevents your storage from growing indefinitely and helps with data privacy regulations.
-   Consider what "old" means for your application. Is it checkpoints older than 30 days? Or perhaps only keep the last 5 checkpoints per user?

#### Testing Your Checkpointer Implementation

-   Thoroughly test your `langgraph conversation memory checkpointer` with various scenarios:
    -   Saving and loading.
    -   Loading non-existent `thread_id`s.
    -   Loading specific `thread_ts` values.
    -   Concurrent access (if your storage supports it).
    -   Error handling during save/load operations.

By following these best practices, you can ensure your `langgraph conversation memory checkpointer` solution is robust, efficient, and secure.

### Advanced Topics and Further Exploration

You've now learned a lot about how to implement conversation memory using `langgraph conversation memory checkpointer`. But the world of LangGraph and state management is vast and full of exciting possibilities. Here are some areas you might want to explore next:

-   **Combining Checkpointers with State Management**: While checkpointers handle persistence, understanding how your graph's `State` is defined and updated is equally important. Dive deeper into [LangGraph State Management](internal-link-to-state-management.md) to master how information flows and transforms within your agent.
-   **Integrating with Logging and Monitoring**: For production applications, knowing what's happening inside your agent is critical. Learn how to combine checkpointer events with logging frameworks and monitoring tools to observe conversation flow and identify issues. This can provide valuable insights into user interactions.
-   **Securing Your Checkpoint Data**: If your conversations contain sensitive user data, encryption and access control are paramount. Explore advanced security measures for your chosen storage backend and how to protect the integrity and privacy of your `langgraph conversation memory checkpointer` data. Our [Securing Your AI Applications](internal-link-to-ai-security.md) blog post might offer more guidance.
-   **Customizing Checkpoint Serialisation**: For complex state objects that aren't easily JSON serializable, you might need to customize how your checkpoint data is converted to and from storage format. This could involve custom encoders/decoders for your chosen checkpointer.
-   **Asynchronous Checkpoint Operations**: For highly concurrent applications, consider implementing asynchronous `get`, `put`, `list`, and `delete` methods in your custom checkpointer. This allows non-blocking I/O operations, improving application responsiveness.

These advanced topics will help you build even more sophisticated and production-ready `langgraph conversation memory checkpointer` applications. The foundational knowledge you've gained today is the perfect stepping stone.

### Conclusion

You've embarked on a detailed journey to understand and implement conversation memory in LangGraph using the powerful `langgraph conversation memory checkpointer`. From the basic concepts of memory and state to the intricacies of built-in and custom checkpointers, you now have a solid foundation. You've seen how to save and load conversation states, manage checkpoint versions, handle cleanup, and even recover from errors.

This ability to remember past interactions is not just a nice-to-have; it's a game-changer for building intelligent, user-friendly, and robust AI applications. Your agents can now maintain context, personalize experiences, and provide seamless dialogues, even across sessions.

The examples provided should give you a clear starting point for integrating checkpointers into your own LangGraph projects. Experiment with the different types, try building your own custom solution, and always think about how memory can enhance your agent's capabilities. Happy building, and may your conversations be ever-persistent!