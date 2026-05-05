---
title: "LangSmith Tracing Deep Dive: How to Inspect Runs, Traces and Token Usage in LangChain"
description: "Inspect your LangChain apps with LangSmith tracing. Learn to deeply analyze runs, traces, and crucial token usage for optimized performance and cost."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangSmith tracing LangChain]
featured: false
image: '/assets/images/langsmith-tracing-deep-dive-runs-traces-token-usage.webp'
---

## LangSmith Tracing Deep Dive: How to Inspect Runs, Traces and Token Usage in LangChain

Have you ever wondered what exactly happens inside your smart AI application? Building tools with LangChain can feel a bit like magic sometimes. You create powerful agents and chains, but understanding their step-by-step journey can be tricky.

This is where LangSmith tracing LangChain comes into play. It's like a special X-ray machine that lets you see everything. It helps you understand, debug, and improve your AI apps. Today, we will take a deep dive into how to use LangSmith to inspect runs, traces, and even track token usage.

### Getting Started with LangSmith Tracing in LangChain

Before we begin our deep dive, you need to set up LangSmith. It's super easy to connect it to your LangChain projects. You just need to set a few special keys and tell LangChain where to send its logs.

First, you need to sign up for LangSmith and get your API key. Once you have it, you can set it as an environment variable on your computer. This tells LangChain how to connect.

{% raw %}
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
os.environ["LANGCHAIN_PROJECT"] = "LangSmith Tracing Deep Dive" # Your project name
```
{% endraw %}

With these settings, LangChain will automatically start sending information to LangSmith. Every time your LangChain code runs, LangSmith records it. This makes LangSmith tracing LangChain a seamless experience.

Let's look at a simple example. We will ask an AI model a basic question.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Make sure you have your OpenAI API key set too!
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Define our AI model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Create a simple prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{question}")
])

# Create a simple chain
chain = prompt | llm

# Invoke the chain
response = chain.invoke({"question": "What is the capital of France?"})
print(response.content)
```
{% endraw %}

After running this code, a "run" is sent to LangSmith. You can then visit the LangSmith UI to see exactly what happened. This simple step is the start of powerful `run inspection`.

### Understanding the LangSmith UI: Your Control Center

The LangSmith UI is where all the magic happens for `LangSmith tracing LangChain`. It's a dashboard designed to show you what your AI applications are doing. When you log in, you'll see a list of your projects and recent runs.

Each entry on this dashboard represents a single "run" of your LangChain application. You can quickly see its name, when it happened, and if it finished successfully. This quick overview is very helpful for spotting problems.

To truly understand what's going on, you'll want to click on a specific run. This opens up a detailed view where you can explore everything. This is your main area for effective `run inspection`.

You can filter runs by project, time, status, and even custom tags. This helps you find exactly what you're looking for, even in busy projects. It makes managing many runs much easier.

### Deep Dive into Runs and Traces

Let's talk about "runs" and "traces" in more detail. Think of a "run" as a single action taken by a part of your LangChain app. For example, calling an LLM, using a tool, or applying a custom parser is each a run.

A "trace" is like a complete story of your application's journey. It's a collection of many related runs that show how everything connects. When your LangChain agent thinks, uses a tool, and then calls an LLM, all these steps form one big trace.

When you click on a run in the LangSmith UI, you usually see the full `trace hierarchy`. This hierarchy shows how different parts of your application call each other. It's presented like a tree, with the main process at the top and smaller steps branching out.

This hierarchical view is very powerful for understanding complex applications. For instance, if you're building a multi-step AI agent with LangGraph, you can see how each state transition and action contributes to the overall process. This kind of detailed view helps you understand the flow, as discussed in [Building Multi-Step AI Agents with LangGraph's StateGraph]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

Let's look at a slightly more complex example with a LangChain expression language (LCEL) chain. This will create a richer `trace hierarchy`.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Assume environment variables are set from before

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
parser = StrOutputParser()

# Define a chain that summarizes input and then asks a question
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following text in one sentence."),
    ("user", "{text}")
])

question_prompt = ChatPromptTemplate.from_messages([
    ("system", "Based on the summary: {summary}\nAnswer the question: {question}"),
    ("user", "Answer this: {final_question}")
])

