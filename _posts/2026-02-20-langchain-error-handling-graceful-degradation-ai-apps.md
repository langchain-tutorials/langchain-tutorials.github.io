---
title: "LangChain Error Handling Best Practices: Graceful Degradation for AI Apps"
description: "Master LangChain graceful degradation error handling best practices to build resilient AI apps, ensuring a smooth, stable user experience."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [langchain graceful degradation error handling]
featured: false
image: '/assets/images/langchain-error-handling-graceful-degradation-ai-apps.webp'
---

## Understanding LangChain Error Handling: Building Resilient AI Apps

Imagine you're talking to a clever AI app, and suddenly it stops working. It might freeze, give a strange error message, or just crash completely. This is a frustrating experience for anyone using the app. We want our AI apps, especially those built with LangChain, to be much more polite.

This is where `langchain graceful degradation error handling` comes in handy. It's about making sure your AI app stays useful, even when things go a little wrong. We want it to "degrade gracefully," meaning it handles errors smoothly without breaking entirely.

You'll learn how to build AI apps that can keep working, perhaps a little differently, when problems arise. This guide will help you understand the best ways to manage errors in your LangChain projects. It focuses on ensuring a smooth experience for your users.

### What is Graceful Degradation?

Graceful degradation is a fancy term for a simple idea. Think of a superhero who loses some powers but can still fly, even if not as fast. Your app should be like that superhero; it might lose some features but keeps its most important parts working. It's about preserving *partial functionality preservation* instead of a total shutdown.

When we talk about `graceful degradation principles`, we mean a set of rules. These rules help us design systems that can handle failures without completely falling apart. You want your users to still get value, even if it's not the full, perfect experience.

For AI apps, this means if a complex AI model is slow, maybe a simpler one can take over. Or if an external service is down, your app can give a helpful, pre-written answer. It's all about making the best of a bad situation.

### Why is Graceful Degradation Important for AI Apps?

AI applications often rely on many different parts working together. They connect to large language models (LLMs), external tools, databases, and more. Any one of these parts can have a problem at any time.

If one part fails, your whole app doesn't have to stop. By using `langchain graceful degradation error handling`, you protect your users from sudden crashes. You provide a better *user experience during errors*, which keeps people happy and coming back.

Building resilient apps is crucial in the real world. It means your app is tough and can handle unexpected issues. This makes your AI app more reliable and trustworthy.

#### The Volatility of AI Services

AI services, especially large language models, can be unpredictable. They might experience high demand, leading to slow responses or timeouts. Sometimes, the API itself might return an unexpected error or simply be unavailable.

These issues are often outside your direct control. You can't stop OpenAI from having a brief outage, but you can prepare your app for it. This preparation involves thinking about how your app will behave when these external services act up.

Understanding these challenges helps you design your error handling strategies. It emphasizes the need for a robust approach to `langchain graceful degradation error handling`.

### Core Graceful Degradation Principles for AI

There are several key ideas that guide graceful degradation. You should keep these in mind when designing your LangChain applications. These principles help you decide what's most important and how to react to problems.

Let's explore some of these foundational ideas that ensure your AI app remains usable. They focus on maintaining a positive interaction even when systems are stressed.

#### Maintaining Core Functionality

The most important principle is to keep the essential parts of your app running. Think about what your app absolutely *must* do for the user. If your AI helps write emails, maybe it can't personalize them fully when degraded, but it can still generate a basic draft.

You need to identify the "must-have" features versus the "nice-to-have" ones. When errors happen, your app should prioritize *maintaining core functionality*. This ensures users can still accomplish their primary goal.

This might mean switching to a simpler path or using cached data. The goal is to avoid a complete functional breakdown.

#### Partial Functionality Preservation

Sometimes, you can't keep *all* core functionality, but you can keep *some*. This is `partial functionality preservation`. If your LangChain app uses multiple tools, and one tool fails, the others can still work.

For example, if your app can search the web and summarize articles, and the web search tool is down, it could still summarize articles you provide. It's about doing what you can with the resources available.

This approach ensures that some value is always delivered, even if it's a reduced set. You're offering a slightly less powerful version of your app, rather than nothing at all.

#### Fallback Responses

A `fallback response` is a pre-defined, safe answer your app can give when it can't figure out a real one. If your AI chatbot can't connect to the LLM, instead of crashing, it could say, "I'm having trouble connecting right now, please try again later." This is much better than silence or an error code.

