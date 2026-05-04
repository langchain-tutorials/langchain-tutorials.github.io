---
title: "How to Define Custom Tools for LangChain OpenAI Function Calling with Pydantic"
description: "Unlock advanced AI! Learn to define LangChain custom tools function calling using Pydantic for powerful, type-safe agents. Master your LangChain development ..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain custom tools function calling]
featured: false
image: '/assets/images/langchain-custom-tools-openai-function-calling-pydantic.webp'
---

## How to Define Custom Tools for LangChain OpenAI Function Calling with Pydantic

Imagine you're talking to a super-smart robot, like Iron Man's Jarvis. This robot can answer questions, but what if you want it to *do* things? Maybe you want it to check the weather, send an email, or even search your company's product catalog.

This is where custom tools come in handy for AI models. LangChain helps you give your AI these special abilities, and Pydantic makes sure your tools understand exactly what to do. You'll learn how to build robust LangChain custom tools function calling capabilities.

### What are Custom Tools and Why Do We Need Them?

Think of custom tools as little apps or functions that your AI can use. When you ask your AI to "check the weather in London," it doesn't magically know how to get weather data. It needs a special tool for that job.

LangChain lets you define these tools, giving your AI the power to interact with the real world or specific systems. This process of creating your own tools is called `custom tool definition`. It's a key part of making your AI truly useful beyond just answering questions.

When an AI model, especially one from OpenAI, decides it needs to perform an action, it often uses something called "function calling." This means the AI generates a special message asking to use one of your predefined tools. It will also tell the tool exactly what information it needs, like "London" for the weather tool.

### Understanding OpenAI Function Calling with LangChain

OpenAI's large language models are super good at understanding what you want. When you give them a list of available tools, they can intelligently decide which tool to use. They even figure out what information the tool needs.

LangChain acts like a bridge, making it easy to connect your custom tools with these powerful AI models. It helps the AI understand the `function schema` of your tools. This schema is like a blueprint that describes what your tool does and what inputs it expects.

Without a clear `function schema`, the AI wouldn't know how to use your tools. Pydantic helps us build these clear blueprints, making the whole process smooth. This is essential for effective LangChain custom tools function calling.

### Pydantic: The Secret Ingredient for Clear Tool Definitions

Pydantic is a wonderful Python library that helps you define how data should look. It makes sure that when your AI calls a tool, the information it sends is exactly what the tool expects. This prevents many errors and makes your AI agents more reliable.

When you use Pydantic, you're essentially creating a `Pydantic args schema`. This schema describes the types of inputs your tool needs. For example, if a tool needs a city name, Pydantic ensures it receives a string and not a number.

This strict definition means your tools always get the correct type of information. It also helps LangChain automatically create the `function schema` that OpenAI models understand. You can learn more about building advanced agents with tools in [this post about Google Gemini function calling]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

### Method 1: Defining Custom Tools with the `@tool` Decorator

The simplest way to define a custom tool in LangChain is by using the `@tool` decorator. This is like putting a special label on a regular Python function, telling LangChain, "Hey, this is a tool!"

You simply write a normal Python function, and then add `@tool` right above it. LangChain will then automatically recognize it as a tool. Let's look at an example for our weather tool.

#### Example 1: A Simple Weather Tool using `@tool`

Here’s how you can define a basic weather checking tool. We'll make it print a message for now, but in a real app, it would connect to a weather API. Notice how we describe what the tool does, which becomes its `tool description`.

{% raw %}
```python
from langchain.agents import tool

@tool
def get_current_weather(location: str) -> str:
    """
    Get the current weather for a specified location.
    
    Args:
        location (str): The city and state/country, e.g., "San Francisco, CA"
    """
    if "London" in location:
        return "It's sunny with a slight breeze in London, 15°C."
    elif "Paris" in location:
        return "Cloudy with a chance of rain in Paris, 12°C."
    else:
        return f"Weather data for {location} is not available."

print(get_current_weather("London"))
print(get_current_weather("New York"))
```
{% endraw %}

In this example, `@tool` turns `get_current_weather` into a callable agent tool. The text inside the triple quotes `"""..."""` is crucial as it becomes the `tool description`. This description tells the AI what the tool does.

