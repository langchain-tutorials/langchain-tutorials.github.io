---
title: "LangGraph Subgraphs Tutorial: Build a Research Agent from Scratch"
description: "Master LangGraph subgraphs with this tutorial. Build a research agent from scratch mastering advanced techniques to create powerful AI applications today."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangGraph subgraphs tutorial]
featured: false
image: '/assets/images/langgraph-subgraphs-tutorial-research-agent.webp'
---

## Welcome to the World of Smart Agents!

Imagine having a super-smart assistant that can do complex research for you. It wouldn't just search once; it would dig deeper, understand what it finds, and give you a clear answer. Building such an intelligent assistant might sound difficult, but with tools like LangGraph, it becomes much easier.

In this **LangGraph subgraphs tutorial**, you will learn how to build a powerful `research agent` from the ground up. We'll start with simple ideas and then show you how to combine them into something truly amazing. Get ready to turn your ideas into a working, smart agent!

## Understanding LangGraph: Your Agent's Brain

Think of LangGraph like a special map for your agent's thoughts and actions. This map shows exactly what your agent should do at each step. It uses something called a "directed acyclic graph," which is just a fancy way of saying a one-way street map for information.

This map helps your agent decide, for example, whether to search for information or to think about what it already knows. LangGraph lets you clearly define the `agent loop`, which is the repeated cycle of thinking and acting your agent performs. It's like giving your agent a step-by-step guide for its day.

### Key Ingredients for Your Smart Agent

To build any agent with LangGraph, you need a few core ingredients. These are like the basic building blocks for your agent's brain. Understanding them is key to mastering this **LangGraph subgraphs tutorial**.

#### Nodes: The Action Stations

Nodes are like different stations on your agent's map. Each node performs a specific task. For example, one node might be "decide what to search for," and another might be "actually search the internet."

When your agent reaches a node, it does its job, and then the information moves to the next station. This keeps the agent's actions organized and clear. You can make nodes do almost anything you can imagine!

#### Edges: The Pathways Between Stations

Edges are the paths that connect your nodes. They tell your agent where to go after finishing a task at one station. Think of them as the arrows on your map that show the direction of travel.

Some edges are simple, always leading to the same next station. Others are "conditional," meaning the agent decides which path to take based on the information it has. This allows for smart decision-making within the `agent loop`.

#### State: The Agent's Memory and Workspace

The state is like your agent's personal notebook. It's where all the information it gathers and processes is stored. As the agent moves from one node to another, the state gets updated with new findings or decisions.

This shared notebook ensures that every part of your agent's brain knows what's happened before and what needs to happen next. It's how the agent remembers the question it's trying to answer and all the search results it found. Without a shared state, your agent would forget things as it moved between tasks.

#### Tool Calling: Giving Your Agent Superpowers

`Tool calling` is how your agent uses special abilities, much like you might use a calculator or a dictionary. These abilities come from `LangChain tools`, which are pre-built functions that your agent can access. For example, a search tool lets your agent look up information on the internet.

When your agent needs to perform an action outside of its "thinking" process, it uses `tool calling`. It asks for the right tool, gives it the necessary information, and then receives the tool's result. This is how a `research agent` can actually go out and find facts.

## The Power of LangGraph Subgraphs Tutorial: Making Agents Smarter

Now, imagine your agent has a very big, complicated task, like writing a detailed report on climate change. If you try to put every single step on one big map, it would become messy and hard to manage. This is where `LangGraph subgraphs tutorial` becomes incredibly helpful.

**Subgraphs** are like mini-maps or specialized departments within your agent's main brain. Instead of one giant map, you have several smaller, focused maps. Each subgraph handles a specific part of the overall mission. For example, you could have one subgraph just for searching the internet, another for summarizing what it finds, and another for writing the final answer.

### Why Use Subgraphs?

Subgraphs offer several powerful advantages:

1.  **Modularity:** You can build and test each mini-map separately. This makes your agent easier to understand and fix if something goes wrong. It's like building a car from different pre-made parts rather than crafting everything from scratch.
2.  **Complexity Management:** For a complex `research agent`, subgraphs break down big problems into smaller, manageable chunks. This prevents the main `agent loop` from becoming overwhelmingly complicated.
3.  **Specialized Tasks:** Each subgraph can be highly specialized in its function. A search subgraph can focus solely on information retrieval, while a synthesis subgraph can focus on understanding and combining that information. This leads to more efficient and accurate task execution.
4.  **Reusability:** Once you build a useful subgraph, you can potentially reuse it in different agents or different parts of the same agent. This saves time and effort.

By using subgraphs, your `research agent` can tackle much harder problems. It's like having different teams working on different parts of a big project, each team a master of its own specific job. This **LangGraph subgraphs tutorial** will guide you through setting up these powerful internal teams.

## Getting Ready: Your Workspace for Building Agents

Before we start building, you need to set up your digital workspace. Think of this as getting your tools ready on your workbench. You'll need Python installed on your computer, which is the programming language we'll use.

Then, you'll install some special libraries, which are like extra toolkits. These include `langchain` for making powerful language models do specific tasks, `langgraph` for building our agent's brain, and `tavily-python` for internet searching. You'll also need some secret keys (API keys) to let your agent use services like OpenAI or Anthropic for thinking, and Tavily for searching.

```bash
pip install -qU langchain langchain-openai langgraph tavily-python
```

After installation, you'll need to set up your API keys. These are like passwords that let your agent use powerful online services. You should get an API key from a large language model provider (like OpenAI or Anthropic) and from Tavily.

