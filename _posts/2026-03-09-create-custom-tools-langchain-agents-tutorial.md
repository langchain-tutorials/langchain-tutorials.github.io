---
title: "Create Custom Tools for LangChain Agents: Complete Tutorial with Examples"
description: "Learn to create custom tools for LangChain agents with this complete tutorial. Build powerful agents by expanding their capabilities using practical examples."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [create custom tools langchain agents]
featured: false
image: '/assets/images/create-custom-tools-langchain-agents-tutorial.webp'
---

## Make Your AI Assistant Smarter: Learn to Create Custom Tools for LangChain Agents

Imagine you have a super smart robot helper. This robot can talk to you and understand many things. But what if you want it to do something very specific, like checking how many cookies are left in your jar or sending a special message to your friend?

That's where making your own custom tools comes in! In this guide, you will learn how to `create custom tools langchain agents`, turning your smart robot into an even more capable helper. We will explore how to teach your LangChain agent new tricks, step by step.

### What Are LangChain Agents and Why Do They Need Tools?

Think of a LangChain agent as an intelligent assistant. It uses a large language model (LLM) to "think" and decide what to do. This "thinking" lets it understand your questions and plan how to answer them.

But an agent can't just do everything by itself. It needs tools to interact with the outside world or to perform specific actions. These tools are like the robot's hands and special gadgets.

For example, an agent might use a "calculator tool" to do math or a "web search tool" to find information online. These are pre-made tools that come with LangChain.

### Why You Need to Create Custom Tools for LangChain Agents

While existing tools are helpful, they can't cover everything you might need. Your business or personal projects often have unique tasks. This is exactly why you need to `create custom tools langchain agents`.

Maybe you want your agent to check your company's sales database, or send a specific type of notification, or even control a smart home device. These are specialized tasks that require specialized tools. You can make these tools yourself.

By learning to `create custom tools langchain agents`, you unlock a whole new level of power. You can make your agents truly unique and tailored to your needs. This makes your AI assistant incredibly flexible and powerful.

### Getting Started: The Basics of Custom Tools

At its heart, a custom tool is just a regular Python function. You write a piece of Python code that does something specific. LangChain then has a special way to understand this function as a tool.

The magic mostly happens with a special label called a "decorator". You'll see how `Tool decorator usage` makes a simple function into a powerful tool. Let's start with a very simple example.

Imagine a tool that just tells you the time. You can write a Python function for that.

```python
import datetime

def get_current_time():
    """Returns the current time."""
    return datetime.datetime.now().strftime("%H:%M:%S")

print(get_current_time())
```

This is just a function. For LangChain to use it, we need to tell LangChain it's a tool.

### Step-by-Step Guide to Create Custom Tools LangChain Agents

Let's walk through how to `create custom tools langchain agents` in detail. Each step is important for your agent to understand and use your new tool correctly.

#### Step 1: Write Your Python Function

First, you need to write the Python code that performs the action you want. This is the core logic of your tool. It should do one specific thing well.

For example, let's create a tool that checks the "weather" for a specific city. The function will just simulate this for now, returning a simple message.

```python
# weather_tool.py
def check_city_weather(city_name: str) -> str:
    """
    Checks the current weather conditions for a specified city.
    For demonstration purposes, this returns a generic weather message.
    """
    if city_name.lower() == "london":
        return "The weather in London is cloudy with a chance of rain."
    elif city_name.lower() == "new york":
        return "It's sunny and warm in New York today."
    else:
        return f"Cannot find weather for {city_name}. Please try a major city."

```

This function takes one input, `city_name`, and gives back a string. This is `custom tool implementation` in its simplest form. Remember to keep your functions focused on a single task.

#### Step 2: Decorate Your Function with `@tool`

Now, to make your Python function a LangChain tool, you use the `@tool` decorator. This is a special Python syntax that essentially "tags" your function. It tells LangChain, "Hey, this function here is a tool!".

You just put `@tool` on the line right above your function definition. This is the most common `Tool decorator usage`.

