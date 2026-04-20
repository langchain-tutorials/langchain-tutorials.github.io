---
title: "LangGraph human-in-the-loop complete guide: interrupts, breakpoints, and feedback"
description: "Unlock advanced control with this LangGraph human-in-the-loop complete guide. Master interrupts, breakpoints, and feedback for powerful, robust AI agent inte..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangGraph human-in-the-loop complete guide]
featured: false
image: '/assets/images/langgraph-human-in-the-loop-complete-guide.webp'
---

## Your Guide to LangGraph Human-in-the-Loop: A Complete Walkthrough

Imagine you're building a smart assistant that helps you plan a trip. Sometimes, the assistant might need your opinion or a quick correction to stay on track. This is where "human-in-the-loop" comes in, letting you guide the AI.

This guide will show you how to build such smart assistants using LangGraph, making sure you are always in control. We will explore how to pause, inspect, and even steer your AI agent with ease. Get ready to understand the **LangGraph human-in-the-loop complete guide**.

### Why Human-in-the-Loop is Super Important for AI Agents

Think of an AI agent as a helpful robot trying to do a task for you. Sometimes, the robot might misunderstand, or it might need extra information you have. If you can't step in and help, the robot might make mistakes or get stuck.

Human-in-the-loop (HITL) means you, a human, can jump into the robot's process at any time. You can check what it's doing, tell it what to do next, or correct its path. This makes the AI much more reliable and useful.

For complex tasks, like planning a long project or managing customer support, human input is key. It helps the AI learn, stay accurate, and handle tricky situations it hasn't seen before. You become the AI's smart co-pilot.

### Getting Started with LangGraph: Your AI's Control Panel

LangGraph is a fantastic tool that helps you build complex AI agents. It lets you create "graphs" where each part of your AI's brain (called a "node") talks to other parts in a specific order. You can learn more about how to set up these multi-step agents in our previous post: [Building Multi-Step AI Agents with LangGraph StateGraph]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

Each step in your agent's journey is a node, and LangGraph manages how data flows between them. The agent remembers things using its "state," which is like a notepad where it writes down what's happening. When you use human-in-the-loop, you'll often be looking at or changing this state.

Let's imagine you have an agent that searches for flights. It might first ask for your destination, then search, then present options. Each of these could be a node in your LangGraph.

### Interrupts: When Your AI Needs to Pause and Ask

An interrupt is like hitting the pause button on your AI agent. It stops the agent at a specific moment and waits for you to give it new instructions. This is super useful when you want to review something or provide crucial information.

LangGraph gives you two main ways to set these pause buttons: `interrupt_before` and `interrupt_after`. Both are powerful, but they work slightly differently. Let's dive into them.

#### Understanding `interrupt_before`

`interrupt_before` tells your agent, "Before you start this next step, stop and ask me." This is great if you want to check the inputs an agent is about to use for a task. You can make sure it has all the correct information before it proceeds.

Imagine your agent needs to book a hotel. You might want it to pause *before* it actually makes the booking request. This way, you can check the dates and hotel choice one last time.

Here's how you might set this up in your LangGraph code:

{% raw %}
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

# Define the state of our agent
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    human_input: str

# Define some nodes (steps) for our agent
def initial_greeting(state: AgentState):
    print("AI: Hello! How can I help you today?")
    return {"messages": ["AI: Hello! How can I help you today?"]}

def ask_for_destination(state: AgentState):
    print("AI: Where would you like to go?")
    return {"messages": ["AI: Where would you like to go?"]}

def confirm_destination(state: AgentState):
    # This node would process human_input
    destination = state.get("human_input", "unknown")
    print(f"AI: You want to go to {destination}, correct?")
    return {"messages": [f"AI: You want to go to {destination}, correct?"]}

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("greet", initial_greeting)
workflow.add_node("ask_dest", ask_for_destination)
workflow.add_node("confirm_dest", confirm_destination)

workflow.set_entry_point("greet")
workflow.add_edge("greet", "ask_dest")

