---
title: "Enterprise LangChain: Error Handling Best Practices for Mission-Critical Systems"
description: "Ensure your mission-critical enterprise LangChain systems run flawlessly. Learn expert error handling best practices to build robust AI applications. Optimiz..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [enterprise langchain error handling mission-critical]
featured: false
image: '/assets/images/enterprise-langchain-error-handling-mission-critical-systems.webp'
---

## Enterprise LangChain: Error Handling Best Practices for Mission-Critical Systems

Imagine a complex machine that helps your business run smoothly every single day. If even a tiny part of it stops working, everything could grind to a halt. This is especially true for systems built with advanced tools like LangChain, which are becoming central to how many large companies operate. When these systems are **mission-critical**, meaning your business absolutely depends on them, errors aren't just annoying; they can be very costly.

You need to make sure your **enterprise LangChain error handling** is top-notch. This means planning for problems before they even happen. This guide will help you understand how to build resilient LangChain applications that can handle unexpected issues and keep your business running smoothly, no matter what.

### Why Error Handling is Crucial for Enterprise LangChain in Mission-Critical Systems

When your LangChain applications are doing important jobs, like helping customers, processing financial data, or automating crucial reports, any downtime or incorrect output can have big consequences. Think about a customer service chatbot that suddenly stops answering. Or perhaps a system that generates legal documents, but due to an error, it misses a key clause.

These situations can lead to lost revenue, unhappy customers, or even legal problems. That's why building strong **enterprise error strategies** into your LangChain projects is not just a good idea, it's a necessity. You need to ensure your systems meet **SLA compliance**, meaning they deliver on their promises about how often they work and how fast they respond.

#### What Makes a System "Mission-Critical"?

A system is "mission-critical" if your business cannot function properly without it. If this system goes down, it directly impacts your main business operations. For example, an online payment gateway is mission-critical for an e-commerce store. A LangChain-powered system that handles fraud detection for a bank would also be mission-critical.

The stakes are high, and every error, no matter how small, needs a clear plan for how to deal with it. This involves understanding various **high availability patterns** and ensuring your system can recover quickly.

#### The Role of LangChain in the Enterprise

LangChain helps you connect powerful language models (like GPT-4) with other tools and data sources. This allows you to build very smart applications. In an enterprise setting, these applications often interact with sensitive data, external APIs, and complex business logic. This intricate web of connections means there are many places where things can go wrong.

Your goal is to anticipate these potential failure points and build safeguards around them. This way, your LangChain solution remains robust and reliable, even when facing unexpected challenges.

### Understanding the Basics: Catching Errors in Python and LangChain

Before we dive into advanced strategies, let's revisit the fundamental way Python deals with errors. You likely already know about `try-except` blocks. These are your first line of defense.

You "try" to run some code, and "except" if something goes wrong. This simple structure allows you to catch specific errors and decide what to do next. For instance, if your LangChain agent tries to call an external API and that API isn't available, you can catch the `requests.exceptions.ConnectionError`.

```python
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_simple_langchain_call(query):
    try:
        # Example of a simple LangChain setup
        llm = OpenAI(temperature=0.7) # In a real enterprise setup, API key would be loaded securely
        prompt = PromptTemplate(input_variables=["query"], template="Answer the following question: {query}")
        chain = LLMChain(llm=llm, prompt=prompt)
        
        result = chain.run(query)
        logging.info(f"LangChain call successful for query: '{% raw %}{query[:50]}{% endraw %}'...")
        return result
    except Exception as e:
        logging.error(f"An error occurred during LangChain call: {% raw %}{e}{% endraw %}")
        return "I am sorry, I am currently unable to process your request."

# Example usage
print(run_simple_langchain_call("What is the capital of France?"))
# Simulate an error (e.g., API key invalid, network issue)
# For a real error, you might intentionally misconfigure `llm` or mock an exception.
# For demonstration, let's just show the error handling path with a placeholder message.
print(run_simple_langchain_call("Tell me about quantum physics but imagine the LLM fails."))
```

In this basic example, you wrap your LangChain operation in a `try-except` block. If any error occurs, you catch it, log it, and provide a polite fallback message to the user. This prevents your application from crashing completely.

### Best Practice 1: Robust Error Detection and Comprehensive Logging

Good logging is like leaving a trail of breadcrumbs so you can find your way back if you get lost. For **enterprise LangChain error handling**, detailed logs are essential for understanding what went wrong, when, and why. Without proper logging, debugging a complex system becomes a nightmare.

You need to record not just that an error happened, but also all the relevant context. This includes the input that led to the error, the specific component that failed, and any unique identifiers related to the transaction.

#### Structured Logging for Clarity

Instead of just printing simple messages, use structured logging. This means your log messages are formatted in a consistent way, often as JSON. This makes them easy for machines to read and analyze later.

Python's built-in `logging` module is powerful and configurable. You can set different logging levels like `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. Each level helps you categorize the importance of a message.

*   `INFO` messages tell you what the system is doing normally.
*   `ERROR` messages indicate a problem that needs attention.
*   `CRITICAL` messages signal a major failure that might stop the system.

**Example: Logging a Failed LLM Call with Context**

Let's enhance our previous example to use structured logging and capture more detail when an LLM call fails. This helps with **enterprise monitoring**.

```python
import logging
import json
import traceback
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException # Specific LangChain error

# Configure logging to output JSON (or a dictionary that can be converted to JSON)
# In a real app, you'd use a library like `structlog` or configure a JSONFormatter.
# For simplicity, we'll mimic structured output.
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "filename": record.filename,
            "lineno": record.lineno,
        }
        if hasattr(record, 'extra_data'):
            log_entry.update(record.extra_data)
        if record.exc_info:
            log_entry['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Handler for console output
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

def run_langchain_with_robust_logging(query, transaction_id="N/A"):
    extra_data = {"query_snippet": query[:100], "transaction_id": transaction_id}
    try:
        # Simulate an LLM call (e.g., could be OpenAI, HuggingFace, etc.)
        llm = OpenAI(temperature=0.7) # Assume API key is configured correctly
        prompt = PromptTemplate(input_variables=["query"], template="Answer the following question: {query}")
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Simulate a potential error, e.g., an LLM API timeout or an invalid response
        if "fail this" in query.lower():
            raise ValueError("Simulated LLM API failure due to specific input")
        
        result = chain.run(query)
        logger.info("LangChain call successful.", extra={"extra_data": extra_data, "result_snippet": {% raw %}{result[:100]}{% endraw %}})
        return result
    except OutputParserException as e:
        # Specific LangChain parsing error
        logger.error(f"Output parsing failed: {% raw %}{e}{% endraw %}", exc_info=True, extra={"extra_data": extra_data, "error_type": "OutputParsingError"})
        return "I had trouble understanding the model's response."
    except ValueError as e:
        # Catch our simulated error or other value-related issues
        logger.error(f"Input or internal value error: {% raw %}{e}{% endraw %}", exc_info=True, extra={"extra_data": extra_data, "error_type": "ValueError"})
        return "There was a problem with the input provided."
    except Exception as e:
        # Catch any other unexpected errors
        logger.critical(f"A critical, unexpected error occurred: {% raw %}{e}{% endraw %}", exc_info=True, extra={"extra_data": extra_data, "error_type": "UnhandledException"})
        return "I am experiencing a severe internal issue and cannot process your request."

# Practical examples
print("\n--- Successful Call ---")
print(run_langchain_with_robust_logging("Explain the concept of neural networks simply.", transaction_id="TXN-001"))

print("\n--- Simulated Failure Call ---")
# This will trigger our simulated ValueError
print(run_langchain_with_robust_logging("Please fail this specific query to test error handling.", transaction_id="TXN-002"))

print("\n--- Another Call ---")
print(run_langchain_with_robust_logging("What are the best practices for cloud security?", transaction_id="TXN-003"))

# You might internally link here to a blog post about logging best practices:
# [Link to your blog post on structured logging in Python]
```

