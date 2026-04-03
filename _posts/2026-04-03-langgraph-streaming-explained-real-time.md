---
title: "LangGraph Streaming Explained: How to Stream Agent Outputs in Real Time"
description: "Unlock LangGraph streaming to deliver real-time agent outputs. Discover how to implement LangGraph streaming for responsive AI applications and enhance user ..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangGraph streaming]
featured: false
image: '/assets/images/langgraph-streaming-explained-real-time.webp'
---

## LangGraph Streaming Explained: How to Stream Agent Outputs in Real Time

Imagine you are asking a super smart friend a tough question. If your friend thinks for a long time and then gives you the whole answer all at once, you might get bored waiting. But what if your friend started telling you parts of the answer as they thought of them? That would be much better, right? You would get information in real time and feel like things are moving along.

This is exactly what **LangGraph streaming** does for your smart AI programs, often called "agents." Instead of waiting for an agent to finish its entire thought process, LangGraph lets you see its **agent output** as it happens. This makes your AI applications feel faster and more interactive, giving you a smooth experience. You can see the magic of **real-time AI** in action, making your interactions feel dynamic and engaging.

### Why Real-Time Matters for Your AI

In today's fast world, waiting is not fun. When you talk to an AI, you want answers now, not later. This need for immediate feedback is why **real-time AI** is so important. It changes how you experience AI, moving from static waiting to dynamic interaction.

Think about a chatbot that answers your questions. If it takes a long time to give you a full response, you might get impatient and close the chat. But if the chatbot starts typing words out one by one, you feel like it is actively thinking and responding to you. This instant feedback makes your experience much better and keeps you engaged.

Streaming makes your AI tools feel alive and helpful, just like talking to a real person. It is all about giving you immediate updates and making sure you are never left wondering what is happening. This is a big step forward in how we interact with intelligent systems.

### Understanding LangGraph Basics

Before we dive into streaming, let's quickly remember what LangGraph is all about. LangGraph is like a special blueprint for building complex AI programs, called agents. It helps you design how your agent will think and make decisions. You can learn more about the basics in our [Introduction to LangGraph](/blog/getting-started-with-langgraph).

LangGraph uses "nodes" and "edges" to map out an agent's steps. Nodes are like little mini-brains where the agent does a specific task, like asking a question or using a tool. Edges are the paths that connect these mini-brains, showing how the agent moves from one step to the next. This setup allows for very powerful and smart agents that can handle many different situations.

The agent has a "state" which is like its memory, holding all the information it needs as it moves through its steps. Each node can update this state, changing what the agent knows or needs to do next. This structured approach helps in building robust and reliable AI systems.

#### The Problem: Waiting for Answers

When you run a traditional LangGraph agent without streaming, it processes everything internally. It goes through all its nodes, makes all its decisions, and then, only at the very end, does it give you its final answer. This means you might be staring at a blank screen, waiting. You won't know if the agent is stuck, thinking hard, or almost done.

This "all or nothing" approach can be frustrating, especially for complex tasks. Imagine if a search engine made you wait until it had found *every single result* before showing you anything. You want to see results appear as they are found. Similarly, with an AI agent, you want to see its progress and partial thoughts, not just the finished product.

Waiting can lead to a poor user experience, making your AI application feel slow and unresponsive. It breaks the feeling of a natural conversation or interaction. This is where **LangGraph streaming** comes in to save the day.

#### The Solution: LangGraph Streaming

**LangGraph streaming** is the answer to the waiting game. It lets you get bits and pieces of your agent's work as soon as they are ready. Instead of one big answer at the end, you get a continuous flow of updates. This is like watching a live feed of your agent's brain in action.

With streaming, you can see what your agent is thinking, which tools it's using, and what kind of information it's gathering. You receive the **agent output** bit by bit, allowing you to react or display it immediately. This greatly improves how fast your application feels to the user.

This technique is super helpful for building interactive tools and chatbots. It makes your AI conversations feel natural and keeps you in the loop. LangGraph streaming transforms a potentially slow process into an engaging and dynamic experience for you.

### How LangGraph Streaming Works

At its heart, **LangGraph streaming** is about sending small pieces of information over time, rather than one large chunk. Think of it like a video stream where you get frames one by one, instead of downloading the whole movie first. This makes everything feel faster and more responsive for you.

When you ask your LangGraph agent to do something, it doesn't just work in secret. With streaming, it sends updates about its progress back to you as it finishes each small part. This could be a word it just thought of, a tool it decided to use, or even just a confirmation that it moved to the next step. It's a continuous conversation between your agent and your application.

This method keeps you informed and engaged, allowing you to build applications that feel very smart and instant. It is a powerful way to bring **real-time AI** experiences to life.

#### The Core Idea: Token Streaming