# Here's where we use interrupt_before
# The agent will pause *before* executing the 'confirm_dest' node.
workflow.add_edge("ask_dest", "confirm_dest", interrupt_before=["confirm_dest"])

workflow.add_edge("confirm_dest", END)

app = workflow.compile()
```
{% endraw %}

In this example, after the agent asks for the destination, it will `interrupt_before` the `confirm_dest` node. You can then provide the destination as `human_input` to the state. This pause allows you to add specific instructions or data that the agent will use in its next step.

#### Understanding `interrupt_after`

`interrupt_after` is the opposite: "After you finish this step, stop and ask me." This is useful when you want to review the *results* of an agent's action. You can see what the AI just did and decide if it was good or if it needs a tweak.

For example, if your agent just searched for flight prices, you might want it to pause *after* it has the results. You can then look at the prices and tell the agent which option you prefer. This ensures the agent doesn't book anything without your final approval.

Let's modify our previous example to use `interrupt_after`:

{% raw %}
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    human_input: str
    search_results: str

def initial_greeting(state: AgentState):
    print("AI: Hello! How can I help you today?")
    return {"messages": ["AI: Hello! How can I help you today?"]}

def ask_for_search_query(state: AgentState):
    print("AI: What would you like to search for?")
    return {"messages": ["AI: What would you like to search for?"]}

def perform_search(state: AgentState):
    query = state.get("human_input", "no query provided")
    # In a real app, this would call a search tool
    results = f"Simulated search results for '{query}'"
    print(f"AI: I found some results for '{query}'.")
    return {"messages": [f"AI: I found some results for '{query}'."], "search_results": results}

def present_results_and_ask(state: AgentState):
    results = state.get("search_results", "No results.")
    print(f"AI: Here are the results: {results}. What do you want to do next?")
    return {"messages": [f"AI: Here are the results: {results}. What do you want to do next?"]}

workflow = StateGraph(AgentState)
workflow.add_node("greet", initial_greeting)
workflow.add_node("ask_query", ask_for_search_query)
workflow.add_node("search_tool", perform_search)
workflow.add_node("present_results", present_results_and_ask)

workflow.set_entry_point("greet")
workflow.add_edge("greet", "ask_query")
workflow.add_edge("ask_query", "search_tool")

# Here we use interrupt_after. The agent will pause *after* 'search_tool' finishes.
workflow.add_edge("search_tool", "present_results", interrupt_after=["search_tool"])

workflow.add_edge("present_results", END)

app = workflow.compile()
```
{% endraw %}

In this setup, the agent finishes `perform_search` and populates `search_results`. Then, it hits the `interrupt_after` pause. You can then review `search_results` and decide how the agent should proceed in the `present_results` node. This gives you a clear moment to intervene after the AI has done some work.

#### How to Use Interrupts in Practice

When an interrupt happens, the LangGraph system stops running. It will give you a chance to inspect the current state of the agent. You can then decide what to do next.

Typically, you will get back an `AgentState` object. You can look at all the messages, variables, and data inside it. This is your window into the AI's mind!

To resume the agent, you will call `app.invoke()` again, often with updated information. This updated information acts as your **LangGraph state update**, guiding the AI forward.

Let's see how this works with our search example:

