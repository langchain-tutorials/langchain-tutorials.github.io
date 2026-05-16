---
title: "Top 10 Best Practices for LangChain Rate Limiting and Retry Strategies in 2026"
description: "Master LangChain rate limiting and retry strategies. Boost your AI app's stability and performance in 2026 with these top 10 best practices."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain rate limiting and retry strategies]
featured: false
image: '/assets/images/langchain-rate-limiting-best-practices-2026.webp'
---

## Top 10 Best Practices for LangChain Rate Limiting and Retry Strategies in 2026

Imagine you're asking a super-smart friend many questions very quickly. If you ask too fast, your friend might get overwhelmed and tell you to slow down. In the world of computers, this is like hitting a "rate limit" when your LangChain application talks to powerful AI models.

When your LangChain app sends too many requests to an API, like OpenAI or Google Gemini, the API might temporarily block you. This is called rate limiting, and it's there to keep the service stable for everyone. To handle this smoothly, we use smart "retry strategies" that teach your app to try again later.

These strategies are super important for building reliable LangChain applications in 2026. They help your app keep working even when things get busy or have a tiny hiccup. Let's explore the best ways to make your LangChain applications resilient and efficient.

### What are LangChain Rate Limiting and Retry Strategies?

Rate limiting is like a traffic controller for your API requests. It makes sure you don't send too many requests in a short time, preventing the API from getting overloaded. Think of it as a limit on how many messages you can send per minute.

Retry strategies are your application's plan B. If an API call fails because of a temporary issue, a retry strategy tells your app to wait a bit and try again. It's like calling your friend back if their phone was busy the first time.

Together, these two ideas ensure your LangChain applications run smoothly and efficiently. They are key for robust `request handling` when dealing with external services. This blog will guide you through the top practices for solid `LangChain rate limiting and retry strategies`.

### Why are these Practices Crucial for LangChain in 2026?

LangChain applications often connect to various powerful AI models and tools. These external services almost always have limits on how many requests you can make. If you ignore these limits, your application will fail often.

Good `API optimization` means your LangChain app can reliably talk to these services without getting blocked. It also means your users get a smooth experience, not frustrating error messages. Mastering `retry policies` ensures your application handles hiccups gracefully, making it more robust.

In 2026, as AI models become even more central to applications, these best practices are not just good to have. They are essential for any serious LangChain developer. Let's dive into the top 10 best practices.

### 1. Understand API Rate Limits

The very first step is to know the rules of the road for each API you use. Every external service, like OpenAI, Anthropic, or Hugging Face, has specific rate limits. These limits tell you how many requests or tokens you can send per minute or second.

You need to read the documentation for each specific API your LangChain app connects to. For example, OpenAI has different limits for tokens per minute (TPM) and requests per minute (RPM). Knowing these numbers helps you plan your `LangChain rate limiting and retry strategies`.

For instance, if you are using Google Gemini models through LangChain, you must check Google Cloud's specific quotas. Understanding these limits prevents your application from hitting unexpected roadblocks. It's like knowing the speed limit before you start driving.

#### Practical Example: Checking OpenAI Limits

You can usually find these limits in the service's developer documentation. OpenAI, for example, shows limits in your API usage dashboard. You might see something like 60,000 TPM and 3,000 RPM for a specific model.

Your LangChain application, especially one leveraging [LangChain Google Gemini Function Calling Agent with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}), needs to respect these. If you're building a RAG application, consider how many calls your vector store might make. A complex retrieval process might quickly hit token limits, especially when working with extensive data, as discussed in [Build RAG Applications with LangChain Vector Store in 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

### 2. Implement Exponential Backoff with Jitter

When an API tells you to slow down (a 429 error), you shouldn't just try again immediately. That's like repeatedly knocking on a locked door. Instead, you should wait a bit, and if it fails again, wait even longer. This clever strategy is called exponential backoff.

Exponential backoff means increasing the waiting time between retries. For example, you might wait 1 second, then 2, then 4, then 8, and so on. This gives the API time to recover and prevents you from making the problem worse. It's a key part of good `retry policies`.

