---
title: "Build Your First AI Agent in Python with LangChain: A Step-by-Step Guide"
description: "Learn to build your first LangChain AI Agent in Python. Our step-by-step guide helps developers create powerful, intelligent AI agents today."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: ["LangChain", "Python", "AI Agents", "LLM", "Tutorial"]
featured: false
image: '/assets/images/build-langchain-ai-agent-python.webp'
---
## Build Your First AI Agent in Python with LangChain: A Step-by-Step Guide

**Code Your Own AI Agent**

The field of artificial intelligence is rapidly evolving, and Large Language Models (LLMs) are at its forefront. While LLMs are powerful, their true potential is unlocked when they can act autonomously, interact with their environment, and solve multi-step problems. This is where the concept of an **LangChain AI Agent** comes into play.

This comprehensive guide will walk you through building your very first intelligent agent using Python and LangChain, a leading framework for [Python AI development]({% post_url 2026-11-15-langchain-python-complete-guide %}). You will learn the core components, understand agentic workflows, and implement a practical example step-by-step. By the end, you will have a runnable **LLM agent** capable of making decisions and utilizing tools to achieve its goals.

### What are AI Agents and Why LangChain?

An AI agent, in the context of Large Language Models, is a system that can reason, plan, and execute actions to achieve a specific objective. Unlike simple LLM chains that follow a predefined sequence of steps, an **LLM agent** exhibits autonomy. It can dynamically decide which tools to use and in what order, based on the current situation and its understanding of the problem.

LangChain provides a robust and flexible framework for building these sophisticated **autonomous agents**. It abstracts away much of the complexity, allowing you to focus on defining the agent's capabilities and goals. This makes LangChain an excellent choice for getting started with **agentic workflows**.

#### Agent vs. Chain: A Quick Comparison

It's important to understand the fundamental difference between a traditional LangChain "chain" and an "agent." This distinction highlights the power and flexibility that **LangChain AI Agents** offer.

| Feature         | LLM Chain                                   | LLM Agent (LangChain AI Agent)                           |
| :-------------- | :------------------------------------------ | :------------------------------------------------------- |
| **Logic Flow**  | Predefined, sequential, hardcoded           | Dynamic, decided by the LLM's reasoning                  |
| **Decision-making** | No internal decision-making beyond prompt | LLM decides actions, tools, and next steps               |
| **Tool Usage**  | Tools are called explicitly in sequence     | LLM chooses which tool to call and when                  |
| **Complexity**  | Simpler, good for fixed workflows           | More complex, handles multi-step, uncertain problems     |
| **Autonomy**    | Low                                         | High, goal-oriented                                      |
| **Use Cases**   | Summarization, fixed Q&A, sentiment analysis | Complex problem-solving, data analysis, interactive tasks |

### Understanding the Core Components of a LangChain AI Agent

Before we dive into coding, let's break down the essential building blocks of any **LangChain AI Agent**. These components work together to enable intelligent and adaptive behavior.

1.  **Large Language Model (LLM):** This is the brain of your agent. The LLM is responsible for understanding the prompt, reasoning about the problem, and deciding on the next action. It interprets observations and formulates responses or further tool calls.

2.  **Tools:** These are functions or APIs that the agent can call to interact with the external world. Tools provide your agent with capabilities beyond pure language generation. Examples include web search, calculators, database queries, or custom API integrations. **Tool calling** is a crucial aspect of **LLM agents**. For a deeper dive, check out our guide on [LangChain Tool Calling for AI Agents]({% post_url 2026-11-16-langchain-tool-calling-ai-agents %}).

3.  **Agent Executor:** This is the runtime that orchestrates the agent's behavior. It manages the loop of thought, action, and observation. The executor receives the LLM's decision (what tool to use and with what input), executes the tool, and feeds the observation back to the LLM for the next turn.

4.  **Prompt:** The prompt is the instruction given to the LLM, guiding its behavior. It typically includes the agent's role, available tools, and the goal. Effective prompting is key to building intelligent **autonomous agents**.

5.  **Memory (Optional but Recommended):** For agents to maintain context over multiple turns, memory is essential. It allows the agent to remember past interactions, decisions, and observations, leading to more coherent and intelligent conversations or task completion.

### Setting Up Your Development Environment

To begin building your **Python LLM agent**, you'll need a clean Python environment. We recommend using `venv` or `conda` to manage your dependencies.

#### Step 1: Create a Virtual Environment

Open your terminal or command prompt and run the following commands:

```bash
python -m venv ai_agent_env
source ai_agent_env/bin/activate # On Windows, use `ai_agent_env\Scripts\activate`
```

