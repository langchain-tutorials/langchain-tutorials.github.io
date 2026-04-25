---
title: "How to Use LangChain Callbacks for Token Usage and Cost Tracking"
description: "Master LangChain callbacks token tracking to optimize your LLM costs. Learn how to monitor token usage effectively and save money on your AI projects today."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain callbacks token tracking]
featured: false
image: '/assets/images/langchain-callbacks-token-usage-cost-tracking.webp'
---

## How to Use LangChain Callbacks for Token Usage and Cost Tracking

Large Language Models (LLMs) are amazing tools, but using them comes with a cost. Just like turning on a light uses electricity, talking to an LLM uses up "tokens." If you don't keep an eye on these tokens, your expenses can quickly grow. This is where LangChain callbacks token tracking becomes incredibly helpful.

Imagine you have a piggy bank for your LLM usage. LangChain callbacks act like a little helper that tells you exactly how much money you're putting in and taking out, helping with your budget monitoring. They let you see the `LLM cost` in real-time. By the end of this guide, you will understand how to use these powerful tools.

### Understanding LangChain Callbacks

First, let's understand what callbacks are. In simple terms, a callback is like a special alert. When something important happens in your LangChain program, a callback can "call back" to a part of your code and tell it what just happened. This is super useful for observing your program as it runs.

LangChain uses these callbacks to let you plug into different stages of an LLM's operation. For example, you can know when an LLM starts thinking or when it finishes giving an answer. This allows for powerful `LangChain callbacks token tracking`.

The core of this system is the `BaseCallbackHandler` class. You create your own special callback by building upon this class. This way, you can customize what information you want to collect and how you want to handle it.

### Why Track Token Usage and Costs?

Tracking your `LLM cost` is very important for many reasons. Every time you send text to an LLM or get text back, you are using tokens. These tokens cost money, especially with popular models from providers like OpenAI. Understanding `token counting` is the first step to financial control.

Without proper `LangChain callbacks token tracking`, you might unknowingly spend more than you planned. This can be a big problem, especially for apps that talk to LLMs many times. Good tracking helps you with essential `budget monitoring`.

By knowing your `OpenAI cost` or the cost from other LLMs, you can make smarter choices. You can decide if a certain prompt is too long or if a different, cheaper model might do the job. It's all about being smart with your resources.

### Setting Up Your Environment

Before we dive into tracking, you need to set up your workspace. You will need Python installed on your computer. Make sure it's a version like 3.9 or newer.

First, let's install the necessary libraries. We'll need `langchain-community`, `langchain-openai`, and `python-dotenv` to manage your secret API keys safely. Open your computer's terminal or command prompt and type these commands.

{% raw %}
```bash
pip install langchain-community langchain-openai python-dotenv
```
{% endraw %}

Next, you'll need an API key from OpenAI (or another LLM provider). Create a file named `.env` in the same folder as your Python code. Inside that file, put your OpenAI API key like this:

{% raw %}
```
OPENAI_API_KEY="your_openai_api_key_here"
```
{% endraw %}

Remember to replace `"your_openai_api_key_here"` with your actual key. This `.env` file keeps your secret key safe and out of your main code. Now you're ready to start building your `LangChain callbacks token tracking` solution.

### Building a Simple Token Usage Tracker

The most important part of `LangChain callbacks token tracking` for usage is a method called `on_llm_end`. This method gets called every time an LLM finishes its job. When it finishes, it gives us special `usage metadata` that includes the number of tokens used.

#### The `on_llm_end` Method Explained

The `on_llm_end` method is like a final report card for each LLM call. After the LLM processes your request and generates a response, this method automatically runs. It receives an object that contains all the juicy details, including the `token counting` information.