You can usually set these as environment variables on your computer. This keeps them safe and out of your code. For example:

```bash
export OPENAI_API_KEY="your_openai_key_here"
export TAVILY_API_KEY="your_tavily_key_here"
```

## Your First Agent: A Simple Searcher

Let's start by building a very simple agent. This agent will only have one main job: to search for information using a tool and then give you the raw search results. This will introduce you to the basic `agent loop` and `tool calling` mechanics before we dive into `LangGraph subgraphs tutorial`.

### Defining the Agent's Tools (LangChain Tools)

Our simple agent needs a way to find information. For this, we'll use Tavily Search, which is a powerful internet search engine. LangChain provides an easy way to turn Tavily into a `LangChain tool` that our agent can use.

We create an instance of the `TavilySearchResults` tool. This tool expects a query (what to search for) and returns the search results.

```python
from langchain_community.tools.tavily_search import TavilySearchResults

# Initialize Tavily search tool
tavily_tool = TavilySearchResults(max_results=5) # Max 5 results per search
tools = [tavily_tool]

print(f"Available tools for our agent: {[tool.name for tool in tools]}")
```

This code snippet sets up one of our first `LangChain tools`. Our agent will use this to perform `tool calling` whenever it needs to look something up. It's like giving your agent a direct link to the internet.

### Setting Up the LLM

Next, our agent needs a "brain" to think and make decisions. This brain will be a Large Language Model (LLM). We'll use OpenAI's model for this example, but you could use Anthropic or others. The LLM will decide whether to call a tool or finish the task.

```python
from langchain_openai import ChatOpenAI

# Initialize the LLM
# We use temperature=0 for more consistent (less creative) answers, good for research
llm = ChatOpenAI(model="gpt-4o", temperature=0)
```

This sets up the core intelligence of our `research agent`. The `llm` is crucial for deciding the next step in the `agent loop`. It's the part that understands your questions and formulates responses or tool requests.

### The Agent's State

The state is the information that flows through our agent's graph. For a simple agent, we might just need to keep track of the messages that go back and forth. LangGraph uses a `TypedDict` to define the structure of this state.

```python
from typing import List, TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, FunctionMessage

# Define the state for our agent
class AgentState(TypedDict):
    # The list of messages in the conversation
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    # This will store the tool result if a tool is called
    tool_result: str | None
```

Here, `messages` will be a list of all chat interactions, building a history. The `tool_result` will temporarily hold what the search tool finds. The `Annotated` part is a special LangGraph way to say how new messages should be added to the list (they should just be added to the end). This state is how information is passed around in the `agent loop`.

### Agent Nodes

Now, let's define the specific actions (nodes) our simple agent can take. We'll have two main nodes: one for the LLM to decide what to do, and one for actually using a tool.

#### `call_model` Node: The Thinker

This node uses the LLM to decide the next action. The LLM will look at the conversation history (the `messages` in our state) and decide if it needs to use a tool or if it can answer directly.

To allow the LLM to use tools, we need to bind our `LangChain tools` to it. This tells the LLM about the tools it has available and how to use them.

```python
# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(tools)

def call_model(state: AgentState):
    """
    Invokes the LLM to make a decision based on the current state.
    It can decide to call a tool or respond directly.
    """
    messages = state['messages']
    print("\n--- LLM is thinking ---")
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}
```

This `call_model` function represents the "thinking" part of our `agent loop`. It's where the LLM processes information and decides what to do next. If the LLM decides to use a tool, its response will contain a `tool_calls` message.

#### `call_tool` Node: The Doer

This node is responsible for executing the tool that the LLM decided to use. It takes the tool call information from the LLM's response and runs the actual `LangChain tool`.

```python
from langchain_core.messages import ToolMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables import RunnableConfig

# Helper function to execute tool calls
def _get_langchain_agent(llm, tools):
    # This is a basic way to create an agent that can execute tools
    # We are simplifying this for direct tool call execution in LangGraph
    # In more complex scenarios, you might define a specific LangChain AgentExecutor here.
    pass # We will handle tool calling directly in our LangGraph node for this example

# A custom tool executor for LangGraph
from langgraph.prebuilt import ToolExecutor

tool_executor = ToolExecutor(tools)

def call_tool(state: AgentState):
    """
    Executes tool calls specified in the latest AI message.
    """
    messages = state['messages']
    last_message = messages[-1]
    print(f"\n--- Calling tool(s): {last_message.tool_calls[0].get('name')} ---")

    # LangGraph expects us to explicitly handle tool calls.
    # We extract the tool_calls from the AI message and execute them.
    # In a real scenario, you might iterate through multiple tool calls.
    if not last_message.tool_calls:
        raise ValueError("No tool calls found in the last AI message.")

    tool_outputs = []
    for tool_call in last_message.tool_calls:
        action = {
            "tool": tool_call['name'],
            "tool_input": tool_call['args']
        }
        output = tool_executor.invoke(action)
        tool_outputs.append(output)

    # Return a ToolMessage with the output
    # For simplicity, we'll join multiple tool outputs if there were more.
    return {"messages": [ToolMessage(content=str(tool_outputs[0]), tool_call_id=tool_call['id'])]}
```

The `call_tool` function is where the `tool calling` actually happens. It receives instructions from the LLM, executes the `LangChain tools`, and then sends the results back into the state. This is a critical part of any `research agent` that needs external information.

### Defining the Agent Loop