```python
# weather_tool_decorated.py
from langchain.tools import tool
import datetime

@tool
def get_current_time_tool():
    """Returns the current time in HH:MM:SS format."""
    return datetime.datetime.now().strftime("%H:%M:%S")

@tool
def check_city_weather(city_name: str) -> str:
    """
    Checks the current weather conditions for a specified city.
    For demonstration purposes, this returns a generic weather message.
    """
    if city_name.lower() == "london":
        return "The weather in London is cloudy with a chance of rain."
    elif city_name.lower() == "new york":
        return "It's sunny and warm in New York today."
    else:
        return f"Cannot find weather for {city_name}. Please try a major city."

```

Now, `get_current_time_tool` and `check_city_weather` are recognized as tools by LangChain. The agent will be able to see and potentially use them. The text inside the `"""Docstring"""` below `@tool` becomes the tool's description.

#### Step 3: Write a Clear Tool Description

The description of your tool is super important. It's how the LangChain agent understands what your tool does and when to use it. Think of it as instructions for your agent. If the description is unclear, the agent might not use your tool, or it might use it incorrectly. This is key for `tool description writing`.

Your description should be:
*   **Clear**: Easy to understand.
*   **Concise**: Not too long, but complete enough.
*   **Action-oriented**: Describe what the tool *does*.
*   **Input-aware**: Mention what kind of input the tool expects.

Let's refine our `check_city_weather` tool's description.

```python
# weather_tool_description.py
from langchain.tools import tool

@tool
def check_city_weather(city_name: str) -> str:
    """
    Useful for getting the current weather for a specific city.
    Input should be the name of the city, e.g., 'London'.
    Returns a string describing the weather conditions.
    """
    if city_name.lower() == "london":
        return "The weather in London is cloudy with a chance of rain."
    elif city_name.lower() == "new york":
        return "It's sunny and warm in New York today."
    else:
        return f"Cannot find weather for {city_name}. Please try a major city."
```

Notice how the description now clearly states its purpose and what input it expects. Good `tool description writing` helps the agent make smart decisions. Without a good description, the agent won't know when to pick your tool over others.

#### Step 4: Define Tool Parameters

Many tools need information to do their job. For our `check_city_weather` tool, it needs to know *which* city's weather to check. This information is called a parameter or argument. `tool parameters definition` is how you tell LangChain what inputs your tool needs.

You define parameters just like you would in any Python function. It's a good idea to use type hints (like `city_name: str`) to make it even clearer what type of information the tool expects.

For more complex inputs, you might want to use Pydantic, a Python library for data validation. This helps ensure the agent sends the right kind of data to your tool. We'll look at that with `structured tool class` later.

Let's make a tool that calculates the area of a rectangle. It needs two parameters: `length` and `width`.

```python
# geometry_tool.py
from langchain.tools import tool

@tool
def calculate_rectangle_area(length: float, width: float) -> float:
    """
    Calculates the area of a rectangle given its length and width.
    Input should be two float numbers: 'length' and 'width'.
    Example: calculate_rectangle_area(length=5.0, width=10.0)
    """
    if length <= 0 or width <= 0:
        return "Error: Length and width must be positive numbers."
    return length * width

```

Here, `length: float` and `width: float` tell LangChain and the agent that these should be numbers with decimal points. This strong `tool parameters definition` prevents errors and helps the agent use the tool correctly.

### Advanced Custom Tool Concepts

Once you understand the basics of how to `create custom tools langchain agents`, you can explore more advanced ways to make your tools even better. These methods offer more control and handle more complex situations.

#### Handling Asynchronous Operations

Sometimes, your tool might take a long time to finish its job. For example, it might need to fetch data from a slow website or perform a complex calculation. If your agent waits for these slow tools, it can become sluggish. This is where `async tool creation` comes in handy.

Asynchronous tools allow your agent to start a task and then do other things while waiting for the tool to finish. It's like sending a letter and not waiting by the mailbox for the reply; you can do other chores in between.