The main idea behind **LangGraph streaming** for text is called **token streaming**. What are tokens? Well, when an AI model creates text, it doesn't make whole words at once. It creates small pieces, like parts of words or single words, called "tokens." For example, the word "streaming" might be broken into "stream" and "ing" or just "streaming" as one token.

With **token streaming**, your LangGraph agent sends these tokens to you as soon as the AI model generates them. So, you see the response building up word by word, or even letter by letter, right before your eyes. This is very similar to how you see text appear when someone is typing in a messaging app. It gives you the immediate feedback you expect from modern applications.

This process is a core part of making your AI interactions feel natural and instant. It prevents long pauses and keeps you engaged with the agent's response as it unfolds.

#### Under the Hood: Server-Sent Events (SSE)

So, how does this streaming magic actually happen behind the scenes? Often, **LangGraph streaming** uses a web technology called **Server-Sent Events**, or **SSE**. Imagine a special doorbell that the server can ring anytime it has a new message for you. You don't have to keep pressing the doorbell to ask "Anything new?" The server just tells you.

**SSE** allows your server (where your LangGraph agent runs) to send a continuous flow of updates to your web browser or application. Your application opens a connection, and the server keeps sending data through that connection whenever something new happens with your agent. This is a very efficient way to send small, real-time updates without needing to constantly ask for new information. It is designed for one-way communication, perfect for streaming **agent output** to you.

This technology is a backbone for many **real-time AI** applications, making sure that your user interface stays updated instantly. It's a simple yet powerful way to deliver dynamic content.

#### Comparing with LangChain Streaming

You might have heard of **LangChain streaming** already, especially if you've worked with AI models before. LangChain is the larger framework that LangGraph is a part of. Both LangChain and LangGraph can do streaming, but they focus on slightly different things.

**LangChain streaming** typically lets you stream the raw output directly from a language model, like getting words back one by one. This is great for showing you the AI's generated text immediately. It's focused on the final text output from a single model call.

**LangGraph streaming**, on the other hand, gives you much more detailed control and insight into the entire agent's process. Because LangGraph manages a graph of nodes and tools, its streaming allows you to see not just the final text, but also *which node* is running, *which tool* is being called, and *what the intermediate thoughts* are. It's a stream of the *agent's entire workflow*, not just the final language model output. This deeper visibility makes **LangGraph streaming** incredibly powerful for complex, multi-step agents, giving you richer **agent output** information.

### Setting Up Your First Streaming Agent

Let's get practical and build a simple LangGraph agent that can stream its output to you. It's easier than you might think! You'll see how to take a basic agent and make it instantly more responsive. We'll walk through each step to make sure you understand everything.

This example will demonstrate the core concept of **LangGraph streaming**, showing you how to set up the graph and then use the special `stream()` method. You'll quickly see the difference between waiting for a full answer and getting **real-time AI** updates. Get ready to make your agents much more dynamic!

#### Step 1: Install LangGraph

First things first, you need to have LangGraph installed on your computer. If you haven't already, you can get it using a simple command. This command fetches all the necessary parts for LangGraph to work. You also want to install the OpenAI library if you plan to use OpenAI models for your agent.

Just open your terminal or command prompt and type these lines. This sets up your environment to start building cool streaming agents.

```bash
pip install langgraph langchain_openai
```

This ensures you have the core tools to create and run your agent. You're now ready to bring your AI agents to life with **LangGraph streaming**.

#### Step 2: Build a Simple Agent

Now, let's create a very simple agent. This agent will have just two steps: one to decide what to do, and another to perform an action. We'll use a `tool` to simulate some external work, and a `model` to decide what to say or do. This structure helps you understand the flow of **LangGraph streaming**.

Our agent will basically take a question, use a tool if needed, and then answer. This basic setup is perfect for showing how **agent output** can be streamed. We'll define a simple graph with a tool node and a final response node.

We'll use a very basic setup for demonstration purposes. In a real application, these steps could be much more complex. Remember, LangGraph allows for intricate decision-making and tool usage, and streaming works just as well with those advanced setups.