Now we connect our nodes with edges to create the `agent loop`. This defines the flow of our agent's thinking and acting. We'll use `Graph` from `langgraph` to build this.

1.  **Initialize the Graph:** Start a new graph.
2.  **Add Nodes:** Add our `call_model` and `call_tool` functions as nodes.
3.  **Set Entry Point:** Tell the graph where to start (always with the LLM thinking).
4.  **Add Conditional Edges:** This is the smart part! We tell the graph: after the LLM thinks, check its response. If it wants to call a tool, go to `call_tool`. If it's ready to answer, finish the graph.

```python
from langgraph.graph import StateGraph, END

# Define the graph
workflow = StateGraph(AgentState)

# Add the nodes
workflow.add_node("llm_node", call_model)
workflow.add_node("tool_node", call_tool)

# Set the entry point - where the graph starts
workflow.set_entry_point("llm_node")

# Define a function to decide the next step after the LLM
def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM wants to call a tool, return "continue" to go to the tool node
    if last_message.tool_calls:
        print("LLM wants to call a tool.")
        return "continue"
    else:
        # Otherwise, the LLM is ready to respond, so we end
        print("LLM is ready to respond.")
        return "end"

# Add conditional edges
workflow.add_conditional_edges(
    "llm_node",      # From the LLM node
    should_continue, # Use this function to decide next step
    {
        "continue": "tool_node", # If 'continue', go to the tool node
        "end": END               # If 'end', finish the graph
    }
)

# After the tool node, always go back to the LLM node for it to process the tool output
workflow.add_edge("tool_node", "llm_node")

# Compile the graph
app = workflow.compile()
print("\n--- Simple Agent Graph Compiled ---")
```

This section really brings the simple agent to life. The `should_continue` function acts as the decision-maker for the `agent loop`. It checks the LLM's last output to see if `tool calling` is needed. If so, it sends the flow to `tool_node`; otherwise, the `agent loop` ends.

### Testing Your Simple Agent

Let's ask our simple agent a question and see it in action! We'll ask it to search for something simple.

```python
from IPython.display import Image, display

# Optional: Visualize the graph (requires graphviz installed)
# try:
#     display(Image(app.get_graph().draw_png()))
# except Exception as e:
#     print(f"Could not draw graph: {e}. Make sure graphviz is installed.")

print("\n--- Invoking Simple Agent ---")
inputs = {"messages": [HumanMessage(content="What are the latest advancements in AI for medical diagnosis?")]}

for s in app.stream(inputs):
    print(s)
    print("---")

# To get the final output directly
final_state = app.invoke(inputs)
print("\n--- Final output from Simple Agent ---")
print(final_state['messages'][-1].content)
```

You'll see the agent's thought process: the LLM thinks, decides to use the Tavily search tool, the tool runs, and then the results are sent back to the LLM. The LLM then processes these results and might respond or decide to search again. For this simple agent, it will likely return the raw search results. This demonstration shows the fundamental `agent loop` in action.

## Level Up: Building a Specialized Research Agent

Our simple agent can search, but a real `research agent` needs to do more than just search once. It needs to:

*   Figure out *what* to search for.
*   Perform multiple searches if needed.
*   Read and understand the search results.
*   Combine different pieces of information.
*   Identify gaps or conflicting data.
*   Finally, write a clear, concise answer.

Trying to cram all these steps into one big, messy graph would be a nightmare. This is exactly why `LangGraph subgraphs tutorial` exists! We will use subgraphs to break down this complex `research agent` into manageable, specialized parts.

### Blueprint for Your Smart Research Assistant

Our advanced `research agent` will have a main brain that oversees everything. This main brain will then delegate tasks to specialized sub-brains, which are our subgraphs.

Here's how we'll structure our `research agent`:

*   **Main Graph:** The overall coordinator. It receives your research question and decides which specialized subgraph to call next.
*   **Deep Dive Search Subgraph:** This mini-agent's job is to conduct thorough searches using `Tavily`, explore different queries, and gather relevant raw information.
*   **Information Synthesis Subgraph:** This mini-agent takes the raw information from the search subgraph and works to understand it, extract key points, and identify any contradictions or missing pieces.
*   **Answer Formulation Subgraph:** Once the information is synthesized, this mini-agent's role is to draft, review, and refine the final answer to your research question.

This modular design makes our `research agent` much more powerful and easier to develop. Each subgraph will have its own `agent loop` and state management.

## Building the Deep Dive Search Subgraph

Let's start by creating the first specialized team: the **Deep Dive Search Subgraph**. This subgraph will be responsible for intelligently finding information. It won't just search once; it will analyze the results and decide if more searching is needed.

### Defining Search Tools

Our search subgraph will primarily rely on the `TavilySearchResults` tool, just like our simple agent. This is a powerful `LangChain tool` for web searching.

```python
# Re-using the TavilySearchResults tool defined earlier
# tavily_tool = TavilySearchResults(max_results=5)
# tools = [tavily_tool] # Our search subgraph will only use this tool initially
```

For more advanced scenarios, you could add other tools here, like a tool to read specific document types or a tool to browse complex websites. This demonstrates how `tool calling` can be extended.

### Search Subgraph State

The state for our search subgraph needs to keep track of its specific task. It will need the original question, what it has searched for, and the results it found.

```python
class SearchState(TypedDict):
    question: str
    search_queries: Annotated[List[str], lambda x, y: x + y] # What we've searched for
    search_results: Annotated[List[str], lambda x, y: x + y] # What we've found
    summary: str | None # A summary of findings so far
    num_iterations: int # To prevent infinite loops
```

