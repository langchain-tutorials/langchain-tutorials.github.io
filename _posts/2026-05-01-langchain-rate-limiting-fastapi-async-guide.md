---
title: "LangChain Rate Limiting and Retry Strategies with FastAPI & Async APIs (Full Guide)"
description: "Master LangChain rate limiting and retry strategies for FastAPI & async APIs. Prevent errors, optimize performance, and build resilient applications now."
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
image: '/assets/images/langchain-rate-limiting-fastapi-async-guide.webp'
---

## Making Your AI Apps Super Reliable: A Guide to LangChain Rate Limiting and Retry Strategies with FastAPI & Async APIs

Have you ever used an app that suddenly stopped working or gave you an error? It can be super frustrating when things break. When you build smart applications with tools like LangChain, you're often talking to many different online services, like big AI models. These services have rules about how often you can ask them questions.

If you ask too many questions too quickly, they might tell you to slow down. This is called "rate limiting," and it's like a traffic cop for data. Also, sometimes things just go wrong for a moment, like a tiny internet hiccup. That's where "retry strategies" come in handy, letting your app try again automatically.

In this full guide, we'll explore how to make your LangChain applications built with FastAPI and using async programming super strong. You will learn how to handle these common challenges smoothly. We'll show you how to implement robust LangChain rate limiting and retry strategies so your apps always work well, even when things get busy.

### Why Your AI Apps Need Special Care: Understanding the Basics

Imagine you have a lemonade stand, and suddenly everyone wants lemonade at the same time. You can only make so many glasses per minute. If too many people ask at once, you might run out of lemons or just get overwhelmed.

Online services work similarly. They can only handle a certain number of requests in a specific time. If your LangChain application sends too many requests to an AI model or another online tool, that service might get overwhelmed and send back an error. This is often called a "429 Too Many Requests" error.

This is exactly why understanding LangChain rate limiting and retry strategies is so important. You want your app to be polite and persistent, not pushy and then give up. By using these strategies, you make sure your application is both efficient and reliable.

#### What is Rate Limiting? Keeping Things Fair

Rate limiting is like a rule that says "you can only send X messages per Y seconds." It helps protect online services from being overloaded. If a service didn't have rate limits, one busy app could slow it down for everyone else.

For your LangChain application, this means you need to be aware of the limits set by the services you use. If you are building an API with FastAPI that uses LangChain, you also want to protect your *own* API. You don't want someone to bombard your server with requests and crash it.

We'll look at how to set up `FastAPI rate limiting` to keep your own service stable. This ensures a good experience for all your users. It's a key part of making your async programming applications robust.

#### What are Retry Strategies? Giving It Another Go

Sometimes, an error isn't because you asked too much, but just a temporary problem. Maybe the internet connection flickered, or the service had a momentary glitch. In these cases, it's often a good idea to just try again.

A retry strategy is how your application decides when and how to try sending a request again after it fails. You wouldn't want to try again immediately and endlessly if the problem isn't temporary. That could make things even worse.

Good `retry middleware` helps your LangChain app intelligently re-send requests. It waits a bit, then tries again, waiting longer each time. This smart approach makes your application much more resilient to little bumps in the road.

### LangChain and External APIs: The Need for Robustness

LangChain is an amazing framework for building applications powered by large language models (LLMs). Whether you're making an AI agent that can use tools or a RAG application, you're constantly talking to external services. For instance, you might use an LLM from OpenAI, Google, or Anthropic.

These LLMs are external APIs, and they all have their own rules. If your LangChain agent is busy answering questions, it might hit those rate limits quickly. Without proper LangChain rate limiting and retry strategies, your agent could fail often.

Imagine your agent trying to use a tool to get some information, but the tool's API is temporarily busy. If your agent just gives up, your whole application stops working. This is where clever retry logic saves the day, allowing the agent to persist. You can learn more about building advanced agents with tools in our guide on [LangChain Google Gemini Function Calling Agent Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

### Building Resilience with FastAPI Rate Limiting

When you build your LangChain application using FastAPI, you're creating an API that other programs or users can talk to. Just like external LLMs have rate limits, your FastAPI application should too. This protects your server and ensures fair usage.

FastAPI is great for `async programming`, meaning it can handle many things at once. However, even with async, your server still has limits on its resources. Setting up `FastAPI rate limiting` is crucial to prevent overload.