{% raw %}
```python
# Assuming 'app' is compiled from the interrupt_after example above

print("--- Starting Agent Run 1 ---")
# First run will go from greet -> ask_query -> search_tool and then interrupt
inputs = {"messages": ["User: Start"]}
config = {"configurable": {"thread_id": "user123"}}
# The app.stream() allows you to see outputs as they happen and manage interrupts
events = app.stream(inputs, config=config)

current_state = None
for i, s in enumerate(events):
    print(f"Event {i}: {s}")
    if "__end__" in s:
        current_state = s["__end__"]
        print(f"Final State: {current_state}")
        break # Agent finished, or we found the interrupt state
    if "__interrupt__" in s:
        current_state = s["__interrupt__"]
        print(f"\n--- INTERRUPTED! Current State: {current_state} ---\n")
        break # We hit the interrupt

# Now, we are at the interrupt after 'search_tool'
# The AI asked "What would you like to search for?"
# Then it performed the search and interrupted.

# Let's say the human provides the search query
# We update the state and resume
print("\n--- Resuming Agent Run 2 with human input ---")
human_query = "LangGraph human-in-the-loop examples"
new_state_for_resume = {"human_input": human_query}

# We need to explicitly tell the app to resume from the interrupted state.
# We also need to pass the *current state* received during the interrupt.
# LangGraph automatically handles updating from the provided dict.
# Here we're using app.invoke for simplicity, but stream can also be used
# if more steps are expected before another interrupt/end.

# We're passing the human_input into the state directly.
# The 'present_results' node will then use this.
final_state = app.invoke(
    {"messages": [f"User: {human_query}"], **current_state}, # Pass the full state + new input
    config=config
)
print(f"Final state after resume: {final_state}")
print("Agent has finished after resume.")
```
{% endraw %}

In the example above, the `app.stream` method lets you process the agent's actions step-by-step. When an `__interrupt__` event is emitted, you capture the `current_state`. Then, you, the human, provide input (like `human_query`). This input is merged into the `current_state` and passed back to `app.invoke()` to resume the graph. This is a direct example of a **LangGraph state update** initiated by a human!

### Breakpoints: Peeking into Your AI's Thoughts without Stopping Everything

Breakpoints are like "soft" interrupts. They allow you to observe what your agent is doing at specific points without completely stopping its execution. It's like having a debugger where you can see variables without pausing the whole program. You can look at the current state, but the agent will keep running by itself.

Why would you use breakpoints? They are fantastic for monitoring. You might want to see the exact state before a critical decision, or after a tool call, just to ensure everything looks right. If something seems off, you can then decide to interrupt the *next* time it runs.

Breakpoints are usually set at the graph level or on specific nodes. When a breakpoint is hit, the graph will emit an event with the current state, but then immediately continue executing.

#### Setting Up Breakpoints in LangGraph

LangGraph allows you to set breakpoints globally or on specific nodes within your graph configuration. You define a list of node names where you want to pause.

Let's modify our search example to include a breakpoint. We'll set a breakpoint *after* the `perform_search` node, but unlike an interrupt, the agent will continue to `present_results` immediately.

{% raw %}
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    human_input: str
    search_results: str

def initial_greeting(state: AgentState):
    print("AI: Hello! How can I help you today?")
    return {"messages": ["AI: Hello! How can I help you today?"]}

def ask_for_search_query(state: AgentState):
    print("AI: What would you like to search for?")
    return {"messages": ["AI: What would you like to search for:"]}

def perform_search(state: AgentState):
    query = state.get("human_input", "no query provided")
    results = f"Simulated search results for '{query}'"
    print(f"AI: Performing search for '{query}'...")
    return {"messages": [f"AI: Performing search for '{query}'..."], "search_results": results}

def present_results_and_ask(state: AgentState):
    results = state.get("search_results", "No results.")
    print(f"AI: Here are the results: {results}. What do you want to do next?")
    return {"messages": [f"AI: Here are the results: {results}. What do you want to do next?"]}

workflow = StateGraph(AgentState)
workflow.add_node("greet", initial_greeting)
workflow.add_node("ask_query", ask_for_search_query)
workflow.add_node("search_tool", perform_search)
workflow.add_node("present_results", present_results_and_ask)

workflow.set_entry_point("greet")
workflow.add_edge("greet", "ask_query")
workflow.add_edge("ask_query", "search_tool")
workflow.add_edge("search_tool", "present_results")
workflow.add_edge("present_results", END)

app = workflow.compile()
```
{% endraw %}

To add the breakpoint, we'll use the `checkpoints` configuration when we run the app. This is how you tell LangGraph to log the state at certain points.

{% raw %}
```python
# Assuming 'app' is compiled from the example above