To create an async tool, you use `async def` instead of just `def` for your function. You also need to make sure any actions inside that function that wait for something (like a web request) also use `await`.

```python
# async_tool_example.py
from langchain.tools import tool
import asyncio
import time

@tool
async def fetch_website_content(url: str) -> str:
    """
    Asynchronously fetches content from a given URL.
    This simulates a slow network request.
    Input should be a string representing the URL.
    """
    print(f"Fetching content from {url} asynchronously...")
    # Simulate a network delay
    await asyncio.sleep(3) # Waits for 3 seconds without blocking the agent
    if "example.com" in url:
        return f"Content from {url}: This is example website content."
    else:
        return f"Failed to fetch content from {url}: Website not found."

```

When the agent uses `fetch_website_content`, it can start the fetching process and then potentially think about the next step or prepare other information while the tool is running in the background. This `async tool creation` is very powerful for responsive agents.

#### Using the `StructuredTool` Class

The `@tool` decorator is great for simple functions, especially when your parameters can be easily described. However, sometimes you need more structure for your tool's inputs. What if your tool needs multiple parameters, or parameters that are optional, or specific data types that need validation? This is where the `structured tool class` shines.

`StructuredTool` allows you to define a schema (a blueprint) for your tool's inputs using Pydantic. Pydantic is a library that helps you define how data should look. This gives you more robust `tool parameters definition`.

To use `StructuredTool`, you often inherit from `BaseTool` (which `StructuredTool` itself does). You define a Pydantic class that represents the inputs your tool expects.

```python
# structured_tool_example.py
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
import time

# 1. Define the input schema using Pydantic
class ProductSearchInput(BaseModel):
    query: str = Field(description="The search term for the product, e.g., 'laptop'")
    max_results: int = Field(default=5, description="Maximum number of search results to return")
    category: str = Field(default=None, description="Optional category to filter results, e.g., 'electronics'")

# 2. Define the function that the tool will call
def _product_search(query: str, max_results: int, category: str = None) -> str:
    """
    Simulates searching for products in an e-commerce catalog.
    Takes a search query, max_results, and an optional category.
    """
    print(f"Searching for '{query}' with {max_results} results in category '{category or 'all'}'...")
    time.sleep(1) # Simulate search time
    results = [
        f"Product A ({query})",
        f"Product B ({query})",
        f"Product C ({query})"
    ]
    if category:
        results = [r for r in results if category in r.lower()]
    return f"Found {min(max_results, len(results))} products: {', '.join(results[:max_results])}"

# 3. Create the StructuredTool instance
product_search_tool = StructuredTool.from_function(
    func=_product_search,
    name="product_search",
    description="Searches for products in the inventory based on a query, max results, and optional category.",
    args_schema=ProductSearchInput,
    handle_tool_error=True # A useful feature for structured tools
)

# You can test it like this:
# print(product_search_tool.run({"query": "smartphone", "max_results": 2}))
# print(product_search_tool.run({"query": "keyboard", "category": "electronics"}))
```

In this example, `ProductSearchInput` tells the agent exactly what inputs are needed and what they mean. The `structured tool class` makes `tool parameters definition` much more robust and clearer for both you and the agent. This is very important when you `create custom tools langchain agents` for complex systems.

#### Inheriting from `BaseTool` for Full Control

For the ultimate control over your tool's behavior, you can directly inherit from LangChain's `BaseTool` class. This approach is for when you want to customize every aspect of your tool, including how it runs, how it handles errors, and even how its inputs are validated. This is the most powerful way to `create custom tools langchain agents`.

When you inherit from `BaseTool`, you must implement at least two main things:
1.  **`name`**: A unique name for your tool.
2.  **`description`**: A detailed explanation of what your tool does.
3.  **`_run(self, *args, **kwargs)`**: The synchronous (normal) method that contains your tool's logic.
4.  **`_arun(self, *args, **kwargs)` (optional)**: The asynchronous method for your tool's logic. If you implement `_arun`, you should generally use it for async operations.
5.  **`args_schema` (optional)**: A Pydantic model for input validation, similar to `StructuredTool`.