Notice how `extra_data` is passed to the logger. This allows you to add specific context, like `transaction_id` or a `query_snippet`. This makes it much easier to trace problems back to their source. For truly **mission-critical** systems, logs should be collected centrally and easily searchable.

### Best Practice 2: Graceful Degradation and Fallbacks

Even the most robust systems will encounter issues sometimes. **Graceful degradation** means that when a part of your system fails, the whole system doesn't collapse. Instead, it continues to operate, perhaps with reduced functionality or a simpler approach. Think of it like a car going into "limp home" mode. It's not ideal, but it gets you where you need to go.

For **enterprise LangChain error handling**, this means planning alternative paths when a primary path fails. You want to maintain **business continuity** as much as possible.

#### Fallback Mechanisms for LLM Calls

If your primary LLM (e.g., a powerful, expensive model) fails or becomes too slow, what then?

1.  **Simpler LLM:** Fall back to a smaller, faster, or cheaper model. It might not be as nuanced, but it can still provide a basic answer.
2.  **Cached Responses:** For common queries, you might have pre-computed or cached answers.
3.  **Static Responses:** A polite "I'm sorry, I cannot fulfill that request right now" is better than a crash.
4.  **Human Hand-off:** For truly complex or sensitive issues, escalate to a human agent.

#### Fallback for Tool Calls

LangChain agents often use tools to fetch information or perform actions (e.g., search the web, query a database, call an internal API). What if one of these tools fails?

1.  **Alternative Tool:** Can another tool provide similar information?
2.  **Partial Data:** Can you proceed with incomplete data, perhaps acknowledging the limitation?
3.  **Default Values:** Use a sensible default if specific data can't be retrieved.

**Example: LangChain Chatbot with LLM and Tool Fallbacks**

Let's imagine a LangChain agent that answers questions about product inventory. It uses an LLM and an external "inventory API" tool.

```python
import logging
from langchain_community.llms import OpenAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain.prompts import PromptTemplate
from langchain import hub # For loading standard prompts

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Use a simple formatter for console output for this example
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# --- Simulate an external Inventory API ---
class MockInventoryAPI:
    def get_stock(self, product_id):
        if product_id == "FAIL_PRODUCT_001":
            logger.warning(f"Simulating failure for product {% raw %}{product_id}{% endraw %}")
            raise ConnectionError("Inventory API is temporarily unavailable.")
        if product_id == "PRODUCT_001":
            return {"product_id": product_id, "stock": 50, "location": "Warehouse A"}
        elif product_id == "PRODUCT_002":
            return {"product_id": product_id, "stock": 0, "location": "Warehouse B"}
        else:
            return {"product_id": product_id, "stock": "unknown", "message": "Product not found."}

inventory_api = MockInventoryAPI()

# --- Define Tools ---
def get_product_stock_tool(product_id: str) -> str:
    """Gets the current stock level for a given product ID from the inventory API."""
    try:
        data = inventory_api.get_stock(product_id)
        if data.get("stock") == "unknown":
            return f"Could not find information for product ID: {% raw %}{product_id}{% endraw %}. {% raw %}{data.get('message', '')}{% endraw %}"
        return f"Product {% raw %}{product_id}{% endraw %} has {% raw %}{data['stock']}{% endraw %} units in stock at {% raw %}{data['location']}{% endraw %}."
    except ConnectionError:
        logger.error(f"Inventory API failed for product {% raw %}{product_id}{% endraw %}. Providing fallback message.")
        return f"I am unable to check the stock for {% raw %}{product_id}{% endraw %} right now. Please try again later or contact support."
    except Exception as e:
        logger.error(f"Unexpected error getting stock for {% raw %}{product_id}{% endraw %}: {% raw %}{e}{% endraw %}")
        return f"An unexpected issue occurred while checking stock for {% raw %}{product_id}{% endraw %}. Please try again."

tools = [
    Tool(
        name="GetProductStock",
        func=get_product_stock_tool,
        description="Useful for getting the current stock level of a product given its ID. Input should be a product ID (e.g., 'PRODUCT_001')."
    ),
]

# --- Define the LLM (primary and fallback) ---
primary_llm = OpenAI(temperature=0.7) # Assume this is powerful but might fail
fallback_llm = OpenAI(temperature=0.5, model_name="gpt-3.5-turbo-instruct") # A simpler, cheaper fallback

# --- Create the LangChain Agent with Fallback ---
# Using the standard ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")

def create_agent_with_fallback(llm, tools, prompt):
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

primary_agent = create_agent_with_fallback(primary_llm, tools, prompt)
fallback_agent = create_agent_with_fallback(fallback_llm, tools, prompt)

def run_agent_with_llm_fallback(query: str):
    logger.info(f"Attempting to run query with primary LLM: {% raw %}{query}{% endraw %}")
    try:
        result = primary_agent.invoke({"input": query})
        return result["output"]
    except Exception as e:
        logger.warning(f"Primary LLM agent failed: {% raw %}{e}{% endraw %}. Falling back to simpler LLM.")
        try:
            result = fallback_agent.invoke({"input": query})
            return f"Note: Using a simpler model due to primary system issues. Result: {% raw %}{result['output']}{% endraw %}"
        except Exception as fallback_e:
            logger.error(f"Fallback LLM also failed: {% raw %}{fallback_e}{% endraw %}. Returning generic error.")
            # Final fallback: a static message or human hand-off
            return "I am currently experiencing technical difficulties and cannot fulfill your request. Please try again later or contact support."

# Practical Examples
print("\n--- Successful Product Stock Check ---")
print(run_agent_with_llm_fallback("What is the stock level for PRODUCT_001?"))

print("\n--- Product Not Found ---")
print(run_agent_with_llm_fallback("How many units of PRODUCT_999 are available?"))

print("\n--- Simulated Tool Failure ---")
# This will trigger the ConnectionError in get_product_stock_tool
print(run_agent_with_llm_fallback("What is the stock for FAIL_PRODUCT_001?"))

# To test LLM fallback, you would typically need to cause the `primary_llm` itself to fail,
# e.g., by invalidating its API key or causing a network issue.
# For demonstration purposes, let's manually trigger the LLM fallback path:
print("\n--- Simulating Primary LLM Failure ---")
# In a real scenario, this would happen automatically if primary_agent.invoke() raises an error.
# For this demo, let's assume `run_agent_with_llm_fallback` caught an error and
# printed the warning about falling back.
# The previous `FAIL_PRODUCT_001` example already shows a tool fallback inside the agent.
# To demonstrate an LLM fallback, you would need to mock an LLM related error higher up.
# For now, observe how the tool error is handled and propagates gracefully within the agent.

# For further reading on high availability:
# [Link to your blog post on high availability patterns]
```

In this example, the `get_product_stock_tool` directly implements a fallback for API issues. If the primary LLM agent itself fails (e.g., due to an `OutputParserException` or network issue talking to the LLM), the `run_agent_with_llm_fallback` function tries a simpler LLM. This multi-layered approach is key for **high availability patterns**.

### Best Practice 3: Idempotency and Transaction Handling

