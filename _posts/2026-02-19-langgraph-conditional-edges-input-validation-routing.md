---
title: "LangGraph Conditional Edges Example: User Input Validation & Dynamic Routing"
description: "Master LangGraph conditional edges for robust user input validation and dynamic routing. Learn practical examples to build smarter, resilient AI apps today."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [conditional edges input validation]
featured: false
image: '/assets/images/langgraph-conditional-edges-input-validation-routing.webp'
---

## LangGraph Conditional Edges Example: User Input Validation & Dynamic Routing

Imagine you're building a smart assistant or a powerful application. This application needs to talk to people and understand what they want. But what if people type something unexpected, or make a mistake? How does your program handle that gracefully?

This is where LangGraph's amazing feature called "conditional edges" comes in handy. It's like a smart traffic cop for your program, guiding information based on certain rules. Today, we will explore how to use **conditional edges input validation** to make your applications smarter and more robust. We'll also see how this helps in **dynamic routing**.

### What Are Conditional Edges in LangGraph?

Think of your LangGraph program as a journey with many stops, called "nodes." Usually, after visiting one stop, you just go to the next one in a fixed line. But what if you need to choose different paths based on what happened at the last stop?

Conditional edges are like decision points on your journey. They let your program look at some information and then decide which stop to visit next. This is super powerful for creating intelligent and flexible workflows. It allows for **validation-based branching** in your AI applications.

### Why is User Input Validation So Important?

When you ask a user for information, they might type anything. They could enter text when you expect a number, or provide an invalid date. If your program just tries to use this bad input, it might crash or give wrong answers. This is why **input validation** is a crucial step.

Validation checks if the user's input follows the rules you set. It's like checking a ticket before someone gets on a train. Good **input sanitization flows** protect your program from bad data. It makes your application more reliable and user-friendly.

#### Common Problems Without Validation:

*   **Errors and Crashes:** Trying to do math with text will break your program.
*   **Wrong Results:** An incorrect date might lead to scheduling issues.
*   **Poor User Experience:** Users get frustrated when things don't work.
*   **Security Risks:** Malicious input can sometimes be used to hack systems.

By using **conditional edges input validation**, you can catch these issues early. You can then guide the user to correct their input before it causes problems. This is a fundamental part of building any robust system.

### Setting Up Our LangGraph Playground

Before we dive into examples, let's quickly set up the basic parts of a LangGraph application. If you're new to LangGraph, you might want to check out our post on [How to build a simple LangGraph agent](/blog/simple-langgraph-agent.md) for a gentler introduction.

#### The `State` of Our Application

In LangGraph, information flows through something called `State`. Think of `State` as a shared notebook where all parts of your program can read and write notes. Our example will use a simple state to hold user input and validation messages.

```python
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
import operator

# Define the state for our graph
class AgentState(TypedDict):
    """
    Represents the state of our agent throughout the graph.
    """
    user_input: str
    validation_errors: List[str]
    is_valid: bool
    attempt_count: int
    feedback_message: str

```

Here, `user_input` will hold what the user types. `validation_errors` will store any problems found. `is_valid` will be `True` if everything is good, and `False` otherwise. `attempt_count` tracks how many times the user has tried. `feedback_message` is what we tell the user.

### Step 1: Gathering User Input

Our first node in the LangGraph will be very simple. Its job is just to get information from the user. For our examples, we'll simulate this with a function that takes an input string. In a real application, this might come from a chatbot interface or a web form.

```python
def get_user_input_node(state: AgentState) -> AgentState:
    """
    Simulates getting user input. In a real app, this might come from an API or user interface.
    """
    current_input = state.get("user_input", "")
    print(f"\nCurrent Input: '{current_input}'")
    
    # Simulate getting new input
    new_input = input("Please enter your age (e.g., 30) or 'quit': ")
    
    if new_input.lower() == 'quit':
        return {"user_input": "quit", "is_valid": False, "feedback_message": "Exiting application."}

    return {"user_input": new_input, "validation_errors": [], "feedback_message": "", "attempt_count": state.get("attempt_count", 0) + 1}
```

This node updates the `user_input` in our `AgentState`. It also clears any old validation errors and messages. We increment `attempt_count` to track retries.

### Step 2: Implementing Conditional Edges Input Validation