Fallback responses are simple, but very effective for *user experience during errors*. They manage expectations and prevent frustration. You can even make them helpful, suggesting alternative actions.

These can be simple strings, or even a call to a much smaller, local model. The key is to have something ready to go when primary systems fail.

#### Degraded Mode Operation

When your app activates its error handling, it enters a `degraded mode operation`. This means it's working but not at its best. Maybe some features are turned off, or responses are slower or less detailed. You could inform the user that the app is currently in a limited mode.

For instance, your LangChain app might switch from a complex, expensive LLM to a cheaper, faster, or even local one. The quality might drop, but the service continues. You're giving the user a choice: wait for full functionality or get a quicker, simpler answer now.

Clear communication about this mode is vital. Users appreciate knowing what's happening.

### LangChain Specific Error Scenarios and Solutions

LangChain brings powerful capabilities, but also specific points where errors can occur. Understanding these helps you implement effective `langchain graceful degradation error handling`. You'll deal with issues related to LLMs, tools, memory, and more.

Let's look at common problems you might encounter and how to build in resilience. These practical scenarios will guide your implementation.

#### LLM API Errors

The most common point of failure in a LangChain app is the LLM API itself. This could be OpenAI, Anthropic, or any other provider. Issues include:

*   **Timeouts:** The LLM takes too long to respond.
*   **Rate Limits:** You're sending too many requests too quickly.
*   **Authentication Errors:** Your API key is wrong or expired.
*   **Server Errors:** The LLM provider's server is having problems.
*   **Bad Request/Invalid Input:** The prompt you sent was too long, or malformed.

**Example: Handling LLM Timeouts and Fallbacks**

You can wrap your LLM calls in a `try-except` block. If a timeout occurs, you can use a `fallback response`.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import logging

# Set up logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
# You might fetch this from environment variables or a configuration file
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here" # Ensure this is set securely

def get_chat_model(temperature=0.7, timeout=10, model_name="gpt-3.5-turbo"):
    """
    Helper function to get a ChatOpenAI instance with specified settings.
    """
    try:
        # Pass timeout directly to ChatOpenAI constructor
        # Note: Depending on LangChain version, timeout might be passed via .invoke or .ainvoke
        # For general network calls, httpx.Timeout or requests.Timeout applies if using those clients
        # LangChain's internal client might have its own default or configurable timeout.
        # Let's simulate a timeout or a network issue in the try-except for the actual call.
        return ChatOpenAI(temperature=temperature, model=model_name)
    except Exception as e:
        logging.error(f"Failed to initialize ChatOpenAI model: {e}")
        return None

def process_query_with_llm_fallback(query: str) -> str:
    """
    Attempts to process a query using an LLM with fallback responses for errors.
    """
    model = get_chat_model()
    if model is None:
        logging.warning("Could not initialize main LLM, returning generic fallback.")
        return "I'm sorry, I cannot connect to the main AI service right now. Please try again later."

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Answer concisely."),
        ("user", "{query}")
    ])
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    try:
        logging.info(f"Attempting to invoke LLM for query: '{query}'")
        # For demonstrating timeout: In a real scenario, you'd configure the LLM client
        # or use a library like `tenacity` for retries with timeouts.
        # Here, we're catching a generic exception for simplicity, assuming a timeout would manifest.
        response = chain.invoke({"query": query}, config={"timeout": 15}) # Setting a timeout for the invoke call if supported by adapter
        logging.info("LLM invocation successful.")
        return response
    except Exception as e:
        # Catch specific exceptions like TimeoutError, APIError, etc. for better handling
        # Example for specific LangChain/OpenAI errors:
        # from openai import RateLimitError, APIError, Timeout
        if "timeout" in str(e).lower(): # Generic check for timeout message
            logging.warning(f"LLM call timed out for query: '{query}' - {e}")
            return "I'm sorry, the AI is taking too long to respond. Could you please rephrase or try again in a moment?"
        elif "rate limit" in str(e).lower(): # Generic check for rate limit message
            logging.warning(f"LLM hit rate limit for query: '{query}' - {e}")
            return "I'm experiencing high demand right now. Please wait a moment before trying again."
        elif "authentication" in str(e).lower() or "api key" in str(e).lower():
            logging.error(f"LLM authentication error: {e}. Please check your API key.")
            return "There's an issue with my internal setup. Please contact support."
        else:
            logging.error(f"An unexpected LLM error occurred for query: '{query}' - {e}")
            return "I'm sorry, I encountered an unexpected problem. Can I help with something simpler?"

