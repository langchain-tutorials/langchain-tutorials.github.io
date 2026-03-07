---
title: "Advanced LangGraph Conditional Edges Examples: Multi-Path Routing Tutorial"
description: "Unlock advanced conditional edges for multi-path routing in LangGraph with practical examples to build dynamic AI agent workflows effectively."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [advanced conditional edges multi-path]
featured: false
image: '/assets/images/advanced-langgraph-conditional-edges-multi-path-routing.webp'
---

## Advanced LangGraph Conditional Edges Examples: Multi-Path Routing Tutorial

Welcome to an exciting journey into the heart of LangGraph! Today, we're going to explore something super powerful: **advanced conditional edges multi-path** routing. This isn't just about simple "yes" or "no" decisions; it's about building smart, adaptable AI agents that can navigate many different paths based on what's happening.

Imagine your AI agent as a sophisticated train network. Basic conditional edges are like a simple switch, sending the train left or right. But with **advanced conditional edges multi-path**, you're building a grand central station with many platforms and intelligent signal systems. These systems decide which track to take based on complex rules, priorities, and even the current weather!

This tutorial will help you understand and build complex routing functions. We'll look at how to create agents that make really smart decisions. You will learn how to design systems that handle **multi-way branching** gracefully, making your AI much more capable.

### What are Conditional Edges in LangGraph?

Before we dive into the advanced stuff, let's quickly remember what conditional edges are. In LangGraph, your AI agent's "brain" is a graph made of nodes and edges. Nodes are like little action stations where your agent does something, like thinking or calling a tool.

Edges are the connections between these nodes. A conditional edge is a special type of connection. It doesn't just send the agent from one node to the next automatically.

Instead, a conditional edge uses a special "router" function. This function looks at the current situation, or "state," of your agent. Based on what it sees, the router decides which of several possible next nodes the agent should go to. Think of it as a crossroads with a traffic controller.

If you want a refresher on the basics, you can check out [Link to your basic LangGraph tutorial] here. Understanding the fundamentals will make diving into **advanced conditional edges multi-path** much smoother. This ensures you have a strong foundation for building sophisticated AI workflows.

### Understanding Multi-Path Routing

**Multi-path routing** simply means that your AI agent can choose from more than two paths to continue its work. Instead of just an "if A, go here; else, go there" scenario, it can be "if A, go to path X; if B, go to path Y; if C, go to path Z; else, go to path W." This opens up many possibilities for building truly intelligent systems.

It allows your agent to handle many different types of requests or situations. This makes your AI more flexible and robust. You can think of it as giving your agent a full map with many routes, not just two roads.

#### Why You Need Multi-Path Routing

You might wonder why this is so important for your AI projects. The simple answer is that real-world problems are rarely simple. They often require **complex routing functions**. A basic chat bot might only need a simple yes/no.

However, a sophisticated AI assistant needs to do much more. It needs to decide if it should answer a question directly, search an external database, ask for more information, or even hand off to a human. This is where **multi-path routing** shines. It allows your agent to handle all these scenarios.

It helps in creating intelligent agents that can adapt to many situations. This ensures that your agent always chooses the most appropriate action. Without **advanced conditional edges multi-path**, your agent would be very limited.

### Advanced Conditional Edges: The Core Concepts

Now, let's explore the cool stuff! **Advanced conditional edges multi-path** routing involves making your router functions much smarter. We're moving beyond simple checks to building truly intelligent decision-making systems.

These techniques allow your agent to process information more deeply. This leads to more nuanced and effective responses. You'll be able to create agents that feel genuinely intelligent.

#### Complex Routing Functions

The heart of **advanced conditional edges multi-path** lies in **complex routing functions**. These are Python functions that take your agent's current state as input. They then return a string that names the next node. Simple routers might just check one variable.

However, complex routers can check multiple variables. They can also perform calculations or even call other small functions to make their decision. This allows for much more sophisticated logic.

Imagine a customer service bot trying to figure out what to do. It might check the user's query for keywords, look at their past interaction history, and even consider the time of day. All these factors contribute to the **multi-criteria routing** decision.

```python
# A simple example of a complex routing function sketch
def decide_next_step(state: dict):
    user_message = state.get("user_input", "").lower()
    has_history = state.get("previous_interactions", 0) > 0
    sentiment = state.get("sentiment", "neutral")

    if "urgent" in user_message or sentiment == "negative":
        return "escalate_to_human"
    elif "help" in user_message and not has_history:
        return "offer_intro_faq"
    elif "product" in user_message:
        return "search_product_info"
    else:
        return "general_chat_response"
```

This function demonstrates **multi-criteria routing** by checking several pieces of information. It uses the message content, interaction history, and sentiment. This enables a more intelligent routing decision.

#### Switch-Case Patterns

Many programming languages have something called a "switch-case" statement. It lets you pick one action from a list of many based on a single value. In LangGraph, you can create similar **switch-case patterns** using your routing functions.

