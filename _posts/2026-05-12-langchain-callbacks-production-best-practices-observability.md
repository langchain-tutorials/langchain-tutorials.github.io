---
title: "LangChain Callbacks in Production: Best Practices for Reliable LLM Observability"
description: "Master LangChain callbacks production best practices for reliable LLM observability. Get expert tips to debug and optimize your AI applications effectively."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain callbacks production best practices]
featured: false
image: '/assets/images/langchain-callbacks-production-best-practices-observability.webp'
---

## LangChain Callbacks in Production: Best Practices for Reliable LLM Observability

Building applications with Large Language Models (LLMs) is an exciting journey. As your applications move from experiments to real-world use, you need a way to see what's happening inside them. This is where LangChain callbacks become incredibly important for `production observability`.

Think of LangChain callbacks as special messengers that tell you exactly what your LLM application is doing. They notify you when an LLM call starts, when a tool is used, or when an error happens. Using these messengers wisely is key for reliable operations in production.

This guide will walk you through the `LangChain callbacks production best practices`. We'll explore how to use them effectively for monitoring, debugging, and improving your LLM applications. You'll learn how to build robust systems that keep you informed, even when things go wrong.

### What are LangChain Callbacks? A Quick Look

LangChain is a framework that helps you build complex applications using LLMs. It lets you chain different components together, like LLMs, prompt templates, and tools. Callbacks are a core part of this framework.

Callbacks are pieces of code that get called at specific moments during your application's execution. For instance, a callback can run when an LLM generates a response or when an agent decides to use a tool. They are like event listeners, waiting for something to happen.

You can customize these callbacks to do almost anything you need. They provide hooks into the internal workings of your LangChain application. This makes them super powerful for understanding and reacting to events within your system.

### Why Callbacks are Crucial in Production

In a live `production` environment, things can go wrong. Your LLM might give a strange answer, a tool might fail, or an API call could time out. Without good `production observability`, finding the problem is like searching in the dark.

Callbacks shine brightly in these situations. They help you log events, track performance, and catch errors before they become bigger issues. Let's look at why they are so vital for `reliable LLM observability`.

#### Debugging Made Easier

Imagine your LangChain agent isn't behaving as expected. Without callbacks, you'd only see the final output, if any. Callbacks let you peek into each step the agent takes.

They show you which prompts were sent to the LLM, what responses came back, and which tools were invoked. This step-by-step breakdown is invaluable for figuring out why your application went off track. You can trace the entire flow, making debugging much simpler.

#### Performance Monitoring and Optimization

How long does it take for your LLM chain to complete a task? Are some steps much slower than others? `Performance monitoring` is essential to keep your users happy.

Callbacks can record the start and end times of various operations. You can use this data to identify bottlenecks and optimize your application's speed. Fast applications lead to better user experiences.

#### Robust Error Handling

Errors will happen; it's a fact of software development. How you handle these errors determines the reliability of your system. Callbacks offer a powerful mechanism for `error handling`.

You can set up callbacks to trigger specific actions when an error occurs. This might include logging the error details, sending an alert to your team, or even retrying a failed step. Good error handling prevents small issues from causing major outages.

#### Auditing and Compliance

In many industries, you need to keep a record of how your systems operate. Callbacks can help you create an audit trail of every interaction with your LLM. This includes inputs, outputs, and any tools used.

This audit trail is useful for security, compliance, and understanding how users interact with your AI. It provides transparency and accountability for your LLM applications.

### Core Best Practices for LangChain Callbacks in Production

To get the most out of `LangChain callbacks in production`, you need to follow some best practices. These guidelines will help you build stable, performant, and observable LLM applications. Implementing these correctly is a cornerstone of `reliable LLM observability`.

#### Keep Callbacks Simple and Focused

Each callback should ideally do one thing and do it well. Don't try to log, send an email, update a database, and call another API all in one callback. This makes them hard to understand and maintain.

If a callback needs to perform multiple, unrelated actions, split it into several smaller, focused callbacks. This adheres to the single responsibility principle. Simple callbacks are easier to test and less likely to introduce bugs.

#### Robust Error Handling within Callbacks

It's ironic but true: your callbacks can also fail. If a callback itself throws an error, it could potentially interrupt your main application flow. You need to protect against this.

Always wrap the logic inside your callbacks with `try-except` blocks. This ensures that even if something goes wrong within the callback, it won't crash your main LangChain application. Log any errors that occur within your callbacks.