# --- Usage Example ---
print("--- Scenario 1: Successful LLM Call ---")
print(process_query_with_llm_fallback("What is the capital of France?"))

print("\n--- Scenario 2: Simulating LLM Timeout (manual override for demonstration) ---")
# To truly simulate a timeout, you'd need to mock the LLM's behavior or use a very short timeout.
# For simplicity, let's just make the 'except' block trigger for a specific query.
def process_query_with_simulated_timeout(query: str) -> str:
    if "timeout" in query.lower():
        raise TimeoutError("Simulated LLM Timeout")
    return process_query_with_llm_fallback(query)

try:
    print(process_query_with_simulated_timeout("Simulate timeout scenario: What is the capital of Germany?"))
except TimeoutError as e:
    # This block will actually catch the simulated TimeoutError
    print(process_query_with_llm_fallback("Simulate timeout scenario: What is the capital of Germany?").replace("I'm sorry, I encountered an unexpected problem.", "I'm sorry, the AI is taking too long to respond."))


print("\n--- Scenario 3: Simulating Rate Limit (manual override for demonstration) ---")
def process_query_with_simulated_rate_limit(query: str) -> str:
    if "rate limit" in query.lower():
        # Raise a general exception and let the specific check inside the function handle it.
        raise Exception("429 Too Many Requests: Rate limit exceeded.")
    return process_query_with_llm_fallback(query)

try:
    print(process_query_with_simulated_rate_limit("Simulate rate limit scenario: Tell me about space."))
except Exception as e:
    print(process_query_with_llm_fallback("Simulate rate limit scenario: Tell me about space.").replace("I'm sorry, I encountered an unexpected problem.", "I'm experiencing high demand right now."))

print("\n--- Scenario 4: Simulating Authentication Error (manual override) ---")
def process_query_with_simulated_auth_error(query: str) -> str:
    if "auth error" in query.lower():
        raise Exception("Authentication Error: Invalid API Key")
    return process_query_with_llm_fallback(query)

try:
    print(process_query_with_simulated_auth_error("Simulate auth error: What day is it?"))
except Exception as e:
    print(process_query_with_llm_fallback("Simulate auth error: What day is it?").replace("I'm sorry, I encountered an unexpected problem.", "There's an issue with my internal setup."))

```
In this example, you see different `fallback responses` for various LLM issues. This ensures that even when the main AI service struggles, your user isn't left in the dark. You are implementing robust `langchain graceful degradation error handling`.

#### Tool Execution Failures

LangChain Agents often use external tools to get information or perform actions. These tools can also fail. A tool might be an API call to a weather service, a database query, or even a web search.

Common tool errors include network issues, invalid API responses, or the tool simply being unavailable. When a tool fails, your agent needs to know how to proceed without it. You want to ensure `partial functionality preservation`.

**Example: Handling Tool Failures with Agent Fallbacks**

If an agent's tool fails, you can teach the agent to:
1.  Try another tool if available for the same task.
2.  Inform the user that the specific tool is unavailable and offer to proceed without it.
3.  Use a general LLM response as a fallback if no tools can complete the request.

Let's illustrate with a simple LangChain agent that uses a "search" tool. If the search tool fails, we want a `fallback response`.

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import logging
import random
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Dummy Search Tool (can simulate failure) ---
@tool
def search_tool(query: str) -> str:
    """Searches the internet for information on a given query."""
    # Simulate potential failure points
    if "fail search" in query.lower():
        logging.error(f"Simulating failure for search query: '{query}'")
        raise ConnectionError("Search service is temporarily unavailable.")
    if "slow search" in query.lower():
        logging.warning(f"Simulating slow search for query: '{query}'")
        import time
        time.sleep(5) # Simulate a long delay
        return f"Simulated slow search result for '{query}': Information found after a delay."

    # Normal operation
    results = {
        "capital of france": "Paris",
        "population of germany": "Around 83 million people.",
        "weather in london": "Cloudy with a chance of rain."
    }
    return results.get(query.lower(), f"Could not find specific search result for '{query}'.")

# --- Agent Setup ---
llm = ChatOpenAI(temperature=0) # Use a low temperature for more predictable agent behavior
tools = [search_tool]

# The prompt for the ReAct agent
template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_agent_with_tool_fallback(question: str) -> str:
    """
    Runs the agent and handles potential tool failures with a graceful fallback.
    """
    try:
        logging.info(f"Running agent for question: '{question}'")
        result = agent_executor.invoke({"input": question})
        return result["output"]
    except ConnectionError as e: # Catch specific errors from the tool
        logging.warning(f"Tool failed for question: '{question}'. Providing a fallback message. Error: {e}")
        return f"I'm sorry, I cannot access external search tools right now to answer '{question}'. Can I help with something else?"
    except Exception as e:
        logging.error(f"An unexpected error occurred while running the agent for '{question}': {e}")
        # Generic fallback for any other unexpected error during agent execution
        return "I encountered an unexpected problem. Please try your question again."

# --- Usage Examples ---
print("\n--- Scenario 1: Successful Tool Use ---")
print(run_agent_with_tool_fallback("What is the capital of France?"))

print("\n--- Scenario 2: Simulated Tool Failure ---")
print(run_agent_with_tool_fallback("Tell me about the weather in London, but fail search."))

print("\n--- Scenario 3: Simulated Slow Tool ---")
print(run_agent_with_tool_fallback("What is the population of Germany? (slow search)"))

print("\n--- Scenario 4: Question not requiring tool (agent should still work) ---")
print(run_agent_with_tool_fallback("Hello, how are you?"))
```
In this scenario, if the `search_tool` encounters a `ConnectionError` (which we simulate for "fail search"), the `run_agent_with_tool_fallback` function catches it. It then returns a polite message to the user, showcasing `partial functionality preservation`. The agent doesn't crash, it just explains its limitation. You're successfully implementing `langchain graceful degradation error handling`.

