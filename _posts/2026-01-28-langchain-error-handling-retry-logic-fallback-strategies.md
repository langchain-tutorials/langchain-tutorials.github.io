---
title: "LangChain Error Handling Best Practices: Retry Logic and Fallback Strategies"
description: "Learn LangChain retry fallback error handling best practices to implement robust retry logic and smart fallback strategies for resilient AI applications."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [langchain retry fallback error handling]
featured: false
image: '/assets/images/langchain-error-handling-retry-logic-fallback-strategies.webp'
---

## LangChain Error Handling Best Practices: Retry Logic and Fallback Strategies

Building cool tools with LangChain is super exciting. You can make smart assistants or content generators. But sometimes, things can go wrong when you talk to these powerful AI models.

Imagine you're asking a question, and the internet hiccups, or the AI service gets busy. Your perfect program might crash. This is why good error handling is so important for your LangChain applications.

This guide will teach you the best ways to handle these problems. We will look at `langchain retry fallback error handling` to make your tools super reliable.

### Understanding Why Errors Happen in LangChain

When your LangChain application talks to a large language model (LLM) like OpenAI or Google's Gemini, it's like sending a message. Many things can stop that message from getting through or cause a weird answer. These are common errors you might face.

For example, the network might be slow, or the AI service might have too many people using it at once. You might send a question the AI can't understand. Knowing these issues helps you prepare for them.

#### Common Kinds of Errors

*   **Network Issues:** Your internet connection might drop for a second. This stops your message from reaching the AI. It's like a bad phone signal.
*   **API Rate Limits:** AI services want everyone to have a fair turn. If you ask too many questions too quickly, they might tell you to slow down. This is called hitting a rate limit.
*   **Server Errors:** Sometimes, the AI service itself might have a tiny problem. It might send back an error message saying it's busy.
*   **Invalid Responses:** The AI might give an answer, but it's not in the format you expected. This can mess up how your program works.
*   **Timeouts:** Your program might wait for an answer from the AI, but it takes too long. It gives up waiting and shows a timeout error.

These errors can stop your application right in its tracks. But don't worry, you can teach your application to deal with them gracefully. You can learn more about general error types in our post on [Understanding API Errors](/blog/understanding-api-errors.md).

### Retry Logic: Giving It Another Go

Imagine you are trying to open a stubborn jar lid. If it doesn't open the first time, you don't just give up. You try again, maybe a little harder, right? That's what `Implementing retry logic` is all about for your programs.

It means your application will automatically try to do something again if it fails the first time. This is super helpful for temporary problems like a quick network glitch or a busy server. Your program becomes more patient and persistent.

#### How Simple Retry Works

When your LangChain code tries to talk to an AI model and gets a temporary error, the retry logic kicks in. Instead of just crashing, it waits a little bit. Then, it tries the exact same thing again.

If that second try also fails, it might try a third time. You can decide how many times it should try. This is known as `max retry configuration`.

Let's say you set the `max retry configuration` to 3. Your program will try up to three times to get the job done. If it still fails after three tries, then it knows it's a bigger problem.

```python
# A very basic idea of what a retry might look like (conceptual)
def call_llm_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            return response # Success!
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
                # In a real scenario, you'd wait here.
                # time.sleep(1)
            else:
                raise # All retries failed, re-raise the last error
```

This simple loop shows the core idea. You keep trying until you succeed or run out of attempts. This is a fundamental part of `langchain retry fallback error handling`.

#### Advanced Retry Patterns for Smarter Retries

Just trying again right away isn't always the best plan. If the AI server is overloaded, trying again instantly will likely fail again. We need smarter ways to retry.

This is where `exponential backoff patterns` and `retry with jitter` come in handy. These patterns make your retries much more effective. They help your application be polite and not add more stress to an already busy system.

##### Exponential Backoff Patterns

Imagine you tried that stubborn jar, and it still didn't open. You might wait a minute, take a breath, and then try again. If it still doesn't open, you might wait five minutes before your next attempt. That's the idea behind `exponential backoff patterns`.