# First part of the chain: summarize
summary_chain = {"text": lambda x: x["document"]} | summarize_prompt | llm | parser

# Second part of the chain: ask question based on summary
full_chain = {
    "summary": summary_chain,
    "final_question": lambda x: x["question"],
    "question": lambda x: x["question"]
} | question_prompt | llm | parser

# Invoke the full chain
response = full_chain.invoke({
    "document": "LangChain is an open-source framework designed to simplify the creation of applications using large language models. It provides tools and abstractions to make it easier to chain together different LLM components, integrate with external data sources, and build complex agentic workflows. LangSmith is a platform for debugging, testing, and monitoring LangChain applications.",
    "question": "What is LangSmith?"
})
print(response)
```
{% endraw %}

When you view this in LangSmith, you'll see a root run for `full_chain`. Inside it, you'll find a nested run for `summary_chain`. Inside `summary_chain`, you'll see the `summarize_prompt`, the `ChatOpenAI` call, and the `StrOutputParser`. This detailed view makes `run inspection` incredibly clear.

### Inspecting Individual Spans and Steps

Every single step in your LangChain application, from a prompt template to an LLM call or a custom tool, is recorded as a "span" in LangSmith. Think of a span as a tiny, detailed record of one action. This process is called `span tracing`.

When you view a trace in the LangSmith UI, you can click on any individual span. This will open up a panel showing all the details for that specific action. You'll see the inputs that went into that step, the outputs it produced, and importantly, any errors that might have occurred.

For example, if you have a chain that uses a custom output parser, you can inspect that specific parser's span. You can see exactly what text it received and what structured data it tried to create. This is super useful for debugging custom components, as highlighted in [Building a Custom Output Parser in LangChain]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}).

Let's make a chain with a custom function to demonstrate `span tracing`. We'll just define a simple custom function that acts as a step.

{% raw %}
```python
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Assume environment variables are set

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
parser = StrOutputParser()

# A custom step that capitalizes the input
def capitalize_text(text: str) -> str:
    print(f"Capitalizing: {text}") # This print will show up in your local console, but LangSmith captures input/output
    return text.upper()

# Create a RunnableLambda for our custom step
capitalizer_step = RunnableLambda(capitalize_text)

# Define a simple chain: prompt -> capitalize -> llm -> parse
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Explain the meaning of: {text}")
])

chain_with_custom_step = prompt | capitalizer_step | llm | parser

# Invoke the chain
response = chain_with_custom_step.invoke({"text": "hello world"})
print(response)
```
{% endraw %}

In LangSmith, you'll see a span for `capitalizer_step`. When you click on it, you'll observe "hello world" as its input and "HELLO WORLD" as its output. If `capitalize_text` had an error, you would see that error detailed within its span, making debugging much easier.

### Uncovering Token Usage and Costs

One of the most valuable features of `LangSmith tracing LangChain` is its ability to track `token counting`. Every time your application interacts with a Large Language Model (LLM), it uses "tokens." Tokens are like the basic building blocks of language that LLMs understand, similar to words or parts of words.

These tokens cost money. Knowing how many tokens your application uses is essential for managing your budget and understanding efficiency. LangSmith automatically records the number of input tokens and output tokens for every LLM call.

When you inspect an LLM call span in the LangSmith UI, you'll see a section dedicated to token usage. It usually shows `Prompt Tokens`, `Completion Tokens`, and `Total Tokens`. This gives you a clear picture of the consumption for that specific interaction.

LangSmith can even help you estimate the cost of your runs based on the token usage and the model prices. This feature is crucial for optimizing your applications, especially when building advanced RAG (Retrieval-Augmented Generation) systems. For RAG applications, where you might query a vector store and then use an LLM, `token counting` helps you manage the costs of both the retrieval and generation phases. You can learn more about building RAG applications in [Build RAG Applications with LangChain and Vector Stores in 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

Let's modify our previous example to explicitly show `token counting` with a slightly longer input.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Assume environment variables are set

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
parser = StrOutputParser()

long_text = """
The quick brown fox jumps over the lazy dog. This is a classic pangram, 
a sentence that contains every letter of the alphabet at least once. 
Pangrams are often used to display typefaces and for typing practice. 
They are also fun linguistic puzzles.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the following text and explain its purpose."),
    ("user", "{text}")
])

# Create a simple chain
analysis_chain = prompt | llm | parser

# Invoke the chain with the longer text
response = analysis_chain.invoke({"text": long_text})
print(response)
```
{% endraw %}

