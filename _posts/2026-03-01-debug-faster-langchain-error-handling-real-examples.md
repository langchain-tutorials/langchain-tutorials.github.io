---
title: "Debug Faster: LangChain Error Handling Best Practices with Real Examples"
description: "Stop struggling! Learn LangChain error handling examples and best practices to debug LangChain applications faster. Build reliable AI agents with confidence."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [debug langchain error handling examples]
featured: false
image: '/assets/images/debug-faster-langchain-error-handling-real-examples.webp'
---

## Debug Faster: LangChain Error Handling Best Practices with Real Examples

Building things with LangChain is super exciting because it helps you make smart apps. But sometimes, these apps don't work exactly as you expect them to. When this happens, it can feel like trying to find a tiny needle in a big haystack. This guide will help you learn how to debug langchain error handling examples faster, like a detective solving a mystery.

You will discover powerful tips and tricks to fix problems quickly. We'll explore common error examples and show you how to solve them step-by-step. Get ready to become a LangChain debugging master.

### Why Debugging LangChain Matters

Imagine you're building a robot friend using LangChain that can chat with people. If your robot starts saying silly things or stops talking completely, you need to find out why. Debugging is like checking your robot's brain to see what went wrong. It helps you understand the problem and make your app work perfectly again.

Knowing how to debug langchain error handling examples is a very important skill. It saves you time and makes sure your awesome projects are reliable. Let's start with some simple yet powerful `debugging techniques` that anyone can use.

### Basic Debugging Tools You Can Use Today

When you start to `debug langchain error handling examples`, you don't always need fancy tools. Sometimes, the best solutions are the simplest ones. We'll look at how to use these everyday tools effectively. These techniques form the foundation for all your future debugging efforts.

#### Use Verbose Mode: Your LangChain X-Ray Vision

One of the easiest ways to see what LangChain is doing inside is by turning on "verbose mode." Think of it like giving your LangChain app X-ray vision. It will print out a lot of helpful information about each step it takes. This can reveal where things might be going wrong.

When you see all the steps, you can pinpoint the exact moment an error happens. This is a crucial first step in any `real-world troubleshooting` scenario. Let's see how you can use `verbose mode usage`.

##### How to Enable Verbose Mode

You can turn on verbose mode when you create your LangChain object, like a chain or an agent. You just set `verbose=True`. It's that simple to get a peek behind the scenes. This little trick provides a ton of information to help you `debug langchain error handling examples`.

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Make sure you have your OpenAI API key set up!
# import os
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

llm = OpenAI(temperature=0) # temperature=0 means it tries to give the same answer each time
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Tell me a fun fact about {topic}.",
)

# See the magic here! verbose=True
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# Now, run the chain and watch the output!
print("--- Running LangChain with Verbose Mode ---")
chain.run("cats")
print("--- Finished Verbose Run ---")
```

When you run this code, you'll see many lines of text printed to your screen. This text shows you the prompt being sent to the LLM (Large Language Model) and the response coming back. If there's an error, you'll often see it pop up right in the middle of this detailed output. This detailed output is invaluable for `debug langchain error handling examples`.

##### Understanding Verbose Output

The verbose output usually shows you:
*   **The prompt:** What text was actually sent to the AI model.
*   **The LLM call:** Details about the model being used and its settings.
*   **The response:** What the AI model answered.
*   **Intermediate steps:** If you have a complex chain, it shows each step.

By looking at these steps, you can often spot if the prompt was wrong, if the model gave an unexpected answer, or if an API call failed. This makes `trace analysis` much easier, even without fancy tools.

#### Print Statements: Your Go-To Detective Notes

Sometimes, you need to know the value of a specific variable at a certain point in your code. Just like writing notes to yourself, `print()` statements let you see these values. They are super helpful for `error isolation` and checking your assumptions. This is a very common and effective `debugging technique`.

You can add `print()` statements almost anywhere in your Python code. They are great for checking inputs, outputs, or any intermediate data. This simple method can provide quick insights when you `debug langchain error handling examples`.

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0)
prompt = PromptTemplate(
    input_variables=["animal"],
    template="What sound does a {animal} make?",
)

chain = LLMChain(llm=llm, prompt=prompt)

animal_input = "dog"
print(f"--- Input for the chain: {animal_input} ---") # Print statement 1

try:
    result = chain.run(animal_input)
    print(f"--- Output from the chain: {result} ---") # Print statement 2
except Exception as e:
    print(f"--- An error occurred: {e} ---") # Print statement 3 for errors
```

Here, you use print statements to track the input you're giving to the chain and the output you get back. If an error happens, the `except` block catches it and prints the error message. This helps you narrow down where the problem is.

##### When to Use Print Statements

*   **Checking inputs:** Make sure your data looks correct before it goes into a LangChain component.
*   **Checking outputs:** See if the component is returning what you expect.
*   **Tracking flow:** Understand which parts of your code are actually running.
*   **Variable inspection:** Quickly see the value of any variable at any time.

Print statements are a basic but powerful part of `debugging techniques`. They are especially useful when you're trying to achieve `error isolation` in a complex system.

#### Debugging Callbacks: Advanced Detective Tools

LangChain offers a cool feature called "callbacks." Callbacks are like special agents you can attach to your LangChain components. They get notified whenever something interesting happens, like an LLM call starts, or a chain finishes. This is an advanced way to get detailed information, even more so than verbose mode.

Using `debugging callbacks` gives you fine-grained control over what information you want to see. You can log specific events or even modify behavior. This is extremely useful for complex `debug langchain error handling examples`. For more about callbacks, you might want to read our blog post on [Mastering LangChain Callbacks](/blog/mastering-langchain-callbacks.md).