Instead of waiting the same amount of time between tries, you wait longer each time. For example, you might wait 1 second after the first failure, then 2 seconds after the second, then 4 seconds after the third. The wait time grows quickly.

This gives the busy server or slow network more time to recover. It also means you're not flooding the system with requests that are likely to fail. This is a very common and effective strategy for `implementing retry logic`.

```python
import time
import math

def call_llm_with_exponential_backoff(prompt, max_retries=5, initial_delay=1):
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            return response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt) # Exponential growth
                print(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            else:
                raise
```

You can see how the `delay` increases each time. This makes your retry strategy much more robust. It's a key technique for `langchain retry fallback error handling`.

##### Retry with Jitter

Now, imagine thousands of applications all trying to talk to the same busy AI server. If they all use the exact same `exponential backoff patterns`, they might all try again at the exact same moment. This can create another surge of requests, causing more problems. This is called a "thundering herd" problem.

`Retry with jitter` helps solve this. "Jitter" means a small, random change. Instead of waiting *exactly* 2 seconds, you might wait between 1.5 and 2.5 seconds. You add a little bit of randomness to your wait time.

This tiny random change helps spread out the retries. It prevents all applications from hitting the server at the exact same moment after a failure. It makes your retry logic even smoother and more polite.

```python
import time
import math
import random

def call_llm_with_jitter(prompt, max_retries=5, initial_delay=1):
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            return response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                base_delay = initial_delay * (2 ** attempt)
                # Add jitter: +/- 25% of the base delay
                jitter = random.uniform(-0.25, 0.25) * base_delay
                delay = max(0.5, base_delay + jitter) # Ensure delay is not too small
                print(f"Waiting {delay:.2f} seconds before retrying with jitter...")
                time.sleep(delay)
            else:
                raise
```

Using `retry with jitter` makes your application a better network citizen. It's an important detail when you are `implementing retry logic` for high-traffic applications. This small addition makes a big difference in preventing cascading failures.

##### Conditional Retry: When to Try Again

Sometimes, an error is not temporary. If you try to access a file that doesn't exist, no amount of retrying will make it appear. In these cases, retrying is a waste of time and resources.

`Conditional retry` means you only retry for specific types of errors. For example, you might retry if you get a network timeout or a "too many requests" error (a 429 HTTP status code). But you would not retry if you get an "invalid API key" error (a 401 status code) or a "bad request" error (a 400 status code).

You need to know which errors are temporary and which are permanent. This way, your program is smart about when to try again. This prevents pointless retries and helps you quickly identify real issues.

```python
import httpx # Assuming you might get HTTPX errors from an API call
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# Define the types of exceptions we consider retryable
RETRYABLE_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ReadTimeout,
    httpx.ProxyError,
    # Add other temporary errors, e.g., rate limit errors if caught specifically
)

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS)
)
def call_llm_conditionally(prompt):
    print("Calling LLM...")
    # Simulate an error based on an external condition or random chance
    import random
    if random.random() < 0.6: # 60% chance of a retryable error
        if random.random() < 0.5:
            raise httpx.ConnectError("Simulated network connection error!")
        else:
            raise httpx.ReadTimeout("Simulated read timeout!")
    elif random.random() < 0.1: # 10% chance of a non-retryable error
        raise ValueError("Non-retryable: Invalid prompt format!")
    
    return "LLM responded: " + prompt[:20] + "..."

# Example of using the function
# try:
#     result = call_llm_conditionally("What is the capital of France?")
#     print(f"Successful response: {result}")
# except Exception as e:
#     print(f"All retries failed or non-retryable error: {e}")
```

This makes your `langchain retry fallback error handling` much more efficient. You only spend effort on problems that have a chance of fixing themselves. You can read more about different error types and how to classify them in our guide on [Handling Specific API Error Codes](/blog/handling-specific-api-error-codes.md).

#### Tools for Retry Logic: Retry Decorators

You don't have to write all the `retry logic` from scratch every time. Smart programmers have built libraries that make it easy. These libraries often use something called `retry decorators`.

A decorator is like a little wrapper you put around your function. It tells your function, "Hey, if you fail, I'll take care of retrying you based on these rules." It keeps your code clean and easy to read.

