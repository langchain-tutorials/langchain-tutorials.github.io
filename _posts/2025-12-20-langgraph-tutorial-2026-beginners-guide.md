---
title: "LangGraph Tutorial 2026: Complete Beginner's Guide to Building AI Agents"
description: "Dive into AI agent creation with our ultimate langgraph tutorial 2026, designed for beginners to easily build powerful, intelligent applications from scratch."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [langgraph tutorial 2026]
featured: false
image: '/images/langgraph-tutorial-2026-beginners-guide.webp'
---

## Welcome to LangGraph Tutorial 2026: Building Smart AI Agents!

Have you ever wanted to make an AI that can think, make choices, and even use tools? It sounds like science fiction, but with LangGraph, it's totally possible! This `langgraph tutorial 2026` will show you how to build amazing AI agents from scratch. We'll start with the very basics, so don't worry if you're new to this.

LangGraph is a super cool tool that helps you connect different parts of an AI model. Think of it like building with LEGOs, where each LEGO piece is a step your AI can take. You can make your AI decide what to do next based on what's happening.

This guide is your complete beginner's journey to `creating first LangGraph agent`. By the end, you'll have a good grasp of how to build AI agents that are much smarter than simple chatbots. Get ready to dive into the exciting world of AI development!

### Getting Started: Installation and Setup

Before we build anything, we need to get our workspace ready. This part of our `langgraph tutorial 2026` covers the `installation and setup` steps. It's like gathering your tools before starting a big project.

First, you'll need Python installed on your computer. Python is a popular programming language that LangGraph uses. If you don't have it, you can download it from the official Python website.

You'll also need a way to manage your Python projects, like a virtual environment. This helps keep your project's dependencies separate from other projects. Open your terminal or command prompt and type these commands.

```bash
# Create a new folder for your project
mkdir langgraph_agent_project
cd langgraph_agent_project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

Now that your virtual environment is active, it's time to install LangGraph. We'll also install a few other libraries that are commonly used with it. These include `langchain-openai` for connecting to AI models and `jupyter` if you want to run code in a notebook.

```bash
pip install -U langgraph langchain-openai "jupyter>=1.0.0"
```

You might also want to install `tavily-python` for search capabilities if you plan to give your agent internet access. We'll cover `adding tools to agents` later in this `langgraph tutorial 2026`. For now, just focus on the core installations.

Once these commands finish, you're all set up! You have the necessary software to begin your journey with LangGraph. Let's move on to understanding how LangGraph agents remember things.

### The Foundation: Defining State Schema

Every smart agent needs a memory to know what's going on. In LangGraph, this memory is called "state." The state holds all the important information as your agent works through a task. This section of our `langgraph tutorial 2026` focuses on `defining state schema`.

Think of state like a checklist or a notebook your agent carries. It writes down important notes as it goes. For example, it might note the user's question, previous answers, or results from a tool.

To make sure our agent's memory is organized, we define a "state schema." This schema is like a blueprint for what information our agent's memory can hold. We use a Python library called Pydantic to help us define this structure. Pydantic makes sure the data is always in the right format.

Let's look at a simple example of a state. Imagine an agent that answers questions. Its state might need to remember the `question` asked and the `answer` it found. We can define this using Python classes.

```python
from typing import TypedDict, List, Annotated
from langgraph.graph.message import AnyMessage, add_message

class AgentState(TypedDict):
    """
    Represents the state of our agent.

    Attributes:
        messages: A list of messages making up the conversation.
        user_query: The initial query from the user.
        tool_output: Any output from tools used by the agent.
    """
    messages: Annotated[List[AnyMessage], add_message]
    user_query: str
    tool_output: str
```

In this `AgentState`, `messages` will keep track of the conversation flow. `user_query` stores the initial question you ask the agent. `tool_output` will hold results from any tools our agent uses. The `Annotated` part with `add_message` is a special LangGraph way to easily add new messages to the list.

You can make your state as simple or as complex as you need. For a more advanced agent, you might add fields like `research_results`, `summary`, or `feedback`. The key is to think about all the pieces of information your agent needs to do its job.

The `defining state schema` step is crucial because it decides what your agent can remember and act upon. Without a well-defined state, your agent would be forgetful and confused. Take your time to design a state that fits your agent's purpose.

### Your First LangGraph Agent: The Building Blocks

Now we're ready for the exciting part: `creating first LangGraph agent`! This is where we put together the pieces to make our agent actually do something. LangGraph uses a concept called a `StateGraph` to build agents.

Imagine a `StateGraph` as a flowchart or a map. It shows all the possible steps (called "nodes") your agent can take. It also shows how your agent moves from one step to another (called "edges"). We will learn `understanding StateGraph nodes and edges` in this section.

#### Nodes: The Action Steps

Nodes are like the individual actions or thoughts your agent has. Each node is a Python function that takes the current `state` as input. It then does something, like thinking of a response or using a tool, and returns updates to the `state`.

Let's create a very simple node that just greets the user. Remember, each node function receives the current `state` and should return an update to that state.

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# Make sure you have your OpenAI API key set up as an environment variable
# import os
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

# This is our language model (the brain of our agent)
llm = ChatOpenAI(model="gpt-4o")

def greet_node(state: AgentState) -> dict:
    """
    A simple node that generates a greeting based on the user's query.
    """
    print("---EXECUTING GREET NODE---")
    user_input = state["user_query"]
    greeting_message = f"Hello! You asked: '{user_input}'. Let me think about that."
    return {"messages": [AIMessage(content=greeting_message)]}
```