##### How Callbacks Work

You create a special "callback handler" object. Then, you pass this object to your LangChain chain or agent. The handler has methods like `on_llm_start`, `on_chain_end`, or `on_tool_error`. LangChain calls these methods automatically during its operation.

This allows you to create custom `debugging techniques` that log exactly what you need. It's much more flexible than just `verbose mode usage`.

```python
from langchain.callbacks.base import BaseCallbackHandler
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import time

class MyDebugCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized: dict, prompts: list, **kwargs) -> None:
        """Run when LLM starts running."""
        print(f"\n--- LLM START (Prompts: {prompts}) ---")

    def on_llm_end(self, response, **kwargs) -> None:
        """Run when LLM ends running."""
        print(f"--- LLM END (Response: {response.generations[0][0].text.strip()[:50]}...) ---")

    def on_chain_start(self, serialized: dict, **kwargs) -> None:
        """Run when chain starts running."""
        print(f"\n--- CHAIN START (Type: {serialized['lc_kwargs']['name']}) ---")

    def on_chain_end(self, outputs: dict, **kwargs) -> None:
        """Run when chain ends running."""
        print(f"--- CHAIN END (Outputs: {outputs}) ---\n")

    def on_tool_start(self, serialized: dict, input_str: str, **kwargs) -> None:
        """Run when tool starts running."""
        print(f"\n--- TOOL START (Tool: {serialized['name']}, Input: {input_str}) ---")

    def on_tool_end(self, output: str, **kwargs) -> None:
        """Run when tool ends running."""
        print(f"--- TOOL END (Output: {output}) ---")

    def on_agent_action(self, action, **kwargs) -> None:
        """Run on agent action."""
        print(f"\n--- AGENT ACTION (Action: {action.log}) ---")

    def on_agent_finish(self, finish, **kwargs) -> None:
        """Run on agent finish."""
        print(f"\n--- AGENT FINISH (Finish: {finish.log}) ---")

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """Run when LLM errors."""
        print(f"\n--- LLM ERROR: {error} ---")

    def on_chain_error(self, error: Exception, **kwargs) -> None:
        """Run when chain errors."""
        print(f"\n--- CHAIN ERROR: {error} ---")

    def on_tool_error(self, error: Exception, **kwargs) -> None:
        """Run when tool errors."""
        print(f"\n--- TOOL ERROR: {error} ---")


llm = OpenAI(temperature=0)
prompt = PromptTemplate(
    input_variables=["query"],
    template="Explain {query} in simple terms.",
)

# Pass your custom callback handler here
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[MyDebugCallback()])

print("\n--- Running LangChain with Custom Callback ---")
chain.run("gravity")
print("--- Finished Callback Run ---")

# Example with an error (e.g., if API key was wrong, or network issue)
# Let's simulate an error by making a bad LLM call (though this won't trigger on_llm_error in this setup directly without a specific API failure)
# For a real error, you might remove your API key temporarily or cause a network issue.
try:
    print("\n--- Running LangChain with Custom Callback (Potential Error Scenario) ---")
    # This won't actually throw an LLM error via callback without a real underlying issue,
    # but demonstrates how callbacks are passed.
    # To truly see on_llm_error, you'd need a failing LLM call (e.g., bad API key, network error)
    # llm_bad = OpenAI(temperature=0, openai_api_key="BAD_KEY") # This would cause an API error
    # chain_bad = LLMChain(llm=llm_bad, prompt=prompt, callbacks=[MyDebugCallback()])
    # chain_bad.run("quantum physics")
    print("--- Simulating an error here would trigger on_llm_error if an actual API error occurred ---")
except Exception as e:
    print(f"Caught an external error: {e}")
print("--- Finished Potential Error Scenario ---")
```

This custom callback prints messages when the LLM starts and ends, and when the chain starts and ends. It also includes methods for `on_llm_error`, `on_chain_error`, and `on_tool_error`. This helps you see the flow of your application and catch errors specifically within these components. It's a powerful way to `debug langchain error handling examples` with great detail.

### Advanced Debugging with LangSmith

While `verbose mode usage` and `debugging callbacks` are great, sometimes you need even more power. This is where `LangSmith debugging` comes in. LangSmith is a special platform built by the creators of LangChain to help you understand, test, and debug your applications better. It’s like having a super-smart assistant for `real-world troubleshooting`.

LangSmith gives you a visual timeline of everything your LangChain app does. You can see every prompt, every AI response, and every tool call. This is incredibly useful for `trace analysis` and understanding complex chains. For setting up LangSmith, you can refer to the official LangChain documentation.

#### What is LangSmith and How It Helps

LangSmith acts like a flight recorder for your LangChain applications. Every time your chain or agent runs, LangSmith records all the details. It shows you exactly what happened, step by step. This makes `error isolation` much easier because you can visually trace the execution path.

It’s especially good for `debug langchain error handling examples` that are complex, involving many steps or tools. You can also use it for `error reproduction`, helping you see if a fixed error stays fixed.

##### Enabling LangSmith

First, you need to sign up for LangSmith and set up your environment variables.
```bash
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="your_langsmith_api_key"
export LANGCHAIN_PROJECT="Your_Project_Name" # (optional)
```

Once these are set, your LangChain runs will automatically be sent to LangSmith.

#### Trace Analysis: Following the Breadcrumbs

When you run your LangChain app with LangSmith enabled, it creates a "trace." A trace is a detailed record of an entire run. You can then go to the LangSmith website and look at these traces. Each trace shows a clear timeline of events.