One popular Python library for this is `tenacity`. It's very powerful and flexible. LangChain itself often uses `tenacity` under the hood for some of its operations.

##### Using `tenacity` for Retry

Let's see how `tenacity` can apply `exponential backoff patterns` with `max retry configuration` and `conditional retry`.

```python
import openai # Or any other LLM library LangChain would wrap
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, wait_random_jitter

# Define retryable exceptions relevant to LLM API calls
RETRYABLE_LLM_ERRORS = (
    openai.APITimeoutError,
    openai.APIConnectionError,
    httpx.RequestError, # For general HTTP errors that might occur
    # Add specific rate limit exceptions if your LLM client exposes them
    # e.g., openai.RateLimitError if it were a distinct class
)

# Simulate an LLM client
class MockLLM:
    def __init__(self, fail_count=3, non_retryable_at_attempt=None):
        self.call_count = 0
        self.fail_count = fail_count
        self.non_retryable_at_attempt = non_retryable_at_attempt

    def invoke(self, prompt: str):
        self.call_count += 1
        print(f"MockLLM: Attempt {self.call_count} for prompt '{prompt}'")

        if self.non_retryable_at_attempt and self.call_count == self.non_retryable_at_attempt:
            print("MockLLM: Simulating a non-retryable error.")
            raise ValueError(f"Non-retryable error on attempt {self.call_count}: Bad input.")

        if self.call_count <= self.fail_count:
            print(f"MockLLM: Simulating a retryable error (APIConnectionError).")
            # Raise a retryable error
            raise openai.APIConnectionError(
                message="Mock connection error",
                http_body=None,
                http_headers=None,
                code=None
            )
        print(f"MockLLM: Successfully responded after {self.call_count} attempts.")
        return f"Mock response for '{prompt}'"

# Use a tenacity decorator for robust retries
@retry(
    wait=wait_exponential(multiplier=1, min=1, max=10) + wait_random_jitter(max_jitter_ms=1000), # Exponential backoff with jitter
    stop=stop_after_attempt(5), # Try a maximum of 5 times (max retry configuration)
    retry=retry_if_exception_type(RETRYABLE_LLM_ERRORS), # Conditional retry
    reraise=True # Re-raise the exception if all retries fail
)
def reliable_llm_call(llm_client, prompt: str):
    """
    A function that calls an LLM and is wrapped with retry logic.
    """
    return llm_client.invoke(prompt)

# --- Example Usage ---
print("\n--- Scenario 1: Successful after retries ---")
mock_llm_client_1 = MockLLM(fail_count=2) # Fails 2 times, succeeds on 3rd
try:
    result = reliable_llm_call(mock_llm_client_1, "What is the capital of France?")
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error after all retries: {e}")


print("\n--- Scenario 2: All retries fail ---")
mock_llm_client_2 = MockLLM(fail_count=5) # Fails 5 times, max attempts is 5
try:
    result = reliable_llm_call(mock_llm_client_2, "Tell me a joke.")
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error after all retries: {type(e).__name__}: {e}")


print("\n--- Scenario 3: Non-retryable error occurs ---")
mock_llm_client_3 = MockLLM(fail_count=1, non_retryable_at_attempt=2) # Fails once, then non-retryable
try:
    result = reliable_llm_call(mock_llm_client_3, "What is [invalid data]?")
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error caught (non-retryable): {type(e).__name__}: {e}")
```