```python
{% raw %}
from langchain_core.callbacks import BaseCallbackHandler
import logging

class SafeLoggingCallback(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        try:
            # Safely log the LLM response
            logging.info(f"LLM Response received: {response.generations[0][0].text[:50]}...")
        except Exception as e:
            logging.error(f"Error in SafeLoggingCallback during on_llm_end: {e}")

    def on_llm_error(self, error, **kwargs):
        try:
            # Safely log LLM errors
            logging.error(f"LLM Error encountered: {error}")
            # Potentially send an alert here
        except Exception as e:
            logging.error(f"Error in SafeLoggingCallback during on_llm_error: {e}")
{% endraw %}
```
This example shows how to add basic `error handling` to your callbacks. You are protecting both the logging and error notification logic. You can see more about custom outputs in [Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}), which might interact with callback outcomes.

#### Embrace Asynchronous Callbacks for Performance

Many `production` environments demand high performance and responsiveness. Synchronous callbacks, which run immediately and block the main thread, can slow down your application. This is where `async callbacks` become essential.

`Async callbacks` allow your LangChain application to continue processing while the callback performs its task in the background. This is crucial for `performance monitoring` and ensures your application remains fast and responsive. For example, if you're building a RAG application, you wouldn't want your logging to delay the user's response from your [Build RAG Applications with LangChain Vector Store]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

```python
{% raw %}
import asyncio
from langchain_core.callbacks import AsyncCallbackHandler
import logging

class AsyncMetricCallback(AsyncCallbackHandler):
    async def on_llm_start(self, serialized, prompts, **kwargs):
        start_time = asyncio.get_event_loop().time()
        self.start_times = getattr(self, 'start_times', {})
        self.start_times[tuple(prompts)] = start_time
        logging.debug(f"LLM call started for prompts: {prompts[0][:30]}...")

    async def on_llm_end(self, response, **kwargs):
        prompts = kwargs.get('prompts') # This might need careful handling depending on LangChain version
        if prompts and tuple(prompts) in self.start_times:
            start_time = self.start_times.pop(tuple(prompts))
            end_time = asyncio.get_event_loop().time()
            duration = end_time - start_time
            logging.info(f"LLM call finished in {duration:.2f} seconds.")
            # Imagine sending this metric to an external system
            await self._send_metric_to_external_system(duration)
        else:
            logging.warning("Could not find start time for LLM call.")

    async def _send_metric_to_external_system(self, duration: float):
        # Simulate an I/O bound operation, like sending to Datadog or Prometheus
        await asyncio.sleep(0.01) # Non-blocking sleep
        logging.info(f"Metric sent to external system: {duration:.2f}s")

# Example usage (simplified, assuming an async chain)
async def run_async_chain_with_callback(chain, prompt):
    callbacks = [AsyncMetricCallback()]
    result = await chain.ainvoke({"input": prompt}, config={"callbacks": callbacks})
    return result
{% endraw %}
```
This example shows an `async callback` that measures the duration of LLM calls. The `_send_metric_to_external_system` method simulates a non-blocking external call. This pattern is vital for maintaining good `performance monitoring` without blocking your application.

#### Comprehensive Logging and Metrics

For robust `production observability`, you need more than just basic print statements. Implement structured logging. This means your logs should be in a machine-readable format like JSON.

Structured logs are easy to parse, filter, and analyze with log management tools. Your callbacks should capture key information: timestamps, event types, chain IDs, LLM inputs/outputs, tool calls, and error messages. This detail helps immensely with debugging and auditing.

