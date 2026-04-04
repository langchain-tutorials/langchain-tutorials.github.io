---
title: "How to Chain OpenAI Function Calls in LangChain for Multi-Step Agent Workflows"
description: "Master LangChain chained function calls to build powerful multi-step AI agents. Learn to link OpenAI function calls and create advanced workflows efficiently."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain chained function calls]
featured: false
image: '/assets/images/langchain-chain-openai-function-calls-multi-step-agent-workflows.webp'
---

## How to Chain OpenAI Function Calls in LangChain for Multi-Step Agent Workflows

Welcome to the exciting world of AI agents! Imagine an AI that doesn't just answer questions but can think step-by-step to solve problems. This is exactly what **multi-step agent** workflows allow us to build. We're going to explore how you can make these agents super smart by using **LangChain chained function calls**.

This guide will show you how to build AI agents that can use multiple tools, one after another, to complete complex tasks. You'll learn the magic behind **sequential tool use** and how it brings advanced AI capabilities to your projects. Let's dive in!

### The Power of Multi-Step Agent Workflows

Think about solving a complex problem in real life. You don't just do one thing and expect it to be finished, right? You often break it down into smaller steps. For example, if you want to bake a cake, you first gather ingredients, then mix them, then bake, and finally decorate.

AI agents work in a similar way. A **multi-step agent** is an AI that can perform a series of actions to achieve a bigger goal. Instead of just giving one answer, it can use different tools, process information, and then decide what to do next. This makes AI much more powerful and versatile.

Without multi-step capabilities, an agent might struggle with tasks that require looking up information, calculating, and then summarizing. **LangChain chained function calls** are what make these sophisticated actions possible. You're giving your agent a brain and the ability to use its hands in sequence.

### Understanding OpenAI Function Calling and LangChain

Before we chain things, let's briefly understand the basics. OpenAI's language models, like GPT-4, have an amazing feature called "function calling." This means the AI can decide that it needs to use a specific tool (like a calculator or a search engine) to answer your question or complete your task.

Instead of directly performing the action, the AI tells you which tool it wants to use and what information to send to it. You then run the tool and give the result back to the AI. LangChain is like a helpful assistant that makes this whole process much easier to manage. It helps you define your tools, create your agents, and manage the back-and-forth conversation with the AI.

LangChain provides a framework that bridges your language model with external data and computation. It lets you create complex applications by combining different components. This includes defining custom tools that your agent can use, which is essential for **LangChain chained function calls**.

### The Core Idea: LangChain Chained Function Calls

What exactly are **LangChain chained function calls**? Imagine your agent needs to find the weather in a city, and then, based on that, decide if it needs to pack an umbrella. This involves two steps: first, checking the weather (Tool 1), and second, deciding about the umbrella (using the information from Tool 1).

**LangChain chained function calls** mean an agent can call one tool, get a result, and then use that result as input for *another* tool, or to decide its next action. This sequence of tool use is critical for any **multi-step agent** workflow. It allows the agent to build up knowledge and progress towards a complex goal.

This capability is what transforms a simple chatbot into an intelligent assistant. You're essentially teaching your AI how to think and act in a sequence, just like a human would. This process is also known as **chained tool calls**, emphasizing the continuous nature of the operations.

### Setting Up Your Environment for Chained Function Calls

To start building your clever agents, you first need to set up your workspace. It's like preparing your tools before starting a craft project. You'll need Python installed on your computer.

First, you'll install the necessary libraries. This includes LangChain itself and the OpenAI library, which lets us talk to OpenAI's models. You can do this using pip, Python's package installer.

```bash
pip install langchain langchain-openai tavily-python # tavily for search tool later
```

Next, you need to tell your program your OpenAI API key. This key is like a secret password that lets your program use OpenAI's powerful AI models. You should never share your API key with anyone. It's best to store it as an environment variable so your code can access it securely without you putting it directly into your script.

```python
import os

# Replace 'your_openai_api_key_here' with your actual key
# It's better to set this in your environment variables, e.g., export OPENAI_API_KEY='sk-...'
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
os.environ["TAVILY_API_KEY"] = "YOUR_TAVILY_API_KEY" # For the search tool example
```

Once these steps are done, you're ready to start building! You have all the pieces in place to begin crafting your **LangChain chained function calls**. Your development environment is now fully prepared for advanced agent development.

### Building Your First Tools for Multi-Step Agent Workflows

Agents become smart because they can use tools. These tools are like apps on your phone; they do specific jobs. For our agents, we define Python functions that the AI can "call" when it needs to.