This `greet_node` takes the `user_query` from the state. It then creates a greeting message and adds it to the `messages` list in the state. Each node needs to be added to our `StateGraph`.

#### Edges: Connecting the Dots

Edges are the arrows that connect your nodes in the flowchart. They tell your agent which step to take next. LangGraph offers different types of edges:

*   **Direct Edges:** Go from one node directly to another.
*   **Conditional Edges:** Decide which node to go to next based on some logic (e.g., if a certain condition in the state is true).

We also need to tell LangGraph where to start and where to finish. These are called the "entry point" and "finish point."

Let's build our `StateGraph` using our `AgentState` and `greet_node`.

```python
from langgraph.graph import StateGraph, START, END

# Define the graph
workflow = StateGraph(AgentState)

# Add the greet node to our workflow
workflow.add_node("greet_user", greet_node)

# Set the entry point (where the graph starts)
workflow.set_entry_point("greet_user")

# Set the finish point (where the graph ends for now)
workflow.set_finish_point("greet_user")

# Compile the graph
app = workflow.compile()
```

In this setup, our agent will simply start at "greet_user" and immediately finish there. It's a very basic agent, but it's a start! You have just learned about `understanding StateGraph nodes and edges` in a simple context.

#### Running Your First Agent

To run this agent, we need to provide an initial state. Remember, the state is the agent's memory. We will pass a `user_query` to kick things off.

```python
initial_state = {"user_query": "What is the weather like today?", "messages": [], "tool_output": ""}

# Invoke the agent with the initial state
result = app.invoke(initial_state)

# Print the final state
print("\n---FINAL STATE---")
print(result)

# Access the messages from the final state
print("\n---AGENT MESSAGES---")
for message in result["messages"]:
    print(message.content)
```

You should see output similar to this:
```
---EXECUTING GREET NODE---

---FINAL STATE---
{'messages': [AIMessage(content="Hello! You asked: 'What is the weather like today?'. Let me think about that.")], 'user_query': 'What is the weather like today?', 'tool_output': ''}

---AGENT MESSAGES---
Hello! You asked: 'What is the weather like today?'. Let me think about that.
```

Congratulations! You've successfully built and run your `creating first LangGraph agent`. It's a small step, but a very important one in your `langgraph tutorial 2026` journey. Now you understand how nodes perform actions and how the graph manages the flow.

### Understanding StateGraph Nodes and Edges in Detail

Let's dig a bit deeper into `understanding StateGraph nodes and edges`. This is key to building complex and intelligent agents. As your agent grows, you'll use more nodes and smarter ways to connect them.

#### More on Nodes

Nodes are the workhorses of your LangGraph agent. Each node should ideally do one specific job. This makes your agent easier to understand and fix. You can have nodes that:
*   **Generate text:** Use an AI model to create responses or ideas.
*   **Call tools:** Interact with external services like web search or calculators.
*   **Process data:** Summarize information, extract keywords, or check conditions.
*   **Make decisions:** Evaluate the state and decide the next step.

Each node function receives the current `state` and must return a dictionary. This dictionary contains updates to the state. LangGraph then merges these updates with the existing state. For example, if your node returns `{"messages": [new_message]}`, that `new_message` will be added to the `messages` list in the global state.

```python
def research_node(state: AgentState) -> dict:
    """
    A placeholder node for performing research.
    """
    print("---EXECUTING RESEARCH NODE---")
    user_query = state["user_query"]
    # In a real agent, this would call a search tool
    research_result = f"Fake research result for '{user_query}': It's sunny with a high of 75°F."
    return {"tool_output": research_result, "messages": [AIMessage(content="I've performed some research.")]}

def respond_node(state: AgentState) -> dict:
    """
    A node that uses the AI model to generate a final response.
    """
    print("---EXECUTING RESPOND NODE---")
    current_messages = state["messages"]
    tool_output = state["tool_output"]
    # Combine previous messages and tool output for the AI model
    prompt = f"Based on the conversation and the following information: {tool_output}, please answer the user's query."
    full_prompt_messages = current_messages + [HumanMessage(content=prompt)]
    
    # Use the LLM to generate a response
    response = llm.invoke(full_prompt_messages)
    return {"messages": [AIMessage(content=response.content)]}
```

Here we added `research_node` and `respond_node`. The `research_node` simulates finding information. The `respond_node` takes all the info and crafts a final answer.

#### More on Edges: The Flow Control

Edges are what make your agent dynamic. They allow your agent to follow different paths based on conditions.

##### Direct Edges

You've already seen `add_edge`. It simply connects two nodes directly.
```python
workflow.add_edge("node_A", "node_B") # Always goes from A to B
```
This is useful for steps that always follow each other, like "research, then summarize."

##### Conditional Edges (`add_conditional_edges`)

This is where the magic happens for smart agents! `add_conditional_edges` lets your agent choose its next step. You define a special function called a "router." This router function looks at the current `state` and decides which node to go to next. It returns the name of the next node.

Let's make a router function for our agent. Our agent will decide if it needs to do research or if it can answer right away.