```python
{% raw %}
import logging
import json
from datetime import datetime
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List, Union

class StructuredLoggingCallback(BaseCallbackHandler):
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _log_event(self, event_type: str, data: Dict[str, Any]):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            **data
        }
        self.logger.info(json.dumps(log_entry))

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> Any:
        self._log_event("chain_start", {
            "chain_type": serialized.get("lc_kwargs", {}).get("chain_type", "unknown"),
            "inputs": inputs,
            "metadata": kwargs.get("metadata", {})
        })

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        self._log_event("chain_end", {
            "outputs": outputs,
            "metadata": kwargs.get("metadata", {})
        })

    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        self._log_event("chain_error", {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "metadata": kwargs.get("metadata", {})
        })

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> Any:
        self._log_event("llm_start", {
            "llm_model": serialized.get("kwargs", {}).get("model_name", "unknown"),
            "prompts": prompts,
            "metadata": kwargs.get("metadata", {})
        })

    def on_llm_end(self, response: Any, **kwargs: Any) -> Any:
        self._log_event("llm_end", {
            "llm_response_text": response.generations[0][0].text[:100] + "..." if response.generations else "",
            "token_usage": response.llm_output.get("token_usage") if response.llm_output else None,
            "metadata": kwargs.get("metadata", {})
        })

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        self._log_event("tool_start", {
            "tool_name": serialized.get("name", "unknown"),
            "tool_input": input_str,
            "metadata": kwargs.get("metadata", {})
        })

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        self._log_event("tool_end", {
            "tool_output": output,
            "metadata": kwargs.get("metadata", {})
        })

    def on_tool_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        self._log_event("tool_error", {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "metadata": kwargs.get("metadata", {})
        })
{% endraw %}
```
This callback logs detailed, structured JSON messages for various events. This is a robust approach to `production observability`. You can send these logs to a centralized log management system for easy analysis.

#### Using LangSmith for Enhanced Observability

For serious `production observability`, `LangSmith` is an indispensable tool. It's built specifically for LangChain applications and offers deep insights. `LangSmith` automatically captures traces, logs, and spans for every operation in your LangChain application.

It's essentially a managed service that uses callbacks under the hood to give you a beautiful, interactive dashboard. You can visualize chains, debug issues, and evaluate model performance. You can also explore complex agent behaviors, even for tools like those described in [LangChain Google Gemini Function Calling Agent with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

Using `LangSmith` simplifies setting up `performance monitoring` and `error handling` significantly. It automatically provides many of the `LangChain callbacks production best practices` out of the box. You only need to set environment variables or pass a client.

```python
{% raw %}
import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# Set environment variables for LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
os.environ["LANGCHAIN_PROJECT"] = "Production LLM App" # Optional: Name your project

# Define a simple chain
llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
chain = LLMChain(llm=llm, prompt=prompt)

# When you run this, LangSmith will automatically capture the trace
# You don't need to manually add callbacks for basic tracing
# result = chain.invoke({"product": "colorful socks"})
# print(result)
{% endraw %}
```
With `LANGCHAIN_TRACING_V2` enabled and `LANGCHAIN_API_KEY` set, `LangSmith` automatically uses its own internal `LangChain callbacks production best practices` to record everything. This provides unparalleled `production observability` without you writing custom callback code for tracing.

#### Context Management and Metadata

Your callbacks often need context about the current operation. For example, which user triggered the request, or what is the unique ID for the current session? LangChain allows you to pass metadata through the `config` dictionary.

You can populate this metadata at the start of a request and access it within your callbacks. This helps tie together disparate log entries and provides crucial context for debugging and `performance monitoring`. Imagine understanding the impact of a slow RAG query from [LangChain Weaviate Hybrid Search for Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}) for a specific user.

```python
{% raw %}
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import logging
import uuid

class ContextualLoggingCallback(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        run_id = kwargs.get("run_id")
        metadata = kwargs.get("metadata", {})
        session_id = metadata.get("session_id", "unknown")
        user_id = metadata.get("user_id", "anonymous")
        logging.info(f"[{session_id}][{user_id}] Chain started with run ID: {run_id}")

    def on_llm_end(self, response, **kwargs):
        run_id = kwargs.get("run_id")
        metadata = kwargs.get("metadata", {})
        session_id = metadata.get("session_id", "unknown")
        user_id = metadata.get("user_id", "anonymous")
        logging.info(f"[{session_id}][{user_id}] LLM finished for run ID: {run_id}, output: {response.generations[0][0].text[:50]}...")

# Example usage
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = PromptTemplate.from_template("Summarize the following text: {text}")
chain = LLMChain(llm=llm, prompt=prompt)

session_id = str(uuid.uuid4())
user_id = "user-123"

# Invoke the chain with metadata
# chain.invoke(
#     {"text": "LangChain is a framework for developing applications powered by language models."},
#     config={
#         "callbacks": [ContextualLoggingCallback()],
#         "metadata": {"session_id": session_id, "user_id": user_id}
#     }
# )
{% endraw %}
```
This callback demonstrates how to access `session_id` and `user_id` from the metadata. This enriches your logs and metrics, crucial for `production observability`.

#### Security Considerations: Redacting Sensitive Data

