---
title: "How to use LangGraph interrupt to pause and resume an AI agent"
description: "Learn to effectively use LangGraph interrupt to pause and resume AI agents. Master control over your AI workflows for enhanced management and efficiency."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangGraph interrupt pause resume]
featured: false
image: '/assets/images/langgraph-interrupt-pause-resume-agent.webp'
---

## How to Use LangGraph Interrupt to Pause and Resume an AI Agent

Imagine you're playing a video game, and sometimes you need to hit the "pause" button. Maybe you need to think about your next move, get a snack, or ask for help. What if your AI agent could do the same thing? That's exactly what the `LangGraph interrupt` feature lets you do!

This amazing tool helps you pause your AI agent right in the middle of its work and then `LangGraph resume graph` whenever you are ready. It's like giving your agent a powerful "pause" and "play" button. We will explore how to use this for pausing and resuming AI agent tasks effectively.

### What is LangGraph Interrupt and Why is it Useful?

LangGraph is a fantastic tool for building complex AI agents that can think and act in multiple steps. Sometimes, during these steps, you might want the agent to stop and wait for you. This is where the `LangGraph interrupt` comes in handy.

It lets you `LangGraph interrupt pause resume` an agent's flow at specific points. Think of it as setting a temporary stop sign for your AI. This is super useful for many reasons, which we'll explore next.

### Why Pause and Resume AI Agents?

Pausing and resuming AI agents offers a lot of control and flexibility. You might want to step in and guide your agent or check its progress. This human touch can make AI agents much more powerful and reliable.

Here are a few big reasons why `LangGraph interrupt pause resume` is a game-changer:

*   **Human-in-the-Loop**: Sometimes, an AI agent needs human approval or input before it can continue. Imagine an agent writing an email; you might want to review it before it sends.
*   **Debugging and Fixing**: If your agent gets stuck or does something unexpected, you can pause it. You can then look at what it was doing, fix the problem, and then `LangGraph resume graph` its work. This is similar to setting `LangGraph breakpoints` in regular code.
*   **Complex Workflows**: For very long or important tasks, you might want to pause after each major step. This ensures everything is going correctly before moving on to the next part.
*   **User Interaction**: You can design agents that ask the user for more information or clarification. The agent pauses, waits for the user's answer, and then continues.

You can learn more about building multi-step agents with LangGraph in this post: [LangGraph StateGraph for Multi-Step AI Agents]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

### Getting Started with LangGraph Interrupt

To begin using `LangGraph interrupt`, you first need to have LangGraph installed. If you haven't already, you can get it with a simple command. Make sure your Python environment is ready for new packages.

Here’s how you can install LangGraph:

```bash
pip install langgraph langchain
```

Once installed, you can start building your agent's graph. Remember, LangGraph uses a "graph" structure where each step is a "node."

### How `interrupt_before` Works

One of the main ways to `LangGraph interrupt` an agent is by using `interrupt_before`. This means the agent will pause *just before* it runs a specific node. It's like saying, "Stop here, but don't do this next thing yet!"

Let's say you have an agent that plans a trip. It might have a step to "book flights" (a tool_node). You could use `interrupt_before` to pause the agent right before it actually tries to book flights. This gives you a chance to confirm the dates and prices.

Consider this example:

```python
{% raw %}
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
import operator

# 1. Define the Agent State
class AgentState(TypedDict):
    query: str
    tool_output: str
    final_answer: str

# 2. Define some simple nodes (steps)
def plan_task(state: AgentState):
    print("Agent is planning...")
    return {"query": state["query"] + " (planned)"}

def use_tool(state: AgentState):
    print("Agent is trying to use a tool...")
    # Simulate a tool call
    return {"tool_output": "Tool executed for: " + state["query"]}

def generate_final_answer(state: AgentState):
    print("Agent is generating final answer...")
    return {"final_answer": "Final answer based on: " + state["query"] + " and " + state["tool_output"]}

# 3. Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("planner", plan_task)
workflow.add_node("tool_executor", use_tool)
workflow.add_node("answer_generator", generate_final_answer)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "tool_executor")
workflow.add_edge("tool_executor", "answer_generator")
workflow.add_edge("answer_generator", END)

# Compile the graph with interrupt_before
app = workflow.compile(interrupt_before=["tool_executor"])

# You can now use 'app' to run your agent
# But it will pause before 'tool_executor'
{% endraw %}
```

In this code, we set `interrupt_before=["tool_executor"]`. This means that when the agent is about to run the `use_tool` node, it will pause. You will then get a chance to inspect its state or provide new input.

### Pausing an Agent Mid-Execution

When an agent hits an `interrupt_before` point, it doesn't just stop silently. LangGraph will actually raise a special error called `InterruptedByType`. This error tells you that the agent has paused and provides you with the current state of the agent. You can then catch this error in your code.

