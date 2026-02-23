---
title: "Production-Ready LangGraph Conditional Edges Examples: Best Practices 2026"
description: "Master production conditional edges best practices for LangGraph with real-world examples, building robust AI agents ready for 2026 and beyond."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [production conditional edges best practices]
featured: false
image: '/assets/images/production-langgraph-conditional-edges-best-practices-2026.webp'
---

## Welcome to Production-Ready LangGraph Conditional Edges: Best Practices 2026

Building smart AI applications often means making decisions. Your application needs to choose different paths based on what's happening. This is where LangGraph conditional edges become super powerful.

They help your AI brain decide "what's next" in a very structured way. In 2026, mastering these conditional edges is key for robust AI systems. We will dive into *production conditional edges best practices* to make your apps shine.

### What are LangGraph Conditional Edges?

Imagine your AI application as a journey with many stops. Conditional edges are like traffic lights or road signs on this journey. They tell your AI which path to take next. This decision depends on specific rules you set.

These rules are simple checks, like "if the user asks a question about sales, go to the sales team bot." If the rule is true, the AI goes one way. If it's false, it goes another.

This flexibility is crucial for complex AI systems. It allows your application to handle many different situations gracefully. Without them, your AI would follow just one fixed path, which isn't very smart.

### Why Are Conditional Edges Essential for Production?

In a real-world, "production" environment, your AI system faces many challenges. Users ask all sorts of questions, and data can be messy. Conditional edges help your AI adapt to these real-time situations. They ensure your application stays reliable and helpful.

They are at the heart of dynamic *production routing patterns*. These patterns make sure your application can handle various scenarios efficiently. Following *production conditional edges best practices* leads to stable and powerful AI.

These practices help your application be ready for anything. They let your AI gracefully manage unexpected inputs or outcomes. This means happier users and a more effective AI system.

### Understanding the Basics of Conditional Edges

Let's start with a simple look at how conditional edges work in LangGraph. You define different "nodes" in your graph, which are like steps or actions. Then, you connect these nodes with "edges." Some edges are simple one-way streets.

Conditional edges are special because they offer choices. They wait for a signal from a "conditional function." This function decides which of several possible paths to take next.