Your LangChain applications might process sensitive information, like personal identifiable information (PII) or confidential business data. Your callbacks, by their nature, can capture and log this data. This poses a security risk if not handled carefully.

Implement redaction or masking for any sensitive data before it's logged or sent to external systems. This is a critical `LangChain callbacks production best practice`. Ensure your `production observability` doesn't come at the cost of data privacy.

```python
{% raw %}
from langchain_core.callbacks import BaseCallbackHandler
import logging
import re

class RedactingCallback(BaseCallbackHandler):
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _redact(self, text: str) -> str:
        # Example: Redact email addresses
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED_EMAIL]", text)
        # Example: Redact credit card numbers (simple regex, not for full compliance)
        text = re.sub(r"\b(?:\d[ -]*?){13,16}\b", "[REDACTED_CC]", text)
        return text

    def on_llm_start(self, serialized, prompts, **kwargs):
        redacted_prompts = [self._redact(p) for p in prompts]
        self.logger.info(f"LLM Call (Redacted Input): {redacted_prompts[0][:50]}...")

    def on_llm_end(self, response, **kwargs):
        redacted_output = self._redact(response.generations[0][0].text)
        self.logger.info(f"LLM Response (Redacted Output): {redacted_output[:50]}...")

    def on_tool_start(self, serialized, input_str, **kwargs):
        redacted_input = self._redact(input_str)
        self.logger.info(f"Tool Call (Redacted Input): {serialized.get('name', 'unknown')} with input: {redacted_input[:50]}...")
{% endraw %}
```
This `RedactingCallback` shows how to strip out potentially sensitive information from prompts and responses. This is a crucial step for maintaining data privacy in `production` environments.

#### Thorough Testing of Your Callbacks

Just like any other part of your application, your callbacks need to be tested. Write unit tests for individual callback handlers to ensure they behave as expected. Test their `error handling` capabilities.

You should also conduct integration tests to verify that callbacks work correctly when integrated with your LangChain application. Ensure they don't introduce unexpected delays or side effects. Well-tested callbacks contribute to reliable `production observability`.

### Implementing Production-Ready Callbacks: Practical Examples

Let's look at some practical examples of `LangChain callbacks production best practices`. These snippets will show you how to apply the principles we've discussed. Each example addresses a common `production observability` need.

#### Example 1: Logging Callback for Detailed `Production Observability`

This callback enhances basic logging by capturing more context for each event. It's a foundational piece for any `production` system. This helps understand the flow of complex multi-step agents, like those built with [LangGraph StateGraph for Multi-Step AI Agent]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