Catching this error is important because it's how you get access to the agent's state at the moment it paused. This state contains all the information the agent had up to that point. It's like getting a snapshot of its brain.

Let's see how you might run this and catch the interrupt:

```python
{% raw %}
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import InterruptedByType

memory = MemorySaver()
app_with_interrupt = workflow.compile(
    interrupt_before=["tool_executor"],
    checkpointer=memory # We need a checkpointer to save/load state
)

config = {"configurable": {"thread_id": "1"}} # A unique ID for this conversation

try:
    print("\n--- Running agent, expecting an interrupt ---")
    # The agent will run until it hits the interrupt_before node
    final_state = app_with_interrupt.invoke({"query": "Find weather in London."}, config)
    print("Agent finished without interrupt:", final_state) # This line might not be reached
except InterruptedByType as e:
    print(f"\nAgent interrupted at node: {e.node_id}")
    print("Current agent state:", e.thread_state.values)
    print("You can now inspect the state or provide new input.")
    # e.thread_state.values contains the full state at interruption
    # You would typically save this state or let the checkpointer handle it.
{% endraw %}
```

When you run this, you will see output indicating that the agent started planning, but then it got interrupted before the "tool_executor" node. The `InterruptedByType` error gives you the `thread_state`, which is exactly what you need to understand where the agent is.

### Understanding the Agent State

When your AI agent pauses, its "brain" — which we call the `state` — is preserved. This state holds all the information the agent has gathered or created so far. It includes your initial prompt, any steps it has completed, and results from any tools it used.

Knowing the state is like looking at all the notes and thoughts your agent has on its desk. This allows you to understand its current thinking process. You can see what it has processed and what it was about to do.

This `thread_state` is crucial for `LangGraph resume graph`. Without it, the agent wouldn't know where to pick up from.

### Resuming Your AI Agent

Now that you've paused your agent and looked at its state, it's time to `LangGraph resume graph` its work. To do this, you simply call the `invoke` method again, but this time, you pass in the `thread_id` that corresponds to the paused conversation. The `checkpointer` (like `MemorySaver` we used) automatically loads the last saved state.

You can also provide new input if needed. This new input will be added to the agent's state, and it will continue from where it left off, considering your new information. This is the "resume" part of `LangGraph interrupt pause resume`.

Let's continue our example from above. After the interrupt, you might provide new input or simply tell it to continue:

```python
{% raw %}
# Assuming the agent was interrupted and you have the config ready
# config = {"configurable": {"thread_id": "1"}} from previous run

print("\n--- Resuming the agent ---")
# To resume, we just call invoke again with the same thread_id.
# The checkpointer will load the last state.
# You can optionally pass new input if you want to influence the next step.
try:
    # Let's say we don't want to provide new input, just continue.
    # The next step would be 'tool_executor' because that's where it paused.
    final_state_after_resume = app_with_interrupt.invoke(None, config)
    print("Agent resumed and finished successfully!")
    print("Final state after resume:", final_state_after_resume)
except InterruptedByType as e:
    print(f"Agent was interrupted again at node: {e.node_id}")
    print("This means the node it was trying to run was also an interrupt point.")
{% endraw %}
```

In this case, `app_with_interrupt.invoke(None, config)` tells LangGraph to continue the conversation with `thread_id="1"` from its last known state. Since `tool_executor` was the next step, it will now try to run `use_tool`, and then `answer_generator`, finally reaching the `END`.

If you wanted to provide specific new input to influence the *next* step (after the interrupt), you would pass a dictionary like `{"some_key": "new_value"}` as the first argument to `invoke`. However, for just resuming, `None` or an empty dictionary is often sufficient.

### Advanced Interrupt Scenarios: LangGraph Breakpoints

`LangGraph interrupt` isn't limited to just one pause point. You can set multiple `LangGraph breakpoints` in your workflow. This allows you to stop the agent at different critical junctions. Think of it as adding several "watch points" in your agent's journey.

For instance, you might want to pause before calling a sensitive API, then again before sending a final message. This gives you fine-grained control over your agent's execution. It's especially useful when building complex `LangGraph StateGraph for Multi-Step AI Agents` ([LangGraph StateGraph for Multi-Step AI Agents]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %})).

You can specify a list of node names in `interrupt_before`:

```python
{% raw %}
# Compile the graph with multiple interrupt points
app_multiple_interrupts = workflow.compile(interrupt_before=["planner", "tool_executor"])

config_multi = {"configurable": {"thread_id": "2"}}

try:
    print("\n--- Running agent with multiple interrupts (first run) ---")
    app_multiple_interrupts.invoke({"query": "Research AI trends."}, config_multi)
except InterruptedByType as e:
    print(f"Agent interrupted at first node: {e.node_id}")
    print("State:", e.thread_state.values)
    print("--- Resuming agent (second run) ---")
    try:
        app_multiple_interrupts.invoke(None, config_multi) # Resumes from 'planner'
    except InterruptedByType as e2:
        print(f"Agent interrupted at second node: {e2.node_id}")
        print("State:", e2.thread_state.values)
        print("--- Resuming agent again (third run) ---")
        app_multiple_interrupts.invoke(None, config_multi) # Resumes from 'tool_executor'
        print("Agent finished after multiple resumes!")
{% endraw %}
```

In this setup, the agent would first pause before "planner", then after you resume, it would pause again before "tool_executor". This multi-step pausing and resuming capability provides powerful debugging and interactive control.

### Handling Human Input During Interrupts

One of the most common reasons to `LangGraph interrupt pause resume` an agent is to get human input. After the agent pauses, you can prompt the user for information, confirmation, or a decision. This information is then passed back to the agent when you resume it.

Let's imagine our trip planning agent pauses before booking flights. You could ask the user: "Are these dates and prices okay? (yes/no)". Based on their answer, you can either let the agent proceed or steer it in a different direction.

Here's how you might incorporate human input:

```python
{% raw %}
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import InterruptedByType
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
import operator

class TravelState(TypedDict):
    query: str
    flight_details: str
    hotel_details: str
    user_approval: str
    final_plan: str

def find_flights(state: TravelState):
    print("Agent finding flight details...")
    # Simulate finding flights
    return {"flight_details": "Flights found: JFK to LHR, $700, Oct 10-17"}

def find_hotels(state: TravelState):
    print("Agent finding hotel details...")
    # Simulate finding hotels
    return {"hotel_details": "Hotels found: Hilton, $200/night, Oct 10-17"}

def create_final_plan(state: TravelState):
    print("Agent creating final plan...")
    if state.get("user_approval") == "yes":
        return {"final_plan": f"Trip approved: {state['flight_details']}, {state['hotel_details']}"}
    else:
        return {"final_plan": "Trip NOT approved. Agent needs to re-plan or stop."}

# Build the graph
travel_workflow = StateGraph(TravelState)
travel_workflow.add_node("find_flights_node", find_flights)
travel_workflow.add_node("find_hotels_node", find_hotels)
travel_workflow.add_node("create_final_plan_node", create_final_plan)

travel_workflow.add_edge(START, "find_flights_node")
travel_workflow.add_edge("find_flights_node", "find_hotels_node")
travel_workflow.add_edge("find_hotels_node", "create_final_plan_node")
travel_workflow.add_edge("create_final_plan_node", END)

# Compile with interrupt before the final plan, assuming user approval is needed
travel_app = travel_workflow.compile(
    interrupt_before=["create_final_plan_node"],
    checkpointer=MemorySaver()
)

travel_config = {"configurable": {"thread_id": "travel_1"}}

print("\n--- Starting travel agent, expecting interrupt for approval ---")
try:
    travel_app.invoke({"query": "Plan a trip to London"}, travel_config)
except InterruptedByType as e:
    print(f"\nAgent paused at: {e.node_id}")
    print("Current state:", e.thread_state.values)

    # Human input step
    user_decision = input("Do you approve the flight and hotel details? (type 'yes' or 'no'): ").lower()

    print("\n--- Resuming agent with human input ---")
    final_travel_state = travel_app.invoke({"user_approval": user_decision}, travel_config)
    print("Agent resumed and finished. Final Plan:")
    print(final_travel_state["final_plan"])
{% endraw %}
```

In this example, after `find_hotels_node`, the agent pauses. We then ask the user for approval. Their "yes" or "no" is then passed back as `{"user_approval": user_decision}` when we resume the agent. The `create_final_plan_node` uses this input to decide what to do next. This is a very powerful way to make your AI agents interactive.

You might also consider using `Langchain Google Gemini Function Calling Agent Custom Tools` ([Langchain Google Gemini Function Calling Agent Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %})) to enable your agent to interact with various systems and then pause for user input.

### Saving and Loading Interrupted States

For real-world applications, you don't just want to pause an agent in memory. You often need to save its state to a database and load it later, perhaps even days later. This is where `LangGraph resume graph` becomes truly robust. LangGraph provides "checkpointers" that handle saving and loading the agent's state for you.

We used `MemorySaver` in our examples, which saves to your computer's memory. For more permanent storage, you would use checkpointers that save to a database like `SQLiteSaver` or even more robust options.

When an agent is interrupted, the checkpointer automatically saves its state. When you call `invoke` again with the same `thread_id`, the checkpointer automatically loads the last saved state. This means you can close your program and restart it, and the agent can pick up exactly where it left off.

