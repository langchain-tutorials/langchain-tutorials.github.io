---
title: "LangChain vs LangGraph: Build Advanced AI Workflows with Python"
description: "Master LangChain LangGraph Workflows for advanced AI development. Build powerful Python applications, comparing frameworks to create robust and efficient..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: ["LangChain", "LangGraph", "Python", "AI Agents", "Workflows"]
featured: false
image: '/assets/images/langchain-langgraph-ai-workflows.webp'
---
## LangChain vs LangGraph: Build Advanced AI Workflows with Python

### Build Smarter AI Workflows

The rapid evolution of Large Language Models (LLMs) has opened new frontiers for intelligent applications. Building sophisticated AI systems, however, often requires more than just calling an LLM API. You need robust frameworks to orchestrate complex interactions, manage state, and enable dynamic decision-making.

This is where LangChain and LangGraph come into play, offering powerful tools for creating advanced AI agents and multi-agent systems. This guide dives deep into both frameworks, helping you understand their nuances and how to leverage them for your next Python AI project. We'll explore their core functionalities, compare their strengths, and provide practical examples for building cutting-edge [LangChain LangGraph Workflows](#langchain-langgraph-workflows).

### Understanding LangChain: The Foundation of LLM Orchestration

LangChain emerged as a foundational framework for developing applications powered by LLMs. It provides a comprehensive set of abstractions and components to streamline the process of building intelligent applications. You can easily connect LLMs with external data sources and computational tools.