#### Output Parsing Errors

After an LLM generates a response, LangChain often uses "output parsers" to turn that raw text into a structured format like a list, JSON, or a specific object. If the LLM's output doesn't match what the parser expects, it will fail.

This is a common issue because LLMs are generative and don't always follow instructions perfectly. You need to handle these parsing errors gracefully.

**Example: Handling Output Parser Errors**

You can catch parsing errors and then either:
1.  Retry the LLM with a more specific prompt.
2.  Try a simpler parser.
3.  Return the raw, unparsed text to the user, perhaps with a warning.
4.  Provide a `fallback response`.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

llm = ChatOpenAI(temperature=0.1)

# --- Define a Pydantic Model for structured output ---
class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age")
    city: str = Field(description="The city where the person lives")

def parse_person_info(text: str, parser_type: str = "pydantic") -> dict:
    """
    Attempts to parse person information from text with error handling.
    """
    if parser_type == "pydantic":
        parser = PydanticOutputParser(pydantic_object=Person)
    elif parser_type == "json":
        parser = JsonOutputParser()
    else:
        raise ValueError("Invalid parser_type. Choose 'pydantic' or 'json'.")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract person information as a JSON object with 'name', 'age', and 'city'. {format_instructions}"),
        ("user", "{text}")
    ])
    
    # Get format instructions from the parser
    format_instructions = parser.get_format_instructions()
    
    chain = prompt | llm | parser

    try:
        logging.info(f"Attempting to parse text using {parser_type} parser.")
        # Pass format instructions to the prompt
        parsed_data = chain.invoke({"text": text, "format_instructions": format_instructions})
        logging.info("Parsing successful.")
        return parsed_data.dict() if parser_type == "pydantic" else parsed_data
    except Exception as e:
        logging.warning(f"Output parsing failed for text: '{text[:50]}...' with {parser_type} parser. Error: {e}")
        # Fallback: return a default structure, or raw text, or a message.
        return {
            "error": "Could not parse information",
            "original_text": text,
            "reason": str(e),
            "fallback_message": "I couldn't understand the information in the expected format. Is there another way I can help?"
        }

# --- Usage Examples ---
print("\n--- Scenario 1: Successful Pydantic Parsing ---")
# LLM will likely return a good JSON for this
print(parse_person_info("John Doe is 30 years old and lives in New York City.", "pydantic"))

print("\n--- Scenario 2: Successful JSON Parsing ---")
print(parse_person_info("Jane Smith is 25 years old and lives in London.", "json"))