With `trace analysis`, you can:
*   **See the full path:** Understand how your data flows through different components.
*   **Inspect inputs/outputs:** Check the exact data exchanged at each step.
*   **Identify bottlenecks:** Find out which part of your chain is taking too long.
*   **Locate errors:** Pinpoint exactly where an error occurred in the sequence.

This visual breakdown is incredibly powerful for `debug langchain error handling examples`, especially when dealing with intricate chains or agent behaviors.

#### Error Reproduction with LangSmith

One of the hardest parts of `real-world troubleshooting` is getting an error to happen again, especially if it only happens sometimes. LangSmith helps with `error reproduction` by letting you replay past runs. If a user reported a bug, you can look up their specific trace.

You can even "share" a problematic trace with others on your team. This means everyone can see the exact same conditions that led to the error. This makes solving tough `common error examples` much faster.

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Ensure LANGCHAIN_TRACING_V2 and LANGCHAIN_API_KEY are set in your environment variables

llm = OpenAI(temperature=0)
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a short poem about {topic}.",
)

chain = LLMChain(llm=llm, prompt=prompt)

print("--- Running LangChain with LangSmith (Check your LangSmith UI) ---")
chain.run("butterflies")
print("--- Finished LangSmith Run ---")

# If an error occurs (e.g., bad API key, or unexpected output from a tool)
# LangSmith would capture this error in the trace.
# You would then go to the LangSmith UI to inspect the specific trace where the error happened.
# This makes it much easier to debug langchain error handling examples by seeing the full context.

try:
    # Simulate an error - for example, if the LLM couldn't connect or gave a malformed response
    # In a real scenario, this would be an actual exception from the LLM.
    llm_error = OpenAI(openai_api_key="sk-BADKEY") # Intentionally bad key
    chain_error = LLMChain(llm=llm_error, prompt=prompt)
    print("\n--- Running LangChain with LangSmith (Simulated Error) ---")
    chain_error.run("ocean")
except Exception as e:
    print(f"--- Caught expected error: {e} ---")
    # Even if caught here, LangSmith will record the trace and the error.
    print("Check LangSmith UI for the trace of this error.")

```
When you run the code with a bad API key, LangSmith will capture the entire trace, including the API key error. You can then go to the LangSmith UI, find this trace, and see the specific error message and context. This helps you `debug langchain error handling examples` related to API issues.

### Common LangChain Error Examples and How to Fix Them

Now, let's dive into some `common error examples` you might encounter when working with LangChain. Knowing these will give you a head start in `real-world troubleshooting`. We'll provide practical ways to `debug langchain error handling examples` you are likely to see.

#### H3: API Key Errors: The Gatekeeper Problem

One of the most frequent issues for beginners is incorrect or missing API keys. LangChain needs these keys to talk to services like OpenAI, Anthropic, or others. If the key is wrong, the gate won't open, and your app can't talk to the AI. This is a classic `common error example`.

##### Symptoms
*   You see messages like "Authentication error," "Invalid API key," or "Rate limit exceeded."
*   The LLM doesn't respond, or your chain just stops.

##### How to Debug and Fix
1.  **Check your environment variables:** Most often, you need to set your API key as an environment variable (like `OPENAI_API_KEY`). Make sure it's spelled correctly and is actually present.
    *   **Tip:** If you're using a `.env` file, ensure you load it properly (e.g., `from dotenv import load_dotenv; load_dotenv()`). For more on environment setup, refer to our guide on [Setting Up Your LangChain Environment](/blog/setup-langchain-env.md).
2.  **Verify the key itself:** Double-check that the key you copied from the service provider is complete and correct. Sometimes a character might be missed.
3.  **Permissions and billing:** Make sure your API key has the right permissions and that your billing account with the service provider is active. A "rate limit" error often means you've hit a usage cap or don't have enough credits.

```python
import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# INCORRECT WAY (simulating a missing/bad key)
# Do NOT hardcode your API key like this in real apps! Use environment variables.
# os.environ["OPENAI_API_KEY"] = "sk-thisisnotarealkey" # A deliberately bad key

llm = OpenAI(temperature=0)
prompt = PromptTemplate(
    input_variables=["animal"],
    template="Tell me a joke about a {animal}.",
)

chain = LLMChain(llm=llm, prompt=prompt)

try:
    print("--- Attempting to run with a potentially bad API key ---")
    chain.run("chicken")
except Exception as e:
    print(f"\n!!! Caught an API Key Error: {e} !!!")
    print("This usually means your OPENAI_API_KEY is missing, incorrect, or expired.")
    print("Please check your environment variables or OpenAI account.")