Now for the exciting part! We'll create a node that checks the user's input. This node won't just perform checks; it will also prepare the `AgentState` so that our conditional edge can make a decision. This is where various **input validation patterns** come into play.

Let's imagine we want the user to enter their age. We have two rules:
1.  The input must be a number.
2.  The number must be between 0 and 120.

```python
def validate_age_node(state: AgentState) -> AgentState:
    """
    Validates the user's age input.
    Checks if it's a number and within a reasonable range (0-120).
    """
    user_input = state["user_input"]
    errors = []
    is_valid = True
    feedback = ""

    if user_input.lower() == 'quit':
        return {"is_valid": False} # Special case to exit

    try:
        age = int(user_input)
        if not (0 <= age <= 120):
            errors.append("Age must be between 0 and 120.")
            is_valid = False
    except ValueError:
        errors.append("Input must be a whole number for age.")
        is_valid = False

    if not is_valid:
        feedback = f"Validation failed: {', '.join(errors)}. Please try again."
        print(f"Validation failed for '{user_input}': {errors}")
    else:
        feedback = f"Thank you, age {age} has been accepted!"
        print(f"Validation successful for '{user_input}'.")

    return {"validation_errors": errors, "is_valid": is_valid, "feedback_message": feedback}

```

The `validate_age_node` function does the actual checking. It returns an updated state with `is_valid` set to `True` or `False`. It also fills `validation_errors` and `feedback_message`. This is a clear example of **validation failure handling** within a node.

#### The Decision Function: The Heart of the Conditional Edge

The conditional edge needs a special function to decide where to go next. This function looks at the current `State` and returns the name of the *next node* to visit. Or, it can return a special `END` signal to stop the graph.

```python
def decide_next_step(state: AgentState) -> str:
    """
    Decision function for conditional edge.
    Routes based on validation success or failure, or if user wants to quit.
    """
    if state["user_input"].lower() == 'quit':
        return "end_process" # A specific node for graceful exit
    if state["is_valid"]:
        return "process_valid_input"
    else:
        # Check if we've exceeded max attempts
        max_attempts = 3
        if state["attempt_count"] >= max_attempts:
            print(f"Maximum attempts ({max_attempts}) reached. Exiting.")
            return "max_attempts_reached"
        else:
            return "get_user_input_again" # Go back to ask for input

```

This `decide_next_step` function is our traffic cop. If `is_valid` is `True`, it tells the graph to go to `"process_valid_input"`. If `is_valid` is `False`, it tells the graph to go to `"get_user_input_again"`. We also added a check for `'quit'` and `max_attempts_reached` to gracefully handle user requests to exit or too many failed attempts. This shows **dynamic form routing** in action, as the path changes based on user input and validation outcomes.

### Step 3: Dynamic Routing Based on Validation Results

Now we connect everything in our LangGraph. We will have different paths for successful validation and for failed validation. This is known as **dynamic routing**, where the flow of your program changes based on runtime conditions.

#### Building the Graph

Let's put together our nodes and edges.

```python
# Dummy nodes for different paths
def process_valid_input_node(state: AgentState) -> AgentState:
    """Node to simulate processing successfully validated input."""
    print(f"\nSUCCESS! Age '{state['user_input']}' is valid and accepted. Proceeding with task.")
    print(state["feedback_message"])
    # In a real app, this would trigger the next main business logic step
    return {"feedback_message": "Input processed successfully."}

def get_user_input_again_node(state: AgentState) -> AgentState:
    """Node to prompt user for input again after validation failure."""
    print(f"\n{state['feedback_message']}")
    print("Please try entering your age again.")
    # Here, we effectively loop back to `get_user_input_node` in the graph setup
    # The actual user input prompt happens in `get_user_input_node`
    return {"user_input": "", "validation_errors": [], "feedback_message": state["feedback_message"]}

def max_attempts_reached_node(state: AgentState) -> AgentState:
    """Node to handle when maximum validation attempts are reached."""
    print(f"\nERROR: Maximum validation attempts reached. Exiting without processing. Last input: '{state['user_input']}'.")
    print(f"Validation errors: {', '.join(state['validation_errors'])}")
    return {"feedback_message": "Max attempts reached. Exited."}

def end_process_node(state: AgentState) -> AgentState:
    """Node to handle a graceful exit when user explicitly quits."""
    print(f"\nUser chose to quit. Exiting application.")
    print(state["feedback_message"])
    return {"feedback_message": "User quit. Exited."}

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("get_user_input", get_user_input_node)
workflow.add_node("validate_age", validate_age_node)
workflow.add_node("process_valid_input", process_valid_input_node)
workflow.add_node("get_user_input_again", get_user_input_again_node)
workflow.add_node("max_attempts_reached", max_attempts_reached_node)
workflow.add_node("end_process", end_process_node)

# Set the entry point
workflow.set_entry_point("get_user_input")

# Add edges
# From get_user_input to validate_age (always validate after getting input)
workflow.add_edge("get_user_input", "validate_age")

# Conditional edge from validate_age
workflow.add_conditional_edges(
    "validate_age",
    decide_next_step,
    {
        "process_valid_input": "process_valid_input",
        "get_user_input_again": "get_user_input", # Loop back to get new input
        "max_attempts_reached": "max_attempts_reached",
        "end_process": "end_process"
    }
)

# End points for successful processing, max attempts, and user quitting
workflow.add_edge("process_valid_input", END)
workflow.add_edge("max_attempts_reached", END)
workflow.add_edge("end_process", END)

# Compile the graph
app = workflow.compile()

# You can visualize the graph if you have graphviz installed:
# from IPython.display import Image, display
# display(Image(app.get_graph().draw_mermaid_png()))
```