Adding "jitter" means you add a small random amount of time to each wait. If many applications all use the same backoff strategy, they might all try again at the exact same moment. Jitter helps spread out these retry attempts, preventing another rush on the API. This is crucial for robust `request handling`.

#### Practical Example: Using `tenacity` in LangChain

Python's `tenacity` library is perfect for implementing this in LangChain. You can wrap your API calls with its `@retry` decorator. It automatically handles exponential backoff and jitter for you.

Here's how you might use it for an OpenAI call within LangChain:

{% raw %}
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from openai import RateLimitError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Initialize your LLM
# Be sure to set your OpenAI API key as an environment variable (OPENAI_API_KEY)
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")

# Define your prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{question}")
])

# Create a chain
chain = prompt | llm

# Define the retry decorator
# We'll retry if RateLimitError occurs
# We'll wait exponentially starting from 1 second, up to 10 seconds,
# for a maximum of 6 attempts.
@retry(
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type(RateLimitError),
    reraise=True # Re-raise the exception if all retries fail
)
def call_llm_with_retry(question: str):
    """
    Function to call the LLM chain with retry logic.
    """
    print(f"Attempting to call LLM for question: '{question[:30]}...'")
    response = chain.invoke({"question": question})
    print("LLM call successful.")
    return response.content