This state is unique to the search subgraph. It holds the context relevant to its `agent loop`, allowing it to perform focused actions. The `num_iterations` is a simple way to prevent the search agent from searching forever if it gets stuck.

### Search Subgraph Nodes

The search subgraph will have a few key nodes to manage its search `agent loop`:

#### `decide_search_query` (LLM decides what to search)

This node uses the LLM to intelligently generate search queries. It looks at the original question and any previous search results to decide what to search for next.

```python
def decide_search_query(state: SearchState):
    """
    LLM decides the next search query based on the question and previous results.
    """
    print("\n--- Search Subgraph: LLM deciding search query ---")
    question = state['question']
    current_queries = state.get('search_queries', [])
    current_results = state.get('search_results', [])

    # If this is the first time, just use the original question
    if not current_queries:
        query_prompt = f"Given the research question: '{question}', what is the initial, most effective search query to find relevant information?"
    else:
        # Otherwise, refine the query based on previous findings
        query_prompt = (
            f"You are researching: '{question}'.\n"
            f"You have already searched for: {current_queries}\n"
            f"And found these partial results: {current_results[:1].__str__()}\n" # Show only first result snippet for brevity
            f"What is the NEXT most effective search query to deepen your understanding or find missing information? "
            f"Respond with ONLY the search query, no other text."
        )

    response = llm.invoke(query_prompt)
    new_query = response.content.strip()

    print(f"Generated search query: '{new_query}'")
    return {"search_queries": [new_query]}
```

This node is the brain of the search subgraph. It uses the LLM's intelligence to guide the `tool calling` process for search.

#### `execute_search` (calls Tavily)

This node performs the actual search using the `tavily_tool`. It takes the query generated by the previous node and gets the results.

```python
def execute_search(state: SearchState):
    """
    Executes the search using the Tavily tool.
    """
    print("\n--- Search Subgraph: Executing search ---")
    latest_query = state['search_queries'][-1]
    
    try:
        search_output = tavily_tool.invoke({"query": latest_query})
        print(f"Search results for '{latest_query}': {search_output[:100]}...") # Show snippet
        return {"search_results": [str(search_output)], "tool_result": str(search_output)}
    except Exception as e:
        print(f"Error during search: {e}")
        return {"search_results": [f"Error during search: {e}"], "tool_result": f"Error during search: {e}"}
```

Here is where the `tool calling` happens within the search subgraph. The `tavily_tool` is invoked to gather external information.

#### `summarize_results` (LLM summarizes findings)

After searching, this node uses the LLM to summarize the newly found information. This helps keep the state manageable and provides a concise overview.

```python
def summarize_results(state: SearchState):
    """
    LLM summarizes the latest search results and decides if more search is needed.
    """
    print("\n--- Search Subgraph: Summarizing results ---")
    question = state['question']
    latest_results = state['search_results'][-1]
    current_summary = state.get('summary', '')

    summary_prompt = (
        f"You are researching: '{question}'.\n"
        f"Here are the latest search results:\n{latest_results}\n\n"
        f"And here is a summary of what you've found so far (if any):\n{current_summary}\n\n"
        f"Based on the new results, update the summary. Then, decide if more searching is needed to fully answer the question. "
        f"If yes, respond with '[MORE_SEARCH]' followed by an updated concise summary. "
        f"If no, respond with '[DONE_SEARCH]' followed by the final concise summary. "
        f"Ensure the summary directly addresses the original question and integrates all relevant information."
    )
    
    response = llm.invoke(summary_prompt)
    content = response.content.strip()

    if content.startswith("[MORE_SEARCH]"):
        new_summary = content.replace("[MORE_SEARCH]", "").strip()
        print("Search Subgraph: More search needed.")
        return {"summary": new_summary, "next_action": "continue_search"}
    else:
        new_summary = content.replace("[DONE_SEARCH]", "").strip()
        print("Search Subgraph: Search complete.")
        return {"summary": new_summary, "next_action": "finish_search"}
```

This `summarize_results` node demonstrates complex `agent loop` logic. The LLM not only summarizes but also makes a conditional decision about the next step, leveraging its understanding of the `research agent`'s goal. It updates the state with `next_action`.

### Search Subgraph Edges

Now, let's connect these nodes to form the `agent loop` for our search subgraph.

```python
from langgraph.graph import Graph

# Define the search subgraph
search_subgraph = Graph(SearchState)

search_subgraph.add_node("decide_query", decide_search_query)
search_subgraph.add_node("execute_search", execute_search)
search_subgraph.add_node("summarize_and_decide", summarize_results)

search_subgraph.set_entry_point("decide_query")

# After deciding query, execute search
search_subgraph.add_edge("decide_query", "execute_search")
# After executing search, summarize and decide
search_subgraph.add_edge("execute_search", "summarize_and_decide")

# After summarizing, conditionally decide if more search is needed
search_subgraph.add_conditional_edges(
    "summarize_and_decide",
    lambda state: state['next_action'], # This assumes 'next_action' is set in summarize_results
    {
        "continue_search": "decide_query", # Loop back to decide a new query
        "finish_search": END               # Exit the subgraph
    }
)

compiled_search_subgraph = search_subgraph.compile()
print("\n--- Deep Dive Search Subgraph Compiled ---")
# display(Image(compiled_search_subgraph.get_graph().draw_png())) # Optional visualization
```