Let's create two simple tools: a calculator and a mock search engine. The calculator will simply add two numbers, and the search engine will pretend to find information. These are perfect for demonstrating **LangChain chained function calls**.

```python
from langchain.tools import tool

# --- Calculator Tool ---
@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two integers together and returns the sum.
    Useful for basic arithmetic operations.
    """
    print(f"Calling add_numbers tool with {a} and {b}")
    return a + b

# --- Mock Search Tool ---
@tool
def search_web(query: str) -> str:
    """Searches the web for a given query and returns a summary of the results.
    Useful for finding current information, facts, or definitions.
    """
    print(f"Calling search_web tool with query: '{query}'")
    if "weather in London" in query.lower():
        return "The weather in London is currently 15 degrees Celsius and cloudy."
    elif "stock price of Apple" in query.lower():
        return "Apple's stock price is $170 today. Three months ago, it was $160."
    elif "current date" in query.lower():
        return "Today's date is October 26, 2023."
    else:
        return f"Couldn't find specific information for '{query}'. Generic search result."

# Collect our tools in a list
tools = [add_numbers, search_web]
```

Each function is decorated with `@tool`, which helps LangChain understand it's an agent tool. We give each tool a clear description, which is very important. The agent uses these descriptions to decide which tool to pick for **sequential tool use**. A good description tells the AI exactly what the tool does and when it's useful.

### Creating a Basic Agent with Tools

Now that we have our tools, let's create a simple agent that can use them. We'll use a chat model from OpenAI, like `ChatOpenAI`, as the brain of our agent. Then, we'll combine the tools and the model to create an agent executor. This executor is what makes the agent think and act.

The agent executor takes your prompt, passes it to the AI model, waits for the AI to decide on a tool call, executes that tool, and then feeds the result back to the AI. This loop continues until the AI thinks it has an answer or has completed the task. This forms the basis of **LangChain chained function calls**.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

# Initialize the language model
# We'll use a capable model that supports function calling
llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

# Define the prompt template for our agent
# This tells the agent its role and how to interact
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage("You are a helpful AI assistant. You can use the provided tools to answer questions."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), # This is where the agent stores its thoughts and tool outputs
    ]
)

# Create the agent
# This agent is designed to use OpenAI's function calling capabilities
agent = create_openai_tools_agent(llm, tools, prompt)

# Create the agent executor
# This is the "engine" that runs the agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

In this setup, `verbose=True` is very helpful for debugging. It lets you see the agent's "thoughts" – when it decides to call a tool, what arguments it uses, and what the tool returns. This insight is crucial for understanding how **LangChain chained function calls** unfold. It helps you see the **sequential tool use** in action.

### Implementing LangChain Chained Function Calls: A Simple Example

Let's put our agent to the test with a task that requires more than one step. Imagine you want to know the current stock price of Apple, and then calculate what it would be if it increased by 10. This requires searching for the stock price first, and then using a calculator.

This is a perfect example of **LangChain chained function calls**. The agent must first use the `search_web` tool to get the stock price. Once it has that number, it then needs to use the `add_numbers` tool to perform the calculation. You'll see the agent decide this all on its own.

```python
print("\n--- Example 1: Chaining Search and Calculator ---")
result = agent_executor.invoke({"input": "What is Apple's current stock price plus 10?"})
print(result["output"])
```

**Expected Agent Output (simplified verbose log):**

```
> Entering new AgentExecutor chain...
Thought: I need to find Apple's current stock price first, then add 10 to it. I will use the `search_web` tool to find the stock price.
Action:
```json
{
  "tool_name": "search_web",
  "tool_input": {
    "query": "Apple's current stock price"
  }
}
```
Observation: Calling search_web tool with query: 'Apple's current stock price'
Apple's stock price is $170 today. Three months ago, it was $160.
Thought: I have the current stock price, which is $170. Now I need to add 10 to it. I will use the `add_numbers` tool.
Action:
```json
{
  "tool_name": "add_numbers",
  "tool_input": {
    "a": 170,
    "b": 10
  }
}
```
Observation: Calling add_numbers tool with 170 and 10
180
Thought: I have calculated the new stock price. I can now provide the answer.
Final Answer: If Apple's current stock price of $170 increases by 10, it would be $180.

> Finished chain.
```

Did you see that? The agent first called `search_web`, extracted the "170" from the result, and then immediately used that "170" as input for the `add_numbers` tool. This seamless flow demonstrates the power of **LangChain chained function calls**. It's a clear instance of **sequential tool use**.

### Beyond Simple Chains: The Need for LangGraph for Complex Workflows