# Example usage (this might hit rate limits if called rapidly)
if __name__ == "__main__":
    try:
        result1 = call_llm_with_retry("What is the capital of France?")
        print(f"Result 1: {result1[:50]}...")

        # Simulate another call that might hit a limit
        result2 = call_llm_with_retry("Tell me a short story about a brave knight.")
        print(f"Result 2: {result2[:50]}...")

    except RateLimitError as e:
        print(f"Failed after multiple retries due to: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
```
{% endraw %}

This example shows how `tenacity` helps your LangChain calls recover from `RateLimitError`. This `API optimization` makes your application much more robust.

### 3. Use LangChain's Built-in Retry Mechanisms

LangChain itself often comes with some built-in retry logic for common LLM providers. Before adding your custom `tenacity` wrappers, always check what's already provided. This can save you a lot of effort and ensure consistent `LangChain rate limiting and retry strategies`.

Many LangChain components, especially those interacting with specific LLM APIs, may have default retry settings. These defaults are often a good starting point and might include basic exponential backoff. However, you might need to customize them for specific `API optimization` needs.

Knowing about these built-in features helps you avoid writing extra code that isn't needed. It also ensures you leverage the framework's strengths. Always refer to the official LangChain documentation for the specific integration you're using.

#### Practical Example: Configuring LLM Retries

Some LangChain LLM classes allow you to pass specific retry parameters. While direct `retry` parameters aren't universally exposed for all errors on `ChatOpenAI` directly in the constructor, you can often configure the underlying client or use custom wrappers.

For instance, `openai.OpenAI` client (which LangChain uses) handles some retries by default. You can often pass `max_retries` when initializing the client. LangChain models sometimes expose ways to configure the client:

{% raw %}
```python
from langchain_openai import ChatOpenAI
from openai import OpenAI

# Initialize the base OpenAI client with custom retry settings
# This is a general Python client, not specific to LangChain directly,
# but LangChain models often accept a pre-configured client.
# Note: LangChain's ChatOpenAI might not always directly expose 'max_retries'
# from its constructor for the client. This example shows a common pattern.
custom_openai_client = OpenAI(
    max_retries=5, # Number of retries for transient errors
)

# If ChatOpenAI could accept a pre-configured client directly (check docs for your version)
# llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", client=custom_openai_client)
# For now, let's show how to explicitly use client retry settings if available.

# More commonly, you'd rely on 'tenacity' or similar for fine-grained control
# as shown in the previous example, or LangChain's internal defaults.

# Let's show how some other LangChain components might implicitly or explicitly
# handle retries or allow configuration.
# The core idea is to know where to look in the LangChain source/docs for retry configs.

# For robust production applications, explicit retry logic like 'tenacity'
# is often preferred for its flexibility in defining retry conditions.

print("LangChain's internal handling might exist or require client configuration.")
print("Always check the specific LLM integration documentation for retry options.")

```
{% endraw %}

This helps with good `API optimization` by letting the LLM handle some transient network issues automatically. For advanced `retry policies`, you'd still combine this with `tenacity`.

### 4. Differentiate Retriable vs. Non-Retriable Errors

Not all errors should trigger a retry. If an API returns an error saying "Your input is invalid" (a 400 or 400-range error), trying again won't fix it. The problem is with your request, not a temporary network glitch. Retrying such errors wastes resources.

You should only retry for transient errors. These are temporary problems like rate limits (429), server errors (5xx codes), or network timeouts. Errors like "authentication failed" (401) or "resource not found" (404) are usually not transient. These require you to fix your code or configuration.

By being smart about which errors to retry, you improve your `request handling` efficiency. This also prevents your application from getting stuck in an endless retry loop for errors it can't solve. It's a crucial part of smart `LangChain rate limiting and retry strategies`.

#### Practical Example: Customizing `tenacity` for Error Types

You can tell `tenacity` exactly which exceptions to retry. This makes your `retry policies` much more intelligent.

{% raw %}
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from openai import RateLimitError, APIError, APIConnectionError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from httpx import HTTPStatusError # Common for underlying HTTP client errors

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{question}")
])
chain = prompt | llm

# Define a list of exceptions that are generally considered retriable
RETRIABLE_EXCEPTIONS = (
    RateLimitError,      # Too many requests
    APIError,            # General API error, could be transient server-side
    APIConnectionError,  # Network issues
    HTTPStatusError,     # Generic HTTP status errors, especially 5xx
                         # You might add specific 5xx errors if httpx exposes them
)

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=20), # Max wait increased for robustness
    stop=stop_after_attempt(7), # Max attempts increased
    retry=retry_if_exception_type(RETRIABLE_EXCEPTIONS),
    reraise=True
)
def call_llm_smart_retry(question: str):
    print(f"Attempting to call LLM with smart retry for: '{question[:30]}...'")
    response = chain.invoke({"question": question})
    print("LLM call successful.")
    return response.content

# Example usage
if __name__ == "__main__":
    try:
        # This call would retry on RateLimitError, APIError, etc.
        result1 = call_llm_smart_retry("Explain quantum entanglement simply.")
        print(f"Smart Retry Result 1: {result1[:50]}...")

        # If an error like 404 (Not Found) or 400 (Bad Request) occurred,
        # and it's not a subclass of the listed exceptions, it would not retry.
        # This prevents pointless retries for bad input.

    except RateLimitError as e:
        print(f"Failed after smart retries due to rate limit: {e}")
    except APIError as e:
        print(f"Failed after smart retries due to API error: {e}")
    except Exception as e:
        print(f"An unretriable or unexpected error occurred: {e}")
```
{% endraw %}

This targeted approach to `retry policies` is vital for effective `API optimization`.

### 5. Configure Timeout Settings

Waiting forever for a response is not an option. If an API call hangs, your application needs to know when to give up and try again, or declare a failure. This is where timeout settings come in handy.

Timeouts define the maximum amount of time your application will wait for an API response. If the response doesn't arrive within that time, the call is considered failed. This prevents your application from getting stuck indefinitely.

Configuring sensible timeouts for your LangChain API calls improves `request handling` and overall system responsiveness. It works hand-in-hand with `LangChain rate limiting and retry strategies` to ensure your app stays agile.

#### Practical Example: Setting Timeouts in LangChain

Many LangChain LLM classes allow you to specify a `timeout` parameter. This directly controls how long your application waits for the AI model's response.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from openai import APITimeoutError, RateLimitError

# Initialize your LLM with a specific timeout
# The 'timeout' parameter can be set for the underlying client if not directly
# exposed by the LangChain class's __init__.
# For ChatOpenAI, it's typically set on the client object itself.
# Let's assume for simplicity we can pass it or it defaults to a client-level setting.
# A common way is to pass it to the underlying client:
# from openai import OpenAI
# client = OpenAI(timeout=15.0) # 15 seconds
# llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, openai_api_key="...", client=client)

# Or, if LangChain directly supports it (check specific model docs):
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", request_timeout=15.0) # 15 seconds timeout
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant who answers quickly."),
    ("user", "{question}")
])
chain = prompt | llm

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30), # Longer max wait for timeout
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((APITimeoutError, RateLimitError)), # Retry on timeout or rate limit
    reraise=True
)
def call_llm_with_timeout_retry(question: str):
    print(f"Attempting LLM call with timeout and retry for: '{question[:30]}...'")
    response = chain.invoke({"question": question})
    print("LLM call successful within timeout.")
    return response.content

