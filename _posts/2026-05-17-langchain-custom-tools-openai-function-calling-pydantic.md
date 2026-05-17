---
title: "How to Define Custom Tools for LangChain OpenAI Function Calling with Pydantic"
description: "Master defining LangChain custom tools for function calling with Pydantic. Unlock powerful AI capabilities and build advanced applications efficiently."
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

Imagine you have a super smart computer brain, like an AI, that can talk to you. This brain is very good at understanding your words and generating text. But what if it needs to do more than just talk?

What if it needs to check the weather, book a calendar appointment, or search for information online? That's where "tools" come in, and LangChain helps your AI brain use these tools. We're going to learn how to make these special tools for your AI.

### What are Custom Tools and Why Does Your AI Need Them?

Think of custom tools as special gadgets your AI can use to interact with the real world or get up-to-date information. Without these tools, your AI is stuck with only what it learned during its training. This means it can't know about today's weather or your friend's new phone number.

LangChain helps your AI decide when and how to use these gadgets. It's like giving your AI a toolbox and teaching it which wrench to use for which task. We'll focus on `LangChain custom tools function calling` specifically for OpenAI models.

OpenAI models have a cool ability called "function calling," which lets them understand when they need a tool and what information to send to it. This makes your AI much more powerful and useful. You can unlock many new possibilities for your AI applications.

### Understanding How AI Models "Call Functions"

When you talk to an AI model, sometimes it realizes it needs more information or needs to perform an action. For example, if you ask "What's the weather like in London tomorrow?", the AI knows it can't just guess the answer. It needs to look it up.

This is where "function calling" happens. The AI doesn't *do* the looking up itself; instead, it cleverly figures out which tool it needs and what information to give that tool. It then tells LangChain: "Hey, I need to call the 'weather tool' for 'London' and 'tomorrow'." LangChain then runs the tool and gives the result back to the AI.

This process is super important for building dynamic and helpful AI agents. It allows the AI to extend its capabilities far beyond just generating text. Your AI can then fetch real-time data or even trigger external actions.

### LangChain's Role in Empowering Your AI with Tools

LangChain acts like the manager of your AI's toolbox. It provides a simple way to create, organize, and use these `custom tool definition`s. Without LangChain, connecting your AI to external functions would be much harder.