```python
def should_continue_research(state: AgentState) -> str:
    """
    Determines whether the agent needs to continue research or can respond.
    """
    print("---DETERMINING NEXT STEP---")
    user_query = state["user_query"]
    # Simple logic: If the query mentions "weather", maybe we need research.
    # Otherwise, we can try to respond directly.
    if "weather" in user_query.lower():
        print("---Decision: Needs Research---")
        return "research_needed"
    else:
        print("---Decision: Ready to Respond---")
        return "respond_directly"
```

This `should_continue_research` function is our decision-maker. It checks the `user_query`. If it sees "weather," it says "research_needed." Otherwise, it says "respond_directly."

Now, let's update our graph with these new nodes and the conditional edge.

```python
# ... (previous setup for workflow, greet_node, AgentState, llm) ...

workflow = StateGraph(AgentState)

# Add our new nodes
workflow.add_node("greet_user", greet_node)
workflow.add_node("do_research", research_node)
workflow.add_node("generate_response", respond_node)

# Set the entry point
workflow.set_entry_point("greet_user")

# After greeting, we need to decide what to do
# We use our conditional routing function here
workflow.add_conditional_edges(
    "greet_user", # From this node
    should_continue_research, # Use this function to decide
    {
        "research_needed": "do_research", # If 'research_needed', go to 'do_research'
        "respond_directly": "generate_response" # If 'respond_directly', go to 'generate_response'
    }
)

# After research, we always go to generate a response
workflow.add_edge("do_research", "generate_response")

# After generating a response, the graph finishes
workflow.set_finish_point("generate_response")

app = workflow.compile()
```

This updated graph is much smarter! It starts with a greeting. Then, based on your question, it either goes to research or directly to respond. Finally, it gives you an answer and finishes. This is a core part of `understanding StateGraph nodes and edges`.

Let's test this more advanced agent.

```python
# Test Case 1: Query needs research
print("\n---TEST CASE 1: Query needs research---")
initial_state_1 = {"user_query": "What is the weather like in New York today?", "messages": [], "tool_output": ""}
result_1 = app.invoke(initial_state_1)
print("\n---AGENT MESSAGES (Test 1)---")
for message in result_1["messages"]:
    print(message.content)

# Test Case 2: Query can be responded directly (based on our simple logic)
print("\n\n---TEST CASE 2: Query can be responded directly---")
initial_state_2 = {"user_query": "Tell me a fun fact about cats.", "messages": [], "tool_output": ""}
result_2 = app.invoke(initial_state_2)
print("\n---AGENT MESSAGES (Test 2)---")
for message in result_2["messages"]:
    print(message.content)
```

Expected output for Test 1:
```
---EXECUTING GREET NODE---
---DETERMINING NEXT STEP---
---Decision: Needs Research---
---EXECUTING RESEARCH NODE---
---EXECUTING RESPOND NODE---

---AGENT MESSAGES (Test 1)---
Hello! You asked: 'What is the weather like in New York today?'. Let me think about that.
I've performed some research.
Based on the conversation and the following information: Fake research result for 'What is the weather like in New York today?': It's sunny with a high of 75°F., please answer the user's query.  The weather in New York today is sunny with a high of 75°F.
```

Expected output for Test 2:
```
---EXECUTING GREET NODE---
---DETERMINING NEXT STEP---
---Decision: Ready to Respond---
---EXECUTING RESPOND NODE---

---AGENT MESSAGES (Test 2)---
Hello! You asked: 'Tell me a fun fact about cats.'. Let me think about that.
Based on the conversation and the following information: , please answer the user's query.  A fun fact about cats is that they can make over 100 different sounds, whereas dogs can only make about 10!
```
Notice how the `research_node` was skipped in the second test case. This shows the power of `conditional routing logic`. You're truly building a thinking agent in this `langgraph tutorial 2026`!

### Empowering Agents with Tools

A truly smart AI agent can do more than just talk; it can act! This means using tools, just like you might use a calculator or a web browser. In this part of our `langgraph tutorial 2026`, we'll focus on `adding tools to agents`.

#### What are Tools?

Tools are functions or external programs that your agent can call. They extend your agent's abilities beyond just generating text.
Common examples include:
*   **Web Search:** To find up-to-date information online.
*   **Calculator:** To perform math problems.
*   **Calendar:** To check or add events.
*   **Database Query:** To retrieve specific data.

LangChain provides a great way to define and use tools, and LangGraph integrates with them seamlessly. We'll use a simple web search tool powered by Tavily for our example.

First, you need to install the Tavily Python library and get an API key from their website. It's usually free for basic use. Remember to set your API key as an environment variable (`TAVILY_API_KEY`).

```bash
pip install tavily-python
```

Now, let's create a tool.

```python
from langchain_community.tools.tavily_research import TavilySearchResults
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage

# Initialize the Tavily search tool
tavily_tool = TavilySearchResults(max_results=3) # Get up to 3 search results

# You can also define custom tools
def get_current_time(location: str) -> str:
    """Gets the current time for a given location."""
    import datetime
    from pytz import timezone
    try:
        tz = timezone(location) # e.g., "America/New_York"
        now = datetime.datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except Exception:
        return "Could not find time for that location. Please specify a valid timezone, e.g., 'America/New_York'."

# LangChain makes it easy to convert regular functions into tools
from langchain_core.tools import tool

@tool
def simple_calculator(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        return str(eval(expression)) # Be careful with eval() in real apps!
    except Exception as e:
        return f"Error calculating: {e}"

# We'll use tavily_tool for our agent
```