Imagine you're trying to send money online, but your internet connection blips. You click "send" again. Did the money send once or twice? This is where **idempotency** comes in. An idempotent operation is one that, when performed multiple times, produces the same result as performing it once. This is extremely important for **data consistency** in **mission-critical** systems.

In LangChain, especially when your agents are performing actions (like writing to a database, sending emails, or making purchases via tools), you must ensure these actions don't have unintended side effects if retried.

#### Ensuring Idempotency in LangChain Tool Calls

When a LangChain agent calls an external tool, that tool's operation should ideally be idempotent.

*   **Unique Transaction IDs:** Pass a unique `transaction_id` with every operation. If the operation is retried, the system can check if that `transaction_id` has already been processed.
*   **Database Constraints:** Use unique constraints on database fields. If an agent tries to insert the same record twice, the database will reject the second attempt.
*   **Status Checks:** Before performing an action, check the current status. For example, before archiving a document, check if it's already archived.

**Example: Idempotent Order Placement Tool**

Let's say a LangChain agent can place orders. Without idempotency, a network glitch could cause duplicate orders.

```python
import logging
import uuid
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# --- Simulate an external Order Processing System ---
class MockOrderProcessor:
    def __init__(self):
        self.processed_orders = {} # Stores transaction_id -> order_details

    def place_order(self, order_details: dict, transaction_id: str) -> dict:
        logger.info(f"Received request to place order with transaction_id: {% raw %}{transaction_id}{% endraw %}")
        
        # Simulate a transient network error 20% of the time
        if time.time() % 10 < 2: # Simple way to occasionally trigger
             logger.warning(f"Simulating transient network issue for {% raw %}{transaction_id}{% endraw %}")
             raise ConnectionError("Temporary network issue with order system.")

        if transaction_id in self.processed_orders:
            logger.warning(f"Order with transaction_id {% raw %}{transaction_id}{% endraw %} already processed. Returning existing result (idempotent).")
            return self.processed_orders[transaction_id]

        logger.info(f"Processing new order {% raw %}{transaction_id}{% endraw %}: {% raw %}{order_details}{% endraw %}")
        # Simulate actual processing time
        time.sleep(1)
        
        # Store and return the result
        result = {
            "status": "completed",
            "order_id": f"ORD-{uuid.uuid4().hex[:8]}",
            "details": order_details,
            "transaction_id": transaction_id
        }
        self.processed_orders[transaction_id] = result
        logger.info(f"Order {% raw %}{result['order_id']}{% endraw %} successfully placed for transaction {% raw %}{transaction_id}{% endraw %}.")
        return result

mock_order_processor = MockOrderProcessor()

# --- LangChain Tool for Idempotent Order Placement ---
def place_order_idempotent_tool(product_name: str, quantity: int, customer_id: str, idempotency_key: str) -> str:
    """
    Places an order for a product with a given quantity and customer ID.
    Uses an idempotency_key to prevent duplicate orders on retry.
    """
    order_details = {
        "product_name": product_name,
        "quantity": quantity,
        "customer_id": customer_id
    }
    try:
        response = mock_order_processor.place_order(order_details, idempotency_key)
        return json.dumps(response)
    except ConnectionError:
        logger.error(f"Failed to place order for {% raw %}{idempotency_key}{% endraw %} due to network error.")
        return f"ERROR: Failed to place order due to temporary network issues. Please check order status with key '{% raw %}{idempotency_key}{% endraw %}'."
    except Exception as e:
        logger.critical(f"Critical error placing order for {% raw %}{idempotency_key}{% endraw %}: {% raw %}{e}{% endraw %}", exc_info=True)
        return f"CRITICAL ERROR: An unexpected error occurred while placing your order. Key: '{% raw %}{idempotency_key}{% endraw %}'."

# --- Integrate into a simple LangChain setup (for demonstration) ---
# (Simplified from full agent for focus on the tool itself)
llm_for_order_creation = OpenAI(temperature=0.0)
order_prompt = PromptTemplate(
    input_variables=["product_name", "quantity", "customer_id", "idempotency_key"],
    template="You are an order placement assistant. Use the 'place_order_idempotent_tool' to place an order for {% raw %}{quantity}{% endraw %} units of {% raw %}{product_name}{% endraw %} for customer {% raw %}{customer_id}{% endraw %} using idempotency key {% raw %}{idempotency_key}{% endraw %}."
)

order_placement_chain = LLMChain(llm=llm_for_order_creation, prompt=order_prompt)

# --- Define the tool for LangChain to use ---
order_tools = [
    Tool(
        name="PlaceOrder",
        func=place_order_idempotent_tool,
        description="Places an order. Requires product_name, quantity, customer_id, and an idempotency_key."
    ),
]

# A simple wrapper to simulate an agent calling the tool
def run_order_placement(product_name, quantity, customer_id):
    # The LangChain agent would generate this idempotency key.
    # For a direct tool call, we generate it here.
    idempotency_key = str(uuid.uuid4())
    logger.info(f"Agent generating idempotency key: {% raw %}{idempotency_key}{% endraw %} for order.")
    
    # In a real agent, this would be part of the `agent.invoke` process.
    # Here, we're directly calling the tool's function, demonstrating its idempotent nature.
    return place_order_idempotent_tool(product_name, quantity, customer_id, idempotency_key)

# Practical Examples
print("\n--- First Order Attempt ---")
first_order_result = run_order_placement("Laptop Pro", 1, "CUST-001")
print(f"Result 1: {% raw %}{first_order_result}{% endraw %}")

print("\n--- Retrying the SAME Order (with the same idempotency key, if agent knows to retry) ---")
# To simulate a retry, we need to manually use the same idempotency key from the first attempt.
# In a real agent, the agent's retry logic would pass this key automatically.
idempotency_key_for_retry = json.loads(first_order_result)["transaction_id"]
print(f"Manually retrying with key: {% raw %}{idempotency_key_for_retry}{% endraw %}")
retry_order_result = place_order_idempotent_tool("Laptop Pro", 1, "CUST-001", idempotency_key_for_retry)
print(f"Result 2 (retry): {% raw %}{retry_order_result}{% endraw %}")

print("\n--- Another NEW Order ---")
print(run_order_placement("Mouse Wireless", 2, "CUST-002"))

# Simulate a transient failure and retry (showing idempotency on retry)
print("\n--- Order with Simulated Transient Failure and Idempotent Retry ---")
temp_idempotency_key = str(uuid.uuid4())
try:
    # This call might fail with ConnectionError
    place_order_idempotent_tool("Keyboard Mechanical", 1, "CUST-003", temp_idempotency_key)
except ConnectionError:
    logger.info(f"Caught ConnectionError for {% raw %}{temp_idempotency_key}{% endraw %}. Retrying...")
    # The next call with the same key should succeed and be unique
    retry_result = place_order_idempotent_tool("Keyboard Mechanical", 1, "CUST-003", temp_idempotency_key)
    print(f"Retry successful: {% raw %}{retry_result}{% endraw %}")

# Further reading on transaction handling:
# [Link to your blog post on distributed transaction patterns]
```

The `MockOrderProcessor` ensures that if `place_order` is called multiple times with the same `transaction_id` (acting as an idempotency key), the order is only processed once. This is fundamental for **transaction handling** and preserving **data consistency**.

### Best Practice 4: Retry Mechanisms with Exponential Backoff

Not all errors are permanent. Many are transient, meaning they are temporary and might resolve themselves if you just try again. These include network glitches, temporary service overloads, or database deadlocks. However, simply retrying immediately and repeatedly is a bad idea. It can make things worse, overwhelming the service that's already struggling.