# CORRECT WAY (assuming your environment variable is set)
# os.environ["OPENAI_API_KEY"] = "YOUR_ACTUAL_OPENAI_API_KEY" # Make sure this is correctly set!
# llm_correct = OpenAI(temperature=0)
# chain_correct = LLMChain(llm=llm_correct, prompt=prompt)
# print("\n--- Attempting to run with a CORRECT API key (if set) ---")
# chain_correct.run("dog")
# print("--- Successfully ran with correct key ---")
```

The error message will clearly tell you it's an authentication problem, helping you quickly `debug langchain error handling examples` related to access.

#### Input/Output Formatting Errors: Talking the Wrong Language

LangChain components expect information in a certain way, and they give it back in a certain way. If you give a component the wrong type of input or try to use its output in the wrong way, you'll get a formatting error. This is a common challenge in `real-world troubleshooting`.

##### Symptoms
*   `KeyError`: When you try to access a piece of information that doesn't exist.
*   `TypeError`: When you pass the wrong type of data (e.g., a number instead of text).
*   Messages like "Missing expected input: foo" or "Invalid argument type."

##### How to Debug and Fix
1.  **Read the error message carefully:** It often tells you exactly what input is missing or what type is wrong.
2.  **Use `print()` statements:** Before and after calling a component, print the inputs and outputs. See if they match what the component expects.
3.  **Check documentation:** Refer to the LangChain documentation for the specific component you're using. It will describe the expected inputs and outputs.

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0)
prompt = PromptTemplate(
    input_variables=["name", "job"], # Expects 'name' and 'job'
    template="My name is {name} and I am a {job}.",
)

chain = LLMChain(llm=llm, prompt=prompt)

# PROBLEM 1: Missing an expected input variable
print("\n--- Problem 1: Missing Input Variable ---")
try:
    # We only provide 'name', but 'job' is also expected
    chain.run({"name": "Alice"})
except Exception as e:
    print(f"!!! Caught a Missing Input Error: {e} !!!")
    print("The prompt expects 'job', but it was not provided.")

# PROBLEM 2: Providing the wrong input format (e.g., a list instead of a dict)
print("\n--- Problem 2: Wrong Input Format ---")
try:
    # Chain.run expects a string or a dict for a single input variable,
    # or a dict for multiple. Here, we try to pass a list.
    chain.run(["Bob", "Engineer"])
except Exception as e:
    print(f"!!! Caught a Formatting Error: {e} !!!")
    print("The input should likely be a dictionary like {'name': 'Bob', 'job': 'Engineer'}.")

# CORRECT WAY
print("\n--- Correct Input Formatting ---")
try:
    result = chain.run({"name": "Charlie", "job": "Scientist"})
    print(f"Correct Output: {result}")
except Exception as e:
    print(f"Caught an unexpected error: {e}")
```

These errors show you why `error isolation` is important. By checking the inputs and outputs at each stage, you can quickly find the part that's "talking the wrong language."

#### Agent and Tool Errors: Your Robot is Confused

LangChain agents are like little decision-makers that can choose which "tools" to use. Tools are functions that help the agent do specific tasks, like searching the internet or doing math. If an agent chooses the wrong tool, or a tool doesn't work as expected, you'll get an agent or tool error. This is a prime area for `debugging techniques`.

##### Symptoms
*   The agent gets stuck in a loop.
*   It chooses a tool that doesn't exist.
*   A tool returns an error message.
*   The agent provides a nonsensical answer.

##### How to Debug and Fix
1.  **Use `verbose=True`:** This is crucial for agents! It shows you the agent's "thought process" and which tools it's trying to use.
2.  **Inspect tool definitions:** Make sure your tools are defined correctly and their descriptions are clear for the agent.
3.  **Check tool inputs/outputs:** Use `print()` statements inside your tools to see what input they receive and what they return.
4.  **LangSmith `trace analysis`:** For complex agents, LangSmith traces are invaluable to see the full sequence of agent thoughts and tool calls.

```python
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.llms import OpenAI

# A simple "tool" that adds two numbers
def add_numbers(num1: str, num2: str) -> str:
    """Adds two numbers together. Input must be two numbers separated by a comma, e.g., '1,2'"""
    try:
        n1, n2 = map(float, num1.split(',')) # Expects input like "1,2"
        return str(n1 + n2)
    except ValueError:
        return "Error: Invalid input. Please provide two numbers separated by a comma."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# A simple "tool" that just returns a fixed error
def always_fails_tool(query: str) -> str:
    """A tool that always fails for demonstration."""
    raise ValueError("This tool is designed to always fail!")

tools = [
    Tool(
        name="Add Two Numbers",
        func=add_numbers,
        description="useful for when you need to add two numbers. Input should be two comma-separated numbers.",
    ),
    Tool(
        name="Failing Tool",
        func=always_fails_tool,
        description="A tool that is designed to fail.",
    )
]

llm = OpenAI(temperature=0)

# Initialize agent with verbose mode to see its thought process
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

print("\n--- Agent trying to use a working tool ---")
try:
    agent.run("What is 5 plus 7?")
except Exception as e:
    print(f"Caught an unexpected error: {e}")

print("\n--- Agent trying to use a failing tool ---")
try:
    agent.run("Use the Failing Tool with any input.")
except Exception as e:
    print(f"\n!!! Caught an Agent/Tool Error: {e} !!!")
    print("The 'Failing Tool' was called and raised an error.")
    print("Check the verbose output above to see the agent's thought process.")

print("\n--- Agent with potential input format issue for tool ---")
try:
    agent.run("Add these numbers: five and seven.") # Agent might struggle to format for tool
except Exception as e:
    print(f"\n!!! Caught a potential Agent/Tool Formatting Error: {e} !!!")
    print("The agent might try to call 'Add Two Numbers' but fails to provide valid input.")
    print("Review the agent's thoughts in verbose mode to see the input it tries to pass.")
```

The `verbose=True` setting is your best friend here. It will show you how the agent decides which tool to use and what input it gives to that tool. This helps immensely when you `debug langchain error handling examples` related to agent reasoning.

#### Chain Configuration Errors: The Building Block Blues

LangChain chains are made by connecting different components together. If you connect them incorrectly, or if a component is missing, your chain won't work. Think of it like trying to build with LEGOs, but some pieces don't fit, or you're missing a key block.

##### Symptoms
*   `ValueError`: Often related to missing parameters or incorrect configurations.
*   `AttributeError`: Trying to access something that doesn't exist on an object.
*   Messages like "Cannot connect X to Y" or "Missing attribute Z."

##### How to Debug and Fix
1.  **Check constructor arguments:** When you create a chain or component, make sure you pass all the required arguments (e.g., `llm`, `prompt`).
2.  **Verify input/output keys:** In more complex chains (like `SequentialChain`), ensure the output of one step matches the input of the next. Use `verbose=True` to confirm this.
3.  **Simplify and test:** If a complex chain fails, break it down into smaller, simpler chains. Test each part individually to achieve `error isolation`.

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0)