print("\n--- Scenario 3: Pydantic Parsing Failure (bad format from LLM) ---")
# Simulating a bad LLM output that doesn't fit the Pydantic schema
# In a real scenario, the LLM might just output plain text or incomplete JSON
def simulate_bad_pydantic_output(text_input: str):
    # This function would be more complex in a real test,
    # but here we're demonstrating the catch mechanism.
    # We directly call the parsing function with text that would fail.
    # For a real LLM, you'd feed the prompt and hope it breaks.
    # Let's override the chain for this specific test to return bad string
    
    # We will just pass a string that LLM might return if it fails to follow instructions
    # and then try to parse it.
    
    # The actual `chain.invoke` inside `parse_person_info` will call LLM.
    # We want to demonstrate that if LLM returns something that does *not* fit the Person model,
    # the PydanticOutputParser will raise an error.
    # Let's make the LLM return a non-JSON string for this test.
    original_llm_invoke = llm.invoke
    def mock_llm_invoke(*args, **kwargs):
        if "bad_parse_test" in kwargs.get("input", ""):
            return "This is just plain text, not JSON or Pydantic format."
        return original_llm_invoke(*args, **kwargs)
        
    llm.invoke = mock_llm_invoke # Temporarily replace LLM's invoke method
    
    try:
        result = parse_person_info(f"bad_parse_test: {text_input}", "pydantic")
    finally:
        llm.invoke = original_llm_invoke # Restore original LLM's invoke method
    return result

print(simulate_bad_pydantic_output("A simple phrase without proper structure."))

print("\n--- Scenario 4: JSON Parsing Failure (LLM returns invalid JSON) ---")
def simulate_bad_json_output(text_input: str):
    original_llm_invoke = llm.invoke
    def mock_llm_invoke(*args, **kwargs):
        if "invalid_json_test" in kwargs.get("input", ""):
            return "{name: 'Alice', age: 28, city: 'Berlin',}" # Malformed JSON
        return original_llm_invoke(*args, **kwargs)
        
    llm.invoke = mock_llm_invoke
    
    try:
        result = parse_person_info(f"invalid_json_test: {text_input}", "json")
    finally:
        llm.invoke = original_llm_invoke
    return result

print(simulate_bad_json_output("Information for Alice."))
```
Here, if the LLM output doesn't conform to the `Person` Pydantic model or valid JSON, the `try-except` block catches the error. It then returns a dictionary indicating the failure and a user-friendly `fallback_message`. This maintains a good *user experience during errors* and demonstrates `langchain graceful degradation error handling`.

### Advanced `LangChain Graceful Degradation Error Handling` Techniques

Beyond simple `try-except` blocks, there are more sophisticated ways to build resilience. These techniques allow for more dynamic and intelligent degradation. They help manage complex failures.

#### Retries and Exponential Backoff

Sometimes, an error is just temporary (a "transient" error). Like a brief network glitch or a busy server. Instead of giving up, you can try again. This is called a "retry."

`Exponential backoff` means waiting a little longer each time you retry. For example, wait 1 second, then 2 seconds, then 4 seconds. This prevents you from hammering a struggling service and gives it time to recover. Libraries like `tenacity` in Python are great for this.

**Example: Using `tenacity` for Retries**

```python
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
import random
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

llm = ChatOpenAI(temperature=0) # Use low temperature for consistency

# --- Simulate an unreliable external service ---
call_count = 0
def unreliable_llm_call_simulator(query: str) -> str:
    """
    Simulates an LLM call that fails a few times before succeeding.
    """
    global call_count
    call_count += 1
    
    if call_count < 3 and "unreliable" in query.lower(): # Fail first 2 attempts for specific queries
        logging.warning(f"Simulated LLM failure on attempt {call_count} for query: '{query}'")
        if random.random() < 0.5:
            raise ConnectionError("Simulated network issue connecting to LLM.")
        else:
            raise Exception("Simulated LLM internal server error.")
    
    logging.info(f"Simulated LLM success on attempt {call_count} for query: '{query}'")
    return f"Response for '{query}' (successful after {call_count} attempts)."

# --- LangChain Integration with Tenacity ---
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10), reraise=True)
def get_llm_response_with_retries(query: str) -> str:
    """
    Wrapper for LLM invocation with retries and exponential backoff.
    """
    global call_count # Reset for each new query call
    if call_count > 0: # Only reset if not first call for this function
        call_count = 0 
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{query}")
    ])
    output_parser = StrOutputParser()
    
    # We'll use our simulator instead of a real LLM here for demonstration
    # In a real app, this would be: chain = prompt | llm | output_parser
    
    # To integrate tenacity with actual LangChain calls, you would typically apply
    # the retry decorator to the method that invokes the LLM or tool.
    # For a chain, it's often best to retry the `invoke` call itself.
    
    # For demonstration, let's wrap the core 'unreliable_llm_call_simulator'
    # in a way that represents how LangChain might call an LLM internally.
    
    # Simulating the LLM call within a LangChain-like context
    formatted_prompt = prompt.invoke({"query": query}).to_string()
    raw_response = unreliable_llm_call_simulator(formatted_prompt)
    
    return output_parser.invoke(raw_response)