This graph definition completes the `agent loop` for the search subgraph. It clearly shows how the `research agent` iteratively refines its search based on previous findings. The conditional edge on "summarize_and_decide" is critical for this iterative process.

## Crafting the Information Synthesis Subgraph

Once the Deep Dive Search Subgraph has gathered all the necessary information, it's time for the **Information Synthesis Subgraph** to take over. This subgraph's job is to make sense of all the raw data, extract key insights, and identify any inconsistencies.

### Synthesis Subgraph State

The state for our synthesis subgraph needs to hold the raw information it receives, the insights it extracts, and any identified gaps or conflicts.

```python
class SynthesisState(TypedDict):
    question: str
    raw_information: str
    key_points: Annotated[List[str], lambda x, y: x + y] # Extracted key points
    analysis_results: str | None # Detailed analysis output
    gaps_conflicts: str | None # Identified gaps or contradictions
    synthesis_status: str # "in_progress" or "completed"
```

This state ensures the synthesis `agent loop` has all the necessary context to perform its specialized task.

### Synthesis Subgraph Nodes

The synthesis subgraph will have nodes to process, analyze, and refine the information:

#### `extract_key_points` (LLM identifies crucial info)

This node takes the raw search results and uses the LLM to pull out the most important facts and details relevant to the original question.

```python
def extract_key_points(state: SynthesisState):
    """
    LLM extracts key points from the raw information.
    """
    print("\n--- Synthesis Subgraph: Extracting key points ---")
    question = state['question']
    raw_info = state['raw_information']
    
    prompt = (
        f"Given the research question: '{question}'\n"
        f"And the following raw information:\n{raw_info}\n\n"
        f"Extract the most important key points and facts that directly answer or are highly relevant to the question. "
        f"Present them as a bulleted list. Be concise and focus on actionable information."
    )
    response = llm.invoke(prompt)
    key_points_str = response.content.strip()
    key_points_list = [point.strip() for point in key_points_str.split('- ') if point.strip()]

    print(f"Extracted key points: {key_points_str[:200]}...")
    return {"key_points": key_points_list, "analysis_results": key_points_str}
```

This node is the first step in turning raw data into structured insights for the `research agent`.

#### `identify_gaps_or_conflicts` (LLM checks for missing info or contradictions)

After extracting key points, this node analyzes them for any missing information or parts that seem to contradict each other. This is crucial for high-quality research.

```python
def identify_gaps_or_conflicts(state: SynthesisState):
    """
    LLM identifies gaps or conflicts in the extracted key points.
    """
    print("\n--- Synthesis Subgraph: Identifying gaps/conflicts ---")
    question = state['question']
    current_key_points = "\n".join(state['key_points'])
    
    prompt = (
        f"You are synthesizing information for the question: '{question}'.\n"
        f"Here are the key points extracted so far:\n{current_key_points}\n\n"
        f"Analyze these key points. Do you notice any missing information that would be critical to fully answer the question? "
        f"Are there any contradictions or inconsistencies between the points? "
        f"If there are gaps or conflicts, describe them clearly and suggest what additional information is needed. "
        f"If the information seems sufficient and consistent, respond with 'NO_GAPS_OR_CONFLICTS'."
    )
    response = llm.invoke(prompt)
    gaps_conflicts_info = response.content.strip()

    if gaps_conflicts_info == "NO_GAPS_OR_CONFLICTS":
        print("Synthesis Subgraph: No significant gaps or conflicts identified.")
        return {"gaps_conflicts": None, "synthesis_status": "completed"}
    else:
        print(f"Synthesis Subgraph: Gaps/Conflicts identified: {gaps_conflicts_info[:200]}...")
        return {"gaps_conflicts": gaps_conflicts_info, "synthesis_status": "in_progress"}
```

This node adds a layer of critical thinking to the `research agent`. If it finds gaps, it can signal back to the main agent to perhaps trigger another search or a different action.

### Synthesis Subgraph Edges

Here's how the nodes in the synthesis subgraph connect:

```python
# Define the synthesis subgraph
synthesis_subgraph = Graph(SynthesisState)

synthesis_subgraph.add_node("extract_points", extract_key_points)
synthesis_subgraph.add_node("identify_issues", identify_gaps_or_conflicts)

synthesis_subgraph.set_entry_point("extract_points")

synthesis_subgraph.add_edge("extract_points", "identify_issues")

synthesis_subgraph.add_conditional_edges(
    "identify_issues",
    lambda state: "continue" if state['synthesis_status'] == "in_progress" and state['gaps_conflicts'] else "end",
    {
        "continue": END, # For simplicity, if gaps are found, it signals back to main agent by ending for now
                        # In a more advanced setup, it might loop back to search via main agent
        "end": END      # If no issues, synthesis is complete
    }
)

compiled_synthesis_subgraph = synthesis_subgraph.compile()
print("\n--- Information Synthesis Subgraph Compiled ---")
# display(Image(compiled_synthesis_subgraph.get_graph().draw_png())) # Optional visualization
```

This subgraph's `agent loop` focuses on analysis and identifying completeness. Currently, if issues are found, it simply ends, signaling to the main agent that more work might be needed. In a full `research agent`, this could trigger another call to the search subgraph.

## Building the Answer Formulation Subgraph

The final step for our `research agent` is to present the findings clearly and concisely. This is the job of the **Answer Formulation Subgraph**. It takes the synthesized information and turns it into a coherent answer.

### Formulation Subgraph State

The state for the formulation subgraph needs the synthesized data, a draft of the answer, and perhaps flags for review and refinement.