#### Basic FastAPI Rate Limiting with `fastapi-limiter`

A popular way to add rate limiting to FastAPI is using libraries like `fastapi-limiter`. This library often uses Redis, a fast database, to keep track of how many requests each user or IP address is making.

First, you need to install the library and a Redis client:

```bash
pip install fastapi-limiter redis
```

Next, you'll set up Redis. For a simple local test, you can run Redis in a Docker container or install it directly.

```bash
docker run -d --name my-redis -p 6379:6379 redis
```

Now, let's see how to integrate it into your FastAPI app.

{% raw %}
```python
from fastapi import FastAPI, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import uvicorn
import redis.asyncio as aioredis
import asyncio

app = FastAPI()

# This is where we'll set up our LangChain components later
# For now, let's simulate a LangChain call
async def simulate_langchain_call(query: str):
    print(f"Simulating LangChain call for: {query}")
    await asyncio.sleep(1) # Simulate some work
    return f"Response for {query} from LangChain."

@app.on_event("startup")
async def startup():
    # Connect to Redis for rate limiting
    # Replace 'redis://localhost:6379' with your Redis URL if it's different
    redis_connection = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    print("FastAPI Limiter initialized with Redis.")

@app.get("/limited-query")
async def limited_query(request: Request, query: str, _: RateLimiter = RateLimiter(times=2, seconds=5)):
    """
    An endpoint that uses LangChain and is rate-limited.
    Allows 2 requests every 5 seconds per client.
    """
    result = await simulate_langchain_call(query)
    return {"message": f"Processed query: '{query}'", "result": result}

@app.get("/unlimited-hello")
async def unlimited_hello():
    """
    An endpoint without rate limiting.
    """
    return {"message": "Hello, this endpoint is unlimited!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
{% endraw %}

In this example, the `@app.on_event("startup")` code makes sure `fastapi-limiter` connects to Redis when your app starts. The `RateLimiter(times=2, seconds=5)` part means that each unique user (based on their IP address by default) can only make 2 requests to `/limited-query` within a 5-second window. If they try more, they'll get a 429 error.

This setup is great for protecting your server from being overwhelmed. It's a simple yet powerful way to incorporate `FastAPI rate limiting` into your `async programming` applications. You can define different limits for different endpoints, giving you fine-grained control.

### Smart Retries for LangChain with `tenacity`

While FastAPI rate limiting protects your API, you also need to protect your LangChain app when it talks to other services. These external services might have their own rate limits or temporary issues. This is where robust retry strategies come into play.

LangChain itself offers some basic retry mechanisms, especially within its LLM wrappers. However, for more advanced and flexible `retry middleware`, a library like `tenacity` is incredibly powerful. `tenacity` helps you add intelligent retry logic to almost any function.

#### Introducing `tenacity`: Your Retry Superhero

`tenacity` is a Python library that makes adding retry logic easy and flexible. You can tell it what kind of errors to retry, how long to wait between retries, and how many times to try again. It supports `async programming` perfectly, which is essential for modern LangChain and FastAPI applications.

First, install `tenacity`:

```bash
pip install tenacity
```

Now, let's see how to use it to make a LangChain call more resilient.

{% raw %}
```python
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from langchain_openai import OpenAI
from langchain_core.exceptions import OutputParserException, LangChainException # Example exceptions
import asyncio
import random

# --- Simulate an unreliable external API call ---
call_count = 0
async def unreliable_llm_call_simulate(prompt: str):
    global call_count
    call_count += 1
    print(f"Attempting LLM call (simulated) for: '{prompt}' - Attempt #{call_count}")
    # Simulate different types of failures
    if call_count % 3 == 0: # Simulate a rate limit or service unavailable
        raise Exception("Service Unavailable or Rate Limited (Simulated)")
    elif call_count % 5 == 0: # Simulate a parsing error that we might not want to retry by default
        raise OutputParserException("Failed to parse LLM output (Simulated)")
    elif call_count % 7 == 0: # Another generic LangChain error
        raise LangChainException("Generic LangChain error (Simulated)")
    
    # Simulate success after some failures
    print(f"Successfully got response for: '{prompt}'")
    return f"LLM response to '{prompt}' after {call_count} attempts."