def process_query_robustly(query: str) -> str:
    """
    Processes a query using the retrying mechanism, with a final fallback.
    """
    try:
        response = get_llm_response_with_retries(query)
        return response
    except RetryError as e:
        logging.error(f"All retry attempts failed for query: '{query}'. Last error: {e.last_attempt.exception()}")
        return "I'm sorry, I've tried multiple times but can't connect to the AI service. Please try again later."
    except Exception as e:
        logging.error(f"An unexpected error occurred during robust processing: {e}")
        return "An unexpected error occurred. Please try again."

# --- Usage Examples ---
print("\n--- Scenario 1: Unreliable Service (should retry and succeed) ---")
print(process_query_robustly("Tell me something about unreliable service."))

global call_count # Reset global counter for the next example
call_count = 0

print("\n--- Scenario 2: Constantly Failing Service (should hit retry limit) ---")
# To simulate consistent failure, we need to modify the simulator or the retry limit.
# Let's make the simulator fail more times than the retry attempts.
original_unreliable_simulator = unreliable_llm_call_simulator
def consistently_failing_simulator(query: str) -> str:
    global call_count
    call_count += 1
    logging.warning(f"Simulated LLM consistently failing on attempt {call_count} for query: '{query}'")
    raise ConnectionError("Simulated persistent network issue.")

# Temporarily replace the simulator for this test
global call_count # Reset call_count for this test
call_count = 0 

# Define a temporary retry function that uses the consistently_failing_simulator
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=2), reraise=True)
def get_llm_response_consistently_failing(query: str) -> str:
    global call_count # Reset for each new query call
    if call_count > 0:
        call_count = 0
    formatted_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{query}")
    ]).invoke({"query": query}).to_string()
    raw_response = consistently_failing_simulator(formatted_prompt)
    return StrOutputParser().invoke(raw_response)

def process_query_consistently_failing(query: str) -> str:
    try:
        response = get_llm_response_consistently_failing(query)
        return response
    except RetryError as e:
        logging.error(f"All retry attempts failed for consistently failing query: '{query}'. Last error: {e.last_attempt.exception()}")
        return "I'm sorry, I've tried multiple times but can't connect to the AI service. Please try again later. (Consistently Failing)"
    except Exception as e:
        logging.error(f"An unexpected error occurred during consistently failing processing: {e}")
        return "An unexpected error occurred. Please try again. (Consistently Failing)"

print(process_query_consistently_failing("Query that consistently fails."))

# Restore original simulator if needed for other tests
globals()['unreliable_llm_call_simulator'] = original_unreliable_simulator
globals()['call_count'] = 0 # Reset for future uses
```
The `get_llm_response_with_retries` function attempts the LLM call multiple times. It waits longer between each attempt. If all attempts fail, it then falls back to a final error message. This is a robust way to handle temporary network issues and contributes to `service level degradation` in a controlled manner.

#### Feature Flags for Degradation

`Feature flags for degradation` are like on/off switches for parts of your app. You can use them to dynamically turn off less critical features if your system is under stress or experiencing errors. This helps to offload demand and preserve `maintaining core functionality`.

For example, if your LangChain app offers both summarization and sophisticated sentiment analysis, you could disable sentiment analysis via a feature flag if the LLM is overloaded. This shifts your app into `degraded mode operation`.

**Example: Simple Feature Flag**

```python
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Feature Flag Configuration (could be from env vars, database, etc.) ---
# For demonstration, we'll use a simple dictionary, but in production,
# you'd use a dedicated feature flag service (e.g., LaunchDarkly, ConfigCat, or a simple database table).
_FEATURE_FLAGS = {
    "ENABLE_ADVANCED_SENTIMENT_ANALYSIS": True,
    "USE_SIMPLER_LLM_ON_DEGRADATION": False, # Switch to True to enable degraded mode
    "ENABLE_IMAGE_GENERATION": True,
}

def get_feature_flag(flag_name: str, default: bool = False) -> bool:
    """
    Retrieves the state of a feature flag.
    In a real app, this would involve a more robust system.
    """
    return _FEATURE_FLAGS.get(flag_name, default)