It takes your Python functions and turns them into something the AI can understand and use. This framework makes it easy to add new capabilities to your AI agent. You can read more about building AI agents with custom tools in this guide: [Building AI Agents with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

LangChain handles the tricky parts, letting you focus on what your tools actually do. It bridges the gap between your AI model's thinking and the real-world actions or data it needs.

### Why Pydantic is Your Best Friend for Defining Tool Inputs

So, your AI knows it needs a tool, and it knows *which* tool. But how does it know *what kind of information* that tool needs? This is where Pydantic comes into play. Pydantic is a library that helps you define how data should look.

Imagine you have a tool that needs a city name and a temperature unit (like Celsius or Fahrenheit). Pydantic lets you say, "Okay, this tool needs a 'city' which must be text, and a 'unit' which must be either 'Celsius' or 'Fahrenheit'." It's like creating a clear instruction manual for the AI. This detailed instruction manual is called a `Pydantic args schema`.

Using Pydantic means that when your AI decides to use a tool, it will automatically try to provide arguments that match your defined structure. This helps prevent errors and ensures your tools get the correct information every time. It's a fantastic way to make your tool inputs clear and robust.

### Defining Your First Custom Tool: A Simple Start

Let's begin by creating a very basic tool. We will start with a simple Python function, then make it a LangChain tool. This will show you the core idea behind `custom tool definition`.

#### Basic Tool Structure with the `@tool` Decorator

In LangChain, you can turn any Python function into a tool using a special tag called an `@tool decorator`. This decorator tells LangChain, "Hey, this function here is a tool that my AI can use." It's like putting a label on your gadget.

The decorator also lets you add a `tool description`. This description is super important because it's how the AI understands what your tool does. A good description helps the AI decide when to use your tool and how.

Here's an example of a very simple tool that just adds two numbers. Notice how the `tool description` explains its purpose clearly.

{% raw %}
```python
from langchain_core.tools import tool

@tool
def add_numbers(a: float, b: float) -> float:
    """Adds two floating-point numbers together and returns their sum.
    This tool is useful for basic arithmetic operations.
    """
    return a + b

# You can now see the tool's description and name
print(f"Tool Name: {add_numbers.name}")
print(f"Tool Description: {add_numbers.description}")
print(f"Tool Args Schema: {add_numbers.args}")
```
{% endraw %}

In this example, the `add_numbers` function becomes a tool. The `description` tells the AI exactly what it does. The `args` part shows that it expects two numbers, `a` and `b`.

### Introducing Pydantic for Detailed Input Schemas

While the previous example worked, it didn't strictly enforce the *type* of `a` and `b` in a way that's easily understandable by an AI model for function calling. This is where Pydantic shines. It allows us to create a formal `Pydantic args schema` for our tool's inputs.

Imagine you have a tool to get specific information about a user. It needs their ID and maybe their name. Pydantic helps you define these inputs very clearly. We create a Pydantic class that inherits from `BaseModel`.

This `BaseModel` from Pydantic is like a blueprint for the arguments your tool expects. It ensures that the arguments provided by the AI match exactly what your tool needs, including their types. Let's make a Pydantic class for our weather tool.

{% raw %}
```python
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    """Input for the weather tool."""
    city: str = Field(description="The name of the city to get weather for, e.g., 'New York'.")
    unit: str = Field(description="The unit for temperature, 'celsius' or 'fahrenheit'.")
```
{% endraw %}

In this `WeatherInput` class, we've defined that our weather tool needs two things: `city` (which must be a string) and `unit` (also a string). The `Field` descriptions are crucial for the AI, as they guide it on what kind of values to provide. This clarity in the `Pydantic args schema` helps the AI generate correct inputs.

#### The `@tool` Decorator with Pydantic `args_schema`

Now we combine our `@tool decorator` with the `Pydantic args schema` we just created. This tells LangChain and the OpenAI model exactly what to expect. The `args_schema` parameter in the `@tool` decorator points to our Pydantic class.

When you use the `args_schema` with the `@tool decorator`, LangChain automatically converts your Pydantic model into a `function schema` that OpenAI understands. This `function schema` is a JSON description of your tool's name, description, and required inputs. It's the language the AI speaks to understand your tool.

Let's make our weather tool using Pydantic:

{% raw %}
```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import random

# Our Pydantic input schema
class WeatherInput(BaseModel):
    """Input for the weather tool."""
    city: str = Field(description="The name of the city to get weather for, e.g., 'London'.")
    unit: str = Field(description="The unit for temperature, 'celsius' or 'fahrenheit'. Must be 'celsius' or 'fahrenheit'.")

@tool(args_schema=WeatherInput)
def get_current_weather(city: str, unit: str) -> str:
    """Get the current weather for a specific city.
    This tool is useful for fetching real-time weather information.
    """
    if unit.lower() not in ["celsius", "fahrenheit"]:
        return "Error: Unit must be 'celsius' or 'fahrenheit'."

    # Simulate fetching weather data
    temperature = random.randint(0, 30) if unit.lower() == "celsius" else random.randint(32, 86)
    conditions = random.choice(["sunny", "cloudy", "rainy", "stormy"])
    return f"The current weather in {city} is {temperature}°{unit.capitalize()} and {conditions}."

# Let's inspect the tool's definition that LangChain generates
print(f"Tool Name: {get_current_weather.name}")
print(f"Tool Description: {get_current_weather.description}")
print(f"Tool Args Schema (raw Pydantic): {get_current_weather.args_schema.schema_json(indent=2)}")
print("\n--- Example of the function schema passed to OpenAI (simplified) ---")
print({
    "name": get_current_weather.name,
    "description": get_current_weather.description,
    "parameters": get_current_weather.args_schema.schema() # This is the JSON schema OpenAI uses
})
```
{% endraw %}

Notice how the `args_schema=WeatherInput` connects our Pydantic blueprint to the `@tool` decorator. The output shows the detailed `function schema` including `name`, `description`, and `parameters` (derived from our Pydantic model), which is what OpenAI sees. This combination is the core of `LangChain custom tools function calling`.

### Building Practical Custom Tools with Pydantic

Now that you understand the basics, let's create a few more practical tools. These examples will show how versatile this approach is for different scenarios. Each tool will have its own clear `Pydantic args schema` and `tool description`.

#### Example 1: A "Search Wikipedia" Tool

Imagine your AI needs to answer questions about historical events or famous people. It doesn't have all this information built-in from its training data. A Wikipedia search tool would be perfect for this!

We'll define an input schema for the search query and a simple function to simulate searching Wikipedia. This tool demonstrates how to fetch external, up-to-date information.

{% raw %}
```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# 1. Define the Pydantic args schema for the Wikipedia search tool
class WikipediaSearchInput(BaseModel):
    """Input for searching Wikipedia."""
    query: str = Field(description="The search query for Wikipedia, e.g., 'Eiffel Tower history'.")
    results_count: int = Field(default=1, description="Number of search results to return (max 3).")

# 2. Define the custom tool using the @tool decorator and Pydantic schema
@tool(args_schema=WikipediaSearchInput)
def search_wikipedia(query: str, results_count: int = 1) -> str:
    """Searches Wikipedia for a given query and returns a summary of the top results.
    This tool is useful for retrieving factual information and background details on various topics.
    """
    if not (1 <= results_count <= 3):
        return "Error: results_count must be between 1 and 3."

    # Simulate a Wikipedia search result
    mock_results = {
        "Eiffel Tower": "The Eiffel Tower is an iron lattice tower on the Champ de Mars in Paris, France. It was constructed from 1887 to 1889 as the entrance to the 1889 World's Fair.",
        "Quantum Physics": "Quantum physics is the study of matter and energy at the most fundamental level. It aims to uncover the properties and behaviors of the very building blocks of nature.",
        "History of AI": "The history of artificial intelligence (AI) began in antiquity, with myths, stories and rumors of artificial beings endowed with intelligence or consciousness by master craftsmen.",
        "Mars exploration": "Mars exploration is the investigation of Mars by astronautical engineering. It involves sending robotic spacecraft to orbit Mars, land on its surface, or even rove across it."
    }

    found_results = [
        desc for topic, desc in mock_results.items() if query.lower() in topic.lower() or query.lower() in desc.lower()
    ]

    if not found_results:
        return f"No relevant Wikipedia results found for '{query}'."

    output = ""
    for i, res in enumerate(found_results[:results_count]):
        output += f"Result {i+1}: {res}\n"
    return output.strip()

# Example usage (for testing the tool directly)
# print(search_wikipedia(query="Eiffel Tower", results_count=1))
# print(search_wikipedia(query="AI history", results_count=2))
```
{% endraw %}

This `search_wikipedia` tool can now be presented to an AI. When the AI gets a question like "Tell me about the Eiffel Tower," it can use this tool, providing "Eiffel Tower" as the `query`. The clear `tool description` and `Pydantic args schema` guide the AI perfectly.

#### Example 2: A "Calendar Event Creator" Tool

What if your AI needs to help you manage your schedule? A tool that can create calendar events would be incredibly useful. This example shows how to handle multiple, more complex inputs, like dates and times.

The `Pydantic args schema` for this tool will include fields like `title`, `date`, `time`, and `duration`. This allows the AI to gather all necessary details from your conversation before attempting to create the event.

{% raw %}
```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

# 1. Define the Pydantic args schema for the calendar event tool
class CreateEventInput(BaseModel):
    """Input for creating a calendar event."""
    title: str = Field(description="The title of the event, e.g., 'Team Meeting'.")
    date: str = Field(description="The date of the event in YYYY-MM-DD format, e.g., '2026-07-20'.")
    time: str = Field(description="The start time of the event in HH:MM format (24-hour), e.g., '14:30'.")
    duration_hours: float = Field(default=1.0, description="The duration of the event in hours, e.g., 1.5 for 1 hour 30 minutes.")
    attendees: list[str] = Field(default=[], description="List of email addresses of attendees, e.g., ['john@example.com', 'jane@example.com'].")

# 2. Define the custom tool using the @tool decorator and Pydantic schema
@tool(args_schema=CreateEventInput)
def create_calendar_event(
    title: str,
    date: str,
    time: str,
    duration_hours: float = 1.0,
    attendees: list[str] = None
) -> str:
    """Creates a new calendar event with the specified details.
    This tool is useful for scheduling meetings, appointments, or reminders.
    """
    try:
        start_datetime_str = f"{date} {time}"
        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(hours=duration_hours)

        attendees_str = ", ".join(attendees) if attendees else "No specific attendees"

        return (f"Calendar event '{title}' successfully created:\n"
                f"  Start: {start_datetime.strftime('%Y-%m-%d %H:%M')}\n"
                f"  End: {end_datetime.strftime('%Y-%m-%d %H:%M')}\n"
                f"  Duration: {duration_hours} hours\n"
                f"  Attendees: {attendees_str}")
    except ValueError as e:
        return f"Error creating event: Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example usage (for testing the tool directly)
# print(create_calendar_event(
#     title="Project Sync-up",
#     date="2026-08-15",
#     time="10:00",
#     duration_hours=0.5,
#     attendees=["alice@example.com"]
# ))
```
{% endraw %}

This tool handles date and time parsing, and even a list of attendees, thanks to the robust `Pydantic args schema`. The AI will naturally ask clarifying questions if it doesn't have all the required information, guided by our `tool description` and input definitions. This makes `LangChain custom tools function calling` powerful for task automation.

#### Example 3: A "Product Recommender" Tool

Let's imagine you're building an AI assistant for an online store. It needs to recommend products to users based on their preferences. This tool can simulate looking up products in a catalog.

The `Pydantic args schema` will include parameters for `product_type`, `min_price`, and `max_price`. This allows for flexible searches based on user input.

{% raw %}
```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import random

# 1. Define the Pydantic args schema for the product recommender tool
class ProductRecommendationInput(BaseModel):
    """Input for recommending products."""
    product_type: str = Field(description="The type of product to recommend, e.g., 'laptop', 'smartphone', 'headset'.")
    min_price: float = Field(default=0.0, description="Minimum price for the recommended product.")
    max_price: float = Field(default=1000.0, description="Maximum price for the recommended product.")
    limit: int = Field(default=3, description="Maximum number of recommendations to return (max 5).")

# 2. Define the custom tool using the @tool decorator and Pydantic schema
@tool(args_schema=ProductRecommendationInput)
def recommend_products(
    product_type: str,
    min_price: float = 0.0,
    max_price: float = 1000.0,
    limit: int = 3
) -> str:
    """Recommends products based on type and price range.
    This tool is useful for assisting users in finding suitable products from a catalog.
    """
    if not (1 <= limit <= 5):
        return "Error: limit must be between 1 and 5."

    mock_products = {
        "laptop": [
            {"name": "UltraBook Pro", "price": 1200, "specs": "16GB RAM, 512GB SSD"},
            {"name": "Gaming Beast X", "price": 1800, "specs": "RTX 4070, 32GB RAM"},
            {"name": "Budget Laptop Lite", "price": 500, "specs": "8GB RAM, 256GB SSD"},
            {"name": "Workstation Master", "price": 2500, "specs": "Intel i9, 64GB RAM"}
        ],
        "smartphone": [
            {"name": "Phone X", "price": 800, "specs": "6.1-inch OLED, 128GB"},
            {"name": "Budget Android", "price": 300, "specs": "6.5-inch LCD, 64GB"},
            {"name": "Flagship Pro", "price": 1100, "specs": "6.7-inch AMOLED, 256GB"}
        ],
        "headset": [
            {"name": "Noise Cancelling Buds", "price": 150, "specs": "Bluetooth 5.2, 24hr battery"},
            {"name": "Gaming Headset RGB", "price": 100, "specs": "7.1 Surround, USB-C"},
            {"name": "Basic Earphones", "price": 30, "specs": "Wired, good for calls"}
        ]
    }

    matching_products = []
    if product_type.lower() in mock_products:
        for product in mock_products[product_type.lower()]:
            if min_price <= product["price"] <= max_price:
                matching_products.append(product)

    if not matching_products:
        return f"No {product_type}s found in the price range ${min_price:.2f}-${max_price:.2f}."

    random.shuffle(matching_products) # Shuffle to give varied recommendations
    recommendations = matching_products[:limit]

    output = f"Here are some {product_type} recommendations:\n"
    for i, rec in enumerate(recommendations):
        output += (f"  {i+1}. {rec['name']} - ${rec['price']:.2f} ({rec['specs']})\n")
    return output.strip()

# Example usage (for testing the tool directly)
# print(recommend_products(product_type="laptop", min_price=500, max_price=1500, limit=2))
# print(recommend_products(product_type="smartphone", max_price=700))
```
{% endraw %}

This `recommend_products` tool allows the AI to respond intelligently to user queries like "Show me some cheap smartphones" or "I need a gaming laptop under $2000." The `Pydantic args schema` handles the price ranges and limits gracefully. This flexibility is key to effective `LangChain custom tools function calling`.

### Integrating Tools with OpenAI Function Calling Agents

Now that we have our custom tools, the next step is to give them to an AI agent. An agent is a special type of AI program that can reason, plan, and use tools to achieve a goal. LangChain provides excellent support for building these agents.

We'll use an OpenAI model and tell it about our tools. The model will then decide which tool to use, if any, based on the user's input. This is where the magic of `LangChain custom tools function calling` truly comes alive.

#### Setting up Your OpenAI Model and Agent

First, you need to import the necessary components from LangChain and set up your OpenAI API key. Remember to replace `"YOUR_OPENAI_API_KEY"` with your actual key. We'll then create an OpenAI chat model.

After that, we'll gather all our custom tools into a list. This list is then given to the `create_tool_calling_agent` function. This agent will use the tools to figure out how to respond to your questions. You can learn more about building robust AI agents in this detailed guide: [Building AI Agents with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

{% raw %}
```python
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Make sure you have your OpenAI API key set as an environment variable
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # Uncomment and set your key if not already set

# 1. Initialize your OpenAI Chat Model
# We'll use a powerful model like GPT-4 or GPT-3.5 Turbo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) # Or "gpt-3.5-turbo"

# 2. Collect all your custom tools
# (Assuming you have defined get_current_weather, search_wikipedia, create_calendar_event, recommend_products)
# Let's re-import them or define them here for completeness
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import random
from datetime import datetime, timedelta

class WeatherInput(BaseModel):
    """Input for the weather tool."""
    city: str = Field(description="The name of the city to get weather for, e.g., 'London'.")
    unit: str = Field(description="The unit for temperature, 'celsius' or 'fahrenheit'. Must be 'celsius' or 'fahrenheit'.")

@tool(args_schema=WeatherInput)
def get_current_weather(city: str, unit: str) -> str:
    """Get the current weather for a specific city.
    This tool is useful for fetching real-time weather information.
    """
    if unit.lower() not in ["celsius", "fahrenheit"]:
        return "Error: Unit must be 'celsius' or 'fahrenheit'."
    temperature = random.randint(0, 30) if unit.lower() == "celsius" else random.randint(32, 86)
    conditions = random.choice(["sunny", "cloudy", "rainy", "stormy"])
    return f"The current weather in {city} is {temperature}°{unit.capitalize()} and {conditions}."

class WikipediaSearchInput(BaseModel):
    """Input for searching Wikipedia."""
    query: str = Field(description="The search query for Wikipedia, e.g., 'Eiffel Tower history'.")
    results_count: int = Field(default=1, description="Number of search results to return (max 3).")

@tool(args_schema=WikipediaSearchInput)
def search_wikipedia(query: str, results_count: int = 1) -> str:
    """Searches Wikipedia for a given query and returns a summary of the top results.
    This tool is useful for retrieving factual information and background details on various topics.
    """
    if not (1 <= results_count <= 3):
        return "Error: results_count must be between 1 and 3."
    mock_results = {
        "Eiffel Tower": "The Eiffel Tower is an iron lattice tower on the Champ de Mars in Paris, France. It was constructed from 1887 to 1889 as the entrance to the 1889 World's Fair.",
        "Quantum Physics": "Quantum physics is the study of matter and energy at the most fundamental level. It aims to uncover the properties and behaviors of the very building blocks of nature.",
    }
    found_results = [
        desc for topic, desc in mock_results.items() if query.lower() in topic.lower() or query.lower() in desc.lower()
    ]
    if not found_results:
        return f"No relevant Wikipedia results found for '{query}'."
    output = ""
    for i, res in enumerate(found_results[:results_count]):
        output += f"Result {i+1}: {res}\n"
    return output.strip()

class CreateEventInput(BaseModel):
    """Input for creating a calendar event."""
    title: str = Field(description="The title of the event, e.g., 'Team Meeting'.")
    date: str = Field(description="The date of the event in YYYY-MM-DD format, e.g., '2026-07-20'.")
    time: str = Field(description="The start time of the event in HH:MM format (24-hour), e.g., '14:30'.")
    duration_hours: float = Field(default=1.0, description="The duration of the event in hours, e.g., 1.5 for 1 hour 30 minutes.")
    attendees: list[str] = Field(default=[], description="List of email addresses of attendees, e.g., ['john@example.com', 'jane@example.com'].")

@tool(args_schema=CreateEventInput)
def create_calendar_event(
    title: str,
    date: str,
    time: str,
    duration_hours: float = 1.0,
    attendees: list[str] = None
) -> str:
    """Creates a new calendar event with the specified details.
    This tool is useful for scheduling meetings, appointments, or reminders.
    """
    try:
        start_datetime_str = f"{date} {time}"
        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + timedelta(hours=duration_hours)
        attendees_str = ", ".join(attendees) if attendees else "No specific attendees"
        return (f"Calendar event '{title}' successfully created:\n"
                f"  Start: {start_datetime.strftime('%Y-%m-%d %H:%M')}\n"
                f"  End: {end_datetime.strftime('%Y-%m-%d %H:%M')}\n"
                f"  Duration: {duration_hours} hours\n"
                f"  Attendees: {attendees_str}")
    except ValueError as e:
        return f"Error creating event: Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time. Details: {e}"

class ProductRecommendationInput(BaseModel):
    """Input for recommending products."""
    product_type: str = Field(description="The type of product to recommend, e.g., 'laptop', 'smartphone', 'headset'.")
    min_price: float = Field(default=0.0, description="Minimum price for the recommended product.")
    max_price: float = Field(default=1000.0, description="Maximum price for the recommended product.")
    limit: int = Field(default=3, description="Maximum number of recommendations to return (max 5).")

@tool(args_schema=ProductRecommendationInput)
def recommend_products(
    product_type: str,
    min_price: float = 0.0,
    max_price: float = 1000.0,
    limit: int = 3
) -> str:
    """Recommends products based on type and price range.
    This tool is useful for assisting users in finding suitable products from a catalog.
    """
    if not (1 <= limit <= 5):
        return "Error: limit must be between 1 and 5."
    mock_products = {
        "laptop": [
            {"name": "UltraBook Pro", "price": 1200, "specs": "16GB RAM, 512GB SSD"},
            {"name": "Gaming Beast X", "price": 1800, "specs": "RTX 4070, 32GB RAM"},
        ],
        "smartphone": [
            {"name": "Phone X", "price": 800, "specs": "6.1-inch OLED, 128GB"},
            {"name": "Budget Android", "price": 300, "specs": "6.5-inch LCD, 64GB"},
        ],
    }
    matching_products = []
    if product_type.lower() in mock_products:
        for product in mock_products[product_type.lower()]:
            if min_price <= product["price"] <= max_price:
                matching_products.append(product)
    if not matching_products:
        return f"No {product_type}s found in the price range ${min_price:.2f}-${max_price:.2f}."
    random.shuffle(matching_products)
    recommendations = matching_products[:limit]
    output = f"Here are some {product_type} recommendations:\n"
    for i, rec in enumerate(recommendations):
        output += (f"  {i+1}. {rec['name']} - ${rec['price']:.2f} ({rec['specs']})\n")
    return output.strip()


all_tools = [get_current_weather, search_wikipedia, create_calendar_event, recommend_products]

# 3. Create the Agent Prompt
# This prompt tells the AI how to behave and use the tools.
# The `tools` variable will be automatically filled by LangChain with the function schemas.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant. You have access to the following tools: {tools}"),
        ("human", "{input}"),
        AIMessage(content="", tool_calls=[]), # This is important for handling tool calls correctly
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 4. Create the Agent
agent = create_tool_calling_agent(llm, all_tools, prompt)

# 5. Create the Agent Executor
# This runs the agent, handling its thought process and tool invocations.
agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)
```
{% endraw %}

In this setup, the `prompt` is very important. It tells the AI about the tools it has and sets the stage for how it should interact. The `verbose=True` in `AgentExecutor` will show you the agent's "thoughts" as it decides to use a tool.

#### Making the Agent Use Your Tools

Now, let's ask our agent questions that require it to use the tools we've defined. You'll see the agent's internal monologue as it decides which `custom tool definition` to use and what arguments to pass, thanks to our `Pydantic args schema` and `tool description`s.

This is the most exciting part, watching your AI come to life and interact with the world through your custom tools. The agent will process your query, identify the need for a tool, call the tool, and then respond to you using the tool's output.

{% raw %}
```python
# Test Case 1: Weather tool
print("--- Query 1: Weather ---")
result_weather = agent_executor.invoke({"input": "What's the weather in Berlin in Celsius?"})
print(f"Agent's final response: {result_weather['output']}\n")

# Test Case 2: Wikipedia tool
print("--- Query 2: Wikipedia Search ---")
result_wiki = agent_executor.invoke({"input": "Tell me about quantum physics from Wikipedia."})
print(f"Agent's final response: {result_wiki['output']}\n")

# Test Case 3: Calendar event tool (requires specific date/time)
print("--- Query 3: Calendar Event ---")
result_calendar = agent_executor.invoke({"input": "Please create a meeting for 'Project Review' on 2026-09-01 at 11:00 AM for 1 hour. Invite charlie@example.com."})
print(f"Agent's final response: {result_calendar['output']}\n")

# Test Case 4: Product recommender tool
print("--- Query 4: Product Recommendation ---")
result_product = agent_executor.invoke({"input": "Can you recommend a smartphone under $500?"})
print(f"Agent's final response: {result_product['output']}\n")

# Test Case 5: A question that doesn't need a tool
print("--- Query 5: General Question ---")
result_general = agent_executor.invoke({"input": "What is the capital of France?"})
print(f"Agent's final response: {result_general['output']}\n")
```
{% endraw %}

When you run this code, you'll observe the agent's thinking process. It will first decide if a tool is needed. If so, it will generate a `tool_call` with the appropriate tool name and `Pydantic args schema` values. LangChain then executes the tool, and the result is fed back to the AI for its final answer.

### Advanced Concepts and Best Practices for Tool Development

As you create more complex `LangChain custom tools function calling` applications, consider these advanced tips. They will help you build more robust and user-friendly tools. Good `custom tool definition` goes a long way.

#### Error Handling in Tools

What if your tool can't complete its task? For instance, what if the weather service is down? Your tool should be designed to handle these situations gracefully. Instead of crashing, it should return an informative error message.

This message is then passed back to the AI. The AI can then tell the user what went wrong or try a different approach. For example, if fetching weather fails, your tool could return "Could not retrieve weather data at this time."

{% raw %}
```python
@tool(args_schema=WeatherInput)
def get_current_weather_robust(city: str, unit: str) -> str:
    """Get the current weather for a specific city, with improved error handling.
    This tool handles potential issues during data retrieval gracefully.
    """
    if unit.lower() not in ["celsius", "fahrenheit"]:
        return "Error: Unit must be 'celsius' or 'fahrenheit'."
    try:
        # Simulate a network error or API failure occasionally
        if random.random() < 0.1: # 10% chance of failure
            raise ConnectionError("Failed to connect to weather service.")

        temperature = random.randint(0, 30) if unit.lower() == "celsius" else random.randint(32, 86)
        conditions = random.choice(["sunny", "cloudy", "rainy", "stormy"])
        return f"The current weather in {city} is {temperature}°{unit.capitalize()} and {conditions}."
    except ConnectionError as e:
        return f"Sorry, I couldn't get the weather for {city} right now due to a connection issue: {e}. Please try again later."
    except Exception as e:
        return f"An unexpected error occurred while fetching weather for {city}: {e}. Please report this issue."
```
{% endraw %}

By anticipating problems, you make your AI agent more reliable and helpful. The AI can then inform the user rather than giving a vague error or simply failing.

#### Asynchronous Tools for Faster Agents

For tools that might take a long time to run (like complex database queries or external API calls), you can define them as asynchronous functions. This allows your agent to potentially do other things while waiting for a tool to finish.

You just add `async` before `def` and `await` inside your function. While the basic agent setup might not fully utilize this, it's a good practice for scalable applications. For more complex agent workflows, especially those involving multiple steps or parallel actions, you might want to look into frameworks like LangGraph: [Building Multi-Step AI Agents with LangGraph's StateGraph]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