# Define prompts
prompt1 = PromptTemplate(
    input_variables=["product"],
    template="What is a good company name for a company that makes {product}?",
)

prompt2 = PromptTemplate(
    input_variables=["company_name"], # This should match the output of chain1
    template="Write a short slogan for the company called {company_name}.",
)

# Chain 1: Generate company name
chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="company_name")

# Chain 2: Generate slogan
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="slogan")

# PROBLEM 1: Missing output_key for a step in SequentialChain
print("\n--- Problem 1: Missing output_key in SequentialChain ---")
try:
    # If chain1 didn't have output_key="company_name", chain2 wouldn't find its input
    # Let's create a chain without the expected output_key for demonstration
    chain1_bad = LLMChain(llm=llm, prompt=prompt1) # Missing output_key
    overall_chain_bad = SimpleSequentialChain(chains=[chain1_bad, chain2], verbose=True)
    overall_chain_bad.run("eco-friendly shoes")
except Exception as e:
    print(f"\n!!! Caught a Chain Configuration Error: {e} !!!")
    print("Chain2 needs 'company_name' as input, but Chain1 is not providing it via 'output_key'.")
    print("Check the 'output_key' of the previous chain and 'input_variables' of the next chain.")

# PROBLEM 2: Input variables mismatch (less common with SimpleSequentialChain, but possible in custom chains)
print("\n--- Problem 2: Input variables mismatch (conceptual) ---")
try:
    prompt_mismatch = PromptTemplate(
        input_variables=["wrong_key"], # Chain2 expects 'company_name', not 'wrong_key'
        template="Write a slogan for {wrong_key}.",
    )
    chain2_mismatch = LLMChain(llm=llm, prompt=prompt_mismatch, output_key="slogan")
    overall_chain_mismatch = SimpleSequentialChain(chains=[chain1, chain2_mismatch], verbose=True)
    overall_chain_mismatch.run("organic food")
except Exception as e:
    print(f"\n!!! Caught a Chain Configuration Mismatch (conceptual): {e} !!!")
    print("Even though chain1 provides 'company_name', chain2_mismatch expects 'wrong_key'.")
    print("This would cause an input error in more complex chain setups.")


# CORRECT WAY
print("\n--- Correct Chain Configuration ---")
overall_chain_correct = SimpleSequentialChain(chains=[chain1, chain2], verbose=True)
try:
    result = overall_chain_correct.run("futuristic cars")
    print(f"\nCorrect Output: {result}")
except Exception as e:
    print(f"Caught an unexpected error: {e}")
```

This example highlights how essential it is for outputs to correctly map to inputs in chained operations. `Verbose mode usage` here shows you exactly which variables are being passed between steps, making it much easier to `debug langchain error handling examples` related to chain structure.

#### Prompt Template Issues: Asking the Wrong Question

Prompt templates are like fill-in-the-blank forms for your AI. You tell the AI what kind of information you need, and then you fill in the blanks with specific details. If your template has a mistake, or you don't provide all the blanks, the AI might get confused or throw an error.

##### Symptoms
*   `KeyError`: If you try to fill a blank that doesn't exist in the template.
*   `ValueError`: If you don't provide values for all the blanks.
*   The AI gives a strange or incomplete answer because the prompt was malformed.

##### How to Debug and Fix
1.  **Check `input_variables`:** Make sure the names in your `input_variables` list match the names inside your `template` string (e.g., `{topic}` must be in `input_variables`).
2.  **Verify provided inputs:** Ensure that when you use the template, you provide values for *all* the `input_variables`.
3.  **Print the final prompt:** Before sending it to the LLM, print the full prompt string to see if it looks correct.

```python
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

llm = OpenAI(temperature=0)

# PROBLEM 1: Input variable not found in template string
print("\n--- Problem 1: Input variable not in template ---")
try:
    # 'animal' is in input_variables, but not in the template string
    prompt_bad_var = PromptTemplate(
        input_variables=["animal"],
        template="Tell me why dogs are great.",
    )
    # This won't directly error on creation but might cause issues later
    # or give a warning. The next error will be more direct.
    chain = LLMChain(llm=llm, prompt=prompt_bad_var)
    chain.run({}) # Running with empty input, as 'animal' isn't used
except Exception as e:
    print(f"!!! Caught a PromptTemplate (conceptual) Error: {e} !!!")
    print("The variable 'animal' is defined but not used in the template.")
    print("This often leads to confusion or unused inputs.")


# PROBLEM 2: Input variable in template, but not in input_variables list
print("\n--- Problem 2: Template variable not in input_variables ---")
try:
    prompt_missing_var = PromptTemplate(
        input_variables=["city"],
        template="What is the capital of {country}?", # {country} is in template but not input_variables
    )
    # This will error when you try to use it with the chain
    chain = LLMChain(llm=llm, prompt=prompt_missing_var)
    chain.run({"city": "Paris"})
except Exception as e:
    print(f"\n!!! Caught a PromptTemplate Error: {e} !!!")
    print("The variable '{country}' is in the template but not in the 'input_variables' list.")
    print("LangChain doesn't know what to fill in for '{country}'.")


# PROBLEM 3: Not providing all required inputs when running the chain
print("\n--- Problem 3: Missing runtime input ---")
try:
    prompt_correct = PromptTemplate(
        input_variables=["city", "country"],
        template="What is the capital of {country}? And what is the main language spoken in {city}?",
    )
    chain = LLMChain(llm=llm, prompt=prompt_correct)
    chain.run({"city": "Berlin"}) # Missing 'country'