#### Integrating Tools into a LangGraph Agent

To use a tool, our agent needs to:
1.  **Decide to use a tool:** This happens in a node.
2.  **Call the tool:** The node executes the tool.
3.  **Process the tool's output:** Another node (or the same one) takes the tool's results and updates the state.

We'll create a new `tool_node` that the AI model will use to decide if it needs a tool. If the AI decides to call a tool, it will send a special message.

Let's update our `AgentState` to keep track of tool calls and their outputs. The `tool_output` field is already there, which is great.

We need a node that can:
*   Receive messages from the user.
*   Use the LLM to decide if a tool is needed.
*   If a tool is needed, respond with a `ToolCall` message.
*   If not, respond directly.

This is a common pattern for `adding tools to agents`.

```python
from langgraph.prebuilt import ToolExecutor, ToolNode

# Tools the agent can use
tools = [tavily_tool, simple_calculator]
tool_executor = ToolExecutor(tools)

def call_model(state: AgentState) -> dict:
    """
    Invokes the LLM to decide what to do next: answer directly or use a tool.
    """
    print("---CALLING MODEL FOR ACTION---")
    current_messages = state["messages"]
    
    # We pass the tools to the LLM so it knows what it can use.
    # The 'tools' argument needs to be passed in a specific way for tool-calling models.
    response = llm.invoke(current_messages, tools=tools)
    
    # Check if the model decided to call a tool
    if response.tool_calls:
        print(f"---MODEL DECIDED TO CALL TOOL: {response.tool_calls}---")
    else:
        print("---MODEL DECIDED TO RESPOND DIRECTLY---")
    
    return {"messages": [response]} # Add the LLM's response (which might contain tool calls) to the state
```

Now, we need a special node to actually *execute* the tool. LangGraph provides `ToolNode` for this, making it very easy.

Our `ToolNode` will receive the tool call message from `call_model` and then run the tool. The output of the tool will be added back to the `messages` in the state as a `ToolMessage`.

Next, we need a router to decide if the AI called a tool or is ready to respond.

```python
def route_agent_action(state: AgentState) -> str:
    """
    Routes the agent based on whether the last message contains tool calls.
    """
    print("---ROUTING AGENT ACTION---")
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("---ROUTE TO TOOL EXECUTION---")
        return "call_tool"
    else:
        print("---ROUTE TO FINAL ANSWER---")
        return "end_conversation"
```

Let's rebuild our `StateGraph` with these tool-using capabilities.

```python
# ... (AgentState, llm setup) ...

# Define the graph
workflow = StateGraph(AgentState)

# Add the main agent node that decides to use tools or respond
workflow.add_node("agent", call_model)

# Add the ToolNode to execute tools
workflow.add_node("tool_node", ToolNode(tool_executor))

# Set the entry point
workflow.set_entry_point("agent")

# Add conditional routing after the agent node
workflow.add_conditional_edges(
    "agent",
    route_agent_action,
    {
        "call_tool": "tool_node",       # If tool call detected, go to tool_node
        "end_conversation": END         # If no tool call, agent is done, go to END
    }
)

# After the tool is executed, it goes back to the agent to process the tool's output
workflow.add_edge("tool_node", "agent")

app = workflow.compile()
```

Let's trace this flow:
1.  **START** -> `agent` node: The user's message comes in. The LLM decides if it needs a tool.
2.  `agent` node -> `route_agent_action`: This function checks the LLM's response.
3.  `route_agent_action` -> `tool_node` (if tool call): The tool is executed.
4.  `tool_node` -> `agent`: The tool's output is added to the state, and the LLM sees it. The LLM can now use this information to decide what to do next. It might call another tool or give a final answer.
5.  `route_agent_action` -> **END** (if no tool call): The LLM has a final answer, and the agent finishes.

This creates a powerful loop where the agent can repeatedly use tools until it's ready to provide a final answer. This is an advanced step in our `langgraph tutorial 2026` for `adding tools to agents`.

Let's test it!

```python
print("\n---TEST CASE 1: Agent using search tool---")
initial_state_tool_1 = {"messages": [HumanMessage(content="What is the current population of Japan?")], "user_query": "", "tool_output": ""}
result_tool_1 = app.invoke(initial_state_tool_1)
print("\n---AGENT MESSAGES (Tool Test 1)---")
for message in result_tool_1["messages"]:
    print(message.content)

print("\n---TEST CASE 2: Agent using calculator tool---")
initial_state_tool_2 = {"messages": [HumanMessage(content="What is 123 * 456?")], "user_query": "", "tool_output": ""}
result_tool_2 = app.invoke(initial_state_tool_2)
print("\n---AGENT MESSAGES (Tool Test 2)---")
for message in result_tool_2["messages"]:
    print(message.content)
```