print("--- Starting Agent Run with Breakpoint ---")
inputs = {"messages": ["User: Find me information about LangChain."]}
config = {
    "configurable": {"thread_id": "user456"},
    # Here's how we set breakpoints!
    # We want to see the state after 'search_tool' node finishes.
    "checkpointer": None, # Disable default checkpointer if not needed for simplicity
    "breakpoints": ["search_tool"], # This will emit an event after 'search_tool'
}

# We'll also provide the human_input directly for this example
# to show how the agent will continue past the breakpoint.
inputs_with_human_input = {
    "messages": ["User: Find me information about LangChain."],
    "human_input": "LangChain frameworks comparison"
}

# The app.stream() will show us the breakpoint event.
events = app.stream(inputs_with_human_input, config=config)

for i, s in enumerate(events):
    print(f"Event {i}: {s}")
    if "__end__" in s:
        print(f"Final State: {s['__end__']}")
        break
    if "__breakpoint__" in s:
        print(f"\n--- BREAKPOINT HIT! State at breakpoint: {s['__breakpoint__']} ---\n")
        print("Agent will continue running automatically...")

print("Agent finished after breakpoint.")
```
{% endraw %}

When you run this code, you'll see a `__breakpoint__` event in the stream output. This event will contain the full state of the agent *at that moment*. The agent won't wait for you; it will just emit the information and keep going. This is excellent for debugging and monitoring, helping you refine your agent's behavior.

### Feedback: Guiding Your AI with Your Input

Feedback is how you, the human, communicate with your AI agent to influence its behavior. This is the core of **LangGraph human-in-the-loop complete guide**. After an interrupt or a breakpoint, you'll want to tell the agent what to do next. LangGraph provides powerful ways to integrate this human feedback.

There are a few primary ways to provide feedback:

1.  **Updating the Agent's State Directly**: This is the most common and flexible method. You modify specific variables in the agent's `AgentState`.
2.  **Simulating Tool Outputs**: If your agent expects a tool to return some data, you can provide that data yourself.
3.  **Changing the Next Node**: In some advanced scenarios, you might even tell the agent which node to run next, bypassing its own decision-making.

Let's look at how to implement these feedback mechanisms.

#### 1. Updating the Agent's State Directly (LangGraph state update)

This is the most direct way to give feedback. When an agent interrupts, you get its current state. You can then modify this state to add new information or correct existing information. When you resume, LangGraph uses this updated state.

Remember our travel planner agent? Suppose it suggests a flight from New York to London, but you wanted Paris. You can update the `destination` variable in its state from "London" to "Paris".

Here's a simple example showing a human providing feedback to correct a `task_description`:

{% raw %}
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class PlanningState(TypedDict):
    task_description: str
    messages: Annotated[List[str], operator.add]
    human_correction: str # For human feedback

def initial_task(state: PlanningState):
    print("AI: What task would you like me to help with?")
    return {"messages": ["AI: What task would you like me to help with?"]}

def clarify_task(state: PlanningState):
    task = state.get("task_description", "no task specified")
    print(f"AI: So, your task is '{task}'. Is that correct?")
    return {"messages": [f"AI: So, your task is '{task}'. Is that correct?"]}

def proceed_with_task(state: PlanningState):
    task = state.get("task_description", "no task specified")
    print(f"AI: Great! I will now proceed with '{task}'.")
    return {"messages": [f"AI: Great! I will now proceed with '{task}'"]}

workflow = StateGraph(PlanningState)
workflow.add_node("start_task", initial_task)
workflow.add_node("clarify", clarify_task)
workflow.add_node("execute", proceed_with_task)

workflow.set_entry_point("start_task")
workflow.add_edge("start_task", "clarify")
workflow.add_edge("clarify", "execute", interrupt_before=["execute"]) # Interrupt before execution

app = workflow.compile()

# --- Run 1: Agent asks for task ---
print("--- Run 1: Agent asks for task ---")
initial_input = {"messages": ["User: I need help with my project."]}
config = {"configurable": {"thread_id": "feedback_test_1"}}
events = app.stream(initial_input, config=config)

current_state = None
for i, s in enumerate(events):
    print(f"Event {i}: {s}")
    if "__interrupt__" in s:
        current_state = s["__interrupt__"]
        print(f"\n--- INTERRUPTED! Current State: {current_state} ---\n")
        break

# --- Human feedback time ---
# The agent interrupted before 'execute'.
# The 'task_description' might be missing or incorrect.
# Let's say the human wants to specify it more precisely.
print("\n--- Human provides feedback ---")
human_feedback_task = "create a detailed marketing plan for new product launch"

# We update the state with the correct task_description
updated_state_for_resume = {
    "task_description": human_feedback_task,
    "messages": [f"User: Actually, the task is to {human_feedback_task}."]
}

# Now we resume the agent with the updated state
print("\n--- Run 2: Resuming with updated state ---")
final_state = app.invoke(
    {**current_state, **updated_state_for_resume}, # Merge current state with human updates
    config=config
)
print(f"Final state after resume: {final_state}")
print("Agent has finished with human-corrected task.")
```
{% endraw %}