```python
class FormulationState(TypedDict):
    question: str
    synthesized_data: str # The summarized and analyzed information from previous stages
    draft_answer: str | None
    review_status: str # "needs_review", "reviewed", "refined"
    final_answer: str | None
```

This state keeps the context for the formulation `agent loop`, ensuring the answer is built correctly.

### Formulation Subgraph Nodes

The formulation subgraph will involve drafting, reviewing, and refining the answer:

#### `draft_response` (LLM creates an initial answer)

This node uses the LLM to generate a first draft of the answer based on all the synthesized information.

```python
def draft_response(state: FormulationState):
    """
    LLM drafts the initial response based on synthesized data.
    """
    print("\n--- Formulation Subgraph: Drafting response ---")
    question = state['question']
    synthesized_data = state['synthesized_data']
    
    prompt = (
        f"Given the research question: '{question}'\n"
        f"And the following synthesized and key information:\n{synthesized_data}\n\n"
        f"Write a comprehensive, clear, and concise answer to the research question. "
        f"Ensure it directly addresses the question using the provided information. "
        f"Do not add information that is not supported by the data."
    )
    response = llm.invoke(prompt)
    draft = response.content.strip()

    print(f"Initial draft created: {draft[:200]}...")
    return {"draft_answer": draft, "review_status": "needs_review"}
```

This node produces the first output of the `research agent` based on its understanding.

#### `review_response` (LLM checks for clarity, completeness)

This node acts as a self-critic. It uses the LLM to review the drafted answer for clarity, accuracy, and whether it fully addresses the original question.

```python
def review_response(state: FormulationState):
    """
    LLM reviews the draft for clarity, completeness, and accuracy.
    """
    print("\n--- Formulation Subgraph: Reviewing response ---")
    question = state['question']
    draft_answer = state['draft_answer']
    
    prompt = (
        f"Review the following draft answer for the research question: '{question}'.\n"
        f"Draft Answer:\n{draft_answer}\n\n"
        f"Critique this draft. Is it clear? Is it complete? Does it directly answer the question? "
        f"Are there any factual inaccuracies based on common knowledge (without needing new search)? "
        f"Suggest specific improvements if needed. If it's excellent, respond with 'NO_IMPROVEMENTS_NEEDED'."
    )
    response = llm.invoke(prompt)
    review_feedback = response.content.strip()

    if review_feedback == "NO_IMPROVEMENTS_NEEDED":
        print("Formulation Subgraph: Draft is excellent, no improvements needed.")
        return {"review_status": "reviewed"}
    else:
        print(f"Formulation Subgraph: Feedback: {review_feedback[:200]}...")
        return {"review_status": "needs_refinement", "feedback": review_feedback} # Add feedback to state if needed for refinement
```

This critical step ensures the quality of the `research agent`'s final output.

#### `refine_response` (LLM makes improvements)

If the review node finds issues, this node takes the feedback and uses the LLM to improve the draft.

```python
def refine_response(state: FormulationState):
    """
    LLM refines the draft based on review feedback.
    """
    print("\n--- Formulation Subgraph: Refining response ---")
    question = state['question']
    draft_answer = state['draft_answer']
    feedback = state.get('feedback', '') # Assuming feedback is added to state by review_response

    if not feedback: # Should not happen if coming from 'needs_refinement'
        print("No feedback to refine. Returning current draft.")
        return {"draft_answer": draft_answer, "review_status": "reviewed"}

    prompt = (
        f"Given the research question: '{question}'\n"
        f"Here is a draft answer:\n{draft_answer}\n\n"
        f"Here is feedback for improvement:\n{feedback}\n\n"
        f"Please revise the draft answer based on this feedback. "
        f"Produce the improved answer."
    )
    response = llm.invoke(prompt)
    refined_answer = response.content.strip()

    print(f"Response refined: {refined_answer[:200]}...")
    return {"draft_answer": refined_answer, "review_status": "needs_review"} # Loop back for another review
```

This node closes the loop for refinement, enabling the `research agent` to iteratively improve its answer. This is a mini-`agent loop` within the subgraph.

### Formulation Subgraph Edges

The edges in the formulation subgraph handle the drafting, reviewing, and refining process.

```python
# Define the formulation subgraph
formulation_subgraph = Graph(FormulationState)

formulation_subgraph.add_node("draft", draft_response)
formulation_subgraph.add_node("review", review_response)
formulation_subgraph.add_node("refine", refine_response)

formulation_subgraph.set_entry_point("draft")

formulation_subgraph.add_edge("draft", "review")

formulation_subgraph.add_conditional_edges(
    "review",
    lambda state: "refine" if state['review_status'] == "needs_refinement" else "end",
    {
        "refine": "refine", # If needs refinement, go to refine
        "end": END          # If reviewed and good, finish
    }
)

formulation_subgraph.add_edge("refine", "review") # After refining, go back to review

compiled_formulation_subgraph = formulation_subgraph.compile()
print("\n--- Answer Formulation Subgraph Compiled ---")
# display(Image(compiled_formulation_subgraph.get_graph().draw_png())) # Optional visualization
```

This defines the iterative process for answer generation. The `agent loop` here allows for self-correction and quality assurance before the final output.

## Bringing It All Together: Your Grand Research Agent

Now, for the exciting part of our **LangGraph subgraphs tutorial**! We will combine all three specialized subgraphs (Search, Synthesis, Formulation) into one powerful main `research agent`. The main agent will act as the orchestrator, deciding which subgraph to call at each stage of the research process.