While our previous example shows basic chaining, real-world **multi-step agent** workflows can get much more complicated. What if an agent needs to try multiple tools, go back and forth, or handle loops? For example, if a search fails, it might need to rephrase the query and try again. Or if it needs to process a list of items, applying the same tool to each one.

This is where LangGraph comes in. LangGraph is an extension of LangChain that helps you build agents as "graphs." Think of a flowchart where each box is an action or a decision point, and arrows show how to move between them. LangGraph lets you define these flows precisely, giving you much more control over the agent's behavior. It's particularly powerful for managing **function call loop** scenarios.

LangGraph helps you define complex sequences, loops, and conditional logic. This is essential for robust **sequential tool use** and building truly intelligent **multi-step agent** systems. It takes **LangChain chained function calls** to the next level by making them programmable and stateful.

### Designing a LangGraph Agent for Complex Chaining

Let's build a more sophisticated **multi-step agent** using LangGraph. Our agent will:
1.  Receive a query.
2.  Search for information.
3.  *If* the search results are not sufficient or clear, it will re-evaluate and search again.
4.  Once satisfied, it will answer the question.

This scenario highlights a **function call loop** – the agent might go back to the search tool multiple times. A regular `AgentExecutor` can do this to some extent, but LangGraph gives you explicit control over the state and transitions.

We'll define an agent state that keeps track of messages (the conversation history) and define nodes for "tool_use" and "agent_decision". We'll then set up conditional edges to control the flow.

```python
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, FunctionMessage
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from langchain_community.tools.tavily_research import TavilySearchResults # Using a real search tool for better demo

# 1. Define our Agent State
# This is what our agent remembers as it works through a problem
class AgentState(TypedDict):
    # The history of messages between the agent and the user
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    # To store previous tool output if needed for re-evaluation
    tool_output: str | None

# 2. Define our tools (we'll use a real search tool this time!)
# Ensure you have TAVILY_API_KEY set in your environment variables
# You might need to install 'langchain-community' and 'tavily-python'
# pip install langchain-community tavily-python
tavily_search = TavilySearchResults(max_results=2) # Limit results for brevity

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.
    Useful for performing calculations.
    """
    print(f"Calling calculator tool with expression: '{expression}'")
    try:
        return str(eval(expression)) # Be careful with eval in production!
    except Exception as e:
        return f"Error calculating: {e}"

tools = [tavily_search, calculator]

# 3. Create the LLM for the agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 4. Create the LangChain Agent (this is the "brain" that suggests tool calls)
# It's an OpenAI tools agent which is good for function calling
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. You can use the provided tools to answer questions. Always try to be concise."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
# We need to pass the tools available to the agent for it to know what to call
agent_runnable = create_openai_tools_agent(llm, tools, agent_prompt)


# 5. Define the nodes in our LangGraph agent
def call_agent(state: AgentState):
    """
    Invokes the LangChain agent with the current conversation history.
    The agent will decide whether to make a tool call or respond directly.
    """
    messages = state["messages"]
    print(f"\n--- Agent Thinking ---")
    response = agent_runnable.invoke({"input": messages[-1].content, "agent_scratchpad": messages[:-1]})
    return {"messages": [response]} # The response itself is a BaseMessage


def call_tool(state: AgentState):
    """
    Executes the tool suggested by the agent.
    """
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    tool_output_messages = []
    print(f"\n--- Tool Call ---")
    for tool_call in tool_calls:
        print(f"Executing tool: {tool_call.name} with args: {tool_call.args}")
        # Find the correct tool and execute it
        found_tool = next(t for t in tools if t.name == tool_call.name)
        output = found_tool.invoke(tool_call.args)
        tool_output_messages.append(FunctionMessage(content=str(output), name=tool_call.name))
        print(f"Tool output: {output}")
    return {"messages": tool_output_messages, "tool_output": tool_output_messages[0].content if tool_output_messages else None} # Store output


# 6. Define the conditional logic (how the agent moves between nodes)
def should_continue(state: AgentState):
    """
    Determines if the agent should continue by calling a tool or if it has finished.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("--- Decision: Agent wants to use a tool ---")
        return "continue" # Go to call_tool node
    else:
        print("--- Decision: Agent wants to respond ---")
        return "end" # Go to END

# 7. Build the Graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_agent)
workflow.add_node("tools", call_tool)

# Set the entry point
workflow.set_entry_point("agent")

# Add edges (how to move between nodes)
workflow.add_conditional_edges(
    "agent",       # From the 'agent' node
    should_continue, # Use this function to decide next step
    {
        "continue": "tools", # If 'continue', go to 'tools' node
        "end": END           # If 'end', the graph finishes
    }
)
# After a tool is called, we want the agent to think again
workflow.add_edge("tools", "agent")

# Compile the graph
app = workflow.compile()

print("\n--- LangGraph Agent Ready ---")
```