Your router function will check a specific value in the state. Then, it will return a different node name for each possible value. This is a very clean way to handle **multi-way branching** when you have many distinct options.

This pattern makes your routing logic easy to read and manage. It is especially useful when your agent has a clear set of predefined actions. Each action corresponds to a specific state value.

```python
# Simulating a switch-case pattern
def route_by_intent(state: dict):
    detected_intent = state.get("intent", "general_query")

    if detected_intent == "booking_flight":
        return "flight_booking_agent"
    elif detected_intent == "check_status":
        return "order_status_checker"
    elif detected_intent == "tech_support":
        return "tech_support_bot"
    elif detected_intent == "feedback":
        return "feedback_collector"
    else:
        return "general_info_handler"
```

Here, the `route_by_intent` function acts like a switch. It routes to different nodes based on the `detected_intent`. This is a prime example of **multi-way branching** implemented cleanly.

#### Cascading Conditions

**Cascading conditions** mean you evaluate conditions one after another, in a specific order. If the first condition is true, you take that path. If not, you check the second condition. If that's true, you take *that* path, and so on.

This is very useful for **priority-based paths**. You can define the most important conditions first. Then, you define less important conditions later.

Think of it like a series of gates. You try to go through Gate A first. If it's locked, you try Gate B. If that's also locked, you try Gate C. This ensures that the most critical paths are always checked first.

```python
# Example of cascading conditions for routing
def route_with_priority(state: dict):
    user_status = state.get("user_tier", "standard")
    issue_urgency = state.get("urgency", "low")
    system_health = state.get("system_status", "ok")

    # Highest priority: System critical issues
    if system_health == "critical":
        return "system_alert_node"

    # Next priority: Urgent issues for VIP users
    if issue_urgency == "high" and user_status == "vip":
        return "vip_emergency_support"

    # Then: Urgent issues for standard users
    if issue_urgency == "high":
        return "standard_emergency_support"

    # Finally: General inquiries
    return "general_inquiry_handler"
```

This `route_with_priority` function shows **cascading conditions**. It checks for critical system alerts first, then urgent VIP issues, then urgent standard issues. This sets up clear **priority-based paths**.

#### Multi-Criteria Routing

**Multi-criteria routing** means that your routing decision depends on more than one piece of information at the same time. You combine several factors to make a smart choice. For example, your agent might look at the user's message, their account type, and the current time of day.

It's like a chef deciding what to cook. They don't just look at one ingredient. They consider all available ingredients, the time of day, and who they are cooking for. This allows for very specific and intelligent routing.

This approach is key for **advanced conditional edges multi-path** scenarios where simple checks are not enough. It allows for highly specific responses. These responses are tailored to complex inputs.

```python
# Combining multiple criteria for a routing decision
def route_by_complex_criteria(state: dict):
    query_type = state.get("query_classification")
    user_segment = state.get("customer_segment")
    is_peak_hours = state.get("is_peak_time")

    if query_type == "technical" and user_segment == "enterprise":
        return "enterprise_tech_support"
    elif query_type == "technical" and user_segment == "consumer" and not is_peak_hours:
        return "automated_tech_troubleshooter"
    elif query_type == "technical" and user_segment == "consumer" and is_peak_hours:
        return "consumer_tech_support_queue" # Route to queue during peak
    elif query_type == "billing" and user_segment == "vip":
        return "vip_billing_support"
    else:
        return "general_enquiry_desk"
```

Here, `route_by_complex_criteria` uses `query_type`, `user_segment`, and `is_peak_hours`. This demonstrates powerful **multi-criteria routing**. It ensures the user gets the right help based on a full picture of their situation.

### Practical Examples of Advanced Conditional Edges Multi-Path

Let's get our hands dirty with some real-world examples. These will help you see how **advanced conditional edges multi-path** truly work in LangGraph. We will use various **advanced routing patterns** to build smart agents.

Each example will show a different way to use **complex routing functions**. This will help you implement **routing optimization** in your own projects. You'll see how to create **multi-way branching** logic effectively.

#### Example 1: Priority-Based Paths for Customer Service

Imagine a customer service chatbot. Not all questions are equally important. Some require immediate human attention, while others can be handled by automated systems or FAQs. We want to route based on urgency. This is a classic case for **priority-based paths**.

**Scenario:** A customer asks a question. The system needs to figure out its priority. High priority (e.g., "account locked") goes to a human. Medium priority (e.g., "billing question") goes to a knowledge base. Low priority (e.g., "general feedback") goes to a suggestion box or FAQ.

**LangGraph State:**
Our agent's memory (state) will store the `user_query`, the `priority_level` we detect, and the `response_type` determined by the routing.

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END