# --- Using tenacity for retry strategies ---
@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10), # Wait 4, 8, 16 seconds... up to 10 seconds max
    stop=stop_after_attempt(5),                          # Try a maximum of 5 times
    retry=retry_if_exception_type(Exception) & ~retry_if_exception_type(OutputParserException),
    reraise=True                                         # Re-raise the last exception if all retries fail
)
async def make_resilient_llm_call(prompt: str):
    """
    Makes a simulated LangChain LLM call with retry logic.
    Retries on general Exceptions but not on OutputParserException.
    """
    global call_count # Reset for each call to see fresh retry logic
    call_count = 0
    return await unreliable_llm_call_simulate(prompt)

async def main():
    print("\n--- Testing resilient LLM call 1 ---")
    try:
        response = await make_resilient_llm_call("Tell me a short story.")
        print(f"Final LLM Response 1: {response}")
    except Exception as e:
        print(f"Failed to get LLM response 1 after retries: {e}")

    print("\n--- Testing resilient LLM call 2 (expecting OutputParserException won't retry) ---")
    global call_count
    call_count = 4 # Pre-set call_count to trigger OutputParserException quickly
    try:
        response = await make_resilient_llm_call("Summarize this text: ...")
        print(f"Final LLM Response 2: {response}")
    except Exception as e:
        print(f"Failed to get LLM response 2 (as expected for OutputParserException): {e}")

    print("\n--- Testing resilient LLM call 3 (eventual success) ---")
    call_count = 0 # Reset for a fresh start
    try:
        response = await make_resilient_llm_call("Generate a poem about space.")
        print(f"Final LLM Response 3: {response}")
    except Exception as e:
        print(f"Failed to get LLM response 3 after retries: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```
{% endraw %}

In this example, the `@retry` decorator from `tenacity` wraps our `unreliable_llm_call_simulate` function.
*   `wait_exponential` means it waits longer after each failed attempt (e.g., 4s, then 8s, up to 10s). This is very important for respecting `LangChain rate limiting` and not making problems worse.
*   `stop_after_attempt(5)` ensures it won't try forever, failing after 5 attempts if still unsuccessful.
*   `retry_if_exception_type(Exception) & ~retry_if_exception_type(OutputParserException)` is super smart. It tells `tenacity` to retry on *any* general error, but *not* if the error is an `OutputParserException`. This is useful because an output parsing error might mean the LLM gave a bad response, not a temporary network glitch, so retrying might not help. For more about output parsing, check out [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}).

This setup is a powerful way to implement `retry middleware` within your `async programming` LangChain applications. It significantly improves the robustness of your external API calls.

### Integrating LangChain Rate Limiting and Retry Strategies with FastAPI

Now let's put it all together. We'll create a FastAPI endpoint that uses LangChain, and we'll apply both FastAPI rate limiting to the endpoint and `tenacity` retries to the LangChain calls within it. This creates a truly resilient system.

First, ensure you have all necessary libraries installed:
```bash
pip install fastapi uvicorn redis "redis[async]" tenacity langchain_openai # And other LangChain deps you might need
```