Let's break down the `add_conditional_edges` part:

*   `"validate_age"`: This is the node where the decision is made.
*   `decide_next_step`: This is our decision function. It looks at the state after `validate_age` runs.
*   The dictionary `{...}`: This maps the output string from `decide_next_step` to the actual node name.
    *   If `decide_next_step` returns `"process_valid_input"`, the graph goes to the `process_valid_input` node.
    *   If it returns `"get_user_input_again"`, the graph loops back to `get_user_input`. This is our **retry logic patterns** in action.
    *   If it returns `"max_attempts_reached"`, the graph goes to `max_attempts_reached`.
    *   If it returns `"end_process"`, the graph goes to `end_process`.

This setup clearly demonstrates **error path routing** and **user feedback paths**. If validation fails, the user is given feedback and asked to try again. If they exceed attempts, a different path is taken.

#### Running Our Example

Let's try running this application.

```python
# Example Usage:
print("--- Starting Age Validation Example ---")
# Initial state (optional, can be empty as get_user_input initializes some)
initial_state = {"user_input": "", "validation_errors": [], "is_valid": False, "attempt_count": 0, "feedback_message": ""}

# The graph will prompt for input inside the 'get_user_input' node
final_state = app.invoke(initial_state) 
print("\n--- Process Finished ---")
print(f"Final State Feedback: {final_state['feedback_message']}")
```

When you run this, it will:
1.  Ask for your age.
2.  If you enter "abc" or "150", it will say "Validation failed..." and ask again. This is the **user feedback paths** in action.
3.  If you do this three times, it will hit `max_attempts_reached` and stop.
4.  If you enter "30", it will say "SUCCESS!" and end the process.
5.  If you enter "quit", it will end gracefully.

This simple example shows the core idea of **conditional edges input validation**. You validate, then you route.

### Example 2: Textual Validation & User Intent Routing

Let's build on our understanding. What if we need to validate text, like a product name? And what if the user's intent depends on whether the product is found or not? This introduces **user intent routing** based on validation.

#### Extending Our State

First, we'll add some new fields to our `AgentState` to support product validation.

```python
class AgentState(TypedDict):
    user_input: str
    validation_errors: List[str]
    is_valid: bool
    attempt_count: int
    feedback_message: str
    
    # New fields for product validation
    product_name: str
    product_found: bool
    available_products: List[str] # Example: ["apple", "banana", "orange"]
```

#### New Nodes for Product Validation

We'll need a new node to get product input and another to validate it.