Let's create a custom tool using `BaseTool inheritance` that interacts with a simple "inventory" system.

```python
# basetool_example.py
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import time

# Simulate an inventory database
_INVENTORY = {
    "apples": 50,
    "bananas": 100,
    "oranges": 75,
}

# 1. Define the input schema for getting inventory
class GetInventorySchema(BaseModel):
    item_name: str = Field(description="The name of the item to check inventory for, e.g., 'apples'")

# 2. Define the input schema for updating inventory
class UpdateInventorySchema(BaseModel):
    item_name: str = Field(description="The name of the item to update")
    quantity: int = Field(description="The new quantity for the item")

# 3. Create the custom tool by inheriting from BaseTool
class InventoryCheckerTool(BaseTool):
    name: str = "inventory_checker"
    description: str = "Checks the current stock level of a specific item in the inventory. Input is the item name."
    args_schema: Type[BaseModel] = GetInventorySchema # Use the schema for input validation

    def _run(self, item_name: str) -> str:
        """Use the tool synchronously."""
        time.sleep(0.5) # Simulate database lookup
        if item_name.lower() in _INVENTORY:
            return f"Current stock of {item_name}: {_INVENTORY[item_name.lower()]}"
        else:
            return f"Item '{item_name}' not found in inventory."

    async def _arun(self, item_name: str) -> str:
        """Use the tool asynchronously."""
        # For simplicity, just call the sync version, but in a real app,
        # you'd use async database calls here.
        return self._run(item_name)

class InventoryUpdaterTool(BaseTool):
    name: str = "inventory_updater"
    description: str = "Updates the stock level of a specific item in the inventory. Input is the item name and new quantity."
    args_schema: Type[BaseModel] = UpdateInventorySchema

    def _run(self, item_name: str, quantity: int) -> str:
        """Use the tool synchronously."""
        time.sleep(0.5) # Simulate database update
        if item_name.lower() in _INVENTORY:
            _INVENTORY[item_name.lower()] = quantity
            return f"Updated stock of {item_name} to {quantity}. New inventory: {_INVENTORY[item_name.lower()]}"
        else:
            _INVENTORY[item_name.lower()] = quantity # Add new item
            return f"Added new item '{item_name}' with quantity {quantity}. New inventory: {_INVENTORY[item_name.lower()]}"

    async def _arun(self, item_name: str, quantity: int) -> str:
        """Use the tool asynchronously."""
        return self._run(item_name, quantity)

# You can use these tools in your agent directly.
# For example:
# checker = InventoryCheckerTool()
# updater = InventoryUpdaterTool()
# print(checker.run(item_name="apples"))
# print(updater.run(item_name="apples", quantity=60))
# print(checker.run(item_name="apples"))
```

This example shows how `BaseTool inheritance` gives you complete freedom to define how your tool behaves. You can define specific input schemas for different tools, manage internal state, and implement complex logic. This method is often preferred for large, production-ready applications where you `create custom tools langchain agents` for specific business workflows.

### Making Your Tools Robust: Error Handling and Testing

Even the best tools can encounter problems. A network might be down, a file might be missing, or a user might provide incorrect input. It's important to make your tools robust, meaning they can handle these issues gracefully. This involves `tool error handling` and `tool testing strategies`.

#### Tool Error Handling

When something goes wrong inside your tool, you don't want it to crash your entire agent. Instead, the tool should catch the error and return a helpful message to the agent. This allows the agent to understand what happened and perhaps try a different approach or inform the user.

You can use standard Python `try-except` blocks within your tool functions.

```python
# error_handling_tool.py
from langchain.tools import tool

@tool
def divide_numbers(numerator: float, denominator: float) -> str:
    """
    Divides two numbers.
    Input should be two float numbers: 'numerator' and 'denominator'.
    Handles division by zero gracefully.
    """
    try:
        if denominator == 0:
            # Instead of crashing, return a specific error message
            return "Error: Cannot divide by zero."
        result = numerator / denominator
        return f"The result of dividing {numerator} by {denominator} is {result}."
    except Exception as e:
        # Catch any other unexpected errors
        return f"An unexpected error occurred during division: {str(e)}"

# Example of how an agent might see it:
# print(divide_numbers(numerator=10, denominator=2))
# print(divide_numbers(numerator=10, denominator=0))
# print(divide_numbers(numerator="ten", denominator=2)) # This would be caught by type hints usually, but 'except' catches general issues
```