# Define your graph state
class AgentState(TypedDict):
    user_query: str
    priority_level: Annotated[str, operator.setitem] # high, medium, low
    response_type: Annotated[str, operator.setitem] # human, knowledge_base, faq, suggestion

# Define nodes (what the agent does at each step)
def analyze_priority_node(state: AgentState):
    """Determines the priority of the user's query."""
    query = state["user_query"].lower()
    if "account locked" in query or "urgent help" in query or "can't access" in query:
        priority = "high"
    elif "billing" in query or "payment" in query or "subscription" in query:
        priority = "medium"
    else:
        priority = "low"
    print(f"--- Node: Analyze Priority ---")
    print(f"Detected priority: {priority} for query: '{state['user_query']}'")
    return {"priority_level": priority}

def human_handoff_node(state: AgentState):
    """Routes to a human agent."""
    print("--- Node: Human Handoff ---")
    print(f"Action: Routing query '{state['user_query']}' to a human agent.")
    return {"response_type": "human"}

def knowledge_base_node(state: AgentState):
    """Searches the knowledge base."""
    print("--- Node: Knowledge Base Search ---")
    print(f"Action: Searching knowledge base for '{state['user_query']}'.")
    return {"response_type": "knowledge_base"}

def faq_node(state: AgentState):
    """Checks the FAQ section."""
    print("--- Node: FAQ Search ---")
    print(f"Action: Checking FAQ for '{state['user_query']}'.")
    return {"response_type": "faq"}

def suggestion_box_node(state: AgentState):
    """Submits feedback to the suggestion box."""
    print("--- Node: Suggestion Box ---")
    print(f"Action: Submitting '{state['user_query']}' to suggestion box.")
    return {"response_type": "suggestion"}

# Define the routing logic (the conditional edge function)
def route_by_priority(state: AgentState):
    """This complex routing function decides the next node based on priority level."""
    priority = state["priority_level"]
    query = state["user_query"].lower()
    print(f"--- Router: Route by Priority ---")
    print(f"Routing based on priority: {priority}")

    if priority == "high":
        print("Path: High Priority -> Human Handoff")
        return "human_handoff"
    elif priority == "medium":
        print("Path: Medium Priority -> Knowledge Base Search")
        return "knowledge_base_search"
    elif priority == "low":
        # Here we demonstrate cascading conditions within the router
        # Further refine low priority into FAQ or suggestion based on keywords
        if "feedback" in query or "suggest" in query or "idea" in query:
            print("Path: Low Priority (Feedback) -> Suggestion Box")
            return "suggestion_box"
        else:
            print("Path: Low Priority (General) -> FAQ Search")
            return "faq_search"

# Build the graph
workflow = StateGraph(AgentState)

# Add all the nodes to our graph
workflow.add_node("analyze_priority", analyze_priority_node)
workflow.add_node("human_handoff", human_handoff_node)
workflow.add_node("knowledge_base_search", knowledge_base_node)
workflow.add_node("faq_search", faq_node)
workflow.add_node("suggestion_box", suggestion_box_node)

# Set the entry point of the graph
workflow.add_edge(START, "analyze_priority")

# Add the advanced conditional edge from 'analyze_priority'
# The 'route_by_priority' function will decide which node to go to next
workflow.add_conditional_edges(
    "analyze_priority", # The node from which the edge originates
    route_by_priority,  # The complex routing function
    {                   # A mapping of possible returns from route_by_priority to actual node names
        "human_handoff": "human_handoff",
        "knowledge_base_search": "knowledge_base_search",
        "faq_search": "faq_search",
        "suggestion_box": "suggestion_box",
    }
)

# All specific response nodes lead to the end of the graph
workflow.add_edge("human_handoff", END)
workflow.add_edge("knowledge_base_search", END)
workflow.add_edge("faq_search", END)
workflow.add_edge("suggestion_box", END)

# Compile the graph to make it ready to run
app = workflow.compile()

# --- Run Examples ---
print("\n--- Running Query 1: Account Locked (High Priority) ---")
app.invoke({"user_query": "My account is locked and I can't access it, urgent help needed!"})
print("\n--- Running Query 2: Billing Question (Medium Priority) ---")
app.invoke({"user_query": "How do I update my payment method for my subscription?"})
print("\n--- Running Query 3: General Feedback (Low Priority - Feedback) ---")
app.invoke({"user_query": "I have an idea to improve your service."})
print("\n--- Running Query 4: Simple Question (Low Priority - General) ---")
app.invoke({"user_query": "What are your business hours on weekends?"})
print("\n--- Running Query 5: Urgent Access Issue (High Priority) ---")
app.invoke({"user_query": "I need immediate assistance, I can't log in!"})
```

**Explanation:**

In this example, the `route_by_priority` function is our **complex routing function**. It first checks the `priority_level` set by the `analyze_priority_node`. This creates **priority-based paths**.

For "high" and "medium" priorities, it directly returns the appropriate next node. For "low" priority, it uses **cascading conditions** within itself. It looks for keywords like "feedback" to decide between `suggestion_box` and `faq_search`. This clearly demonstrates **multi-way branching** based on granular conditions.

#### Example 2: Weighted Routing Logic for Load Balancing

Sometimes, you don't want to just pick one path. You might want to distribute requests across several paths. This is where **weighted routing logic** comes in handy. You can assign "weights" or probabilities to different paths.

**Scenario:** You have three different AI models (or external APIs) that can answer user questions. Model A is the newest and most accurate but also the slowest (so we send 50% of requests there). Model B is faster but less accurate (30% of requests). Model C is a fallback, very fast but basic (20% of requests). We want to distribute queries based on these weights.

**LangGraph State:**
The state will track `user_query`, the `chosen_model`, and the `model_response`.

```python
import operator
import random
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    user_query: str
    chosen_model: Annotated[str, operator.setitem] # model_A, model_B, model_C
    model_response: Annotated[str, operator.setitem]