except Exception as e:
    print(f"\n!!! Caught a Missing Input Error: {e} !!!")
    print("The prompt expects both 'city' and 'country', but 'country' was missing.")

# CORRECT WAY
print("\n--- Correct Prompt Template Usage ---")
try:
    prompt_correct = PromptTemplate(
        input_variables=["city", "country"],
        template="What is the capital of {country}? And what is the main language spoken in {city}?",
    )
    chain = LLMChain(llm=llm, prompt=prompt_correct)
    result = chain.run({"city": "Rome", "country": "Italy"})
    print(f"Correct Output: {result}")
except Exception as e:
    print(f"Caught an unexpected error: {e}")
```

These errors show that the `PromptTemplate` expects a perfect match between its `input_variables` and the curly braces `{}` in its `template` string. Using `verbose=True` with your chain can also show you the final prompt sent to the LLM, helping you visually inspect for errors. This is a common part of `debug langchain error handling examples`.

#### Memory Errors: Your AI Forgetting Things

LangChain applications often need "memory" to remember past conversations or information. If memory isn't set up correctly, or if you try to use it in a way it wasn't designed for, your AI might forget what you just said or throw an error.

##### Symptoms
*   The AI repeats itself or ignores past messages.
*   `KeyError` when trying to retrieve memory.
*   Messages like "Cannot load data from memory" or "Memory type not supported."

##### How to Debug and Fix
1.  **Check `memory_key`:** Ensure the `memory_key` in your chain matches the output key from your memory component.
2.  **Verify memory type:** Make sure you're using the right kind of memory for your needs (e.g., `ConversationBufferMemory` for simple chat history).
3.  **Inspect memory contents:** Use `print()` statements to see what's actually being stored in memory at different points in your conversation.

```python
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm = OpenAI(temperature=0)

# PROBLEM 1: Incorrect memory_key
print("\n--- Problem 1: Incorrect memory_key ---")
try:
    # memory_key defaults to 'history' in ConversationBufferMemory,
    # but the ConversationChain expects 'chat_history' by default.
    # This mismatch causes the chain to not find the history it expects.
    bad_memory = ConversationBufferMemory(memory_key="wrong_key")
    bad_chain = ConversationChain(llm=llm, memory=bad_memory, verbose=True)
    bad_chain.run("Hi there!")
except Exception as e:
    print(f"\n!!! Caught a Memory Error (Key Mismatch): {e} !!!")
    print("The ConversationChain couldn't find its expected 'chat_history' because memory_key was 'wrong_key'.")

# PROBLEM 2: Forgetting to pass memory to the chain (conceptual)
print("\n--- Problem 2: Forgetting to pass memory (conceptual) ---")
try:
    # If you forget to pass 'memory' to ConversationChain, it won't remember anything
    no_memory_chain = ConversationChain(llm=llm, verbose=True) # No memory object passed
    print("\nFirst turn without memory:")
    no_memory_chain.run("My favorite color is blue.")
    print("Second turn without memory:")
    result = no_memory_chain.run("What is my favorite color?")
    print(f"Result (should be forgotten): {result}")
    print("Notice the AI doesn't remember the favorite color.")
except Exception as e:
    print(f"Caught an unexpected error: {e}")

# CORRECT WAY
print("\n--- Correct Memory Usage ---")
try:
    correct_memory = ConversationBufferMemory(memory_key="chat_history") # Correct memory_key
    correct_chain = ConversationChain(llm=llm, memory=correct_memory, verbose=True)
    print("\nFirst turn with correct memory:")
    correct_chain.run("My favorite animal is a cat.")
    print("Second turn with correct memory:")
    result = correct_chain.run("What is my favorite animal?")
    print(f"Correct Output (should remember): {result}")
except Exception as e:
    print(f"Caught an unexpected error: {e}")
```
`Verbose mode usage` is again very helpful here. It will show you the entire prompt, including the history that's being sent to the LLM. If the history is empty or incorrect, you'll see it right there, helping you `debug langchain error handling examples` related to memory.

### Error Isolation: Finding the Culprit

When you encounter an error, it's like a messy room. You need to tidy it up to find what you're looking for. `Error isolation` means narrowing down the problem to the smallest possible piece of code. This is a core `debugging technique`.

#### Divide and Conquer: Break It Down

If your LangChain application is large and complex, don't try to fix everything at once.
1.  **Break it into smaller parts:** Identify the main components (e.g., prompt, LLM, chain, agent, tool).
2.  **Test each part separately:** Run each component on its own with very simple inputs.
3.  **Find the failing part:** Once you find which smaller part breaks, you know where to focus your attention.

For example, if a complex agent is failing, first test if the LLM works on its own. Then test each tool individually. Then combine them. This systematic approach greatly speeds up `debug langchain error handling examples`.

#### Minimal Reproducible Example (MRE): Tiny Bug Traps

An MRE is the smallest amount of code that still shows the error. When you have a bug, try to remove as much code as possible until the error still appears. This helps you:
*   **Understand the root cause:** You see exactly what combination of code creates the problem.
*   **Share with others:** If you need help, an MRE makes it easy for others to understand and `error reproduction` simple.
*   **Focus your fix:** You don't get distracted by unrelated code.

Creating an MRE is a powerful `debugging technique` for any `real-world troubleshooting`.

```python
# Original complex setup (conceptual, imagine this is much larger)
# from langchain.agents import AgentType, initialize_agent, Tool
# from langchain.llms import OpenAI
# from langchain.chains import RetrievalQA
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# import faiss
#
# llm = OpenAI()
# embeddings = OpenAIEmbeddings()
# vectorstore = FAISS.load_local("my_faiss_index", embeddings)
# qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
#
# tools = [
#     Tool(name="QA System", func=qa_chain.run, description="useful for answering questions"),
#     Tool(name="Calculator", func=lambda x: eval(x), description="useful for math"),
# ]
# agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# agent.run("What is the capital of France?")

