---
title: "LangChain Error Handling Best Practices: Logging and Monitoring Guide"
description: "Master LangChain error logging, monitoring, and best practices for robust LLM apps. Learn key strategies to prevent common issues and ensure smooth operation."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [langchain error logging monitoring best practices]
featured: false
image: '/assets/images/langchain-error-handling-logging-monitoring-guide.webp'
---

# LangChain Error Handling Best Practices: Logging and Monitoring Guide

Building smart applications with LangChain is exciting! You can create powerful AI agents and complex chains that do amazing things. But just like any computer program, sometimes things can go wrong.

When your LangChain app doesn't work as expected, it can be tricky to figure out why. This is where good `langchain error logging monitoring best practices` come into play. They help you understand problems and fix them quickly.

Imagine your LangChain app as a friendly robot. If the robot gets stuck, you need a way for it to tell you what happened. Logging is like the robot writing down its thoughts, and monitoring is like you keeping an eye on the robot's health.

This guide will show you how to use `langchain error logging monitoring best practices` to keep your AI apps running smoothly. We will explore simple ways to track what your LangChain app is doing. You'll learn how to spot problems before they become big headaches.

## Why LangChain Error Logging is Your AI's Best Friend

Think of logging as keeping a diary for your LangChain application. Every time something important happens, good or bad, your app writes it down. This diary helps you understand its behavior later.

When an error pops up, `langchain error logging` becomes super important. It tells you exactly what went wrong, where it happened, and sometimes even why. Without logs, finding problems is like searching for a needle in a haystack blindfolded.

Good logging helps you debug your LangChain chains and agents faster. It gives you clues when your AI gives unexpected answers or gets stuck in a loop. You can review the step-by-step actions that led to the issue.

### Understanding Different Log Levels

Not all diary entries are equally important. Some are just notes, while others are urgent warnings. This is why we use different `log levels configuration`. Each level tells you how serious a message is.

*   **DEBUG:** These are very detailed messages, like talking to yourself while solving a puzzle. You use them when you need to understand every tiny step your LangChain app takes. They are usually turned off in live applications.

*   **INFO:** These messages tell you about normal events, like "I started task A" or "I finished task B." They show the general flow of your application. These are helpful for understanding what your app is doing day-to-day.

*   **WARNING:** These logs mean "Hmm, something unexpected happened, but I can keep going." Maybe an optional setting was missing, or a backup method was used. You should usually check these out.

*   **ERROR:** This means "Uh oh, I hit a problem, and I can't complete what I was trying to do." This is a significant issue that needs your attention. Your LangChain chain might have failed completely.

*   **CRITICAL:** These are "Emergency! Everything is broken!" messages. This level is for very serious failures that might stop your entire application. You need to drop everything and fix these immediately.

By setting the right `log levels configuration`, you can control how much information your app records. You can choose to see only warnings and errors in your live application. Then, when you're debugging, you can switch to DEBUG to see everything.

### Implementing Basic Logging in LangChain

Python has a built-in `logging` module that is very powerful. LangChain works well with this standard Python logging. You can set it up to start recording messages right away.

Here’s how you can get started with basic logging in your LangChain application:

```python
import logging
import sys

# Set up the logger
# We're making a logger named 'langchain_app'
logger = logging.getLogger('langchain_app')
# We want to see all messages from INFO level and above
logger.setLevel(logging.INFO)

# Create a handler to send logs to the console (standard output)
handler = logging.StreamHandler(sys.stdout)
# We're setting the handler to also show all messages from INFO level and above
handler.setLevel(logging.INFO)

# Create a formatter to make log messages look nice
# It will show time, log level, and the message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to our logger
logger.addHandler(handler)

# Now you can use the logger in your LangChain code
logger.info("LangChain application started.")

try:
    # Example of a simple LangChain operation
    # (Let's imagine some LangChain code here)
    # from langchain_community.llms import OpenAI # Just for illustration, not actual usage
    # llm = OpenAI()
    # result = llm.invoke("What is the capital of France?")
    # logger.info(f"LLM successfully invoked. Result: {result}")

    # Simulating an error
    raise ValueError("Something went wrong during chain execution!")

except Exception as e:
    logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    logger.warning("Chain might have failed to complete its task.")

logger.info("LangChain application finished.")
```

In this example, you see how to create a logger and send messages at different levels. The `exc_info=True` in the error log is very important. It tells the logger to include all the details about the error, like where it happened in the code. This is a crucial part of `langchain error logging`.