# Example usage
if __name__ == "__main__":
    try:
        # If the API takes longer than 15 seconds, an APITimeoutError will be raised
        # and tenacity will attempt a retry.
        result = call_llm_with_timeout_retry("What are the key differences between general AI and narrow AI? Give a detailed explanation that might take a moment.")
        print(f"Timeout Retry Result: {result[:100]}...")
    except APITimeoutError as e:
        print(f"Failed after retries due to API timeout: {e}")
    except RateLimitError as e:
        print(f"Failed after retries due to rate limit: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
```
{% endraw %}

Setting `request_timeout` ensures your LangChain application doesn't hang forever, boosting your `API optimization`.

### 6. Monitor API Usage and Health

You can't fix what you don't know is broken or stressed. Monitoring your API usage is like checking your car's fuel gauge and engine lights. It tells you if you're getting close to your rate limits or if the API itself is having issues.

Use monitoring tools to track the number of requests you're sending, the response times, and the error rates. Many API providers offer dashboards where you can see this information. Logging your application's API calls and responses is also very helpful.

Regular monitoring allows you to proactively adjust your `LangChain rate limiting and retry strategies`. You can increase capacity, optimize your calls, or inform users if an external service is struggling. This is crucial for maintaining excellent `request handling`.

#### Practical Example: Simple Logging for Monitoring

While full monitoring systems are complex, you can start with simple logging. This helps you track successes, failures, and retries within your LangChain application.

{% raw %}
```python
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
from openai import RateLimitError, APITimeoutError

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", request_timeout=15.0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise AI assistant."),
    ("user", "{question}")
])
chain = prompt | llm

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError)),
    before_sleep=before_sleep_log(logger, logging.INFO), # Log before each retry wait
    reraise=True
)
def call_llm_with_monitoring(question: str):
    logger.info(f"Attempting LLM call for: '{question[:30]}...'")
    response = chain.invoke({"question": question})
    logger.info("LLM call successful.")
    return response.content

# Example usage
if __name__ == "__main__":
    try:
        result = call_llm_with_monitoring("Summarize the economic impact of quantum computing in one paragraph.")
        logger.info(f"Monitoring Result: {result[:100]}...")
    except RateLimitError as e:
        logger.error(f"Failed after retries due to rate limit: {e}")
    except APITimeoutError as e:
        logger.error(f"Failed after retries due to API timeout: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
```
{% endraw %}

This simple logging gives you visibility into your `retry policies` and API interactions. It's a fundamental part of `API optimization`.

### 7. Implement Client-Side Rate Limiting

While APIs have their own rate limits, you can also control your outgoing request rate from your application. This is called client-side rate limiting. It's like having your own traffic controller before your requests even leave your app.

Client-side rate limiting helps prevent you from even *hitting* the API's rate limits in the first place. You can enforce your own rules, perhaps being a bit more conservative than the API's limits. This creates a smoother experience and reduces the chance of errors.

Common techniques include using "token bucket" or "leaky bucket" algorithms. These manage a steady flow of requests, ensuring you don't send bursts that exceed limits. It's a proactive approach to `LangChain rate limiting and retry strategies`.

#### Practical Example: Using a Rate Limiter Library

Python libraries like `limiter` or `ratelimit` can help you implement client-side rate limiting. You can apply them to your LangChain API calls.

Let's use a conceptual example, as directly integrating these can vary. Imagine you want to ensure your LangChain app doesn't send more than 10 requests per minute to OpenAI, regardless of OpenAI's actual limit.

{% raw %}
```python
from ratelimit import limits, sleep_and_retry
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a wise advisor."),
    ("user", "{question}")
])
chain = prompt | llm