You should see the agent deciding to call the `tavily_tool` for the population query and `simple_calculator` for the math query. It will then use the tool's output to give you an answer. The conversation might look like:
- Human asks a question.
- LLM responds with a ToolCall (e.g., `tool_code('tavily_search_results_json', {'query': 'current population of Japan'})`).
- ToolNode executes `tavily_search_results_json` and adds the result as a `ToolMessage`.
- LLM sees the `ToolMessage` and generates a final `AIMessage` answer.

This multi-turn thinking and action is what makes LangGraph so powerful for `building AI agents`.

### Smart Decisions: Conditional Routing Logic

We've touched on `conditional routing logic` already, but let's explore it more deeply. This is the brain of your agent, allowing it to make dynamic decisions about its workflow. Without it, your agent would follow a fixed path every time, which isn't very smart!

Conditional routing means that your agent doesn't just go from A to B. It can look at its `state` (its memory) and decide whether to go to B, C, or even back to A. This is crucial for creating agents that adapt to different situations and user inputs.

#### How it Works with `add_conditional_edges`

The core of conditional routing is the "router function" you provide to `add_conditional_edges`. This function:
1.  Takes the current `state` of the agent as its input.
2.  Performs some logic (e.g., checks keywords, reviews previous tool outputs, looks at message types).
3.  Returns a string, which is the name of the *next node* the agent should execute.

If the router function returns a node name that isn't defined in the `add_conditional_edges` map, LangGraph will raise an error. Always make sure your router covers all possible outcomes.

Let's imagine an agent that needs to answer questions, but also learn new facts.

##### State for Learning Agent

```python
class LearningAgentState(TypedDict):
    messages: Annotated[List[AnyMessage], add_message]
    facts_learned: List[str]
```
Here, `facts_learned` is a new list to store information.

##### Nodes for Learning Agent

```python
def check_for_learning_node(state: LearningAgentState) -> dict:
    """
    Checks if the user's message contains a new fact to learn.
    """
    print("---CHECKING FOR LEARNING OPPORTUNITY---")
    last_human_message = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_human_message = msg.content
            break
    
    if "learn about" in last_human_message.lower():
        fact_to_learn = last_human_message.split("learn about", 1)[1].strip()
        print(f"---Identified fact to learn: {fact_to_learn}---")
        return {"facts_learned": [f"Learned: {fact_to_learn}"]}
    else:
        print("---No new fact to learn---")
        return {} # No change to state, or an empty dict
```

```python
def generate_response_node(state: LearningAgentState) -> dict:
    """
    Generates a response using the LLM, potentially including learned facts.
    """
    print("---GENERATING RESPONSE---")
    current_messages = state["messages"]
    facts = state.get("facts_learned", [])
    
    context = ""
    if facts:
        context = f"Here are some facts I know: {'; '.join(facts)}. "
    
    # Get the last human message for a concise prompt
    last_human_message = ""
    for msg in reversed(current_messages):
        if isinstance(msg, HumanMessage):
            last_human_message = msg.content
            break

    prompt = f"{context}Based on the conversation, respond to: '{last_human_message}'."
    
    response = llm.invoke(current_messages + [HumanMessage(content=prompt)])
    return {"messages": [AIMessage(content=response.content)]}
```

##### Router for Learning Agent

```python
def route_learning_agent(state: LearningAgentState) -> str:
    """
    Routes based on whether a new fact was identified for learning.
    """
    print("---ROUTING LEARNING AGENT---")
    # Check if 'facts_learned' was updated in the previous step
    # This example assumes check_for_learning_node returns a new item in 'facts_learned' only if it learned something.
    # A more robust check might look for a specific flag or the nature of the last message.
    
    # Simpler check: If the last update to state added a new item to facts_learned list, route to "acknowledge_learning"
    # This requires a slightly different state update from check_for_learning_node or a more direct flag.
    # For this example, let's assume if 'learn about' was in the query, we go to learning path.
    last_human_message = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_human_message = msg.content
            break
            
    if "learn about" in last_human_message.lower():
        return "acknowledge_learning"
    else:
        return "respond_normally"
```

##### Building the Learning Graph

```python
learning_workflow = StateGraph(LearningAgentState)

learning_workflow.add_node("check_learning", check_for_learning_node)
learning_workflow.add_node("generate_response", generate_response_node)
# This node will acknowledge learning and then route to generate_response
def acknowledge_learning_node(state: LearningAgentState) -> dict:
    print("---ACKNOWLEDGING LEARNING---")
    last_learned_fact = state["facts_learned"][-1] if state["facts_learned"] else "something new"
    return {"messages": [AIMessage(content=f"Understood! I've noted down: {last_learned_fact}.")]}

learning_workflow.add_node("acknowledge_learning", acknowledge_learning_node)

learning_workflow.set_entry_point("check_learning")

learning_workflow.add_conditional_edges(
    "check_learning",
    route_learning_agent,
    {
        "acknowledge_learning": "acknowledge_learning",
        "respond_normally": "generate_response"
    }
)

learning_workflow.add_edge("acknowledge_learning", "generate_response") # After acknowledging, respond

learning_workflow.set_finish_point("generate_response")

learning_app = learning_workflow.compile()
```

This `learning_app` uses `conditional routing logic` to decide if it needs to process a new fact. If you ask it to "learn about cats," it will go through `check_learning`, then `acknowledge_learning`, and finally `generate_response`. If you just ask "Hello," it goes directly to `generate_response`.