By implementing `tool error handling`, you ensure your agent remains stable and can provide more informative responses to users, even when issues arise. It's a crucial part of `custom tool implementation`.

#### Tool Testing Strategies

Just like any other piece of code, your custom tools need to be tested. Testing helps you make sure your tools work as expected and don't introduce unexpected bugs. There are a few `tool testing strategies` you can use.

1.  **Unit Testing**: Test the core Python function directly, without involving LangChain. This checks if the logic of your tool is correct.
2.  **Integration Testing**: Test your tool within a simple LangChain agent setup. This checks if the agent can correctly call and interpret your tool's output.

Let's look at an example for unit testing our `divide_numbers` tool. You would typically use a testing framework like `pytest` or Python's built-in `unittest`.

```python
# test_divide_numbers.py
import unittest
from error_handling_tool import divide_numbers # Assuming divide_numbers is in error_handling_tool.py

class TestDivideNumbersTool(unittest.TestCase):

    def test_positive_division(self):
        # Test a normal case
        result = divide_numbers(numerator=10, denominator=2)
        self.assertEqual(result, "The result of dividing 10 by 2 is 5.0.")

    def test_division_by_zero(self):
        # Test error handling for division by zero
        result = divide_numbers(numerator=10, denominator=0)
        self.assertEqual(result, "Error: Cannot divide by zero.")

    def test_negative_numbers(self):
        # Test with negative numbers
        result = divide_numbers(numerator=-10, denominator=2)
        self.assertEqual(result, "The result of dividing -10 by 2 is -5.0.")

    def test_float_results(self):
        # Test with numbers that result in a float
        result = divide_numbers(numerator=7, denominator=2)
        self.assertEqual(result, "The result of dividing 7 by 2 is 3.5.")

if __name__ == '__main__':
    unittest.main()

```

Running this test file (e.g., `python -m unittest test_divide_numbers.py`) would tell you if your tool's logic is sound. This systematic approach to `tool testing strategies` ensures high quality when you `create custom tools langchain agents`. For integration testing, you would create a minimal agent with your tool and prompt it to use it. You can learn more about agent testing by reading [this internal blog post on effective agent testing strategies](/blog/effective-agent-testing-strategies).

### Integrating Custom Tools with LangChain Agents

Once you have created and tested your custom tools, the next step is to give them to your LangChain agent. This is how the agent becomes aware of its new capabilities and can decide when to use them.

#### How Agents Use Your Tools

When you define an agent, you provide it with a list of tools. The agent then uses its "thinking" process (powered by the LLM) to look at your request and decide which tool (if any) to use. It reads the `tool description writing` and understands the `tool parameters definition` to make this choice.

The agent's decision-making process often involves:
1.  **Observation**: Looking at the current situation or user prompt.
2.  **Thought**: Deciding if a tool is needed, which tool, and what inputs to give it.
3.  **Action**: Calling the chosen tool with the specified inputs.
4.  **Observation (Tool Output)**: Reading the tool's result.
5.  **Thought (Again)**: Deciding the next step based on the tool's output, or formulating a final answer.

This cycle continues until the agent believes it has completed the task. You can read more about how agents decide which tools to use in [this guide on LangChain Agent Architectures and Decision Making](/blog/langchain-agent-architectures-decision-making).

#### Example: A Custom Inventory Management Agent

Let's bring everything together with an example. We'll use our `InventoryCheckerTool` and `InventoryUpdaterTool` from the `BaseTool` inheritance section to create a simple inventory management agent. This demonstrates how to `create custom tools langchain agents` for a practical application.