# Define client-side rate limit: 10 calls per 60 seconds (1 minute)
CALLS_PER_MINUTE = 10
ONE_MINUTE = 60

@sleep_and_retry # This decorator handles the waiting if the limit is hit
@limits(calls=CALLS_PER_MINUTE, period=ONE_MINUTE)
def call_llm_with_client_rate_limit(question: str):
    """
    Function to call the LLM chain, respecting a client-side rate limit.
    """
    logger.info(f"Attempting LLM call (client-side limited) for: '{question[:30]}...'")
    response = chain.invoke({"question": question})
    logger.info("LLM call successful (client-side limit respected).")
    return response.content

# Example usage
if __name__ == "__main__":
    print("Starting client-side rate limit test...")
    for i in range(15): # Try to make more calls than allowed in a minute
        try:
            start_time = time.time()
            result = call_llm_with_client_rate_limit(f"What is the {i+1}th wonder of the world?")
            end_time = time.time()
            logger.info(f"Call {i+1} completed in {end_time - start_time:.2f}s. Result: {result[:50]}...")
            # time.sleep(0.5) # Simulate some processing time between calls
        except Exception as e:
            logger.error(f"Error during call {i+1}: {e}")

    print("Finished client-side rate limit test.")
```
{% endraw %}

This client-side control improves `request handling` by throttling your outgoing requests before they even reach the API. It's a smart `API optimization`.

### 8. Use Asynchronous Processing

Sending requests one by one can be slow, especially if you have to wait for each response. Asynchronous processing allows your LangChain application to send multiple requests at nearly the same time. It doesn't wait for one to finish before starting the next.

Think of it like a chef preparing several dishes at once instead of one after another. While one dish is simmering, the chef starts chopping vegetables for the next. This makes your application much faster and more efficient.

Asynchronous operations are excellent for managing a high volume of `request handling` and can indirectly help with rate limits. By completing tasks faster, you can sometimes fit more successful requests within a time window. It also pairs well with robust `retry policies`.

#### Practical Example: Async with LangChain Chains

LangChain chains can often be called asynchronously using `ainvoke()`. This lets you fire off multiple prompts without blocking your program.

{% raw %}
```python
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise AI assistant."),
    ("user", "{question}")
])
chain = prompt | llm

async def run_async_llm_calls():
    questions = [
        "What is the capital of Japan?",
        "Who wrote 'Romeo and Juliet'?",
        "Explain photosynthesis in one sentence.",
        "What is the largest ocean on Earth?",
        "What is the Pythagorean theorem?"
    ]

    print("Starting asynchronous LLM calls...")
    tasks = []
    for q in questions:
        # Using ainvoke to run the chain asynchronously
        tasks.append(chain.ainvoke({"question": q}))

    # Gather all results when they are ready
    results = await asyncio.gather(*tasks)

    print("\nAsynchronous LLM calls completed:")
    for i, res in enumerate(results):
        print(f"Question {i+1}: '{questions[i]}'\nAnswer: {res.content[:70]}...\n")

# To run the asynchronous function
if __name__ == "__main__":
    asyncio.run(run_async_llm_calls())