In the LangSmith UI, navigate to the `ChatOpenAI` span within this trace. You will clearly see the prompt tokens used for `long_text` and the system message, along with the completion tokens for the AI's response. This direct `token counting` helps you understand the economic impact of your prompts and model outputs.

### Tracking Performance: Latency and Time

Beyond tokens and costs, understanding how fast your application runs is super important. `Latency tracking` is another powerful feature of `LangSmith tracing LangChain`. It measures how long each step and the overall trace takes to complete.

When you look at a trace in LangSmith, you'll often see timing information next to each span. This tells you exactly how much time was spent on that particular action. The UI also provides a visual timeline view, showing you which steps ran in parallel and which took the longest.

Identifying slow parts of your application, also known as "bottlenecks," is much easier with `latency tracking`. For instance, if you notice your database lookup is consistently taking too long in a RAG system, you know where to focus your optimization efforts. This is especially relevant when dealing with scalable RAG architectures, as discussed in [LangChain Weaviate Hybrid Search for Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

Let's create a chain that simulates a slow operation to see `latency tracking` in action. We'll add a short delay.

{% raw %}
```python
import time
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Assume environment variables are set

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
parser = StrOutputParser()

# A custom step that simulates a delay (e.g., an external API call)
def simulate_slow_operation(input_text: str) -> str:
    print(f"Starting slow operation for: {input_text}")
    time.sleep(2) # Simulate a 2-second delay
    print("Slow operation finished.")
    return f"Processed: {input_text}"

# Create a RunnableLambda for our simulated slow step
slow_step = RunnableLambda(simulate_slow_operation)

# Define a chain: prompt -> slow_step -> llm -> parse
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "Summarize this processed text: {text}")
])

chain_with_slow_step = {"text": lambda x: x["query"]} | slow_step | prompt | llm | parser

# Invoke the chain
response = chain_with_slow_step.invoke({"query": "AI advancements"})
print(response)
```
{% endraw %}

In the LangSmith UI, when you examine the trace for `chain_with_slow_step`, you'll clearly see the `simulate_slow_operation` span with a duration of approximately 2 seconds. This immediate visual feedback from `latency tracking` helps you pinpoint exactly where your application spends most of its time. Such insights are invaluable for optimizing performance.

### Filtering and Organizing Your Runs

As you develop more complex LangChain applications, you'll generate many runs. Finding specific runs or comparing different versions can become challenging. LangSmith provides excellent tools for filtering and organizing your data. This is key for effective `run inspection`.

You can add "tags" to your runs to categorize them. For example, you might tag runs as `test`, `production`, `experiment-A`, or `prompt-v2`. This allows you to quickly filter your dashboard to see only runs related to a specific category.

Naming your runs thoughtfully also makes a big difference. Instead of generic names, give them descriptive labels like `summarization-agent-v1`, `rag-query-test`, or `gemini-function-call-attempt`. This helps you immediately understand the purpose of each run when you're browsing the `LangSmith UI`. For agents that use function calling, meaningful run names can help track different tool uses, as explored in [LangChain Google Gemini Function Calling Agent with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

You can also attach custom metadata to your runs. This lets you store extra information relevant to that specific execution, such as user IDs, specific input parameters, or experiment configurations. This metadata is searchable, providing even more powerful filtering options.

Let's see how to add tags and custom names to our runs.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig

# Assume environment variables are set

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly chatbot."),
    ("user", "Tell me a fun fact about {topic}.")
])

fun_fact_chain = prompt | llm | parser

# Define a config for our run, including a name and tags
config = RunnableConfig(
    run_name="FunFactGenerator-Experiment-A",
    tags=["fun-facts", "experiment-A", "test-run"]
)

# Invoke the chain with the custom config
response = fun_fact_chain.invoke({"topic": "cats"}, config=config)
print(response)

