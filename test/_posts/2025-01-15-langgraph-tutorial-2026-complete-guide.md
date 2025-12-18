---
layout: single
title: "LangGraph Tutorial 2025: Complete Beginner's Guide to Building AI Agents"
date: 2025-01-15
categories:
  - LangGraph
  - AI-Agents
  - Tutorial
tags:
  - langgraph
  - langchain
  - ai-agents
  - python
  - tutorial-2025
excerpt: "Learn LangGraph from scratch in 2025. Build your first AI agent with step-by-step instructions, working code examples, and best practices for production deployment."
header:
  overlay_image: /assets/images/langgraph-tutorial-header.jpg
  overlay_filter: 0.5
  teaser: /assets/images/langgraph-tutorial-teaser.jpg
toc: true
toc_sticky: true
---

## What is LangGraph?

LangGraph is the newest framework from LangChain for building stateful, multi-actor applications with Large Language Models (LLMs). Released in late 2024, it's now the **recommended way** to build AI agents, replacing the older AgentExecutor.

### Why LangGraph Over Traditional LangChain?

- **Better Control**: Full control over agent flow and decision-making
- **State Management**: Built-in state persistence across steps
- **Debugging**: Easier to debug complex workflows
- **Production-Ready**: Designed for real-world applications

## What You'll Build

By the end of this tutorial, you'll create a functional AI agent that can:
- Answer questions using multiple tools
- Maintain conversation context
- Make decisions based on previous steps
- Handle errors gracefully

**Estimated time**: 30 minutes

## Prerequisites

Before starting, ensure you have:
```bash
Python 3.9+
pip or conda package manager
OpenAI API key (get one at platform.openai.com)
```

## Installation

Install the required packages:
```bash
pip install langgraph langchain-openai langchain-core
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Understanding LangGraph Core Concepts

### 1. StateGraph

The `StateGraph` is the foundation of LangGraph. It manages:
- **Nodes**: Functions that process data
- **Edges**: Connections between nodes
- **State**: Data passed between nodes

### 2. State Schema

Define what data flows through your graph:
```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
```

## Building Your First LangGraph Agent

### Step 1: Import Dependencies
```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
```

### Step 2: Define the State
```python
class AgentState(TypedDict):
    """State that gets passed between nodes."""
    messages: Annotated[list, add_messages]
```

### Step 3: Create the Agent Node
```python
# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

def agent_node(state: AgentState):
    """Process messages and generate response."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}
```

### Step 4: Build the Graph
```python
# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)

# Define edges
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Compile the graph
app = workflow.compile()
```

### Step 5: Run Your Agent
```python
# Create initial state
initial_state = {
    "messages": [HumanMessage(content="What is LangGraph?")]
}

# Execute the graph
result = app.invoke(initial_state)

# Print the response
print(result["messages"][-1].content)
```

**Output:**
```
LangGraph is a framework for building stateful, multi-actor applications 
with LLMs. It provides fine-grained control over agent workflows and state 
management, making it ideal for production applications.
```

## Adding Tools to Your Agent

Let's make your agent more powerful by adding tool-calling capabilities:
```python
from langchain_core.tools import tool

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    # Simplified for tutorial
    return f"Wikipedia results for: {query}"

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid expression"

# Bind tools to the LLM
tools = [search_wikipedia, calculate]
llm_with_tools = llm.bind_tools(tools)
```

### Updated Agent Node with Tools
```python
def agent_with_tools(state: AgentState):
    """Agent that can use tools."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_node(state: AgentState):
    """Execute tools based on agent's decision."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Execute tool calls
    tool_results = []
    for tool_call in last_message.tool_calls:
        tool = {t.name: t for t in tools}[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        tool_results.append(result)
    
    return {"messages": tool_results}
```

## Conditional Routing

Add logic to determine the next step:
```python
def should_continue(state: AgentState):
    """Determine if agent should continue or end."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If there are tool calls, continue to tool node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # Otherwise, end
    return END

# Updated workflow with conditional routing
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_with_tools)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile()
```

## Complete Working Example

Here's the full code for a functional LangGraph agent:
```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# Define tools
@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"The weather in {location} is sunny, 72°F"

# State definition
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize LLM with tools
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

# Define nodes
def agent_node(state: AgentState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def tool_node(state: AgentState):
    last_message = state["messages"][-1]
    results = []
    for tool_call in last_message.tool_calls:
        tool = {t.name: t for t in tools}[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        results.append(result)
    return {"messages": results}

# Routing logic
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# Compile
app = workflow.compile()

# Test it!
response = app.invoke({
    "messages": [HumanMessage(content="What's the weather in San Francisco?")]
})

print(response["messages"][-1].content)
```

## Common Patterns and Best Practices

### 1. Error Handling
```python
def safe_agent_node(state: AgentState):
    try:
        return agent_node(state)
    except Exception as e:
        return {"messages": [f"Error: {str(e)}"]}
```

### 2. Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_agent_node(state: AgentState):
    logger.info(f"Processing {len(state['messages'])} messages")
    result = agent_node(state)
    logger.info("Agent processing complete")
    return result
```

### 3. State Persistence
```python
from langgraph.checkpoint.memory import MemorySaver

# Add checkpointing
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

## Debugging Your LangGraph Agent

### Visualize the Graph
```python
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
```

### Step-by-Step Execution
```python
for step in app.stream(initial_state):
    print(f"Step: {step}")
```

## Next Steps

Congratulations! You've built your first LangGraph agent. Here's what to explore next:

1. **[LangGraph Memory Patterns](/langgraph-memory-patterns/)** - Add conversation history
2. **[Multi-Agent Systems with LangGraph](/multi-agent-langgraph/)** - Coordinate multiple agents
3. **[Deploy LangGraph to Production](/deploy-langgraph-production/)** - Take it live

## Resources

- 📚 [Official LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- 💻 [Complete Code on GitHub](https://github.com/langchain-tutorials/langgraph-examples)
- 🎥 [Video Tutorial](#)
- 💬 [Join Our Discord](#)

## Conclusion

LangGraph represents a significant evolution in building AI agents. Its stateful architecture and fine-grained control make it perfect for production applications.

**What will you build with LangGraph?** Share your projects in the comments below!

---

*Found this tutorial helpful? [Subscribe for weekly LangChain tutorials](#) and [star our GitHub repo](https://github.com/langchain-tutorials)!*

### Recommended Reading

- [LangChain vs LangGraph: Complete Comparison](/langchain-vs-langgraph/)
- [10 LangGraph Patterns Every Developer Should Know](/langgraph-patterns/)
- [LangGraph Performance Optimization Guide](/langgraph-optimization/)