### The Main Research Agent's State

The main agent's state needs to be broad enough to encompass all stages of the research. It will manage the overall `agent loop`.

```python
class ResearchAgentState(TypedDict):
    question: str
    current_task: str # E.g., "search", "synthesize", "formulate"
    research_results: str | None
    synthesized_data: str | None
    final_output: str | None
    iterations: int # To limit overall execution
```

This state serves as the central hub for all information exchange between the main `agent loop` and its subgraphs.

### Main Agent Nodes

The main agent will have a node to decide the next big step and nodes to call each subgraph.

#### `decide_next_task` (LLM decides whether to call search, synthesis, or formulation subgraph)

This is the main brain of our `research agent`. It looks at the current state and decides which specialized subgraph is needed next.

```python
def decide_next_task(state: ResearchAgentState):
    """
    LLM decides the next major task: search, synthesize, formulate, or finish.
    """
    print(f"\n--- Main Agent: Deciding next task (Iteration: {state['iterations']}) ---")
    question = state['question']
    current_results = state.get('research_results', '')
    synthesized = state.get('synthesized_data', '')
    
    prompt = (
        f"You are a master research agent. Your goal is to answer the question: '{question}'.\n"
        f"Current raw research results:\n{current_results[:500]}...\n"
        f"Current synthesized data:\n{synthesized[:500]}...\n"
        f"Based on the above, what is the most appropriate next step?\n"
        f"Options: 'CALL_SEARCH_SUBGRAPH', 'CALL_SYNTHESIS_SUBGRAPH', 'CALL_FORMULATION_SUBGRAPH', 'FINISH'.\n"
        f"If you need more raw data, call SEARCH. If you have raw data and need to understand it, call SYNTHESIS. "
        f"If you have synthesized data and need to create a final answer, call FORMULATION. "
        f"If the answer is ready, call FINISH. Respond with ONLY the chosen action."
    )
    
    response = llm.invoke(prompt)
    action = response.content.strip().upper()
    print(f"Main Agent decided: {action}")
    
    if action not in ["CALL_SEARCH_SUBGRAPH", "CALL_SYNTHESIS_SUBGRAPH", "CALL_FORMULATION_SUBGRAPH", "FINISH"]:
        print(f"Warning: LLM returned unexpected action: {action}. Defaulting to FINISH.")
        action = "FINISH"

    return {"current_task": action, "iterations": state['iterations'] + 1}
```

This node orchestrates the entire `agent loop` of the `research agent`. It uses the LLM to make high-level strategic decisions.

#### Calling Subgraphs as Nodes

Each subgraph itself can be treated as a "node" within the main graph. LangGraph makes this very easy. We define functions that invoke our compiled subgraphs.

```python
def call_deep_dive_search_subgraph(state: ResearchAgentState):
    """
    Invokes the Deep Dive Search Subgraph.
    """
    print("\n--- Main Agent: Calling Deep Dive Search Subgraph ---")
    search_input = {"question": state['question'], "iterations": 0} # Reset iterations for subgraph
    
    # We invoke the compiled subgraph and pass its state
    # The output of the subgraph will be its final state
    search_output_state = compiled_search_subgraph.invoke(search_input)
    
    final_summary = search_output_state.get('summary', '')
    print(f"Deep Dive Search Subgraph finished. Summary: {final_summary[:200]}...")
    return {"research_results": final_summary, "current_task": "post_search_processing"} # Update with its summary
```

```python
def call_information_synthesis_subgraph(state: ResearchAgentState):
    """
    Invokes the Information Synthesis Subgraph.
    """
    print("\n--- Main Agent: Calling Information Synthesis Subgraph ---")
    if not state.get('research_results'):
        print("Warning: No research results found for synthesis. Proceeding with empty data.")
        
    synthesis_input = {
        "question": state['question'],
        "raw_information": state.get('research_results', 'No raw information found.')
    }
    
    synthesis_output_state = compiled_synthesis_subgraph.invoke(synthesis_input)
    
    synthesized_info = synthesis_output_state.get('analysis_results', '') # Or some other key
    gaps_conflicts = synthesis_output_state.get('gaps_conflicts')
    
    if gaps_conflicts:
        print(f"Synthesis Subgraph found gaps/conflicts: {gaps_conflicts[:100]}...")
        # In a real agent, you might want to re-trigger search based on this.
        # For this example, we'll just store it and proceed.
        synthesized_info += f"\n\nNote: Identified gaps/conflicts: {gaps_conflicts}"
        
    print(f"Information Synthesis Subgraph finished. Synthesized data: {synthesized_info[:200]}...")
    return {"synthesized_data": synthesized_info, "current_task": "post_synthesis_processing"}
```

```python
def call_answer_formulation_subgraph(state: ResearchAgentState):
    """
    Invokes the Answer Formulation Subgraph.
    """
    print("\n--- Main Agent: Calling Answer Formulation Subgraph ---")
    if not state.get('synthesized_data'):
        print("Warning: No synthesized data found for formulation. Proceeding with empty data.")

    formulation_input = {
        "question": state['question'],
        "synthesized_data": state.get('synthesized_data', 'No synthesized data available.')
    }
    
    formulation_output_state = compiled_formulation_subgraph.invoke(formulation_input)
    
    final_answer = formulation_output_state.get('draft_answer', formulation_output_state.get('final_answer', '')) # Get either
    print(f"Answer Formulation Subgraph finished. Final Answer: {final_answer[:200]}...")
    return {"final_output": final_answer, "current_task": "finished"}
```