```
{% endraw %}

This use of async helps with `API optimization` by making your requests more concurrent. If you combine this with `LangChain rate limiting and retry strategies`, you get a powerful and efficient system. For complex multi-step agents, asynchronous execution with tools can be very effective, as explored in articles like [LangGraph StateGraph for Multi-Step AI Agents]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

### 9. Implement Centralized Retry Policies

If you have many different parts of your LangChain application making API calls, it's best to have a single, consistent way to handle retries. This is called a centralized retry policy. It's like having one set of rules for all traffic lights in a city.

Centralizing your retry logic means you don't have to copy-paste the same code everywhere. If you need to change a retry setting, you only change it in one place. This makes your code cleaner, easier to manage, and less prone to errors.

A consistent approach to `retry policies` ensures that all your API interactions follow the same best practices. This is vital for complex LangChain applications, especially those using custom output parsers or advanced search techniques, which are discussed in [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}) and [LangChain Weaviate Hybrid Search for Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

#### Practical Example: A Global Retry Wrapper

You can create a utility function or a class that encapsulates your retry logic. This function then becomes the single entry point for all API calls requiring retries.

{% raw %}
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
from openai import RateLimitError, APIError, APIConnectionError, APITimeoutError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define our standard retry decorator
STANDARD_RETRIES = retry(
    wait=wait_exponential(multiplier=1, min=1, max=60), # Wait up to 60 seconds
    stop=stop_after_attempt(8), # Up to 8 attempts
    retry=retry_if_exception_type((
        RateLimitError,
        APIError,
        APIConnectionError,
        APITimeoutError
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING), # Log warnings before retries
    reraise=True
)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", request_timeout=20.0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI specializing in historical facts."),
    ("user", "{question}")
])
chain = prompt | llm

@STANDARD_RETRIES
def call_llm_with_global_retry(question: str):
    """
    Function using the globally defined retry policy.
    """
    logger.info(f"Attempting LLM call with global retry for: '{question[:30]}...'")
    response = chain.invoke({"question": question})
    logger.info("LLM call successful with global retry policy.")
    return response.content

# Example usage for different parts of the application
if __name__ == "__main__":
    try:
        fact1 = call_llm_with_global_retry("When was the Battle of Hastings?")
        print(f"Fact 1: {fact1.content[:50]}...")

        # Another part of the app uses the same policy
        fact2 = call_llm_with_global_retry("Who was the first emperor of Rome?")
        print(f"Fact 2: {fact2.content[:50]}...")

    except Exception as e:
        logger.error(f"Global retry policy failed for an LLM call: {e}")
```
{% endraw %}

This pattern ensures consistent `LangChain rate limiting and retry strategies` across your entire application. It's a best practice for `API optimization`.

### 10. Implement Circuit Breakers

Even with the best retry strategies, sometimes an API might be down for a long time. Continuously retrying a completely broken service is pointless and can make things worse. A circuit breaker pattern is designed for these situations.

A circuit breaker is like an electrical fuse in your house. If too many failures happen in a row, the circuit breaker "trips," stopping further requests to that service for a while. This gives the service time to recover and prevents your application from wasting resources on doomed calls.

After a set time, the circuit breaker will allow a few "test" requests to pass through. If these succeed, it "resets" and allows normal traffic again. If they fail, it "stays open" for longer. This intelligent `request handling` is vital for extreme scenarios. It helps to differentiate truly unavailable services from transient issues, ensuring your `retry policies` are smart.

#### Practical Example: Using `pybreaker` with LangChain

The `pybreaker` library can add circuit breaker functionality to your LangChain calls. This makes your application extremely resilient.