```python
def get_product_input_node(state: AgentState) -> AgentState:
    """Gets product name input from the user."""
    print(f"\nAvailable products: {state.get('available_products', ['apple', 'banana'])}")
    product_input = input("Please enter a product name or 'quit': ")
    if product_input.lower() == 'quit':
        return {"user_input": "quit", "is_valid": False, "feedback_message": "Exiting product selection."}
    return {"user_input": product_input, "validation_errors": [], "feedback_message": "", "attempt_count": state.get("attempt_count", 0) + 1}

def validate_product_node(state: AgentState) -> AgentState:
    """
    Validates if the entered product name is in the list of available products.
    """
    user_input = state["user_input"].lower().strip()
    available_products = state.get("available_products", ["apple", "banana", "orange"]) # Default list
    
    errors = []
    is_valid = True
    product_found = False
    feedback = ""

    if user_input == 'quit':
        return {"is_valid": False} # Special case to exit
    
    if user_input in available_products:
        product_found = True
        feedback = f"Product '{user_input}' found! What would you like to do?"
        print(f"Product '{user_input}' is available.")
    else:
        errors.append(f"Product '{user_input}' not found. Please choose from: {', '.join(available_products)}.")
        is_valid = False
        feedback = f"Validation failed: {', '.join(errors)}. Please try again."
        print(f"Product '{user_input}' not found.")

    return {"validation_errors": errors, "is_valid": is_valid, "product_name": user_input, "product_found": product_found, "feedback_message": feedback}

```

#### New Decision Function for Product Routing

Our decision function will now check `product_found` to route.

```python
def decide_product_path(state: AgentState) -> str:
    """
    Routes based on whether the product was found, or if user wants to quit.
    """
    if state["user_input"].lower() == 'quit':
        return "end_process"
    if state["product_found"]:
        return "handle_product_intent" # Product found, now decide what to do
    else:
        # Check max attempts for product input
        max_attempts = 2
        if state["attempt_count"] >= max_attempts:
            print(f"Maximum attempts ({max_attempts}) reached for product selection. Exiting.")
            return "max_attempts_reached"
        else:
            return "get_product_input" # Ask for product again

```

#### Nodes for Handling Product Intent

If a product is found, we might have different follow-up actions. This is true **user intent routing**.

```python
def handle_product_intent_node(state: AgentState) -> AgentState:
    """Node to ask the user what they want to do with the found product."""
    print(f"\nProduct '{state['product_name']}' is available. Do you want to 'buy', 'check_details', or 'cancel'?")
    intent_input = input("Your choice: ")
    return {"user_input": intent_input.lower(), "product_name": state["product_name"]} # Overwrite user_input for next decision

def route_product_intent(state: AgentState) -> str:
    """Routes based on user's stated intent for the product."""
    intent = state["user_input"]
    if intent == "buy":
        return "process_purchase"
    elif intent == "check_details":
        return "show_product_details"
    elif intent == "cancel":
        print("Okay, cancelling product action.")
        return "end_process" # User chose to cancel this specific flow
    else:
        print(f"Unknown intent '{intent}'. Please choose 'buy', 'check_details', or 'cancel'.")
        # For simplicity, if unknown, let's just end or loop back to asking intent.
        # A more robust system would have a dedicated "ask_intent_again" node.
        return "handle_product_intent" # Loop back to ask for intent again

def process_purchase_node(state: AgentState) -> AgentState:
    """Simulates processing a purchase."""
    print(f"\nProcessing purchase for '{state['product_name']}'. Thank you!")
    return {"feedback_message": "Purchase completed."}

def show_product_details_node(state: AgentState) -> AgentState:
    """Simulates showing product details."""
    print(f"\nShowing details for '{state['product_name']}'. It's a great choice!")
    return {"feedback_message": "Details shown."}

```

#### Rebuilding the Graph for Product Flow

Now, let's assemble this into a new graph. Notice how we are chaining **form validation workflows** together.