Specifically, it provides details like `prompt_tokens` (how many tokens your question used) and `completion_tokens` (how many tokens the LLM's answer used). This `usage metadata` is exactly what we need to calculate costs and track usage. By using `on_llm_end`, you can ensure accurate `budget monitoring`.

Let's create our first custom callback to perform basic `token counting`. We will make a class that inherits from `BaseCallbackHandler` and then override the `on_llm_end` method. This simple example will just print the token usage.

#### Example 1: Basic Token Count for an LLM Call

Here’s how you can make a simple callback to track tokens. This code defines a `MyTokenTracker` class. It has a special method, `on_llm_end`, which runs when the LLM finishes.

{% raw %}
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

load_dotenv()

class MyTokenTracker(BaseCallbackHandler):
    """Callback handler for tracking token usage."""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0

    def on_llm_end(self, response, **kwargs):
        """Called at the end of an LLM call."""
        if response.llm_output is not None and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)

            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += total_tokens

            print(f"--- LLM Call Ended ---")
            print(f"Prompt Tokens: {prompt_tokens}")
            print(f"Completion Tokens: {completion_tokens}")
            print(f"Total Tokens for this call: {total_tokens}")
            print(f"--- Cumulative Tokens ---")
            print(f"Total Prompt Tokens (overall): {self.total_prompt_tokens}")
            print(f"Total Completion Tokens (overall): {self.total_completion_tokens}")
            print(f"Total Tokens (overall): {self.total_tokens}")
            print(f"----------------------")
        else:
            print("No token usage metadata found for this LLM call.")

# Now, let's use our tracker with an LLM
tracker = MyTokenTracker()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, callbacks=[tracker])

print("\n--- Making first LLM call ---")
response1 = llm.invoke("What is the capital of France?")

print("\n--- Making second LLM call ---")
response2 = llm.invoke("Tell me a short joke.")