```python
from typing import TypedDict, Annotated, List, Union
import operator
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Make sure you have your OpenAI API key set as an environment variable
# import os
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Define a simple tool
@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculates the sum of two numbers."""
    return a + b

# Define the Agent State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    intermediate_steps: Annotated[List[AgentAction], operator.add]

# Define the agent's decision-making node
def run_agent(state: AgentState):
    """
    Decides whether to use a tool or respond directly.
    """
    model = ChatOpenAI(temperature=0, streaming=True) # Important: enable streaming on the model itself!
    tools = [calculate_sum]
    # Bind tools to the model
    model_with_tools = model.bind_tools(tools)

    # Convert messages to a format the model understands
    # LangChain agents typically expect a specific message format for tool use
    # For a simple example, we'll try to get it to use the tool if numbers are mentioned.
    # In a real agent, you'd use a more sophisticated prompt and agent executor.
    
    # For a direct example, let's just make it call the tool if the last message contains "sum"
    last_message = state["messages"][-1].content
    if "sum" in last_message.lower() and "calculate" in last_message.lower():
        # This is a very simplistic way to force a tool call for demonstration.
        # A real agent would use the LLM to decide.
        # Let's assume the user asks for "calculate sum of 5 and 3"
        import re
        numbers = re.findall(r'\d+', last_message)
        if len(numbers) == 2:
            a, b = int(numbers[0]), int(numbers[1])
            # This would normally be an AgentAction, but for this simple example,
            # we'll simulate the tool call directly to demonstrate streaming the tool's result.
            # In a full agent, the model_with_tools would output AgentAction directly.
            return {"intermediate_steps": [AgentAction(tool="calculate_sum", tool_input={"a": a, "b": b}, log=f"Calling calculate_sum with a={a}, b={b}")]}
    
    # If no tool is called (or decision to call tool is not made)
    response = model_with_tools.invoke(state["messages"])
    # This might be AgentFinish or AgentAction if the model decides to use a tool
    return {"messages": [response]}


# Define the tool execution node
def execute_tool(state: AgentState):
    """
    Executes a tool call.
    """
    last_action = state["intermediate_steps"][-1]
    tool_name = last_action.tool
    tool_input = last_action.tool_input
    
    # Assuming calculate_sum is the only tool for simplicity
    if tool_name == "calculate_sum":
        result = calculate_sum.invoke(tool_input)
        return {"messages": [("tool_output", str(result))]} # Return tool output as a message
    return {"messages": [("error", "Unknown tool")]}

# Define the entry point for decision making
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if isinstance(last_message, tuple) and last_message[0] == "tool_output":
        # If the last message was a tool output, we're done with the tool part
        return "end" # Go to end or a final response step
    if isinstance(last_message, BaseMessage) and isinstance(last_message.content, str):
        # If the last message is a string, it means the model might have responded directly
        # or is waiting for tool output
        if "final_answer" in last_message.content.lower():
            return "end"
        if last_message.tool_calls:
            return "call_tool" # Model wants to call a tool
    return "continue_thinking" # Model wants to continue thinking or respond

# Build the LangGraph graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", run_agent)
workflow.add_node("tool", execute_tool)

# Set the entry point
workflow.set_entry_point("agent")

# Define edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue_thinking": "agent", # Loop back to agent if more thinking is needed (e.g. tool result processing)
        "call_tool": "tool",
        "end": END
    }
)
workflow.add_edge("tool", "agent") # After tool execution, go back to agent to process tool output or respond

# Compile the graph
app = workflow.compile()
```

This code sets up a basic agent. It has a `calculate_sum` tool, an `AgentState` to manage messages, and two core nodes: `run_agent` for decision-making and `execute_tool` for running the tool. The `should_continue` function decides the next step based on the agent's current state. Crucially, we ensured the `ChatOpenAI` model itself has `streaming=True`. This is key for **token streaming** from the LLM within the agent.

#### Step 3: Make it Stream!

Now for the exciting part: making this agent stream its **agent output**. Instead of using `invoke()`, which waits for everything, we use the `stream()` method. This method returns a special kind of object that you can loop through, getting updates as they happen. Each update will tell you what the agent is doing at that exact moment.

You will see different types of events as you iterate through the stream. These events can tell you when a node starts, when a tool is called, or when the final answer is being generated. This detailed visibility is what makes **LangGraph streaming** so powerful and gives you true **real-time AI** insights.

```python
# Now, let's stream the output!
print("--- Streaming Agent Output ---")
for s in app.stream({"messages": [("user", "What is the sum of 10 and 15?")]}):
    print(s)
    print("---")

print("\n--- Streaming Agent Output for direct response ---")
for s in app.stream({"messages": [("user", "Tell me a joke.")]}):
    print(s)
    print("---")
```

When you run this code, you'll immediately notice the difference. Instead of one big output, you'll see multiple smaller outputs appearing over time. Each one represents a step or a partial thought from your agent. This is the essence of **LangGraph streaming** in action, providing instant feedback and dynamic interaction. You are no longer waiting; you are observing the AI's thought process in **real time**.

### Diving Deeper into Streaming Outputs

When you use `app.stream()`, you're not just getting a final answer. You're getting a rich flow of information about what your agent is doing at every moment. This detailed feedback is a major advantage of **LangGraph streaming**. It lets you understand your agent's internal workings in a way that traditional, non-streaming methods cannot.

Each piece of information you receive from the stream is called an "event." These events tell you specific things, like which node just ran, what its output was, or if a tool was used. This deep insight helps you build more transparent and debuggable AI applications. You can even use these different event types to show different things to your user, enhancing the **real-time AI** experience significantly.