In this example, the agent paused, giving you a chance to look at its `task_description`. You then provided a new, more accurate `task_description` as feedback. This new information was merged into the agent's state, directly influencing its next action (`proceed_with_task`). This is a fundamental **LangGraph state update** mechanism.

#### 2. Simulating Tool Outputs for Feedback

Sometimes, an AI agent relies on "tools" (like a calculator, a search engine, or a calendar app) to do its job. When an agent calls a tool, it expects a certain type of output. If you interrupt the agent *after* it decided to use a tool but *before* the tool actually runs, you can provide the expected tool output yourself!

This is powerful for testing or when a real tool might be slow or unavailable. You can "pretend" the tool ran and give the agent the data it needs to continue. You can learn more about how agents use custom tools here: [LangChain Google Gemini Function Calling Agent with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

Let's imagine an agent that needs to fetch weather. It decides to call a `get_weather` tool. If we interrupt it, we can provide the weather data directly.

{% raw %}
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class WeatherAgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    tool_calls: List[dict] # To store simulated tool calls
    tool_outputs: List[str] # To store simulated tool outputs
    location: str

def ask_weather_location(state: WeatherAgentState):
    print("AI: What city's weather would you like to know?")
    return {"messages": ["AI: What city's weather would you like to know?"]}

def decide_tool_call(state: WeatherAgentState):
    # In a real agent, an LLM would decide this
    location = state.get("location", "New York") # Assuming human already provided location
    print(f"AI: Okay, I will call a tool to get weather for {location}.")
    # Simulate an LLM output requesting a tool call
    simulated_tool_call = {
        "name": "get_weather",
        "args": {"city": location}
    }
    return {"messages": [f"AI: Decided to call get_weather tool for {location}."], "tool_calls": [simulated_tool_call]}

def process_weather_info(state: WeatherAgentState):
    weather_data = state.get("tool_outputs", ["No weather data."])[0]
    print(f"AI: The weather information is: {weather_data}")
    return {"messages": [f"AI: The weather information is: {weather_data}"]}

workflow = StateGraph(WeatherAgentState)
workflow.add_node("ask_location", ask_weather_location)
workflow.add_node("decide_tool", decide_tool_call)
workflow.add_node("process_info", process_weather_info)

workflow.set_entry_point("ask_location")
workflow.add_edge("ask_location", "decide_tool")

# Interrupt *after* the agent decides to call the tool, but *before* it gets output
workflow.add_edge("decide_tool", "process_info", interrupt_after=["decide_tool"])
workflow.add_edge("process_info", END)

app = workflow.compile()

# --- Run 1: Agent asks for location, decides tool call, then interrupts ---
print("--- Run 1: Agent asks for location, decides tool call, then interrupts ---")
initial_input = {"messages": ["User: What's the weather like in London?"], "location": "London"}
config = {"configurable": {"thread_id": "tool_feedback_test"}}
events = app.stream(initial_input, config=config)

current_state = None
for i, s in enumerate(events):
    print(f"Event {i}: {s}")
    if "__interrupt__" in s:
        current_state = s["__interrupt__"]
        print(f"\n--- INTERRUPTED! Current State: {current_state} ---\n")
        break

# --- Human feedback: Provide simulated tool output ---
print("\n--- Human provides simulated tool output ---")
# The agent expected a tool to run and produce output.
# We will provide that output directly.
simulated_weather_output = "It's sunny and 20°C in London."
updated_state_for_resume = {
    "tool_outputs": [simulated_weather_output], # Provide the tool output
    "messages": [f"User: (Simulated tool output: {simulated_weather_output})"]
}

# Resume the agent with the simulated tool output
print("\n--- Run 2: Resuming with simulated tool output ---")
final_state = app.invoke(
    {**current_state, **updated_state_for_resume},
    config=config
)
print(f"Final state after resume: {final_state}")
print("Agent has finished with simulated tool output.")
```
{% endraw %}

Here, the agent interrupted after `decide_tool`. This means it decided *what* tool to call, but didn't actually run it yet. As the human, you stepped in and provided the `tool_outputs` directly, effectively simulating the tool's response. The agent then proceeded as if the tool had run successfully, using your provided data.

#### 3. Changing the Next Node (Advanced Feedback)

In very advanced scenarios, you might want to completely override the agent's decision on where to go next. LangGraph's `invoke` or `stream` method allows you to specify a `next_node` parameter in the `config`. This tells LangGraph to jump directly to a specific node after an interrupt.

This is less common for typical human-in-the-loop flows where you're just tweaking data. However, it can be useful for debugging or for creating highly interactive "choose your own adventure" style AI agents.

### Putting It All Together: A Complete Human-in-the-Loop Scenario

Let's build a more comprehensive example. Imagine an AI assistant that helps you write emails. It needs to:
1.  Ask for the email topic.
2.  Draft the email.
3.  Allow you to review and edit the draft (interrupt!).
4.  Optionally, perform a grammar check if you ask for it (another interrupt point for tool simulation).
5.  Finalize the email.

We'll use both `interrupt_before` and `interrupt_after` for different feedback points, demonstrating the full **LangGraph human-in-the-loop complete guide**.

First, let's define our state and nodes:

{% raw %}
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# Define the state for our email agent
class EmailAgentState(TypedDict):
    topic: str
    draft: str
    review_comments: Optional[str] # Human feedback for review
    grammar_check_requested: bool # Flag for grammar check
    grammar_check_result: Optional[str] # Result of grammar check
    messages: Annotated[List[BaseMessage], operator.add] # Using LangChain BaseMessage for richer history

# Node 1: Get the email topic
def get_topic(state: EmailAgentState):
    print("\nAI: What should be the topic of this email?")
    return {"messages": [AIMessage(content="What should be the topic of this email?")]}

# Node 2: Draft the email based on the topic
def draft_email(state: EmailAgentState):
    topic = state.get("topic", "a general update")
    # Simulate LLM drafting an email
    draft_content = f"Subject: Regarding {topic}\n\nDear Team,\n\nThis email is about {topic}. More details to follow.\n\nBest regards,\n[Your Name]"
    print(f"\nAI: I've drafted an email for '{topic}'.")
    return {"draft": draft_content, "messages": [AIMessage(content=f"I've drafted an email for '{topic}'. Here's the draft:\n{draft_content}")]}

# Node 3: Review and provide feedback
def review_draft(state: EmailAgentState):
    current_draft = state.get("draft", "No draft yet.")
    print(f"\nAI: Please review the current draft:\n---\n{current_draft}\n---\nDo you have any comments or edits? Or would you like a grammar check? (Type 'grammar' to request)")
    # We will expect human_input here, which will be 'review_comments' or 'grammar'
    return {"messages": [AIMessage(content="Please review the draft and provide comments/edits or type 'grammar' for a check.")]}

# Node 4: Perform grammar check (simulated tool)
def perform_grammar_check(state: EmailAgentState):
    current_draft = state.get("draft", "")
    # Simulate a grammar check tool
    if "More details to follow." in current_draft:
        corrected_draft = current_draft.replace("More details to follow.", "Further details will be provided.")
        grammar_result = f"Grammar check found a potential passive voice/phrasing issue. Suggested change: '{corrected_draft}'"
        return {"grammar_check_result": grammar_result, "draft": corrected_draft, "messages": [AIMessage(content=f"Grammar check complete. Here are the findings:\n{grammar_result}")]}
    else:
        return {"grammar_check_result": "No major issues found.", "messages": [AIMessage(content="Grammar check complete. No major issues found.")]}

# Node 5: Finalize the email
def finalize_email(state: EmailAgentState):
    final_draft = state.get("draft", "No final draft.")
    print(f"\nAI: The final email is ready:\n---\n{final_draft}\n---\n")
    return {"messages": [AIMessage(content="The final email is ready.")]}

# Define a conditional edge for grammar check
def should_grammar_check(state: EmailAgentState):
    if state.get("grammar_check_requested"):
        return "grammar_check"
    else:
        return "finalize"

# Build the workflow
workflow = StateGraph(EmailAgentState)

workflow.add_node("get_topic", get_topic)
workflow.add_node("draft_email", draft_email)
workflow.add_node("review_draft", review_draft)
workflow.add_node("grammar_check", perform_grammar_check)
workflow.add_node("finalize_email", finalize_email)

workflow.set_entry_point("get_topic")
workflow.add_edge("get_topic", "draft_email")

# Interrupt AFTER drafting so human can review the output
workflow.add_edge("draft_email", "review_draft", interrupt_after=["draft_email"])

# After review_draft, we have a conditional edge
# If grammar_check_requested is true, go to grammar_check, else go to finalize
workflow.add_conditional_edge("review_draft", should_grammar_check, {
    "grammar_check": "grammar_check",
    "finalize": "finalize_email"
})

# After grammar check, interrupt again to review results, then finalize
workflow.add_edge("grammar_check", "finalize_email", interrupt_after=["grammar_check"])

workflow.add_edge("finalize_email", END)

app = workflow.compile()
```
{% endraw %}

Now, let's simulate the human interaction:

{% raw %}
```python
print("--- Starting Email Agent ---")
config = {"configurable": {"thread_id": "email_workflow_1"}}
current_state = {"messages": [HumanMessage(content="Start")]} # Initial input

# --- Step 1: Get Topic (AI asks for topic) ---
print("\n--- Phase 1: AI asks for topic ---")
events = app.stream(current_state, config=config)
for s in events:
    print(s)
    if "__end__" in s or "__interrupt__" in s:
        current_state = s.get("__end__", s.get("__interrupt__"))
        break

# Human provides topic
human_topic = "Quarterly Sales Report Summary"
current_state_after_topic = {
    **current_state,
    "topic": human_topic,
    "messages": [HumanMessage(content=human_topic)]
}

# --- Step 2: Draft Email (AI drafts, then interrupts for review) ---
print("\n--- Phase 2: AI drafts email and waits for review ---")
events = app.stream(current_state_after_topic, config=config)
for s in events:
    print(s)
    if "__end__" in s or "__interrupt__" in s:
        current_state = s.get("__end__", s.get("__interrupt__"))
        break

# --- Human Review 1: Edit the draft ---
# Agent paused after 'draft_email'. Human reviews it.
print("\n--- Human provides initial draft review feedback ---")
# Let's say the human wants to add more detail and change a phrase.
new_draft_content = current_state["draft"].replace(
    "More details to follow.",
    "The full report will be presented in next week's meeting. Key highlights are attached."
)
human_review_comments = "Added more specific info about the report and attachments."

updated_state_after_review = {
    **current_state,
    "draft": new_draft_content,
    "review_comments": human_review_comments,
    "messages": [HumanMessage(content=f"Human feedback: {human_review_comments} Updated draft: {new_draft_content}")]
}

# --- Step 3: Agent processes review, then decides on grammar check or finalize ---
print("\n--- Phase 3: Agent processes review and potentially asks for grammar check ---")
events = app.stream(updated_state_after_review, config=config)
for s in events:
    print(s)
    if "__end__" in s or "__interrupt__" in s:
        current_state = s.get("__end__", s.get("__interrupt__"))
        break

# The agent should have gone to 'review_draft' then either 'grammar_check' or 'finalize_email'
# If grammar check was not requested, it would go straight to finalize.
# Let's now assume human wants a grammar check.
print("\n--- Human requests grammar check ---")
human_request_grammar = True # This would come from user input 'grammar'
updated_state_for_grammar = {
    **current_state,
    "grammar_check_requested": human_request_grammar,
    "messages": [HumanMessage(content="User: Please perform a grammar check.")]
}

# --- Step 4: Agent performs grammar check, then interrupts to review grammar results ---
print("\n--- Phase 4: Agent performs grammar check and waits for review ---")
events = app.stream(updated_state_for_grammar, config=config)
for s in events:
    print(s)
    if "__end__" in s or "__interrupt__" in s:
        current_state = s.get("__end__", s.get("__interrupt__"))
        break

# --- Human Review 2: Review grammar check results ---
print("\n--- Human reviews grammar check results and accepts changes ---")
# The agent paused after 'grammar_check'. Human reviews the suggestions.
# Let's assume the human accepts the grammar correction.
# The 'draft' should already be updated by the grammar_check node.
final_human_feedback = "Looks good. Accept grammar changes."
final_state_after_grammar_review = {
    **current_state,
    "messages": [HumanMessage(content=final_human_feedback)]
}

# --- Step 5: Agent finalizes email ---
print("\n--- Phase 5: Agent finalizes email ---")
events = app.stream(final_state_after_grammar_review, config=config)
for s in events:
    print(s)
    if "__end__" in s or "__interrupt__" in s:
        current_state = s.get("__end__", s.get("__interrupt__"))
        break

print("\n--- Workflow Complete! ---")
print(f"Final State: {current_state}")
```
{% endraw %}

This example shows a full round-trip of interaction. The agent asks for information, drafts something, then pauses for your review. You can then edit the draft, or even ask the agent to perform another action (like a grammar check). Each time you provide input, you are performing a **LangGraph state update**, actively guiding the AI.

### Advanced Tips for LangGraph Human-in-the-Loop

*   **Clear Prompts for Humans**: When the agent interrupts, make sure the message you give to the human is very clear. What feedback is needed? What are the options?
*   **Version Control for State**: For very critical applications, consider having a way to "undo" or revert the agent's state if human feedback leads it astray. LangGraph's checkpointer can help here.
*   **User Interface (UI) Integration**: In a real application, you'd integrate these interrupts and feedback loops with a user interface. This UI would display the agent's current state, allow the human to input text, and then send the updated state back to LangGraph.
*   **Error Handling**: What happens if the human provides invalid feedback? Your LangGraph should have nodes to gracefully handle such situations, perhaps by asking for clarification.
*   **Combining with RAG**: Imagine an agent that performs Retrieval Augmented Generation (RAG) to answer questions. You could interrupt it after it retrieves documents to let the human verify if the documents are relevant before the AI generates an answer. This ensures the information base is correct. You can learn more about RAG here: [Build RAG Applications with LangChain Vector Store 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

### Conclusion

You've now got a comprehensive understanding of building **LangGraph human-in-the-loop** systems. You know how to use **LangGraph interrupt_before interrupt_after** to pause your AI, and how **LangGraph breakpoints** allow you to peek into its workings. Most importantly, you understand how to provide effective feedback through **LangGraph state update** to steer your agent towards the best possible outcome.

By putting humans in the loop, you create more robust, reliable, and user-friendly AI applications. Your AI agents become true collaborators, combining the speed of automation with the wisdom and judgment of human intelligence. Keep experimenting, and empower your AI with the human touch!