print("\n--- Final Cumulative Token Usage ---")
print(f"Final Total Prompt Tokens: {tracker.total_prompt_tokens}")
print(f"Final Total Completion Tokens: {tracker.total_completion_tokens}")
print(f"Final Total Tokens: {tracker.total_tokens}")
```
{% endraw %}

In this example, `MyTokenTracker` keeps a running total of all tokens. Each time an LLM call finishes, `on_llm_end` updates these totals and prints them. You can see how the `usage metadata` provides the exact `token counting` for each interaction. This is a foundational step in `LangChain callbacks token tracking`.

### Adding Cost Estimation to Your Tracker

Knowing the number of tokens is great, but knowing the actual `LLM cost` is even better for `budget monitoring`. Different LLM models have different prices. Usually, there's one price for input tokens (what you send) and another for output tokens (what you get back). This applies to `OpenAI cost` and many other providers.

#### Understanding LLM Pricing Models

LLM providers like OpenAI charge based on the number of tokens used. It's not a flat fee. For example, a model might charge $0.0005 for every 1,000 input tokens and $0.0015 for every 1,000 output tokens. These rates vary greatly by model and provider.

When you get `usage metadata` from `on_llm_end`, it tells you the `prompt_tokens` and `completion_tokens`. We can then use these numbers with a simple pricing table to calculate the exact `OpenAI cost` for that specific interaction. Keeping these pricing models in mind is key to accurate `budget monitoring`.

Let's enhance our `MyTokenTracker` to not only count tokens but also estimate the cost. We'll need to define a simple dictionary that holds the pricing for the model we are using. This will turn our `token counting` into actionable `LLM cost` data.

#### Example 2: Token Counting and Cost Tracking for a Single LLM Call

Let's modify our `MyTokenTracker` to include cost calculations. We'll add a `model_prices` dictionary to store the cost per 1000 tokens for our chosen model. This way, we can immediately see the financial impact of each LLM call. This is a crucial step for `LangChain callbacks token tracking`.

{% raw %}
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

load_dotenv()

class CostTokenTracker(BaseCallbackHandler):
    """Callback handler for tracking token usage and estimating cost."""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        # Define pricing for common OpenAI models (per 1k tokens)
        # Note: These prices are illustrative and may change. Always check official docs.
        self.model_prices = {
            "gpt-3.5-turbo": {"input_cost_per_1k_tokens": 0.0005, "output_cost_per_1k_tokens": 0.0015},
            "gpt-4": {"input_cost_per_1k_tokens": 0.03, "output_cost_per_1k_tokens": 0.06},
            "gpt-4-turbo": {"input_cost_per_1k_tokens": 0.01, "output_cost_per_1k_tokens": 0.03},
        }
        self.current_model = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        """Called at the start of an LLM call. Get the model name."""
        # This part helps identify the model used if it's dynamic
        # For ChatOpenAI, the model name is usually in serialized_args
        llm_name = serialized.get("kwargs", {}).get("model_name")
        if llm_name:
            self.current_model = llm_name
        else:
            self.current_model = "unknown"
        # print(f"LLM Call Started with model: {self.current_model}")


    def on_llm_end(self, response, **kwargs):
        """Called at the end of an LLM call."""
        if response.llm_output is not None and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)

            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += total_tokens

            # Calculate cost
            cost = 0.0
            if self.current_model in self.model_prices:
                model_price_info = self.model_prices[self.current_model]
                cost += (prompt_tokens / 1000) * model_price_info["input_cost_per_1k_tokens"]
                cost += (completion_tokens / 1000) * model_price_info["output_cost_per_1k_tokens"]
                self.total_cost += cost
            else:
                print(f"Warning: No price info for model '{self.current_model}'. Cost not calculated.")

            print(f"--- LLM Call Ended ({self.current_model}) ---")
            print(f"Prompt Tokens: {prompt_tokens}")
            print(f"Completion Tokens: {completion_tokens}")
            print(f"Total Tokens for this call: {total_tokens}")
            print(f"Estimated Cost for this call: ${cost:.6f}")
            print(f"--- Cumulative ---")
            print(f"Total Prompt Tokens: {self.total_prompt_tokens}")
            print(f"Total Completion Tokens: {self.total_completion_tokens}")
            print(f"Total Tokens: {self.total_tokens}")
            print(f"Total Estimated Cost: ${self.total_cost:.6f}")
            print(f"----------------------")
        else:
            print("No token usage metadata found for this LLM call.")

# Let's use our new cost tracker
tracker = CostTokenTracker()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, callbacks=[tracker])

print("\n--- Making first LLM call (long prompt) ---")
long_prompt = "Explain the concept of quantum entanglement in simple terms. Provide a metaphor for better understanding, and describe its implications for quantum computing. Make sure your explanation is thorough but easy to grasp for someone with no physics background."
response1 = llm.invoke(long_prompt)

print("\n--- Making second LLM call (short prompt, different model potentially) ---")
# To demonstrate model flexibility, you could uncomment the lines below and use a different model
# but for simplicity and consistent tracking with a single LLM instance, we'll keep the same model.
# llm_gpt4 = ChatOpenAI(model="gpt-4", temperature=0, callbacks=[tracker])
# response2 = llm_gpt4.invoke("What is the capital of Japan?")
response2 = llm.invoke("Summarize the key takeaways from the quantum entanglement explanation.")


print("\n--- Final Cumulative Usage and Cost ---")
print(f"Final Total Prompt Tokens: {tracker.total_prompt_tokens}")
print(f"Final Total Completion Tokens: {tracker.total_completion_tokens}")
print(f"Final Total Tokens: {tracker.total_tokens}")
print(f"Final Total Estimated Cost: ${tracker.total_cost:.6f}")
```
{% endraw %}

Now, our `CostTokenTracker` can give you a quick estimate of your `OpenAI cost` for each interaction. We added `on_llm_start` to capture the model name, which is important because pricing changes between models. This precise `usage metadata` and `token counting` is essential for effective `budget monitoring`.

### Tracking Tokens Across Chains and Agents

Most of the time, you won't just make single LLM calls. You'll use LangChain's chains and agents, which make many LLM calls behind the scenes. Our `LangChain callbacks token tracking` system is designed to work seamlessly with these more complex structures.

When you use a chain or an agent, each individual LLM interaction within that chain or agent will still trigger your `on_llm_end` callback. This means your tracker will collect `usage metadata` for every step. This provides a comprehensive view of your `LLM cost`.

#### Example 3: Tracking with a Simple LLMChain

An `LLMChain` is a sequence of actions that involve an LLM. For instance, you might have a chain that takes a user's question, formats it, sends it to an LLM, and then processes the answer. Even though it's one "chain" operation, it still has one or more underlying LLM calls.

Our callback will capture the `token counting` for each of these internal LLM calls. This helps you understand the `LLM cost` for an entire multi-step process. Let's see how our `CostTokenTracker` works with an `LLMChain`.