#### What You Get Back

When you iterate through the `stream()` method, you get a dictionary for each event. This dictionary contains information about the current state of the agent or the specific output from a node. It typically includes keys like `__end__`, `__start__`, or the name of the node that just finished its work.

For example, you might see an event like `{"agent": {"messages": [...]}}`, indicating that the "agent" node has produced some messages. Or you might see `{"__end__": {"messages": [...]}}` when the graph completes. Understanding these event structures is key to processing the streamed **agent output** effectively. This detailed information allows you to create dynamic user interfaces that respond instantly to your agent's actions.

The structure of these events gives you fine-grained control over how you present the agent's progress. You can show loading indicators, display intermediate thoughts, or even animate the UI as your agent processes information.

#### Streaming Different Parts of the Agent

One of the coolest things about **LangGraph streaming** is that you can get updates from almost every part of your agent's journey. It's not just about the final answer; it's about seeing all the steps in between. This means you can track the agent's thought process very closely. This flexibility allows you to customize the **real-time AI** experience for your users.

You can choose to stream just the final text, or you can get detailed events about every single node that runs. This level of granularity makes **LangGraph streaming** incredibly powerful for debugging, monitoring, and building rich user interfaces. You'll never be in the dark about what your agent is doing.

This deep insight helps you understand and explain how your agent arrived at its conclusions. It truly unlocks the potential of transparent and interactive AI systems.

##### Streaming Node Outputs

When a node in your LangGraph workflow finishes its task, **LangGraph streaming** can send you an event with that node's output. This means you get to see the results of each individual step as soon as they are computed. For example, if you have a node that summarizes a document, you will get the summary as soon as that node is done, without waiting for the entire agent to finish its whole process. This is incredibly useful for providing progressive updates to the user.

You'll see events like `{"my_summary_node": {"output": "..."}}` appear in your stream. This provides you with direct access to the intermediate thoughts and data. It helps you track the agent's progress and see exactly what information it's working with at each stage.

This detailed **agent output** allows you to build very responsive interfaces. You can show users the steps being taken, building trust and transparency in your AI application.

##### Streaming Tool Calls

Imagine your agent decides it needs to use a tool, like our `calculate_sum` example. With **LangGraph streaming**, you'll get an event telling you exactly when the agent decides to use that tool. Then, once the tool runs and returns a result, you'll get another event with the tool's output. This is a powerful feature for understanding your agent's actions.

You might see an event like `{"tool_node": {"tool_calls": [{"name": "calculate_sum", "args": {"a": 10, "b": 15}}]}}` when the tool is about to be called. Then, later, an event might contain `{"tool_node": {"output": "25"}}` once the tool has completed. This real-time feedback on tool usage is fantastic for debugging and for showing users that your agent is actively performing actions.

This level of detail in the **agent output** is crucial for complex agents that interact with external systems. It allows you to visualize the agent's active engagement with its environment, making the **real-time AI** experience much richer.

##### Streaming Final Agent Response

Of course, the most common thing you want to stream is the agent's final answer. **LangGraph streaming** makes sure you get the complete text response as it's being generated, word by word, or token by token. This is where **token streaming** really shines. You see the answer build up on your screen, just like a person is typing. This is what makes chatbots feel so responsive.

The events for the final response will usually be part of the `messages` key in an event from the final node or the `__end__` event. You can extract the new tokens from these messages and append them to your display. This continuous flow of text creates a highly engaging and dynamic user experience, preventing any perceived lag.

This is the most visible benefit of **LangGraph streaming** for end-users, transforming a static wait into an interactive unveiling of the **agent output**. It's the core of what makes **real-time AI** feel truly instantaneous.

#### Code Example: Advanced Streaming with Event Types

Let's expand our previous example to show how you can specifically look for and handle different types of events in the stream. This allows you to build a more detailed and informative user interface. We'll track node starts, node ends, and the final response.

By filtering and processing these events, you can create a much richer **real-time AI** experience. You can display messages like "Agent is thinking...", "Using calculator...", and then stream the final text as it arrives. This kind of detailed feedback keeps the user informed and engaged throughout the process.