Here's a conceptual look at how you might use `SQLiteSaver` for persistent storage:

```python
{% raw %}
from langgraph.checkpoint.sqlite import SQLiteSaver
import os

# Create a checkpointer that saves to a SQLite database file
# Make sure your database path is secure and accessible
db_path = "langgraph_checkpoints.sqlite"
memory = SQLiteSaver.from_file(db_path)

# Then, compile your app with this checkpointer
# For example, using our earlier workflow:
# app_persistent = workflow.compile(
#     interrupt_before=["tool_executor"],
#     checkpointer=memory
# )

# The rest of the invoke/resume logic remains similar,
# but now the state is stored on disk!

print(f"Agent states will be saved to: {db_path}")
print("You can close and reopen your application, and agents can resume.")
{% endraw %}
```

With a persistent checkpointer, you can `LangGraph resume graph` even if your program crashes or is intentionally shut down. This is essential for building reliable AI systems.

### Real-World Use Cases for LangGraph Interrupt

The ability to `LangGraph interrupt pause resume` an agent opens up many practical possibilities. Here are a few examples of how you can use this feature in real applications:

*   **Financial Advisor Agent**: An agent that gives financial advice might pause before making any investment recommendations. It waits for the user to confirm their risk tolerance or income changes. After confirmation, it can `LangGraph resume graph` to finalize the advice.
*   **Customer Support Agent**: A customer service agent could gather information, then pause and present a summary to the user. It asks, "Did I understand correctly?" If the user says no, the agent can adjust its understanding before trying to find a solution.
*   **Creative Writing Assistant**: An AI assisting with a story might pause after drafting a paragraph or suggesting a plot twist. It waits for the writer to provide feedback or direction, then continues the story.
*   **Complex Data Analysis**: An agent performing complex data analysis might pause after preparing a large report. It waits for a human analyst to review the initial findings before proceeding with deeper analysis or generating final conclusions. This is where tools like `Langchain Weaviate Hybrid Search Scalable RAG` ([Langchain Weaviate Hybrid Search Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %})) or `Langchain Semantic Text Splitter Chunk by Meaning` ([Langchain Semantic Text Splitter Chunk by Meaning]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %})) could be used by an agent to process data before the pause.
*   **Approval Workflows**: Any process requiring manager approval, like ordering supplies or approving a project plan. The agent prepares the request, pauses for approval, and then acts on the decision.

These examples show how `LangGraph interrupt` makes AI agents more collaborative and reliable.

### Troubleshooting Common Issues

While `LangGraph interrupt pause resume` is powerful, you might run into a few common issues. Don't worry, they're usually easy to fix!

*   **Agent Not Interrupting**:
    *   **Check `interrupt_before` list**: Make sure the node name you provided in `interrupt_before` is spelled correctly and matches an actual node in your graph.
    *   **Node never reached**: The agent might not be reaching the node you specified due to a different path or an error earlier in the graph. Check your graph edges and conditional logic.
*   **`InterruptedByType` Not Caught**:
    *   **Missing `try-except` block**: Ensure your code is wrapped in a `try...except InterruptedByType as e:` block. If not, the program will crash instead of pausing gracefully.
*   **Agent Not Resuming Correctly**:
    *   **Incorrect `thread_id`**: When resuming, you *must* use the same `thread_id` that was used when the agent was paused. Otherwise, LangGraph won't find the correct saved state.
    *   **No checkpointer**: If you haven't configured a `checkpointer` (like `MemorySaver` or `SQLiteSaver`), LangGraph won't have anywhere to save the state, and resumption won't work across `invoke` calls.
    *   **State modification issues**: Avoid directly changing the `thread_state` you get from `e.thread_state.values`. Instead, provide new input via the `invoke` method.
*   **Multiple Interruptions at Once**:
    *   If your `interrupt_before` list contains multiple nodes, the agent will pause at the *first* one it encounters in its execution path. You must resume it for it to potentially hit the *next* interrupt point.

Always remember to inspect the `thread_state` when an interruption occurs. It provides valuable clues about what the agent was doing and why it paused.

For further insights into handling agent outputs, you might find this tutorial helpful: [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}). This can help you understand and control what your agent sends back at each step, even during an interrupt.

### Conclusion

You've learned how `LangGraph interrupt` is like a "pause" button for your AI agents, giving you incredible control. By using `interrupt_before`, you can set specific `LangGraph breakpoints` where your agent will stop and wait. This lets you inspect its state, provide human input, or fix issues.

Then, you can `LangGraph resume graph` its work using the same thread ID, picking up exactly where it left off. This `LangGraph interrupt pause resume` capability makes your AI agents more interactive, reliable, and powerful for complex tasks. Whether for human approval, debugging, or building intricate workflows, the interrupt feature is an essential tool in your LangGraph toolkit.