{% raw %}
```python
from fastapi import FastAPI, Request, HTTPException, status
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import uvicorn
import redis.asyncio as aioredis
import asyncio
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, before_sleep_log
import logging
import sys

# LangChain specific imports
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.exceptions import OutputParserException, LangChainException

# Set up logging for tenacity
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(
    title="LangChain Resilient API",
    description="A FastAPI service demonstrating LangChain rate limiting and retry strategies.",
    version="1.0.0"
)

# --- Initialize Redis for FastAPI Limiter ---
@app.on_event("startup")
async def startup():
    redis_connection = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)
    print("FastAPI Limiter initialized with Redis.")

# --- LangChain Component Setup ---
# You would typically get your API key from environment variables
# For this example, let's assume it's set or you put a placeholder
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Ensure OpenAI API key is set
# if not os.getenv("OPENAI_API_KEY"):
#     raise ValueError("OPENAI_API_KEY environment variable not set.")

# Initialize OpenAI LLM (we'll simulate it for this example to control failures)
# llm = OpenAI(temperature=0.7)

# We'll use a simulated LLM for controlled testing of retries
call_count_for_simulated_llm = 0
async def simulated_openai_llm_invoke(prompt_value: str):
    global call_count_for_simulated_llm
    call_count_for_simulated_llm += 1
    print(f"  [Simulated LLM] Attempt {call_count_for_simulated_llm} for prompt: '{prompt_value[:50]}...'")
    
    # Simulate different failure modes
    # Fail on 1st and 3rd attempt, succeed on 2nd and 4th, etc. for a specific scenario
    if call_count_for_simulated_llm % 4 == 1 or call_count_for_simulated_llm % 4 == 3:
        await asyncio.sleep(0.5) # Simulate network delay before failure
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Simulated LLM Rate Limit/Service Unavailable"
        )
    # Simulate a non-retryable error sometimes, e.g., bad input or parser error
    elif call_count_for_simulated_llm % 7 == 0:
        await asyncio.sleep(0.2)
        raise OutputParserException("Simulated LLM output parsing error or bad request format.")
    
    await asyncio.sleep(random.uniform(0.1, 0.5)) # Simulate varying LLM response time
    return {"text": f"Simulated LLM response to '{prompt_value[:50]}...' (Attempt {call_count_for_simulated_llm})"}

class SimulatedOpenAI:
    """A minimal class to simulate OpenAI LLM's invoke method."""
    async def invoke(self, prompt_value: str):
        return await simulated_openai_llm_invoke(prompt_value)

simulated_llm = SimulatedOpenAI()

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that answers questions concisely."),
    ("user", "{query}")
])
output_parser = StrOutputParser()

# Create a LangChain runnable chain
chain: Runnable = prompt_template | simulated_llm | output_parser

# --- Tenacity Retry Strategy for LangChain Calls ---
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=20), # Exponential backoff: 2s, 4s, 8s... max 20s
    stop=stop_after_attempt(6),                          # Max 6 attempts
    retry=(retry_if_exception_type(HTTPException) & 
           retry_if_exception_type(status.HTTP_429_TOO_MANY_REQUESTS)) |
           retry_if_exception_type(asyncio.TimeoutError) | # Also retry on timeouts
           retry_if_exception_type(Exception),             # Catch other general errors
    reraise=True,
    before_sleep=before_sleep_log(log, logging.INFO) # Log before sleeping
)
async def invoke_langchain_with_retries(input_data: dict) -> str:
    """
    Invokes the LangChain runnable with built-in tenacity retry logic.
    Specific exceptions like 429 and general exceptions are retried.
    OutputParserException is NOT retried by this setup.
    """
    global call_count_for_simulated_llm
    call_count_for_simulated_llm = 0 # Reset for each new request
    
    # Check if the exception type should specifically NOT be retried (e.g., parsing errors)
    try:
        result = await chain.invoke(input_data)
        return result
    except OutputParserException as e:
        log.error(f"Non-retryable OutputParserException during LangChain invocation: {e}")
        # Re-raise immediately if it's a type we don't want to retry
        raise e
    except Exception as e:
        log.warning(f"Caught an exception during LangChain invocation (will retry if configured): {e}")
        raise e # Re-raise to let tenacity handle it if it matches the retry criteria

# --- FastAPI Endpoints ---

@app.post("/ask-ai")
async def ask_ai_with_rate_limit_and_retries(
    request: Request, 
    query: str, 
    _: RateLimiter = RateLimiter(times=5, seconds=10) # 5 requests every 10 seconds per client
):
    """
    An API endpoint that processes a user query using LangChain.
    - Protected by FastAPI rate limiting (5 requests / 10 seconds).
    - LangChain internal calls use tenacity for retries.
    """
    log.info(f"Received request for query: '{query}'")
    try:
        response_from_llm = await invoke_langchain_with_retries({"query": query})
        log.info(f"Successfully processed query: '{query}'")
        return {"query": query, "response": response_from_llm}
    except HTTPException as e:
        log.error(f"Final failure after retries for query '{query}': {e.detail}")
        raise HTTPException(
            status_code=e.status_code,
            detail=f"AI service failed after multiple retries: {e.detail}"
        )
    except Exception as e:
        log.error(f"Unexpected error after retries for query '{query}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred while processing your request: {e}"
        )

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is up and running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
{% endraw %}

In this comprehensive example:
1.  **FastAPI Rate Limiting**: The `/ask-ai` endpoint is protected by `RateLimiter(times=5, seconds=10)`. This means any single user IP can make only 5 calls within a 10-second window. This is our `FastAPI rate limiting` in action.
2.  **Simulated LangChain Call**: We've set up a `simulated_openai_llm_invoke` function to act like an LLM that sometimes fails. This allows us to easily test our retry logic without hitting real API limits or incurring costs.
3.  **Tenacity Retries**: The `invoke_langchain_with_retries` function wraps our LangChain `chain.invoke`. It uses `tenacity` to retry if the simulated LLM call returns a `HTTPException` with a 429 status code (simulating a rate limit or service unavailable). It also retries on generic `Exception` but specifically `NOT` on `OutputParserException`. The `before_sleep_log` helps you see the retries happening.
4.  **Error Handling**: The `/ask-ai` endpoint catches potential `HTTPException` (like the 429 from our simulated LLM after all retries fail) and generic `Exception` to provide meaningful error messages to the client.

This setup showcases how you can combine `FastAPI rate limiting` to protect your service with `tenacity` as `retry middleware` to make your LangChain external calls robust. It's a prime example of effective `async programming` for resilient AI applications.

### Understanding the Flow of a Resilient AI App

Let's trace how a request moves through this combined system:

1.  **User sends request to your FastAPI app**: A user or another program sends a query to `/ask-ai`.
2.  **FastAPI Rate Limiting Check**: `fastapi-limiter` immediately checks if this user has exceeded their allowed requests.
    *   If **over limit**: FastAPI sends back a `429 Too Many Requests` error directly. Your internal LangChain logic is never even touched. This protects your server resources.
    *   If **within limit**: The request proceeds to your `/ask-ai` function.
3.  **LangChain Call with Retries**: Inside `/ask-ai`, `invoke_langchain_with_retries` is called.
    *   This function tries to talk to the simulated LLM (or a real one).
    *   If the LLM call fails with a retryable error (like a 429 from the LLM or a generic issue), `tenacity` waits and tries again. It logs each attempt.
    *   If the LLM call fails with a non-retryable error (like an `OutputParserException`), `tenacity` stops immediately and raises the error.
    *   If the LLM call eventually succeeds within the retry limits, the response is returned.
    *   If all retries fail, `tenacity` raises the last error.
4.  **Final Response to User**:
    *   If LangChain processing was successful, your FastAPI endpoint sends back the AI's response.
    *   If LangChain processing failed (after all retries), your FastAPI endpoint catches the error and sends an appropriate error message to the user (e.g., "AI service failed after multiple retries").

This layered approach ensures that both your service and your interactions with external services are protected. It's the cornerstone of building reliable applications with LangChain and `async programming`. You can also explore building more complex AI agents with state using frameworks like [LangGraph StateGraph Multi-Step AI Agent]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

### Advanced Considerations for LangChain Rate Limiting and Retry Strategies

Beyond the basic setup, there are more advanced ways to fine-tune your LangChain rate limiting and retry strategies. These help your application handle even more complex scenarios.

#### Different Error Types for Retries

Not all errors should be retried. As seen with `OutputParserException`, some errors signal a deeper problem that retrying won't fix.
You might want to specifically retry on:
*   `HTTP 429 Too Many Requests`
*   `HTTP 503 Service Unavailable`
*   Network timeouts (like `asyncio.TimeoutError`)
*   Connection errors

You might want to *avoid* retrying on:
*   `HTTP 400 Bad Request` (Your input is wrong)
*   `HTTP 401 Unauthorized` (Your API key is bad)
*   `HTTP 404 Not Found` (The resource doesn't exist)
*   `OutputParserException` (The AI's response format is unexpected, which might mean a prompt issue).

Carefully choosing which exceptions trigger retries makes your `retry middleware` much more effective.

#### Circuit Breakers

Imagine a situation where an external API is completely down for a long time. If your `retry middleware` keeps trying and trying, it wastes your resources and might even make the problem worse for the failing service. A "circuit breaker" pattern can help here.

A circuit breaker is like an electrical fuse. If too many failures happen in a short time, it "trips" and stops sending requests to that service for a while. After a cool-down period, it might try one or two requests to see if the service is back up. If it is, the circuit "closes" and normal operation resumes.

While `tenacity` doesn't have a built-in circuit breaker, libraries like `pybreaker` can be integrated. This is a more advanced pattern but crucial for truly robust systems.

#### Global vs. Per-User Rate Limiting

In our FastAPI example, `fastapi-limiter` by default uses the client's IP address for rate limiting. This is a "per-user" or "per-client" limit.
You might also need a "global" rate limit for your entire FastAPI application, regardless of the client. This prevents your server from exceeding its total capacity.
You can achieve this by having a global `RateLimiter` on your main app or using a different key generator for `fastapi-limiter`.

#### Distributed Rate Limiting

If your FastAPI application runs on multiple servers, you'll need a way to share the rate limiting information across all of them. This is where Redis (which `fastapi-limiter` uses) becomes essential. All your FastAPI instances can talk to the same Redis server to keep a consistent count of requests. This is key for scalable `async programming` services.

#### Dynamic Limits and Configuration

Sometimes, the rate limits of external APIs can change. Instead of hardcoding `times=X` and `seconds=Y` in your code, consider storing these values in a configuration file or environment variables. This allows you to update limits without changing and redeploying your code. You can also fetch them dynamically from an API if the external service provides this.

### Practical Scenario: Building a LangChain RAG Application with Resilient Features

Let's imagine you're building a RAG (Retrieval Augmented Generation) application using LangChain. This application retrieves information from a vector store and then uses an LLM to generate answers. Both the vector store and the LLM are external services.

For an in-depth guide on RAG applications, you can refer to our posts on [Build RAG Applications LangChain Vector Store 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}) and [LangChain Weaviate Hybrid Search Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

Here's how LangChain rate limiting and retry strategies fit into this:

*   **FastAPI Endpoint**: Your `/rag-query` endpoint in FastAPI allows users to ask questions. This endpoint needs `FastAPI rate limiting` to prevent a single user from overwhelming your service.
    ```python
    @app.post("/rag-query")
    async def get_rag_answer(request: Request, query: str, _: RateLimiter = RateLimiter(times=3, seconds=15)):
        # ... RAG logic here ...
    ```
*   **Vector Store Calls**: When your LangChain app queries the vector store (e.g., Weaviate, Pinecone), this is an external API call. These calls can sometimes fail due to network issues or the vector store's own rate limits. You would wrap these calls with `tenacity`.
    ```python
    from langchain_community.vectorstores import Weaviate
    # ... Weaviate client setup ...

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(4))
    async def get_docs_from_vectorstore(query: str):
        # This function would internally call weaviate_client.similarity_search_with_score
        # or similar methods.
        print(f"  Attempting vector store search for: {query}")
        # Simulate Weaviate call
        await asyncio.sleep(0.5)
        if random.random() < 0.3: # 30% chance of failure
            raise Exception("Simulated Vector Store API error")
        return [f"Doc 1 for {query}", f"Doc 2 for {query}"]

    # ... in your /rag-query endpoint ...
    retrieved_docs = await get_docs_from_vectorstore(query)
    ```
*   **LLM Calls**: After retrieving documents, your LangChain chain sends the prompt and documents to the LLM. This is another critical external API call. This is where the `invoke_langchain_with_retries` function we built earlier (or similar `tenacity` wrapped LLM invocation) is crucial.
    ```python
    # ... inside /rag-query endpoint after getting docs ...
    full_prompt_for_llm = f"Context: {retrieved_docs}\nQuestion: {query}"
    final_answer = await invoke_langchain_with_retries({"query": full_prompt_for_llm})
    ```
By applying `LangChain rate limiting and retry strategies` at each interaction point, your RAG application becomes much more dependable. If the vector store glitches, `tenacity` will retry. If the LLM is busy, `tenacity` will also retry. If a user floods your API, `FastAPI rate limiting` will handle it gracefully. This layering of resilience is essential for any serious `async programming` application.

### Conclusion: Building Unstoppable AI Applications

You've learned that building resilient AI applications with LangChain, FastAPI, and `async programming` is about smart planning and implementation. Dealing with `LangChain rate limiting and retry strategies` isn't just a good idea; it's a necessity for production-ready systems. Without them, your users might face frustrating errors, and your servers could buckle under unexpected load.

By using tools like `fastapi-limiter` for `FastAPI rate limiting` and `tenacity` for robust `retry middleware`, you equip your applications to handle the unpredictable nature of external services and user behavior. This guide has provided you with the foundational knowledge and practical examples to make your LangChain applications not just smart, but also incredibly reliable.

Keep exploring the world of LangChain and its powerful capabilities. You can dive deeper into various components of LangChain for building complex systems, for example, by looking into [Top LangChain Alternatives 2026: 10 Frameworks Compared & Ranked]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}) to understand its place in the ecosystem. Your journey towards building unbreakable AI applications is well underway!