```python
from typing import TypedDict, Annotated, List, Union
import operator
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.base import BaseCheckpointSaver

# Define a simple tool
@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculates the sum of two numbers."""
    print(f"DEBUG: Calling calculate_sum with a={a}, b={b}") # Debug print
    return a + b

# Define the Agent State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    intermediate_steps: Annotated[List[AgentAction], operator.add]
    
# Define the agent's decision-making node
def run_agent_node(state: AgentState):
    """
    Decides whether to use a tool or respond directly.
    """
    print("DEBUG: Entering run_agent_node") # Debug print
    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
    tools = [calculate_sum]
    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(state["messages"])
    print(f"DEBUG: LLM responded: {response}") # Debug print

    if isinstance(response, AIMessage) and response.tool_calls:
        # If the LLM decided to call a tool, return the tool calls
        return {"intermediate_steps": [AgentAction(
            tool=tc.name, 
            tool_input=tc.args, 
            log=f"Calling tool: {tc.name} with args: {tc.args}"
        ) for tc in response.tool_calls]}
    else:
        # Otherwise, the LLM is responding directly
        return {"messages": [response]}

# Define the tool execution node
def execute_tool_node(state: AgentState):
    """
    Executes a tool call.
    """
    print("DEBUG: Entering execute_tool_node") # Debug print
    last_action = state["intermediate_steps"][-1]
    tool_name = last_action.tool
    tool_input = last_action.tool_input
    
    # In a real app, you'd have a mapping of tool names to actual functions
    if tool_name == "calculate_sum":
        result = calculate_sum.invoke(tool_input)
        print(f"DEBUG: Tool '{tool_name}' result: {result}") # Debug print
        # Return the tool output as a ToolMessage
        return {"messages": [ToolMessage(content=str(result), tool_call_id=last_action.tool_call_id if hasattr(last_action, 'tool_call_id') else "default_id")]}
    
    print(f"DEBUG: Unknown tool: {tool_name}") # Debug print
    return {"messages": [ToolMessage(content=f"Error: Unknown tool {tool_name}", tool_call_id="error_id")]}

# Define the entry point for decision making
def should_continue(state: AgentState):
    print("DEBUG: Entering should_continue") # Debug print
    last_message = state["messages"][-1]
    if isinstance(last_message, ToolMessage):
        # If the last message was a tool output, go back to the agent to process it
        return "continue_agent"
    elif isinstance(last_message, AIMessage) and not last_message.tool_calls:
        # If the agent responded directly and didn't call a tool, we are done
        return "end"
    elif isinstance(last_message, AIMessage) and last_message.tool_calls:
        # If the agent wants to call a tool, go to the tool execution node
        return "call_tool"
    print("DEBUG: should_continue - default to continue_agent") # Debug print
    return "continue_agent" # Fallback, should ideally not be reached if logic is complete

# Build the LangGraph graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", run_agent_node)
workflow.add_node("tool", execute_tool_node)

# Set the entry point
workflow.set_entry_point("agent")

# Define edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue_agent": "agent", # Loop back to agent to process tool result or continue thinking
        "call_tool": "tool",      # Agent wants to call a tool
        "end": END                # Agent has a final response
    }
)
workflow.add_edge("tool", "agent") # After tool execution, go back to agent to process tool output

# Compile the graph
app = workflow.compile()


print("--- Advanced Streaming Example ---")

user_input = "What is 123 plus 456? Give me the exact sum."

# Event types: "start", "end", "stream_start", "stream_end", "node", "action", "tool_end"
# By default, app.stream() yields events for each node's output.
# You can also use `events=True` to get more granular event types if available (LangChain >= 0.1.0)

print(f"\nQuery: {user_input}")
full_response = ""
for chunk in app.stream({"messages": [HumanMessage(content=user_input)]}, stream_mode="values"):
    if "agent" in chunk:
        # This chunk contains output from the 'agent' node, which means it's an LLM response or tool call decision
        if isinstance(chunk["agent"], dict) and "messages" in chunk["agent"]:
            for msg in chunk["agent"]["messages"]:
                if isinstance(msg, AIMessage):
                    # This is where the actual LLM tokens might stream out
                    if msg.content:
                        # Print incrementally for token streaming
                        print(f"Agent is responding: {msg.content}", end="", flush=True)
                        full_response += msg.content
                    if msg.tool_calls:
                        print(f"\nAgent decided to call a tool: {msg.tool_calls[0].name} with args {msg.tool_calls[0].args}")
        elif isinstance(chunk["agent"], dict) and "intermediate_steps" in chunk["agent"]:
            # This is where an AgentAction from the agent node would appear if it decided to use a tool
            for action in chunk["agent"]["intermediate_steps"]:
                print(f"\nAgent decided to perform action: {action.tool} with input {action.tool_input}")
    elif "tool" in chunk:
        # This chunk contains output from the 'tool' node, which means it's the result of a tool execution
        if isinstance(chunk["tool"], dict) and "messages" in chunk["tool"]:
            for msg in chunk["tool"]["messages"]:
                if isinstance(msg, ToolMessage):
                    print(f"\nTool '{msg.name if msg.name else 'unknown_tool'}' finished with result: {msg.content}")
    elif "__end__" in chunk:
        print("\n--- Agent finished ---")
        if isinstance(chunk["__end__"], dict) and "messages" in chunk["__end__"]:
            for msg in chunk["__end__"]["messages"]:
                if isinstance(msg, AIMessage):
                    print(f"Final AI Message: {msg.content}")
                    full_response = msg.content # Update with final complete message if it exists
                elif isinstance(msg, HumanMessage):
                    pass # Ignore user messages at the end for final response summary
                elif isinstance(msg, ToolMessage):
                    pass # Ignore tool messages at the end for final response summary
    else:
        # For other internal events or states, you might log them
        # print(f"Other chunk type: {chunk}")
        pass # We're only interested in specific node outputs for now

print(f"\n\nOverall full response collected: {full_response}")

print("\n--- Another example: Simple question without tool ---")
user_input_2 = "Hello, how are you today?"
full_response_2 = ""
for chunk in app.stream({"messages": [HumanMessage(content=user_input_2)]}, stream_mode="values"):
    if "agent" in chunk and isinstance(chunk["agent"], dict) and "messages" in chunk["agent"]:
        for msg in chunk["agent"]["messages"]:
            if isinstance(msg, AIMessage):
                if msg.content:
                    print(f"Agent: {msg.content}", end="", flush=True)
                    full_response_2 += msg.content
    elif "__end__" in chunk:
        print("\n--- Agent finished ---")
        if isinstance(chunk["__end__"], dict) and "messages" in chunk["__end__"]:
            for msg in chunk["__end__"]["messages"]:
                if isinstance(msg, AIMessage):
                    print(f"Final AI Message: {msg.content}")
                    full_response_2 = msg.content
    else:
        pass

print(f"\n\nOverall full response collected: {full_response_2}")
```