## Mastering LangChain Logging Techniques

Just writing down messages isn't always enough. For `langchain error logging monitoring best practices`, you need to make your logs useful. This means using `structured logging` and good `error log formatting`.

### What is Structured Logging?

Imagine a diary where every entry is a simple sentence. Finding specific information later would be hard. `Structured logging` is like writing your diary entries in a very organized way, using labels for each piece of information.

Instead of a simple sentence like "User tried to do X and it failed," structured logging might look like this:

```json
{
  "timestamp": "2023-10-27T10:30:00Z",
  "level": "ERROR",
  "message": "User action failed",
  "user_id": "user123",
  "action": "purchase_item",
  "item_id": "product_A",
  "error_type": "PaymentProcessorError",
  "chain_step": "payment_processing_agent"
}
```

See how clear that is? Each piece of data has a key (like `user_id` or `error_type`) and a value. This makes it much easier for computers to read and analyze your logs. It’s a core part of `langchain error logging monitoring best practices`.

### Benefits of Structured Logging for LangChain

*   **Easy Searching:** You can quickly search for all errors related to `user_id: "user123"` or all failures in `chain_step: "payment_processing_agent"`.
*   **Better Analysis:** Tools can automatically count how many times `error_type: "PaymentProcessorError"` occurs. This helps in `monitoring error rates`.
*   **Faster Debugging:** All relevant information is right there in the log entry. You don't have to guess what happened.
*   **Compatibility:** Many `log aggregation` and monitoring platforms expect or prefer structured logs.

### Practical Structured Logging Example

You can achieve structured logging in Python using different libraries, or by formatting your log messages as JSON. Here's a simple example using the standard `logging` module and JSON:

```python
import logging
import sys
import json
import datetime

logger = logging.getLogger('langchain_structured_app')
logger.setLevel(logging.INFO)

# Custom formatter to output JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            # Add any extra fields passed in 'extra' dict
            **getattr(record, 'extra_fields', {})
        }
        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

# Example usage in a LangChain context
def run_my_langchain_agent(user_input: str, user_id: str):
    logger.info("Attempting to run agent.", extra_fields={"user_id": user_id, "input": user_input})
    try:
        # Simulate an agent call
        if "fail" in user_input.lower():
            raise ValueError("Agent encountered a critical word.")
        
        # Simulating a successful LangChain operation
        result = f"Agent processed '{user_input}' successfully."
        logger.info(result, extra_fields={"user_id": user_id, "output": result, "status": "success"})
        return result
    except Exception as e:
        logger.error(f"Agent failed for input: '{user_input}'", 
                     extra_fields={"user_id": user_id, "error_type": type(e).__name__, "agent_step": "final_answer_generation"},
                     exc_info=True)
        return "Sorry, I couldn't complete that request."

# Test cases
run_my_langchain_agent("Hello, world!", "user_A")
run_my_langchain_agent("Please fail this task.", "user_B")
```

The `extra_fields` in the logger calls allow you to add custom data to each log entry. This is the heart of `structured logging` and immensely useful for `log analysis techniques`. For more advanced structured logging, libraries like `python-json-logger` or `structlog` can make this even easier.

### Error Log Formatting

While `structured logging` handles the data, `error log formatting` makes sure that when a human reads the log, it's clear and understandable. Even with JSON, the actual error message and traceback need to be readable.

When an exception happens in Python, it generates a "traceback." This traceback is like a map showing all the functions your program called leading up to the error. It's crucial for debugging. Always include the traceback for `ERROR` and `CRITICAL` logs.

The `exc_info=True` parameter in `logger.error()` does exactly this. It includes the traceback automatically. Make sure your `JsonFormatter` or chosen structured logging tool handles this traceback nicely. You want it to be a string or a list of strings within your JSON, not an unparsed mess.

## Bringing All Your Logs Together: Centralized Logging

Imagine your LangChain application is made of many small parts, maybe running on different computers. Each part creates its own log diary. Reading all these diaries separately to find a problem would be a nightmare. This is where `centralized logging` and `log aggregation` come in.

`Centralized logging` means gathering all your log messages from different parts of your application and putting them in one single place. `Log aggregation` is the process of collecting these logs. It's like having a big digital library for all your application's diaries.

### Benefits of Centralized Logging