```python
# Build the graph for product validation
product_workflow = StateGraph(AgentState)

# Add nodes
product_workflow.add_node("get_product_input", get_product_input_node)
product_workflow.add_node("validate_product", validate_product_node)
product_workflow.add_node("get_product_input_again", get_product_input_node) # Reuse the same input node for retries
product_workflow.add_node("handle_product_intent", handle_product_intent_node)
product_workflow.add_node("process_purchase", process_purchase_node)
product_workflow.add_node("show_product_details", show_product_details_node)
product_workflow.add_node("max_attempts_reached", max_attempts_reached_node) # Reuse from age example
product_workflow.add_node("end_process", end_process_node) # Reuse from age example

# Set initial state for available products
initial_product_state = {"available_products": ["apple", "banana", "orange"], "attempt_count": 0}
product_workflow.set_entry_point("get_product_input")

# Edges
product_workflow.add_edge("get_product_input", "validate_product")

# Conditional edge from validate_product
product_workflow.add_conditional_edges(
    "validate_product",
    decide_product_path,
    {
        "handle_product_intent": "handle_product_intent",
        "get_product_input": "get_product_input", # Loop back to get new input
        "max_attempts_reached": "max_attempts_reached",
        "end_process": "end_process"
    }
)

# Conditional edge from handle_product_intent for sub-routing
product_workflow.add_conditional_edges(
    "handle_product_intent",
    route_product_intent,
    {
        "process_purchase": "process_purchase",
        "show_product_details": "show_product_details",
        "handle_product_intent": "handle_product_intent", # Loop back to ask for intent again
        "end_process": "end_process"
    }
)

# End points for the various product paths
product_workflow.add_edge("process_purchase", END)
product_workflow.add_edge("show_product_details", END)
product_workflow.add_edge("max_attempts_reached", END)
product_workflow.add_edge("end_process", END)

product_app = product_workflow.compile()

# Example Usage:
print("\n--- Starting Product Validation and Intent Routing Example ---")
final_product_state = product_app.invoke(initial_product_state)
print("\n--- Product Process Finished ---")
print(f"Final State Feedback: {final_product_state['feedback_message']}")
```

This extended example shows how **conditional edges input validation** allows for very specific **user intent routing**. If the product is found (validation succeeds), we then route to ask about the *user's intent* for that product. If it's not found, we loop back or exit. This is a powerful demonstration of **dynamic form routing**.

### Advanced Form Validation Workflows with LangGraph

Sometimes, you need to validate multiple pieces of information from a user, perhaps in a sequence. LangGraph's structure makes this very manageable. You can chain validation nodes or even have a single comprehensive validation node that checks many things.

#### Chaining Multiple Validations

Imagine an order form where you need both age (from our first example) and product (from our second example). You can string these validations together.

```python
# To combine, we'd adjust the state and decision functions to manage a multi-stage validation.
# For instance, after age validation, if valid, you move to product input.
# The `decide_next_step` function could be modified to track overall progress.

# Example of a combined decision function:
def decide_combined_flow(state: AgentState) -> str:
    if state["user_input"].lower() == 'quit':
        return "end_process"

    # Assume we have a 'current_validation_stage' in state (e.g., "age", "product")
    current_stage = state.get("current_validation_stage", "age")

    if current_stage == "age":
        if state["is_valid"]:
            # Age is valid, now move to product validation
            return "get_product_input"
        else:
            # Age is invalid, loop back or exit based on attempt_count
            max_attempts = 3
            if state["attempt_count"] >= max_attempts:
                return "max_attempts_reached"
            else:
                return "get_user_input" # Ask for age again

    elif current_stage == "product":
        if state["product_found"]:
            # Product is valid, move to intent handling
            return "handle_product_intent"
        else:
            # Product invalid, loop back or exit
            max_attempts = 2
            if state["attempt_count"] >= max_attempts:
                return "max_attempts_reached"
            else:
                return "get_product_input" # Ask for product again
    
    return "error_state" # Should not happen

```

In this setup, your graph would first go through age validation. Once the age is valid, the `decide_combined_flow` function would direct it to the product input node. This creates sophisticated **form validation workflows**.

#### Using a Single Comprehensive Validator Node

For simpler forms, you might have one node that performs all checks and returns a detailed validation report.

```python
def comprehensive_validator_node(state: AgentState) -> AgentState:
    """
    Performs multiple validation checks and returns a summary.
    """
    user_input_age = state.get("age_input", "")
    user_input_product = state.get("product_input", "")
    
    errors = []
    is_overall_valid = True
    
    # Age validation
    try:
        age = int(user_input_age)
        if not (0 <= age <= 120):
            errors.append("Age must be between 0 and 120.")
            is_overall_valid = False
    except ValueError:
        if user_input_age: # Only add error if something was actually entered
            errors.append("Age must be a whole number.")
            is_overall_valid = False

    # Product validation
    available_products = ["apple", "banana", "orange"]
    product_found = False
    if user_input_product.lower().strip() not in available_products:
        if user_input_product:
            errors.append(f"Product '{user_input_product}' not found. Available: {', '.join(available_products)}.")
            is_overall_valid = False
        product_found = False
    else:
        product_found = True

    feedback = f"Overall validation status: {'Success' if is_overall_valid else 'Failed'}."
    if errors:
        feedback += f" Errors: {'; '.join(errors)}"

    return {
        "validation_errors": errors, 
        "is_valid": is_overall_valid, 
        "feedback_message": feedback,
        "product_found": product_found # Still useful for later routing if needed
    }

```

