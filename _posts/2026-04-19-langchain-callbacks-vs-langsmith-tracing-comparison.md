---
title: "LangChain Callbacks vs LangSmith Tracing: Which Monitoring Approach Should You Use"
description: "Struggling with LangChain monitoring? Discover the pros and cons of LangChain callbacks vs LangSmith tracing. Choose the ideal solution for your AI projects ..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain callbacks vs LangSmith tracing]
featured: false
image: '/assets/images/langchain-callbacks-vs-langsmith-tracing-comparison.webp'
---

## LangChain Callbacks vs LangSmith Tracing: Which Monitoring Approach Should You Use?

Building applications with large language models (LLMs) can feel like magic, but sometimes things don't go as planned. When your AI application gives a strange answer, you need to peek inside to see what happened. This is where monitoring tools become super important.

You have two main ways to look "under the hood" of your [LangChain](https://www.langchain.com/) applications: LangChain Callbacks and LangSmith Tracing. Both help you understand how your LLM chains and agents are working. Choosing between them depends on what you need to see and how deeply you want to investigate.

This guide will help you understand the core differences between LangChain callbacks vs LangSmith tracing. We will explore what each one does, how they work, and when you should pick one over the other. By the end, you'll know exactly which monitoring approach is best for your projects.

### Understanding the Need for Monitoring LLM Applications

Imagine you're baking a cake, but you can't see anything happening inside the oven. You just put in ingredients and hope for the best, checking only when it's done. This is often how building LLM applications feels without good monitoring.

When your LangChain agent is trying to answer a complex question, many steps happen behind the scenes. It might call a language model, use a tool, search a database, or even chain multiple thoughts together. If the final answer is wrong, figuring out why can be a real puzzle.

Monitoring helps you watch each step of your application's journey. It lets you see what inputs were given, what the LLM thought, and what tools were used. This detailed view is crucial for LLM debugging and improving your application's reliability. Effective observability tools are essential for any serious LLM development.

### What are LangChain Callbacks?

LangChain callbacks are like little helpers you can attach to different parts of your LangChain application. Think of them as event listeners that get notified when certain things happen. They let you run your own code at specific points during a chain's execution.

These callbacks are triggered by events such as a chain starting, a language model being called, or a tool being used. You can tell LangChain to execute a custom function whenever one of these events occurs. This gives you direct control over what data you want to capture or what actions you want to take.

You can use LangChain callbacks to print messages to your console, log information to a file, or even send data to a different logging system. They are highly customizable and integrated directly into the LangChain framework. This allows for a very flexible monitoring comparison right within your code.

#### How LangChain Callbacks Work

When you create a `CallbackHandler` in LangChain, you're essentially defining a set of rules. Each rule tells your application what to do when a specific event happens. For example, you might have a rule for `on_llm_start` and another for `on_chain_end`.

You then pass your custom `CallbackHandler` to your LangChain chain or agent. As the chain runs, it will automatically call the methods you defined in your handler at the right moments. This lets you observe the flow of information step-by-step.

These handlers are plain Python classes that inherit from `BaseCallbackHandler`. You override methods like `on_llm_start`, `on_chain_end`, `on_tool_start`, and more. This makes them very powerful for custom logging or even changing behavior dynamically.

#### Practical Example: Basic Console Logging with Callbacks

Let's look at a simple example where we use a LangChain callback to print out what our LLM is doing. This helps us understand the prompt and response in real-time. It's a fundamental step in LLM debugging for a small application.

First, you need to import the necessary parts and define a simple chain. We will use a basic `ChatOpenAI` model for this. Make sure you have your OpenAI API key set up in your environment variables.

{% raw %}
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
import os

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# 1. Define a custom callback handler
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        """Called when LLM starts running."""
        print(f"\n--- LLM Started ---")
        print(f"Prompts sent to LLM: {prompts}")

    def on_llm_end(self, response, **kwargs):
        """Called when LLM ends running."""
        print(f"LLM Response received: {response.generations[0][0].text}")
        print(f"--- LLM Ended ---\n")

    def on_chain_start(self, serialized: dict, **kwargs):
        """Called when chain starts running."""
        print(f"\n### Chain Started ###")
        print(f"Chain type: {serialized.get('lc_kwargs', {}).get('name') or serialized.get('lc_toolname')}")


    def on_chain_end(self, outputs: dict, **kwargs):
        """Called when chain ends running."""
        print(f"Chain output: {outputs}")
        print(f"### Chain Ended ###\n")

# 2. Create an instance of your callback handler
my_handler = MyCustomHandler()

# 3. Define your LLM and prompt
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("Tell me a short {animal} joke.")

# 4. Create a simple chain and pass the callback handler
chain = prompt | llm

# 5. Invoke the chain with the callback handler
print("--- Invoking chain with callbacks ---")
chain.invoke({"animal": "cat"}, config={"callbacks": [my_handler]})

print("\n--- Invoking chain WITHOUT callbacks ---")
chain.invoke({"animal": "dog"})
```
{% endraw %}

In this example, when you run the chain with `my_handler`, you'll see messages printed before the LLM call and after it. This helps you trace the execution flow directly in your terminal. Without the callback, you only see the final result, making it harder to debug intermediate steps.

#### Pros of LangChain Callbacks

*   **High Customization:** You have complete control over what happens during each event. You can log, store, or even modify data as it passes through your chain. This makes them excellent observability tools for specific needs.
*   **Local Control:** Callbacks run directly within your application's process. You don't need an external service, which is great for local development and testing. This also means no external network latency.
*   **Simple Setup for Basic Needs:** For simple logging or monitoring a few specific events, setting up a `BaseCallbackHandler` is straightforward. You can quickly add monitoring without much overhead.
*   **No Cost (Typically):** Since they run locally, there are no additional service costs associated with using LangChain callbacks. This is a significant advantage for budget-conscious projects or personal exploration.
*   **Flexibility for Advanced Use Cases:** You can build complex systems on top of callbacks, like custom metrics collection or real-time alerts. For instance, you could implement a custom output parser that uses a callback to validate output, as discussed in [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}).

#### Cons of LangChain Callbacks

*   **Limited Visualization:** Callbacks typically output to a console or log file. They don't offer a rich, visual interface for understanding complex chains. You need to parse text logs yourself.
*   **No Centralized Storage:** If your application runs across multiple machines or needs historical data, you'll have to build your own storage solution. This adds complexity and maintenance burden.
*   **Manual Aggregation:** Understanding trends or common failure points requires manually analyzing logs, which can be time-consuming. You lose the benefit of automatic data aggregation.
*   **Complexity for Large Systems:** While flexible, building a comprehensive monitoring system with callbacks for a large-scale, multi-user application can become very complex. You might need to integrate with external observability tools manually.
*   **Difficulty in Collaboration:** Sharing and discussing traces with team members is harder when monitoring relies on local logs. There's no single source of truth or shared interface.

### What is LangSmith Tracing?

LangSmith Tracing is a specialized platform built by the creators of LangChain to provide deep visibility into your LLM applications. It's more than just logging; it's a dedicated observability tool designed for the unique challenges of AI development. LangSmith acts like a flight recorder for your LangChain application.

Every action, thought, and interaction within your chain or agent is recorded as a "span" and grouped into a "trace." These traces are then sent to the LangSmith platform, where you can view them in a user-friendly web interface. This offers a powerful monitoring comparison against simple callbacks.

LangSmith helps you debug, test, and evaluate your LLM applications more effectively. It provides a visual timeline of your chain's execution, showing you exactly what happened at each step. This makes LLM debugging much more intuitive and collaborative.

#### How LangSmith Tracing Works

When you enable LangSmith in your LangChain application, every component within your chain automatically sends data to the LangSmith cloud service. This data includes inputs, outputs, timestamps, errors, and metadata for each operation. It creates a detailed timeline of events.

Each operation, like calling an LLM, using a tool, or running a chain, becomes a "span." These spans are organized hierarchically into a "trace," representing one complete run of your application. You can think of a trace as the entire journey of a single request through your system.

The LangSmith UI then visualizes these traces, allowing you to click into each span to see its details. You can inspect prompts, responses, intermediate steps, and even tool calls. This centralized, visual approach vastly improves your ability to analyze and debug your applications.

#### Practical Example: Setting Up LangSmith Tracing

To use LangSmith, you first need to sign up for an account on their website (smith.langchain.com) and get an API key. Then, you set up a few environment variables in your development environment. This allows your LangChain application to automatically send traces to your LangSmith project.

{% raw %}
```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain import hub

# Set LangSmith environment variables
# You would get these from your LangSmith account
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
# os.environ["LANGCHAIN_PROJECT"] = "My First LangChain Project" # Or whatever you want to name your project

# Make sure you also have your OpenAI API key set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Define your LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define a simple tool (e.g., a calculator-like function)
def multiply(a: int, b: int) -> int:
    """Multiplies two integers."""
    return a * b

tools = [
    Tool(
        name="Multiply",
        func=lambda x: multiply(int(x.split(',')[0]), int(x.split(',')[1])),
        description="Useful for when you need to multiply two numbers. Input should be two comma-separated integers, e.g., '2,3'",
    )
]

# Get the prompt for the ReAct agent
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Invoke the agent
print("--- Invoking agent with LangSmith Tracing enabled ---")
agent_executor.invoke({"input": "What is 7 times 8?"})

print("\n--- Invoking agent with a different question ---")
agent_executor.invoke({"input": "What is the capital of France?"})

```
{% endraw %}

When you run this code *with the LangSmith environment variables set*, it will execute your agent. While the `verbose=True` prints some output to your console, the real magic happens in LangSmith. You can then go to `smith.langchain.com` (or your self-hosted instance) and navigate to your project. There, you will find detailed traces of each agent execution, including the LLM calls, tool uses, and intermediate thoughts.

You'll see a visual representation of how the agent decided to use the "Multiply" tool. This level of detail is invaluable for LLM debugging. It allows you to quickly pinpoint where an agent might be making incorrect decisions.

#### Pros of LangSmith Tracing

*   **Rich Visualization:** LangSmith provides a beautiful, interactive UI that displays traces as a timeline. You can easily see the flow, inputs, outputs, and errors for every step. This makes debugging complex chains much easier.
*   **Centralized Storage & History:** All your traces are stored securely in the LangSmith platform. This means you have a historical record of your application's behavior. You can revisit past runs, compare them, and analyze performance over time.
*   **Collaboration Features:** The web UI makes it easy to share traces with team members. Everyone can access the same debugging information, fostering better collaboration. This is a crucial aspect of modern observability tools.
*   **Advanced Evaluation & Monitoring:** Beyond just tracing, LangSmith offers tools for dataset creation, testing, evaluation, and even A/B testing different prompts or models. This moves beyond simple monitoring comparison to full-fledged MLops for LLMs.
*   **Built-in LLM Debugging:** It's specifically designed for LangChain and LLM applications, meaning it understands the nuances of LLM calls, chain types, and agent steps. This specialized focus helps with precise LLM debugging.
*   **Performance Metrics:** LangSmith automatically collects metrics like latency and token usage for each step. This allows you to identify bottlenecks and optimize your application's performance.

#### Cons of LangSmith Tracing

*   **Requires an External Service:** LangSmith is a cloud-based platform (or self-hosted enterprise solution). This means you need an internet connection and may incur costs depending on your usage plan. It's not purely local.
*   **Learning Curve:** While user-friendly, getting the most out of LangSmith's advanced features might require a bit of a learning curve. Understanding traces, datasets, and evaluations takes time.
*   **Potential for Data Privacy Concerns:** Since traces are sent to an external service, you need to consider data privacy and security. Ensure you're comfortable sending your application's intermediate data to a third-party platform, especially for sensitive information.
*   **Can Be Overkill for Simple Projects:** For very small, personal projects with straightforward chains, the full power of LangSmith might be more than you need. LangChain callbacks could be sufficient in such cases.
*   **Dependency on LangSmith Ecosystem:** While tightly integrated with LangChain, it means you're somewhat tied to their ecosystem for advanced monitoring. If you decide to use [top LangChain alternatives]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}), you might need different monitoring solutions.

### LangChain Callbacks vs LangSmith Tracing: A Closer Look

Now let's dive deeper into a direct monitoring comparison between LangChain callbacks vs LangSmith tracing across several key aspects. This will help you decide which one aligns better with your project's needs.

#### Ease of Setup

*   **LangChain Callbacks:** Setting up basic callbacks is very easy. You define a Python class, override a few methods, and pass it to your chain. It's all within your existing codebase, requiring no external accounts or configurations. This makes them quick to implement for local, ad-hoc debugging.
*   **LangSmith Tracing:** Requires a bit more initial setup. You need to create a LangSmith account, get an API key, and set environment variables. Once done, tracing is often automatic for many LangChain components. However, the initial hurdle is slightly higher than for simple callbacks.

#### Level of Detail / Scope

*   **LangChain Callbacks:** You control precisely what events you want to capture and what information you extract. You can get very granular, but you must manually code every piece of data you want to log. The scope is defined by what you explicitly implement.
*   **LangSmith Tracing:** Captures a comprehensive, standardized set of data for every operation by default. This includes inputs, outputs, tokens, latency, errors, and metadata. It provides a holistic view of the entire chain run without you having to write specific logging code for each piece of information.

#### Data Storage and Persistence

*   **LangChain Callbacks:** Data captured by callbacks is typically ephemeral (printed to console) or stored in files you manage. There's no built-in mechanism for persistent, structured storage across multiple runs or users. You'd need to integrate with a database or logging system yourself.
*   **LangSmith Tracing:** All traces and spans are automatically stored in the LangSmith cloud platform. This provides a persistent, searchable history of all your application's runs. You can easily go back in time, review specific interactions, and analyze trends.

#### Visualization and User Interface (UI)

*   **LangChain Callbacks:** Generally offer no built-in visualization. You interact with text logs in your terminal or a log file. To visualize data, you would need to export it and use another tool like a spreadsheet or a custom dashboard. This requires more effort for effective monitoring comparison.
*   **LangSmith Tracing:** Provides a powerful web-based UI that visually represents your traces. You see a clear hierarchy of steps, timelines, and details for each operation. This visual approach is incredibly helpful for understanding complex agentic flows, especially for tools like [LangGraph StateGraph Multi-Step AI Agent]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

#### Debugging Capabilities (LLM Debugging)

*   **LangChain Callbacks:** Excellent for breakpoint-style debugging where you want to inspect variables at specific points during execution. You can insert `print()` statements or use a debugger. However, understanding the *overall flow* of a complex chain from console logs can be challenging.
*   **LangSmith Tracing:** Offers superior LLM debugging for complex applications. Its visual timeline lets you quickly identify where an agent went off track, which tool it called incorrectly, or which LLM prompt led to a bad response. You can pinpoint errors and understand the reasoning process more efficiently.

#### Cost

*   **LangChain Callbacks:** Free to use, as they run entirely within your application. The only costs would be associated with any external logging systems you integrate them with.
*   **LangSmith Tracing:** LangSmith offers a free tier, but for higher usage volumes or advanced features, it typically involves a subscription cost. The pricing model is usually based on the number of traces or tokens. It's a managed service, so you pay for the convenience and features.

#### Customization

*   **LangChain Callbacks:** Highly customizable. You write the code, so you can make it do almost anything at each event. This includes modifying data, performing custom validations, or triggering alerts based on specific conditions. This flexibility is a core advantage.
*   **LangSmith Tracing:** While it collects a lot of data automatically, advanced customization within the LangSmith UI or data pipeline is less direct. You can add custom tags or metadata to traces, but modifying the core tracing behavior requires interacting with the LangSmith API or framework.

#### Scalability

*   **LangChain Callbacks:** Managing logs from callbacks across many concurrent users or distributed applications can be challenging. You need a robust logging infrastructure (e.g., ELK stack, Splunk) to collect, aggregate, and analyze logs effectively at scale.
*   **LangSmith Tracing:** Designed for scalability. It handles collecting and storing traces from many concurrent requests across distributed systems. The platform takes care of the infrastructure, allowing you to focus on developing your application rather than managing your observability tools.

#### Integration with Other Observability Tools

*   **LangChain Callbacks:** Can be integrated with virtually any observability tool. You can write a callback handler that sends data to Prometheus, Grafana, Datadog, or your custom analytics platform. The integration requires manual coding for each specific tool.
*   **LangSmith Tracing:** Is a comprehensive observability tool in itself, providing many features typically found in separate tools. While it can export data, its primary design is to be a self-contained monitoring and evaluation platform for LLMs.

### When to Use LangChain Callbacks?

You might choose LangChain callbacks for several specific scenarios where their simplicity and direct control are most beneficial. They are excellent for quick, local insights into your LLM applications.

Use callbacks when you need immediate, in-process feedback during development. If you're building a new chain and just want to see the intermediate prompts and responses as you test, a simple callback can print this information to your console. This is perfect for initial LLM debugging without needing an external service.

Callbacks are also ideal for highly customized logging or specific actions. For instance, you might want to log only specific errors to a custom file format or trigger an alert if a certain token count is exceeded. Since you write the callback code, you have complete freedom to define these custom behaviors.

If your project has strict data privacy requirements or operates in an air-gapped environment, callbacks are a good choice. They keep all data within your control, as no information leaves your local system. This ensures sensitive data remains secure and compliant with internal policies.

For small projects or proof-of-concepts, where setting up a full external monitoring solution might be overkill, callbacks offer a lightweight alternative. They provide enough visibility to get the job done without adding complexity or cost. Think of a simple [build RAG applications LangChain vector store]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}) where you just need to ensure the retriever is working.

Finally, consider callbacks if you're integrating with an existing enterprise logging infrastructure. You can write a callback that formats LangChain events into your company's standard log format and sends them to your existing logging system. This leverages existing observability tools without introducing new platforms.

### When to Use LangSmith Tracing?

LangSmith tracing becomes indispensable as your LLM applications grow in complexity, scope, or team size. It's designed for serious development, deployment, and ongoing maintenance of AI systems.

You should definitely use LangSmith when you are working on complex agents or multi-step chains. Projects involving [LangGraph StateGraph Multi-Step AI Agent]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}) or [LangChain Google Gemini function calling agent custom tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}) generate intricate execution paths. LangSmith's visual traces make it much easier to understand and debug these complex interactions, which would be nearly impossible with raw logs.

For teams collaborating on LLM applications, LangSmith is a game-changer. It provides a shared platform where everyone can view, analyze, and discuss traces. This centralized view significantly improves team efficiency and speeds up debugging cycles, promoting better communication among developers.

If you need robust evaluation and testing capabilities, LangSmith is the clear choice. It allows you to create datasets from your traces, run automated tests, and compare different models or prompt versions. This is crucial for systematically improving your application's performance and reliability, going beyond simple monitoring comparison.

When your application is deployed in production, LangSmith offers essential ongoing monitoring. You can track performance metrics, identify regressions, and quickly diagnose issues that arise in a live environment. Its historical data and visualization are invaluable for maintaining high-quality service.

Finally, use LangSmith if you need to optimize your LLM application for cost and speed. It automatically collects token usage and latency metrics for each step. This data helps you identify expensive or slow parts of your chain, enabling targeted optimizations, especially relevant for services like [LangChain Weaviate hybrid search scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}) where query costs can vary.

### Hybrid Approach: Can They Work Together?

Yes, LangChain callbacks and LangSmith tracing are not mutually exclusive; they can absolutely work together! In fact, combining them can offer the best of both worlds. You can leverage the detailed, visual tracing of LangSmith while also implementing specific, custom actions with callbacks.

For example, you can enable LangSmith tracing globally for comprehensive monitoring and LLM debugging. This gives you all the benefits of centralized storage, visualization, and evaluation for your team. You get a complete picture of your application's performance and behavior.

At the same time, you might implement a very specific custom callback for a particular component or event. Perhaps you have a custom output parser where you need to perform an immediate, critical validation step before the output is passed to the next chain. You could use a `BaseCallbackHandler` for this validation, as demonstrated in [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}), which works alongside LangSmith tracing.

Another use case could be a callback that pushes specific, aggregated metrics to your company's existing dashboard solution. While LangSmith provides its own metrics, you might have legacy systems that rely on a particular format. Your custom callback can act as a bridge, sending tailored data without disrupting LangSmith's comprehensive tracing.

This hybrid approach allows you to capture the broad, visual context provided by LangSmith for overall observability. Simultaneously, you can use callbacks for niche, real-time, or highly specialized actions that don't need to be part of the general trace. It ensures you have fine-grained control where it matters most, while benefiting from a powerful managed service for everything else.

### Practical Examples and Walkthroughs

Let's explore some more detailed practical examples for both LangChain callbacks and LangSmith tracing. These examples will illustrate how each approach provides visibility into your LangChain applications.

#### Example 1: Custom Callback for Detailed Tool Monitoring

Imagine you have an agent that uses multiple tools. You want to specifically monitor the inputs and outputs of each tool call, perhaps even logging it to a custom file or checking for specific patterns. LangChain callbacks are perfect for this targeted monitoring.

We'll define a custom callback that logs tool inputs and outputs. This allows for specific LLM debugging related to tool usage.

{% raw %}
```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain import hub
from langchain_core.callbacks import BaseCallbackHandler, CallbackManager

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Define a custom tool callback handler
class ToolLoggerCallback(BaseCallbackHandler):
    def on_tool_start(self, serialized: dict, input_str: str, **kwargs):
        """Called when a tool starts running."""
        tool_name = serialized.get("name", "Unknown Tool")
        print(f"\n--- Tool '{tool_name}' Started ---")
        print(f"Tool input: '{input_str}'")

    def on_tool_end(self, output: str, **kwargs):
        """Called when a tool ends running."""
        print(f"Tool output: '{output}'")
        print(f"--- Tool Ended ---\n")

# Define your LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define tools
def add_numbers(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

def subtract_numbers(a: int, b: int) -> int:
    """Subtracts two integers."""
    return a - b

tools = [
    Tool(
        name="Add",
        func=lambda x: add_numbers(int(x.split(',')[0]), int(x.split(',')[1])),
        description="Useful for when you need to add two numbers. Input should be two comma-separated integers, e.g., '2,3'",
    ),
    Tool(
        name="Subtract",
        func=lambda x: subtract_numbers(int(x.split(',')[0]), int(x.split(',')[1])),
        description="Useful for when you need to subtract two numbers. Input should be two comma-separated integers, e.g., '5,2'",
    )
]

# Get the prompt for the ReAct agent
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create an agent executor and pass the custom callback manager
# You can pass multiple callbacks in a list to CallbackManager
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    # Here we pass our custom callback handler
    callback_manager=CallbackManager([ToolLoggerCallback()])
)

# Invoke the agent with a question that requires tool use
print("--- Invoking agent with tool logging callback ---")
agent_executor.invoke({"input": "What is 10 plus 5 minus 2?"})

print("\n--- Invoking agent with a different question ---")
agent_executor.invoke({"input": "What is the result of 100 minus 30 plus 15?"})
```
{% endraw %}

When you run this code, you'll see your `ToolLoggerCallback` spring into action. It will print messages indicating when a tool starts, what input it received, and what output it produced. This provides a very clear, step-by-step breakdown of how your agent interacts with its tools, which is crucial for monitoring comparison and effective LLM debugging.

#### Example 2: Using LangSmith for Comprehensive Agent Debugging

Now, let's enable LangSmith tracing for a similar agent scenario. Instead of just seeing tool logs in the console, we'll see a complete visual trace of the agent's thought process, LLM calls, and tool interactions. This requires setting up your LangSmith environment variables.

{% raw %}
```python
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain import hub

# Set LangSmith environment variables
# IMPORTANT: Replace with your actual API key and project name
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
# os.environ["LANGCHAIN_PROJECT"] = "Advanced Agent Debugging"

# Make sure you also have your OpenAI API key set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Define your LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define tools
def search_web(query: str) -> str:
    """Searches the web for the given query."""
    print(f"--- Performing web search for: '{query}' ---")
    # In a real application, this would call a search API
    if "capital of france" in query.lower():
        return "Paris is the capital of France."
    elif "highest mountain" in query.lower():
        return "Mount Everest is the highest mountain."
    else:
        return f"No specific information found for '{query}'."

def calculate_expression(expression: str) -> str:
    """Evaluates a mathematical expression."""
    print(f"--- Calculating expression: '{expression}' ---")
    try:
        return str(eval(expression)) # Be careful with eval in production!
    except Exception as e:
        return f"Error calculating: {e}"

tools = [
    Tool(
        name="WebSearch",
        func=search_web,
        description="Useful for when you need to answer questions by searching the web. Input should be a search query.",
    ),
    Tool(
        name="Calculator",
        func=calculate_expression,
        description="Useful for when you need to evaluate mathematical expressions. Input should be a valid mathematical expression, e.g., '2*3+5'.",
    )
]

# Get the prompt for the ReAct agent
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Invoke the agent
print("--- Invoking agent with LangSmith Tracing ---")
agent_executor.invoke({"input": "What is the capital of France and what is 15 plus 7?"})

print("\n--- Invoking agent with a complex query ---")
agent_executor.invoke({"input": "What is 25 divided by 5, and then multiplied by the number of continents on Earth?"})
```
{% endraw %}

When you run this code *with LangSmith environment variables configured*, it will execute the agent. You'll see some verbose output in your terminal, but the true power lies on the LangSmith platform. Go to your LangSmith project, and you will find detailed traces for each invocation.

For the query "What is the capital of France and what is 15 plus 7?", you'll see:
1.  The initial agent thought process.
2.  An LLM call for reasoning.
3.  The agent deciding to use the "WebSearch" tool with "capital of France" as input.
4.  The output from the "WebSearch" tool.
5.  Another LLM call for reasoning.
6.  The agent deciding to use the "Calculator" tool with "15 + 7" as input.
7.  The output from the "Calculator" tool.
8.  The final LLM call to synthesize the answer.

This visual breakdown makes it incredibly easy to follow the agent's logic. If the agent makes a mistake, you can pinpoint exactly which LLM call or tool usage led to the incorrect step. This level of detail in monitoring comparison is unparalleled for LLM debugging.

### Advanced Monitoring with LangSmith

LangSmith goes far beyond simple tracing to provide a complete platform for LLM operations. Once you have traces, you can use them for more advanced scenarios.

For instance, you can take a set of successful traces and turn them into a "dataset." This dataset can then be used to evaluate changes to your prompts, models, or retrieval strategies. If you're building sophisticated RAG applications, perhaps with [LangChain Weaviate hybrid search scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}), you can compare how different embeddings or search algorithms affect answer quality.

LangSmith allows you to run "evaluators" against your datasets. These can be human evaluators or even AI-powered evaluators that score the quality of your application's responses. This is a critical step for continuous improvement and ensuring your LLM application meets performance targets. You can track metrics over time, identifying when changes cause regressions or improvements.

Moreover, LangSmith supports A/B testing different versions of your chains or agents. You can deploy two versions simultaneously and see which one performs better based on user feedback or automated evaluations. This data-driven approach is essential for optimizing complex systems and understanding the true impact of your modifications.

### Making Your Choice: A Monitoring Comparison Summary

Here's a quick summary table to help you with your monitoring comparison and decide between LangChain callbacks vs LangSmith tracing:

| Feature                   | LangChain Callbacks                               | LangSmith Tracing                                  |
| :------------------------ | :------------------------------------------------ | :------------------------------------------------- |
| **Primary Use**           | Local debugging, custom logging, specific actions | Comprehensive monitoring, evaluation, collaboration |
| **Setup**                 | Easy, in-code                                     | External account + env vars                         |
| **Data Storage**          | Local (console/files), manual persistence         | Centralized, persistent in cloud                    |
| **Visualization**         | None (text logs)                                  | Rich, interactive web UI                           |
| **LLM Debugging**         | Step-by-step console inspection, breakpoints      | Visual timeline, error pinpointing                 |
| **Cost**                  | Free                                              | Free tier, then paid subscription                  |
| **Collaboration**         | Difficult (shared logs)                           | Excellent (shared platform)                        |
| **Scalability**           | Requires custom logging infrastructure            | Built-in for distributed applications              |
| **Advanced Features**     | Highly customizable local actions                 | Datasets, evaluations, A/B testing, metrics        |
| **Data Control/Privacy**  | Full local control                                | External service (consider privacy)                |

### Conclusion

Both LangChain callbacks and LangSmith tracing are valuable observability tools for your LLM applications. Your choice between them, or even using a hybrid approach, depends entirely on your project's specific needs, complexity, and team structure. Understanding the differences between LangChain callbacks vs LangSmith tracing is key to making an informed decision.

For simple, local development, or very specific custom logging requirements, LangChain callbacks offer a straightforward and free solution. They give you direct, granular control over specific events within your code. This is perfect for initial experimentation and quick LLM debugging.

However, as your LangChain applications grow more complex, involve multiple developers, or move into production, LangSmith tracing becomes the superior choice. Its centralized, visual monitoring, evaluation features, and collaboration tools significantly enhance your ability to build, debug, and optimize robust LLM systems. LangSmith is designed to be a comprehensive platform, moving beyond basic monitoring comparison to full lifecycle management for AI applications.

Ultimately, the best monitoring approach is the one that gives you the clearest understanding of your application's behavior and helps you solve problems most efficiently. Whether you opt for the simplicity of callbacks, the power of LangSmith, or a combination of both, investing in good observability tools will save you time and frustration in your LLM development journey.