# Another run with different tags
config_v2 = RunnableConfig(
    run_name="FunFactGenerator-Experiment-B",
    tags=["fun-facts", "experiment-B", "production-candidate"]
)
response_v2 = fun_fact_chain.invoke({"topic": "dogs"}, config=config_v2)
print(response_v2)
```
{% endraw %}

In the `LangSmith UI`, you can now use the filter bar to search for runs tagged with "experiment-A" or "production-candidate". You'll also easily spot runs named "FunFactGenerator-Experiment-A" in your list. This organized approach greatly improves your ability to perform efficient `run inspection`.

### Advanced Tracing Techniques

Moving beyond basic tracing, LangSmith offers more advanced ways to customize your `LangSmith tracing LangChain` experience. These techniques give you even finer control over what data is recorded and how it's presented.

One useful technique is to dynamically set run names based on your inputs or logic. Instead of a static name, you can make the run name reflect what the chain is doing. For instance, `Agent-Query: {user_query}` helps immediately understand the purpose of a particular agent run.

Adding custom metadata not just at the top-level run but also to individual spans can provide deeper context. Imagine you have a RAG system; you could add metadata to the retrieval span that includes the specific documents retrieved or the score of the similarity search. This enriches the `span tracing` data immensely.

LangSmith is also excellent for comparing different runs or "experiments." You can set up parallel runs with slightly different prompts, models, or chain configurations and easily compare their performance, token usage, and outputs side-by-side. This is crucial for A/B testing and iterating on your AI applications. For example, comparing different semantic text splitters could be an interesting experiment, as explored in [LangChain Semantic Text Splitter: Chunk by Meaning]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}).

Here's an example of adding custom metadata to a run.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig

# Assume environment variables are set

llm_model_A = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
llm_model_B = ChatOpenAI(model="gpt-4", temperature=0.7) # Using a different model for comparison
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "What is the capital of {country}?")
])

chain_A = prompt | llm_model_A | parser
chain_B = prompt | llm_model_B | parser

# Run with Model A and custom metadata
config_A = RunnableConfig(
    run_name="CapitalQuery-ModelA",
    tags=["model-comparison", "gpt-3.5-turbo"],
    metadata={"user_id": "user123", "version": "v1.0", "temperature": 0.7}
)
response_A = chain_A.invoke({"country": "Germany"}, config=config_A)
print(f"Model A: {response_A}")

# Run with Model B and different custom metadata
config_B = RunnableConfig(
    run_name="CapitalQuery-ModelB",
    tags=["model-comparison", "gpt-4"],
    metadata={"user_id": "user123", "version": "v1.0", "temperature": 0.7, "cost_priority": "high"}
)
response_B = chain_B.invoke({"country": "Germany"}, config=config_B)
print(f"Model B: {response_B}")
```
{% endraw %}

In LangSmith, you can now compare these two runs side-by-side. You'll see their respective run names, tags, and critically, the custom metadata you attached. This allows for deep analysis during `run inspection`, helping you make informed decisions about your model choices and configurations.

### Troubleshooting and Debugging with LangSmith

LangSmith is an incredibly powerful tool for troubleshooting your LangChain applications. When something goes wrong, instead of guessing, you can use `LangSmith tracing LangChain` to pinpoint the exact issue.

Common issues like incorrect prompt formatting, unexpected outputs from tools, or errors in custom logic become much easier to spot. You can quickly see which `span tracing` step failed, what its inputs were, and the error message it produced. This significantly speeds up the debugging process.

For instance, if your agent is stuck in a loop or produces irrelevant outputs, you can follow its `trace hierarchy` step by step. You might discover that a tool is returning unexpected data, or the LLM is misinterpreting the prompt. This helps you refine your prompts, adjust tool definitions, or fix bugs in your custom code.

Debugging complex agents, especially those involving multiple steps and conditional logic, can be a headache without proper tools. LangSmith makes it much simpler to understand why an agent chose a particular path or failed to complete a task. This is particularly useful for debugging stateful agents built with tools like LangGraph, as discussed in [Building Multi-Step AI Agents with LangGraph's StateGraph]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

Let's create an example that could potentially lead to an error or an unexpected output, and then see how LangSmith helps us debug it.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.exceptions import OutputParserException # Import for example

# Assume environment variables are set

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
parser = StrOutputParser()

# A custom "tool" that might sometimes fail or return unexpected format
def process_data_tool(input_data: str) -> str:
    if "error" in input_data.lower():
        # Simulate a tool error
        raise ValueError("Simulated processing error with 'error' keyword.")
    if "complex_data" in input_data.lower():
        # Simulate a complex, possibly problematic output
        return "SUCCESS::DATA_XYZ_123::status=processed"
    return f"Processed simple: {input_data}"

# Runnable for our custom tool
data_tool_runnable = RunnableLambda(process_data_tool)

# Define a chain: user input -> custom tool -> LLM to interpret result
prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the following tool output and give a simple summary."),
    ("user", "{tool_output}")
])