This node would return `is_overall_valid` and the list of errors. Your conditional edge would then route based on `is_overall_valid`. This approach consolidates **input validation patterns** into one place, useful for simpler forms.

### Implementing Retry Logic Patterns and User Feedback Paths

We've touched on this in our examples, but let's make it explicit. A good user experience often involves giving the user a chance to correct their mistakes. This means using **retry logic patterns** and clear **user feedback paths**.

In our age validation example, the `decide_next_step` function sends the user back to `get_user_input` if `is_valid` is `False`. This is a retry. We also included `attempt_count` to limit how many times a user can retry before the system gives up or escalates.

The `feedback_message` in our `AgentState` is crucial for **user feedback paths**. Instead of just saying "Error!", we provide specific reasons: "Input must be a whole number for age." or "Age must be between 0 and 120." Clear feedback helps the user understand what went wrong and how to fix it.

Consider these enhancements:
*   **Contextual Feedback:** If the error is about a minimum value, the message could dynamically suggest a valid range.
*   **Helpful Suggestions:** If a product name is close to an available one (e.g., "aple" vs "apple"), suggest the correct spelling.
*   **Escalation:** After too many failed attempts, instead of just exiting, route to a human agent or provide a link to a help page. This is part of sophisticated **validation failure handling**.

### Beyond Validation: More User Intent Routing

Once input is validated, `conditional edges` continue to be incredibly useful for **user intent routing**. For example, a customer support bot might first validate a customer ID. Once validated, it can then route the user to different functions based on their *next* intent: "check order status," "talk to support," or "update profile."

This is where your LangGraph agent really shines, moving beyond simple validation to complex, multi-turn conversations. You can learn more about this in a blog post about [Advanced Agent Routing with LLMs](/blog/advanced-agent-routing-llms.md) (fictional internal link).

### Putting It All Together: A Comprehensive Dynamic Form Routing Example

Let's imagine a customer service flow. The customer first provides their ID. We validate it. If valid, we ask what they want to do. If invalid, we ask them to try again, with a limit.

#### Updated `AgentState`

```python
class CustomerServiceState(TypedDict):
    current_input: str
    customer_id: str
    is_id_valid: bool
    customer_intent: str
    validation_errors: List[str]
    attempt_count: int
    feedback_message: str
```

#### New Nodes for Customer ID and Intent