You can learn more about the fundamentals in our [Introduction to LangGraph](https://example.com/blog/langgraph-basics/) post. Think of it as a decision-making crossroads for your AI workflow.

```python
from langgraph.graph import StateGraph, END

# 1. Define your graph state (what information passes between steps)
class GraphState:
    question: str = ""
    category: str = ""
    answer: str = ""

# 2. Define your nodes (steps in your process)
def categorize_question(state: GraphState):
    question = state.question
    # Imagine a smart model here that categorizes the question
    if "price" in question.lower() or "cost" in question.lower():
        category = "pricing"
    elif "delivery" in question.lower() or "shipping" in question.lower():
        category = "shipping"
    else:
        category = "general"
    print(f"Categorized as: {category}")
    return {"category": category}

def handle_pricing_query(state: GraphState):
    print("Handling pricing query...")
    return {"answer": "Our pricing details are available on our website."}

def handle_shipping_query(state: GraphState):
    print("Handling shipping query...")
    return {"answer": "Shipping usually takes 3-5 business days."}

def handle_general_query(state: GraphState):
    print("Handling general query...")
    return {"answer": "I'm not sure how to answer that specific question yet."}

# 3. Define the conditional edge logic
def route_question(state: GraphState):
    if state.category == "pricing":
        return "pricing_handler"
    elif state.category == "shipping":
        return "shipping_handler"
    else:
        return "general_handler"

# 4. Build the graph
workflow = StateGraph(GraphState)

workflow.add_node("categorizer", categorize_question)
workflow.add_node("pricing_handler", handle_pricing_query)
workflow.add_node("shipping_handler", handle_shipping_query)
workflow.add_node("general_handler", handle_general_query)

workflow.set_entry_point("categorizer")

# Conditional edge: after 'categorizer', route based on the category
workflow.add_conditional_edges(
    "categorizer", # From this node
    route_question, # Use this function to decide next
    { # Mapping results to nodes
        "pricing_handler": "pricing_handler",
        "shipping_handler": "shipping_handler",
        "general_handler": "general_handler",
    }
)

# End the graph from each handler
workflow.add_edge("pricing_handler", END)
workflow.add_edge("shipping_handler", END)
workflow.add_edge("general_handler", END)

app = workflow.compile()

# Example usage
print("--- Query 1: Pricing ---")
app.invoke({"question": "What is the cost of your premium plan?"})
print("\n--- Query 2: Shipping ---")
app.invoke({"question": "How long for delivery?"})
print("\n--- Query 3: General ---")
app.invoke({"question": "Tell me a joke."})
```
In this example, `route_question` is our conditional function. It looks at the `category` from the `categorizer` node. Then, it decides whether to go to `pricing_handler`, `shipping_handler`, or `general_handler`. This is a core example of *production conditional edges best practices* in action.

### Essential Production Routing Patterns

When building real-world AI applications, you'll use various *production routing patterns*. These patterns are like blueprints for how your AI makes complex decisions. They help manage the flow of information and tasks. Using the right pattern can make your system much more efficient and reliable.

#### Simple Sequential Routing

This is the most basic pattern, where steps happen one after another. A conditional edge might decide if a step is skipped. For example, if a user's request is already complete, the AI might skip directly to finishing the task.

It's straightforward and easy to understand. This pattern is great for tasks with a clear, linear progression.

#### Fan-Out and Fan-In Routing

Sometimes your AI needs to do several things at once. A "fan-out" pattern lets your conditional logic send the workflow to multiple paths in parallel. This can speed things up. For example, simultaneously checking a database and calling an external API.

After these parallel tasks are done, a "fan-in" pattern brings all the results back together. This combined information is then used for the next step. This is a common part of advanced *production conditional edges best practices*.

#### Retry Loops for Resilience

In production, things can sometimes go wrong. An API might fail, or a model might return a bad answer. A retry loop is a pattern where your conditional edge decides to try a step again if it fails. This improves your system's resilience.

You might add a limit to retries, like "try 3 times then give up." This prevents endless loops and helps with *error handling best practices*. It's about building robustness into your AI.

#### Decision Trees for Complex Logic

When your AI needs to make many nested decisions, a decision tree pattern is useful. It's like a flowchart where each decision point is a conditional edge. You can break down a big problem into smaller, manageable choices.

For instance, your AI might first decide if a query is internal or external. Then, if internal, it might decide if it's about HR or IT. This helps manage *edge complexity management* effectively. This approach makes complex logic easier to follow and maintain.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class MultiPathState(TypedDict):
    query: str
    decision_step_1: str | None
    decision_step_2: str | None
    final_output: str | None

def initial_analysis(state: MultiPathState):
    query = state["query"].lower()
    if "admin" in query or "policy" in query:
        decision = "internal_policy"
    elif "product" in query or "feature" in query:
        decision = "product_info"
    else:
        decision = "general_inquiry"
    print(f"Initial analysis decision: {decision}")
    return {"decision_step_1": decision}

def handle_internal_policy(state: MultiPathState):
    query = state["query"].lower()
    if "hr" in query:
        decision = "hr_policy"
    else:
        decision = "it_policy"
    print(f"Handling internal policy decision: {decision}")
    return {"decision_step_2": decision}

def process_hr_policy(state: MultiPathState):
    print(f"Processing HR policy for: {state['query']}")
    return {"final_output": "Access HR policy database."}

def process_it_policy(state: MultiPathState):
    print(f"Processing IT policy for: {state['query']}")
    return {"final_output": "Consult IT policy documents."}

def process_product_info(state: MultiPathState):
    print(f"Processing product information for: {state['query']}")
    return {"final_output": "Search product documentation."}

def process_general_inquiry(state: MultiPathState):
    print(f"Processing general inquiry for: {state['query']}")
    return {"final_output": "Redirect to general support."}

def route_step_1(state: MultiPathState):
    if state["decision_step_1"] == "internal_policy":
        return "internal_policy_handler"
    elif state["decision_step_1"] == "product_info":
        return "product_info_handler"
    else:
        return "general_inquiry_handler"

def route_step_2_internal(state: MultiPathState):
    if state["decision_step_2"] == "hr_policy":
        return "hr_policy_processor"
    else: # Must be "it_policy"
        return "it_policy_processor"

workflow = StateGraph(MultiPathState)

workflow.add_node("initial_analysis", initial_analysis)
workflow.add_node("internal_policy_handler", handle_internal_policy)
workflow.add_node("product_info_handler", process_product_info)
workflow.add_node("general_inquiry_handler", process_general_inquiry)
workflow.add_node("hr_policy_processor", process_hr_policy)
workflow.add_node("it_policy_processor", process_it_policy)

workflow.set_entry_point("initial_analysis")

workflow.add_conditional_edges(
    "initial_analysis",
    route_step_1,
    {
        "internal_policy_handler": "internal_policy_handler",
        "product_info_handler": "product_info_handler",
        "general_inquiry_handler": "general_inquiry_handler",
    }
)

workflow.add_conditional_edges(
    "internal_policy_handler",
    route_step_2_internal,
    {
        "hr_policy_processor": "hr_policy_processor",
        "it_policy_processor": "it_policy_processor",
    }
)

workflow.add_edge("product_info_handler", END)
workflow.add_edge("general_inquiry_handler", END)
workflow.add_edge("hr_policy_processor", END)
workflow.add_edge("it_policy_processor", END)

app = workflow.compile()

print("\n--- Query 1: HR Policy ---")
app.invoke({"query": "What is the company's HR leave policy?"})

print("\n--- Query 2: Product Feature ---")
app.invoke({"query": "How does the new search feature work?"})

print("\n--- Query 3: IT Policy ---")
app.invoke({"query": "I need help with our VPN policy."})

print("\n--- Query 4: General ---")
app.invoke({"query": "Can you recommend a good book?"})
```
This example shows how nested conditional edges create a decision tree. The AI makes an initial choice, then another choice based on the first. This structure is excellent for *scalable conditional logic* as your application grows.

### Designing Scalable Conditional Logic

As your AI application gets bigger, its decision-making logic also becomes more complex. Designing for *scalable conditional logic* means making sure your system can grow without becoming a messy tangle. It's about keeping things clean and easy to manage.

Good design ensures that adding new features or changing existing ones is simple. You don't want to rewrite everything each time you update a rule. This is a core part of *production conditional edges best practices*.

#### Modularity with Functions

Break down complex decisions into smaller, independent functions. Instead of one giant function that handles everything, have several small ones. Each function should do just one specific job. For example, one function checks user permissions, another checks data availability.

This makes your code much easier to read and test. If a rule changes, you only update one small function, not a huge block of code. This is crucial for *maintainable routing code*.

#### Avoiding Monolithic Conditions

A "monolithic" condition is one big function that tries to decide everything. This is hard to understand and even harder to change. Imagine a single function with dozens of `if/elif/else` statements. This is exactly what you want to avoid.

Instead, chain smaller conditional edges together. Or, use a lookup table to map states to decisions. This approach makes your logic clearer and more flexible. It directly contributes to better *edge complexity management*.

#### Externalizing Configuration

For truly *scalable conditional logic*, don't hardcode all your decision rules directly into the code. Instead, store them in a separate configuration file or database. This allows you to change rules without deploying new code.

For example, you could have a JSON file that defines mappings. Or, use environment variables for simple flags. This makes your system adaptable and agile.

```python
from langgraph.graph import StateGraph, END
import json
from typing import TypedDict, Literal

# Load rules from an external configuration file
# For a real app, this would be a file like 'routing_rules.json'
# or fetched from a config service.
CONFIG_RULES = """
{
    "support_priority": {
        "premium": "priority_support_handler",
        "standard": "standard_support_handler",
        "guest": "community_support_handler"
    },
    "default_route": "standard_support_handler"
}
"""

ROUTING_CONFIG = json.loads(CONFIG_RULES)

class SupportState(TypedDict):
    user_type: Literal["premium", "standard", "guest"]
    query: str
    response: str | None

def check_user_type(state: SupportState):
    # In a real app, this would come from user session/authentication
    user_type = state["user_type"]
    print(f"User type detected: {user_type}")
    return {"user_type": user_type}

def handle_priority_support(state: SupportState):
    print("Engaging priority support team...")
    return {"response": "Connecting you to a dedicated premium agent."}

def handle_standard_support(state: SupportState):
    print("Engaging standard support team...")
    return {"response": "Connecting you to a standard support agent."}

def handle_community_support(state: SupportState):
    print("Redirecting to community forums...")
    return {"response": "Please visit our community forums for guest support."}

# Conditional function that uses external configuration
def route_by_user_type(state: SupportState):
    user_type = state["user_type"]
    # Look up the next step in the external config
    next_node = ROUTING_CONFIG["support_priority"].get(user_type, ROUTING_CONFIG["default_route"])
    print(f"Routing user type '{user_type}' to: {next_node}")
    return next_node

workflow = StateGraph(SupportState)

workflow.add_node("user_type_checker", check_user_type)
workflow.add_node("priority_support_handler", handle_priority_support)
workflow.add_node("standard_support_handler", handle_standard_support)
workflow.add_node("community_support_handler", handle_community_support)

workflow.set_entry_point("user_type_checker")

workflow.add_conditional_edges(
    "user_type_checker",
    route_by_user_type,
    {
        "priority_support_handler": "priority_support_handler",
        "standard_support_handler": "standard_support_handler",
        "community_support_handler": "community_support_handler",
    }
)

workflow.add_edge("priority_support_handler", END)
workflow.add_edge("standard_support_handler", END)
workflow.add_edge("community_support_handler", END)

app = workflow.compile()

print("--- User 1: Premium ---")
app.invoke({"user_type": "premium", "query": "My system is down!"})

print("\n--- User 2: Standard ---")
app.invoke({"user_type": "standard", "query": "How do I reset my password?"})

print("\n--- User 3: Guest ---")
app.invoke({"user_type": "guest", "query": "General question."})

# If we wanted to change routing, we would just update ROUTING_CONFIG
# without touching the graph logic.
```
This example shows how using a `ROUTING_CONFIG` dictionary allows for flexible, *scalable conditional logic*. You can change how `route_by_user_type` behaves just by changing the `CONFIG_RULES` string. This is a very powerful *production conditional edges best practices* technique.

### Achieving Peak Performance Optimization

Performance is super important in production AI systems. Slow decisions mean slow responses, which frustrates users. *Performance optimization* for your conditional edges means making sure decisions happen quickly and efficiently. Every millisecond counts.

Your goal is to reduce unnecessary work for your AI. This makes your application faster and more cost-effective. These are key aspects of *production conditional edges best practices*.

#### Early Exit Conditions

Sometimes, you know the answer very early in the process. An "early exit" condition lets your AI stop processing and give an answer right away. For example, if a user simply types "hello," there's no need to run complex analytics.

You can have a conditional edge check for these simple cases first. If met, it routes directly to a "greeting" node and ends the workflow. This saves a lot of processing power and time.

#### Minimizing LLM Calls

Large Language Models (LLMs) are powerful but can be slow and expensive. Your conditional logic should aim to use LLMs only when absolutely necessary. Can a simple keyword check suffice? Can you use a smaller, faster model for initial categorization?

Using cheaper, faster methods for early decisions improves *performance optimization*. Only pass data to a big LLM if your conditional logic determines it's truly needed.

#### Caching and Memoization

If your conditional function repeatedly calculates the same thing for the same input, use caching or memoization. This stores the result of a calculation after the first time it runs. If the function is called again with the same input, it returns the stored result instantly.

This is especially useful for conditions that involve looking up static data or running small, idempotent (same input, same output) computations. It's a smart way to boost *performance optimization*.

```python
from langgraph.graph import StateGraph, END
import functools
import time
from typing import TypedDict

class PerformanceState(TypedDict):
    query: str
    cached_result: str | None
    expensive_check_done: bool
    final_output: str | None

# A function that simulates an expensive check (e.g., a slow database query or a small LLM call)
@functools.lru_cache(maxsize=128) # Caches up to 128 unique calls
def _expensive_sentiment_check(text: str) -> str:
    print(f"Running expensive sentiment check for: '{text}'...")
    time.sleep(1) # Simulate delay
    if "urgent" in text.lower() or "broken" in text.lower():
        return "negative_urgent"
    elif "happy" in text.lower() or "great" in text.lower():
        return "positive"
    return "neutral"

def initial_categorization(state: PerformanceState):
    query = state["query"].lower()
    if query in ["hi", "hello", "hey"]:
        print("Early exit: simple greeting detected.")
        return {"final_output": "Hello there! How can I help you quickly?"}
    
    # Check for cached results if the query needs expensive processing
    sentiment = _expensive_sentiment_check(query)
    return {"cached_result": sentiment, "expensive_check_done": True}

def handle_negative_urgent(state: PerformanceState):
    print("Routing to urgent support for negative query.")
    return {"final_output": "Connecting you to an emergency support agent immediately."}

def handle_positive_feedback(state: PerformanceState):
    print("Routing to feedback capture for positive query.")
    return {"final_output": "Thank you for your positive feedback! We appreciate it."}

def handle_neutral_query(state: PerformanceState):
    print("Routing to general query handler for neutral query.")
    return {"final_output": "Processing your general request."}

def route_after_initial_check(state: PerformanceState):
    # If early exit was triggered, the 'final_output' would already be set
    if state.get("final_output"): # Check if an early exit happened
        return "early_exit" # Route to a dummy node or directly to END if possible, but LangGraph needs a node to transition to.
    
    sentiment = state["cached_result"]
    if sentiment == "negative_urgent":
        return "negative_urgent_handler"
    elif sentiment == "positive":
        return "positive_feedback_handler"
    else:
        return "neutral_query_handler"

workflow = StateGraph(PerformanceState)

workflow.add_node("initial_categorization", initial_categorization)
workflow.add_node("negative_urgent_handler", handle_negative_urgent)
workflow.add_node("positive_feedback_handler", handle_positive_feedback)
workflow.add_node("neutral_query_handler", handle_neutral_query)
# Dummy node for early exit to properly terminate the graph
workflow.add_node("early_exit_node", lambda state: state) 

workflow.set_entry_point("initial_categorization")

workflow.add_conditional_edges(
    "initial_categorization",
    route_after_initial_check,
    {
        "early_exit": "early_exit_node",
        "negative_urgent_handler": "negative_urgent_handler",
        "positive_feedback_handler": "positive_feedback_handler",
        "neutral_query_handler": "neutral_query_handler",
    }
)

workflow.add_edge("negative_urgent_handler", END)
workflow.add_edge("positive_feedback_handler", END)
workflow.add_edge("neutral_query_handler", END)
workflow.add_edge("early_exit_node", END) # Connect the early exit dummy node to END

app = workflow.compile()

print("--- Query 1: Simple Greeting (Early Exit) ---")
app.invoke({"query": "Hi"}) # Should be fast

print("\n--- Query 2: Negative Urgent (Expensive Check 1) ---")
app.invoke({"query": "My system is broken and urgent!"}) # Should take ~1 second

print("\n--- Query 3: Negative Urgent (Cached, Fast) ---")
app.invoke({"query": "My system is broken and urgent!"}) # Should be fast due to cache

print("\n--- Query 4: Positive Feedback ---")
app.invoke({"query": "I am so happy with your service!"}) # Should take ~1 second

print("\n--- Query 5: Neutral Query ---")
app.invoke({"query": "Tell me about the weather."}) # Should take ~1 second
```
This example shows an "early exit" for simple greetings. It also uses `@functools.lru_cache` for `_expensive_sentiment_check`. This demonstrates how *performance optimization* can be achieved with caching and early exits. Re-running the same "broken and urgent" query will be much faster.

### Managing Edge Complexity for Clarity

Complex AI systems can quickly become hard to understand. *Edge complexity management* is about keeping your graph's decision points clear and easy to follow. A messy graph is prone to errors and difficult to update. Good management is a core *production conditional edges best practices* concept.

You want anyone looking at your code to quickly grasp what's happening. Clarity leads to fewer bugs and faster development.

#### Clear Naming Conventions

Give your conditional functions and their return values descriptive names. Instead of `func1` or `route_a`, use names like `decide_user_role` or `route_to_premium_support`. This makes the purpose immediately obvious.

Clear names are like signposts in your code. They guide you and others through the logic.

#### In-Code Documentation and Comments

Even with good names, some complex conditions need more explanation. Use comments within your conditional functions. Explain *why* a decision is made in a certain way, especially for non-obvious logic. Documenting the expected inputs and outputs is also very helpful.

This is a vital part of *documentation strategies*. Good comments act as mini-guides for your code.

#### Helper Functions for Logic

If your conditional logic involves several steps, break them into smaller helper functions. The main conditional function then just calls these helpers. For example, instead of calculating a user's score inside the conditional function, call a `calculate_user_score()` helper.

This keeps your conditional function lean and focused. It also makes the individual logic pieces reusable and testable.

#### Limiting Decisions Per Edge

Don't try to make too many different decisions within a single conditional edge. If a single edge has more than 3-4 possible paths, consider breaking it down. You can often chain multiple simpler conditional edges instead.

This improves *edge complexity management* by preventing any single point from becoming overwhelming. Each edge should have a clear, limited scope.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ComplexRoutingState(TypedDict):
    user_status: str # e.g., "new", "returning", "vip"
    query_intent: str # e.g., "sales", "support", "technical"
    priority_level: int # 1 (high) to 5 (low)
    processed_response: str | None

# Helper function to determine priority based on multiple factors
def _determine_routing_priority(user_status: str, query_intent: str) -> str:
    # This logic could be much more complex, possibly using an LLM or a rule engine
    if user_status == "vip" or query_intent == "technical":
        return "high_priority"
    elif user_status == "returning" and query_intent == "support":
        return "medium_priority"
    return "low_priority"

# Node to process initial request and set intent/status
def identify_request_details(state: ComplexRoutingState):
    # Simulate identifying user status and query intent
    # In a real app, this would involve auth, NLU models, etc.
    user_status = "returning" if "existing" in state["query_intent"] else "new"
    query_intent = "sales" if "buy" in state["query_intent"] else "support" if "help" in state["query_intent"] else "technical" if "bug" in state["query_intent"] else "general"
    
    # Using the helper function to calculate the actual routing priority
    routing_priority_str = _determine_routing_priority(user_status, query_intent)
    
    print(f"Request identified: User='{user_status}', Intent='{query_intent}', Routing_Priority='{routing_priority_str}'")
    return {"user_status": user_status, "query_intent": query_intent, "priority_level": routing_priority_str}

def handle_high_priority_case(state: ComplexRoutingState):
    print("Routing to dedicated high-priority agent.")
    return {"processed_response": "High-priority support dispatched."}

def handle_medium_priority_case(state: ComplexRoutingState):
    print("Routing to standard agent with elevated urgency.")
    return {"processed_response": "Standard support with priority."}

def handle_low_priority_case(state: ComplexRoutingState):
    print("Routing to general queue or knowledge base.")
    return {"processed_response": "General support initiated."}

# Conditional function - kept clean by using helper for actual logic
def route_by_calculated_priority(state: ComplexRoutingState):
    """
    Decides the next step based on the 'priority_level' determined
    in the 'identify_request_details' node.
    This function primarily routes based on a pre-calculated value,
    keeping the conditional logic simple and focused.
    """
    priority = state["priority_level"] # This comes from _determine_routing_priority
    print(f"Conditional edge routing based on priority: {priority}")
    if priority == "high_priority":
        return "high_priority_handler"
    elif priority == "medium_priority":
        return "medium_priority_handler"
    else: # Default or "low_priority"
        return "low_priority_handler"

workflow = StateGraph(ComplexRoutingState)

workflow.add_node("identify_request_details", identify_request_details)
workflow.add_node("high_priority_handler", handle_high_priority_case)
workflow.add_node("medium_priority_handler", handle_medium_priority_case)
workflow.add_node("low_priority_handler", handle_low_priority_case)

workflow.set_entry_point("identify_request_details")

workflow.add_conditional_edges(
    "identify_request_details",
    route_by_calculated_priority,
    {
        "high_priority_handler": "high_priority_handler",
        "medium_priority_handler": "medium_priority_handler",
        "low_priority_handler": "low_priority_handler",
    }
)

workflow.add_edge("high_priority_handler", END)
workflow.add_edge("medium_priority_handler", END)
workflow.add_edge("low_priority_handler", END)

app = workflow.compile()

print("--- Query 1: VIP/Technical ---")
app.invoke({"user_status": "vip", "query_intent": "bug in payment system"})

print("\n--- Query 2: Returning Customer Support ---")
app.invoke({"user_status": "returning", "query_intent": "help with my account"})

print("\n--- Query 3: New Customer General ---")
app.invoke({"user_status": "new", "query_intent": "general query about product"})
```
This example shows how `_determine_routing_priority` is a helper function. It keeps `route_by_calculated_priority` clean and focused. This helps with *edge complexity management* and *maintainable routing code*.

### Writing Maintainable Routing Code

Your AI system will evolve over time. New features will be added, and old ones will change. *Maintainable routing code* is code that is easy to understand, modify, and extend. This is a hallmark of good *production conditional edges best practices*.

It prevents your code from becoming a tangled mess. Good maintenance practices save you time and reduce stress in the long run.

#### Clear Code Structure

Organize your conditional functions logically. Group related functions together. Use clear module or file structures. For example, all routing decisions for a specific domain (like "customer support") could live in one file.

This makes it easy to find what you're looking for. It also prevents accidental changes to unrelated parts of the system.

#### Separation of Concerns

Each part of your code should have one specific responsibility. Your conditional functions should *only* decide where to go next. They should not perform heavy data processing or call external APIs themselves. Those tasks belong in separate nodes or helper functions.

This "separation of concerns" makes your code cleaner. It also makes individual components easier to test.

#### DRY Principle (Don't Repeat Yourself)

If you find yourself writing the same decision logic in multiple places, stop and refactor. Create a reusable helper function or a shared conditional. Repeating code makes your system harder to update.

When you need to change a rule, you want to change it in only one place. This is fundamental for *maintainable routing code*.

#### Meaningful Comments and Docstrings

Beyond simple comments, use Python docstrings for your functions. These explain what the function does, its parameters, and what it returns. This is crucial documentation embedded directly in your code.

For conditional functions, clearly state what each return value means. This helps others understand the different paths your graph can take. It ties into overall *documentation strategies*.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

# Define graph state, making sure it's clear what data is shared
class MaintenanceState(TypedDict):
    user_input: str
    processed_intent: Literal["greet", "query", "exit", "unknown"]
    response: str | None

# --- Helper Functions (Separation of Concerns) ---
def _analyze_user_intent(text: str) -> Literal["greet", "query", "exit", "unknown"]:
    """
    Analyzes the user's input to determine their primary intent.
    This function handles the logic for intent classification, separate from routing.
    """
    if text.lower() in ["hi", "hello", "hey"]:
        return "greet"
    elif text.lower() in ["bye", "exit", "quit"]:
        return "exit"
    elif "question" in text.lower() or "?" in text:
        return "query"
    return "unknown"

# --- Graph Nodes (Each with a single responsibility) ---
def process_input_node(state: MaintenanceState):
    """
    Receives user input and identifies the primary intent.
    Sets the 'processed_intent' in the graph state.
    """
    user_input = state["user_input"]
    intent = _analyze_user_intent(user_input) # Delegate logic to helper
    print(f"Input processed. Intent: {intent}")
    return {"processed_intent": intent}

def greet_user_node(state: MaintenanceState):
    """Generates a greeting response."""
    print("Generating greeting.")
    return {"response": "Hello! How can I assist you today?"}

def handle_query_node(state: MaintenanceState):
    """Handles general user queries."""
    print(f"Handling query: {state['user_input']}")
    return {"response": f"I'm processing your query: '{state['user_input']}'"}

def handle_unknown_node(state: MaintenanceState):
    """Provides a fallback response for unknown intents."""
    print("Handling unknown intent.")
    return {"response": "I didn't quite understand that. Can you please rephrase?"}

# --- Conditional Edge Function (Routing Logic Only) ---
def route_on_intent(state: MaintenanceState) -> str:
    """
    Routes the workflow based on the 'processed_intent' in the graph state.
    Expected return values: "greet_handler", "query_handler", "unknown_handler", "exit_point".
    """
    intent = state["processed_intent"]
    print(f"Routing based on intent: {intent}")
    if intent == "greet":
        return "greet_handler"
    elif intent == "query":
        return "query_handler"
    elif intent == "unknown":
        return "unknown_handler"
    elif intent == "exit":
        return "exit_point" # A special return value to signify termination
    else:
        # Fallback for unexpected intents, though _analyze_user_intent should prevent this
        return "unknown_handler"

# --- Build the Graph ---
workflow = StateGraph(MaintenanceState)

workflow.add_node("input_processor", process_input_node)
workflow.add_node("greet_handler", greet_user_node)
workflow.add_node("query_handler", handle_query_node)
workflow.add_node("unknown_handler", handle_unknown_node)

workflow.set_entry_point("input_processor")

# Add conditional edges with clear mapping
workflow.add_conditional_edges(
    "input_processor",
    route_on_intent,
    {
        "greet_handler": "greet_handler",
        "query_handler": "query_handler",
        "unknown_handler": "unknown_handler",
        "exit_point": END, # Directly route to END for exit intent
    }
)

# Connect remaining handlers to END for simple flow
workflow.add_edge("greet_handler", END)
workflow.add_edge("query_handler", END)
workflow.add_edge("unknown_handler", END)

app = workflow.compile()

print("--- Test 1: Greeting ---")
print(app.invoke({"user_input": "Hello"}))

print("\n--- Test 2: Query ---")
print(app.invoke({"user_input": "I have a question about my order."}))

print("\n--- Test 3: Unknown ---")
print(app.invoke({"user_input": "Gibberish text."}))

print("\n--- Test 4: Exit ---")
print(app.invoke({"user_input": "Bye"}))
```
This example shows clean separation: `_analyze_user_intent` handles classification, and `route_on_intent` only routes. Nodes like `greet_user_node` have specific roles. This structure promotes *maintainable routing code*. It also highlights good *documentation strategies* with docstrings.

### Robust Error Handling Best Practices

In a production system, errors are not "if" but "when." *Error handling best practices* for your conditional edges ensure your AI application doesn't crash when things go wrong. Instead, it should fail gracefully, provide useful feedback, or try an alternative path. This is crucial for reliability.

A robust system anticipates failures and has a plan for them. This protects your users and keeps your AI running smoothly.

#### Try-Except Blocks within Conditionals

If your conditional function performs any operation that might fail (e.g., calling an external service, parsing bad data), wrap it in a `try-except` block. This catches errors before they break your entire graph. Inside the `except` block, you can return a default path or log the error.

This prevents a single hiccup from bringing down your whole system. It's a fundamental part of *error handling best practices*.

#### Graceful Degradation and Fallback Paths

When an error occurs, your system shouldn't just stop. It should "degrade gracefully." This means providing a simpler or less perfect service instead of no service at all. Your conditional edges can route to a "fallback" node if an error is detected.

For example, if a specific AI model fails, route to a simpler, more generic model or a human agent. This maintains a basic level of service.

#### Retries with Exponential Backoff

For transient errors (like network glitches), retrying the operation can often succeed. However, don't just retry immediately. Use "exponential backoff," waiting longer after each failed attempt. This prevents overwhelming the failing service.

Your conditional edge could route back to the failing node, with logic to increment a retry counter. After too many retries, it could then route to a fallback. This is a common *production routing patterns* for resilience.

#### Specific Error States

Introduce specific error states or flags in your graph's state. If a node encounters an error, it sets this flag. Then, your conditional edges can check this flag to route to an error handling flow.

This provides clear signals for decision-making. It makes your *error handling best practices* explicit within your graph logic.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict
import random
import time

# Define state with an error flag and retry count
class ErrorHandlingState(TypedDict):
    task_input: str
    is_error: bool
    retry_count: int
    processed_output: str | None
    error_message: str | None

MAX_RETRIES = 2

# Node that might fail
def unreliable_task_node(state: ErrorHandlingState):
    """
    Simulates a task that randomly fails or succeeds.
    If it fails, it sets is_error to True.
    """
    print(f"Attempting unreliable task for: {state['task_input']} (Retry #{state['retry_count'] + 1})")
    
    # Simulate a network error or processing failure
    if random.random() < 0.6 and state["retry_count"] < MAX_RETRIES: # Fail 60% of the time initially
        print("Unreliable task FAILED!")
        return {"is_error": True, "error_message": "Transient error during processing.", "retry_count": state["retry_count"] + 1}
    else:
        print("Unreliable task SUCCEEDED!")
        return {"is_error": False, "processed_output": f"Successfully processed: {state['task_input']}"}

def notify_failure_node(state: ErrorHandlingState):
    """Notifies about persistent failure."""
    print(f"Task permanently failed after {state['retry_count']} retries.")
    return {"processed_output": f"Failed to process '{state['task_input']}' due to persistent error: {state['error_message']}. Please try again later."}

def complete_successfully_node(state: ErrorHandlingState):
    """Confirms successful completion."""
    print("Task completed successfully!")
    return state # Pass through existing state

# Conditional function for routing based on error status and retry count
def route_on_task_status(state: ErrorHandlingState) -> str:
    """
    Routes based on whether the unreliable task succeeded or failed.
    Implements retry logic with a max retry count.
    """
    if not state["is_error"]:
        print("Routing to success handler.")
        return "success"
    else:
        if state["retry_count"] < MAX_RETRIES:
            print(f"Routing to retry: Attempt {state['retry_count'] + 1} of {MAX_RETRIES}.")
            time.sleep(1 * (2 ** (state["retry_count"] - 1))) # Exponential backoff
            return "retry"
        else:
            print("Routing to permanent failure handler.")
            return "failure"

# Build the Graph
workflow = StateGraph(ErrorHandlingState)

workflow.add_node("unreliable_task", unreliable_task_node)
workflow.add_node("notify_failure", notify_failure_node)
workflow.add_node("complete_success", complete_successfully_node)

workflow.set_entry_point("unreliable_task") # Start here

# Conditional edge from the unreliable task
workflow.add_conditional_edges(
    "unreliable_task",
    route_on_task_status,
    {
        "success": "complete_success",
        "retry": "unreliable_task", # Loop back to the same node for retry
        "failure": "notify_failure",
    }
)

# Connect final nodes to END
workflow.add_edge("complete_success", END)
workflow.add_edge("notify_failure", END)

app = workflow.compile()

# Example usage
print("--- Test 1: Task that might fail and retry ---")
# Reset retry count for each invocation
app.invoke({"task_input": "important data", "is_error": False, "retry_count": 0}) 

print("\n--- Test 2: Another attempt ---")
app.invoke({"task_input": "critical report", "is_error": False, "retry_count": 0})
```
This example shows `unreliable_task_node` setting `is_error` and `retry_count`. The `route_on_task_status` function then uses this to decide whether to retry or go to a failure handler. This is a practical example of *error handling best practices* including retries with backoff.

### Thorough Testing Conditional Edges

Your AI application's decisions are critical. If the conditional logic is wrong, the entire system can go off track. *Testing conditional edges* thoroughly ensures your AI makes the right choices every time. It catches bugs before they reach your users. This is a fundamental *production conditional edges best practices*.

Good testing saves you from headaches in production. It builds confidence in your AI's reliability.

#### Unit Tests for Conditions

Each conditional function should have its own "unit test." A unit test checks a single piece of code in isolation. You provide different inputs to your conditional function and check if it returns the correct next step. For example, test `route_question(state_with_pricing_category)` to ensure it returns `"pricing_handler"`.

This makes sure each decision rule works exactly as expected. It's the first line of defense in *testing conditional edges*.

#### Integration Tests for Graph Paths

While unit tests check individual functions, integration tests check how different parts of your graph work together. You run a full input through your LangGraph application and assert that it follows the correct sequence of nodes. This confirms the entire flow behaves as intended.

Integration tests help catch errors where one node's output might unexpectedly affect a conditional edge's decision. This is vital for complex *production routing patterns*.

#### Edge Cases and Negative Testing

Don't just test the "happy path" (what's supposed to happen). Also, test "edge cases" and "negative scenarios." What happens if the input is unexpected? What if a category is missing? What if an external service returns an error?