This creates and activates a new virtual environment named `ai_agent_env`. All subsequent package installations will be isolated within this environment.

#### Step 2: Install Required Libraries

Next, install LangChain and a suitable LLM provider. We'll use OpenAI for this tutorial due to its widespread adoption and strong performance. You'll also need `duckduckgo_search` for a basic web search tool.

```bash
pip install langchain langchain-openai duckduckgo-search
```

#### Step 3: Configure API Keys


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2784742237479601"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2784742237479601"
     data-ad-slot="7340313511"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>


You'll need an OpenAI API key to access their models. Set it as an environment variable for security and convenience.

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

Replace `"your_openai_api_key_here"` with your actual OpenAI API key. On Windows, use `set OPENAI_API_KEY="your_openai_api_key_here"`.

### Building Your First LangChain AI Agent: A Step-by-Step Guide

Now, let's dive into the code and construct a simple yet powerful **LangChain AI Agent**. This agent will be able to perform calculations and search the web to answer questions.

#### Step 1: Initialize the Large Language Model (LLM)

First, we need to instantiate our LLM. We'll use OpenAI's `gpt-4o` model for its strong reasoning capabilities.

```python
# ai_agent_tutorial.py
from langchain_openai import ChatOpenAI

# Initialize the LLM
# You can choose other models like "gpt-3.5-turbo" if you prefer.
llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

Here, `temperature=0` encourages deterministic and factual responses, which is often desirable for agents performing tasks.

#### Step 2: Define the Tools for Your Agent

Tools are the hands and feet of your **LLM agent**, allowing it to interact with the outside world. For our first agent, we'll implement a simple calculator and a web search tool.

```python
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Define a calculator tool
@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.
    Use this tool to solve arithmetic problems.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error evaluating expression: {e}"

# Define a web search tool
search = DuckDuckGoSearchRun()

# Group all tools
tools = [calculator, search]
```

In this snippet:
- We use `@tool` decorator from `langchain_core.tools` to easily convert a Python function into a LangChain tool. This function, `calculator`, takes a string `expression` and evaluates it.
- `DuckDuckGoSearchRun()` provides a convenient way to integrate web search capabilities.
- We collect all our defined tools into a `tools` list. These are the external functionalities our **autonomous agent** can leverage.

#### Step 3: Create the LangChain AI Agent

LangChain offers different types of agents, with `create_tool_calling_agent` being a modern and highly recommended approach. This function leverages the LLM's native **tool calling** capabilities.

```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

# Define the prompt template for the agent
# This system message instructs the LLM on its role and capabilities.
system_message = SystemMessage(
    content=(
        "You are a helpful AI assistant. You have access to the following tools: {tools}. "
        "Your goal is to answer the user's questions truthfully and accurately. "
        "If a question requires calculation or information from the web, use the appropriate tool. "
        "Always respond concisely and directly to the user's query."
    )
)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message.content),
        ("placeholder", "{chat_history}"), # For memory, though not yet implemented here
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"), # Where agent's thoughts and tool outputs go
    ]
)

# Create the agent
# The create_tool_calling_agent is optimized for LLMs with native tool-calling abilities.
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the AgentExecutor
# The executor manages the agent's logic loop (thought-action-observation).
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

Here's what each part does:
- `system_message`: This crucial part of the prompt tells the **LangChain AI Agent** about its identity, goals, and the tools it possesses. Good system prompts are vital for effective **LLM agents**.
- `ChatPromptTemplate`: We use a `ChatPromptTemplate` to structure our prompts, which is standard for conversational models.
- `create_tool_calling_agent`: This function assembles the core agent logic, connecting the LLM, tools, and prompt. It specifically utilizes the LLM's native ability to parse tool calls.
- `AgentExecutor`: This is the engine that runs the agent. `verbose=True` is incredibly useful for debugging, as it shows the agent's internal thought process, tool calls, and observations. This helps you understand how your **Python LLM agent** makes decisions.

#### Step 4: Run Your First LangChain AI Agent

Now that everything is set up, let's put our **autonomous agent** to the test!

```python
# Run the agent with some queries
print("--- Query 1: Simple Calculation ---")
response_1 = agent_executor.invoke({"input": "What is 1234 * 5678?"})
print(response_1["output"])


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2784742237479601"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2784742237479601"
     data-ad-slot="7340313511"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>


print("\n--- Query 2: Web Search ---")
response_2 = agent_executor.invoke({"input": "What is the capital of France?"})
print(response_2["output"])

print("\n--- Query 3: Combined Task ---")
response_3 = agent_executor.invoke({"input": "What is the current population of Tokyo, and what is 500 divided by 25?"})
print(response_3["output"])

print("\n--- Query 4: Unanswerable without external tools ---")
response_4 = agent_executor.invoke({"input": "Tell me a joke."})
print(response_4["output"]) # Expect LLM to answer directly without tools
```