```python
def get_customer_id_node(state: CustomerServiceState) -> CustomerServiceState:
    """Gets customer ID input."""
    print(f"\nWelcome! Current attempt: {state.get('attempt_count', 0) + 1}")
    id_input = input("Please enter your 6-digit customer ID or 'quit': ")
    if id_input.lower() == 'quit':
        return {"current_input": "quit", "feedback_message": "Exiting customer service."}
    return {"current_input": id_input, "validation_errors": [], "feedback_message": "", "attempt_count": state.get("attempt_count", 0) + 1}

def validate_customer_id_node(state: CustomerServiceState) -> CustomerServiceState:
    """Validates if customer ID is a 6-digit number."""
    customer_id_str = state["current_input"]
    errors = []
    is_valid = True
    feedback = ""

    if customer_id_str.lower() == 'quit':
        return {"is_id_valid": False}
    
    if len(customer_id_str) != 6 or not customer_id_str.isdigit():
        errors.append("Customer ID must be a 6-digit number.")
        is_valid = False
    
    if not is_valid:
        feedback = f"Validation failed: {', '.join(errors)}. Please try again."
        print(f"Validation failed for ID '{customer_id_str}': {errors}")
    else:
        feedback = f"Customer ID '{customer_id_str}' accepted."
        print(f"Validation successful for ID '{customer_id_str}'.")

    return {"validation_errors": errors, "is_id_valid": is_valid, "customer_id": customer_id_str, "feedback_message": feedback}

def ask_customer_intent_node(state: CustomerServiceState) -> CustomerServiceState:
    """Asks the customer what they need assistance with."""
    print(f"\nHello, Customer ID {state['customer_id']}! How can I help you today?")
    print("Options: 'order_status', 'tech_support', 'billing_query', 'speak_to_agent', 'cancel'.")
    intent_input = input("Please enter your request: ")
    return {"customer_intent": intent_input.lower(), "current_input": intent_input.lower()} # Store intent and current_input for next decision

def route_customer_intent_node(state: CustomerServiceState) -> str:
    """Routes based on the customer's stated intent."""
    intent = state["customer_intent"]
    if intent == "order_status":
        return "handle_order_status"
    elif intent == "tech_support":
        return "handle_tech_support"
    elif intent == "billing_query":
        return "handle_billing_query"
    elif intent == "speak_to_agent":
        return "escalate_to_agent"
    elif intent == "cancel":
        print("Okay, cancelling current customer service request.")
        return "end_process"
    else:
        print(f"I don't understand '{intent}'. Please choose from the options.")
        return "ask_customer_intent" # Loop back to ask again

# Dummy nodes for handling different intents
def handle_order_status_node(state: CustomerServiceState) -> CustomerServiceState:
    print(f"\nRetrieving order status for Customer ID: {state['customer_id']}...")
    print("Your last order (ID: XYZ123) was shipped yesterday.")
    return {"feedback_message": "Order status provided."}

def handle_tech_support_node(state: CustomerServiceState) -> CustomerServiceState:
    print(f"\nConnecting you to tech support for Customer ID: {state['customer_id']}...")
    print("Please describe your technical issue in more detail.")
    return {"feedback_message": "Tech support engaged."}

def handle_billing_query_node(state: CustomerServiceState) -> CustomerServiceState:
    print(f"\nAccessing billing information for Customer ID: {state['customer_id']}...")
    print("Your last bill was $50.00 due on 15th of this month.")
    return {"feedback_message": "Billing info provided."}

def escalate_to_agent_node(state: CustomerServiceState) -> CustomerServiceState:
    print(f"\nEscalating to a live agent for Customer ID: {state['customer_id']}...")
    print("Please wait while we connect you to an available agent.")
    return {"feedback_message": "Escalated to agent."}

def customer_id_failed_attempts_node(state: CustomerServiceState) -> CustomerServiceState:
    print(f"\nERROR: Maximum customer ID validation attempts reached. Please try again later or visit our website.")
    print(f"Last input: '{state['current_input']}'. Errors: {', '.join(state['validation_errors'])}")
    return {"feedback_message": "Max ID attempts. Exited."}

def customer_service_end_process_node(state: CustomerServiceState) -> CustomerServiceState:
    print(f"\nThank you for contacting customer service. Goodbye!")
    return {"feedback_message": "Customer service session ended."}
```

#### Decision Function for Customer ID Validation

```python
def decide_id_validation_path(state: CustomerServiceState) -> str:
    if state["current_input"].lower() == 'quit':
        return "end_service"
    if state["is_id_valid"]:
        return "ask_customer_intent"
    else:
        max_attempts = 3
        if state["attempt_count"] >= max_attempts:
            return "customer_id_failed_attempts"
        else:
            return "get_customer_id" # Loop back to get ID again
```

#### The Full Customer Service Graph

```python
# Build the customer service graph
customer_workflow = StateGraph(CustomerServiceState)

# Add nodes
customer_workflow.add_node("get_customer_id", get_customer_id_node)
customer_workflow.add_node("validate_customer_id", validate_customer_id_node)
customer_workflow.add_node("ask_customer_intent", ask_customer_intent_node)
customer_workflow.add_node("handle_order_status", handle_order_status_node)
customer_workflow.add_node("handle_tech_support", handle_tech_support_node)
customer_workflow.add_node("handle_billing_query", handle_billing_query_node)
customer_workflow.add_node("escalate_to_agent", escalate_to_agent_node)
customer_workflow.add_node("customer_id_failed_attempts", customer_id_failed_attempts_node)
customer_workflow.add_node("end_service", customer_service_end_process_node)

# Set entry point
customer_workflow.set_entry_point("get_customer_id")

# Edges for ID validation
customer_workflow.add_edge("get_customer_id", "validate_customer_id")
customer_workflow.add_conditional_edges(
    "validate_customer_id",
    decide_id_validation_path,
    {
        "ask_customer_intent": "ask_customer_intent",
        "get_customer_id": "get_customer_id", # Loop back for retry
        "customer_id_failed_attempts": "customer_id_failed_attempts",
        "end_service": "end_service"
    }
)

# Conditional edges for customer intent routing
customer_workflow.add_conditional_edges(
    "ask_customer_intent",
    route_customer_intent_node,
    {
        "handle_order_status": "handle_order_status",
        "handle_tech_support": "handle_tech_support",
        "handle_billing_query": "handle_billing_query",
        "escalate_to_agent": "escalate_to_agent",
        "ask_customer_intent": "ask_customer_intent", # Loop back if intent not understood
        "end_service": "end_service"
    }
)

# End points for the various service paths
customer_workflow.add_edge("handle_order_status", END)
customer_workflow.add_edge("handle_tech_support", END)
customer_workflow.add_edge("handle_billing_query", END)
customer_workflow.add_edge("escalate_to_agent", END)
customer_workflow.add_edge("customer_id_failed_attempts", END)
customer_workflow.add_edge("end_service", END)

customer_app = customer_workflow.compile()

# Example Usage
print("\n--- Starting Comprehensive Customer Service Example ---")
initial_customer_state = {"attempt_count": 0, "validation_errors": [], "feedback_message": ""}
final_customer_state = customer_app.invoke(initial_customer_state)
print("\n--- Customer Service Process Finished ---")
print(f"Final State Feedback: {final_customer_state['feedback_message']}")

```