```python
{% raw %}
import logging
from datetime import datetime
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List, Union

class DetailedObservabilityCallback(BaseCallbackHandler):
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger("langchain_app")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.chain_run_data = {} # To store data across a single chain run

    def _log_event(self, event_type: str, message: str, **kwargs: Any):
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": event_type,
                "message": message,
                **kwargs
            }
            # For simplicity, we'll log as string, but in production, consider JSON logging
            self.logger.info(log_entry)
        except Exception as e:
            self.logger.error(f"Error logging event: {e}")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id")
        self.chain_run_data[run_id] = {"start_time": datetime.utcnow(), "inputs": inputs}
        self._log_event(
            "chain_start",
            f"Chain '{serialized.get('lc_kwargs', {}).get('chain_type', 'Unknown')}' started.",
            run_id=str(run_id),
            chain_type=serialized.get('lc_kwargs', {}).get('chain_type', 'Unknown'),
            inputs=inputs
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id")
        data = self.chain_run_data.pop(run_id, {})
        duration = (datetime.utcnow() - data.get("start_time", datetime.utcnow())).total_seconds()
        self._log_event(
            "chain_end",
            f"Chain finished in {duration:.2f} seconds.",
            run_id=str(run_id),
            outputs=outputs,
            duration_seconds=duration,
            inputs_at_start=data.get("inputs")
        )

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id")
        self.chain_run_data.get(run_id, {})[f"llm_start_{kwargs.get('parent_run_id', run_id)}"] = datetime.utcnow()
        self._log_event(
            "llm_start",
            f"LLM call to model '{serialized.get('kwargs', {}).get('model_name', 'Unknown')}' started.",
            run_id=str(run_id),
            parent_run_id=str(kwargs.get("parent_run_id")),
            model_name=serialized.get('kwargs', {}).get('model_name', 'Unknown'),
            prompt_preview=prompts[0][:100] # Log a preview of the prompt
        )

    def on_llm_end(self, response: Any, **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id")
        start_time_key = f"llm_start_{kwargs.get('parent_run_id', run_id)}"
        start_time = self.chain_run_data.get(run_id, {}).pop(start_time_key, datetime.utcnow())
        duration = (datetime.utcnow() - start_time).total_seconds()
        token_usage = response.llm_output.get("token_usage") if response.llm_output else None

        self._log_event(
            "llm_end",
            f"LLM call finished in {duration:.2f} seconds.",
            run_id=str(run_id),
            parent_run_id=str(kwargs.get("parent_run_id")),
            duration_seconds=duration,
            token_usage=token_usage,
            response_preview=response.generations[0][0].text[:100] if response.generations else ""
        )

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id")
        self.chain_run_data.get(run_id, {})[f"tool_start_{kwargs.get('parent_run_id', run_id)}"] = datetime.utcnow()
        self._log_event(
            "tool_start",
            f"Tool '{serialized.get('name', 'Unknown')}' started with input.",
            run_id=str(run_id),
            parent_run_id=str(kwargs.get("parent_run_id")),
            tool_name=serialized.get('name', 'Unknown'),
            tool_input_preview=input_str[:100]
        )

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id")
        start_time_key = f"tool_start_{kwargs.get('parent_run_id', run_id)}"
        start_time = self.chain_run_data.get(run_id, {}).pop(start_time_key, datetime.utcnow())
        duration = (datetime.utcnow() - start_time).total_seconds()
        self._log_event(
            "tool_end",
            f"Tool finished in {duration:.2f} seconds.",
            run_id=str(run_id),
            parent_run_id=str(kwargs.get("parent_run_id")),
            duration_seconds=duration,
            tool_output_preview=output[:100]
        )

    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id")
        self._log_event(
            "chain_error",
            f"Chain encountered an error: {str(error)}",
            run_id=str(run_id),
            error_type=type(error).__name__,
            error_message=str(error)
        )
{% endraw %}
```
This callback provides a rich set of logs for `production observability`. It captures start/end times, inputs, outputs, and errors for chains, LLMs, and tools. This information is crucial for understanding how your application behaves in `production`.

#### Example 2: Performance Monitoring Callback for Latency Tracking

Measuring the time taken for each component is vital for `performance monitoring`. This callback tracks the duration of LLM calls and chain executions. It's a key part of `LangChain callbacks production best practices`.

```python
{% raw %}
import time
from langchain_core.callbacks import BaseCallbackHandler
import logging

class PerformanceMonitoringCallback(BaseCallbackHandler):
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger("performance_monitor")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.timestamps = {}

    def on_llm_start(self, serialized, prompts, **kwargs):
        run_id = kwargs.get("run_id")
        self.timestamps[f"llm_start_{run_id}"] = time.time()
        self.logger.debug(f"LLM {run_id} started.")

    def on_llm_end(self, response, **kwargs):
        run_id = kwargs.get("run_id")
        start_time = self.timestamps.pop(f"llm_start_{run_id}", time.time())
        duration = time.time() - start_time
        self.logger.info(f"LLM {run_id} finished. Duration: {duration:.4f}s")
        # In a real production system, you'd send this to Prometheus/Grafana or Datadog
        self._send_metric("llm_duration_seconds", duration, {"model": kwargs.get("name", "unknown")})

    def on_chain_start(self, serialized, inputs, **kwargs):
        run_id = kwargs.get("run_id")
        self.timestamps[f"chain_start_{run_id}"] = time.time()
        self.logger.debug(f"Chain {run_id} started.")

    def on_chain_end(self, outputs, **kwargs):
        run_id = kwargs.get("run_id")
        start_time = self.timestamps.pop(f"chain_start_{run_id}", time.time())
        duration = time.time() - start_time
        self.logger.info(f"Chain {run_id} finished. Duration: {duration:.4f}s")
        self._send_metric("chain_duration_seconds", duration, {"chain_type": serialized.get("lc_kwargs", {}).get("chain_type", "unknown")})

    def _send_metric(self, metric_name: str, value: float, tags: dict = None):
        # Placeholder for sending metrics to an actual monitoring system
        tags_str = ", ".join([f"{k}={v}" for k, v in tags.items()]) if tags else ""
        self.logger.debug(f"METRIC: {metric_name}={value} ({tags_str})")
        # Example: Push to a metrics service (e.g., StatsD, Prometheus client)
        # statsd_client.gauge(metric_name, value, tags=tags)
{% endraw %}
```
This callback uses `time.time()` to measure the duration of LLM and chain operations. It then logs these durations. In a real `production` setup, the `_send_metric` method would push data to a dedicated `performance monitoring` system.