def analyze_sentiment(text: str, advanced: bool = True) -> str:
    """
    Simulates sentiment analysis.
    """
    if advanced and get_feature_flag("ENABLE_ADVANCED_SENTIMENT_ANALYSIS"):
        logging.info("Performing advanced sentiment analysis.")
        # Simulate LLM call for advanced analysis
        if random.random() < 0.1: # 10% chance of failure for advanced analysis
            raise Exception("Advanced sentiment analysis service failed.")
        return f"Advanced sentiment: {text} is very positive!" if "great" in text.lower() else f"Advanced sentiment: {text} is neutral."
    else:
        logging.info("Performing basic sentiment analysis.")
        return f"Basic sentiment: {text} is positive." if "great" in text.lower() else f"Basic sentiment: {text} is generally neutral."

def generate_image(prompt: str) -> str:
    """
    Simulates image generation.
    """
    if get_feature_flag("ENABLE_IMAGE_GENERATION"):
        logging.info(f"Generating image for: {prompt}")
        if random.random() < 0.2: # 20% chance of image gen failure
            raise Exception("Image generation service is overloaded.")
        return f"Image successfully generated for '{prompt}'."
    else:
        logging.warning("Image generation is disabled by feature flag.")
        return "Image generation feature is currently unavailable."

def process_user_request(request_text: str) -> list[str]:
    """
    Processes a user request with degradation based on feature flags.
    """
    responses = []

    # Handle sentiment analysis
    try:
        # Check if advanced sentiment is enabled. If not, or if it fails, fall back to basic.
        if get_feature_flag("ENABLE_ADVANCED_SENTIMENT_ANALYSIS"):
            sentiment_response = analyze_sentiment(request_text, advanced=True)
        else:
            sentiment_response = analyze_sentiment(request_text, advanced=False)
        responses.append(sentiment_response)
    except Exception as e:
        logging.error(f"Error in advanced sentiment analysis: {e}. Falling back to basic or default.")
        responses.append(analyze_sentiment(request_text, advanced=False)) # Fallback to basic
        responses.append("Note: Advanced sentiment analysis is currently experiencing issues.")

    # Handle image generation
    try:
        image_response = generate_image(f"A picture of {request_text}")
        responses.append(image_response)
    except Exception as e:
        logging.error(f"Error in image generation: {e}. Feature might be disabled or degraded.")
        responses.append("Image generation is currently unavailable due to high demand or errors.")

    return responses

# --- Usage Examples ---
print("\n--- Scenario 1: All features enabled (default) ---")
print(process_user_request("This is a great day!"))

print("\n--- Scenario 2: Disable advanced sentiment via feature flag ---")
_FEATURE_FLAGS["ENABLE_ADVANCED_SENTIMENT_ANALYSIS"] = False
print(process_user_request("This is an okay day."))

print("\n--- Scenario 3: Simulate advanced sentiment failure (flag is True, but error occurs) ---")
_FEATURE_FLAGS["ENABLE_ADVANCED_SENTIMENT_ANALYSIS"] = True # Re-enable for this test
print(process_user_request("This is a truly great day! (testing advanced sentiment failure)"))

print("\n--- Scenario 4: Disable image generation via feature flag ---")
_FEATURE_FLAGS["ENABLE_IMAGE_GENERATION"] = False
print(process_user_request("A beautiful sunset."))