This is where **retry mechanisms with exponential backoff** come in. This strategy means:

1.  **Retry after a delay:** Don't try again immediately.
2.  **Increase delay exponentially:** If the first retry fails, wait longer for the second, even longer for the third, and so on. (e.g., 1 second, then 2 seconds, then 4 seconds, then 8 seconds).
3.  **Add Jitter:** Randomize the delay slightly to prevent all retrying services from hitting at the exact same moment. This avoids a "thundering herd" problem.
4.  **Set a maximum number of retries:** Eventually, give up if it keeps failing.

This strategy is a cornerstone of robust **enterprise error strategies**.

**Example: Retrying an External API Call from a LangChain Agent**

Python libraries like `tenacity` make implementing exponential backoff very easy.

```python
import logging
import random
import time
from tenacity import retry, stop_after_attempt, wait_exponential, before_log, after_log, RetryError
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# --- Simulate an unreliable external service (e.g., an LLM API) ---
class UnreliableLLMService:
    def __init__(self, failure_rate=0.4): # 40% chance of failure
        self.failure_rate = failure_rate
        self.call_count = 0

    def generate_text(self, prompt_text: str) -> str:
        self.call_count += 1
        logger.info(f"Attempt {% raw %}{self.call_count}{% endraw %}: Calling external LLM service for prompt '{% raw %}{prompt_text[:50]}{% endraw %}...'")
        
        if random.random() < self.failure_rate:
            logger.warning(f"Attempt {% raw %}{self.call_count}{% endraw %}: Simulated transient error from LLM service!")
            raise ConnectionError("LLM API temporarily unavailable or timed out.")
        
        logger.info(f"Attempt {% raw %}{self.call_count}{% endraw %}: LLM service call successful.")
        return f"Generated text for: '{% raw %}{prompt_text}{% endraw %}' successfully."

unreliable_llm_service = UnreliableLLMService()

# --- LangChain integration with Tenacity for retries ---
@retry(
    stop=stop_after_attempt(5), # Try a maximum of 5 times
    wait=wait_exponential(multiplier=1, min=2, max=10), # Start with 2s, max 10s wait, exponential growth
    retry_error_cls=ConnectionError, # Only retry on ConnectionError (or similar transient errors)
    before=before_log(logger, logging.INFO), # Log before each attempt
    after=after_log(logger, logging.INFO), # Log after each attempt
    reraise=True # Re-raise the exception if all retries fail
)
def reliable_llm_call_with_retry(prompt_text: str) -> str:
    """
    Attempts to call the unreliable LLM service with retries and exponential backoff.
    """
    return unreliable_llm_service.generate_text(prompt_text)

# --- Full LangChain chain using the reliable LLM call ---
class CustomReliableLLM(OpenAI): # Inherit to override _call method
    def _call(self, prompt: str, stop=None, run_manager=None, **kwargs) -> str:
        # LangChain's internal _call method is what ultimately talks to the LLM.
        # We wrap our retry logic here.
        try:
            return reliable_llm_call_with_retry(prompt)
        except RetryError as e:
            # If all retries failed, tenacity will re-raise the last exception.
            logger.critical(f"All retries failed for LLM call: {% raw %}{e}{% endraw %}. Returning fallback message.")
            raise ConnectionError(f"LLM service permanently unavailable after multiple retries. Original error: {% raw %}{e}{% endraw %}")

# Use our custom LLM that incorporates the retry logic
llm_with_retry = CustomReliableLLM(temperature=0.0)
prompt_template = PromptTemplate(input_variables=["topic"], template="Write a short paragraph about {topic}.")
chain_with_retry = LLMChain(llm=llm_with_retry, prompt=prompt_template)

# Practical Examples
print("\n--- Attempting a query that might need retries ---")
try:
    result = chain_with_retry.run("cloud computing")
    print(f"Final Result: {result}")
except ConnectionError as e:
    print(f"Failed after all retries: {e}")

print("\n--- Another attempt ---")
try:
    result = chain_with_retry.run("distributed databases")
    print(f"Final Result: {result}")
except ConnectionError as e:
    print(f"Failed after all retries: {e}")

# To really see the retry in action, increase `unreliable_llm_service.failure_rate` or
# just run it multiple times.
unreliable_llm_service.failure_rate = 0.8 # Make it more likely to fail
print("\n--- Attempting a query with higher failure rate ---")
try:
    result = chain_with_retry.run("quantum mechanics")
    print(f"Final Result: {result}")
except ConnectionError as e:
    print(f"Failed after all retries: {e}")
```

Here, the `reliable_llm_call_with_retry` function, decorated with `@retry`, automatically handles retries with exponential backoff for `ConnectionError`. This pattern significantly improves the reliability of your LangChain application when interacting with potentially flaky external services.

### Best Practice 5: Circuit Breakers to Prevent Cascading Failures

Think of an electrical circuit breaker in your house. If an appliance tries to draw too much power, the breaker "trips." It doesn't just keep trying to send power, which could damage the appliance or cause a fire. Instead, it stops the flow of power to protect the system.

A **circuit breaker pattern** in software works similarly. If a service (like an external API that your LangChain agent uses) starts to consistently fail or respond slowly, the circuit breaker "trips." This means your LangChain application will immediately stop trying to call that failing service. Instead, it will immediately return an error or a fallback.

This prevents your application from:

*   **Hammering a struggling service:** Giving it time to recover.
*   **Waiting for timeouts:** Your application won't waste time waiting for a response that will never come.
*   **Cascading failures:** If one service fails, it doesn't cause your LangChain application (and other services that depend on it) to also fail.

This is a crucial pattern for **high availability patterns** and **enterprise monitoring**. Libraries like `pybreaker` or even `tenacity` (with some configuration) can help implement this.

**Example: LangChain Agent with a Circuit Breaker for an External Tool**

Let's use a `pybreaker` circuit breaker to protect our LangChain agent from a consistently failing `Payment Gateway` tool.