def choose_model_by_weight_node(state: AgentState):
    """Chooses a model based on predefined weights."""
    weights = {
        "model_A": 0.5, # 50% chance
        "model_B": 0.3, # 30% chance
        "model_C": 0.2, # 20% chance
    }
    
    # Randomly select a model based on weights
    chosen = random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]
    print(f"--- Node: Choose Model by Weight ---")
    print(f"Weighted routing chose: {chosen} for query: '{state['user_query']}'")
    return {"chosen_model": chosen}

def model_A_node(state: AgentState):
    """Simulates processing by Model A."""
    print("--- Node: Model A Processing ---")
    print(f"Model A processing query: '{state['user_query']}' (high accuracy, slow)")
    return {"model_response": f"Response from Model A for '{state['user_query']}'"}

def model_B_node(state: AgentState):
    """Simulates processing by Model B."""
    print("--- Node: Model B Processing ---")
    print(f"Model B processing query: '{state['user_query']}' (medium accuracy, faster)")
    return {"model_response": f"Response from Model B for '{state['user_query']}'"}

def model_C_node(state: AgentState):
    """Simulates processing by Model C."""
    print("--- Node: Model C Processing ---")
    print(f"Model C processing query: '{state['user_query']}' (basic accuracy, fastest)")
    return {"model_response": f"Response from Model C for '{state['user_query']}'"}

# The routing logic will simply read the chosen_model from the state
def route_to_model(state: AgentState):
    """This router sends the query to the chosen model node."""
    chosen_model = state["chosen_model"]
    print(f"--- Router: Route to Model ---")
    print(f"Routing to: {chosen_model}")
    return chosen_model

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("choose_model_by_weight", choose_model_by_weight_node)
workflow.add_node("model_A_process", model_A_node)
workflow.add_node("model_B_process", model_B_node)
workflow.add_node("model_C_process", model_C_node)

workflow.add_edge(START, "choose_model_by_weight")

workflow.add_conditional_edges(
    "choose_model_by_weight",
    route_to_model,
    {
        "model_A": "model_A_process",
        "model_B": "model_B_process",
        "model_C": "model_C_process",
    }
)

workflow.add_edge("model_A_process", END)
workflow.add_edge("model_B_process", END)
workflow.add_edge("model_C_process", END)

app = workflow.compile()

# --- Run Examples multiple times to see the weighted distribution ---
print("\n--- Running Multiple Queries for Weighted Routing ---")
for i in range(10):
    print(f"\n--- Query {i+1} ---")
    app.invoke({"user_query": f"Tell me about LangGraph (query {i+1})."})