LangChain simplifies common patterns like Retrieval Augmented Generation (RAG), conversational agents, and tool-using agents. It focuses on modularity, allowing you to compose various components into intricate chains. This modular approach is key to developing versatile [Python AI](#python-ai) applications.

#### Core Concepts in LangChain

LangChain is built around several key abstractions that help manage the complexity of LLM interactions. Understanding these components is crucial for effective [LangChain development](#langchain-development).

*   **LLMs & ChatModels:** These are the interfaces to different language models, handling text generation and conversational interactions. You can easily swap between providers like OpenAI, Anthropic, or Hugging Face.
*   **Prompts:** Templates and formatting utilities that structure inputs for LLMs, enabling consistent and effective communication. Prompt templates are essential for guiding model behavior.
*   **Chains:** Sequences of calls to LLMs or other utilities, allowing you to combine multiple operations into a single logical unit. Chains can range from simple LLM calls to complex data processing flows.
*   **Agents:** Dynamic systems that use an LLM to decide which actions to take and in what order, based on available tools. Agents are designed to handle more open-ended tasks by reasoning.
*   **Tools:** Functions that agents can call to interact with the outside world, such as searching the web, querying a database, or performing calculations. Tools extend the capabilities of your [AI agents](#ai-agents).
*   **Memory:** Components that store and retrieve past interactions, providing conversational context to LLMs and agents. This is vital for stateful applications.

#### LangChain Architecture Explained

LangChain's architecture promotes a modular and composable design. At its heart, it's about chaining together different components. These components interact in a linear or directed acyclic graph (DAG) fashion to achieve a specific task.

For instance, a RAG workflow might involve a Retriever to fetch relevant documents, followed by a Prompt template to format the context, and finally an LLM to generate the answer. You define the flow, and LangChain manages the execution. This structure is excellent for sequential and predictable [LLM orchestration](#llm-orchestration).

Here's a simplified architectural overview:

| Component Category | Description                                                      | Example Components                                       |
| :----------------- | :--------------------------------------------------------------- | :------------------------------------------------------- |
| **Models**         | Interfaces for LLMs, ChatModels, and Embeddings                  | `ChatOpenAI`, `HuggingFaceEmbeddings`                    |
| **Prompts**        | Tools for constructing and optimizing prompts for LLMs           | `ChatPromptTemplate`, `MessagesPlaceholder`              |
| **Chains**         | Combining LLMs and other components into sequences               | `LLMChain`, `RunnableSequence`, `RetrievalQA`            |
| **Retrievers**     | Fetching relevant documents from a knowledge base                | `VectorStoreRetriever`, `MultiQueryRetriever`            |
| **Agents**         | LLMs that decide actions using tools                             | `create_react_agent`, `AgentExecutor`                    |
| **Tools**          | Functions an agent can use to interact with the environment      | `Tool`, `DuckDuckGoSearchRun`, custom tools              |
| **Memory**         | Persisting state between agent or chain runs                     | `ConversationBufferMemory`, `ChatMessageHistory`         |
| **Output Parsers** | Structuring the output from LLMs into desired formats            | `PydanticOutputParser`, `StrOutputParser`                |

#### Practical LangChain Example: Building a Simple RAG Workflow

Let's illustrate LangChain's power by building a basic RAG system. This system will answer questions based on a provided text document, extending beyond the LLM's initial training data. You'll see how to integrate different components seamlessly. For a more detailed guide, check out our [LangChain RAG tutorial]({% post_url 2026-11-04-langchain-rag-tutorial %}).

First, ensure you have the necessary libraries installed and an OpenAI API key configured.

{% raw %}
```python
# pip install langchain langchain-openai langchain-community chromadb
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# 1. Load a document
# Let's create a dummy document file
with open("paul_graham_essay.txt", "w") as f:
    f.write("""
    What I Worked On
    Paul Graham
    January 2021

    It's 2021, which means I've been working on startups for 25 years.
    I started my first startup, Viaweb, in 1995. We built software for
    building online stores. We sold it to Yahoo in 1998.

    After Yahoo, I started Y Combinator in 2005 with Jessica Livingston,
    Robert Morris, and Trevor Blackwell. Y Combinator funds startups.
    Some of the most famous companies that came out of YC include
    Dropbox, Airbnb, Stripe, and Reddit.

    My work has always been about making things, especially software.
    I love programming, and I believe in the power of small,
    focused teams to create great products.
    """)

loader = TextLoader("paul_graham_essay.txt")
documents = loader.load()

# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and store in a vector database
# Using an in-memory ChromaDB for simplicity
vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings())

# 4. Create a retriever
retriever = vectorstore.as_retriever()

# 5. Define the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 6. Set up the RAG chain using LangChain's RetrievalQA
# We'll use a specific prompt template for RAG
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant for question-answering tasks. "
                   "Use the following pieces of retrieved context to answer the question. "
                   "If you don't know the answer, just say that you don't know."),
        ("human", "Question: {question}\nContext: {context}")
    ]
)

# Initialize the RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm,
    chain_type="stuff", # 'stuff' means combining all retrieved docs into one prompt
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)

# 7. Ask a question
question = "When did Paul Graham start Y Combinator and what are some famous companies from it?"
result = qa_chain.invoke({"query": question})

print(f"Answer: {result['result']}")
print(f"Source Documents: {[doc.metadata for doc in result['source_documents']]}")
```
{% endraw %}

This example demonstrates how LangChain orchestrates multiple steps: loading, splitting, embedding, retrieving, and generating. This linear flow is ideal for many common tasks. For more insights into chunking strategies for RAG, refer to our post on [mastering LangChain RAG chunking]({% post_url 2026-11-05-mastering-langchain-rag-chunking %}).

### Introducing LangGraph: State, Cycles, and Advanced Agent Workflows

While LangChain excels at defining sequential or DAG-based workflows, it can become challenging for truly dynamic, stateful, and cyclical agent behaviors. This is where LangGraph steps in, building upon LangChain's core components to enable more sophisticated [graph-based workflows](#graph-based-workflows). LangGraph is an extension of LangChain, specifically designed for creating robust and resilient [multi-agent systems](#multi-agent-systems).

LangGraph addresses the need for explicit state management and complex control flow, including conditional routing and human-in-the-loop interactions. It allows you to model your AI applications as state machines. This capability is vital for building advanced [AI agents](#ai-agents) that can reason, take multiple steps, and recover from errors.

#### Why LangGraph? Limitations of Traditional LangChain

Traditional LangChain `AgentExecutor`s are powerful but have limitations when it comes to complex, multi-turn, and highly conditional interactions:

*   **State Management:** Agents typically pass a simple dictionary state, which can be cumbersome for intricate, persistent state across many turns.
*   **Arbitrary Control Flow:** While chains allow for sequences, complex conditionals, loops, or concurrent execution are harder to express natively.
*   **Observability:** Understanding the exact path an agent took, especially with multiple tool calls and re-tries, can be difficult.
*   **Cyclical Logic:** True conversational cycles or iterative refinement loops are challenging to implement cleanly within the standard `AgentExecutor` paradigm.

LangGraph provides a clearer, more explicit way to define these complex dynamics. It brings the concept of a "state machine" to agent design.

#### Core Concepts in LangGraph

LangGraph leverages graph theory to define the flow and state transitions of your AI application. This approach makes complex interactions more manageable and transparent.

*   **Graph:** The fundamental structure, defining nodes (computational steps) and edges (transitions between steps).
*   **Nodes:** Represent individual computational units or steps in your workflow. A node can be an LLM call, a tool invocation, a custom function, or even another LangChain chain.
*   **Edges:** Define the transitions between nodes. Edges can be fixed (always go from A to B) or conditional (go from A to B or A to C based on some output).
*   **State:** A shared object that is passed between nodes and updated by them. LangGraph's state allows for robust [state management](#state-management) across multiple steps and cycles.
*   **Checkpoints:** LangGraph can persist the state of your graph, enabling long-running conversations, recovery from failures, and human oversight.
*   **Entry/Exit Points:** Define where the graph starts and where it can terminate.

#### LangGraph Architecture Explained

LangGraph models your application as a directed graph where nodes are processing steps and edges define the flow. Unlike simple LangChain chains, LangGraph allows for arbitrary cycles and conditional routing, making it perfect for dynamic agent behavior. Each node receives the current state, performs an action, and returns an update to the state.

Think of it as a flowchart where each box is a node and arrows are edges. The power comes from being able to loop back, branch based on decisions, and maintain a consistent state throughout. This explicit [graph-based workflows](#graph-based-workflows) design significantly enhances control and clarity. For a deeper dive into agent orchestration with LangGraph, see our [LangGraph AI agent tutorial]({% post_url 2026-11-04-langgraph-ai-agent-tutorial %}) and [LangGraph multi-agent orchestration]({% post_url 2026-11-03-langgraph-multi-agent-orchestration %}).

Here's a conceptual diagram of a simple LangGraph workflow:

```
+---------------+      +-------------------+
|   Start Node  |----->|  LLM Decision Node |
+---------------+      +-------------------+
        ^                       |
        |                       | (Conditional)
        |                       V
        |               +-------------------+
        |               |    Tool Use Node  |<----+
        |               +-------------------+     |
        |                       |                   | (Retry/Refine)
        |                       V                   |
        +-----------------------+                   |
                Output Node <-----------------------+
```


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


#### Practical LangGraph Example: Building a Stateful Conversational Agent

Let's build a simple conversational agent using LangGraph that can decide whether to use a tool based on user input. This example highlights state management and conditional routing. We'll use a fake tool for demonstration purposes.

First, install the necessary libraries: `langchain_core`, `langgraph`, `langchain-openai`.

{% raw %}
```python
# pip install langchain_core langgraph langchain-openai
import os
from typing import TypedDict, Annotated, List, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# 1. Define the Agent State
# This is the state that will be passed between nodes in the graph
class AgentState(TypedDict):
    chat_history: Annotated[List[BaseMessage], lambda x, y: x + y]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    return_value: str
    intermediate_steps: Annotated[List[tuple[AgentAction, str]], lambda x, y: x + y]

# 2. Define Tools
@tool
def get_current_weather(location: str) -> str:
    """Gets the current weather for a given location."""
    if "london" in location.lower():
        return "It's rainy and 10°C in London."
    elif "paris" in location.lower():
        return "It's sunny and 18°C in Paris."
    else:
        return f"Sorry, I don't have weather information for {location}."

tools = [get_current_weather]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. Define the Agent Node (LLM for decision making)
def run_agent(state: AgentState):
    print("---RUN AGENT---")
    # Get the latest message from chat history
    current_message = state['chat_history'][-1]

    # Tool calling is typically done via structured output from LLMs
    # Here, we'll simulate an agent's decision to use a tool
    if "weather" in current_message.content.lower():
        # Simulate an AgentAction for weather tool
        # In a real LangChain agent, this would be generated by the LLM
        return AgentAction(tool="get_current_weather", tool_input={"location": current_message.content.split("for")[-1].strip()}, log="")
    else:
        # Simulate an AgentFinish for direct LLM response
        return AgentFinish(return_values={"output": f"I received your message: '{current_message.content}'. How can I help further?"}, log="")

# 4. Define the Tool Node
def run_tool(state: AgentState):
    print("---RUN TOOL---")
    agent_outcome = state['agent_outcome']
    if agent_outcome and isinstance(agent_outcome, AgentAction):
        tool_name = agent_outcome.tool
        tool_input = agent_outcome.tool_input
        selected_tool = next(t for t in tools if t.name == tool_name)
        tool_output = selected_tool.invoke(tool_input)

        # Update the state with tool output
        state['intermediate_steps'].append((agent_outcome, tool_output))
        state['chat_history'].append(HumanMessage(content=f"Tool output: {tool_output}")) # Add tool output to history
        state['return_value'] = tool_output # Store the tool output
    return state # Return the updated state

# 5. Define the End Node (where the final response is generated or returned)
def final_response_node(state: AgentState):
    print("---FINAL RESPONSE---")
    # This node could generate a final LLM response based on the state
    # For simplicity, we'll just return the current return_value or chat history
    if state.get('return_value'):
        print(f"Agent Final Response: {state['return_value']}")
        return state
    else:
        last_message = state['chat_history'][-1].content
        print(f"Agent Final Response: {last_message}")
        return state

# 6. Define the Conditional Edge
def decide_next_step(state: AgentState):
    print("---DECIDE NEXT STEP---")
    if isinstance(state['agent_outcome'], AgentAction):
        print("---Decision: TOOL---")
        return "call_tool"
    else:
        print("---Decision: END---")
        return "end_response"

# 7. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_agent)
workflow.add_node("call_tool", run_tool)
workflow.add_node("end_response", final_response_node)

workflow.set_entry_point("agent")

# Add edges
workflow.add_conditional_edges(
    "agent",  # From agent node
    decide_next_step,
    {
        "call_tool": "call_tool", # If agent decides to call tool, go to 'call_tool'
        "end_response": "end_response", # If agent decides to end, go to 'end_response'
    }
)

# After tool call, always go to end response for this simple example
workflow.add_edge("call_tool", "end_response")
workflow.add_edge("end_response", END) # Mark 'end_response' as a terminal node

app = workflow.compile()

# 8. Run the Agent
print("\n--- Running with Tool Use ---")
inputs = {"chat_history": [HumanMessage(content="What's the weather for London?")]}
for s in app.stream(inputs):
    print(s)

print("\n--- Running without Tool Use ---")
inputs = {"chat_history": [HumanMessage(content="Tell me a joke.")]}
for s in app.stream(inputs):
    print(s)
```
{% endraw %}

This example shows how `AgentState` is passed and updated, and how `decide_next_step` conditionally routes the execution. This explicit control over transitions and state makes LangGraph incredibly powerful for [multi-agent systems](#multi-agent-systems) and dynamic [LLM workflow orchestration](#llm-workflow-orchestration). You can learn more about building and coordinating multi-agent systems with LangGraph in our dedicated post on [LangGraph multi-agent coordination]({% post_url 2026-11-07-langgraph-multi-agent-coordination %}).

### LangChain vs LangGraph: A Deep Dive Comparison

While LangChain and LangGraph are closely related and often used together, they serve different primary purposes. Understanding their distinct advantages helps you choose the right tool for your specific [LangChain LangGraph Workflows](#langchain-langgraph-workflows).

#### Key Differences and Use Cases

Let's break down the core distinctions in a comparison table:

| Feature             | LangChain (Core)                                         | LangGraph                                                      |
| :------------------ | :------------------------------------------------------- | :------------------------------------------------------------- |
| **Primary Focus**   | Component library, sequential/DAG chains, basic agents | State machine for multi-step agent behaviors, complex control flow, cycles |
| **Control Flow**    | Linear sequences, directed acyclic graphs (DAGs)       | Arbitrary graphs with nodes, edges, conditionals, cycles       |
| **State Management**| Implicit via `AgentExecutor` or explicit in simple chains, often passed as a dict. Limited persistence. | Explicit, mutable `State` object passed between nodes. Checkpointing for persistence. |
| **Complexity**      | Suited for straightforward tasks, single-turn agents, RAG | Ideal for complex, multi-turn, stateful, and iterative agents; multi-agent systems |
| **Agent Design**    | `AgentExecutor` handles simple tool use and response cycles | Enables explicit modeling of agent "thoughts," actions, and observations as graph nodes. Finite state machines. |
| **Observability**   | Trace logs from `AgentExecutor`                         | Graph visualization (with libraries like `mermaid`), clear state transitions |
| **Best For**        | Simple chatbots, RAG applications, data processing pipelines, initial agent prototyping | Conversational AI, multi-agent collaboration, autonomous agents, human-in-the-loop systems, iterative refinement |
| **Relationship**    | LangGraph builds *on* LangChain components. Nodes in LangGraph can be LangChain chains, LLMs, or tools. | Extends LangChain's capabilities for complex agent behaviors. |

#### When to Use LangChain (Core)

You should primarily use LangChain's core components when:

*   **Building simple, sequential workflows:** If your task involves a clear sequence of steps (e.g., retrieving data, formatting, then generating), LangChain chains are perfect.
*   **Implementing basic RAG applications:** For standard Retrieval Augmented Generation, LangChain provides all the necessary components like retrievers, vector stores, and RAG chains.
*   **Rapid Prototyping:** Its ease of use and rich component library allow for quick development of initial LLM-powered features.
*   **Single-turn agent interactions:** When an agent needs to perform one or a few tool calls and then respond, without complex internal loops or state.
*   **Data processing with LLMs:** Using LLMs to extract information, summarize documents, or classify text in a pipeline fashion.

#### When to Use LangGraph

LangGraph becomes indispensable for scenarios demanding advanced control and state:

*   **Complex Conversational Agents:** When your agent needs to maintain rich context, adapt its behavior over multiple turns, or handle interruptions. This is crucial for truly intelligent [AI agents](#ai-agents).
*   **Multi-Agent Systems:** Orchestrating multiple specialized agents that collaborate, delegate tasks, and refine results iteratively. Think of a team of experts.
*   **Autonomous Agents:** Designing agents that can plan, execute, observe results, and self-correct, often involving cycles of reasoning and action.
*   **Human-in-the-Loop Workflows:** When you need explicit points for human review, approval, or intervention within a complex AI process.
*   **Stateful Systems:** Any application where the internal state needs to be explicitly managed, inspected, and potentially persisted for long-running interactions or recovery.
*   **Implementing custom agent logic:** If `AgentExecutor`'s fixed decision loop is too restrictive, LangGraph gives you full control over the agent's "thought" process.

#### How They Complement Each Other

It's not truly LangChain *vs* LangGraph; it's often LangChain *and* LangGraph. LangGraph is an extension built *on top* of LangChain.

*   You use LangChain components (LLMs, tools, chains, parsers) *within* the nodes of a LangGraph workflow.
*   LangGraph provides the "operating system" for your agents, while LangChain provides the "applications" (the individual LLM calls, tools, and chains) that run on that system.
*   This synergistic relationship allows you to leverage LangChain's vast ecosystem of integrations and components while gaining LangGraph's superior control over complex execution flows and [state management](#state-management).

For instance, a LangGraph node could be a `RetrievalQA` chain from LangChain, a tool invocation, or even a custom prompt engineering step using LangChain's prompt templates. This modularity empowers you to build highly sophisticated [LangChain LangGraph Workflows](#langchain-langgraph-workflows).

### Building Advanced AI Workflows: Practical Examples

Let's dive into more complex scenarios to demonstrate how LangGraph, often in conjunction with LangChain components, enables sophisticated [LLM orchestration](#llm-orchestration) and [multi-agent systems](#multi-agent-systems).

#### Example 1: A Multi-Agent Research System with LangGraph

Imagine building a system where different AI agents collaborate to research a topic. One agent finds information, another summarizes, and a third critiques the summary. This is a classic use case for [multi-agent systems](#multi-agent-systems) and [graph-based workflows](#graph-based-workflows) that LangGraph excels at.

**Problem:** Answer a complex question by researching, summarizing, and then critiquing the summary.

**Architecture:**
*   **Researcher Agent:** Uses a search tool to find relevant information.
*   **Summarizer Agent:** Takes research results and condenses them.
*   **Critic Agent:** Evaluates the summary for completeness, accuracy, and bias, providing feedback.
*   **Coordinator:** A LangGraph state machine orchestrates these agents.

**Shared State:** We need a state that holds the query, research results, summary, and critique.

First, set up your environment and imports.

{% raw %}
```python
# pip install langchain langchain-openai langchain-community langgraph beautifulsoup4
import os
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from langgraph.graph import StateGraph, END

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Define the state for the multi-agent system
class ResearchState(TypedDict):
    query: str
    research_results: Annotated[List[str], lambda x, y: x + y]
    summary: str
    critique: str
    num_critiques: int # To limit critique loops

# Define Tools (using a dummy search tool for simplicity)
@tool
def dummy_search(query: str) -> str:
    """Searches the internet for information on a given query."""
    print(f"---SEARCHING FOR: {query}---")
    if "quantum computing" in query.lower():
        return "Quantum computing uses quantum-mechanical phenomena like superposition and entanglement to perform computations. It can solve problems intractable for classical computers, such as factoring large numbers and simulating complex molecules. Companies like IBM, Google, and Microsoft are leading its development."
    elif "artificial intelligence" in query.lower():
        return "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines programmed to think like humans and mimic their actions. It encompasses machine learning, deep learning, natural language processing, and computer vision. AI is transforming various industries, from healthcare to finance."
    else:
        return f"No specific research results found for '{query}'. This is a placeholder result."

tools = [dummy_search]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


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


# Helper function to create an agent
def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"), # Placeholder for chat history, not strictly used in this agent logic
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    return executor

# Define Agent Nodes
def researcher_node(state: ResearchState):
    print("---RESEARCHER NODE---")
    query = state["query"]
    system_prompt = "You are a diligent researcher. Use the search tool to find comprehensive information about the user's query."
    researcher_agent = create_agent(llm, tools, system_prompt)

    # LangChain AgentExecutor requires 'input'
    result = researcher_agent.invoke({"input": query, "chat_history": []})

    # Assume the output from agent is directly the research results
    # In a real scenario, you might parse `result['output']` more carefully
    research_output = result['output']

    # Update state
    return {"research_results": [research_output]}

def summarizer_node(state: ResearchState):
    print("---SUMMARIZER NODE---")
    research_results = "\n".join(state["research_results"])
    query = state["query"]

    # Use LLM to summarize
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a skilled summarizer. Condense the provided research results into a concise summary, addressing the original query. Highlight key facts and findings."),
        ("human", f"Original Query: {query}\n\nResearch Results:\n{research_results}\n\nProvide a summary:")
    ])
    chain = prompt | llm
    summary = chain.invoke({"query": query, "research_results": research_results}).content

    # Update state
    return {"summary": summary}

def critic_node(state: ResearchState):
    print("---CRITIC NODE---")
    summary = state["summary"]
    research_results = "\n".join(state["research_results"])
    query = state["query"]

    # Use LLM to critique
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a critical reviewer. Evaluate the provided summary against the original research results and query. Point out any missing key information, inaccuracies, or biases. Suggest improvements."),
        ("human", f"Original Query: {query}\n\nResearch Results:\n{research_results}\n\nSummary to Critique:\n{summary}\n\nCritique the summary and suggest improvements:")
    ])
    chain = prompt | llm
    critique = chain.invoke({"query": query, "research_results": research_results, "summary": summary}).content

    # Update state
    return {"critique": critique, "num_critiques": state.get("num_critiques", 0) + 1}

# Conditional Edge: Decide if summary needs refinement
def decide_to_refine(state: ResearchState):
    print("---DECIDE TO REFINE---")
    # A simple heuristic: if critique suggests "missing information" or "inaccurate"
    # and we haven't critiqued too many times, refine.
    # In a real system, this would be more sophisticated (e.g., LLM to decide)

    if "missing information" in state["critique"].lower() or "inaccurate" in state["critique"].lower():
        if state["num_critiques"] < 2: # Limit refinement loops
            print("---Decision: REFINE---")
            return "summarize" # Go back to summarizer
    print("---Decision: END---")
    return "end"

# Build the LangGraph Workflow
workflow = StateGraph(ResearchState)

workflow.add_node("research", researcher_node)
workflow.add_node("summarize", summarizer_node)
workflow.add_node("critique", critic_node)

workflow.set_entry_point("research")

workflow.add_edge("research", "summarize")
workflow.add_edge("summarize", "critique")

workflow.add_conditional_edges(
    "critique",
    decide_to_refine,
    {
        "summarize": "summarize", # If critique requires refinement, go back to summarize
        "end": END               # Otherwise, end the workflow
    }
)

app = workflow.compile()

# Run the multi-agent system
final_state = app.invoke({"query": "Explain quantum computing and its applications.", "research_results": [], "summary": "", "critique": "", "num_critiques": 0})

print("\n--- FINAL OUTPUT ---")
print(f"Query: {final_state['query']}")
print(f"Research Results: {final_state['research_results']}")
print(f"Final Summary: {final_state['summary']}")
print(f"Critique: {final_state['critique']}")
print(f"Number of Critiques: {final_state['num_critiques']}")

final_state_ai = app.invoke({"query": "What is Artificial Intelligence?", "research_results": [], "summary": "", "critique": "", "num_critiques": 0})
print("\n--- FINAL OUTPUT for AI ---")
print(f"Query: {final_state_ai['query']}")
print(f"Final Summary: {final_state_ai['summary']}")
print(f"Critique: {final_state_ai['critique']}")
```
{% endraw %}

This example shows a powerful pattern: agents collaborating, passing state, and conditionally looping for refinement. The `num_critiques` in the state ensures we don't get stuck in an infinite loop. This explicit orchestration is a hallmark of effective [LangChain LangGraph Workflows](#langchain-langgraph-workflows).

#### Example 2: Stateful Conversational AI with Tool Use and LangGraph

Combining LangGraph's state management with LangChain's tool-use capabilities allows for highly interactive and persistent conversational agents. You can build agents that remember past interactions and intelligently decide when and how to use external tools.

**Problem:** Create a customer support agent that can answer FAQs (using RAG) and also look up order statuses (using a tool), remembering previous turns.

**Architecture:**
*   **Chat History:** Stored in LangGraph's state.
*   **LLM Decision Node:** An LLM decides if a tool is needed or if it can answer directly.
*   **Tool Node:** Invokes a custom tool (e.g., `get_order_status`).
*   **RAG Node:** Uses a LangChain `RetrievalQA` chain for FAQ answering.
*   **Response Node:** Formulates the final user-facing answer.

Let's expand on our previous LangGraph example.

{% raw %}
```python
# pip install langchain langchain-openai langchain-community langgraph chromadb
import os
from typing import TypedDict, Annotated, List, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# 1. Define the Agent State
class ConversationalAgentState(TypedDict):
    chat_history: Annotated[List[BaseMessage], lambda x, y: x + y]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    tool_output: str
    intermediate_steps: Annotated[List[tuple[AgentAction, str]], lambda x, y: x + y]

# 2. Define Tools
@tool
def get_order_status(order_id: str) -> str:
    """Retrieves the current status of a customer order."""
    if order_id == "12345":
        return "Order 12345: Shipped, ETA tomorrow."
    elif order_id == "67890":
        return "Order 67890: Processing."
    else:
        return f"Order {order_id}: Not found."

tools = [get_order_status]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Setup a simple RAG system for FAQs
# Create a dummy FAQ document
with open("faqs.txt", "w") as f:
    f.write("""
    FAQ Document:

    Q: What is your return policy?
    A: We offer a 30-day return policy for unused items with original packaging.

    Q: How can I contact customer support?
    A: You can reach us via email at support@example.com or call us at 1-800-123-4567 during business hours.

    Q: Do you ship internationally?
    A: Yes, we ship to over 100 countries worldwide. Shipping fees apply.
    """)

loader = TextLoader("faqs.txt")
faq_docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
faq_chunks = text_splitter.split_documents(faq_docs)
faq_vectorstore = Chroma.from_documents(faq_chunks, OpenAIEmbeddings())
faq_retriever = faq_vectorstore.as_retriever()

rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant answering customer questions based on the provided FAQs. "
                   "If you cannot find the answer in the FAQs, simply state that you don't know."),
        ("human", "Question: {question}\nContext: {context}")
    ]
)

faq_qa_chain = RetrievalQA.from_chain_type(
    llm,
    chain_type="stuff",
    retriever=faq_retriever,
    chain_type_kwargs={"prompt": rag_prompt}
)

# 3. Define the Agent Node (LLM for decision making and direct responses)
def call_llm_or_agent(state: ConversationalAgentState):
    print("---CALL LLM OR AGENT NODE---")
    messages = state["chat_history"]

    # Try to use LangChain's create_openai_functions_agent for tool calling
    # This acts as the "brain" deciding to use a tool or directly respond
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful customer support agent. You have access to tools to assist the user. "
                       "If the user asks about order status, use the 'get_order_status' tool. "
                       "Otherwise, try to answer directly or indicate if you need more info."),
            ("placeholder", "{chat_history}"), # This will be filled by LangGraph
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # We pass tools to the LLM to enable function calling
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

    # The agent_executor takes the latest human message as input
    response = agent_executor.invoke({"input": messages[-1].content, "chat_history": messages[:-1]})

    # The agent_executor output could be a direct answer or a tool invocation
    if isinstance(response['output'], AgentAction):
        # This branch won't be hit directly with AgentExecutor.invoke,
        # as it returns the final answer or executes the tool directly.
        # For LangGraph, we need to explicitly return the AgentAction
        return {"agent_outcome": response['output']}
    else:
        # If agent_executor produced a direct answer
        return {"chat_history": [AIMessage(content=response['output'])], "agent_outcome": AgentFinish(return_values={"output": response['output']}, log="")}

# 4. Define the Tool Node
def call_tool(state: ConversationalAgentState):
    print("---CALL TOOL NODE---")
    agent_outcome = state['agent_outcome']

    if isinstance(agent_outcome, AgentAction):
        tool_name = agent_outcome.tool
        tool_input = agent_outcome.tool_input
        selected_tool = next(t for t in tools if t.name == tool_name)
        tool_output = selected_tool.invoke(tool_input)

        # Add tool output to chat history and intermediate steps
        state['chat_history'].append(AIMessage(content=f"Tool Used: {tool_name}, Output: {tool_output}"))
        state['intermediate_steps'].append((agent_outcome, tool_output))
        state['tool_output'] = tool_output # Store for potential final response
    return state

# 5. Define the RAG Node for FAQ
def call_rag(state: ConversationalAgentState):
    print("---CALL RAG NODE---")
    question = state["chat_history"][-1].content # Last user message
    rag_response = faq_qa_chain.invoke({"query": question})

    rag_answer = rag_response['result']


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


    # Add RAG answer to chat history
    state['chat_history'].append(AIMessage(content=rag_answer))
    return state

# 6. Define the Conditional Edges
def decide_what_to_do(state: ConversationalAgentState):
    print("---DECIDE WHAT TO DO---")
    last_message_content = state["chat_history"][-1].content.lower()

    if "order status" in last_message_content:
        # If the user is asking about order status, we assume the LLM (in call_llm_or_agent)
        # would have decided to use the get_order_status tool.
        # This conditional is a simplification for routing.
        # A more robust solution would inspect agent_outcome for AgentAction.
        return "call_tool"
    elif "faq" in last_message_content or "question" in last_message_content or "return policy" in last_message_content:
        return "call_rag"
    else:
        # If no specific tool or RAG needed, let the LLM give a direct answer
        return "final_response"

def decide_after_tool_or_rag(state: ConversationalAgentState):
    print("---DECIDE AFTER TOOL OR RAG---")
    # After a tool call or RAG, we can go straight to the final response
    return "final_response"

# 7. Build the Graph
workflow = StateGraph(ConversationalAgentState)

workflow.add_node("llm_decision", call_llm_or_agent)
workflow.add_node("call_tool", call_tool)
workflow.add_node("call_rag", call_rag)
workflow.add_node("final_response", lambda state: state) # Simply pass state to END

workflow.set_entry_point("llm_decision")

# The LLM decision node itself will update the chat_history.
# We then need to decide if a tool was implicitly called or if we have a direct answer.
# For this example, let's simplify routing based on user input for clarity.
workflow.add_conditional_edges(
    "llm_decision",
    decide_what_to_do,
    {
        "call_tool": "call_tool",
        "call_rag": "call_rag",
        "final_response": "final_response",
    }
)

workflow.add_edge("call_tool", "final_response")
workflow.add_edge("call_rag", "final_response")
workflow.add_edge("final_response", END)

app = workflow.compile()

# 8. Run the Conversational Agent
print("\n--- Conversational Agent - Order Status ---")
inputs1 = {"chat_history": [HumanMessage(content="What's the status of order 12345?")]}
for s in app.stream(inputs1):
    print(s)

print("\n--- Conversational Agent - FAQ ---")
inputs2 = {"chat_history": [HumanMessage(content="What is your return policy?")]}
for s in app.stream(inputs2):
    print(s)

print("\n--- Conversational Agent - General Query ---")
inputs3 = {"chat_history": [HumanMessage(content="Hello there!")]}
for s in app.stream(inputs3):
    print(s)

print("\n--- Conversational Agent - Unknown Order ---")
inputs4 = {"chat_history": [HumanMessage(content="What's the status of order 99999?")]}
for s in app.stream(inputs4):
    print(s)
```
{% endraw %}

This sophisticated agent demonstrates how LangGraph can orchestrate different types of actions (LLM direct response, tool use, RAG) based on context and state. The `chat_history` is continuously updated, maintaining the conversation's flow. This pattern is essential for building dynamic and context-aware [LangChain LangGraph Workflows](#langchain-langgraph-workflows).

### Best Practices for LangChain and LangGraph Development

Building robust AI workflows requires more than just knowing the syntax. Adhering to best practices ensures your applications are scalable, maintainable, and performant.

#### Modularity and Reusability

*   **Break down complex tasks:** Decompose your workflows into smaller, manageable LangChain components or LangGraph nodes. Each node should ideally have a single responsibility.
*   **Encapsulate logic:** Wrap common patterns (e.g., a specific RAG chain, a complex tool invocation) into reusable functions or custom LangChain runnables. This promotes clean code.
*   **Define clear interfaces:** Ensure the inputs and outputs of your components and nodes are well-defined, making integration smoother.

#### State Management

*   **Design your state carefully:** For LangGraph, think about all the information your agents need across turns. Make your `TypedDict` for state comprehensive yet lean.
*   **Immutable updates:** While LangGraph's state is mutable, try to design nodes to return new state objects or clearly define how they modify existing ones.
*   **Checkpointing:** Utilize LangGraph's checkpointing for long-running conversations or critical [state management](#state-management) where you might need to restart or review.

#### Observability and Debugging

*   **Verbose logging:** Enable `verbose=True` in `AgentExecutor` or add print statements within your LangGraph nodes. This helps trace execution flow.
*   **LangChain Callbacks:** Leverage LangChain's callback system to monitor LLM calls, tool usage, and chain execution.
*   **Graph Visualization:** For complex LangGraph workflows, visualize the graph (e.g., with Mermaid or Graphviz) to understand possible paths.

#### Prompt Engineering

*   **Iterate and refine prompts:** Prompts are critical. Test different phrasings, few-shot examples, and instructions to get desired behavior from your LLMs.
*   **System Messages:** Use clear system messages to define the role and constraints of your agents.
*   **Tool Descriptions:** Write precise and informative tool descriptions. The LLM relies on these to decide when and how to use tools effectively.

#### Evaluation and Testing

*   **Unit Tests:** Write unit tests for individual LangChain components, tools, and LangGraph nodes.
*   **End-to-End Tests:** Develop integration tests for your entire [AI agents](#ai-agents) and workflows.
*   **Quantitative Evaluation:** Use metrics and datasets to [evaluate LangChain agents]({% post_url 2026-11-06-evaluate-langchain-agents %}) systematically. This is crucial for performance improvements.
*   **Human-in-the-Loop:** For critical applications, integrate human review into your testing process.

#### Performance and Optimization

*   **Caching:** Implement caching for LLM calls and expensive tool invocations to reduce latency and API costs.
*   **Batching:** When possible, batch multiple LLM calls or retrievals.
*   **Model Selection:** Choose appropriate LLM models (e.g., smaller, faster models for simple tasks, larger models for complex reasoning).
*   **Asynchronous Operations:** Utilize `async/await` for concurrent operations where possible to improve throughput.

### Advanced Topics and Integrations

The world of AI workflows is constantly expanding. Both LangChain and LangGraph are designed to be extensible, allowing you to integrate cutting-edge capabilities.

#### Multimodal Agents

Modern LLMs are increasingly multimodal, capable of processing and generating various data types like text, images, and audio. You can extend your [LangChain LangGraph Workflows](#langchain-langgraph-workflows) to incorporate these capabilities. For instance, an agent might analyze an image, then use its textual description to perform a search.
You can explore how to build such systems by referencing our guide on [building multimodal agents with LangChain and Gemini]({% post_url 2026-11-08-build-multimodal-agents-langchain-gemini %}).

#### Serverless Deployments

Deploying complex AI agents can be challenging, but serverless platforms offer scalable and cost-effective solutions. You can package your LangChain and LangGraph applications into serverless functions (e.g., AWS Lambda, Google Cloud Functions) or containers (e.g., AWS Fargate). This enables your [LangChain LangGraph Workflows](#langchain-langgraph-workflows) to scale on demand without managing infrastructure.
Learn more about deploying such systems in a serverless environment with our article on [serverless LangChain agents on AWS Fargate]({% post_url 2026-11-07-serverless-langchain-agents-data-lake-aws-fargate %}).

#### Integrating with Other Systems

LangChain and LangGraph are designed to be part of larger software ecosystems. You can integrate them with:

*   **Databases:** For persistent storage of chat history, user profiles, or specific knowledge bases.
*   **APIs:** Connect to any external service (CRM, ERP, payment gateways) via custom tools.
*   **Monitoring and Observability Tools:** Link with platforms like LangSmith, Weights & Biases, or custom logging solutions to gain deep insights into agent behavior.
*   **User Interfaces:** Build interactive frontends (e.g., Streamlit, Gradio, web apps) to interact with your agents.

### Conclusion

You've embarked on a comprehensive journey through LangChain and LangGraph, two indispensable frameworks for building sophisticated [LangChain LangGraph Workflows](#langchain-langgraph-workflows) in Python. LangChain provides the robust components for interacting with LLMs and structuring basic chains, making it perfect for tasks like RAG and straightforward agents. LangGraph, building upon LangChain, empowers you to construct complex, stateful, and cyclical [multi-agent systems](#multi-agent-systems) through its intuitive graph-based approach.

By understanding their individual strengths and how they complement each other, you are now equipped to design and implement advanced [AI agents](#ai-agents) that can reason, adapt, and collaborate. The future of AI applications hinges on such intelligent orchestration, and with LangChain and LangGraph, you have powerful tools at your disposal to shape that future. Continue experimenting, building, and pushing the boundaries of what's possible with AI.

### Frequently Asked Questions (FAQs)

#### Q1: What is the main difference between LangChain and LangGraph?
A1: LangChain is a general framework for building LLM applications, offering components for chains, agents, tools, and memory. LangGraph is an extension of LangChain specifically designed for creating stateful, multi-step agent workflows with arbitrary control flow, including cycles and conditionals. LangGraph excels at explicit [state management](#state-management) and orchestrating complex [multi-agent systems](#multi-agent-systems).

#### Q2: Can I use LangChain components within LangGraph?
A2: Absolutely, and this is a common and recommended practice. LangGraph nodes can encapsulate any LangChain runnable, such as LLMs, tools, or entire LangChain chains. LangGraph provides the orchestration layer, while LangChain provides the individual building blocks.

#### Q3: When should I choose LangGraph over a traditional LangChain AgentExecutor?
A3: Choose LangGraph when you need explicit control over an agent's internal thought process, require complex conditional routing, need to implement iterative refinement loops, or are building [multi-agent systems](#multi-agent-systems) where agents collaborate. If your agent needs to maintain rich, mutable state across many steps or handle human intervention points, LangGraph is the better choice. For simpler, linear agent tasks, a LangChain `AgentExecutor` might suffice.

#### Q4: Is LangGraph harder to learn than LangChain?
A4: LangGraph introduces new concepts like nodes, edges, and state graphs, which can have a slightly steeper learning curve initially compared to LangChain's more linear chains. However, for complex [AI agents](#ai-agents), the explicit structure of LangGraph often makes the overall application logic clearer and easier to debug in the long run.

#### Q5: How do I manage state in LangGraph?
A5: In LangGraph, state is typically managed using a `TypedDict` that defines the shared information passed between nodes. Each node receives the current state, performs its computation, and returns an update to the state. LangGraph then merges these updates into the central state object. You can also use checkpointing to persist this state.

#### Q6: Are there any performance considerations when using LangGraph?
A6: While LangGraph adds a layer of abstraction, its performance overhead is generally minimal. The primary performance factors will still be the speed of your LLMs, external tool calls, and data retrieval processes. Careful design of your graph to minimize unnecessary steps and optimize node execution is key. As with any complex system, effective caching and asynchronous operations can significantly improve throughput for your [LangChain LangGraph Workflows](#langchain-langgraph-workflows).

#### Q7: What kind of [AI agents](#ai-agents) can I build with LangGraph?
A7: You can build a wide array of advanced [AI agents](#ai-agents) with LangGraph, including:
*   **Conversational AI:** Agents that maintain context, use tools, and provide multi-turn responses.
*   **Autonomous Research Agents:** Systems that can plan research, execute searches, summarize, and critique findings.
*   **Customer Support Bots:** Agents that can diagnose issues, query databases, and escalate to human agents when needed.
*   **Code Generation and Refinement Agents:** Agents that iteratively generate, test, and debug code.
*   **Human-in-the-Loop Systems:** Workflows where human input or approval is required at specific stages.