This LangGraph agent provides a structured way to handle **LangChain chained function calls**. Each step is a node, and the `should_continue` function acts as the decision-maker, guiding the agent's flow. This is crucial for **multi-step agent** workflows that need robust decision-making and potential **function call loop** behavior.

### Practical Example: Complex Chaining with LangGraph

Let's test our `LangGraph agent` with a question that might require multiple search attempts or a combination of tools.

#### Scenario 1: Basic Chaining (Search + Calculator)

```python
print("\n--- LangGraph Example 1: Search and Calculate ---")
inputs = {"messages": [HumanMessage(content="What is the square root of the number of active volcanoes in the world?")]}
for s in app.stream(inputs):
    if "__end__" not in s:
        print(s)
print(s) # Print final state

# Or directly get the result
# final_state = app.invoke(inputs)
# print(f"\nFinal Answer: {final_state['messages'][-1].content}")
```

**Expected Flow (simplified):**
1.  **Agent Node**: User asks about volcanoes.
2.  **should_continue**: Agent decides to call `tavily_search` tool for "number of active volcanoes".
3.  **Tools Node**: `tavily_search` is executed, returns a number (e.g., "around 1500").
4.  **Agent Node (re-enters)**: Agent receives search result.
5.  **should_continue**: Agent decides to call `calculator` tool for "sqrt(1500)".
6.  **Tools Node**: `calculator` is executed, returns the result.
7.  **Agent Node (re-enters)**: Agent receives calculation result.
8.  **should_continue**: Agent decides it has the final answer.
9.  **END**: Graph finishes, agent outputs the answer.

This clearly shows **sequential tool use** and how the `LangGraph agent` moves through its defined states.

#### Scenario 2: Handling Ambiguity or Multiple Searches (Simulated)

Let's simulate a scenario where the agent might need to re-evaluate or search twice. While our current `tavily_search` will give a direct answer, you can imagine scenarios where the first search is too broad, and the agent needs to refine its query.

```python
print("\n--- LangGraph Example 2: More Complex Search (Simulated) ---")
# For this example, we'll manually feed the agent a less-than-ideal search result
# to simulate it needing to re-evaluate or perform a secondary search.
# In a real scenario, the LLM would naturally decide to refine its query.

inputs_complex = {"messages": [HumanMessage(content="Tell me about the biggest recent tech acquisition and its impact.")]}
for s in app.stream(inputs_complex):
    if "__end__" not in s:
        print(s)
print(s)
```

In a more advanced setup, the `call_agent` node could analyze the `tool_output` from the `call_tool` node. If the output is "empty" or "not relevant," the agent could then decide to call `tavily_search` again with a modified query, creating a true **function call loop**. LangGraph allows you to build this logic right into your `should_continue` function or by adding more decision nodes. This makes building a robust **multi-step agent** significantly easier.

### Handling Complex Function Call Loops and Conditional Logic

The real power of LangGraph for **LangChain chained function calls** comes with its ability to manage **function call loop** scenarios and complex conditional logic. Imagine an agent that needs to extract data from a document, then summarize it, then ask follow-up questions *based on the summary*, and potentially re-read parts of the document.

**Example: Iterative Refinement**

An agent might perform an initial search, get some results, then realize it needs more specific information. It could then formulate a *new* search query based on the initial results, run the search again, and repeat this until it has sufficient data. This is a classic **function call loop**.

To implement this, your `should_continue` function or additional helper nodes would need to evaluate the `tool_output` stored in the `AgentState`.
*   If `tool_output` indicates missing information: Transition back to the `agent` node to generate a new tool call (a refined search).
*   If `tool_output` is sufficient: Transition to another tool (e.g., a summarizer or calculator) or to `END`.

This dynamic decision-making is what makes **multi-step agent** workflows truly intelligent. You can define specific checks within your graph nodes to ensure the agent progresses optimally. This level of control is harder to achieve with simpler `AgentExecutor` setups.

### Best Practices for LangChain Chained Function Calls

Building effective **multi-step agent** workflows requires more than just knowing the code; it requires good design principles. Here are some best practices:

*   **Clear Tool Descriptions:** This is paramount. The AI relies entirely on your tool descriptions to decide when and how to use them. Be precise about what each tool does and what kind of input it expects. Think of it like writing an instruction manual for a very smart, but literal, intern.
*   **Small, Focused Tools:** Each tool should do one thing well. Don't try to make a "super-tool" that does everything. This makes your tools easier to test, debug, and for the AI to understand their purpose. It also facilitates fine-grained **sequential tool use**.
*   **Robust Error Handling in Tools:** What happens if your calculator gets non-numeric input? Or if your search tool fails? Your Python functions that act as tools should gracefully handle errors. Return informative error messages so the AI can potentially understand the failure and try a different approach.
*   **Managing Context Window Limits:** Language models have a limit on how much text they can remember in a conversation (the "context window"). In long **multi-step agent** workflows with many **LangChain chained function calls**, the conversation history can grow very large. You might need strategies like summarizing past turns or only keeping the most recent, relevant messages.
*   **Verbose Logging for Debugging:** Always start with `verbose=True` for your agent executors or use print statements in LangGraph nodes. Seeing the agent's thought process is invaluable for understanding why it chose a particular tool or made a specific decision. This helps you debug unintended **function call loop** behavior.
*   **When to Use Simple Chains vs. LangGraph:**
    *   **Simple AgentExecutor:** Good for straightforward **LangChain chained function calls** where the flow is mostly linear (Tool A -> Tool B -> Answer). Ideal for agents that generally know the path to take.
    *   **LangGraph Agent:** Essential for complex **multi-step agent** workflows involving conditional logic, loops, retries, and explicit state management. Use it when your agent needs to dynamically adapt its strategy based on tool outputs or intermediate results. This is where advanced **sequential tool use** patterns shine.
*   **Test Thoroughly:** Test your agents with various inputs, including edge cases and unexpected queries. Does it handle irrelevant questions gracefully? Does it get stuck in a **function call loop**? Comprehensive testing will reveal weaknesses in your agent's design.

### Troubleshooting Common Issues

Even with best practices, you might run into bumps. Here are some common problems and how to approach them:

*   **Agent Not Calling the Right Tool:**
    *   **Check tool descriptions:** Are they clear and specific? Does the prompt suggest a tool's use case that doesn't match its description?
    *   **Check prompt:** Does your `SystemMessage` clearly instruct the agent to use tools? Sometimes, making the prompt more explicit about tool use can help.
    *   **Test individual tools:** Make sure each tool works correctly when called directly, outside the agent.
*   **Infinite Function Call Loop:**
    *   This often happens in LangGraph when your conditional logic `should_continue` always returns `continue` or your agent consistently suggests the same tool without making progress.
    *   **Review agent's "thoughts" (verbose log):** What is the agent thinking before it re-calls the tool? Is it getting stuck on a particular piece of information?
    *   **Examine tool output:** Is the tool returning an unexpected result that makes the agent believe it needs to try again?
    *   **Add "stopping" conditions:** In LangGraph, explicitly define conditions under which the graph should reach `END`. For instance, if an agent has tried a specific tool 'X' number of times, it should stop or try a different strategy.
*   **Tool Output Not Being Used Correctly:**
    *   **Check tool function return types:** Is your tool returning the data type (string, int, JSON) that the AI expects or can easily parse?
    *   **Review agent's "thoughts":** Is the AI correctly understanding the observation it receives from the tool? Sometimes, a very long or complex tool output might confuse the AI. You might need to make tool outputs more concise or structured.
    *   **Prompt engineering:** If the output is complex, you might need to instruct the AI in your prompt on how to interpret or extract information from tool results.
*   **Agent Not Reaching a Final Answer:**
    *   This can be related to loops or ambiguous goals.
    *   Ensure your prompt clearly defines what constitutes a "final answer" or task completion.
    *   For LangGraph, ensure all possible paths eventually lead to `END`.

By carefully reviewing the agent's internal monologue (when `verbose=True`) and the outputs of your tools, you can usually pinpoint where the breakdown in your **LangChain chained function calls** is occurring.

### Conclusion: Unlocking Complex AI Capabilities

You've now learned about the fascinating world of **LangChain chained function calls** and how they enable powerful **multi-step agent** workflows. From simple **sequential tool use** to complex **function call loop** scenarios managed by a `LangGraph agent`, you have the knowledge to build AI assistants that can tackle truly challenging tasks.

By allowing agents to use multiple tools in sequence, gather information, and make decisions along the way, you are moving beyond basic question-answering. You are empowering your AI to become a problem-solver. Whether you're building a data analysis agent, a creative writing assistant, or a customer support bot, the ability to chain tool calls is a game-changer.

Keep experimenting with different tools and complex scenarios. The field of AI agents is rapidly evolving, and mastering **LangChain chained function calls** is a crucial skill. What complex **multi-step agent** will you build next? The possibilities are truly endless!