```

**Explanation:**

Here, `choose_model_by_weight_node` performs the core logic for **weighted routing logic**. It uses `random.choices` to select a model based on the defined probabilities. The `route_to_model` function then simply reads this choice from the state.

This demonstrates how to implement **advanced conditional edges multi-path** for load balancing or A/B testing scenarios. Each path (Model A, B, or C) has a different likelihood of being chosen. This helps in **routing optimization** by distributing tasks intelligently.

#### Example 3: Parallel Path Evaluation or First-Match Routing

Sometimes, you need to check several conditions. You want to pick the first one that matches, or perhaps run things in a way that *feels* parallel. This is useful for decision trees where multiple rules could apply.

**Scenario:** An agent needs to respond to a user query. It has several specialized tools or functions it can use. It should try to use the most specific tool first. If that doesn't fit, it tries the next best, and so on. If no specific tool is suitable, it defaults to a general LLM response. This is a form of **cascading conditions** that gives the appearance of **parallel path evaluation** for decision-making.

**LangGraph State:**
The state will hold `user_query`, `tool_used`, and `final_response`.

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    user_query: str
    tool_used: Annotated[str, operator.setitem]
    final_response: Annotated[str, operator.setitem]

# Define "tool" nodes
def weather_tool_node(state: AgentState):
    """Simulates calling a weather API."""
    city = "New York" # For simplicity, let's assume detection happens earlier
    print(f"--- Node: Weather Tool ---")
    print(f"Querying weather for '{city}' based on '{state['user_query']}'")
    return {"tool_used": "weather_api", "final_response": f"The weather in {city} is sunny and 75°F."}

def calculator_tool_node(state: AgentState):
    """Simulates calling a calculator tool."""
    print(f"--- Node: Calculator Tool ---")
    print(f"Performing calculation for '{state['user_query']}'")
    return {"tool_used": "calculator", "final_response": f"The answer to your math question is 42."}

def knowledge_base_tool_node(state: AgentState):
    """Simulates searching a specific knowledge base."""
    print(f"--- Node: Knowledge Base Tool ---")
    print(f"Searching internal knowledge base for '{state['user_query']}'")
    return {"tool_used": "knowledge_base", "final_response": f"According to our knowledge base, [info related to '{state['user_query']}']."}

def general_llm_node(state: AgentState):
    """Simulates a general LLM response."""
    print(f"--- Node: General LLM ---")
    print(f"Providing general LLM response for '{state['user_query']}'")
    return {"tool_used": "general_llm", "final_response": f"As an AI, I can tell you that '{state['user_query']}' is an interesting topic."}

# Routing function that acts like a cascading 'if-else if'
def route_to_best_tool(state: AgentState):
    """
    This routing function checks for specific keywords to decide which tool to use.
    It uses cascading conditions (first match wins).
    """
    query = state["user_query"].lower()
    print(f"--- Router: Route to Best Tool ---")
    print(f"Evaluating query: '{state['user_query']}' for best tool match.")

    # Prioritize specific tools
    if "weather" in query or "temperature" in query:
        print("Path: Matches Weather Tool")
        return "weather_tool"
    elif "calculate" in query or "math" in query or "plus" in query or "minus" in query:
        print("Path: Matches Calculator Tool")
        return "calculator_tool"
    elif "who is" in query or "what is" in query: # Example for a knowledge base
        print("Path: Matches Knowledge Base Tool")
        return "knowledge_base_tool"
    else:
        print("Path: No specific tool match -> General LLM")
        return "general_llm_response"

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("route_start", lambda x: x) # A dummy node to start routing
workflow.add_node("weather_tool", weather_tool_node)
workflow.add_node("calculator_tool", calculator_tool_node)
workflow.add_node("knowledge_base_tool", knowledge_base_tool_node)
workflow.add_node("general_llm_response", general_llm_node)

workflow.add_edge(START, "route_start")

workflow.add_conditional_edges(
    "route_start",
    route_to_best_tool,
    {
        "weather_tool": "weather_tool",
        "calculator_tool": "calculator_tool",
        "knowledge_base_tool": "knowledge_base_tool",
        "general_llm_response": "general_llm_response",
    }
)

workflow.add_edge("weather_tool", END)
workflow.add_edge("calculator_tool", END)
workflow.add_edge("knowledge_base_tool", END)
workflow.add_edge("general_llm_response", END)

app = workflow.compile()

# --- Run Examples ---
print("\n--- Running Query 1: Weather Question ---")
app.invoke({"user_query": "What's the temperature outside?"})
print("\n--- Running Query 2: Calculation Question ---")
app.invoke({"user_query": "Calculate 5 plus 7."})
print("\n--- Running Query 3: Knowledge Base Question ---")
app.invoke({"user_query": "What is the capital of France?"})
print("\n--- Running Query 4: General Question ---")
app.invoke({"user_query": "Tell me a joke."})
print("\n--- Running Query 5: Another Weather Question ---")
app.invoke({"user_query": "Is it going to rain tomorrow?"})
```

**Explanation:**

The `route_to_best_tool` function embodies **cascading conditions** for tool selection. It evaluates a series of `if/elif` statements. The first condition that matches the `user_query` dictates the chosen path. This effectively simulates **parallel path evaluation** for finding the most suitable tool. This is a common pattern for **routing optimization** in tool-calling agents. It makes sure the most specialized tool is attempted first.

#### Example 4: Dynamic Tool Selection with Multi-Criteria Routing

Combining multiple pieces of information for routing leads to very smart agents. This is **multi-criteria routing**. Your agent can look at the user's input, the current data available, and even its internal confidence.

**Scenario:** An agent needs to decide which tool to use. It has an "external search" tool and an "internal database" tool. It should use the external search if the query seems general or about recent events. It should use the internal database if the query is specific to known data or past interactions. If the query requires both or is very complex, it might escalate to an advanced LLM reasoning node.

**LangGraph State:**
The state will manage `user_query`, `query_category` (e.g., "general", "specific"), `data_available` (boolean), and `chosen_action`.

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    user_query: str
    query_category: Annotated[str, operator.setitem] # general, specific, complex
    data_available: Annotated[bool, operator.setitem] # True if internal data might exist
    chosen_action: Annotated[str, operator.setitem]