When you run this code, you'll see the `verbose=True` output, showing the agent's "thought," "action," and "observation" steps. This provides invaluable insight into how your **LangChain AI Agent** reasons and utilizes its tools.

Example output for a query (simplified, actual output will be verbose):

```
--- Query 1: Simple Calculation ---
> Entering new AgentExecutor chain...
Thought: The user is asking for a mathematical calculation. I should use the `calculator` tool to solve this.
Action:
```
{% raw %}
```json
{
  "tool_code": "calculator",
  "tool_input": "1234 * 5678"
}
```
{% endraw %}
Observation: 7006652
Thought: I have successfully calculated the result. Now I will respond to the user.
Action:
```
{% raw %}
```json
{
  "tool_code": "final_answer",
  "tool_input": "7006652"
}
```
{% endraw %}
> Finished chain.
7006652

--- Query 2: Web Search ---
> Entering new AgentExecutor chain...
Thought: The user is asking for factual information about the capital of France. I should use the `DuckDuckGoSearchRun` tool to find this information.
Action:
```
{% raw %}
```json
{
  "tool_code": "search",
  "tool_input": "capital of France"
}
```
{% endraw %}
Observation: Paris is the capital and most populous city of France.
Thought: I have found the capital of France. Now I will respond to the user.
Action:
```
{% raw %}
```json
{
  "tool_code": "final_answer",
  "tool_input": "The capital of France is Paris."
}
```
{% endraw %}
> Finished chain.
The capital of France is Paris.
```

This demonstrates the core of **agentic workflows**: the LLM analyzes the input, decides on an action (which tool to use), executes the tool, observes the result, and then decides on the next action until the goal is achieved.

### Adding Memory to Your LangChain AI Agent

For agents to handle multi-turn conversations or retain context across interactions, they need memory. LangChain provides various memory types, and we'll integrate a simple `ChatMessageHistory` with `RunnableWithMessageHistory` for our agent.

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from collections import defaultdict