```python
import logging
import random
import time
from pybreaker import CircuitBreaker, CircuitBreakerError
from langchain_community.llms import OpenAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain.prompts import PromptTemplate
from langchain import hub

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# --- Simulate an unreliable Payment Gateway API ---
class MockPaymentGateway:
    def __init__(self, failure_rate=0.6): # 60% chance of failure initially
        self.failure_rate = failure_rate
        self.call_count = 0

    def process_payment(self, amount: float, customer_id: str) -> dict:
        self.call_count += 1
        logger.info(f"Payment attempt {% raw %}{self.call_count}{% endraw %}: Processing payment for customer {% raw %}{customer_id}{% endraw %}, amount {% raw %}{amount}{% endraw %}")
        
        if random.random() < self.failure_rate:
            logger.error(f"Payment attempt {% raw %}{self.call_count}{% endraw %}: Simulated payment gateway failure!")
            # Simulate different types of errors
            if random.random() < 0.5:
                raise ConnectionError("Payment Gateway is unreachable.")
            else:
                raise ValueError("Payment Gateway returned invalid response.")
        
        logger.info(f"Payment attempt {% raw %}{self.call_count}{% endraw %}: Payment successful.")
        return {"status": "success", "transaction_id": f"PAY-{random.randint(1000, 9999)}", "amount": amount}

mock_payment_gateway = MockPaymentGateway()

# --- Configure the Circuit Breaker ---
# The circuit breaker will transition:
# - from CLOSED to OPEN after 3 consecutive failures.
# - stay OPEN for 10 seconds.
# - transition from OPEN to HALF-OPEN after 10 seconds.
# - if a call succeeds in HALF-OPEN, it goes back to CLOSED.
# - if a call fails in HALF-OPEN, it goes back to OPEN.
payment_breaker = CircuitBreaker(
    fail_max=3,
    reset_timeout=10, # seconds
    exclude=[TypeError], # Don't trip on TypeErrors, only specific gateway errors
    listeners=[] # Can add listeners for state changes
)

# --- Define the LangChain Tool, protected by the Circuit Breaker ---
@payment_breaker
def process_payment_tool(amount: float, customer_id: str) -> str:
    """Processes a payment using the external payment gateway."""
    try:
        response = mock_payment_gateway.process_payment(amount, customer_id)
        return json.dumps(response)
    except (ConnectionError, ValueError) as e:
        # These are the errors that `pybreaker` will count as failures
        logger.error(f"Payment processing failed: {% raw %}{e}{% endraw %}")
        raise # Re-raise for the circuit breaker to count it
    except Exception as e:
        logger.critical(f"An unexpected error occurred in payment tool: {e}")
        raise # Re-raise for general error handling

tools = [
    Tool(
        name="ProcessPayment",
        func=process_payment_tool,
        description="Processes a payment. Requires amount (float) and customer_id (str)."
    ),
]

# --- Create the LangChain Agent ---
llm = OpenAI(temperature=0.0)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Function to run the agent and handle circuit breaker errors
def run_payment_agent(query: str):
    logger.info(f"\n--- Running agent for query: '{query}' ---")
    try:
        response = agent_executor.invoke({"input": query})
        print(f"Agent Output: {% raw %}{response['output']}{% endraw %}")
    except CircuitBreakerError:
        logger.error("Circuit breaker is OPEN! Payment gateway is currently unavailable. Please try again later.")
        print("Agent Output: I am sorry, the payment system is temporarily offline. Please try again in a few moments.")
    except Exception as e:
        logger.critical(f"An unexpected error occurred during agent execution: {e}")
        print(f"Agent Output: An internal system error occurred. Please contact support. Error: {% raw %}{e}{% endraw %}")

# Practical Examples
print("--- Initial attempts (likely to fail and trip the breaker) ---")
for i in range(5): # Make a few calls to trip the breaker
    run_payment_agent(f"Process a payment of 100.00 for customer CUST-ABC-00{% raw %}{i}{% endraw %}.")
    time.sleep(1) # Small delay between attempts

print(f"\nCircuit Breaker State: {payment_breaker.current_state}")

print("\n--- After breaker is tripped, further calls should fail immediately ---")
run_payment_agent("Process a payment of 50.00 for customer CUST-DEF.")
run_payment_agent("Process a payment of 75.00 for customer CUST-GHI.")

print(f"\nCircuit Breaker State: {payment_breaker.current_state}")

print("\n--- Waiting for breaker to reset (10 seconds) ---")
time.sleep(10) # Wait for the reset_timeout
print(f"Circuit Breaker State after waiting: {payment_breaker.current_state} (should be HALF-OPEN)")

print("\n--- First call after reset (Half-Open state) ---")
# This call determines if the breaker closes or re-opens
run_payment_agent("Process a test payment of 25.00 for customer CUST-JMK.")
print(f"Circuit Breaker State after Half-Open attempt: {payment_breaker.current_state}")

# To demonstrate closing the breaker, you might need to temporarily reduce the `mock_payment_gateway.failure_rate`
# or run this section multiple times until a successful call happens in HALF-OPEN.
mock_payment_gateway.failure_rate = 0.1 # Make it more reliable for the next attempts

print("\n--- More attempts (should eventually close the breaker if successful) ---")
for i in range(3):
    run_payment_agent(f"Process a small payment for CUST-ZXY-{% raw %}{i}{% endraw %}.")
    time.sleep(1)
print(f"Circuit Breaker State: {payment_breaker.current_state}")

# For more on high availability:
# [Link to your blog post on building resilient microservices]
```

This example shows how `pybreaker` steps in. After a few failures, the circuit breaker opens, and subsequent calls to `process_payment_tool` immediately fail with `CircuitBreakerError` without even trying the actual payment gateway. After the `reset_timeout`, it goes to `HALF-OPEN` to test the service. If it succeeds, it closes; if it fails, it re-opens. This crucial pattern helps manage **enterprise monitoring** and prevents system overload.

### Best Practice 6: Error Escalation and Alerting

Knowing an error occurred is good, but knowing *who* needs to know, *when*, and *how* is even better. **Error escalation procedures** are formal steps defining how critical issues are communicated and resolved. For **mission-critical** LangChain systems, you need a clear system for **enterprise monitoring**.

Different error severities require different responses:

*   **DEBUG/INFO:** Routine messages, typically only seen by developers during debugging.
*   **WARNING:** Something unusual happened, but the system can still proceed. Might indicate a potential future problem.
*   **ERROR:** A problem occurred that prevented a specific operation from completing. Requires investigation.
*   **CRITICAL:** A severe failure that impacts core functionality or system stability. Needs immediate attention.

#### Alerting Tools and Channels

*   **Logging Platforms:** Centralized logging (ELK stack, Splunk, DataDog) for general error visibility.
*   **Messaging Platforms:** Slack, Microsoft Teams for less urgent notifications.
*   **On-Call Systems:** PagerDuty, Opsgenie for immediate alerts to on-call engineers (for CRITICAL errors).
*   **Email:** For reports or less time-sensitive alerts.
*   **Dashboards:** Grafana, Prometheus dashboards for real-time visualization of error rates and system health.

**Example: Defining Error Escalation for a LangChain-powered Financial Advisor Bot**

Imagine a LangChain bot that gives financial advice. Errors here could be very sensitive due to **compliance requirements**.