# Helper node to classify query and check data availability
def classify_query_and_data(state: AgentState):
    query = state["user_query"].lower()
    
    category = "general"
    data_exists = False

    if "latest news" in query or "current events" in query:
        category = "general" # External search likely needed
    elif "my account" in query or "order id" in query or "internal policy" in query:
        category = "specific" # Internal data likely exists
        data_exists = True
    elif "analyze" in query or "compare" in query and ("trends" in query or "reports" in query):
        category = "complex" # Might need advanced reasoning
        data_exists = True # Assume some internal reports are available

    print(f"--- Node: Classify Query & Data ---")
    print(f"Query '{state['user_query']}' classified as '{category}'. Internal data available: {data_exists}.")
    return {"query_category": category, "data_available": data_exists}

# Define tool nodes
def external_search_node(state: AgentState):
    print(f"--- Node: External Search ---")
    print(f"Performing external search for: '{state['user_query']}'")
    return {"chosen_action": "external_search", "final_response": f"External search results for '{state['user_query']}'."}

def internal_database_node(state: AgentState):
    print(f"--- Node: Internal Database ---")
    print(f"Querying internal database for: '{state['user_query']}'")
    return {"chosen_action": "internal_database", "final_response": f"Internal database results for '{state['user_query']}'."}

def advanced_reasoning_node(state: AgentState):
    print(f"--- Node: Advanced Reasoning ---")
    print(f"Engaging advanced LLM reasoning for: '{state['user_query']}'")
    return {"chosen_action": "advanced_reasoning", "final_response": f"Advanced analysis of '{state['user_query']}' completed."}

def default_response_node(state: AgentState):
    print(f"--- Node: Default Response ---")
    print(f"Providing a polite default response for: '{state['user_query']}'")
    return {"chosen_action": "default_response", "final_response": f"I'm not sure how to handle '{state['user_query']}' at the moment. Can you rephrase?"}

# Routing function using multiple criteria
def route_by_dynamic_tool_selection(state: AgentState):
    """
    This router uses multi-criteria routing to decide the best action.
    It considers query category and data availability.
    """
    category = state["query_category"]
    data_exists = state["data_available"]
    
    print(f"--- Router: Route by Dynamic Tool Selection ---")
    print(f"Routing based on category: '{category}' and data_available: {data_exists}")

    if category == "complex":
        print("Path: Complex query -> Advanced Reasoning")
        return "advanced_reasoning_tool"
    elif category == "specific" and data_exists:
        print("Path: Specific query with internal data -> Internal Database")
        return "internal_database_tool"
    elif category == "general" and not data_exists: # Or even if data_exists but external is better for general
        print("Path: General query -> External Search")
        return "external_search_tool"
    else:
        print("Path: Fallback -> Default Response")
        return "default_tool"

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("classify_query_and_data", classify_query_and_data)
workflow.add_node("external_search_tool", external_search_node)
workflow.add_node("internal_database_tool", internal_database_node)
workflow.add_node("advanced_reasoning_tool", advanced_reasoning_node)
workflow.add_node("default_tool", default_response_node)

workflow.add_edge(START, "classify_query_and_data")

workflow.add_conditional_edges(
    "classify_query_and_data",
    route_by_dynamic_tool_selection,
    {
        "external_search_tool": "external_search_tool",
        "internal_database_tool": "internal_database_tool",
        "advanced_reasoning_tool": "advanced_reasoning_tool",
        "default_tool": "default_tool",
    }
)

workflow.add_edge("external_search_tool", END)
workflow.add_edge("internal_database_tool", END)
workflow.add_edge("advanced_reasoning_tool", END)
workflow.add_edge("default_tool", END)

app = workflow.compile()