# Reset flags for subsequent executions if this were part of a larger system
_FEATURE_FLAGS = {
    "ENABLE_ADVANCED_SENTIMENT_ANALYSIS": True,
    "USE_SIMPLER_LLM_ON_DEGRADATION": False,
    "ENABLE_IMAGE_GENERATION": True,
}
```
This example shows how to use a dictionary as a simple feature flag system. You could flip `ENABLE_ADVANCED_SENTIMENT_ANALYSIS` to `False` to instantly disable it without changing code. This is a powerful tool for `degraded mode operation` and `maintaining core functionality` under stress.

#### Progressive Enhancement (Related Concept)

While graceful degradation focuses on handling failures, `progressive enhancement` is a related concept. It means starting with a basic, working version of your app and then adding more advanced features if the user's browser or system supports them.

For AI, this might mean starting with a simple, fast LLM and upgrading to a more powerful, slower one if the user explicitly requests it or if the system has spare capacity. It's building from simple to complex, rather than complex to simple (degradation).

### Monitoring Degradation

It's not enough to just implement `langchain graceful degradation error handling`. You also need to know *when* your app is degrading. This is where `degradation monitoring` comes in. You need to keep an eye on how your app is performing.

You should track key metrics like:
*   **Error Rates:** How often are errors occurring?
*   **Response Times:** Are responses getting slower?
*   **Fallback Usage:** How often are fallback mechanisms being triggered?
*   **Resource Usage:** Are CPU, memory, or API quotas hitting limits?

**Tools for Monitoring:**

*   **Logging:** Detailed logs help you see what went wrong and when.
*   **Metrics Dashboards:** Tools like Prometheus, Grafana, Datadog can show you graphs of your app's health.
*   **Alerting:** Set up alerts to notify you immediately if degradation thresholds are crossed. For instance, if fallback responses make up 20% of all interactions, you should get an alert.

You might want to refer to our blog post on `[Monitoring AI Applications](/blog/monitoring-ai-applications)` for more in-depth information.

**Example: Logging Fallback Responses**

```python
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def perform_critical_action() -> str:
    """
    Simulates a critical action that might fail.
    """
    if time.time() % 3 < 1: # Simulate failure about 33% of the time
        raise ConnectionRefusedError("Critical service is down!")
    return "Critical action completed successfully."

def execute_with_fallback_logging() -> str:
    """
    Executes a critical action and logs when a fallback is used.
    """
    try:
        result = perform_critical_action()
        logging.info("Critical action succeeded.")
        return result
    except ConnectionRefusedError as e:
        logging.warning(f"CRITICAL_ACTION_DEGRADED: Fallback triggered due to error: {e}")
        return "Critical action failed, using degraded mode. Please try again later for full functionality."
    except Exception as e:
        logging.error(f"UNEXPECTED_ERROR: An unexpected error occurred: {e}")
        return "An unexpected error occurred. Providing generic fallback."

# --- Usage Examples (run multiple times to see degradation) ---
print("\n--- Degradation Monitoring Simulation ---")
for i in range(5):
    print(f"Attempt {i+1}: {execute_with_fallback_logging()}")
    time.sleep(0.5) # Small delay to simulate real-world calls
```
In this example, every time the `ConnectionRefusedError` is caught, a specific `CRITICAL_ACTION_DEGRADED` log message is emitted. You can then configure your monitoring tools to count these specific log entries. If the count goes above a certain threshold, it indicates your app is frequently in `degraded mode operation`.

### Best Practices Summary for `LangChain Graceful Degradation Error Handling`

To recap, building robust AI apps with LangChain means being prepared for failure. Here's a quick checklist of `graceful degradation principles` you should follow:

*   **Identify Critical Paths:** What absolutely *must* work? Protect these parts first.
*   **Implement `try-except` Blocks:** Wrap external calls (LLMs, tools) and parsing logic.
*   **Provide Clear `Fallback Responses`:** Give users helpful messages instead of errors.
*   **Use Retries with Exponential Backoff:** For transient errors, try again intelligently.
*   **Plan for `Partial Functionality Preservation`:** If one feature breaks, can others still work?
*   **Consider `Degraded Mode Operation`:** Can your app offer a simpler, less resource-intensive version of itself?
*   **Employ `Feature Flags for Degradation`:** Be able to dynamically switch off non-essential features.
*   **Implement `Degradation Monitoring`:** Know when your app is degrading and why.
*   **Educate Users:** Inform users when your app is in a degraded state. This improves *user experience during errors*.

By following these guidelines, you'll create LangChain applications that are not only powerful but also incredibly reliable and user-friendly, even when faced with the unexpected. You are ensuring your `service level degradation` is controlled.

### Moving Forward with Robust AI

Building AI applications with LangChain opens up a world of possibilities. However, the complexity of these systems means that errors are an inevitable part of their lifecycle. By mastering `langchain graceful degradation error handling`, you're not just fixing bugs; you're building trust with your users.

Remember, a gracefully degrading app is a polite app. It tells the user what's happening, offers alternatives, and tries its best to keep working. This approach leads to more reliable, enjoyable, and sustainable AI experiences. You are empowering your AI app to perform `maintaining core functionality` even when facing challenges.

Keep these best practices in mind as you develop your LangChain projects. Your users will thank you for the smooth experience, even in challenging conditions. For more on building foundational components, you can explore our post on `[Building Basic LangChain Chains](/blog/building-basic-langchain-chains)`.