# --- How to create a Minimal Reproducible Example (MRE) ---
# If the above agent failed, you'd start simplifying:

# Step 1: Does the LLM work?
print("\n--- MRE Step 1: Testing the LLM directly ---")
from langchain.llms import OpenAI
try:
    llm = OpenAI(temperature=0)
    response = llm("Hello, world!")
    print(f"LLM works: {response.strip()}")
except Exception as e:
    print(f"LLM itself is failing: {e}")
    # If it fails here, the problem is likely API key or OpenAI access.

# Step 2: Does a simple Chain work?
print("\n--- MRE Step 2: Testing a simple Chain ---")
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
try:
    prompt = PromptTemplate(input_variables=["topic"], template="Tell me about {topic}.")
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run("AI")
    print(f"Simple chain works: {response.strip()}")
except Exception as e:
    print(f"Simple chain is failing: {e}")
    # If it fails here, the problem might be prompt formatting or chain setup.

# Step 3: Does a specific Tool work on its own?
print("\n--- MRE Step 3: Testing a specific Tool directly ---")
# Let's test the Calculator tool if it was part of the problem.
def simple_calculator(expression: str) -> str:
    """Evaluates a simple mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error in calculation: {e}"
try:
    result = simple_calculator("5+5")
    print(f"Calculator tool works: {result}")
    result_fail = simple_calculator("abc")
    print(f"Calculator tool (fail test): {result_fail}")
except Exception as e:
    print(f"Tool itself is failing: {e}")
    # If it fails here, the tool's logic is the problem.

# ... and so on for each component.
# By isolating and testing, you can debug langchain error handling examples much faster.
```

This step-by-step breakdown allows you to find the exact point of failure. This is the essence of `error isolation` and makes `real-world troubleshooting` manageable.

### Integrating Other Debugging Tools

Sometimes, the built-in LangChain debugging features aren't enough, or you want to use tools you're already familiar with. You can integrate standard Python `debugging techniques` into your LangChain workflow.

#### IDE Debuggers: Step-by-Step Inspection

If you use an Integrated Development Environment (IDE) like VS Code or PyCharm, they come with powerful debuggers. These debuggers allow you to:
*   **Set breakpoints:** Pause your code at a specific line.
*   **Step through code:** Execute your code line by line.
*   **Inspect variables:** See the value of any variable at any point.
*   **Call stack analysis:** See which functions called which functions to reach the current point.

Using an IDE debugger is a very effective way to `debug langchain error handling examples` in detail. It allows you to see the exact state of your program at any moment.

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Assume you have your OpenAI API key set as an environment variable
llm = OpenAI(temperature=0)
prompt = PromptTemplate(
    input_variables=["thing"],
    template="Explain {thing} in a fun way.",
)

def run_explanation_chain(item_to_explain: str):
    """
    A function to run the explanation chain.
    You can set a breakpoint inside this function in your IDE.
    """
    print(f"Attempting to explain: {item_to_explain}")
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Set a breakpoint on the next line in your IDE!
    # In VS Code, click to the left of the line number.
    # In PyCharm, click in the gutter next to the line number.
    final_result = chain.run(thing=item_to_explain) 
    
    print(f"Explanation completed.")
    return final_result

if __name__ == "__main__":
    print("\n--- Running with IDE Debugger (Set a breakpoint!) ---")
    try:
        explanation = run_explanation_chain("black holes")
        print(f"Result: {explanation}")
    except Exception as e:
        print(f"An error occurred during explanation: {e}")

    # Example of a potential error point that you could debug:
    # If prompt had a typo in input_variables or template,
    # the chain.run might fail. You'd step through to see why.
    print("\n--- Running another example (imagine a bug here) ---")
    try:
        # If 'thing' was missing or misspelled in the prompt template,
        # 'chain.run' might fail here, and the debugger would show you.
        explanation_error = run_explanation_chain("quantum entanglement")
        print(f"Result for quantum entanglement: {explanation_error}")
    except Exception as e:
        print(f"Caught an error in the second run: {e}")
```

When you set a breakpoint on `final_result = chain.run(thing=item_to_explain)` and run your script in debug mode, your program will pause there. You can then inspect the `chain` object, the `prompt`, and the `item_to_explain` to ensure everything is correct before the LLM call. This helps immensely with `debugging tools integration`.

#### Logging Libraries: Persistent Debugging Records

For long-running applications, or when you can't be there to watch `verbose mode usage`, Python's `logging` library is your friend. You can send detailed messages to files, a console, or even remote services. This is essential for `real-world troubleshooting` in production environments.

You can configure different levels of logs (DEBUG, INFO, WARNING, ERROR, CRITICAL) to control how much detail you see. This is part of robust `debugging tools integration`.

```python
import logging
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

llm = OpenAI(temperature=0)
prompt = PromptTemplate(
    input_variables=["concept"],
    template="What is the main idea behind {concept}?",
)

def get_concept_explanation(concept: str) -> str:
    logger.info(f"Starting explanation for concept: '{concept}'")
    try:
        chain = LLMChain(llm=llm, prompt=prompt)
        # You can add more detailed logging here if needed
        # logger.debug(f"Prompt template: {prompt.template}")
        # logger.debug(f"LLM temperature: {llm.temperature}")

        explanation = chain.run(concept)
        logger.info(f"Successfully got explanation for '{concept}'.")
        return explanation
    except Exception as e:
        logger.error(f"Error getting explanation for '{concept}': {e}", exc_info=True)
        # exc_info=True adds traceback to the log
        raise # Re-raise the exception after logging

if __name__ == "__main__":
    print("\n--- Running with Python Logging ---")
    try:
        result1 = get_concept_explanation("recursion")
        print(f"Explanation 1: {result1.strip()}")
    except Exception:
        print("Failed to get explanation 1. Check logs.")

    # Simulate an error scenario (e.g., if a bad API key was used or input was wrong)
    try:
        # Imagine 'concept' was actually 'missing_var_in_prompt'
        # or LLM had an issue
        result2 = get_concept_explanation("parallel computing") # This will likely run fine
        print(f"Explanation 2: {result2.strip()}")
    except Exception:
        print("Failed to get explanation 2. Check logs.")

    # If you change the logging level to DEBUG, you'd see more specific details
    # For example, by default, LangChain's internal logging also uses the `logging` module.
    # If you wanted to see LangChain's internal DEBUG logs too, you could set:
    # logging.getLogger("langchain").setLevel(logging.DEBUG)
    # This would give you a lot of verbose output through the standard logging system.
```

With logging, your `debug langchain error handling examples` efforts leave a paper trail. You can review past runs to see the context of errors, even if they happened hours ago. This is crucial for diagnosing intermittent issues.

### Real-World Troubleshooting Scenarios

Let's put all these `debugging techniques` into action with some `real-world troubleshooting` scenarios. This will help you see how to apply the knowledge of `debug langchain error handling examples` in practical situations.

#### Scenario 1: My Chatbot Gives Nonsense Answers

You've built a chatbot that uses an agent to answer questions, but sometimes it gives totally irrelevant or silly answers.

##### Troubleshooting Steps
1.  **Enable `verbose=True` for the agent:** This is your first and most important step. Watch its "thought process."
2.  **`Trace analysis` with LangSmith:** If the verbose output is too fast or complex, send the runs to LangSmith. Look at the traces for the bad answers.
3.  **Inspect agent thoughts:**
    *   Did the agent misunderstand the question? (Prompt engineering issue)
    *   Did it choose the wrong tool? (Tool description or agent logic issue)
    *   Did a tool return unexpected output that confused the agent? (Tool bug)
4.  **`Error isolation`:** If you suspect a tool, run that tool directly with the input the agent gave it. See if it works as expected.
5.  **Refine tool descriptions or system prompt:** Update the agent's instructions or the tool descriptions to make them clearer.

#### Scenario 2: My Chain is Super Slow

Your LangChain application is working, but it takes a very long time to respond. Users are complaining about the delay.

##### Troubleshooting Steps
1.  **`Verbose mode usage` or `debugging callbacks`:** Turn these on to see the timing of each step. Which part is taking the longest?
    *   Is it the LLM call? (Could be network latency, model size, or rate limits).
    *   Is it a complex Python function in one of your tools?
    *   Is it a database query or vector store lookup?
2.  **`Trace analysis` with LangSmith:** LangSmith often provides timings for each span in a trace, making it easy to identify bottlenecks.
3.  **Optimize slow components:**
    *   **LLM:** Try a faster model, adjust `temperature` (lower temperature can sometimes be faster), or implement caching.
    *   **Tools:** Optimize your tool's internal logic, make database queries more efficient.
    *   **External APIs:** Ensure your calls to external services are optimized and efficient.

#### Scenario 3: My Application Crashes with a Python Error

Your LangChain application suddenly stops working and shows a long, scary Python error message (a "traceback").

##### Troubleshooting Steps
1.  **Read the traceback from bottom to top:** The most important part is usually at the very end (the error message itself) and then the lines just above it which show *where* in your code the error happened.
2.  **Identify the error type:** Is it a `KeyError`, `TypeError`, `ValueError`, `AttributeError`, or something else? This points to the kind of mistake.
3.  **`Error isolation`:** Use `print()` statements or an IDE debugger to inspect variables around the line where the error occurred. What were the values of inputs/outputs?
4.  **`Error reproduction`:** Try to make the error happen again with the smallest possible amount of code (MRE).
5.  **Check `common error examples`:** Does the error message or context match any of the common errors we discussed (API key, input/output format, etc.)?

### Best Practices for Debugging LangChain

To effectively `debug langchain error handling examples`, keep these best practices in mind:

*   **Start Simple:** Always begin with `verbose mode usage` or `print()` statements.
*   **Be Systematic:** Use `error isolation` techniques like divide and conquer to narrow down issues.
*   **Leverage LangSmith:** For anything beyond simple chains, `LangSmith debugging` with `trace analysis` and `error reproduction` is a game-changer.
*   **Use Callbacks:** For custom logging or specific event handling, `debugging callbacks` offer great flexibility.
*   **Understand Error Messages:** Learn what `KeyError`, `TypeError`, etc., typically mean in a LangChain context.
*   **Test Components Individually:** Don't wait for the whole application to fail; test smaller pieces as you build them.
*   **Document:** Keep notes of peculiar errors and their solutions. This helps with future `real-world troubleshooting`.

### Conclusion

Debugging is a vital skill for anyone working with LangChain. By mastering these `debugging techniques`, from basic `verbose mode usage` to advanced `LangSmith debugging`, you'll be able to quickly identify and fix issues. You now have a toolkit to tackle `common error examples` and perform `real-world troubleshooting` with confidence.

Remember, every error is a chance to learn and make your applications stronger. Keep practicing these tips, and you'll soon be debugging faster and building even more amazing AI applications. Happy debugging!