{% raw %}
```python
import asyncio

@tool(args_schema=WeatherInput)
async def get_current_weather_async(city: str, unit: str) -> str:
    """Asynchronously get the current weather for a specific city."""
    await asyncio.sleep(1) # Simulate a delay for an async operation
    temperature = random.randint(0, 30) if unit.lower() == "celsius" else random.randint(32, 86)
    conditions = random.choice(["sunny", "cloudy", "rainy", "stormy"])
    return f"The current weather in {city} is {temperature}°{unit.capitalize()} and {conditions} (async)."
```
{% endraw %}

This `async` approach can make your agents feel faster and more responsive, especially when dealing with many tools or long-running operations.

#### Providing Good Tool Descriptions

We've mentioned this before, but it's worth repeating: a clear and concise `tool description` is paramount. It's the primary way the AI understands what your tool does and when to use it. Think of it as explaining your tool to a very smart but literal colleague.

Good descriptions should:
*   Clearly state the tool's purpose.
*   Mention what kind of questions it can answer or actions it can perform.
*   Hint at its input requirements or limitations.

Poor descriptions lead to the AI misusing tools or not using them at all. This means your `custom tool definition` is only as good as its description.

#### Tool Naming Conventions

Choose clear, descriptive names for your tools, like `get_current_weather` or `search_wikipedia`. Avoid vague names like `do_stuff` or `process_data`. A good name immediately tells you and the AI what the tool is for.