{% raw %}
```python
from pybreaker import CircuitBreaker, CircuitBreakerError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{question}")
])
chain = prompt | llm

# Initialize a circuit breaker
# It will trip if 3 consecutive failures occur (fail_max=3)
# It will stay open for 5 seconds (reset_timeout=5)
# After reset_timeout, it enters HALF-OPEN state, allowing one test request.
# If test request fails, goes back to OPEN. If succeeds, goes to CLOSED.
openai_breaker = CircuitBreaker(
    fail_max=3,
    reset_timeout=5,
    exclude=(ValueError,) # Don't trip for these exceptions, e.g., bad input
)

def call_llm_with_circuit_breaker(question: str):
    """
    Function to call the LLM chain, protected by a circuit breaker.
    """
    try:
        # Use the circuit breaker to protect the LLM call
        response = openai_breaker.call(chain.invoke, {"question": question})
        logger.info("LLM call successful (protected by circuit breaker).")
        return response.content
    except CircuitBreakerError:
        logger.error("Circuit breaker is OPEN. LLM call was prevented.")
        raise # Re-raise to indicate failure to the caller
    except Exception as e:
        logger.error(f"LLM call failed, circuit breaker recorded: {e}")
        raise # pybreaker will intercept this and potentially trip

# Example usage
if __name__ == "__main__":
    print("Starting circuit breaker test...")
    # Simulate a few successful calls first
    for i in range(2):
        try:
            result = call_llm_with_circuit_breaker(f"What is the capital of planet {i+1}?")
            logger.info(f"Success {i+1}: {result[:50]}...")
        except Exception as e:
            logger.error(f"Caught unexpected error in main loop: {e}")
        time.sleep(0.1)

    print("\nSimulating failures to trip the circuit breaker...")
    # Simulate failures (e.g., API is down or throwing errors)
    # For a real test, you'd make the LLM call itself fail (e.g., mock the LLM or break API key)
    # Here, we'll manually trip it for demonstration
    for _ in range(openai_breaker.fail_max + 1): # +1 to ensure it trips
        try:
            # Manually forcing a failure for demo purposes
            raise ConnectionError("Simulated API connection error to trip breaker")
            # In a real app, this would be an actual API exception
            # call_llm_with_circuit_breaker("This question will fail to trip the breaker.")
        except ConnectionError as e:
            logger.warning(f"Simulated failure: {e}")
            # The circuit breaker needs to observe these exceptions to trip
            try:
                # We call the breaker's `call` method with a failing function
                # to manually demonstrate tripping
                openai_breaker.call(lambda: (_ for _ in ()).throw(ConnectionError("Simulated API connection error")))
            except (CircuitBreakerError, ConnectionError):
                pass # Expected behavior

        time.sleep(0.1) # Small delay

    print(f"\nCircuit Breaker state after failures: {openai_breaker.current_state}")

    print("\nAttempting calls while circuit breaker is OPEN...")
    # Now, try to call while the breaker is open
    for i in range(3):
        try:
            result = call_llm_with_circuit_breaker(f"What happens if I try again? {i+1}")
            logger.info(f"Unexpected success {i+1}: {result[:50]}...")
        except CircuitBreakerError:
            logger.info(f"Call {i+1} prevented by circuit breaker as expected.")
        except Exception as e:
            logger.error(f"Unexpected error during open circuit: {e}")
        time.sleep(0.1)

    print(f"\nWaiting for reset_timeout ({openai_breaker.reset_timeout}s)...")
    time.sleep(openai_breaker.reset_timeout + 1) # Wait for breaker to go HALF-OPEN

    print(f"\nCircuit Breaker state after timeout: {openai_breaker.current_state}")
    print("Attempting a call in HALF-OPEN state (should allow one test request)...")
    try:
        result = call_llm_with_circuit_breaker("Test question for HALF-OPEN state.")
        logger.info(f"Test call succeeded. Breaker should be CLOSED. Result: {result[:50]}...")
    except CircuitBreakerError:
        logger.info("Test call failed. Breaker should be OPEN again.")
    except Exception as e:
        logger.error(f"Unexpected error during HALF-OPEN test: {e}")

    print(f"\nFinal Circuit Breaker state: {openai_breaker.current_state}")

```
{% endraw %}

Implementing circuit breakers is an advanced but vital `API optimization` technique for your `LangChain rate limiting and retry strategies`. It ensures your application gracefully handles prolonged service outages without continuous, futile retries.

### Conclusion

Building robust LangChain applications in 2026 means being prepared for the unpredictable nature of external API interactions. `LangChain rate limiting and retry strategies` are not just technical details; they are fundamental pillars of reliable and efficient `request handling`. By understanding API limits, intelligently retrying errors with exponential backoff and jitter, and setting sensible timeouts, you can make your applications much more resilient.

Beyond these basics, implementing client-side rate limiting, leveraging asynchronous processing, centralizing your `retry policies`, and adding circuit breakers will elevate your `API optimization` to the next level. These practices ensure your LangChain applications can withstand temporary outages and high traffic, providing a smooth experience for your users. Adopt these best practices to build future-proof AI applications with LangChain.