#### Example 3: Error Notification Callback for Prompt `Error Handling`

When an error happens, you need to know about it immediately. This callback focuses on `error handling` by notifying you of failures. It's a critical component of `LangChain callbacks production best practices`.

```python
{% raw %}
import logging
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, Union

class ErrorNotificationCallback(BaseCallbackHandler):
    def __init__(self, logger: logging.Logger = None, notification_service=None):
        self.logger = logger or logging.getLogger("error_notifier")
        self.logger.setLevel(logging.ERROR)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.notification_service = notification_service # e.g., a Slack client, PagerDuty API

    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id", "unknown")
        error_message = f"Chain (Run ID: {run_id}) failed: {type(error).__name__} - {str(error)}"
        self.logger.error(error_message, exc_info=True)
        if self.notification_service:
            try:
                self.notification_service.send_alert(f"CRITICAL LangChain Error: {error_message}")
            except Exception as e:
                self.logger.exception(f"Failed to send notification for chain error: {e}")

    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id", "unknown")
        parent_run_id = kwargs.get("parent_run_id", "unknown")
        error_message = f"LLM Call (Run ID: {run_id}, Parent: {parent_run_id}) failed: {type(error).__name__} - {str(error)}"
        self.logger.error(error_message, exc_info=True)
        if self.notification_service:
            try:
                self.notification_service.send_alert(f"CRITICAL LLM Error: {error_message}")
            except Exception as e:
                self.logger.exception(f"Failed to send notification for LLM error: {e}")

    def on_tool_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        run_id = kwargs.get("run_id", "unknown")
        parent_run_id = kwargs.get("parent_run_id", "unknown")
        tool_name = kwargs.get("serialized", {}).get("name", "unknown tool")
        error_message = f"Tool '{tool_name}' (Run ID: {run_id}, Parent: {parent_run_id}) failed: {type(error).__name__} - {str(error)}"
        self.logger.error(error_message, exc_info=True)
        if self.notification_service:
            try:
                self.notification_service.send_alert(f"CRITICAL Tool Error: {error_message}")
            except Exception as e:
                self.logger.exception(f"Failed to send notification for tool error: {e}")

# Dummy Notification Service
class DummyNotificationService:
    def send_alert(self, message: str):
        print(f"--- ALERT SENT ---: {message}")

# Example usage with a dummy service
# notification_service = DummyNotificationService()
# callbacks = [ErrorNotificationCallback(notification_service=notification_service)]
#
# from langchain_openai import ChatOpenAI
# from langchain.chains import LLMChain
# from langchain_core.prompts import PromptTemplate
#
# llm = ChatOpenAI(model="gpt-3.5-turbo-012345", temperature=0) # Use a non-existent model to force an error
# prompt = PromptTemplate.from_template("Tell me a story about {subject}")
# chain = LLMChain(llm=llm, prompt=prompt)
#
# try:
#     chain.invoke({"subject": "a magical cat"}, config={"callbacks": callbacks})
# except Exception:
#     pass # We expect an error, so we catch it
{% endraw %}
```
This callback logs detailed error messages and attempts to send alerts. The `notification_service` could be integrated with Slack, PagerDuty, or any other alerting system. This ensures prompt `error handling` and improves overall `production observability`.

#### Example 4: Cost Tracking Callback for LLM Token Usage

LLM costs can quickly add up in `production`. A cost tracking callback helps you monitor token usage and estimate expenses. This is a crucial part of `LangChain callbacks production best practices` for budget management.