# In-memory store for chat histories
# In a real application, this would be a database or persistent store.
store = defaultdict(ChatMessageHistory)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Helper function to retrieve chat history for a given session."""
    return store[session_id]

# Wrap the agent executor with history management
agent_with_memory = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input", # Key for the input messages
    history_messages_key="chat_history", # Key where history will be injected into the prompt
    # The agent_executor already expects 'input' and 'chat_history' as defined in the prompt.
)

# Now, run the agent with memory, specifying a session_id
print("\n--- Query with Memory (Session 1) ---")
response_m1 = agent_with_memory.invoke(
    {"input": "What is 100 * 5?"},
    config={"configurable": {"session_id": "session1"}}
)
print(response_m1["output"])

print("\n--- Query with Memory (Session 1, follow-up) ---")
response_m2 = agent_with_memory.invoke(
    {"input": "And what is that divided by 25?"},
    config={"configurable": {"session_id": "session1"}}
)
print(response_m2["output"])

print("\n--- Query with Memory (Session 2, new session) ---")
response_m3 = agent_with_memory.invoke(
    {"input": "What was the result from the previous conversation?"},
    config={"configurable": {"session_id": "session2"}} # New session, no memory of session 1
)
print(response_m3["output"])
```

With `RunnableWithMessageHistory`, your **Python AI development** now includes conversational memory. The `session_id` allows you to manage different conversations independently. Notice how the agent in `session1` remembers the previous calculation, while `session2` starts fresh. This is a critical enhancement for building useful **intelligent agents**.

### Architecture of a LangChain AI Agent

Visualizing the internal loop helps understand how a **LangChain AI Agent** operates. The `AgentExecutor` is at the heart of this process.

```
+----------------+
|  User Input    |
+-------+--------+
        |
        v
+-------+--------+
|  Agent Executor|
| (Orchestration)|
+-------+--------+
        |
        v
+-------+--------+
|  LLM (Brain)   |
| - Reasons      |
| - Plans        |
| - Decides      |
+-------+--------+
        | (Thought & Action)
        v
+------------------+
| Did LLM request  |
| a Tool?          |
| (e.g., calculator,|
|  search)         |
+--------+---------+
    Yes  |     No (Final Answer)
         v     /
+--------+---------+    +----------------+
| Execute Tool     |    | Output to User |
| (e.g., calculator(expr), |<--------------+
|  search(query))  |
+--------+---------+
         | (Observation/Result)
         v
+--------+---------+
| Feed Observation |
| back to LLM      |
+--------+---------+
         ^
         | (Loop continues until final answer)
```

This cycle of **Thought -> Action -> Observation** is fundamental to **LLM agents**. The `AgentExecutor` tirelessly manages this loop, ensuring your agent can dynamically respond to complex tasks. For building more complex and scalable agents, consider exploring [LangGraph for Scalable Agents]({% post_url 2026-11-15-langgraph-scalable-agents %}), which provides even finer-grained control over these state transitions.

### Expanding Your Agent's Capabilities: Custom Tools and Advanced Features

The real power of **LangChain AI Agents** comes from equipping them with diverse and custom tools. You're not limited to predefined tools; you can wrap any Python function or API call into a tool.

#### Creating a Custom Tool Example

Let's imagine you want your agent to interact with a custom database or internal API.

```python
from langchain_core.tools import tool

@tool
def get_current_stock_price(ticker: str) -> str:
    """Fetches the current stock price for a given stock ticker symbol.
    Input should be a valid stock ticker, e.g., 'AAPL', 'MSFT'.
    """
    # In a real application, this would call an external API
    # For demonstration, we'll return a dummy value
    if ticker.upper() == "AAPL":
        return "AAPL: $175.50"
    elif ticker.upper() == "MSFT":
        return "MSFT: $420.10"
    else:
        return f"Stock price for {ticker.upper()} not found or invalid ticker."


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2784742237479601"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2784742237479601"
     data-ad-slot="7340313511"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>


# Add this new tool to your existing list of tools
tools_with_custom = tools + [get_current_stock_price]

# Re-create the agent executor with the new tools
agent_with_custom_tool = create_tool_calling_agent(llm, tools_with_custom, prompt)
agent_executor_with_custom = AgentExecutor(agent=agent_with_custom_tool, tools=tools_with_custom, verbose=True)

print("\n--- Query with Custom Stock Price Tool ---")
response_stock = agent_executor_with_custom.invoke({"input": "What is the stock price of MSFT?"})
print(response_stock["output"])

print("\n--- Query with Custom Stock Price Tool (Invalid) ---")
response_stock_invalid = agent_executor_with_custom.invoke({"input": "What is the stock price of GOOG?"})
print(response_stock_invalid["output"])
```

By adding `get_current_stock_price`, your agent can now answer questions related to stock prices, demonstrating the extensibility of **LangChain AI Agents**.

#### Observability with LangSmith

As your agents become more complex, debugging and understanding their behavior become crucial. LangChain integrates seamlessly with LangSmith, a platform for **LangChain observability**. LangSmith allows you to trace your agent's execution, inspect tool calls, and analyze LLM inputs and outputs.

To use LangSmith, you'd typically set `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` environment variables. You can then monitor your agent runs directly in the LangSmith UI. This is highly recommended for any serious **Python AI development**. For a detailed guide, refer to the [LangChain Observability with LangSmith tutorial]({% post_url 2026-11-13-langchain-observability-langsmith-tutorial %}).

#### Exploring Agent Types and Prompts

LangChain offers various agent constructors, each optimized for different LLM capabilities and use cases. While `create_tool_calling_agent` is powerful, you might encounter others like `create_react_agent` (for ReAct-style reasoning) or `create_json_agent` (for LLMs that produce JSON actions). The choice depends on your LLM and specific requirements for **agentic workflows**.

The prompt is another area for significant customization and improvement. Experiment with different system messages and few-shot examples to guide your **LLM agent** towards better decision-making and more accurate tool usage. This falls under the broader topic of **tool calling fine-tuning** for optimal agent performance, which you can learn more about in [LangChain Tool Calling Fine-Tuning]({% post_url 2026-11-16-langchain-tool-calling-fine-tuning %}).

### Best Practices for Building LangChain AI Agents

To ensure your **LangChain AI Agent** is robust and effective, consider these best practices:

*   **Clear Tool Descriptions:** Provide concise and accurate `docstrings` for your tools. The LLM relies heavily on these descriptions to understand when and how to use each tool.
*   **Handle Tool Errors Gracefully:** Your tools should anticipate and handle potential errors, returning informative messages to the LLM. This allows the agent to recover or inform the user.
*   **Specific Prompts:** Guide your LLM with clear instructions in the system message. Define its role, limitations, and desired output format.
*   **Verbose Mode for Debugging:** Always start with `verbose=True` in `AgentExecutor`. This provides invaluable insights into the agent's reasoning process and helps debug unexpected behavior.
*   **Memory Management:** Implement appropriate memory solutions for multi-turn interactions. Consider using summarization or conversation buffer memory for longer contexts.
*   **Testing and Iteration:** **LLM agents** are often complex. Test thoroughly with various inputs, edge cases, and user intents. Iterate on your tools and prompts based on observations.
*   **Security:** Be mindful of the capabilities you grant to your agent, especially with tools that access external systems or sensitive data. Validate inputs and restrict permissions where necessary.
*   **Cost Management:** Be aware of the costs associated with LLM API calls, especially in `verbose` mode or with long chains of tool calls. Monitor usage, possibly with LangSmith.

### Frequently Asked Questions (FAQs)

#### Q1: What is the main difference between a LangChain Agent and a Chain?
A LangChain Agent has an **LLM agent** at its core that can dynamically decide which tools to use and in what order, based on the input and observations. A Chain, on the other hand, follows a predefined, fixed sequence of steps or calls. Agents exhibit more autonomy and decision-making capabilities.

#### Q2: Can I use any LLM with LangChain Agents?
Yes, LangChain is designed to be LLM-agnostic. While this tutorial used OpenAI's models, you can integrate other models like Google Gemini, Anthropic Claude, or even open-source models (e.g., Llama 2 with [LangChain, Llama2, Qdrant for RAG Chatbots]({% post_url 2026-11-14-langchain-llama2-qdrant-rag-chatbot %})) by using their respective LangChain integrations. Ensure the LLM you choose has strong **tool calling** capabilities for optimal agent performance.

#### Q3: How do I create my own custom tools for a LangChain AI Agent?
You can create custom tools by simply writing a Python function and decorating it with `@tool` from `langchain_core.tools`. The function's `docstring` is crucial as it serves as the description the LLM uses to understand the tool's purpose and usage.

#### Q4: Why is my LangChain AI Agent not using a tool even when it should?
Several factors can cause this:
*   **Poor Tool Description:** The tool's docstring might not clearly explain its purpose or input requirements to the LLM.
*   **Prompting Issues:** The agent's system prompt might not adequately emphasize tool usage or define its role.
*   **LLM Capabilities:** The chosen LLM might not be strong enough in **tool calling** or complex reasoning.
*   **Input Format:** The input you're providing might not align with what the LLM expects to trigger a tool.
*   **Incorrect `tools` list:** Ensure all intended tools are passed correctly to `create_tool_calling_agent` and `AgentExecutor`.

#### Q5: How can I debug my LangChain AI Agent?
Use `verbose=True` when initializing your `AgentExecutor` to see the agent's internal thought process, tool calls, and observations. For more advanced debugging and monitoring, integrate [LangSmith]({% post_url 2026-11-13-langchain-observability-langsmith-tutorial %}), which provides detailed traces of every step in your agent's execution.

#### Q6: What's the difference between `create_tool_calling_agent` and `create_react_agent`?
`create_tool_calling_agent` leverages modern LLMs' native ability to output structured JSON for tool calls, which is often more robust and efficient. `create_react_agent` implements the ReAct (Reasoning and Acting) framework, where the LLM's thought process and actions are explicitly formatted in text, often requiring more sophisticated parsing. `create_tool_calling_agent` is generally recommended for compatible LLMs.

#### Q7: Can LangChain Agents handle asynchronous operations?
Yes, LangChain supports asynchronous operations. Many components, including LLMs and tools, have `async` versions (`ainvoke`, `abatch`). You can build asynchronous **agentic workflows** using these capabilities, which is crucial for scalable applications.

#### Q8: Where can I find more examples of LangChain agents?
The LangChain documentation is an excellent resource. You can also explore the [LangChain Agents Free Sandbox]({% post_url 2026-11-13-langchain-agents-free-sandbox %}) for interactive examples and experimentation.

### Conclusion

Congratulations! You've successfully built your first **LangChain AI Agent** in Python. You now understand the fundamental concepts of **LLM agents**, **tool calling**, **agentic workflows**, and how to assemble these components with LangChain. This foundation empowers you to create increasingly sophisticated and **autonomous agents** capable of solving complex problems.

This is just the beginning of your journey into **Python AI development**. Experiment with different tools, explore advanced prompting techniques, and consider integrating more complex memory systems. The possibilities with **Large Language Models** and LangChain are immense. Keep building, learning, and innovating!