```python
print("\n---TEST CASE: Learning Agent - Learn a fact---")
initial_learning_state_1 = {"messages": [HumanMessage(content="Hey agent, please learn about how photosynthesis works.")], "facts_learned": []}
result_learning_1 = learning_app.invoke(initial_learning_state_1)
print("\n---AGENT MESSAGES (Learning Test 1)---")
for message in result_learning_1["messages"]:
    print(message.content)
print(f"---Facts Learned: {result_learning_1['facts_learned']}---")

print("\n---TEST CASE: Learning Agent - Regular question---")
initial_learning_state_2 = {"messages": [HumanMessage(content="What's your favorite color?")], "facts_learned": result_learning_1["facts_learned"]} # Carry over learned facts
result_learning_2 = learning_app.invoke(initial_learning_state_2)
print("\n---AGENT MESSAGES (Learning Test 2)---")
for message in result_learning_2["messages"]:
    print(message.content)
print(f"---Facts Learned: {result_learning_2['facts_learned']}---")
```

The output will show the agent acknowledging the learning and then responding. In the second test, it will just respond normally, possibly referencing the learned fact if the LLM is smart enough to use the context. This example clearly shows how your agent's path changes based on the input, thanks to `conditional routing logic`. This is a powerful concept in this `langgraph tutorial 2026`.

### Complete Working Examples with Code

Let's bring everything together into a more complex, practical agent. This section of our `langgraph tutorial 2026` provides `complete working examples with code` for a "Research and Summarize Agent." This agent will be able to:
1.  Receive a query from the user.
2.  Decide if it needs to use a web search tool.
3.  Execute the web search.
4.  Summarize the findings.
5.  Deliver a concise answer.

This agent will use multiple nodes, conditional routing, and tools.

#### 1. Define Agent State

```python
from typing import TypedDict, List, Annotated
from langgraph.graph.message import AnyMessage, add_message
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_research import TavilySearchResults
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolExecutor, ToolNode

class ResearchAgentState(TypedDict):
    messages: Annotated[List[AnyMessage], add_message]
    user_query: str
    search_results: str # To store results from the search tool
    summary: str # To store the final summary
```

#### 2. Define Tools and LLM

```python
# Initialize the LLM (model)
llm = ChatOpenAI(model="gpt-4o", temperature=0) # temperature=0 makes it more factual

# Initialize the search tool
tavily_tool = TavilySearchResults(max_results=3)
tools = [tavily_tool]
tool_executor = ToolExecutor(tools)
```

#### 3. Define Nodes

##### Node 1: Initial Query and Tool Decision
This node will receive the user's query and decide if it needs to search.

```python
def agent_node(state: ResearchAgentState) -> dict:
    """
    This agent node uses the LLM to decide whether to call a tool or respond directly.
    """
    print("---AGENT NODE: DECIDING ACTION---")
    current_messages = state["messages"]
    
    # If it's the very first message, set the user_query
    if not state.get("user_query"):
        for msg in current_messages:
            if isinstance(msg, HumanMessage):
                state["user_query"] = msg.content
                break
    
    # Invoke LLM with tools
    response = llm.invoke(current_messages, tools=tools)
    
    if response.tool_calls:
        print(f"---AGENT DECIDED TO CALL TOOL: {response.tool_calls}---")
    else:
        print("---AGENT DECIDED TO RESPOND DIRECTLY (NO TOOL CALL)---")
        
    return {"messages": [response]}
```

##### Node 2: Tool Execution (Pre-built `ToolNode`)
This node will execute any tool calls made by the `agent_node`.

```python
# ToolNode is a pre-built node in LangGraph for executing tools
tool_execution_node = ToolNode(tool_executor)
```

##### Node 3: Summarize Results
This node will take the search results and summarize them using the LLM.

```python
def summarize_results_node(state: ResearchAgentState) -> dict:
    """
    This node summarizes the search results using the LLM.
    """
    print("---SUMMARIZE RESULTS NODE: SUMMARIZING---")
    current_messages = state["messages"]
    user_query = state["user_query"]

    # Find the tool message containing the search results
    search_output = ""
    for msg in reversed(current_messages):
        if isinstance(msg, ToolMessage):
            search_output = msg.content
            break
            
    if not search_output:
        print("---WARNING: No search output found for summarization.---")
        return {"summary": "No specific search results to summarize."}
    
    # Prompt the LLM to summarize the findings based on the original query
    summary_prompt = (
        f"Based on the following search results for the query '{user_query}', "
        f"please provide a concise summary:\n\n{search_output}"
    )
    
    summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
    print("---SUMMARY GENERATED---")
    return {"summary": summary_response.content, "messages": [AIMessage(content=summary_response.content)]}
```

##### Node 4: Final Response
This node will use the summary (or direct LLM response) to provide a final answer.

```python
def final_response_node(state: ResearchAgentState) -> dict:
    """
    This node generates the final answer to the user.
    """
    print("---FINAL RESPONSE NODE: GENERATING FINAL ANSWER---")
    final_summary = state.get("summary", "")
    user_query = state["user_query"]

    if final_summary:
        response_content = f"Based on my research for '{user_query}', here is the summary:\n{final_summary}"
    else:
        # If no summary, it means the agent likely responded directly without tools
        # We try to find the last AI message
        last_ai_message = ""
        for msg in reversed(state["messages"]):
            if isinstance(msg, AIMessage) and not msg.tool_calls:
                last_ai_message = msg.content
                break
        response_content = last_ai_message if last_ai_message else f"I'm sorry, I couldn't process your request for '{user_query}'."

    return {"messages": [AIMessage(content=response_content)]}
```