{% raw %}
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

load_dotenv()

# Re-using our CostTokenTracker class from Example 2
class CostTokenTracker(BaseCallbackHandler):
    """Callback handler for tracking token usage and estimating cost."""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.model_prices = {
            "gpt-3.5-turbo": {"input_cost_per_1k_tokens": 0.0005, "output_cost_per_1k_tokens": 0.0015},
            "gpt-4": {"input_cost_per_1k_tokens": 0.03, "output_cost_per_1k_tokens": 0.06},
            "gpt-4-turbo": {"input_cost_per_1k_tokens": 0.01, "output_cost_per_1k_tokens": 0.03},
        }
        self.current_model = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        llm_name = serialized.get("kwargs", {}).get("model_name")
        if llm_name:
            self.current_model = llm_name
        else:
            self.current_model = "unknown"

    def on_llm_end(self, response, **kwargs):
        if response.llm_output is not None and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)

            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += total_tokens

            cost = 0.0
            if self.current_model in self.model_prices:
                model_price_info = self.model_prices[self.current_model]
                cost += (prompt_tokens / 1000) * model_price_info["input_cost_per_1k_tokens"]
                cost += (completion_tokens / 1000) * model_price_info["output_cost_per_1k_tokens"]
                self.total_cost += cost
            else:
                print(f"Warning: No price info for model '{self.current_model}'. Cost not calculated.")

            print(f"--- LLM Call Ended ({self.current_model}) ---")
            print(f"Prompt Tokens: {prompt_tokens}")
            print(f"Completion Tokens: {completion_tokens}")
            print(f"Total Tokens for this call: {total_tokens}")
            print(f"Estimated Cost for this call: ${cost:.6f}")
            print(f"--- Cumulative ---")
            print(f"Total Prompt Tokens: {self.total_prompt_tokens}")
            print(f"Total Completion Tokens: {self.total_completion_tokens}")
            print(f"Total Tokens: {self.total_tokens}")
            print(f"Total Estimated Cost: ${self.total_cost:.6f}")
            print(f"----------------------")
        else:
            print("No token usage metadata found for this LLM call.")

tracker = CostTokenTracker()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, callbacks=[tracker])

# Define a prompt template
prompt = ChatPromptTemplate.from_template("What is the main idea of {topic}? Explain it concisely.")

# Create an LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

print("\n--- Invoking LLMChain ---")
response = chain.invoke({"topic": "artificial intelligence"})