These tests expose weaknesses in your conditional logic and help implement *error handling best practices*. They ensure your system is robust even under unusual circumstances.

#### Mocking External Services

If your conditional logic depends on external services (like a database or another API), "mock" them during testing. Mocking means creating a fake version of the service that returns predictable results. This makes your tests faster and more reliable, as they don't depend on actual external systems being available.

This allows you to simulate specific scenarios, like an API failing or returning a specific data set. It is key for thorough *testing conditional edges*.

```python
import pytest
from langgraph.graph import StateGraph, END
from typing import TypedDict
import time

# --- Mock LangGraph Setup for Testing ---
class TestState(TypedDict):
    data_type: str
    result: str | None
    error_flag: bool | None

def mock_data_classifier(state: TestState):
    """Mocks a node that classifies data."""
    print(f"Mocking classification for: {state['data_type']}")
    if state["data_type"] == "invalid":
        return {"error_flag": True}
    return {"data_type": state["data_type"], "error_flag": False}

def mock_handler_a(state: TestState):
    """Mocks handler A."""
    print("Mocking Handler A.")
    return {"result": "Handled by A"}

def mock_handler_b(state: TestState):
    """Mocks Handler B."""
    print("Mocking Handler B.")
    return {"result": "Handled by B"}

def mock_error_handler(state: TestState):
    """Mocks an error handler."""
    print("Mocking Error Handler.")
    return {"result": "Handled by Error"}

def test_router_function(state: TestState) -> str:
    """
    Conditional function to be tested.
    Routes based on 'data_type' and 'error_flag'.
    """
    if state.get("error_flag"):
        return "error_route"
    elif state["data_type"] == "type_a":
        return "route_a"
    elif state["data_type"] == "type_b":
        return "route_b"
    else:
        return "error_route" # Fallback for unknown valid types

# --- LangGraph App for Integration Tests ---
def create_test_app():
    workflow = StateGraph(TestState)
    workflow.add_node("classifier", mock_data_classifier)
    workflow.add_node("handler_a", mock_handler_a)
    workflow.add_node("handler_b", mock_handler_b)
    workflow.add_node("error_handler", mock_error_handler)

    workflow.set_entry_point("classifier")
    workflow.add_conditional_edges(
        "classifier",
        test_router_function, # Our conditional function under test
        {
            "route_a": "handler_a",
            "route_b": "handler_b",
            "error_route": "error_handler",
        }
    )
    workflow.add_edge("handler_a", END)
    workflow.add_edge("handler_b", END)
    workflow.add_edge("error_handler", END)
    return workflow.compile()

# --- Unit Tests for the Conditional Function ---
def test_router_function_type_a():
    """Tests if 'type_a' correctly routes to 'route_a'."""
    state_input = {"data_type": "type_a", "result": None, "error_flag": False}
    assert test_router_function(state_input) == "route_a"

def test_router_function_type_b():
    """Tests if 'type_b' correctly routes to 'route_b'."""
    state_input = {"data_type": "type_b", "result": None, "error_flag": False}
    assert test_router_function(state_input) == "route_b"

def test_router_function_invalid_type():
    """Tests if an unknown data_type routes to 'error_route'."""
    state_input = {"data_type": "unknown_type", "result": None, "error_flag": False}
    assert test_router_function(state_input) == "error_route"

def test_router_function_error_flag_true():
    """Tests if error_flag=True always routes to 'error_route'."""
    state_input = {"data_type": "type_a", "result": None, "error_flag": True}
    assert test_router_function(state_input) == "error_route"

# --- Integration Tests for the Full Graph Paths ---
@pytest.fixture(scope="module")
def app_for_integration_test():
    return create_test_app()

def test_integration_path_type_a(app_for_integration_test):
    """Tests the full graph path for 'type_a' input."""
    initial_state = {"data_type": "type_a", "result": None, "error_flag": False}
    final_state = app_for_integration_test.invoke(initial_state)
    assert final_state["result"] == "Handled by A"

def test_integration_path_type_b(app_for_integration_test):
    """Tests the full graph path for 'type_b' input."""
    initial_state = {"data_type": "type_b", "result": None, "error_flag": False}
    final_state = app_for_integration_test.invoke(initial_state)
    assert final_state["result"] == "Handled by B"

def test_integration_path_invalid_data(app_for_integration_test):
    """Tests the full graph path for 'invalid' input."""
    initial_state = {"data_type": "invalid", "result": None, "error_flag": None}
    final_state = app_for_integration_test.invoke(initial_state)
    assert final_state["result"] == "Handled by Error"

# To run these tests:
# 1. Save the code as a Python file (e.g., `test_langgraph_routing.py`).
# 2. Make sure you have pytest installed (`pip install pytest`).
# 3. Run `pytest` from your terminal in the same directory.
```
This example shows how to write unit tests for the `test_router_function` itself. It also provides integration tests for the full LangGraph app using `pytest`. This structured approach is fundamental for *testing conditional edges* effectively.