#### 4. Define Conditional Routing Logic

```python
def route_next_step(state: ResearchAgentState) -> str:
    """
    Routes the agent based on whether the last message from the LLM contains tool calls.
    """
    print("---ROUTING NEXT STEP---")
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        print("---ROUTE: TOOL CALL DETECTED, EXECUTE TOOL---")
        return "call_tool"
    
    # Check if a summary has just been generated
    if state.get("summary") and not state.get("final_response_sent"): # Add a flag to prevent re-summary
        print("---ROUTE: SUMMARY GENERATED, PROCEED TO FINAL RESPONSE---")
        return "generate_final_response"

    # If no tool calls and no summary needed, it means agent has a direct answer
    print("---ROUTE: DIRECT RESPONSE, END---")
    return "end_conversation"
```

#### 5. Build the Graph

```python
research_workflow = StateGraph(ResearchAgentState)

# Add nodes
research_workflow.add_node("agent", agent_node)
research_workflow.add_node("tool_executor", tool_execution_node)
research_workflow.add_node("summarize_results", summarize_results_node)
research_workflow.add_node("final_response", final_response_node)

# Set the entry point
research_workflow.set_entry_point("agent")

# Define edges
# From agent: Decide whether to call a tool or finish
research_workflow.add_conditional_edges(
    "agent",
    route_next_step,
    {
        "call_tool": "tool_executor",
        "end_conversation": "final_response" # If agent gives direct answer, go to final response
    }
)

# After tool execution, go back to the agent to process tool results
research_workflow.add_edge("tool_executor", "agent")

# After agent processes tool results, it might decide to summarize or give final answer
# This edge needs to correctly route after agent_node runs again with tool results.
# For simplicity, let's assume agent_node will eventually lead to summarizing or direct end
# A more robust solution might require a separate router after agent_node if it returns multiple paths.

# Let's adjust the routing a bit for clarity for this example.
# If `agent` determines it has a final answer (no tool_calls), it should go to `final_response`.
# If `agent` calls a tool, it goes to `tool_executor`, then back to `agent`.
# After `agent` has seen tool results, it needs to then decide if it summarizes or gives final response.

# Let's create a clearer flow for the research agent
# 1. Agent gets query, decides if search is needed.
# 2. If search is needed, call tool_executor.
# 3. After tool_executor, agent should summarize.
# 4. After summarization, agent gives final response.

# New flow:
# A -> decide (search/summarize/end)
# Search path: A -> tool -> summarize -> final_response -> END
# Direct answer path: A -> final_response -> END

def research_router(state: ResearchAgentState) -> str:
    """
    Routes the agent after a main 'think' node.
    """
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "call_tool"
    else:
        # If no tool calls, it means the agent has either an initial direct answer,
        # or has processed tool results and is ready to summarize/finish.
        # We need more logic here. Let's make the agent always summarize after a tool.
        # This state needs to track if a tool was *just* run.
        
        # Simple logic: if 'search_results' exist, means tool was run, go to summarize.
        # Otherwise, go to final response directly.
        if state.get("search_results"):
            return "summarize"
        else:
            return "direct_response"

research_workflow.add_conditional_edges(
    "agent",
    research_router,
    {
        "call_tool": "tool_executor",
        "summarize": "summarize_results",
        "direct_response": "final_response"
    }
)

research_workflow.add_edge("tool_executor", "summarize_results") # After tool, always summarize

research_workflow.add_edge("summarize_results", "final_response") # After summarizing, give final response

research_workflow.set_finish_point("final_response")

research_app = research_workflow.compile()
```

This updated graph logic provides a clearer path for `complete working examples with code`.

#### 6. Run the Agent

```python
print("\n---RUNNING RESEARCH AND SUMMARIZE AGENT---")
initial_research_state = {"messages": [HumanMessage(content="What is the capital of France and its current population?")], "user_query": "", "search_results": "", "summary": ""}
result_research = research_app.invoke(initial_research_state)

print("\n---FINAL RESEARCH AGENT MESSAGES---")
for message in result_research["messages"]:
    print(message.content)

print("\n---FINAL SUMMARY---")
print(result_research["summary"])


print("\n---RUNNING RESEARCH AND SUMMARIZE AGENT (Direct Answer)---")
initial_research_state_direct = {"messages": [HumanMessage(content="Hello, how are you?")], "user_query": "", "search_results": "", "summary": ""}
result_research_direct = research_app.invoke(initial_research_state_direct)

print("\n---FINAL RESEARCH AGENT MESSAGES (Direct)---")
for message in result_research_direct["messages"]:
    print(result_research_direct["summary"] if result_research_direct["summary"] else message.content) # Display summary or last message

print("\n---FINAL SUMMARY (Direct)---")
print(result_research_direct["summary"])
```

This `complete working examples with code` demonstrates a powerful `building AI agents` pattern. The agent intelligently decides whether to search, then summarizes, and finally answers. This covers a significant portion of our `langgraph tutorial 2026`.