print("\n--- Final Cumulative Usage and Cost ---")
print(f"Final Total Prompt Tokens: {tracker.total_prompt_tokens}")
print(f"Final Total Completion Tokens: {tracker.total_completion_tokens}")
print(f"Final Total Tokens: {tracker.total_tokens}")
print(f"Final Total Estimated Cost: ${tracker.total_cost:.6f}")
```
{% endraw %}

You'll notice that even though we call `chain.invoke()` only once, our `on_llm_end` method still fires. This is because the chain internally makes an LLM call. This demonstrates the power of `LangChain callbacks token tracking` for complex operations and `budget monitoring`.

#### Example 4: Tracking with a LangChain Agent (More Complex)

Agents are even more dynamic than chains. They can decide which tools to use, and they might make multiple LLM calls in a single interaction to achieve a goal. Tracking `LLM cost` with agents is especially critical due to their unpredictable nature.

Each decision an agent makes and each tool it uses can involve an LLM call. Our callback will diligently track the `token counting` for all these individual calls. This gives you a clear picture of the `OpenAI cost` incurred by your agent's thought process.

For even more advanced agent building, you might explore frameworks like LangGraph, which offers state management for multi-step AI agents. You can learn more about [building multi-step AI agents with LangGraph]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}). Similarly, for integrating custom tools, consider [LangChain Google Gemini Function Calling Agent Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

Let's use a simple agent to see our `CostTokenTracker` in action. We'll use a basic `AgentExecutor` with a tool.

{% raw %}
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

# Re-using our CostTokenTracker class from Example 2/3
class CostTokenTracker(BaseCallbackHandler):
    """Callback handler for tracking token usage and estimating cost."""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.model_prices = {
            "gpt-3.5-turbo": {"input_cost_per_1k_tokens": 0.0005, "output_cost_per_1k_tokens": 0.0015},
            "gpt-4": {"input_cost_per_1k_tokens": 0.03, "output_cost_per_1k_tokens": 0.06},
            "gpt-4-turbo": {"input_cost_per_1k_tokens": 0.01, "output_cost_per_1k_tokens": 0.03},
        }
        self.current_model = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        llm_name = serialized.get("kwargs", {}).get("model_name")
        if llm_name:
            self.current_model = llm_name
        else:
            self.current_model = "unknown"

    def on_llm_end(self, response, **kwargs):
        if response.llm_output is not None and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens = token_usage.get("total_tokens", 0)

            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += total_tokens

            cost = 0.0
            if self.current_model in self.model_prices:
                model_price_info = self.model_prices[self.current_model]
                cost += (prompt_tokens / 1000) * model_price_info["input_cost_per_1k_tokens"]
                cost += (completion_tokens / 1000) * model_price_info["output_cost_per_1k_tokens"]
                self.total_cost += cost
            else:
                print(f"Warning: No price info for model '{self.current_model}'. Cost not calculated.")

            print(f"--- LLM Call Ended ({self.current_model}) ---")
            print(f"Prompt Tokens: {prompt_tokens}")
            print(f"Completion Tokens: {completion_tokens}")
            print(f"Total Tokens for this call: {total_tokens}")
            print(f"Estimated Cost for this call: ${cost:.6f}")
            print(f"--- Cumulative ---")
            print(f"Total Prompt Tokens: {self.total_prompt_tokens}")
            print(f"Total Completion Tokens: {self.total_completion_tokens}")
            print(f"Total Tokens: {self.total_tokens}")
            print(f"Total Estimated Cost: ${self.total_cost:.6f}")
            print(f"----------------------")
        else:
            print("No token usage metadata found for this LLM call.")

# Define a simple tool
@tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location"""
    if "london" in location.lower():
        return "It's sunny and 20 degrees Celsius in London."
    elif "paris" in location.lower():
        return "It's cloudy and 15 degrees Celsius in Paris."
    else:
        return f"Weather data not available for {location}."

tools = [get_current_weather]

# Initialize LLM and Tracker
tracker = CostTokenTracker()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, callbacks=[tracker])

# Define the agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Create the agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, callbacks=[tracker])

print("\n--- Invoking AgentExecutor ---")
response = agent_executor.invoke({"input": "What is the weather in London?"})

print("\n--- Final Cumulative Usage and Cost ---")
print(f"Final Total Prompt Tokens: {tracker.total_prompt_tokens}")
print(f"Final Total Completion Tokens: {tracker.total_completion_tokens}")
print(f"Final Total Tokens: {tracker.total_tokens}")
print(f"Final Total Estimated Cost: ${tracker.total_cost:.6f}")
```
{% endraw %}

When you run the agent, you'll see multiple "LLM Call Ended" messages. This shows that the agent made several LLM calls: one to decide what to do, another to process the tool's output, and perhaps another to formulate the final answer. Each of these steps contributes to your `OpenAI cost`, and our `LangChain callbacks token tracking` captures them all, providing excellent `usage metadata` for `budget monitoring`.

### Storing and Analyzing Usage Data

Printing the `LLM cost` and `token counting` to the console is useful for immediate feedback. However, for serious `budget monitoring` and understanding long-term trends, you'll want to store this data. This lets you analyze `usage metadata` over time, generate reports, and make informed decisions.

#### Example 5: Storing Data in a List (Simple History)

A simple way to store the data is to keep it in a list within your callback class. Each time `on_llm_end` is triggered, you can record the details of that specific LLM call. This creates a history of all your interactions, complete with `token counting` and `OpenAI cost`.

Let's modify our `CostTokenTracker` to keep a list of all individual LLM call records. This provides a basic logging mechanism for your `LangChain callbacks token tracking`.