debugging_chain = {"tool_output": data_tool_runnable} | prompt | llm | parser

print("--- Running first scenario (simple) ---")
try:
    response_simple = debugging_chain.invoke({"input_data": "some regular data"})
    print(f"Simple response: {response_simple}")
except Exception as e:
    print(f"Simple scenario error: {e}")

print("\n--- Running second scenario (error) ---")
try:
    response_error = debugging_chain.invoke({"input_data": "trigger an error"})
    print(f"Error response: {response_error}")
except Exception as e:
    print(f"Error scenario error: {e}")

print("\n--- Running third scenario (complex output) ---")
try:
    response_complex = debugging_chain.invoke({"input_data": "complex_data"})
    print(f"Complex response: {response_complex}")
except Exception as e:
    print(f"Complex scenario error: {e}")
```
{% endraw %}

In the `LangSmith UI`, for the "error" scenario, you'll see the trace marked as failed. Clicking into the `data_tool_runnable` span will reveal the exact `ValueError` with its traceback. For the "complex output" scenario, you can inspect the input to the `ChatOpenAI` call and see if the LLM correctly interpreted "SUCCESS::DATA_XYZ_123::status=processed". This hands-on `span tracing` directly shows you the issue.

### Best Practices for Effective LangSmith Tracing

To get the most out of `LangSmith tracing LangChain`, it's helpful to follow a few best practices. These tips will ensure your traces are clear, useful, and easy to work with.

1.  **Trace All Significant Components:** Make sure all custom tools, important functions, and every part of your chain are being tracked. If a step isn't traced, you have a blind spot. LangSmith usually does this automatically for LangChain components, but custom functions might need to be wrapped in `RunnableLambda` or similar.

2.  **Use Descriptive Run Names:** As we discussed, clear run names make `run inspection` much easier. Instead of generic names, give your runs names that explain their purpose or the query they are processing. This helps you quickly locate relevant traces in the `LangSmith UI`.

3.  **Leverage Tags and Metadata:** Use tags to categorize your runs (e.g., `prod`, `dev`, `test`, `experiment-A`). Metadata can hold specific details about a run, like user IDs, version numbers, or specific parameters. These are powerful for filtering and comparing.

4.  **Regularly Review Traces for Performance and Cost:** Don't just trace when things break. Periodically check your `token counting` and `latency tracking` for your most common workflows. You might discover unexpected costs or performance bottlenecks that you can optimize. This is especially true as you scale your applications. While LangSmith is great, sometimes you might also consider [top LangChain alternatives]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}) to compare features if specific needs arise beyond LangSmith's scope.

5.  **Add Feedback to Runs:** LangSmith allows you to add feedback (like a thumbs up or down) to runs. This is great for marking good or bad responses, which can then be used to filter and analyze your application's quality over time. You can even use this feedback to create datasets for fine-tuning.

6.  **Integrate LangSmith into Your Testing Pipeline:** Use LangSmith to monitor your integration tests. This allows you to automatically check if changes to your prompts or code introduce new errors or performance regressions. Every test run can become a trace.

By adopting these practices, you'll transform LangSmith from a simple debugging tool into a comprehensive observability platform for your LangChain applications. It helps you understand, debug, and continuously improve your AI workflows.

### Conclusion

You've now taken a deep dive into `LangSmith tracing LangChain`, exploring its powerful capabilities. We've seen how to inspect runs, understand the `trace hierarchy`, and drill down into individual `span tracing` steps. You also learned the importance of `token counting` for cost management and `latency tracking` for performance optimization.

The `LangSmith UI` acts as your control center for all this valuable information, making `run inspection` intuitive and efficient. By following best practices, you can make LangSmith an indispensable part of your LangChain development workflow. Start integrating LangSmith today to gain unparalleled visibility into your AI applications and build even better, more reliable, and cost-effective solutions.