The `location: str` part is a type hint, telling Python and LangChain that `location` should be a string. LangChain uses this hint to build the `function schema` for the OpenAI model. This is a very straightforward way to create a `custom tool definition`.

### Method 2: Defining Custom Tools as Pydantic Models (Class-Based)

Sometimes your tools need more complex inputs than just a single string. Or maybe you want more control over how the tool's inputs are defined and validated. This is where using Pydantic models directly becomes very powerful.

When you use a Pydantic model, you define a class that inherits from `BaseModel`. Inside this class, you list all the arguments your tool expects, along with their types and even default values. LangChain will use this `Pydantic args schema` to understand your tool's inputs.

#### Example 2: A Product Search Tool with Multiple Parameters

Let's imagine we have a tool to search for products in an online store. This tool might need a search query, a maximum price, and a category. Defining this with a simple `@tool` might be messy for the AI to understand the arguments clearly.

Using a Pydantic model for the `Pydantic args schema` makes it very clear what inputs are needed. It also allows for more advanced validation.

First, we define our Pydantic model for the tool's inputs:

{% raw %}
```python
from pydantic import BaseModel, Field

class ProductSearchInput(BaseModel):
    """Input for searching products in an online store."""
    query: str = Field(description="The search term for the product, e.g., 'smartphone'")
    max_price: float = Field(default=None, description="Maximum price for the product (optional)")
    category: str = Field(default="electronics", description="Category to search within, defaults to 'electronics'")

# You can test the Pydantic model directly
try:
    search_params = ProductSearchInput(query="laptop", max_price=1200.0)
    print(search_params.model_dump_json(indent=2))

    invalid_params = ProductSearchInput(query="monitor", max_price="expensive")
except Exception as e:
    print(f"\nCaught expected error for invalid input: {e}")
```
{% endraw %}

Notice how we use `Field` from Pydantic to add descriptions to each parameter. This is incredibly helpful for the `tool description` that the AI sees. It clarifies what each input means.

Now, let's create the actual tool function that uses this `ProductSearchInput` model:

{% raw %}
```python
from langchain.tools import BaseTool
from typing import Type

class ProductSearchTool(BaseTool):
    name: str = "product_search"
    description: str = "Searches for products in an online store with specified query, max price, and category."
    args_schema: Type[BaseModel] = ProductSearchInput

    def _run(self, query: str, max_price: float = None, category: str = "electronics") -> str:
        """
        Use the tool to search for products.
        In a real application, this would call an external API.
        """
        print(f"DEBUG: Searching for '{query}' in category '{category}' with max price '{max_price}'")
        if query == "smartphone" and category == "electronics":
            if max_price and max_price < 500:
                return "Found 'Budget Smartphone X' for $399 and 'Value Phone Y' for $299."
            return "Found 'Flagship Smartphone Z' for $999 and 'Mid-range Phone A' for $600."
        elif query == "laptop" and category == "electronics":
            if max_price and max_price < 1000:
                return "Found 'Student Laptop Pro' for $850."
            return "Found 'Gaming Laptop Extreme' for $1800 and 'Ultrabook Pro' for $1300."
        else:
            return f"No products found matching '{query}' in category '{category}'."

    async def _arun(self, query: str, max_price: float = None, category: str = "electronics") -> str:
        """Asynchronous version of the tool."""
        # For simplicity, we'll just call the synchronous version
        return self._run(query, max_price, category)

# Example of how to use this tool directly (without an agent)
product_tool = ProductSearchTool()
print(product_tool.run(query="smartphone", max_price=700.0, category="electronics"))
print(product_tool.run(query="laptop", category="electronics"))
print(product_tool.run(query="socks", category="clothing"))
```
{% endraw %}

Here, `ProductSearchTool` inherits from `BaseTool`. We explicitly define its `name` and `description`. Crucially, `args_schema: Type[BaseModel] = ProductSearchInput` tells LangChain to use our Pydantic model for the tool's input structure. The `_run` method is where the actual logic of your tool lives. This `custom tool definition` offers a powerful way to manage complex inputs.

### Integrating Custom Tools with LangChain Agents and OpenAI Models

Once you've defined your `LangChain custom tools function calling` capabilities, the next step is to let your AI agent use them. LangChain makes this very straightforward by allowing you to pass a list of your tools to the agent. The agent, powered by an OpenAI model, will then decide when and how to use them.