*   **One Place to Search:** When something goes wrong, you don't have to log into many different servers. All logs are in one dashboard.
*   **Correlate Events:** You can see how an action in one part of your LangChain application affects another part. For example, a request hitting your API gateway, then moving through a LangChain agent, and finally storing results in a database.
*   **Long-Term Storage:** Centralized systems can store logs for a long time. This is useful for auditing, compliance, and looking back at past issues.
*   **Security:** Centralized logging can also be used as a `SIEM tool` (Security Information and Event Management). It helps detect unusual activities or security threats by analyzing log patterns across your system. For more on security, you might find this internal link useful: [Securing Your LangChain Applications: A Developer's Guide](/blog/securing-langchain-apps.md).
*   **Monitoring and Alerting:** Once logs are in one place, it's easier to set up `monitoring error rates` and `alerting strategies` based on the content of these logs.

### Popular Centralized Logging Solutions

Many powerful tools can help you with `centralized logging` and `log aggregation`. These tools can collect logs, store them efficiently, and provide great interfaces for searching and analyzing.

*   **ELK Stack (Elasticsearch, Logstash, Kibana):** This is a very popular open-source choice.
    *   **Logstash** collects logs from everywhere.
    *   **Elasticsearch** stores and indexes the logs, making them super fast to search.
    *   **Kibana** provides a beautiful web interface to visualize and explore your logs.
    You can learn more and get started with their documentation [here](https://www.elastic.co/what-is/elk-stack).
    *Affiliate Link: If you're looking for a hosted ELK solution, [Elastic Cloud](https://cloud.elastic.co/registration?locale=en&cloud_id=40030097a8a0f8b1e4f483c6b24d9c79&utm_source=affiliate&utm_medium=referral&utm_campaign=my_blog_name) offers managed services.*

*   **Splunk:** A powerful, enterprise-grade platform for machine data. It's known for its robust search and analysis capabilities, particularly strong as a `SIEM tool`.
    *You can explore Splunk's capabilities on their official website [here](https://www.splunk.com/).*

*   **Datadog:** A cloud-based `observability setup` platform that combines logging, metrics, and tracing. It's known for its ease of use and comprehensive dashboards.
    *Datadog offers a trial and more information on their logging management services [here](https://www.datadoghq.com/product/log-management/).*
    *Affiliate Link: [Start your Datadog free trial](https://www.datadoghq.com/free-trial/?ref=myblogname) and see how it can simplify your log management.*

*   **Other Log Management Solutions:** There are many other excellent `log management solutions` available, both open-source and commercial. Some include Loki (with Grafana), Graylog, Sumologic, and LogRhythm. Choosing the right one depends on your budget, scale, and specific needs.

## Keeping an Eye on Things: Monitoring LangChain Errors

Logging tells you what happened, but `monitoring error rates` tells you how often it's happening and if things are getting worse. Monitoring is like having a watchful guard for your LangChain application. It constantly checks important numbers and behaviors.

When it comes to `langchain error logging monitoring best practices`, monitoring helps you:
*   **Spot trends:** Are errors increasing over time?
*   **Understand impact:** How many users are affected by an error?
*   **Measure performance:** Is your LangChain app slow?

### Metrics Collection for LangChain

`Metrics collection` means gathering numbers about your application's performance and health. Instead of just logging an error message, you also count how many errors occurred.

Useful metrics for LangChain applications include:
*   **Total requests:** How many times your LangChain agent was asked to do something.
*   **Successful requests:** How many times it completed its task without errors.
*   **Failed requests:** How many times an error occurred.
*   **Error rate:** The percentage of failed requests (`Failed requests / Total requests * 100`). This is crucial for `monitoring error rates`.
*   **Latency/Response time:** How long it takes for your LangChain agent to respond.
*   **Token usage:** How many tokens (parts of words) your LLM consumed for each request. This can affect cost.
*   **Specific agent/chain failures:** Counting errors for particular parts of your LangChain app.

### How to Collect Metrics

You can collect metrics in your LangChain application using libraries or by integrating with dedicated `metrics platforms`.

*   **Prometheus:** A very popular open-source `metrics platform`. It "scrapes" (collects) metrics from your applications at regular intervals. Your LangChain app would expose a special web endpoint with metrics data.
    *Learn more about Prometheus on their official website [here](https://prometheus.io/).*
    *Affiliate Link: For managed Prometheus services, consider providers like [Grafana Cloud](https://grafana.com/products/cloud/?via=my_blog_name) which offer hosted solutions.*

*   **Grafana:** Often used with Prometheus, Grafana is an open-source tool for creating beautiful dashboards to visualize your metrics. You can see graphs of your `monitoring error rates` over time, latency, and more.
    *Explore Grafana's features and download it [here](https://grafana.com/).*

*   **Datadog:** As mentioned before, Datadog also provides strong `metrics platforms` capabilities, allowing you to collect, visualize, and alert on any metric.
    *Affiliate Link: [Sign up for Datadog](https://www.datadoghq.com/free-trial/?ref=myblogname) to easily monitor your LangChain application's performance.*

### Practical Metrics Example in Python

You can use a simple counter from a library like `Prometheus client` for Python to expose metrics.

```python
from prometheus_client import Counter, Gauge, generate_latest
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import logging

# Set up basic logging for this example
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define Prometheus metrics
LANGCHAIN_REQUESTS_TOTAL = Counter(
    'langchain_requests_total', 
    'Total number of LangChain requests.', 
    ['status'] # 'status' can be 'success' or 'failure'
)
LANGCHAIN_LATENCY_SECONDS = Gauge(
    'langchain_latency_seconds', 
    'Latency of LangChain requests in seconds.', 
    ['chain_name']
)
LANGCHAIN_ERROR_COUNT = Counter(
    'langchain_error_count',
    'Count of specific LangChain errors.',
    ['error_type', 'chain_name']
)

def run_my_complex_langchain_chain(chain_name: str, simulate_error: bool = False):
    start_time = time.time()
    try:
        logger.info(f"Running LangChain chain: {chain_name}")
        # Simulate LangChain processing
        if simulate_error:
            raise ValueError("LLM API call failed or chain logic error.")
        
        time.sleep(0.5) # Simulate work
        logger.info(f"Chain {chain_name} completed successfully.")
        
        LANGCHAIN_REQUESTS_TOTAL.labels(status='success').inc()
        LANGCHAIN_LATENCY_SECONDS.labels(chain_name=chain_name).set(time.time() - start_time)
        return "Chain completed!"
    except Exception as e:
        logger.error(f"Error in chain {chain_name}: {e}", exc_info=True)
        LANGCHAIN_REQUESTS_TOTAL.labels(status='failure').inc()
        LANGCHAIN_ERROR_COUNT.labels(error_type=type(e).__name__, chain_name=chain_name).inc()
        LANGCHAIN_LATENCY_SECONDS.labels(chain_name=chain_name).set(time.time() - start_time) # Log latency even on error
        return "Chain failed!"

# Example usage
run_my_complex_langchain_chain("summarization_chain", simulate_error=False)
run_my_complex_langchain_chain("qa_agent_chain", simulate_error=True)
run_my_complex_langchain_chain("summarization_chain", simulate_error=False)
run_my_complex_langchain_chain("qa_agent_chain", simulate_error=False)

# This part sets up a simple web server to expose metrics for Prometheus
class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_latest())
        else:
            self.send_response(404)
            self.end_headers()

def run_metrics_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MetricsHandler)
    logger.info(f"Serving metrics on http://localhost:{port}/metrics")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Stopping metrics server.")
        httpd.server_close()

# To run the metrics server, uncomment the line below and run this script.
# Prometheus would then scrape http://localhost:8000/metrics
# run_metrics_server()
```

This code snippet shows how you can instrument your LangChain code to increase counters for successes and failures. You can then use tools like Prometheus to scrape these metrics and Grafana to visualize them, helping you with `monitoring error rates`. You might also want to check out our post on [Getting Started with Prometheus and Grafana for Your AI Apps](/blog/prometheus-grafana-ai-apps.md) for a deeper dive.

## Getting Alerted When Things Go Wrong

Monitoring shows you what's happening, but `alerting strategies` are what tell you "Hey, look here, something needs your attention now!" It's like having a smoke detector for your LangChain application. When critical issues occur, you need to know immediately.

Alerts trigger notifications when certain conditions are met. For example, if your `monitoring error rates` go above a certain percentage, or if a `CRITICAL` log message appears.

### Designing Effective Alerting Strategies

Good `alerting strategies` are vital for `langchain error logging monitoring best practices`. You don't want too many alerts (which can make you ignore them), but you also don't want to miss important ones.

Here are some tips:
*   **Alert on critical errors:** Always get notified when `ERROR` or `CRITICAL` logs appear in large numbers or specific types.
*   **Thresholds for error rates:** If your LangChain agent's success rate drops below 90% for 5 minutes, send an alert.
*   **Latency spikes:** If your agent takes too long to respond, it might be stuck or overloaded.
*   **Key performance indicators (KPIs):** If a core function of your LangChain app isn't working, alert.
*   **Paging the right people:** Make sure alerts go to the right team or person who can fix the issue.

### Common Alerting Tools

*   **PagerDuty:** A widely used `alerting services` platform that specializes in on-call management. It ensures that the right person is notified at the right time, escalating alerts if they are not acknowledged.
    *Learn more about PagerDuty's incident management [here](https://www.pagerduty.com/).*
    *Affiliate Link: Improve your incident response with [PagerDuty's reliable alerting solutions](https://www.pagerduty.com/sign-up?affid=my_blog_name).*

*   **Grafana Alerting:** If you are already using Grafana for visualization with Prometheus, you can set up alerts directly within Grafana. It can send notifications via email, Slack, PagerDuty, and other channels.

*   **Cloud Provider Alerts:** AWS CloudWatch, Google Cloud Monitoring, Azure Monitor all offer robust alerting capabilities that integrate with their respective logging and metrics services.

*   **Webhook Integrations:** Many `log management solutions` and `metrics platforms` can send alerts to webhooks. These webhooks can then trigger messages in Slack, Microsoft Teams, or custom scripts.

By combining `centralized logging` with `metrics collection` and well-defined `alerting strategies`, you create a powerful defense for your LangChain applications. This allows you to proactive identify and address issues, maintaining the reliability of your AI services.

## Seeing the Whole Picture: Observability for LangChain

`Observability setup` is about understanding what's happening inside your system without having to stop it or add new code for every question. It goes beyond just logs and metrics. It combines logs, metrics, and traces to give you a complete story.

For complex LangChain applications, where many components interact, `observability setup` is key. It helps you answer tough questions like "Why did this specific user's request take so long?" or "Which part of my agent chain introduced this unexpected behavior?"

### What is a Trace?

While logs are diary entries and metrics are numbers, a "trace" is like following one specific customer's journey through your entire LangChain application. It shows you every step, how long each step took, and if any errors happened at any point.

Imagine a user asks your LangChain agent a question. A trace would show:
1.  The request arriving at your API.
2.  The request being passed to the LangChain runtime.
3.  Each tool call the agent makes.
4.  Each LLM call with its prompt and response.
5.  The final answer being sent back.

If there's an error, the trace points exactly to where it occurred. This level of detail is incredibly helpful for complex LangChain chains and agents, and crucial for effective `log analysis techniques`.

### Setting up Observability for LangChain

Achieving full `observability setup` for LangChain apps often involves:
1.  **Instrumenting your code:** Adding small pieces of code to generate logs, metrics, and traces. LangChain itself has some built-in tracing capabilities.
2.  **Using an APM (Application Performance Monitoring) tool:** Tools like Datadog, New Relic, or Dynatrace are designed to collect and visualize all these signals.
3.  **Distributed Tracing Systems:** OpenTelemetry is an open-source standard for collecting telemetry data (logs, metrics, traces). It allows you to send data to various backends.

Datadog, as mentioned before, is a comprehensive platform for `observability setup`. It provides unified dashboards for logs, metrics, and traces, making it easier to correlate events and understand performance across your LangChain applications.

*Affiliate Link: For a complete observability solution, explore [Datadog's platform](https://www.datadoghq.com/free-trial/?ref=myblogname) which integrates logs, metrics, and traces seamlessly.*

### Log Analysis Techniques

Once you have all your logs collected, stored, and maybe even structured, how do you make sense of them? `Log analysis techniques` are methods to get insights from your log data.

*   **Searching and Filtering:** The most basic technique. You search for specific keywords, error codes, user IDs, or time ranges. This is where `structured logging` truly shines.
*   **Pattern Recognition:** Looking for repeated sequences of events or errors. For example, if a specific sequence of agent steps always leads to a failure, that's a pattern.
*   **Trend Analysis:** Using `metrics platforms` like Grafana to visualize log counts over time. Are error logs spiking after a new deployment?
*   **Anomaly Detection:** Automatically finding unusual events or deviations from normal behavior. This often uses machine learning to spot things humans might miss. For example, an unusually high number of calls to a specific external API by your LangChain agent.
*   **Correlation:** Connecting events from different parts of your system. Did a database error cause your LangChain agent to fail? `Centralized logging` and traces make this much easier.
*   **Root Cause Analysis:** Using all available data (logs, metrics, traces) to identify the fundamental reason for a problem. This is the ultimate goal of all `langchain error logging monitoring best practices`.

### Learning More About Observability

If you want to dive deeper into `observability setup` and `log analysis techniques`, there are many great resources. Online courses can provide structured learning.

*Affiliate Link: Consider investing in an [Observability Fundamentals Course](https://www.coursera.org/browse/computer-science/software-development) to master these critical skills and make your LangChain applications more robust.*

For enterprise-level security and compliance, `SIEM tools` are essential. These tools collect security-related logs from all sources, including your LangChain applications, and analyze them for threats. They help ensure your AI systems are not only performant but also secure.

## Practical Examples: Bringing it All Together

Let's look at a more complete example that combines logging, error handling, and a hint of metrics in a LangChain context.

### Example 1: Handling Tool Errors in an Agent

LangChain agents often use "tools" to perform actions. What happens if a tool fails? You need to catch that error and log it properly.

```python
import logging
import sys
import json
import datetime
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import OpenAI # Replace with your actual LLM
# from langchain_openai import OpenAI # Modern way if using OpenAI
import os

# --- Logger Setup (reusing our JSON formatter) ---
logger = logging.getLogger('langchain_agent_app')
logger.setLevel(logging.INFO)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            **getattr(record, 'extra_fields', {})
        }
        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

# --- Define Prometheus Metrics (simple counters for demonstration) ---
from prometheus_client import Counter, Gauge, generate_latest
import time

LANGCHAIN_AGENT_CALLS_TOTAL = Counter(
    'langchain_agent_calls_total', 
    'Total number of LangChain agent calls.', 
    ['agent_name', 'status']
)
LANGCHAIN_TOOL_CALLS_TOTAL = Counter(
    'langchain_tool_calls_total', 
    'Total number of LangChain tool calls.', 
    ['tool_name', 'status']
)
LANGCHAIN_TOOL_LATENCY_SECONDS = Gauge(
    'langchain_tool_latency_seconds',
    'Latency of LangChain tool calls in seconds.',
    ['tool_name']
)

# --- Define a custom tool that might fail ---
@tool
def divide_numbers(numbers_string: str) -> str:
    """Divides two numbers. Input should be a comma-separated string of two numbers, e.g., '10,2'.
       Returns the result or raises an error if division by zero or invalid input."""
    LANGCHAIN_TOOL_CALLS_TOTAL.labels(tool_name='divide_numbers', status='attempt').inc()
    start_time = time.time()
    try:
        num1_str, num2_str = numbers_string.split(',')
        num1 = float(num1_str.strip())
        num2 = float(num2_str.strip())

        if num2 == 0:
            raise ValueError("Cannot divide by zero!")
        
        result = num1 / num2
        LANGCHAIN_TOOL_CALLS_TOTAL.labels(tool_name='divide_numbers', status='success').inc()
        logger.info(f"Tool 'divide_numbers' executed successfully.", 
                    extra_fields={"tool_name": "divide_numbers", "input": numbers_string, "result": result})
        LANGCHAIN_TOOL_LATENCY_SECONDS.labels(tool_name='divide_numbers').set(time.time() - start_time)
        return str(result)
    except Exception as e:
        LANGCHAIN_TOOL_CALLS_TOTAL.labels(tool_name='divide_numbers', status='failure').inc()
        logger.error(f"Error in tool 'divide_numbers': {e}", 
                     extra_fields={"tool_name": "divide_numbers", "input": numbers_string, "error_type": type(e).__name__},
                     exc_info=True)
        LANGCHAIN_TOOL_LATENCY_SECONDS.labels(tool_name='divide_numbers').set(time.time() - start_time)
        # Re-raise or return a specific error message for the agent to handle
        raise e # Let the agent's error handling mechanism take over

# --- Set up the LangChain Agent ---
tools = [divide_numbers]
# Replace with your actual LLM setup (e.g., from langchain_openai import ChatOpenAI)
llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-your-openai-key-here")) 

prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True)

# --- Function to run the agent with logging and metrics ---
def run_agent_with_handling(query: str, agent_name: str = "MathAgent"):
    logger.info(f"Agent '{agent_name}' received query.", 
                extra_fields={"agent_name": agent_name, "query": query})
    LANGCHAIN_AGENT_CALLS_TOTAL.labels(agent_name=agent_name, status='attempt').inc()
    try:
        result = agent_executor.invoke({"input": query})
        logger.info(f"Agent '{agent_name}' completed query successfully.", 
                    extra_fields={"agent_name": agent_name, "query": query, "result": result.get('output')})
        LANGCHAIN_AGENT_CALLS_TOTAL.labels(agent_name=agent_name, status='success').inc()
        print(f"\n--- Agent Result for '{query}' ---")
        print(result.get('output'))
        print("-----------------------------------\n")
        return result
    except Exception as e:
        logger.error(f"Agent '{agent_name}' failed for query: '{query}'", 
                     extra_fields={"agent_name": agent_name, "query": query, "error_type": type(e).__name__},
                     exc_info=True)
        LANGCHAIN_AGENT_CALLS_TOTAL.labels(agent_name=agent_name, status='failure').inc()
        print(f"\n--- Agent Failed for '{query}' ---")
        print(f"Error: {e}")
        print("-----------------------------------\n")
        return {"output": "I'm sorry, I encountered an error and cannot fulfill your request."}

# --- Test Cases ---
run_agent_with_handling("What is 100 divided by 4?")
run_agent_with_handling("What is 50 divided by 0?") # This should trigger an error in the tool
run_agent_with_handling("Tell me a story.") # Agent might not use the tool, but still runs
run_agent_with_handling("Calculate 7 divided by 2.")

# To see Prometheus metrics, you would typically run a separate server
# or have your main application expose them. For demonstration:
# print("\n--- Current Prometheus Metrics (for demonstration) ---")
# print(generate_latest().decode('utf-8'))
# print("----------------------------------------------------\n")
```

This example shows:
*   **Structured logging:** Using `JsonFormatter` to make logs machine-readable.
*   **Log levels:** Using `INFO` for normal flow and `ERROR` for exceptions.
*   **Error handling:** The `try-except` block around the tool call and the agent invocation.
*   **Metrics:** Simple counters for agent and tool calls, helping `monitoring error rates`.
*   **`exc_info=True`:** Ensuring full stack traces are captured for errors.

This approach gives you a clear audit trail and measurable data about your LangChain agent's performance and failures. It's a key part of `langchain error logging monitoring best practices`.

### Example 2: Catching Errors in a Chain

If you're using LangChain chains, you can also wrap their execution in `try-except` blocks.

```python
import logging
import sys
import json
import datetime
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import OpenAI # or from langchain_openai import OpenAI
import os

# --- Logger Setup (reusing our JSON formatter) ---
logger = logging.getLogger('langchain_chain_app')
logger.setLevel(logging.INFO)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            **getattr(record, 'extra_fields', {})
        }
        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

# --- Define Prometheus Metrics for Chains ---
from prometheus_client import Counter
LANGCHAIN_CHAIN_CALLS_TOTAL = Counter(
    'langchain_chain_calls_total',
    'Total number of LangChain chain calls.',
    ['chain_name', 'status']
)

# --- Set up a simple LangChain Chain ---
llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-your-openai-key-here"))
prompt = PromptTemplate.from_template("Tell me a very short story about {topic}.")
story_chain = LLMChain(llm=llm, prompt=prompt)

# --- Function to run the chain with error handling, logging, and metrics ---
def run_story_chain(topic: str):
    chain_name = "StoryGeneratorChain"
    logger.info(f"Attempting to generate story for topic: '{topic}'", 
                extra_fields={"chain_name": chain_name, "topic": topic})
    LANGCHAIN_CHAIN_CALLS_TOTAL.labels(chain_name=chain_name, status='attempt').inc()
    try:
        # Simulate an LLM error if the topic is 'error'
        if topic.lower() == "error":
            raise ValueError("LLM token limit exceeded or API error simulated!")

        result = story_chain.invoke({"topic": topic})
        story = result.get('text', 'No story generated.')
        logger.info(f"Story generated successfully for topic: '{topic}'", 
                    extra_fields={"chain_name": chain_name, "topic": topic, "story_length": len(story)})
        LANGCHAIN_CHAIN_CALLS_TOTAL.labels(chain_name=chain_name, status='success').inc()
        print(f"\n--- Story for '{topic}' ---")
        print(story)
        print("----------------------------\n")
        return story
    except Exception as e:
        logger.error(f"Failed to generate story for topic: '{topic}'", 
                     extra_fields={"chain_name": chain_name, "topic": topic, "error_type": type(e).__name__},
                     exc_info=True)
        LANGCHAIN_CHAIN_CALLS_TOTAL.labels(chain_name=chain_name, status='failure').inc()
        print(f"\n--- Story Generation Failed for '{topic}' ---")
        print(f"Error: {e}")
        print("---------------------------------------------\n")
        return "I'm sorry, I couldn't generate a story for that topic."

# --- Test Cases ---
run_story_chain("a brave knight")
run_story_chain("error") # This should simulate a failure
run_story_chain("a fluffy cat")
```

This snippet reinforces the `langchain error logging monitoring best practices` for chains. Every invocation is logged, potential errors are caught and logged with full details, and simple metrics track the chain's overall health.

## Choosing the Right Tools for Your LangChain Setup

Selecting the best `log management solutions`, `metrics platforms`, and `alerting services` depends on your team's size, budget, technical skills, and compliance requirements.

Here's a quick comparison:

| Feature                   | Small Project (Solo/Small Team)                       | Medium Project (Growing Startup)                      | Large Project (Enterprise)                               |
| :------------------------ | :---------------------------------------------------- | :---------------------------------------------------- | :------------------------------------------------------- |
| **Logging**               | Python `logging` to file/console                      | ELK Stack (self-hosted), Grafana Loki, CloudWatch Logs | Splunk, Datadog, ELK Stack (managed), Sumologic          |
| **Metrics**               | Basic custom counters, Prometheus + Grafana (simple)  | Prometheus + Grafana, Datadog (basic metrics)         | Datadog, New Relic, Dynatrace, Cloud Monitoring          |
| **Alerting**              | Email, Slack webhooks                                 | Grafana Alerting, Opsgenie, PagerDuty (starter)       | PagerDuty, VictorOps, dedicated `SIEM tools` if security critical |
| **Observability**         | Manual correlation of logs/metrics                    | Datadog, basic OpenTelemetry                          | Full APM solutions (Datadog, New Relic), OpenTelemetry with advanced backends |
| **Ease of Setup**         | High                                                  | Medium                                                | Low (requires specialized knowledge)                     |
| **Cost**                  | Free/Low                                              | Moderate                                              | High                                                     |

For `log management solutions`, if you are just starting, simple file logging is fine. But as your application grows, moving to `centralized logging` with tools like ELK, Datadog, or Splunk becomes essential. These platforms offer powerful `log analysis techniques`.

When it comes to `metrics platforms`, Prometheus and Grafana are excellent open-source choices that give you a lot of control. Cloud-based solutions like Datadog provide ease of use and integrated `observability setup`.

Finally, for `alerting strategies`, make sure your alerts are actionable. Use services like PagerDuty for critical incidents that require immediate human intervention. You can also integrate alerts with your team's communication tools, such as Slack.

### Further Reading

Ensure your LangChain applications are robust and reliable:

- [LangChain Performance Tuning 2026](/langchain-performance-tuning-2026/)
- [Deploy LangChain Production 2026](/deploy-langchain-production-2026/)
- [LangChain Streaming Responses Tutorial 2026](/langchain-streaming-responses-2026/)
- [LangChain Cost Optimization 2026](/langchain-cost-optimization-2026/)
- [LangChain Tools Agents 2026: Production-Ready Patterns](/langchain-tools-agents-2026/)

## Conclusion

Mastering `langchain error logging monitoring best practices` is not just a technical task; it's about making your AI applications reliable, understandable, and manageable. By carefully logging information, collecting relevant metrics, and setting up smart alerts, you empower yourself to diagnose issues quickly and keep your LangChain applications running smoothly.

Remember to embrace `structured logging` to make your logs easy to read by both humans and machines. Use appropriate `log levels configuration` to filter noise. Employ `centralized logging` and `log aggregation` to bring all your data into one place for effective `log analysis techniques`. And don't forget `monitoring error rates` and `alerting strategies` to be proactive when problems arise.

Investing in a good `observability setup` for your LangChain projects will pay off immensely as they grow in complexity and importance. Start simple, and gradually add more sophisticated tools and practices as your needs evolve. Happy building with LangChain!