```python
{% raw %}
from langchain_core.callbacks import BaseCallbackHandler
import logging
from typing import Any, Dict

# Define a simple token cost mapping (example values)
TOKEN_COST_PER_MILLION = {
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
    # Add other models as needed
}

class CostTrackingCallback(BaseCallbackHandler):
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger("cost_tracker")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.total_cost = 0.0

    def on_llm_end(self, response: Any, **kwargs: Any) -> Any:
        try:
            llm_output = response.llm_output
            if llm_output and "token_usage" in llm_output:
                prompt_tokens = llm_output["token_usage"].get("prompt_tokens", 0)
                completion_tokens = llm_output["token_usage"].get("completion_tokens", 0)
                model_name = kwargs.get("llm_name", "unknown_model") # LangChain often provides llm_name

                model_costs = TOKEN_COST_PER_MILLION.get(model_name)
                if model_costs:
                    cost_input = (prompt_tokens / 1_000_000) * model_costs["input"]
                    cost_output = (completion_tokens / 1_000_000) * model_costs["output"]
                    current_llm_cost = cost_input + cost_output
                    self.total_cost += current_llm_cost

                    self.logger.info(
                        f"LLM {model_name} usage - Prompt: {prompt_tokens} tokens, "
                        f"Completion: {completion_tokens} tokens. Current Cost: ${current_llm_cost:.6f}"
                    )
                    self.logger.info(f"Total estimated cost so far: ${self.total_cost:.6f}")
                else:
                    self.logger.warning(f"No cost defined for model: {model_name}. Cannot track cost.")
        except Exception as e:
            self.logger.error(f"Error in CostTrackingCallback: {e}")

# Example usage (assuming an LLM call happens)
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage
#
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# cost_callback = CostTrackingCallback()
#
# response = llm.invoke(
#     [HumanMessage(content="Hello, how are you today? What is the weather like in London?")],
#     config={"callbacks": [cost_callback]}
# )
#
# response = llm.invoke(
#     [HumanMessage(content="Write a short poem about a cat.")],
#     config={"callbacks": [cost_callback]}
# )
#
# print(f"Final estimated application cost: ${cost_callback.total_cost:.6f}")
{% endraw %}
```
This callback calculates the estimated cost based on token usage and predefined rates. It's a pragmatic way to keep an eye on expenses in a `production` environment.

#### Example 5: Async Callback for External Service Integration

Sometimes your callbacks need to interact with external services, like message queues or analytics platforms. Using `async callbacks` for these interactions is crucial to avoid blocking your application. This is a prime example of `async callbacks` being part of `LangChain callbacks production best practices`.

```python
{% raw %}
import asyncio
from langchain_core.callbacks import AsyncCallbackHandler
import logging

class AsyncExternalServiceCallback(AsyncCallbackHandler):
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger("async_external")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    async def _send_to_analytics_service(self, event_data: dict):
        """Simulates an async call to an external analytics service."""
        try:
            # This could be an actual aiohttp or httpx call
            await asyncio.sleep(0.05) # Simulate network latency
            self.logger.info(f"Successfully sent event to analytics: {event_data.get('event_type')}")
        except Exception as e:
            self.logger.error(f"Failed to send event to analytics service: {e}")

    async def on_chain_end(self, outputs, **kwargs):
        run_id = str(kwargs.get("run_id"))
        chain_type = kwargs.get("serialized", {}).get("lc_kwargs", {}).get("chain_type", "unknown")
        
        event_data = {
            "event_type": "chain_completed",
            "chain_id": run_id,
            "chain_type": chain_type,
            "output_preview": str(outputs)[:100]
        }
        await self._send_to_analytics_service(event_data)

    async def on_llm_end(self, response, **kwargs):
        run_id = str(kwargs.get("run_id"))
        model_name = kwargs.get("serialized", {}).get("kwargs", {}).get("model_name", "unknown")
        token_usage = response.llm_output.get("token_usage") if response.llm_output else {}

        event_data = {
            "event_type": "llm_response_received",
            "llm_id": run_id,
            "model_name": model_name,
            "prompt_tokens": token_usage.get("prompt_tokens", 0),
            "completion_tokens": token_usage.get("completion_tokens", 0),
            "response_preview": response.generations[0][0].text[:100] if response.generations else ""
        }
        await self._send_to_analytics_service(event_data)

    async def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        run_id = str(kwargs.get("run_id"))
        tool_name = kwargs.get("serialized", {}).get("name", "unknown")

        event_data = {
            "event_type": "tool_executed",
            "tool_id": run_id,
            "tool_name": tool_name,
            "tool_output_preview": output[:100]
        }
        await self._send_to_analytics_service(event_data)

# Example usage with an async chain
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains import LLMChain
#
# async def main():
#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
#     prompt = ChatPromptTemplate.from_template("What is the capital of {country}?")
#     chain = LLMChain(llm=llm, prompt=prompt)
#
#     callbacks = [AsyncExternalServiceCallback()]
#
#     await chain.ainvoke({"country": "France"}, config={"callbacks": callbacks})
#     await chain.ainvoke({"country": "Germany"}, config={"callbacks": callbacks})
#
# if __name__ == "__main__":
#     asyncio.run(main())
{% endraw %}
```
This `async callback` sends event data to a simulated analytics service without blocking the main program. This pattern is ideal for integrating with any external, I/O-bound service. It ensures that your `performance monitoring` remains efficient.