You'll typically set up an OpenAI model (like `gpt-4` or `gpt-3.5-turbo`) and then create an agent that understands how to use functions. The agent will then observe user inputs, check its available tools, and choose the best one.

#### Example 3: Building an Agent that Uses Our Custom Tools

Let's bring our `get_current_weather` and `ProductSearchTool` together with an OpenAI agent. This agent will now be able to answer questions about weather and search for products.

First, make sure you have your OpenAI API key set up.

{% raw %}
```python
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Assuming get_current_weather and ProductSearchTool definitions are available from above
# Let's redefine them here for a complete runnable example
from langchain.agents import tool
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

@tool
def get_current_weather(location: str) -> str:
    """
    Get the current weather for a specified location.
    
    Args:
        location (str): The city and state/country, e.g., "San Francisco, CA"
    """
    if "London" in location:
        return "It's sunny with a slight breeze in London, 15°C."
    elif "Paris" in location:
        return "Cloudy with a chance of rain in Paris, 12°C."
    else:
        return f"Weather data for {location} is not available."

class ProductSearchInput(BaseModel):
    """Input for searching products in an online store."""
    query: str = Field(description="The search term for the product, e.g., 'smartphone'")
    max_price: float = Field(default=None, description="Maximum price for the product (optional)")
    category: str = Field(default="electronics", description="Category to search within, defaults to 'electronics'")

class ProductSearchTool(BaseTool):
    name: str = "product_search"
    description: str = "Searches for products in an online store with specified query, max price, and category."
    args_schema: Type[BaseModel] = ProductSearchInput

    def _run(self, query: str, max_price: float = None, category: str = "electronics") -> str:
        """
        Use the tool to search for products.
        In a real application, this would call an external API.
        """
        print(f"DEBUG: Searching for '{query}' in category '{category}' with max price '{max_price}'")
        if query == "smartphone" and category == "electronics":
            if max_price and max_price < 500:
                return "Found 'Budget Smartphone X' for $399 and 'Value Phone Y' for $299."
            return "Found 'Flagship Smartphone Z' for $999 and 'Mid-range Phone A' for $600."
        elif query == "laptop" and category == "electronics":
            if max_price and max_price < 1000:
                return "Found 'Student Laptop Pro' for $850."
            return "Found 'Gaming Laptop Extreme' for $1800 and 'Ultrabook Pro' for $1300."
        else:
            return f"No products found matching '{query}' in category '{category}'."

    async def _arun(self, query: str, max_price: float = None, category: str = "electronics") -> str:
        """Asynchronous version of the tool."""
        return self._run(query, max_price, category)

# Initialize the OpenAI model
# Make sure to set your OPENAI_API_KEY environment variable
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create a list of our custom tools
tools = [get_current_weather, ProductSearchTool()]

# Define the prompt for the agent
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that can check weather and search for products."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the OpenAI functions agent
agent = create_openai_functions_agent(llm, tools, prompt)

# Create the AgentExecutor to run the agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Let's test our agent!
print("\n--- Agent Conversation 1: Weather ---")
response1 = agent_executor.invoke({"input": "What's the weather like in London?"})
print(response1["output"])

print("\n--- Agent Conversation 2: Product Search ---")
response2 = agent_executor.invoke({"input": "Find me a smartphone under $500."})
print(response2["output"])

print("\n--- Agent Conversation 3: Product Search with category ---")
response3 = agent_executor.invoke({"input": "I need a new laptop, preferably under $1000."})
print(response3["output"])

print("\n--- Agent Conversation 4: General Question ---")
response4 = agent_executor.invoke({"input": "What is the capital of France?"})
print(response4["output"])
```
{% endraw %}

In this code, we first set up our `ChatOpenAI` model. Then, we gather all our custom tools into a list. The `create_openai_functions_agent` function takes our `llm`, `tools`, and a `prompt` to build the agent.

The `AgentExecutor` is what actually runs the agent, processing inputs and using the tools as needed. When you run this, you'll see the agent's thought process, including when it decides to call `get_current_weather` or `product_search` based on your questions. This demonstrates effective `LangChain custom tools function calling`.

### Advanced Custom Tool Definition Concepts

As you become more comfortable with basic `custom tool definition`, you might want to explore more advanced features. Pydantic offers many ways to make your `Pydantic args schema` even more robust.