{% raw %}
```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

load_dotenv()

class PersistentCostTokenTracker(BaseCallbackHandler):
    """Callback handler for tracking token usage and estimating cost, with data storage."""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.call_history = [] # This list will store details of each LLM call
        self.model_prices = {
            "gpt-3.5-turbo": {"input_cost_per_1k_tokens": 0.0005, "output_cost_per_1k_tokens": 0.0015},
            "gpt-4": {"input_cost_per_1k_tokens": 0.03, "output_cost_per_1k_tokens": 0.06},
            "gpt-4-turbo": {"input_cost_per_1k_tokens": 0.01, "output_cost_per_1k_tokens": 0.03},
        }
        self.current_model = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        llm_name = serialized.get("kwargs", {}).get("model_name")
        if llm_name:
            self.current_model = llm_name
        else:
            self.current_model = "unknown"

    def on_llm_end(self, response, **kwargs):
        if response.llm_output is not None and "token_usage" in response.llm_output:
            token_usage = response.llm_output["token_usage"]
            prompt_tokens = token_usage.get("prompt_tokens", 0)
            completion_tokens = token_usage.get("completion_tokens", 0)
            total_tokens_for_call = token_usage.get("total_tokens", 0) # Renamed to avoid confusion with self.total_tokens

            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += total_tokens_for_call

            cost = 0.0
            if self.current_model in self.model_prices:
                model_price_info = self.model_prices[self.current_model]
                cost += (prompt_tokens / 1000) * model_price_info["input_cost_per_1k_tokens"]
                cost += (completion_tokens / 1000) * model_price_info["output_cost_per_1k_tokens"]
                self.total_cost += cost
            else:
                print(f"Warning: No price info for model '{self.current_model}'. Cost not calculated.")

            # Store the details of this specific call
            self.call_history.append({
                "model": self.current_model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens_for_call": total_tokens_for_call,
                "estimated_cost_for_call": cost,
                "timestamp": datetime.now().isoformat() # Added timestamp for better tracking
            })

            print(f"--- LLM Call Ended ({self.current_model}) ---")
            print(f"Prompt Tokens: {prompt_tokens}")
            print(f"Completion Tokens: {completion_tokens}")
            print(f"Total Tokens for this call: {total_tokens_for_call}")
            print(f"Estimated Cost for this call: ${cost:.6f}")
            print(f"--- Cumulative ---")
            print(f"Total Prompt Tokens: {self.total_prompt_tokens}")
            print(f"Total Completion Tokens: {self.total_completion_tokens}")
            print(f"Total Tokens: {self.total_tokens}")
            print(f"Total Estimated Cost: ${self.total_cost:.6f}")
            print(f"----------------------")
        else:
            print("No token usage metadata found for this LLM call.")

# Add datetime for timestamps
from datetime import datetime

tracker = PersistentCostTokenTracker()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, callbacks=[tracker])

print("\n--- Making first LLM call ---")
llm.invoke("What is the highest mountain in the world?")

print("\n--- Making second LLM call ---")
llm.invoke("Who was the first person to climb Mount Everest?")

print("\n--- Final Cumulative Usage and Cost ---")
print(f"Final Total Prompt Tokens: {tracker.total_prompt_tokens}")
print(f"Final Total Completion Tokens: {tracker.total_completion_tokens}")
print(f"Final Total Tokens: {tracker.total_tokens}")
print(f"Final Total Estimated Cost: ${tracker.total_cost:.6f}")

print("\n--- Call History (last 2 calls) ---")
for i, call in enumerate(tracker.call_history):
    print(f"Call {i+1}: Model={call['model']}, Tokens={call['total_tokens_for_call']}, Cost=${call['estimated_cost_for_call']:.6f}, Time={call['timestamp']}")
```
{% endraw %}

Now, `tracker.call_history` contains a list of dictionaries, each representing a single LLM call with its `usage metadata`, `token counting`, and estimated `LLM cost`. This simple in-memory storage is excellent for quick debugging or small applications, offering basic `budget monitoring` capabilities.

#### Advanced Storage Considerations

For larger applications and robust `budget monitoring`, you'll want to move beyond in-memory lists. You could save this data to:
*   **A file:** Like a CSV or JSON file, simple for exporting.
*   **A database:** A SQL database (e.g., SQLite, PostgreSQL) or a NoSQL database (e.g., MongoDB) would allow you to store massive amounts of `usage metadata`, query it, and generate complex reports.
*   **A logging system:** Tools like Elastic Stack (ELK) or cloud logging services can collect this data and provide dashboards for visualization.