This makes debugging easier and helps the AI quickly identify the correct tool for a given task. Consistent naming also improves the overall readability and maintainability of your codebase.

### Troubleshooting Common Issues

Even with the best planning, you might encounter issues. Here are some common problems and how to solve them. Understanding these can save you a lot of time when working with `LangChain custom tools function calling`.

#### AI Not Using the Right Tool (or Any Tool)

If your AI isn't using a tool when you expect it to, or it's choosing the wrong one, here's what to check:

*   **Review your `tool description`:** Is it clear, concise, and specific about the tool's purpose? Does it clearly explain what the tool *does*? If the description is vague, the AI might not understand when to trigger it.
*   **Examine the prompt:** Is the user's input clear enough for the AI to understand that a tool is needed? Sometimes, rephrasing the question helps. The prompt you give the agent plays a big role in its decision-making.
*   **Check `Pydantic args schema` `Field` descriptions:** Do the descriptions for each argument guide the AI on what values to provide? The AI might hesitate if it's unsure what kind of data to put in. Make sure your `function schema` is well-defined.
*   **Ensure tools are passed to the agent:** Double-check that all your desired tools are included in the list passed to `create_tool_calling_agent` and `AgentExecutor`.
*   **Model capabilities:** Some smaller or older models might be less adept at function calling. Try using a more capable model like `gpt-4o-mini` or `gpt-4o`.