```python
import logging
import os # For simulated environment variables
import smtplib # For simulating email
from email.mime.text import MIMEText
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Simulate external alerting systems
class AlertingService:
    def send_slack_message(self, message: str, channel: str = "#alerts-dev"):
        logger.info(f"SLACK ALERT sent to {channel}: {message}")
        # In real code, use Slack API client
        # slack_client.chat_postMessage(channel=channel, text=message)

    def trigger_pagerduty_alert(self, incident_key: str, summary: str, severity: str = "critical"):
        logger.warning(f"PAGERDUTY ALERT triggered: Severity={severity}, Key={incident_key}, Summary='{summary}'")
        # In real code, use PagerDuty API client

    def send_email(self, subject: str, body: str, recipient: str):
        logger.info(f"EMAIL ALERT sent to {recipient}: Subject='{subject}'")
        # In real code, configure SMTP properly
        # msg = MIMEText(body)
        # msg['Subject'] = subject
        # msg['From'] = "alerts@yourcompany.com"
        # msg['To'] = recipient
        # with smtplib.SMTP("smtp.yourcompany.com") as server:
        #     server.send_message(msg)

alert_service = AlertingService()

# --- Define Error Escalation Procedure ---
def handle_langchain_error(error_type: str, message: str, transaction_id: str, severity: str = "error"):
    timestamp = datetime.now().isoformat()
    log_entry_message = f"[{% raw %}{severity.upper()}{% endraw %}] LangChain Error: {% raw %}{error_type}{% endraw %} - {% raw %}{message}{% endraw %} (Transaction ID: {% raw %}{transaction_id}{% endraw %})"
    
    # Log the error regardless of severity
    if severity == "debug":
        logger.debug(log_entry_message)
    elif severity == "info":
        logger.info(log_entry_message)
    elif severity == "warning":
        logger.warning(log_entry_message)
    elif severity == "error":
        logger.error(log_entry_message, extra={"error_type": error_type, "transaction_id": transaction_id})
    elif severity == "critical":
        logger.critical(log_entry_message, extra={"error_type": error_type, "transaction_id": transaction_id})
    else:
        logger.error(f"Unknown severity '{severity}' for error: {log_entry_message}")
        severity = "error" # Default to error for unknown

    # Escalation logic based on severity
    if severity == "warning":
        alert_service.send_slack_message(f"WARN: LangChain issue: {message}", channel="#langchain-warnings")
    elif severity == "error":
        alert_service.send_slack_message(f"ERROR: LangChain operational error: {message}", channel="#langchain-errors")
        alert_service.send_email(
            subject=f"[LangChain Error] {error_type} - {transaction_id}",
            body=f"Details: {message}\nTimestamp: {timestamp}\nTxn ID: {transaction_id}",
            recipient="devops-team@yourcompany.com"
        )
    elif severity == "critical":
        alert_service.trigger_pagerduty_alert(
            incident_key=f"langchain-critical-{transaction_id}",
            summary=f"CRITICAL LangChain failure: {error_type} - {message}",
            severity="critical"
        )
        alert_service.send_email(
            subject=f"[CRITICAL LangChain] {error_type} - {transaction_id}",
            body=f"IMMEDIATE ACTION REQUIRED. Details: {message}\nTimestamp: {timestamp}\nTxn ID: {transaction_id}",
            recipient="oncall-engineers@yourcompany.com"
        )
        alert_service.send_slack_message(f"<!channel> CRITICAL: LangChain system failure: {message}", channel="#incidents")
    
    # After escalation, you might also update a central monitoring dashboard
    # monitor_client.increment_error_counter(error_type, severity)


# Example usage in a LangChain context:
def simulate_financial_advice_bot(query: str, client_id: str):
    transaction_id = f"FIN-TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{client_id}"
    try:
        # Simulate an LLM call or tool usage
        if "invalid stock query" in query.lower():
            raise ValueError("Invalid stock symbol detected.")
        if "api timeout" in query.lower():
            raise ConnectionError("External Stock API timed out.")
        if "critical system crash" in query.lower():
            # Simulate a very serious internal component failure
            raise RuntimeError("Core financial calculation module crashed.")
        
        # Simulate successful processing
        logger.info(f"Successfully processed financial query for {client_id}.", extra={"transaction_id": transaction_id})
        return f"Advice for '{query}': The market is looking good for you."
    except ValueError as e:
        handle_langchain_error("InputValidationError", f"User input parsing failed: {e}", transaction_id, "error")
        return "I couldn't understand your request due to an invalid input. Please rephrase."
    except ConnectionError as e:
        handle_langchain_error("ExternalAPIFailure", f"Failed to connect to external data source: {e}", transaction_id, "error")
        return "I'm having trouble accessing real-time data. Please try again later."
    except RuntimeError as e:
        handle_langchain_error("SystemComponentCrash", f"Core system module failed: {e}", transaction_id, "critical")
        return "Our system is experiencing a critical issue. Please contact support immediately."
    except Exception as e:
        # Catch any other unforeseen errors as critical
        handle_langchain_error("UnhandledException", f"An unexpected error occurred: {e}", transaction_id, "critical")
        return "An unexpected and severe error occurred. Our team has been notified."

# Practical Examples
simulate_financial_advice_bot("What is the current price of AAPL?", "CLIENT-001")
simulate_financial_advice_bot("Show me a report for invalid stock query.", "CLIENT-002")
simulate_financial_advice_bot("Analyze my portfolio but the API timeout.", "CLIENT-003")
simulate_financial_advice_bot("Help me with my retirement planning but critical system crash.", "CLIENT-004")

# For more on compliance:
# [Link to your blog post on compliance requirements for AI systems]
```

This setup ensures that errors are not just logged but also acted upon based on their severity. Minor issues might just send a Slack notification, while critical ones trigger a PagerDuty alert and an email to the on-call team. This structured approach is vital for meeting **compliance requirements** and ensuring swift recovery.

### Best Practice 7: Implementing Compensating Transactions (Advanced)