In this example, the `@retry` decorator makes `reliable_llm_call` very robust. It includes `exponential backoff patterns`, `retry with jitter`, and `conditional retry`. This is a powerful way to manage `langchain retry fallback error handling` effectively. You can learn more about `tenacity` on its [PyPI page](https://pypi.org/project/tenacity/).

### Fallback Strategies: Having a Backup Plan

What happens if, after all your retries, the LangChain application still can't get an answer? You've tried five times with `exponential backoff patterns` and `jitter`, but the AI service is just completely down. This is where `fallback chain design` comes into play.

A `fallback strategy` is your backup plan. It's what your application does when the main plan, even with retries, doesn't work. It's like having a spare tire when your main tire goes flat. It keeps your application from completely breaking down.

#### Designing Your Fallback Chain

A `fallback chain design` means you have a series of backup options. If the first backup doesn't work, you try the next one, and so on. This creates a resilient flow for your application.

Think of it as a priority list of what to do. Your primary choice is the full, powerful LLM. If that fails, maybe you try a simpler, cheaper LLM. If that also fails, maybe you provide a predefined answer.

LangChain itself offers mechanisms like `with_fallback` that help you build these chains easily. You are basically telling LangChain, "If this part fails, try this next thing instead." This is essential for good `langchain retry fallback error handling`.

##### Simple Fallback Options

1.  **Alternative Model Fallback:** Use a different, perhaps smaller or more robust, LLM.
2.  **Cached Responses:** Return an answer you've used before for a similar question.
3.  **Default/Canned Response:** Provide a generic "I can't answer that right now" message.
4.  **Error Notification:** Tell the user or log the error for a human to fix.

#### Alternative Model Fallback

One of the most powerful `fallback chain design` strategies is `alternative model fallback`. You might be using a very advanced and expensive LLM for most tasks. But if that model fails, you could switch to a simpler, perhaps cheaper, or locally hosted model.

This backup model might not give as detailed or nuanced answers. However, it will still provide *some* kind of answer. This is much better than your application crashing or giving no response at all.

For example, if your primary model is OpenAI's GPT-4, your `alternative model fallback` could be GPT-3.5 or even a smaller open-source model like Llama 2 running on a local server. The goal is to keep the conversation going.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnableLambda

# Imagine these are your primary and fallback LLMs
# In a real scenario, ChatOpenAI could be configured to actually fail for testing.
# For this example, we'll simulate primary_llm failure explicitly.
primary_llm = ChatOpenAI(model="gpt-4", temperature=0.7) # Your main powerful model
# Fallback to a cheaper or local model like Ollama
# Make sure you have Ollama running: https://ollama.ai/
# And a model pulled, e.g., 'ollama pull llama2'
fallback_llm = ChatOllama(model="llama2")
# Another fallback could be an even simpler, hardcoded response
def simple_fallback_response(input_dict):
    print("Executing simple_fallback_response...")
    return f"I'm sorry, I cannot process your request fully right now, but here's a general thought: {input_dict['question']} is an interesting topic."

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{question}")
])