In this example, we iterate through the `app.stream()` output and check for different keys in each `chunk`. We print messages for when the agent is "thinking," when it "decides to call a tool," when the "tool finished," and the "final AI message." This gives you a clear picture of the agent's internal process and its **real-time AI** actions. The `stream_mode="values"` is crucial here to get the node outputs directly.

### Practical Use Cases for LangGraph Streaming

**LangGraph streaming** isn't just a cool technical trick; it's a powerful feature that transforms how you build and interact with AI applications. By making your agents communicate in **real time**, you open up many possibilities for better user experiences and more efficient systems. It allows you to create applications that feel genuinely responsive and intelligent.

Let's explore some common and impactful ways you can use **LangGraph streaming** in your projects. You'll see how streaming can improve different types of AI systems, from simple chatbots to complex decision-making assistants. These examples highlight the versatility of streaming **agent output**.

#### Chatbots and Conversational AI

This is perhaps the most obvious and impactful use case for **LangGraph streaming**. When you interact with a chatbot, you expect it to be responsive, much like talking to a human. Waiting for a chatbot to generate its full response before showing anything can feel slow and unnatural.

With **LangGraph streaming**, your chatbot can start displaying its answer word by word as soon as the AI model generates the first **token**. This creates a fluid, dynamic conversation where you see the reply building in **real time**. It makes the chatbot feel faster, more intelligent, and much more engaging, keeping you active in the conversation.

This improves the user experience significantly, making your AI assistants feel less like a computer and more like a helpful conversational partner. You get immediate feedback, which is key for maintaining engagement in any dialogue.

#### Interactive Tools and Assistants

Beyond chatbots, many AI applications serve as interactive tools or assistants that help you complete tasks. Imagine an AI assistant that helps you write code, plan a trip, or analyze data. In these scenarios, providing immediate feedback on its progress is incredibly valuable.

**LangGraph streaming** allows these interactive tools to show you what they are doing step-by-step. If your assistant needs to search a database, call an API, or perform a complex calculation, you can stream the updates. You can see messages like "Searching flight prices...", "Analyzing data...", or "Generating code snippet..." as the agent works. This transparency builds trust and keeps you informed throughout the process.

This **real-time AI** feedback not only enhances the user experience but also makes the tools more intuitive and easier to use. You always know the status of your request, making the application feel more reliable.

#### Complex Workflows

Some AI agents are designed to handle very complex tasks that involve many steps, decisions, and external tool calls. For these complex workflows, it can be hard to know if the agent is progressing correctly or if it's stuck. **LangGraph streaming** provides a solution to this challenge.

By streaming the **agent output** at each node, you can monitor the agent's progress in **real time**. You can see which path it takes through the graph, what intermediate results it generates, and when it makes critical decisions. This is invaluable for debugging complex agents and understanding their behavior.

For users, this means they can follow along with the agent's sophisticated process, gaining insights into how it arrives at its final conclusion. It turns a black-box operation into a transparent and observable workflow, leveraging the power of **real-time AI** for complex problem-solving. You can even visualize the graph's execution live.

#### Code Example: Building a Streaming UI (Conceptual/Pseudo-code)