### Advanced Strategies for Callback Management

Beyond individual callbacks, managing them effectively is a `LangChain callbacks production best practice`. You might use multiple callbacks, or need to control their behavior.

#### Callback Handlers vs. Callback Managers

LangChain provides `BaseCallbackHandler` (which we've used) and `BaseCallbackManager`.
*   **Callback Handlers** are individual callbacks, like the ones we've created. They define what happens for specific events.
*   **Callback Managers** are containers for multiple handlers. They dispatch events to all registered handlers. You usually interact with managers implicitly when passing a list of handlers to `config={"callbacks": [...]}`.

For most uses, simply passing a list of `BaseCallbackHandler` instances is enough. LangChain will create a manager internally. However, for more control, you can create and customize your own `CallbackManager`.

#### Customizing Callback Manager

You can create a `CallbackManager` to pre-configure a set of handlers or to filter which events go to which handler. This is useful for complex `production` setups.

```python
{% raw %}
from langchain_core.callbacks import CallbackManager, BaseCallbackHandler
import logging
from typing import Any, Dict, List, Union

class SimpleLogger(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        logging.info(f"Logger: LLM End - {response.generations[0][0].text[:30]}...")

class SimpleNotifier(BaseCallbackHandler):
    def on_chain_error(self, error, **kwargs):
        logging.error(f"Notifier: Chain Error - {str(error)}")

# You can create a callback manager explicitly
# This is useful if you want to reuse a specific set of handlers
# my_callback_manager = CallbackManager([SimpleLogger(), SimpleNotifier()])

# Then pass it to your chain's config
# chain.invoke({"input": "test"}, config={"callbacks": my_callback_manager})

# Usually, LangChain handles this automatically if you pass a list:
# chain.invoke({"input": "test"}, config={"callbacks": [SimpleLogger(), SimpleNotifier()]})
{% endraw %}
```
Using a `CallbackManager` can help structure your callback logic for `production observability`.

#### Filtering Callbacks

Sometimes you don't want all callbacks to run for every event. LangChain allows you to configure callbacks with `tags` or `verbose` flags. You can also implement custom logic within your `on_xxx_start` methods to decide whether to proceed.

This helps reduce noise and improves `performance monitoring` by preventing unnecessary operations. Efficient filtering is part of `LangChain callbacks production best practices`.

### Troubleshooting Common Callback Issues in Production

Even with best practices, you might encounter issues. Here are some common problems and tips for `error handling`.

*   **Callbacks Slowing Down Your Application**: If your `production` app is suddenly slow, check your callbacks. Are they doing heavy I/O synchronously? Switch to `async callbacks` or defer heavy tasks to a background queue. Ensure they are kept simple.
*   **Callbacks Failing Silently**: This is a dangerous issue. Always include robust `error handling` (try-except blocks) within your callbacks. Log any internal callback errors so you know when they fail.
*   **Too Much Data Being Logged**: Over-logging can overwhelm your logging system and incur costs. Implement careful redaction and configure logging levels appropriately. Use `verbose=False` or specific tags to reduce output for less critical components.
*   **Callbacks Not Being Triggered**: Double-check that your callbacks are correctly passed to the `config={"callbacks": ...}` parameter of your chain or agent. Ensure you're using the correct `BaseCallbackHandler` or `AsyncCallbackHandler` base class.

### Conclusion

`LangChain callbacks production best practices` are not just good ideas; they are essential for building `reliable LLM observability`. By implementing robust `error handling`, embracing `async callbacks` for `performance monitoring`, and leveraging tools like `LangSmith`, you can gain unprecedented visibility into your LLM applications.

These practices ensure that your `production` systems are stable, debuggable, and performant. You are now equipped to build LangChain applications that truly shine in the real world. Happy building! If you want to dive deeper into LangChain's capabilities, explore articles like [Top LangChain Alternatives 2026: 10 Frameworks Compared & Ranked]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}) for broader context on the ecosystem, or [LangChain Semantic Text Splitter: Chunk by Meaning]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}) for a specific component.