First, make sure you have LangChain and an LLM configured. You'll need an OpenAI API key or similar.

```python
# inventory_agent_example.py
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import time
import os

# Set your API key from environment variables
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # Make sure to set this up

# --- Inventory Tools Definition (from basetool_example.py) ---
_INVENTORY = {
    "apples": 50,
    "bananas": 100,
    "oranges": 75,
}

class GetInventorySchema(BaseModel):
    item_name: str = Field(description="The name of the item to check inventory for, e.g., 'apples'")

class UpdateInventorySchema(BaseModel):
    item_name: str = Field(description="The name of the item to update")
    quantity: int = Field(description="The new quantity for the item")

class InventoryCheckerTool(BaseTool):
    name: str = "inventory_checker"
    description: str = "Checks the current stock level of a specific item in the inventory. Input is the item name."
    args_schema: Type[BaseModel] = GetInventorySchema

    def _run(self, item_name: str) -> str:
        time.sleep(0.5)
        if item_name.lower() in _INVENTORY:
            return f"Current stock of {item_name}: {_INVENTORY[item_name.lower()]}"
        else:
            return f"Item '{item_name}' not found in inventory."

    async def _arun(self, item_name: str) -> str:
        return self._run(item_name)

class InventoryUpdaterTool(BaseTool):
    name: str = "inventory_updater"
    description: str = "Updates the stock level of a specific item in the inventory. Input is the item name and new quantity."
    args_schema: Type[BaseModel] = UpdateInventorySchema

    def _run(self, item_name: str, quantity: int) -> str:
        time.sleep(0.5)
        if item_name.lower() in _INVENTORY:
            _INVENTORY[item_name.lower()] = quantity
            return f"Updated stock of {item_name} to {quantity}."
        else:
            _INVENTORY[item_name.lower()] = quantity
            return f"Added new item '{item_name}' with quantity {quantity}."

    async def _arun(self, item_name: str, quantity: int) -> str:
        return self._run(item_name, quantity)
# --- End of Tools Definition ---

# Initialize the LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o") # Using gpt-4o for better performance

# Get the prompt for the ReAct agent
prompt = hub.pull("hwchase17/react")

# Create instances of our custom tools
tools = [InventoryCheckerTool(), InventoryUpdaterTool()]

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

print("--- Inventory Agent Ready ---")
print("Initial inventory:", _INVENTORY)

# Interact with the agent
print("\n--- Checking stock for apples ---")
response1 = agent_executor.invoke({"input": "What is the stock level for apples?"})
print(f"Agent's response: {response1['output']}")
print("Current inventory:", _INVENTORY)

print("\n--- Updating stock for bananas ---")
response2 = agent_executor.invoke({"input": "Update bananas stock to 120."})
print(f"Agent's response: {response2['output']}")
print("Current inventory:", _INVENTORY)

print("\n--- Checking stock for oranges ---")
response3 = agent_executor.invoke({"input": "How many oranges do we have?"})
print(f"Agent's response: {response3['output']}")
print("Current inventory:", _INVENTORY)

print("\n--- Adding a new item ---")
response4 = agent_executor.invoke({"input": "Add bread to inventory with 30 units."})
print(f"Agent's response: {response4['output']}")
print("Current inventory:", _INVENTORY)

print("\n--- Checking stock for an unknown item ---")
response5 = agent_executor.invoke({"input": "Check stock for grapes."})
print(f"Agent's response: {response5['output']}")
print("Current inventory:", _INVENTORY)
```

In this example, the agent dynamically chooses to use `inventory_checker` when asked about stock levels and `inventory_updater` when instructed to change stock. The `verbose=True` option shows the agent's "thoughts" and "actions," giving you a peek into its decision-making process. This complete setup truly demonstrates how to `create custom tools langchain agents` and put them to work.

### Best Practices for `create custom tools langchain agents`

To make sure your custom tools are as effective as possible, keep these best practices in mind. They will help you `create custom tools langchain agents` that are reliable and powerful.

#### Clear and Concise Tool Descriptions