# --- Run Examples ---
print("\n--- Running Query 1: General News ---")
app.invoke({"user_query": "What's the latest news on AI trends?"})
print("\n--- Running Query 2: Specific Account Info ---")
app.invoke({"user_query": "Can you check my order ID 12345?"})
print("\n--- Running Query 3: Complex Analysis ---")
app.invoke({"user_query": "Analyze the sales reports from Q1 vs Q2."})
print("\n--- Running Query 4: Simple Unknown Query ---")
app.invoke({"user_query": "Tell me something random."})
print("\n--- Running Query 5: Specific Policy Question ---")
app.invoke({"user_query": "What is the company's return policy?"})
```

**Explanation:**

The `route_by_dynamic_tool_selection` function uses `query_category` and `data_available` from the state. It makes routing decisions using **multi-criteria routing**. This allows the agent to intelligently pick between an `external_search_tool`, `internal_database_tool`, or `advanced_reasoning_tool`. This flexibility makes it a powerful example of **advanced conditional edges multi-path** logic. It also includes a `default_tool` for anything that doesn't fit the other rules.

#### Example 5: Human-in-the-Loop with Cascading Conditions

For critical applications, sometimes an AI simply can't handle a situation. In these cases, it's vital to involve a human. We can design **cascading conditions** to escalate to a human only when automated paths have been exhausted or when specific high-stakes conditions are met. This is a crucial **advanced routing pattern**.

**Scenario:** An agent tries to resolve a user's technical issue. First, it tries an automated troubleshooter. If that fails (or reports "unresolved"), it then tries a specialized AI knowledge base. If *that* also fails, or if the user explicitly asks for human help, the agent routes to a human support agent.

**LangGraph State:**
The state will include `user_query`, `issue_resolved` (boolean, or a status string), `human_requested` (boolean), and `final_action`.

```python
import operator
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    user_query: str
    issue_resolved: Annotated[str, operator.setitem] # "resolved", "unresolved", "error"
    human_requested: Annotated[bool, operator.setitem]
    final_action: Annotated[str, operator.setitem]

# Helper node to check if human was requested
def check_human_request_node(state: AgentState):
    query = state["user_query"].lower()
    human_req = "human" in query or "agent" in query or "speak to someone" in query or "escalate" in query
    print(f"--- Node: Check Human Request ---")
    print(f"User requested human: {human_req} for query: '{state['user_query']}'")
    return {"human_requested": human_req}

# Automated troubleshooter node
def automated_troubleshooter_node(state: AgentState):
    query = state["user_query"].lower()
    print(f"--- Node: Automated Troubleshooter ---")
    print(f"Attempting automated troubleshooting for: '{state['user_query']}'")
    
    # Simulate resolution based on query content
    if "restart" in query or "power cycle" in query:
        print("Issue resolved by automated step!")
        return {"issue_resolved": "resolved"}
    else:
        print("Automated troubleshooter could not resolve.")
        return {"issue_resolved": "unresolved"}

# Specialized AI knowledge base node
def specialized_kb_node(state: AgentState):
    query = state["user_query"].lower()
    print(f"--- Node: Specialized KB Search ---")
    print(f"Searching specialized knowledge base for: '{state['user_query']}'")
    
    # Simulate finding an answer
    if "driver" in query or "software update" in query:
        print("Specialized KB found a potential solution!")
        return {"issue_resolved": "resolved"}
    else:
        print("Specialized KB could not find a solution.")
        return {"issue_resolved": "unresolved"}

# Human handoff node
def human_support_node(state: AgentState):
    print(f"--- Node: Human Support ---")
    print(f"Escalating '{state['user_query']}' to a human support agent.")
    return {"final_action": "human_support", "issue_resolved": "pending_human"}

# Resolution confirmation/default node
def issue_resolved_node(state: AgentState):
    print(f"--- Node: Issue Resolved ---")
    print(f"User's issue '{state['user_query']}' has been resolved: {state['issue_resolved']}.")
    return {"final_action": "resolved_by_automation"}

# Routing function with cascading conditions for human-in-the-loop
def route_for_support(state: AgentState):
    """
    This router uses cascading conditions to determine the next step,
    prioritizing human intervention when requested or all automated paths fail.
    """
    human_req = state["human_requested"]
    issue_status = state["issue_resolved"]
    
    print(f"--- Router: Route for Support ---")
    print(f"Routing based on human_requested: {human_req}, issue_status: {issue_status}")

    # Highest priority: User explicitly asked for human
    if human_req:
        print("Path: Human requested -> Human Support")
        return "human_support"
    
    # Next: If automated troubleshooter failed, try specialized KB
    if issue_status == "unresolved" and state.get("last_node") == "automated_troubleshooter":
        print("Path: Troubleshooter unresolved -> Specialized KB")
        return "specialized_kb_tool"
    
    # Next: If specialized KB also failed, escalate to human
    if issue_status == "unresolved" and state.get("last_node") == "specialized_kb_tool":
        print("Path: Specialized KB unresolved -> Human Support")
        return "human_support"
    
    # Default path for starting or if resolved
    if issue_status == "resolved":
        print("Path: Issue resolved -> End")
        return "resolved_path"
    else: # Should ideally be the starting point of the automated process
        print("Path: Starting automation -> Automated Troubleshooter")
        return "automated_troubleshooter_tool"

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("check_human_request", check_human_request_node)
workflow.add_node("automated_troubleshooter", automated_troubleshooter_node)
workflow.add_node("specialized_kb_tool", specialized_kb_node)
workflow.add_node("human_support", human_support_node)
workflow.add_node("resolved_path", issue_resolved_node) # Node to mark as resolved and end

workflow.add_edge(START, "check_human_request")

# The first conditional edge: after checking for human request
workflow.add_conditional_edges(
    "check_human_request",
    route_for_support, # This router will decide based on human_requested and issue_status
    {
        "human_support": "human_support",
        "automated_troubleshooter_tool": "automated_troubleshooter",
    }
)