This comprehensive example fully showcases **dynamic form routing**. The customer's journey through the service is entirely driven by their input and its validation. We first validate the ID, and then based on that success, we dynamically route to ask for their intent. Their subsequent intent then leads to another dynamic routing decision. This provides a very flexible and robust conversation flow for any application.

### Benefits of Using Conditional Edges for Validation and Routing

Using `conditional edges input validation` in LangGraph brings many advantages:

*   **Robustness:** Your application becomes much more resistant to bad or unexpected user input. This prevents crashes and ensures reliable operation.
*   **Better User Experience:** Users get clear, immediate feedback on their input, and are guided on how to correct mistakes. This makes the application feel smart and helpful.
*   **Clear Logic:** The graph structure clearly separates validation logic from business logic. Each node has a single, easy-to-understand job. This aids in **validation-based branching**.
*   **Maintainability:** Changes to validation rules or routing paths are localized to specific nodes or decision functions. This makes your code easier to update and debug.
*   **Flexibility:** You can easily add new validation rules, new routing paths, or new stages to your **form validation workflows** without overhauling your entire system. This is the essence of **dynamic form routing**.
*   **Security:** Proper `input sanitization flows` and validation help mitigate common security vulnerabilities by ensuring that only expected data types and formats enter your system.
*   **Error Path Management:** You have explicit control over `error path routing`, allowing you to define exactly what happens when validation fails (retry, escalate, exit).

### Tips for Best Practices

To make the most of conditional edges for validation and routing:

1.  **Keep Nodes Focused:** Each node should do one thing well. A validation node should just validate, not try to process the input.
2.  **Clear Decision Functions:** Your decision functions should be simple and easy to read. They should clearly state the logic for routing.
3.  **Comprehensive Error Messages:** Provide specific and actionable feedback to the user when validation fails. Help them understand *why* it failed and *how* to fix it.
4.  **Define Max Retries:** Implement `retry logic patterns` with a sensible limit. Don't let users get stuck in an endless loop of failed validation.
5.  **Test Thoroughly:** Test all possible paths, including successful validations, failed validations, maximum retries, and explicit exits.
6.  **Use Semantic Keywords Naturally:** As you build out your nodes and functions, think about how to naturally weave in keywords like `conditional edges input validation`, `dynamic routing`, `user intent routing`, and `validation-based branching` in your internal documentation and comments.

### Conclusion

LangGraph's `conditional edges` are a powerful tool for building intelligent and resilient applications. By mastering `conditional edges input validation`, you can create programs that not only understand user input but also guide users effectively through complex processes. This leads to better user experiences, more robust systems, and clear, maintainable code.

We've seen how to implement basic numeric and textual `input validation patterns`, set up `dynamic routing` based on validation outcomes, manage `error path routing` with `retry logic patterns`, and provide helpful `user feedback paths`. The examples highlight how these concepts come together to create sophisticated `form validation workflows` and intelligent `user intent routing`.

Now, it's your turn! Experiment with LangGraph and `conditional edges` to make your applications smarter. Check out the [official LangGraph documentation](https://python.langchain.com/docs/langgraph/) for even more advanced features. Happy coding!