### Monitoring Routing Decisions in Production

Once your AI application is live, you need to know how it's behaving. *Monitoring routing decisions* helps you understand if your conditional logic is working as intended. Are decisions being made correctly? Are errors happening? This feedback is essential for continuous improvement. It is a key aspect of *production conditional edges best practices*.

Good monitoring helps you quickly spot and fix issues. It ensures your AI remains reliable and performant.

#### Comprehensive Logging

Log every significant decision made by your conditional edges. Include details like the input state, the chosen path, and any relevant outcomes. Use structured logging (e.g., JSON logs) to make it easy to parse and analyze later.

These logs are invaluable for debugging. They help you trace the exact path an interaction took through your graph.

#### Tracing Tools

For complex graphs, tracing tools like OpenTelemetry can visualize the entire execution path. They show you which nodes were visited, how long each step took, and which conditional edges were triggered. This provides a clear, visual map of your AI's decision-making process.

Traces are particularly useful for understanding performance bottlenecks and unexpected routing. They offer deep insights into *production routing patterns*.

#### Metrics and Dashboards

Collect metrics on your conditional edges. How often is each path taken? What is the error rate for specific decision points? How long do conditional functions take to execute? Display these metrics on a dashboard.

This gives you a high-level overview of your system's health. Alerts can be set up if certain metrics cross a threshold, helping you react quickly. This is essential for overall *performance optimization*.