#### Handling Optional Parameters and Default Values

You've already seen `max_price: float = Field(default=None, description="...")` in `ProductSearchInput`. This tells Pydantic that `max_price` is optional and will be `None` if not provided. This helps the AI understand which parameters it doesn't *have* to provide.

#### Using Enums for Constrained Choices

What if your tool can only accept a specific set of values for an input? For example, a `priority` for a task could only be "low," "medium," or "high." Pydantic allows you to use Python's `Enum` to enforce this.

{% raw %}
```python
from enum import Enum
from pydantic import BaseModel, Field

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CreateTaskInput(BaseModel):
    """Input for creating a new task."""
    task_name: str = Field(description="The name or description of the task.")
    priority: Priority = Field(default=Priority.MEDIUM, description="The priority level of the task (low, medium, high).")
    due_date: str = Field(default=None, description="Optional due date for the task (YYYY-MM-DD format).")

@tool
def create_task(task_name: str, priority: Priority = Priority.MEDIUM, due_date: str = None) -> str:
    """
    Creates a new task with a given name, priority, and optional due date.
    
    Args:
        task_name (str): The name of the task.
        priority (Priority): The priority of the task.
        due_date (str): The due date of the task.
    """
    return f"Task '{task_name}' created with priority '{priority.value}' and due date '{due_date or 'none'}'. (Mock)"

# Test the tool directly
print(create_task("Review blog post", priority=Priority.HIGH))
print(create_task("Schedule meeting", due_date="2026-05-15"))
```
{% endraw %}

By using `Priority` (an Enum) as the type hint for `priority`, you guide the AI. It will understand that it should pick one of the defined values for this parameter. This creates a very precise `function schema`.

#### Asynchronous Tools

For tools that might take a long time to complete (like making a network request), it's often better to define them as asynchronous functions. This allows your agent to do other things while waiting for the tool to finish.

You define `_arun` instead of `_run` in `BaseTool` when you want an asynchronous tool. Our `ProductSearchTool` example already included an `_arun` method.

{% raw %}
```python
import asyncio
from langchain.tools import BaseTool

class AsyncExampleTool(BaseTool):
    name: str = "async_example"
    description: str = "An example of an asynchronous tool that simulates a delay."
    
    def _run(self, duration: int) -> str:
        raise NotImplementedError("AsyncExampleTool does not support synchronous run.")

    async def _arun(self, duration: int) -> str:
        """Simulates an asynchronous operation with a delay."""
        print(f"Async tool started, waiting for {duration} seconds...")
        await asyncio.sleep(duration)
        print(f"Async tool finished after {duration} seconds.")
        return f"Simulated async operation completed in {duration} seconds."

# To run an async tool, you typically need an event loop
async def run_async_tool():
    async_tool = AsyncExampleTool()
    result = await async_tool.arun(3)
    print(result)

# asyncio.run(run_async_tool()) # Uncomment to run
```
{% endraw %}

When the agent uses an `async` tool, LangChain will automatically call its `_arun` method. This is important for building high-performance AI agents.

### Best Practices for LangChain Custom Tools Function Calling

To make your AI agents as effective as possible, follow these best practices when defining your custom tools. Good `custom tool definition` is key to success.

*   **Clear and Concise `tool description`:** This is perhaps the most critical part. The AI model relies heavily on the `tool description` to understand *when* to use your tool and *what* it does. Be precise and clear.
    *   **Bad:** "A tool for data."
    *   **Good:** "Retrieves the latest stock price for a given company ticker symbol."
*   **Granular Tools:** Break down complex tasks into smaller, more focused tools. Instead of one "CRM management" tool, have separate tools for "create_contact," "update_contact," and "find_contact." This gives the AI more flexibility.
*   **Meaningful Parameter Names:** Use descriptive names for your function arguments (e.g., `city_name` instead of `c`). This also contributes to a clearer `Pydantic args schema`.
*   **Add Descriptions to Pydantic Fields:** As shown with `Field(description="...")`, add descriptions to individual parameters within your Pydantic models. This provides even more detail to the AI.
*   **Error Handling within Tools:** Your tools should gracefully handle errors (e.g., API failures, invalid inputs from external systems). Return helpful error messages to the AI so it can inform the user or try a different approach.
*   **Testing Your Custom Tools:** Before integrating with an agent, test your tools directly in Python. Make sure they work as expected with various inputs.
*   **Security Considerations:** If your tools interact with sensitive systems or data, consider authentication, authorization, and input sanitization. Never expose raw API keys directly in client-side code.
*   **Version Control:** Like any other code, keep your `custom tool definition` under version control.
*   **Reusability:** Design tools that can be reused across different agents or applications. For more about agent design, you might find [this post on building multi-step AI agents with LangGraph]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}) helpful.