While building a full web UI is beyond a simple code snippet here, let's think about how a front-end (like a web page) would use the streamed output from a LangGraph agent. This is where **SSE** (Server-Sent Events) often comes into play. Your web page would open a connection to your server, and the server would send the **LangGraph streaming** events as **SSE** messages.

Here's how you might conceptualize the front-end logic:

```javascript
// --- Conceptual Front-end JavaScript Code ---

const outputDiv = document.getElementById('agent-output');
const statusDiv = document.getElementById('agent-status');
let currentAgentResponse = '';

function setupStreamingAgent(query) {
    statusDiv.textContent = 'Agent thinking...';
    outputDiv.textContent = ''; // Clear previous output
    currentAgentResponse = '';

    // In a real app, this would be a POST request to your backend endpoint
    // that uses app.stream() and sends events via SSE.
    const eventSource = new EventSource(`/api/stream_agent?query=${encodeURIComponent(query)}`);

    eventSource.onmessage = function(event) {
        const chunk = JSON.parse(event.data);

        // Process different types of events from LangGraph streaming
        if (chunk && chunk.type === "node_output" && chunk.node_name === "agent") {
            // This is likely LLM output or a decision from the agent node
            if (chunk.content && chunk.content.messages) {
                // Look for AIMessage content for token streaming
                chunk.content.messages.forEach(msg => {
                    if (msg.type === "ai" && msg.content) {
                        currentAgentResponse += msg.content;
                        outputDiv.textContent = currentAgentResponse; // Update displayed text
                        outputDiv.scrollTop = outputDiv.scrollHeight; // Scroll to bottom
                    }
                });
            } else if (chunk.tool_calls) {
                statusDiv.textContent = `Agent decided to use tool: ${chunk.tool_calls[0].name}`;
            }
        } else if (chunk && chunk.type === "node_output" && chunk.node_name === "tool") {
            // This is the output from a tool
            if (chunk.content && chunk.content.messages) {
                chunk.content.messages.forEach(msg => {
                    if (msg.type === "tool") {
                        statusDiv.textContent = `Tool '${msg.name || 'unknown'}' finished with result: ${msg.content}`;
                        outputDiv.innerHTML += `<br><i>(Tool Result: ${msg.content})</i><br>`; // Display tool result
                        outputDiv.scrollTop = outputDiv.scrollHeight;
                    }
                });
            }
        } else if (chunk && chunk.type === "end") {
            statusDiv.textContent = 'Agent finished!';
            eventSource.close(); // Close the connection
            // Display final messages if needed (could be included in node_output too)
        } else {
            // Optional: log other event types for debugging
            // console.log("Other event:", chunk);
        }
    };

    eventSource.onerror = function(err) {
        console.error("EventSource failed:", err);
        statusDiv.textContent = 'Error during streaming.';
        eventSource.close();
    };
}

// Example usage:
// setupStreamingAgent("What is the sum of 10 and 15? Tell me the final answer.");
```

This conceptual example shows how the front-end would listen for events. It updates the `outputDiv` with the streaming text from the agent and updates the `statusDiv` based on agent actions like tool calls or completion. This pattern allows for rich, **real-time AI** interfaces that keep users engaged and informed. The underlying **SSE** connection ensures a continuous flow of **agent output**.

### Tips and Tricks for Efficient Streaming

While **LangGraph streaming** is powerful, getting the most out of it involves a few best practices. You want to ensure your streaming experience is not just functional but also fast and reliable for your users. These tips will help you optimize your agent for **real-time AI** delivery.

Thinking about how your agent processes information and how that information is sent back to you can significantly improve performance. It’s about more than just turning on a switch; it's about designing for a smooth, continuous flow of **agent output**.

#### Handle Errors Gracefully

Things can go wrong in any complex system, and AI agents are no exception. An external API might fail, a tool might return an error, or the language model might produce unexpected output. When these errors happen during streaming, you don't want your entire application to crash or freeze. It's crucial to handle these issues gracefully.

Your streaming loop should include `try-except` blocks to catch potential errors from the agent or the underlying systems. If an error occurs, you should send an error message to the client through the stream, rather than just breaking the connection. This allows your UI to display a helpful error message to the user, like "Something went wrong, please try again." This ensures a robust **real-time AI** experience, even when facing unexpected issues.

Providing clear error feedback maintains a professional user experience. You can also log these errors for later debugging, helping you improve your agent over time.

#### Batching vs. Pure Streaming

Sometimes, a hybrid approach might be more efficient than pure **token streaming** for certain parts of your agent. "Batching" means waiting for a slightly larger chunk of information before sending it, instead of sending every single token or event immediately. For instance, if your agent needs to perform a very quick, non-text-generating step (like a simple lookup), it might be faster to complete that step entirely and then send its result as one event, rather than trying to stream micro-updates during that brief process.