Each of these functions acts as a proxy for the entire `agent loop` of its respective subgraph. This is the core of how `LangGraph subgraphs tutorial` enables modularity.

### Main Agent Edges

Now, we connect these main agent nodes and subgraph calls to define the overall research flow.

```python
# Define the main graph
research_agent_workflow = StateGraph(ResearchAgentState)

# Add nodes for the main agent's decision and subgraph calls
research_agent_workflow.add_node("decide_task", decide_next_task)
research_agent_workflow.add_node("call_search", call_deep_dive_search_subgraph)
research_agent_workflow.add_node("call_synthesis", call_information_synthesis_subgraph)
research_agent_workflow.add_node("call_formulation", call_answer_formulation_subgraph)

# Set the entry point
research_agent_workflow.set_entry_point("decide_task")

# Add conditional edges based on the 'current_task' decided by 'decide_task'
research_agent_workflow.add_conditional_edges(
    "decide_task",
    lambda state: state['current_task'],
    {
        "CALL_SEARCH_SUBGRAPH": "call_search",
        "CALL_SYNTHESIS_SUBGRAPH": "call_synthesis",
        "CALL_FORMULATION_SUBGRAPH": "call_formulation",
        "FINISH": END
    }
)

# After each subgraph, always go back to 'decide_task' to figure out the next step
research_agent_workflow.add_edge("call_search", "decide_task")
research_agent_workflow.add_edge("call_synthesis", "decide_task")
research_agent_workflow.add_edge("call_formulation", "decide_task")

# Compile the full research agent
full_research_agent = research_agent_workflow.compile()
print("\n--- Full Research Agent with Subgraphs Compiled ---")
# display(Image(full_research_agent.get_graph().draw_png())) # Optional visualization
```

This completes the full `research agent`! The `agent loop` now flows between high-level decision-making and specialized subgraphs, making it incredibly flexible and powerful.

## Putting Your Research Agent to Work

Let's test our complete `research agent` with a challenging question. Watch how it intelligently navigates between its search, synthesis, and formulation subgraphs to get you an answer.

```python
print("\n--- Invoking Full Research Agent ---")
research_question = "What are the long-term environmental impacts of widespread adoption of electric vehicles, beyond just tailpipe emissions?"

initial_state = {"question": research_question, "iterations": 0}

# Stream the execution to see the agent's progress
for s in full_research_agent.stream(initial_state):
    print(s)
    print("---")

# Get the final output
final_research_state = full_research_agent.invoke(initial_state)
print("\n--- Final Answer from Research Agent ---")
print(final_research_state.get('final_output', 'Could not get final answer.'))
```

When you run this, you will see output from the `decide_next_task` node, followed by output from the `Deep Dive Search Subgraph`, then back to `decide_next_task`, potentially to the `Information Synthesis Subgraph`, and finally to the `Answer Formulation Subgraph`. This clearly demonstrates the `agent loop` operating across subgraphs, showcasing the true power of `LangGraph subgraphs tutorial`.

You'll observe the agent's progress step-by-step. First, it will decide to search. The search subgraph will run its own mini-loop, generating queries, executing `tool calling` with `Tavily`, and summarizing. Once the search subgraph completes, the main agent takes over again, decides to synthesize, and so on. This intelligent delegation is the heart of our `research agent`.

## Beyond the Basics: Making Your Agent Even Smarter

You've built a powerful `research agent` using `LangGraph subgraphs tutorial`! But the journey doesn't have to stop here. Here are some ideas to make your agent even smarter:

*   **Error Handling:** What if a tool fails? You could add nodes to gracefully handle errors, retry actions, or inform the user.
*   **Human-in-the-Loop:** For complex decisions or when the agent is unsure, you could add nodes that pause and ask for human input. This ensures quality and allows for collaborative intelligence. If you want to learn more about advanced `tool calling` strategies that incorporate human feedback, check out our post on [Advanced Tool Calling with LangChain](internal-link-to-tool-calling-post.md).
*   **Memory Management:** For longer, multi-turn conversations, you might want to implement more sophisticated memory for your agent, beyond just the current state. LangChain offers excellent tools for this.
*   **More Sophisticated LangChain Tools:** Explore other `LangChain tools` like document loaders, code interpreters, or even custom tools to expand your agent's capabilities. Your `research agent` could summarize PDFs or analyze data files.
*   **Dynamic Subgraph Creation:** For truly dynamic agents, you might even have the LLM decide which *type* of subgraph to create and execute on the fly, tailoring its approach to the problem.

This **LangGraph subgraphs tutorial** has shown you the foundational principles. The possibilities are truly endless once you master these concepts.

## Your Journey with LangGraph Subgraphs Continues!

Congratulations! You've just completed an in-depth **LangGraph subgraphs tutorial** and built a sophisticated `research agent` from scratch. You learned about:

*   The core components of LangGraph: nodes, edges, and state.
*   How to integrate `LangChain tools` for `tool calling`, exemplified by `Tavily` search.
*   The power of `LangGraph subgraphs` for organizing complex `agent loop` logic.
*   How to design, implement, and combine specialized subgraphs for deep research, information synthesis, and answer formulation.

This modular approach allows you to create highly capable and robust AI agents. Now it's your turn to experiment! Try changing the research question, adding new `LangChain tools`, or creating entirely new subgraphs for different tasks. The world of AI agents is yours to explore, and LangGraph gives you the map to navigate it. Happy building!