#### Invalid Tool Arguments

If the AI tries to use a tool but provides incorrect arguments, leading to Pydantic validation errors or runtime issues, consider these points:

*   **Pydantic `Field` validation:** Have you added sufficient validation (e.g., `min_length`, `pattern`, `enum`) to your `Pydantic args schema`? This helps catch issues early. For example, for a "unit" field, you could use an `Enum` to restrict choices to "celsius" or "fahrenheit".
*   **Clarity in `Field` descriptions:** Are the `description` attributes for each `Field` in your Pydantic model explicit about the expected format or valid values? For instance, stating "date in YYYY-MM-DD format" is crucial. This helps the AI generate correctly formatted arguments for the `function schema`.
*   **Agent's reasoning:** Look at the `verbose=True` output from `AgentExecutor`. Does the agent show that it *understood* the required format but still made a mistake, or did it never grasp the format in the first place? This can point to an issue with either the prompt or the tool's definition clarity.

By carefully reviewing your `custom tool definition`, especially the `tool description` and `Pydantic args schema`, you can often resolve most issues. The key is clear communication, both from you to the tool, and from the tool to the AI.

### Conclusion

You've learned how to empower your LangChain AI agents with custom tools using Pydantic and OpenAI function calling. We covered everything from creating simple `custom tool definition`s with the `@tool decorator` to building complex ones with detailed `Pydantic args schema`s. You now understand how to define a `function schema` that your AI can understand.

By integrating these tools, your AI can move beyond just generating text. It can interact with external systems, fetch real-time data, and perform actions in the real world. This capability makes your AI assistants incredibly versatile and powerful, enabling `LangChain custom tools function calling` for a wide range of applications.

Keep practicing and experimenting with different types of tools. The clearer your `tool description`s and `Pydantic args schema`s are, the smarter and more reliable your AI agent will become. Start building your own powerful tool-using AI agents today!