### Troubleshooting Common Issues

Even with the best practices, you might run into problems. Here are some common issues and how to fix them for `LangChain custom tools function calling`.

*   **Tool Not Being Called:**
    *   **Check `tool description`:** Is it clear enough for the AI to understand its purpose?
    *   **Check `Pydantic args schema`:** Does the schema accurately reflect the arguments the AI is likely to provide? Are there missing or confusing parameters?
    *   **Prompt:** Is your agent's system prompt guiding it to use tools? Sometimes you need to explicitly tell the agent, "You have access to these tools..."
    *   **LLM Model:** Some older or less capable LLM models are not as good at function calling. Ensure you're using a capable OpenAI model (e.g., `gpt-3.5-turbo`, `gpt-4`).
*   **Incorrect Arguments Passed to Tool:**
    *   **Pydantic Validation Errors:** If you see Pydantic validation errors, it means the AI tried to pass data that didn't match your `Pydantic args schema`. Review your `BaseModel` definitions.
    *   **Type Mismatches:** Did the AI try to send a string when you expected an integer, or vice versa? Make sure your type hints are correct.
*   **Tool Called But Returns Generic Error:**
    *   This usually means your tool's internal logic failed. Add more `print` statements or logging inside your tool's `_run` (or `_arun`) method to debug.
    *   Check for external API call failures if your tool connects to other services.

### Real-World Use Cases for Custom Tools

The ability to define custom tools opens up a world of possibilities for your LangChain applications. Here are just a few real-world examples of how `LangChain custom tools function calling` can be applied:

*   **Connecting to Databases:**
    *   Tools to query SQL databases (e.g., `get_customer_info(customer_id: str)`).
    *   Tools to update records (e.g., `update_order_status(order_id: str, new_status: str)`).
*   **Making API Calls to External Services:**
    *   Integrating with e-commerce platforms (our `ProductSearchTool` is a good example).
    *   Connecting to CRM systems (e.g., `create_lead(name: str, email: str)`).
    *   Accessing financial data APIs (e.g., `get_stock_quote(ticker: str)`).
    *   Managing calendars or scheduling (e.g., `create_calendar_event(title: str, start_time: str, end_time: str)`).
*   **Performing Complex Calculations:**
    *   Tools for specific mathematical functions (e.g., `calculate_compound_interest(principal, rate, years)`).
    *   Tools for data analysis or statistical operations that are too complex for the LLM to do itself.
*   **Interacting with Internal Systems:**
    *   Triggering workflows in an internal system (e.g., `approve_expense_report(report_id: str)`).
    *   Retrieving internal documentation from a knowledge base. You could even integrate with a RAG system by having a tool that performs a specific type of search, similar to what's discussed in [this article on building RAG applications with LangChain vector stores]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).
*   **Sending Notifications:**
    *   Tools to send emails (e.g., `send_email(recipient: str, subject: str, body: str)`).
    *   Tools to send messages via Slack, Teams, or other messaging platforms.

By leveraging these types of tools, your AI agents can move beyond just answering questions. They can become proactive assistants that perform actions and automate tasks.

### Conclusion

You've learned how to empower your LangChain agents by defining `LangChain custom tools function calling` capabilities using Pydantic. We covered both the simple `@tool` decorator for straightforward functions and the more powerful class-based approach with Pydantic models for complex `Pydantic args schema`.

Understanding how to craft a precise `tool description` and a robust `function schema` is vital. Pydantic makes sure your tools are reliable, preventing errors and ensuring smooth communication between your AI and the functions it can call.

Now you have the knowledge to build incredibly powerful and useful AI agents. Go ahead and start experimenting with your own `custom tool definition`! The more tools you give your AI, the more intelligent and helpful it can become.