Always remember that the agent relies heavily on your tool's description. Spend time crafting `tool description writing` that is:
*   **Specific**: "Adds a new user to the CRM system" is better than "Handles users."
*   **Actionable**: Describe what the tool *does*.
*   **Input-focused**: Mention what inputs the tool expects and in what format.
*   **Outcome-oriented**: Briefly state what the tool returns or achieves.

Avoid vague language. The clearer your description, the better the agent will perform.

#### Granular Tool Design

Design your tools to do one thing and do it well. Avoid creating "Swiss Army knife" tools that try to do too many different things.
*   **Good**: `add_user`, `delete_user`, `update_user_profile`.
*   **Bad**: `manage_users` (which might try to do all of the above based on complex input).

Smaller, focused tools are easier to describe, test, and for the agent to use correctly. If a complex task requires multiple steps, the agent can chain together several small tools.

#### Robust Input Validation

Ensure your tools can handle unexpected or invalid inputs. Use `Pydantic` with `StructuredTool` or `BaseTool` for explicit `tool parameters definition` and validation.
*   Check for required parameters.
*   Validate data types (e.g., ensure a number is actually a number).
*   Check for valid ranges or specific formats (e.g., dates, emails).

This prevents errors within your tool and provides better feedback to the agent, which can then ask the user for clarification.

#### Effective Tool Documentation

Beyond the `description` for the agent, good `tool documentation best practices` are crucial for *you* and *other developers*.
*   **Docstrings**: Use clear Python docstrings for your functions and classes, explaining their purpose, parameters, and return values.
*   **README files**: If you have many tools, a README file in your tools directory can explain the overall purpose and how to set them up.
*   **Examples**: Include small code examples demonstrating how to use your tools directly.

Well-documented tools are easier to maintain, debug, and expand. You can find more comprehensive advice on this topic in [our guide on how to document your Python code effectively](/blog/how-to-document-python-code-effectively).

### Troubleshooting Common Issues

Even with best practices, you might run into problems when you `create custom tools langchain agents`. Here are a couple of common issues and how to fix them.

#### Agent Not Using Your Tool

If your agent seems to ignore your custom tool, consider these points:
*   **Is the description clear enough?** The agent might not understand what your tool does. Rewrite the `tool description writing` to be more precise and action-oriented.
*   **Are the input parameters correctly defined?** If the agent can't figure out how to provide the right inputs, it won't use the tool. Check `tool parameters definition`.
*   **Is the tool actually passed to the agent?** Double-check that your tool is included in the list of tools when you define the `AgentExecutor`.
*   **Is the agent's prompt sufficient?** Sometimes the LLM needs a little more guidance in its system prompt to prefer your tools for certain tasks.
*   **Is your LLM powerful enough?** Simpler LLMs (e.g., older GPT-3.5 models) might struggle more with complex tool use and reasoning. Using a more advanced model like GPT-4 can significantly improve tool usage.

#### Tool Errors Breaking the Agent

If your agent crashes when it tries to use your tool:
*   **Review `tool error handling`**: Make sure your tool functions have `try-except` blocks to catch potential errors. Instead of crashing, they should return an informative string.
*   **Check input validation**: The agent might be sending invalid input to your tool. Ensure your tool checks its inputs and handles bad data gracefully. Using `Pydantic` schemas for `tool parameters definition` is very helpful here.
*   **Inspect logs**: If `verbose=True` is set for your `AgentExecutor`, look at the detailed logs. They often show the exact error message that caused the crash.

### Conclusion

You've learned how to `create custom tools langchain agents`, from simple functions with the `@tool` decorator to advanced `BaseTool inheritance` with structured inputs. You now understand the importance of clear `tool description writing`, robust `tool parameters definition`, and proper `tool error handling`.

By making your own tools, you give your LangChain agents superpowers. They can interact with your unique systems, automate specific workflows, and become truly tailored assistants. Start experimenting with your own ideas, and watch your agents become smarter and more capable! The ability to `create custom tools langchain agents` is a powerful skill for anyone looking to build advanced AI applications.