Sometimes, simply retrying an operation or providing a fallback isn't enough. In complex, multi-step operations performed by LangChain agents, one step might succeed while a later one fails. If you can't retry the failed step (e.g., it's a permanent error), you might need to *undo* the previous successful steps. This is known as a **compensating transaction**.

Imagine a LangChain agent that:
1.  Reserves a product in inventory.
2.  Processes a payment.
3.  Creates a shipping label.

If step 1 and 2 succeed, but step 3 fails permanently (e.g., invalid address), you can't just leave the product reserved and the payment processed. You need to:
*   Un-reserve the product.
*   Refund the payment.

This ensures **data consistency** across your systems and is a more advanced form of **transaction handling**. It's often associated with the Saga pattern in microservices architecture.

**Example: LangChain Order Processing with Compensation**

Let's adapt our order placement example. Now, if shipping fails, we need to compensate.

```python
import logging
import uuid
import time
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# --- Simulate external services with compensation actions ---
class MockInventoryService:
    def __init__(self):
        self.reserved_items = {} # order_id -> product_id, quantity

    def reserve_product(self, product_id: str, quantity: int, order_id: str) -> bool:
        logger.info(f"Inventory: Attempting to reserve {quantity} of {product_id} for order {order_id}.")
        if product_id == "OUT_OF_STOCK":
            logger.warning("Inventory: Product OUT_OF_STOCK. Cannot reserve.")
            return False
        # Simulate reservation
        self.reserved_items[order_id] = {"product_id": product_id, "quantity": quantity}
        logger.info(f"Inventory: {quantity} of {product_id} reserved for order {order_id}.")
        return True

    def unreserve_product(self, order_id: str) -> bool:
        if order_id in self.reserved_items:
            product_id = self.reserved_items[order_id]["product_id"]
            quantity = self.reserved_items[order_id]["quantity"]
            del self.reserved_items[order_id]
            logger.info(f"Inventory: {quantity} of {product_id} unreserved for order {order_id} (compensation).")
            return True
        logger.warning(f"Inventory: No reservation found for order {order_id} to unreserve.")
        return False

class MockPaymentGateway:
    def __init__(self):
        self.processed_payments = {} # order_id -> amount

    def process_payment(self, amount: float, customer_id: str, order_id: str) -> bool:
        logger.info(f"Payment: Attempting to process {amount} for customer {customer_id}, order {order_id}.")
        if amount > 1000: # Simulate a payment failure condition
            logger.error("Payment: Payment amount too high. Transaction declined.")
            return False
        # Simulate payment processing
        self.processed_payments[order_id] = amount
        logger.info(f"Payment: {amount} processed for order {order_id}.")
        return True

    def refund_payment(self, order_id: str) -> bool:
        if order_id in self.processed_payments:
            amount = self.processed_payments[order_id]
            del self.processed_payments[order_id]
            logger.info(f"Payment: {amount} refunded for order {order_id} (compensation).")
            return True
        logger.warning(f"Payment: No payment found for order {order_id} to refund.")
        return False

class MockShippingService:
    def __init__(self):
        self.shipped_orders = {}

    def create_shipping_label(self, order_id: str, address: str) -> bool:
        logger.info(f"Shipping: Attempting to create label for order {order_id} to {address}.")
        if "INVALID_ADDRESS" in address.upper():
            logger.error("Shipping: Invalid address detected. Cannot create label.")
            raise ValueError("Invalid shipping address.")
        # Simulate label creation
        self.shipped_orders[order_id] = address
        logger.info(f"Shipping: Label created for order {order_id}.")
        return True
    
    def cancel_shipping_label(self, order_id: str) -> bool:
        if order_id in self.shipped_orders:
            address = self.shipped_orders[order_id]
            del self.shipped_orders[order_id]
            logger.info(f"Shipping: Label cancelled for order {order_id} to {address} (compensation).")
            return True
        logger.warning(f"Shipping: No label found for order {order_id} to cancel.")
        return False


inventory_service = MockInventoryService()
payment_gateway = MockPaymentGateway()
shipping_service = MockShippingService()

# --- LangChain Agent simulating multi-step order processing ---
def process_full_order_with_compensation(product_id: str, quantity: int, customer_id: str, amount: float, shipping_address: str) -> str:
    order_id = f"ORDER-{uuid.uuid4().hex[:8]}"
    logger.info(f"Starting full order process for {order_id}...")
    
    steps_completed = []

    try:
        # Step 1: Reserve Product
        if not inventory_service.reserve_product(product_id, quantity, order_id):
            return f"Order {order_id} failed: Product {product_id} could not be reserved."
        steps_completed.append("inventory_reserved")
        
        # Step 2: Process Payment
        if not payment_gateway.process_payment(amount, customer_id, order_id):
            return f"Order {order_id} failed: Payment could not be processed."
        steps_completed.append("payment_processed")

        # Step 3: Create Shipping Label
        shipping_service.create_shipping_label(order_id, shipping_address)
        steps_completed.append("shipping_label_created")

        logger.info(f"Order {order_id} fully processed successfully!")
        return f"Order {order_id} for {product_id} (x{quantity}) placed successfully. Payment {amount} processed. Shipping to {shipping_address}."

    except (ValueError, RuntimeError) as e:
        logger.error(f"Order {order_id} failed at shipping step due to permanent error: {e}. Initiating compensation.")
        return f"Order {order_id} failed during shipping: {e}. Initiating compensation."
    except Exception as e:
        logger.critical(f"Order {order_id} failed due to unexpected error: {e}. Initiating compensation.", exc_info=True)
        return f"Order {order_id} failed due to an unexpected error. Initiating compensation."
    finally:
        # Compensation logic
        if "shipping_label_created" in steps_completed:
            # If shipping succeeded but something else failed later (not in this simple example, but for completeness)
            shipping_service.cancel_shipping_label(order_id)
        if "payment_processed" in steps_completed:
            # Always refund if payment was processed but order couldn't complete
            payment_gateway.refund_payment(order_id)
        if "inventory_reserved" in steps_completed:
            # Always unreserve if inventory was reserved but order couldn't complete
            inventory_service.unreserve_product(order_id)
        
        if "shipping_label_created" not in steps_completed and "payment_processed" in steps_completed:
            logger.info(f"Compensation complete for order {order_id}. State rolled back.")
        elif "payment_processed" not in steps_completed and "inventory_reserved" in steps_completed:
            logger.info(f"Compensation complete for order {order_id}. State rolled back.")
        elif not steps_completed:
             logger.info(f"No compensation needed for order {order_id} as no steps completed.")


# Practical Examples
print("\n--- Successful Order ---")
print(process_full_order_with_compensation("PROD_A", 2, "CUST-001", 50.00, "123 Main St"))

print("\n--- Order Failing at Inventory Step ---")
print(process_full_order_with_compensation("OUT_OF_STOCK", 1, "CUST-002", 20.00, "456 Oak Ave"))

print("\n--- Order Failing at Payment Step ---")
print(process_full_order_with_compensation("PROD_B", 1, "CUST-003", 1500.00, "789 Pine Rd")) # Amount too high

print("\n--- Order Failing at Shipping Step (Compensation Triggered) ---")
# This will complete inventory and payment, then fail at shipping, triggering refunds and unreservation
print(process_full_order_with_compensation("PROD_C", 3, "CUST-004", 75.00, "INVALID_ADDRESS"))

# For more on distributed transactions:
# [Link to your blog post on Saga pattern and distributed transactions]
```

In this example, the `finally` block acts as our compensation mechanism. If any step fails after `inventory_reserved` or `payment_processed`, the system attempts to unreserve the product and refund the payment. This pattern ensures **data consistency** and is critical for **transaction handling** in complex enterprise workflows.

### Best Practice 8: Disaster Recovery and Business Continuity Planning

What happens if an entire data center goes offline? Or a critical cloud service provider experiences a widespread outage? These are extreme but possible scenarios. **Disaster recovery planning** and **business continuity** are about preparing for the worst-case scenarios to minimize downtime and data loss for your **mission-critical** LangChain systems. This directly impacts your ability to meet **SLA compliance**.

Key aspects include:

*   **Backup Strategies:** Regularly back up all critical data, including:
    *   Vector stores (embeddings, indexed documents).
    *   Chat histories and conversation logs.
    *   Configuration files for LangChain agents and tools.
    *   Any external databases used by your LangChain applications.
*   **Geographic Redundancy:** Deploy your LangChain infrastructure across multiple regions or availability zones. If one region fails, traffic can be rerouted to another.
*   **Recovery Point Objective (RPO) and Recovery Time Objective (RTO):**
    *   **RPO:** How much data loss can you tolerate? (e.g., last 15 minutes of data).
    *   **RTO:** How quickly must the system be back online? (e.g., within 4 hours).
    *   These objectives define your DR strategy.
*   **Regular Testing:** You can't just have a plan; you must test it regularly. Perform disaster recovery drills to ensure your team knows how to react and your systems can indeed recover.

**Example: Planning for LangChain Vector Store Disaster Recovery**

A vector store (like FAISS, Chroma, Pinecone, Weaviate) is often the brain of a LangChain application, holding all its knowledge. Losing it is catastrophic.

```python
import logging
import os
import shutil
from datetime import datetime
import time

# Simulate a vector store library (e.g., FAISS)
class MockVectorStore:
    def __init__(self, name="default_vector_store", data={}):
        self.name = name
        self.data = data # Simple dict for demonstration
        self.last_update = datetime.now()
        logger.info(f"MockVectorStore '{self.name}' initialized.")

    def add_documents(self, docs: dict):
        self.data.update(docs)
        self.last_update = datetime.now()
        logger.info(f"MockVectorStore '{self.name}': Added {len(docs)} documents.")

    def query(self, text: str) -> str:
        # Simulate a query
        if not self.data:
            return "No documents in vector store."
        for key, value in self.data.items():
            if text in value:
                return f"Found '{value}' related to '{text}'."
        return "No relevant information found."
    
    def save_to_disk(self, path: str):
        # Simulate saving to a file
        filepath = os.path.join(path, f"{self.name}.json")
        with open(filepath, 'w') as f:
            json.dump({"data": self.data, "last_update": self.last_update.isoformat()}, f)
        logger.info(f"MockVectorStore '{self.name}' saved to {filepath}.")

    @classmethod
    def load_from_disk(cls, name: str, path: str):
        filepath = os.path.join(path, f"{name}.json")
        if not os.path.exists(filepath):
            logger.error(f"Failed to load '{name}': File not found at {filepath}")
            return None
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)
        instance = cls(name=name, data=loaded_data["data"])
        instance.last_update = datetime.fromisoformat(loaded_data["last_update"])
        logger.info(f"MockVectorStore '{name}' loaded from {filepath}.")
        return instance

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# --- Disaster Recovery Functions ---
BACKUP_DIR = "vector_store_backups"
PRIMARY_STORE_NAME = "enterprise_knowledge_base"
REPLICA_STORE_NAME = "dr_knowledge_base_replica"

def create_backup(vector_store: MockVectorStore):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{vector_store.name}_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)
    vector_store.save_to_disk(backup_path)
    logger.info(f"Full backup of '{vector_store.name}' created at {backup_path}")
    return backup_path

def restore_from_backup(store_name: str) -> MockVectorStore:
    # Find the latest backup
    backups = [d for d in os.listdir(BACKUP_DIR) if os.path.isdir(os.path.join(BACKUP_DIR, d)) and d.startswith(store_name)]
    if not backups:
        logger.error(f"No backups found for '{store_name}'. Cannot restore.")
        return None
    latest_backup_dir = sorted(backups, reverse=True)[0] # Get the latest by timestamp
    latest_backup_path = os.path.join(BACKUP_DIR, latest_backup_dir)
    
    logger.info(f"Attempting to restore '{store_name}' from latest backup: {latest_backup_path}")
    restored_store = MockVectorStore.load_from_disk(store_name, latest_backup_path)
    return restored_store

def sync_to_dr_replica(primary_store: MockVectorStore, replica_store: MockVectorStore):
    # In a real system, this would be a continuous replication process.
    # Here, we simulate by overwriting the replica's data with primary's.
    replica_store.data = primary_store.data.copy()
    replica_store.last_update = primary_store.last_update
    logger.info(f"Data from '{primary_store.name}' synced to '{replica_store.name}' (DR replica).")

# --- Main simulation ---
if __name__ == "__main__":
    # Clean up previous backups for a fresh run
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)

    # 1. Initialize primary vector store
    primary_vector_store = MockVectorStore(name=PRIMARY_STORE_NAME)
    primary_vector_store.add_documents({"doc1": "LangChain for enterprise solutions", "doc2": "Error handling best practices"})
    logger.info(f"Primary store query: {primary_vector_store.query('enterprise solutions')}")

    # 2. Create a backup
    backup_path = create_backup(primary_vector_store)
    
    # 3. Simulate updates to the primary store
    time.sleep(1) # Simulate time passing
    primary_vector_store.add_documents({"doc3": "High availability patterns for AI"})
    logger.info(f"Primary store query after update: {primary_vector_store.query('high availability')}")

    # 4. Initialize DR replica (could be in another region)
    dr_replica_vector_store = MockVectorStore(name=REPLICA_STORE_NAME)
    sync_to_dr_replica(primary_vector_store, dr_replica_vector_store)
    logger.info(f"DR replica query: {dr_replica_vector_store.query('error handling')}")

    # 5. Simulate a disaster: Primary store becomes corrupt/unavailable
    logger.critical("\n--- SIMULATING DISASTER: Primary vector store corrupted/lost! ---")
    del primary_vector_store # Simulate loss of the primary instance
    primary_vector_store = None

    # 6. Attempt recovery from DR replica or backup
    logger.info("Attempting to failover to DR replica...")
    if dr_replica_vector_store and dr_replica_vector_store.data:
        # Check if replica is up-to-date enough (RPO check)
        logger.info(f"Successfully failed over to DR replica. Query: {dr_replica_vector_store.query('AI patterns')}")
        # Now promote the replica to be the new primary
        new_primary_store = dr_replica_vector_store
    else:
        logger.warning("DR replica is not available or empty. Attempting restore from backup.")
        new_primary_store = restore_from_backup(PRIMARY_STORE_NAME)
        if new_primary_store:
            logger.info(f"Successfully restored from backup. Query: {new_primary_store.query('enterprise solutions')}")
        else:
            logger.critical("Failed to recover from both replica and backup. Major data loss/downtime.")

    # 7. Resume operations with the recovered store
    if new_primary_store:
        logger.info("\n--- Operations resumed with recovered store ---")
        new_primary_store.add_documents({"doc4": "Post-disaster recovery steps"})
        logger.info(f"New primary store query: {new_primary_store.query('recovery steps')}")

    # Clean up backups
    # shutil.rmtree(BACKUP_DIR)

# For a deep dive into business continuity:
# [Link to your blog post on building a business continuity plan]
```

This example shows a basic **disaster recovery planning** strategy for a vector store. You create backups and maintain a replica. If the primary store fails, you first attempt to use the replica (for faster RTO) or fall back to restoring from the latest backup (to meet RPO). This multi-layered approach is critical for **business continuity** and meeting strict **SLA compliance**.

### Tools and Libraries for Enterprise Error Handling

Implementing these best practices isn't something you have to do from scratch. Many powerful Python libraries and services can help your **enterprise LangChain error handling** efforts:

*   **`tenacity`:** Excellent for implementing robust retry logic with exponential backoff and jitter. (Used in Best Practice 4).
*   **`pybreaker`:** A solid library for implementing the circuit breaker pattern. (Used in Best Practice 5).
*   **`logging` (Python's built-in):** Fundamental for comprehensive and structured logging. Combine with `structlog` for even better structured logs. (Used in Best Practice 1).
*   **Monitoring Systems:**
    *   **Prometheus & Grafana:** For collecting metrics (error rates, latency) and creating real-time dashboards for **enterprise monitoring**.
    *   **ELK Stack (Elasticsearch, Logstash, Kibana):** For centralized log aggregation, searching, and visualization.
    *   **DataDog, Splunk, New Relic:** Commercial solutions offering comprehensive monitoring, alerting, and tracing capabilities.
*   **Alerting Tools:**
    *   **PagerDuty, Opsgenie:** For managing on-call rotations and critical incident alerting.
    *   **Slack, Microsoft Teams:** For less urgent notifications and team communication.
*   **Cloud Provider Services:** Many cloud providers (AWS, Azure, GCP) offer managed services for logging, monitoring, and database replication, which are essential for **disaster recovery planning** and **high availability patterns**.

### Testing Your Error Handling Strategies

Implementing these strategies is only half the battle. You need to verify that they actually work! Testing error handling is often overlooked but is paramount for **mission-critical** systems.

*   **Unit Tests:** Test individual components (like your `get_product_stock_tool` or `reliable_llm_call_with_retry`) by mocking failures (e.g., raise a `ConnectionError` when a simulated API is called).
*   **Integration Tests:** Test how different parts of your LangChain application interact when errors occur. For example, does your agent correctly fall back when a tool fails?
*   **End-to-End Tests:** Simulate entire user journeys where failures are injected at various points.
*   **Chaos Engineering (Advanced):** Intentionally inject failures into a production or staging environment to see how the system reacts. Tools like Chaos Monkey can help. This helps uncover weaknesses in your **business continuity** plans that manual testing might miss.

By regularly testing your error handling, you gain confidence that your **enterprise LangChain error handling** will perform as expected when a real incident occurs.

### Conclusion

Building **mission-critical** applications with LangChain requires more than just clever prompts and powerful tools. It demands a robust approach to **enterprise LangChain error handling**. By embracing best practices like comprehensive logging, graceful degradation, idempotency, retries with exponential backoff, circuit breakers, clear escalation procedures, compensating transactions, and thorough **disaster recovery planning**, you can transform your LangChain applications from fragile experiments into resilient, dependable workhorses.

You have the power to build systems that not only perform brilliantly but also gracefully withstand the inevitable bumps in the road. Start implementing these strategies today to ensure your **enterprise LangChain** solutions are ready for anything the real world throws at them, maintaining **SLA compliance** and safeguarding your business operations.