Pure **LangGraph streaming** is ideal for long-running text generation from LLMs. However, for quick intermediate steps or tool calls that are very fast, sending an "event_started" and "event_finished" might be sufficient, rather than attempting to break down every millisecond of that process. Decide what level of granularity makes sense for each part of your agent to optimize both responsiveness and efficiency.

The goal is to balance the feeling of **real-time AI** with the overhead of sending too many tiny messages. Find the sweet spot for your specific application.

#### Optimizing Agent Performance

The speed of your **LangGraph streaming** is directly tied to the speed of your underlying agent. If your agent takes a long time to think or to use its tools, then even with streaming, the overall process will still be slow. **Token streaming** helps reduce perceived latency, but it doesn't magically make a slow agent fast.

Focus on optimizing the individual nodes in your graph. Can you make your tool calls faster? Are your prompts efficient? Is your language model choice appropriate for the task (e.g., a smaller, faster model for simple tasks)? Reducing the latency of each step in your agent directly translates to a faster and more fluid **real-time AI** stream. You can find more tips on making your agents faster in our blog post on [Optimizing Your LangGraph Agents](/blog/optimizing-langgraph-agents).

Efficient agents lead to efficient **LangGraph streaming**, providing the best possible user experience. Every improvement in processing time will be immediately noticeable to your users.

### Common Questions About LangGraph Streaming

You might have a few questions popping up in your mind about **LangGraph streaming**. It's a powerful concept, and it's natural to wonder about its limits and practical implications. Let's address some of the most common questions to help you better understand and utilize this feature for **real-time AI**.

Understanding these points will help you confidently build streaming applications. We'll cover speed, tool interactions, and control over what gets streamed.

#### Is it always faster?

**LangGraph streaming** *feels* faster to the user because they see immediate progress, but it doesn't necessarily make the *total time* for the agent to complete its task shorter. In fact, sending many small updates can sometimes add a tiny bit of overhead compared to sending one large message at the very end. The main benefit is perceived speed and improved user experience.

Imagine downloading a large file. If you see a progress bar move quickly, it *feels* faster than waiting for 100% completion all at once, even if the actual download time is the same. Similarly, **token streaming** provides that crucial progress feedback. So, while the overall execution time might be similar, the user's experience of **real-time AI** is significantly enhanced. It's about responsiveness, not raw computation speed.

The perceived speed is what truly matters for user satisfaction in many interactive applications.

#### What if my agent uses external tools?

Yes, **LangGraph streaming** works wonderfully even when your agent uses external tools. When your agent decides to call a tool, you'll receive an event indicating that the tool is being invoked. Then, while the tool is running, there might be a pause in the stream until the tool returns its result. Once the tool finishes, you'll get another event containing the tool's output.

After the tool's output is received by the agent, the agent will process it, and then the text generation (if any) will resume streaming. This allows you to show users a clear sequence: "Agent thinking...", "Calling Calculator...", "Calculator returned X", "Agent processing result...", "Agent responding: Y". This transparency in **agent output** is key for interactive, tool-using **real-time AI**.

You can show dynamic loading states or messages during tool execution to keep the user informed. This makes the entire interaction very transparent and engaging for you.

#### Can I stream parts of the output?

Absolutely! This is one of the strengths of **LangGraph streaming**. You have fine-grained control over what you stream. You can choose to only stream the final text output, similar to basic **LangChain streaming**. Or, you can choose to stream more detailed events, like when each node starts and finishes, what the intermediate **agent output** is, or when specific tools are called.

The `app.stream()` method provides different `stream_mode` options and allows you to inspect each chunk, giving you flexibility. You can filter these events on your server-side before sending them to the client, or process them on the client-side to display only the most relevant information. This level of control allows you to customize the **real-time AI** experience precisely for your application's needs, making it very versatile.

This granular control means you can tailor the streaming experience to be as simple or as detailed as you require.

### Conclusion

You've learned that **LangGraph streaming** is a game-changer for building responsive and interactive AI applications. By allowing you to see your agent's **agent output** in **real time**, it transforms slow waiting into dynamic engagement. This isn't just a technical detail; it fundamentally changes how users experience your AI.

We explored how **token streaming** delivers text word-by-word, how **SSE** powers this continuous flow, and how LangGraph provides deeper insights compared to simpler **LangChain streaming**. You've seen practical examples of setting up and processing streamed outputs, covering everything from simple responses to complex tool interactions. The ability to observe your agent's thought process step-by-step is incredibly powerful for both users and developers.

Now, you have the knowledge to build your own **real-time AI** applications that truly come alive. Go ahead and experiment with **LangGraph streaming** to make your agents faster, more transparent, and incredibly engaging. The future of interactive AI is here, and you are ready to build it!