When storing data, consider adding more `usage metadata` from the `on_llm_end` method, like the actual prompt or response (if privacy allows), to get even richer insights into your `LLM cost`.

### Advanced Callback Features for LangChain Callbacks Token Tracking

LangChain callbacks offer more than just `on_llm_end`. There are several other methods you can override in your `BaseCallbackHandler` to get a deeper understanding of your application's behavior and enhance your `LangChain callbacks token tracking`.

#### Handling Errors (`on_llm_error`)

Sometimes, LLM calls can fail. Perhaps the API key is wrong, or the model is overloaded. The `on_llm_error` method gets called whenever an error happens during an LLM interaction. You can use this to log the error, send an alert, or even try to re-run the failed part of your code.

This is important for `budget monitoring` too. If an LLM call fails, you still want to know if any tokens were used before the failure. While `token counting` might not always be available for a failed call, logging the error helps debug and prevents unexpected `LLM cost` from repeated failed attempts.

#### Streaming Responses (`on_llm_new_token`)

Some LLMs can stream their responses, meaning they send back words one by one instead of waiting to finish the whole answer. The `on_llm_new_token` method is called for each new token that arrives during streaming.

While not directly used for `token counting` or `OpenAI cost` calculation (as final token counts are available in `on_llm_end`), this method is useful for displaying progress to users. If you are building a real-time chat application, this is how you make the response appear as it's being generated.

#### Context Management

You might want to pass information between different callback methods or keep track of the context of an ongoing operation. For example, you might want to link a series of LLM calls that belong to a single "user request." LangChain's callback manager can help with this.

Each callback method receives a `run_id` and `parent_run_id`. These IDs allow you to create a tree-like structure of all operations. This `usage metadata` is incredibly valuable for debugging complex chains and agents. It helps you see how different LLM calls relate to each other, improving your overall `LangChain callbacks token tracking` and `budget monitoring`.

#### Callback Managers (`CallbackManager`, `AsyncCallbackManager`)

When you have multiple callbacks, you can group them using a `CallbackManager`. This manager ensures that all your callbacks are triggered correctly. For applications that handle many requests at once (asynchronous operations), you'd use `AsyncCallbackManager`.

Using a `CallbackManager` is especially helpful if you want different callbacks to do different things: one for `token counting`, another for logging, and another for security checks. You can pass a list of your custom callback handler instances to the `CallbackManager`, and then pass the manager to your LLM or chain.

### Best Practices for Budget Monitoring and LLM Cost Control

Effective `budget monitoring` is key to using LLMs sustainably. By actively engaging in `LangChain callbacks token tracking`, you are already taking a huge step in the right direction. Here are some best practices to keep your `LLM cost` in check.

*   **Always Use `LangChain Callbacks Token Tracking`:** As you've seen, callbacks are your eyes and ears into LLM usage. Integrate them from the start into all your LangChain applications. This allows for continuous `token counting` and `OpenAI cost` estimation.
*   **Set Spending Alerts:** Don't just track; act on the data. Set up automated alerts (e.g., email, Slack message) when your `LLM cost` approaches a certain limit within a day or month. This proactive approach helps prevent bill shock.
*   **Review `Usage Metadata` Regularly:** Make it a habit to look at your token and cost reports. Identify patterns: Are certain features consuming more tokens than others? Can you find ways to optimize? This data is invaluable for `budget monitoring`.
*   **Optimize Prompts to Reduce `Token Counting`:** Shorter, clearer, and more efficient prompts lead to fewer input tokens and often shorter, more focused responses, reducing completion tokens. Experiment with different phrasings to get the same quality of output with fewer tokens. For example, using a system message to define the model's role upfront can reduce the need for lengthy instructions in every user prompt.
*   **Choose Appropriate Models for Tasks:** Don't use the most powerful (and expensive) LLM for every task. A simpler model might be perfectly sufficient for basic summarization or classification, significantly lowering your `OpenAI cost`. Match the model's capability to the task's complexity.
*   **Implement Caching:** For repetitive queries, use caching mechanisms to store previous LLM responses. This prevents redundant LLM calls, saving tokens and money. LangChain has built-in caching features you can explore.
*   **Use Retrieval-Augmented Generation (RAG) Wisely:** RAG applications, which retrieve information from your own data before querying an LLM, can be very powerful. However, the retrieval process itself and the context sent to the LLM can add to `token counting`. Be mindful of the size of the retrieved context you send to the LLM. Learn more about building such applications in [Build RAG Applications LangChain Vector Store]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).
*   **Batch Requests When Possible:** If you have many small, independent LLM requests, sometimes it's more efficient to combine them into a single larger request if the LLM API supports it. This can sometimes lead to better pricing or reduced overhead, though `token counting` will still apply.
*   **Monitor for Infinite Loops in Agents:** Agents, especially complex ones, can sometimes get stuck in loops, repeatedly calling the LLM. Your `LangChain callbacks token tracking` will quickly highlight this by showing a sudden spike in `token counting` and `LLM cost`. Implement safeguards like maximum iteration limits for agents.