#### A/B Testing Routing Strategies

Sometimes you have multiple ideas for how a conditional edge should behave. Use A/B testing to compare different routing strategies in production. Send a small percentage of traffic through a new decision logic and compare its performance against the old one.

This scientific approach helps you optimize your *production conditional edges best practices* based on real-world data.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict
import logging
import json
import time

# Configure logging to output JSON (or similar structured format)
logging.basicConfig(level=logging.INFO, format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
logger = logging.getLogger(__name__)

class MonitoringState(TypedDict):
    query: str
    intent: str | None
    sentiment: str | None
    route_chosen: str | None
    response: str | None
    decision_timestamp: float | None

def classify_query_node(state: MonitoringState):
    """Simulates query classification."""
    intent = "sales" if "buy" in state["query"].lower() else "support" if "help" in state["query"].lower() else "general"
    sentiment = "positive" if "great" in state["query"].lower() else "negative" if "bad" in state["query"].lower() else "neutral"
    
    # Log the output of this node
    logger.info(json.dumps({"event": "node_output", "node": "classify_query_node", "query": state["query"], "intent": intent, "sentiment": sentiment}))
    return {"intent": intent, "sentiment": sentiment}

def handle_sales(state: MonitoringState):
    """Handles sales-related queries."""
    print("Handling sales query.")
    return {"response": "Sales team is ready to assist you!"}

def handle_support(state: MonitoringState):
    """Handles support-related queries."""
    print("Handling support query.")
    return {"response": "Our support agents will help you shortly."}

def handle_general(state: MonitoringState):
    """Handles general queries."""
    print("Handling general query.")
    return {"response": "Here's some general information."}

def route_by_intent_and_sentiment(state: MonitoringState) -> str:
    """
    Conditional function that makes routing decisions and logs them.
    """
    intent = state["intent"]
    sentiment = state["sentiment"]
    route = "general_handler" # Default route
    
    if intent == "sales":
        route = "sales_handler"
    elif intent == "support":
        if sentiment == "negative":
            route = "priority_support_handler" # Imagine a dedicated node for urgent support
        else:
            route = "support_handler"
    
    # Log the decision of the conditional edge
    logger.info(json.dumps({
        "event": "conditional_edge_decision",
        "from_node": "classify_query_node",
        "decision_function": "route_by_intent_and_sentiment",
        "input_intent": intent,
        "input_sentiment": sentiment,
        "chosen_route": route,
        "decision_time_ms": time.time() # This can be used for metrics
    }))
    
    return route

# Build the Graph
workflow = StateGraph(MonitoringState)

workflow.add_node("classify_query_node", classify_query_node)
workflow.add_node("sales_handler", handle_sales)
workflow.add_node("support_handler", handle_support)
workflow.add_node("general_handler", handle_general)
# For demonstration, let's just route priority support to standard support
workflow.add_node("priority_support_handler", handle_support) 

workflow.set_entry_point("classify_query_node")

workflow.add_conditional_edges(
    "classify_query_node",
    route_by_intent_and_sentiment,
    {
        "sales_handler": "sales_handler",
        "support_handler": "support_handler",
        "priority_support_handler": "priority_support_handler",
        "general_handler": "general_handler",
    }
)

workflow.add_edge("sales_handler", END)
workflow.add_edge("support_handler", END)
workflow.add_edge("priority_support_handler", END)
workflow.add_edge("general_handler", END)

app = workflow.compile()

# Example usage
print("--- Sales Query ---")
app.invoke({"query": "I want to buy your product."})

print("\n--- Negative Support Query ---")
app.invoke({"query": "My product is bad, I need urgent help!"})

print("\n--- Positive Support Query ---")
app.invoke({"query": "I love my product, but I have a question."})

print("\n--- General Query ---")
app.invoke({"query": "Tell me a fun fact."})
```
This example uses Python's `logging` module to demonstrate *monitoring routing decisions*. It logs the input and chosen path for each conditional decision in JSON format. This structured logging is key for easily analyzing how your *production routing patterns* are performing.

### Effective Documentation Strategies

Even the smartest AI system is useless if no one understands how it works. *Documentation strategies* are about clearly explaining your LangGraph conditional edges. This includes why decisions are made and how the system flows. Good documentation is a critical part of *production conditional edges best practices*.

It ensures that new team members can quickly get up to speed. It also helps prevent errors when making updates.

#### In-Code Comments and Docstrings

As mentioned before, comments and docstrings are your first line of defense. Use them generously within your conditional functions. Explain the purpose, inputs, outputs, and any non-obvious logic.

Think of them as small notes to your future self or another developer. They are vital for *maintainable routing code*.

#### READMEs and Architectural Diagrams

For your entire LangGraph application, create a `README.md` file. This should give a high-level overview of the system. Include a section explaining the main conditional edges and their purpose.

For complex graphs, an architectural diagram (like a flowchart) is incredibly helpful. Tools like Mermaid.js or Graphviz can generate these directly from graph definitions. This visual aid makes *edge complexity management* much easier to grasp.

#### Confluence/Wiki Documentation

Beyond code, maintain a wiki or knowledge base (like Confluence). Document the business rules that drive your conditional logic. Explain the "why" behind certain routing decisions. This provides context that code alone cannot always convey.

Link directly to your code and diagrams from these documents. This ensures consistency and thoroughness.

#### Version Control for Documentation

Treat your documentation like code. Store it in version control (like Git). This ensures that changes are tracked, reviewed, and properly deployed alongside your code. Outdated documentation is worse than no documentation.

This practice is essential for keeping your *documentation strategies* effective over time.

```python
# example_conditional_logic.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

"""
# LangGraph Customer Support Router Documentation

## Overview
This LangGraph application routes customer support queries to appropriate handlers based on intent,
priority, and a sentiment analysis. It demonstrates dynamic conditional routing for a production system.

## Graph Structure
- **entry_point**: `classify_and_prioritize_node`
- **Nodes**:
    - `classify_and_prioritize_node`: Analyzes user query for intent and sentiment, and assigns a priority.
    - `premium_support_handler`: Handles high-priority/premium customer issues.
    - `standard_support_handler`: Manages general customer support queries.
    - `feedback_collector`: Collects positive feedback without engaging a human agent.
    - `escalation_handler`: Routes critical issues for human agent review.
    - `knowledge_base_search`: For general informational queries.

## Conditional Edges
The primary routing logic is handled by `route_by_query_attributes` originating from `classify_and_prioritize_node`.
It uses the following logic:
1. **Critical/Negative Sentiment**: If the sentiment is 'negative' and the priority is 'high', routes to `escalation_handler`.
2. **Sales Intent**: If the intent is 'sales', routes to `premium_support_handler` (for lead handling).
3. **Positive Feedback**: If sentiment is 'positive' AND intent is 'general', routes to `feedback_collector`.
4. **General Support**: If intent is 'support' or 'general' (and not critical/negative), routes to `standard_support_handler`.
5. **Default Fallback**: Anything else, routes to `knowledge_base_search`.

## How to use
Run `app.invoke({"query": "Your customer query here"})` with various inputs
to observe the routing behavior. Refer to the `Monitoring Routing Decisions` blog post
for tips on observing the flow in production.

## Maintainability Notes
- All routing decisions are encapsulated in `route_by_query_attributes`.
- Helper functions are used within `classify_and_prioritize_node` for clarity.
- Logging is integrated for production monitoring.
"""

class CustomerState(TypedDict):
    query: str
    intent: Literal["sales", "support", "feedback", "general"] | None
    sentiment: Literal["positive", "negative", "neutral"] | None
    priority: Literal["high", "medium", "low"] | None
    response: str | None

# Helper functions for classification (would be LLM calls in reality)
def _get_intent(text: str) -> Literal["sales", "support", "feedback", "general"]:
    if "buy" in text.lower() or "price" in text.lower(): return "sales"
    if "help" in text.lower() or "problem" in text.lower(): return "support"
    if "great" in text.lower() or "love" in text.lower(): return "feedback"
    return "general"

def _get_sentiment(text: str) -> Literal["positive", "negative", "neutral"]:
    if "bad" in text.lower() or "broken" in text.lower(): return "negative"
    if "great" in text.lower() or "happy" in text.lower(): return "positive"
    return "neutral"

def _get_priority(intent: str, sentiment: str) -> Literal["high", "medium", "low"]:
    if intent == "support" and sentiment == "negative": return "high"
    if intent == "sales": return "high"
    return "medium"

def classify_and_prioritize_node(state: CustomerState):
    """
    Node responsible for classifying the user query, determining sentiment,
    and assigning a priority level for routing.
    """
    query = state["query"]
    intent = _get_intent(query)
    sentiment = _get_sentiment(query)
    priority = _get_priority(intent, sentiment)
    print(f"Classified: Intent={intent}, Sentiment={sentiment}, Priority={priority}")
    return {"intent": intent, "sentiment": sentiment, "priority": priority}

def premium_support_handler(state: CustomerState):
    """Handles high-value sales leads or premium customer support."""
    print("Routing to Premium Support.")
    return {"response": "Connecting you with a premium agent."}

def standard_support_handler(state: CustomerState):
    """Handles general support queries."""
    print("Routing to Standard Support.")
    return {"response": "Connecting you with a standard support agent."}

def feedback_collector(state: CustomerState):
    """Collects positive feedback without engaging an agent."""
    print("Collecting feedback.")
    return {"response": "Thank you for your feedback! We appreciate it."}

def escalation_handler(state: CustomerState):
    """Handles critical or highly negative issues requiring immediate attention."""
    print("Escalating to critical incident team.")
    return {"response": "Your issue has been escalated to our critical incident team."}

def knowledge_base_search(state: CustomerState):
    """Provides self-service via knowledge base for general queries."""
    print("Searching Knowledge Base.")
    return {"response": "Searching our knowledge base for '{state['query']}'."}

def route_by_query_attributes(state: CustomerState) -> str:
    """
    Conditional function that determines the next graph node based on
    the classified intent, sentiment, and priority from the previous node.

    Returns:
        str: The name of the next node to transition to.
        - "escalation_handler" for critical issues.
        - "premium_support_handler" for sales leads.
        - "feedback_collector" for positive feedback.
        - "standard_support_handler" for general support.
        - "knowledge_base_search" as a fallback.
    """
    intent = state["intent"]
    sentiment = state["sentiment"]
    priority = state["priority"]
    
    # Priority 1: Critical issues (negative sentiment, high priority)
    if sentiment == "negative" and priority == "high":
        print(f"Decision: Negative sentiment, high priority -> Escalation")
        return "escalation_handler"
    # Priority 2: Sales intent (high priority)
    elif intent == "sales":
        print(f"Decision: Sales intent -> Premium Support")
        return "premium_support_handler"
    # Priority 3: Positive feedback (general intent)
    elif sentiment == "positive" and intent == "general":
        print(f"Decision: Positive feedback -> Feedback Collector")
        return "feedback_collector"
    # Priority 4: Standard support or general inquiry
    elif intent == "support" or intent == "general":
        print(f"Decision: Standard Support/General Query -> Standard Support")
        return "standard_support_handler"
    # Default Fallback
    else:
        print(f"Decision: Default Fallback -> Knowledge Base Search")
        return "knowledge_base_search"

# Build the LangGraph workflow
workflow = StateGraph(CustomerState)

workflow.add_node("classify_and_prioritize_node", classify_and_prioritize_node)
workflow.add_node("premium_support_handler", premium_support_handler)
workflow.add_node("standard_support_handler", standard_support_handler)
workflow.add_node("feedback_collector", feedback_collector)
workflow.add_node("escalation_handler", escalation_handler)
workflow.add_node("knowledge_base_search", knowledge_base_search)

workflow.set_entry_point("classify_and_prioritize_node")

workflow.add_conditional_edges(
    "classify_and_prioritize_node",
    route_by_query_attributes,
    {
        "premium_support_handler": "premium_support_handler",
        "standard_support_handler": "standard_support_handler",
        "feedback_collector": "feedback_collector",
        "escalation_handler": "escalation_handler",
        "knowledge_base_search": "knowledge_base_search",
    }
)

workflow.add_edge("premium_support_handler", END)
workflow.add_edge("standard_support_handler", END)
workflow.add_edge("feedback_collector", END)
workflow.add_edge("escalation_handler", END)
workflow.add_edge("knowledge_base_search", END)

app = workflow.compile()

# Example Invocations
print("--- Test 1: Critical Negative Support ---")
app.invoke({"query": "My product is broken and it's a critical bug. I need help now!"})

print("\n--- Test 2: Sales Inquiry ---")
app.invoke({"query": "How much does your enterprise plan cost? I want to buy."})

print("\n--- Test 3: Positive Feedback ---")
app.invoke({"query": "Your service is great, I love it!"})

print("\n--- Test 4: General Support Question ---")
app.invoke({"query": "I have a question about my account."})

print("\n--- Test 5: Uncategorized General Query ---")
app.invoke({"query": "Tell me about the weather."})
```
This example uses a large Python docstring at the top. It explains the entire graph, its nodes, and the conditional edge logic. This is an excellent example of *documentation strategies* that promote *maintainable routing code* and clarify *edge complexity management*.

### Refactoring Complex Conditions

As your AI application evolves, some conditional logic might become overly complicated. *Refactoring complex conditions* means reorganizing and simplifying them without changing their behavior. This makes your code cleaner, easier to understand, and more robust. It is a continuous part of *production conditional edges best practices*.

Refactoring is not just about fixing bugs; it's about improving the quality of your code. It's an ongoing process to keep your system healthy.

#### When to Refactor

Refactor when a conditional function becomes too long, has too many nested `if/elif/else` statements, or is difficult to read. If you struggle to explain what a conditional edge does, it's a sign to refactor. Also, if you find yourself copying and pasting logic, it's time to consolidate.

Look for areas where new features are hard to add without breaking existing ones. This indicates complexity has gotten out of hand.

#### Strategies for Refactoring

1.  **Extract Helper Functions**: Break down large conditional logic into smaller, focused helper functions. Each helper should perform a single logical check (e.g., `is_vip_user()`, `is_urgent_query()`). Your main conditional function then calls these helpers. This helps manage *edge complexity management*.
2.  **Use Lookup Tables/Dictionaries**: Instead of a long `if/elif` chain, map conditions to outcomes using a dictionary. For example, `routing_map = {"sales": "sales_node", "support": "support_node"}`. This is cleaner and more *scalable conditional logic*.
3.  **Introduce a Rule Engine**: For very complex, dynamic rules, consider an external rule engine. This separates your decision logic entirely from your code. Rules can then be managed and updated by non-developers. This is an advanced *production routing patterns* technique.
4.  **Chain Conditional Edges**: Instead of one conditional edge making all decisions, use several smaller conditional edges in sequence. Each edge makes one binary or limited choice. This breaks down complexity into manageable steps.

#### Incremental Refactoring

Don't try to refactor everything at once. Make small, controlled changes. Refactor one conditional edge or one helper function at a time. Run tests after each change to ensure nothing broke.

This incremental approach reduces risk. It helps maintain stability while improving your *maintainable routing code*. You can find more tips on this in our [Advanced Code Refactoring](https://example.com/blog/advanced-code-refactoring/) guide.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class RefactorState(TypedDict):
    query: str
    user_segment: str # e.g., "guest", "standard", "premium"
    detected_intent: str # e.g., "product", "billing", "general"
    response: str | None

# --- ORIGINAL, COMPLEX CONDITIONAL FUNCTION (Illustrative, NOT part of the graph) ---
def _original_complex_router(state: RefactorState) -> str:
    """
    This is an example of a complex conditional function that needs refactoring.
    It combines too many checks and is hard to read.
    """
    user = state["user_segment"]
    intent = state["detected_intent"]
    query = state["query"].lower()

    if user == "premium":
        if intent == "billing" and "urgent" in query:
            return "premium_billing_escalation"
        elif intent == "product":
            return "premium_product_support"
        else:
            return "premium_general_support"
    elif user == "standard":
        if intent == "billing":
            if "dispute" in query:
                return "standard_billing_dispute"
            else:
                return "standard_billing_general"
        elif intent == "product":
            if "technical" in query:
                return "standard_product_technical"
            else:
                return "standard_product_general"
        else:
            return "standard_general_support"
    else: # guest
        if intent == "product" and "demo" in query:
            return "guest_product_demo"
        else:
            return "guest_general_inquiry"

# --- REFACTORED APPROACH ---

# 1. Helper functions to encapsulate specific checks
def is_premium_user(state: RefactorState) -> bool:
    return state["user_segment"] == "premium"

def is_billing_intent(state: RefactorState) -> bool:
    return state["detected_intent"] == "billing"

def is_product_intent(state: RefactorState) -> bool:
    return state["detected_intent"] == "product"

def is_urgent_query(state: RefactorState) -> bool:
    return "urgent" in state["query"].lower()

def is_dispute_query(state: RefactorState) -> bool:
    return "dispute" in state["query"].lower()

def is_technical_query(state: RefactorState) -> bool:
    return "technical" in state["query"].lower()

def is_demo_query(state: RefactorState) -> bool:
    return "demo" in state["query"].lower()

# 2. Refactored conditional function using helpers and a more structured flow
def refactored_router(state: RefactorState) -> str:
    """
    Refactored conditional router using helper functions for clarity.
    This manages routing based on user segment, intent, and query details.
    """
    if is_premium_user(state):
        if is_billing_intent(state) and is_urgent_query(state):
            return "premium_billing_escalation"
        elif is_product_intent(state):
            return "premium_product_support"
        else:
            return "premium_general_support"
    
    elif state["user_segment"] == "standard":
        if is_billing_intent(state):
            if is_dispute_query(state):
                return "standard_billing_dispute"
            else:
                return "standard_billing_general"
        elif is_product_intent(state):
            if is_technical_query(state):
                return "standard_product_technical"
            else:
                return "standard_product_general"
        else:
            return "standard_general_support"
            
    else: # Guest user
        if is_product_intent(state) and is_demo_query(state):
            return "guest_product_demo"
        else:
            return "guest_general_inquiry"

# --- Nodes for the Graph ---
def classify_input(state: RefactorState):
    """Simulates classifying user and intent."""
    query_lower = state["query"].lower()
    user = "guest"
    if "premium" in query_lower: user = "premium"
    elif "standard" in query_lower: user = "standard"
    
    intent = "general"
    if "bill" in query_lower or "invoice" in query_lower: intent = "billing"
    elif "product" in query_lower or "feature" in query_lower: intent = "product"
    
    print(f"Input classified: User='{user}', Intent='{intent}'")
    return {"user_segment": user, "detected_intent": intent}

def generic_handler(state: RefactorState, handler_name: str):
    print(f"Routing to {handler_name}.")
    return {"response": f"Handled by {handler_name} for query: {state['query']}"}

# Define nodes dynamically to avoid repetition for generic handlers
node_names = [
    "premium_billing_escalation", "premium_product_support", "premium_general_support",
    "standard_billing_dispute", "standard_billing_general", "standard_product_technical",
    "standard_product_general", "standard_general_support",
    "guest_product_demo", "guest_general_inquiry"
]
node_map = {name: lambda s, n=name: generic_handler(s, n) for name in node_names}

# Build the Graph
workflow = StateGraph(RefactorState)

workflow.add_node("classify_input", classify_input)
for name, func in node_map.items():
    workflow.add_node(name, func)

workflow.set_entry_point("classify_input")

workflow.add_conditional_edges(
    "classify_input",
    refactored_router,
    {name: name for name in node_names} # Map all node names
)

for name in node_names:
    workflow.add_edge(name, END)

app = workflow.compile()

# Example Invocations
print("--- Test 1: Premium Urgent Billing ---")
app.invoke({"query": "premium user urgent bill query"})

print("\n--- Test 2: Standard Product Technical ---")
app.invoke({"query": "standard user technical product question"})

print("\n--- Test 3: Guest Product Demo ---")
app.invoke({"query": "guest user interested in product demo"})

print("\n--- Test 4: Standard Billing General ---")
app.invoke({"query": "standard user general billing inquiry"})
```
This example first shows an imagined "original_complex_router" to illustrate what to avoid. Then, it demonstrates how to *refactor complex conditions* using small, clear helper functions like `is_premium_user`. The `refactored_router` becomes much easier to read and maintain. This is a vital part of *production conditional edges best practices*.

### Conclusion: Mastering Conditional Edges for Production AI in 2026

You've now explored the critical aspects of building robust, production-ready AI applications using LangGraph conditional edges. We've covered everything from basic *production routing patterns* to advanced *refactoring complex conditions*. By applying these *production conditional edges best practices*, you can create AI systems that are not just smart but also reliable, scalable, and easy to maintain.

Remember, the goal for 2026 is to build AI that adapts seamlessly to real-world scenarios. This requires careful design, rigorous testing, and continuous monitoring of your conditional logic. Embrace these principles, and your LangGraph applications will stand strong.

Start implementing these strategies in your LangGraph projects today. Build AI that makes smart decisions every time! Your users and your future self will thank you.