# A second conditional edge after the automated troubleshooter
workflow.add_conditional_edges(
    "automated_troubleshooter",
    route_for_support, # Re-use the same router
    {
        "human_support": "human_support",
        "specialized_kb_tool": "specialized_kb_tool",
        "resolved_path": "resolved_path",
    }
)

# A third conditional edge after the specialized KB
workflow.add_conditional_edges(
    "specialized_kb_tool",
    route_for_support, # Re-use the same router
    {
        "human_support": "human_support",
        "resolved_path": "resolved_path",
    }
)

workflow.add_edge("human_support", END)
workflow.add_edge("resolved_path", END)

app = workflow.compile()

# --- Run Examples ---
print("\n--- Running Query 1: Direct Human Request ---")
app.invoke({"user_query": "I need to speak to an agent immediately."})
print("\n--- Running Query 2: Simple Troubleshoot (Resolved) ---")
app.invoke({"user_query": "My internet isn't working, I already tried restarting."}) # Simulates troubleshooter resolving due to keyword
print("\n--- Running Query 3: Troubleshoot Fails, KB Fails (Escalates) ---")
app.invoke({"user_query": "My printer is making a strange noise."}) # Neither automated nor KB handles this well
print("\n--- Running Query 4: Troubleshoot Fails, KB Resolves ---")
app.invoke({"user_query": "I need to update my printer drivers."}) # Automated fails, KB resolves
```

**Explanation:**

This example uses **cascading conditions** within the `route_for_support` function. This function is called multiple times throughout the graph. It prioritizes a direct human request. If no human is requested, it tries the `automated_troubleshooter`. If that fails (`issue_resolved` is "unresolved"), it tries the `specialized_kb_tool`. If *that* also fails, it finally routes to `human_support`. This is a sophisticated example of **advanced conditional edges multi-path** for reliable **human-in-the-loop** workflows. It's a great demonstration of **routing optimization** for critical paths.

### Tips for Routing Optimization

Building these complex systems is powerful, but you also want them to be efficient and easy to manage. Here are some tips for **routing optimization**:

#### Keep Routing Functions Clear

Your router functions can become very complex. Make sure they are easy to read and understand. Use clear variable names and add comments to explain your logic. This helps you and others understand how your agent makes decisions.

Well-structured router functions are key for **complex routing functions**. This also helps in debugging and maintenance. Think of it as leaving clear instructions.

#### Test Your Routing Thoroughly

Just like any other code, your routing logic needs to be tested. Make sure that all possible inputs lead to the correct paths. Test edge cases and unexpected inputs. This is crucial for **multi-way branching** reliability.

You can create many example `user_query` values and run them through your app. Check the output carefully to ensure the routing decisions are always correct. This helps ensure **routing optimization** is effective.

#### Consider Performance

For very large graphs or agents handling many requests, the speed of your routing function matters. Avoid very heavy computations within your router if possible. Sometimes, pre-processing the state in a separate node can make the router faster.

While LangGraph is efficient, overly complex logic can slow things down. Balancing complexity with performance is part of **advanced routing patterns**. This ensures a smooth user experience.

### Advanced Routing Patterns

Beyond the examples, there are more abstract **advanced routing patterns** you can explore. These are ways to structure your graph to solve common problems.

#### Fan-out/Fan-in

This pattern involves sending the agent to multiple nodes at once (fan-out). Then, it waits for all (or some) of them to finish before continuing (fan-in). Imagine sending a query to three different search engines and then summarizing the results.

This is a powerful form of **parallel path evaluation**. It allows you to gather information from multiple sources concurrently. This can speed up your agent's response time and improve the quality of its answers.

#### Circuit Breaker Pattern

This pattern is about handling failures gracefully. If a particular path or service is failing repeatedly, the circuit breaker temporarily stops sending requests to it. It might reroute to a fallback option instead.

This ensures the overall system remains stable. It's a key part of building robust AI agents. This **advanced routing pattern** improves the resilience of your system.

### Conclusion

You've now explored the fascinating world of **advanced conditional edges multi-path** routing in LangGraph. You understand how to build **complex routing functions** that go beyond simple "if/else" statements. We've seen how to implement **multi-way branching** using **switch-case patterns** and **cascading conditions**.

We also covered how to create **priority-based paths**, **weighted routing logic**, and **multi-criteria routing** for truly intelligent decision-making. Through practical examples, you've seen how these **advanced routing patterns** can solve real-world problems. They enable everything from customer service bots to dynamic tool selection.

Remember, the power of LangGraph lies in its flexibility. By mastering **advanced conditional edges multi-path**, you can design AI agents that are not just smart, but adaptable and robust. Keep experimenting with these techniques to build the next generation of intelligent systems! Happy graphing!