By following these best practices, you can ensure that your LLM applications are not only powerful but also cost-effective and sustainable.

### Troubleshooting Common Issues

Even with the best intentions, you might run into some hiccups when setting up your `LangChain callbacks token tracking`. Here are a few common issues and how to tackle them:

*   **Callbacks Not Firing:**
    *   **Did you pass the `callbacks` argument?** Make sure you're passing `callbacks=[your_tracker_instance]` to your `ChatOpenAI` (or other LLM), `LLMChain`, `AgentExecutor`, or other LangChain components. If you forget, your callback won't be used.
    *   **Is your `BaseCallbackHandler` correctly inherited?** Double-check that your custom class correctly extends `BaseCallbackHandler` from `langchain.callbacks.base`.
    *   **Are you overriding the correct method?** For token usage, `on_llm_end` is key. If you're expecting `on_llm_start` or `on_llm_error` to fire, ensure you've properly implemented them.
*   **Incorrect `Token Counting` or Missing `Usage Metadata`:**
    *   **Model Compatibility:** Not all LLMs or API providers return `token_usage` in the same format, or at all. Most major providers like OpenAI do, but if you're using a niche model, verify its output structure. The `response.llm_output` might be structured differently.
    *   **Check the `response.llm_output` structure:** Print `response.llm_output` inside `on_llm_end` to see its exact content. This helps confirm if `token_usage` is present and what keys it contains (e.g., `prompt_tokens`, `completion_tokens`).
    *   **LangChain Version:** Ensure your LangChain libraries are up to date. Newer versions might have better `usage metadata` consistency. Run `pip install --upgrade langchain-community langchain-openai`.
*   **API Key Issues:**
    *   **Environment Variable Not Loaded:** If you're getting authentication errors, ensure your `.env` file is in the correct directory and `load_dotenv()` is called at the very beginning of your script.
    *   **Incorrect Key:** Double-check that the `OPENAI_API_KEY` in your `.env` file is correct and doesn't have extra spaces or characters.
*   **Cost Calculation Errors:**
    *   **Outdated Pricing:** LLM providers can change their pricing models. Always refer to the official documentation for the most current rates for `OpenAI cost` or other providers. Update your `model_prices` dictionary as needed.
    *   **Model Name Mismatch:** Ensure the `current_model` name captured in `on_llm_start` exactly matches the keys in your `model_prices` dictionary. Case sensitivity can be an issue.

By systematically checking these points, you can usually resolve most issues related to `LangChain callbacks token tracking` and ensure your `budget monitoring` is accurate.

### Conclusion

You've now learned how to harness the power of `LangChain callbacks token tracking`. This essential skill allows you to see the hidden costs of your LLM applications. By implementing custom callback handlers, you can perform accurate `token counting` and estimate your `OpenAI cost` or other `LLM cost` in real-time.

Understanding `usage metadata` through the `on_llm_end` method gives you the data you need for smart `budget monitoring`. Whether you're running simple LLM calls, complex chains, or dynamic agents, your tracker will keep a watchful eye on your resource consumption. This level of insight empowers you to build more efficient, transparent, and cost-effective AI solutions. Keep tracking, keep optimizing, and take control of your LLM expenses!