### Testing and Debugging Tips

Building AI agents, especially with complex flows like LangGraph, can sometimes feel like solving a puzzle. This section of our `langgraph tutorial 2026` will give you some helpful `testing and debugging tips`. Learning how to find and fix problems quickly is a super important skill!

#### 1. Print Statements are Your Friends

The easiest way to see what's happening inside your agent is to add `print()` statements. In each of your node functions and router functions, print a message saying which function is currently running. Also, print the important parts of the `state` at the beginning and end of each function.

Example:
```python
def my_node(state: AgentState) -> dict:
    print(f"---Entering MY_NODE. Current query: {state['user_query']}---")
    # ... node logic ...
    print(f"---Exiting MY_NODE. State updated.---")
    return {"some_key": "some_value"}
```
This helps you trace the execution path and see how the state changes.

#### 2. Visualizing the Graph

For complex graphs, it's hard to keep track of all the nodes and edges in your head. LangGraph can generate a visual representation of your graph! This is like looking at a real flowchart.

You'll need to install `graphviz` for this:
```bash
pip install pygraphviz graphviz
```
Then, you can save your graph as an image:
```python
# Assuming 'app' is your compiled LangGraph workflow
from IPython.display import Image, display

# If you're in a Jupyter notebook:
display(Image(app.get_graph().draw_png()))

# Or to save to a file:
app.get_graph().draw_png("my_agent_graph.png")
```
Looking at the `my_agent_graph.png` file will show you exactly how your nodes are connected. This is invaluable for `testing and debugging tips`.

#### 3. Step-by-Step Execution

Sometimes you want to see the state at *every single step* of the agent's journey. LangGraph allows you to iterate through the execution steps.

```python
for s in app.stream(initial_state):
    print(s)
    print("-----")
```
The `app.stream()` method yields the state after each node's execution. This lets you inspect the full state after every single action, making it easy to spot where things go wrong.

#### 4. Check State Updates Carefully

A common mistake is that a node doesn't update the state correctly.
*   **Did you return a dictionary from your node?** Nodes must return a dictionary with state updates.
*   **Are the keys in the dictionary correct?** They must match the keys in your `AgentState`.
*   **Are you correctly using `Annotated[List[AnyMessage], add_message]`?** If you return `{"messages": [new_message]}`, it should add `new_message` to the list, not replace it. If you want to replace, you might need `replace_messages`. Read the LangGraph documentation for specific `Annotated` behaviors.

#### 5. Is Your Router Function Returning the Right Node Name?

When using `add_conditional_edges`, your router function must return a string that matches one of the keys in your mapping. If it returns something else, or `None`, your graph will likely crash or not follow the expected path. Always double-check the return values.

#### 6. Mocking Tools

When `adding tools to agents`, sometimes the external tool might be slow or costly. For `testing and debugging tips`, you can create "mock" versions of your tools. A mock tool is a fake tool that just returns a fixed, predictable result without actually calling the external service.

```python
# Original tool
# tavily_tool = TavilySearchResults(max_results=3)

# Mock tool
class MockTavilySearchResults:
    def invoke(self, query: str) -> str:
        print(f"---MOCK TAVILY: Simulating search for '{query}'---")
        if "population" in query.lower():
            return "[{'title': 'Mock Population Data', 'content': 'The mock population is 80 million.'}]"
        else:
            return "[{'title': 'Mock Generic Result', 'content': 'This is a mock search result.'}]"

mock_tavily_tool = MockTavilySearchResults()
mock_tools = [mock_tavily_tool]
mock_tool_executor = ToolExecutor(mock_tools)

# Then, when compiling your graph, use mock_tool_executor instead of the real one.
# workflow.add_node("tool_executor", ToolNode(mock_tool_executor))
```
This allows you to test your agent's logic quickly without relying on external services. This is a crucial `testing and debugging tips` strategy.

#### 7. Start Simple and Add Complexity

When you're building a new agent, don't try to build the whole complex thing at once. Start with just two nodes and a direct edge. Get that working. Then add a third node. Then try a conditional edge. Incrementally building your agent makes `testing and debugging tips` much easier because you know that each new piece you add is the most likely source of any new problems.

By following these `testing and debugging tips`, you'll be much more efficient in building robust AI agents with LangGraph. This completes our deep dive into this `langgraph tutorial 2026`.

### Conclusion: Your LangGraph Journey Continues

You've come a long way in this `langgraph tutorial 2026`! We started by getting your computer ready with `installation and setup`. Then, you learned about `defining state schema`, which is like giving your agent a memory. You took your first steps in `creating first LangGraph agent` by understanding `StateGraph nodes and edges`.

We then made your agents smarter by `adding tools to agents`, letting them interact with the outside world. You mastered `conditional routing logic`, which allows your agent to make intelligent decisions. Finally, we brought it all together with `complete working examples with code` and shared important `testing and debugging tips`.

You now have a solid foundation for `building AI agents` using LangGraph. The possibilities are truly endless! You can create agents that research, plan, interact with users, or even control other systems.

Keep experimenting, keep building, and don't be afraid to try new things. The world of AI is constantly evolving, and with LangGraph, you have a powerful tool at your fingertips. Happy coding, and we look forward to what you'll build in 2026 and beyond!