# --- Simulate a primary LLM that *might* fail ---
class FailingChatOpenAI(ChatOpenAI):
    def __init__(self, should_fail=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._should_fail = should_fail
        print(f"FailingChatOpenAI initialized. Will fail: {self._should_fail}")

    def invoke(self, input, config=None):
        if self._should_fail:
            print("FailingChatOpenAI: Simulating a critical error (e.g., API key invalid, permanent outage).")
            raise ValueError("Simulated critical error: API not available!")
        print("FailingChatOpenAI: Successfully invoked (this path shouldn't be reached if should_fail is True).")
        return super().invoke(input, config)

# Primary LLM that we configure to fail for demonstration
failing_primary_llm = FailingChatOpenAI(should_fail=True, model="gpt-4", temperature=0.7)
working_primary_llm = FailingChatOpenAI(should_fail=False, model="gpt-4", temperature=0.7)


# Building the fallback chain
# This shows how you can use LangChain's .with_fallback()
# The order matters: primary -> fallback LLM -> simple function
chain_with_llm_fallback = prompt | failing_primary_llm.with_fallback(fallback_llm).with_fallback(RunnableLambda(simple_fallback_response))

# --- Example Usage ---
print("\n--- Scenario 1: Primary LLM Fails, Fallback LLM works ---")
try:
    response = chain_with_llm_fallback.invoke({"question": "Explain quantum physics simply."})
    print(f"Final response: {response.content}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# To demonstrate working primary, swap failing_primary_llm with working_primary_llm
print("\n--- Scenario 2: Primary LLM Works (if configured not to fail) ---")
chain_with_working_primary = prompt | working_primary_llm.with_fallback(fallback_llm).with_fallback(RunnableLambda(simple_fallback_response))
try:
    response = chain_with_working_primary.invoke({"question": "What is the capital of France?"})
    print(f"Final response: {response.content}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

In this example, the `with_fallback` method is a core part of `langchain retry fallback error handling`. It gracefully switches to a backup model, maintaining service even if the primary one has issues. The `fallback chain design` here is clear: primary model first, then a general model, then a fixed response.

#### Other Useful Fallbacks

Besides switching models, you have other simple yet effective `fallback strategies`.

*   **Default Answers:** For very common questions, you might have a pre-written answer. If the LLM fails, you can just return this default. For example, "What is your name?" might always return "I am an AI assistant."
*   **Cached Results:** If you've asked the same question before, you might have stored the answer. If the LLM fails, you can give the old, stored answer. This is good for saving costs too.
*   **User Notification:** Sometimes, the best fallback is just to tell the user that something went wrong. You can say, "I'm experiencing technical difficulties; please try again later."
*   **Logging and Alerting:** When a fallback is used, it's a good idea to record this event. This helps you understand why your primary systems are failing. You might also send an alert to a developer.

```python
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def get_cached_response(question):
    # Simulate a cache lookup
    cache = {
        "what is the weather like?": "The weather is currently sunny.",
        "who are you?": "I am an AI assistant.",
    }
    print(f"Checking cache for: {question}")
    return cache.get(question.lower(), None)

def general_error_message(input_dict):
    print("Executing general_error_message fallback...")
    return "I apologize, but I am unable to process your request at this moment. Please try again later."

# Combining cached and general message as a fallback sequence
# This would go *after* LLM fallbacks if they also fail
cached_or_default_fallback = (
    RunnableLambda(lambda x: get_cached_response(x['question'])) | StrOutputParser()
).with_fallback(RunnableLambda(general_error_message) | StrOutputParser())

# Example of how it might be used in a larger chain after LLMs have failed
# chain_after_llms_fail = (failing_llm_chain).with_fallback(cached_or_default_fallback)

# To demonstrate directly:
print("\n--- Scenario 3: Cached Fallback ---")
try:
    response = cached_or_default_fallback.invoke({"question": "Who are you?"})
    print(f"Fallback response: {response}")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Scenario 4: General Error Message Fallback ---")
try:
    response = cached_or_default_fallback.invoke({"question": "What is the meaning of life?"}) # Not in cache
    print(f"Fallback response: {response}")
except Exception as e:
    print(f"Error: {e}")
```

These `fallback strategies` ensure that your application remains user-friendly. Even when things go wrong, it can still provide some level of service. This is vital for a robust user experience and a complete `langchain retry fallback error handling` strategy.

### Combining Retry and Fallback for Robustness

Now, let's put it all together. The best `langchain retry fallback error handling` uses both retry logic and fallback strategies. They work hand-in-hand to create a super resilient application.

Think of it as a defense system. First, you try to fix the problem yourself (retry). If you can't fix it after a few tries, you switch to a backup plan (fallback). This layered approach handles a wide range of issues.

#### The Flow: Try -> Retry -> Fallback

Here's the typical flow of how these two ideas work together:

1.  **Try:** Your LangChain application makes its primary call to the LLM.
2.  **Retry:** If the primary call fails with a temporary error (like a timeout or rate limit), the retry logic kicks in. It tries again, using `exponential backoff patterns` and `jitter` for a few times (`max retry configuration`).
3.  **Fallback:** If all retries fail, or if the original error was a permanent one, the application moves to its `fallback chain design`. It tries the first backup, then the second, and so on.

This sequence ensures that you exhaust all chances of succeeding with your primary model before switching to a less ideal, but still functional, backup.

#### Fallback Sequence Optimization

When you design your `fallback chain design`, the order of your fallbacks matters. This is called `fallback sequence optimization`. You want to try the "best" fallback first, then the next best, and so on.

For example, a `fallback sequence optimization` might look like this:

1.  **Primary LLM Call** (with `retry decorators` for temporary errors).
2.  **Fallback to Alternative Powerful LLM** (e.g., GPT-3.5 if GPT-4 fails).
3.  **Fallback to Simpler/Cheaper LLM** (e.g., a local Llama model).
4.  **Fallback to Cached Response** (if question is in cache).
5.  **Fallback to Default/Canned Response** (for general answers).
6.  **Finally, Log Error and Inform User** (if nothing else works).

This careful `fallback sequence optimization` ensures that you deliver the best possible experience under challenging conditions. It prevents you from resorting to a generic message too quickly. You can read more about designing resilient systems in our article on [Building Fault-Tolerant AI Applications](/blog/building-fault-tolerant-ai-applications.md).

### Advanced Concepts for Super Reliability

To make your LangChain applications truly bulletproof, you can explore even more advanced techniques. These go beyond simple retries and fallbacks to handle very difficult or persistent problems.

#### Circuit Breaker Pattern

Imagine you have an electric circuit. If there's a problem, like too much power, a circuit breaker trips. It cuts off the power to prevent damage. This is a very similar idea to the `circuit breaker pattern` in software.

If your LangChain application repeatedly fails when trying to talk to a specific AI service, it might be overloaded or broken. Instead of continually trying and failing (and adding more stress), the `circuit breaker pattern` "trips." It temporarily stops your application from trying to call that broken service.

For a set period, any request to that service will immediately fail without even trying. This gives the broken service time to recover. After a while, the circuit breaker might "half-open" and allow a single test request. If that succeeds, it "closes" again, allowing normal traffic. If it fails, it "opens" again for longer.

This pattern is great for preventing cascading failures and protecting both your application and the external service. It's an advanced part of `langchain retry fallback error handling`.

```python
from pybreaker import CircuitBreaker, CircuitBreakerError
import time

# Create a circuit breaker
# fail_max: How many consecutive failures before the circuit opens
# reset_timeout: How long to wait before trying to close (in seconds)
llm_breaker = CircuitBreaker(fail_max=3, reset_timeout=10)

# Simulate an LLM function that fails sometimes
class MockLLMService:
    def __init__(self, failure_rate=0.7):
        self.failure_rate = failure_rate
        self.call_count = 0

    def invoke(self, prompt):
        self.call_count += 1
        if random.random() < self.failure_rate:
            print(f"MockLLMService: Attempt {self.call_count} failing...")
            raise Exception("Simulated LLM service error!")
        print(f"MockLLMService: Attempt {self.call_count} succeeding!")
        return f"Response for: {prompt}"

mock_service = MockLLMService(failure_rate=0.8) # High failure rate for demo

# Use the circuit breaker to protect the LLM call
# @llm_breaker
def call_protected_llm(prompt):
    return mock_service.invoke(prompt)

print("--- Circuit Breaker Demo ---")
for i in range(10):
    try:
        print(f"\n--- Request {i+1} ---")
        with llm_breaker: # Wrap the call in the breaker context
            result = call_protected_llm("Tell me something interesting.")
            print(f"Success: {result}")
    except CircuitBreakerError:
        print(f"CircuitBreaker is OPEN! Skipping call to LLM service.")
    except Exception as e:
        print(f"Caught an error from LLM: {e}")
    time.sleep(1) # Wait a bit between requests

print("\n--- Waiting for circuit to potentially close ---")
time.sleep(llm_breaker.reset_timeout + 2) # Wait longer than reset_timeout

print("\n--- Trying again after reset timeout ---")
try:
    with llm_breaker:
        result = call_protected_llm("Last attempt to tell something interesting.")
        print(f"Success: {result}")
except CircuitBreakerError:
    print(f"CircuitBreaker is OPEN! Still skipping call to LLM service.")
except Exception as e:
    print(f"Caught an error from LLM: {e}")
```

This demo shows how the circuit breaker can open after several failures. When it's open, it immediately raises a `CircuitBreakerError` without even trying to call the service. After the `reset_timeout`, it might try again. This helps manage overloaded services very effectively.

#### Monitoring and Alerting

You can't fix what you don't know is broken. Good `langchain retry fallback error handling` includes robust monitoring and alerting.

*   **Monitoring:** Keep an eye on how often retries are happening, and how often fallbacks are used. Are certain AI models failing more than others? Are your requests frequently hitting rate limits? Tools like Prometheus and Grafana can help you visualize this data.
*   **Alerting:** If retries become too frequent, or if fallbacks are being used constantly, you need to know immediately. Set up alerts (via email, SMS, or Slack) to notify your team. This allows you to jump in and fix underlying problems before they get worse.

Understanding these metrics helps you fine-tune your `max retry configuration`, `exponential backoff patterns`, and `fallback chain design`. This proactive approach helps maintain high reliability.

#### Testing Your Error Handling

It's not enough to just write `retry logic` and `fallback strategies`. You must test them! How do you know your `conditional retry` works if you never simulate the specific error?

*   **Unit Tests:** Write small tests for individual components. Can your retry decorator handle a temporary network error?
*   **Integration Tests:** Test how your LangChain application behaves when talking to a *mocked* LLM that deliberately throws errors (like in our examples).
*   **Chaos Engineering:** For very critical applications, you can even intentionally break things in a controlled way (e.g., temporarily block network access to an LLM) to see how your system reacts. This ensures your `langchain retry fallback error handling` is truly robust.

Testing is the only way to be confident that your application will behave as expected when things inevitably go wrong.

### Practical Examples and Code Snippets

Let's combine some of these concepts into a more comprehensive LangChain example, tying together `retry decorators`, `exponential backoff patterns`, and `fallback chain design`.

For this example, we'll use a `tenacity` decorated function and LangChain's `with_fallback`.

```python
import openai # For potential LLM errors
import httpx # For network errors
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, wait_random_jitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnableLambda, chain as runnable_chain
from langchain_core.output_parsers import StrOutputParser
import time
import random

# --- 1. Define Retry Logic with Tenacity ---
RETRYABLE_LLM_API_ERRORS = (
    openai.APITimeoutError,
    openai.APIConnectionError,
    httpx.RequestError, # General network issues
    # Note: openai.RateLimitError is often a distinct exception, include if relevant
    # You might also create custom exceptions for internal temporary failures
)

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=10) + wait_random_jitter(max_jitter_ms=1000),
    stop=stop_after_attempt(4), # Max 4 attempts (1 initial + 3 retries)
    retry=retry_if_exception_type(RETRYABLE_LLM_API_ERRORS),
    reraise=True # Re-raise if all retries fail, so fallback can catch it
)
def call_llm_with_tenacity_retry(llm_instance, prompt_input):
    """
    A wrapper function to apply tenacity retry logic directly to an LLM invocation.
    This simulates a LangChain component invoking the LLM.
    """
    print(f"  Attempting LLM call (actual invoke for: '{prompt_input['question'][:30]}...')")
    # Simulate an intermittent error for demonstration
    if random.random() < 0.7: # 70% chance of failure for primary
        raise openai.APIConnectionError(message="Simulated temporary API connection loss", http_body=None, http_headers=None, code=None)
    return llm_instance.invoke(prompt_input['question'])

# --- 2. Define Fallback Strategies ---

# Main LLM (configured to often fail for demo)
# In a real app, this would be a regular ChatOpenAI instance
class FrequentlyFailingChatOpenAI(ChatOpenAI):
    def invoke(self, input, config=None):
        # We handle retry outside for clarity; this just fails if our wrapper asks it to.
        # This class will just be called inside call_llm_with_tenacity_retry
        return super().invoke(input, config)

primary_llm = FrequentlyFailingChatOpenAI(model="gpt-4", temperature=0.7)
# For the actual invocation within the retry loop, we need a LangChain runnable.
# This creates a runnable that first formats the prompt, then calls our retried function.
retried_primary_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant focused on high quality answers."),
        ("user", "{question}")
    ])
    | RunnableLambda(lambda x: call_llm_with_tenacity_retry(primary_llm, x))
    | StrOutputParser()
)


# First Fallback: A simpler, cheaper LLM (e.g., GPT-3.5 or local Ollama)
fallback_llm_1 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
fallback_chain_1 = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a backup AI assistant providing concise answers."),
        ("user", "{question}")
    ])
    | fallback_llm_1
    | StrOutputParser()
)

# Second Fallback: A very simple, local/community LLM (e.g., Ollama's Llama2)
# Ensure Ollama is running and 'llama2' model is pulled.
fallback_llm_2 = ChatOllama(model="llama2")
fallback_chain_2 = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a basic AI assistant providing very short answers."),
        ("user", "{question}")
    ])
    | fallback_llm_2
    | StrOutputParser()
)

# Third Fallback: Cached response or generic message
cache = {
    "what is the capital of france?": "Paris is the capital of France.",
    "who is albert einstein?": "Albert Einstein was a famous physicist.",
}

def get_cached_or_default_response(input_dict):
    question = input_dict['question'].lower()
    if question in cache:
        print(f"    Fallback: Found cached response for '{question}'")
        return cache[question]
    else:
        print(f"    Fallback: No cached response, returning general message.")
        return "I am sorry, I am currently unable to provide a specific answer. Please try again or ask a different question."

fallback_chain_3 = RunnableLambda(get_cached_or_default_response) | StrOutputParser()

# --- 3. Build the Complete Chain with Fallbacks ---

# Primary chain with retry logic applied via the wrapper
# Then chain fallbacks using .with_fallback()
final_robust_chain = retried_primary_chain.with_fallback(fallback_chain_1).with_fallback(fallback_chain_2).with_fallback(fallback_chain_3)

# --- Example Usage ---
print("--- Starting Robust LangChain Demo ---")

questions = [
    "What is the capital of France?", # Should hit cache if primary fails
    "Explain the concept of general relativity simply.", # More complex, likely hit deeper fallbacks
    "Tell me a short story about a brave knight.", # New question, will go through all fallbacks
    "Who is Albert Einstein?", # Should hit cache
]

for i, q in enumerate(questions):
    print(f"\n--- Processing Question {i+1}: '{q}' ---")
    try:
        response = final_robust_chain.invoke({"question": q})
        print(f"Final Robust Response: {response}")
    except Exception as e:
        print(f"CRITICAL ERROR: All fallbacks failed! {e}")
```

This comprehensive example shows `langchain retry fallback error handling` in action. You have a primary chain protected by `retry decorators` (`tenacity`). If that fails after its `max retry configuration` (4 attempts), LangChain automatically moves to `fallback chain design` using `with_fallback`. It tries `alternative model fallback`s and then a default/cached response. This makes your application very resilient.

### Best Practices Summary

To recap, here are the key best practices for `langchain retry fallback error handling`:

*   **Implement Retry Logic:** Use `retry decorators` like `tenacity` for temporary errors.
*   **Use Smart Retries:** Employ `exponential backoff patterns` and `retry with jitter` to avoid overwhelming services.
*   **Configure Max Retries:** Set a reasonable `max retry configuration` to prevent infinite loops.
*   **Conditional Retry:** Only retry for errors that are likely to resolve themselves.
*   **Design Fallback Chains:** Create a clear `fallback chain design` with ordered backup options.
*   **Utilize Alternative Models:** Implement `alternative model fallback` to maintain service quality.
*   **Optimize Fallback Sequence:** Arrange your `fallback sequence optimization` from best backup to simplest.
*   **Consider Circuit Breakers:** For very critical services, use the `circuit breaker pattern`.
*   **Monitor and Alert:** Track errors and fallback usage, and set up alerts for critical issues.
*   **Test Thoroughly:** Always test your error handling to ensure it works as expected.

By following these practices, you can build LangChain applications that are not only powerful but also incredibly robust and reliable.

### Conclusion

Building with LangChain is about creating smart and effective AI tools. But true effectiveness means building tools that don't break down when faced with everyday challenges like network issues or busy servers. By mastering `langchain retry fallback error handling`, you give your applications the resilience they need.

You've learned how `retry logic` helps your application be patient and persistent. You've also seen how `fallback strategies` provide a safety net, ensuring your users always get some kind of response. Combining these techniques creates truly dependable AI experiences. Go forth and build robust LangChain applications!