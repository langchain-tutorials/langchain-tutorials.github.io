---
title: "Master LangChain: Build Advanced AI Apps with Python - A Full Guide"
description: "Learn LangChain Python with this full tutorial. Build advanced AI apps and integrate LLMs to create powerful production-ready solutions."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: ["LangChain", "Python", "AI Development", "LLMs", "RAG"]
featured: false
image: '/assets/images/langchain-python-complete-guide.webp'
---
## Master LangChain: Build Advanced AI Apps with Python - A Full Guide

Master AI with LangChain Python, the revolutionary framework transforming how developers build intelligent applications. This comprehensive guide will walk you through every essential aspect, from foundational concepts to advanced `LangChain integrations`. You'll learn to `build AI apps` that leverage the power of Large Language Models (LLMs) with remarkable efficiency and creativity.

Whether you're looking for a `LangChain Python tutorial` for beginners or an in-depth dive into `LLM applications`, you've come to the right place. We'll explore `RAG systems`, `LangChain agents`, `prompt engineering`, and much more. By the end of this `LangChain tutorial`, you'll be equipped to create sophisticated, production-ready AI solutions.

### 1. Introduction to LangChain and Its Importance

LangChain is an open-source framework designed to simplify the development of applications powered by language models. It provides a structured way to combine various components, enabling complex interactions beyond simple API calls. With LangChain, you can chain together LLMs, external data sources, and computational tools.

This framework is essential for modern `Python AI development` because it addresses the core challenges of building `LLM applications`. It helps manage context, orchestrate multiple model calls, and integrate diverse data sources. For developers, this means faster development cycles and more robust AI products.

You can leverage LangChain to create anything from intelligent chatbots to data analysis tools and autonomous agents. This `LangChain Python tutorial` aims to provide you with the practical knowledge to bring your AI ideas to life.

### 2. Getting Started with LangChain

Before we dive into advanced topics, let's set up your development environment and run a basic LangChain example. You'll need Python 3.8+ installed on your system. We will also cover essential configuration for LLM access.

#### 2.1. Installation

First, install the LangChain library using pip. You might also need specific integrations, like `langchain-openai` for OpenAI models or `langchain-community` for general utilities.

```python
pip install langchain langchain-openai langchain-community
```

For specific vector stores, document loaders, or other tools, you'll install their respective packages. For example, `pip install pypdf` for PDF loading or `pip install qdrant-client` for Qdrant.

#### 2.2. Environment Setup and API Keys

Most LLMs require an API key for access. It's best practice to store these securely, typically as environment variables. Create a `.env` file in your project root or set them directly in your shell.

```bash
# .env file content
OPENAI_API_KEY="your_openai_api_key_here"
# Add other keys like HUGGINGFACEHUB_API_TOKEN, etc.
```

To load these variables in your Python script, you can use the `dotenv` library. Install it with `pip install python-dotenv`.

```python
import os
from dotenv import load_dotenv

load_dotenv() # This loads variables from .env file

# Now you can access them
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Warning: OPENAI_API_KEY not set. Please set it in your environment or .env file.")
```

#### 2.3. Your First LangChain Interaction

Let's start with a simple interaction using an OpenAI model. This will demonstrate the basic flow: model initialization, prompt, and response.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Initialize the ChatModel
# You can specify the model name, e.g., "gpt-4" or "gpt-3.5-turbo"
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 2. Define a simple prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Answer the user's questions concisely."),
    ("user", "{question}")
])

# 3. Create a chain by combining the prompt and the LLM
chain = prompt | llm

# 4. Invoke the chain with your question
response = chain.invoke({"question": "What is the capital of France?"})

# 5. Print the response content
print(response.content)
```

This simple `LangChain Python example` shows how to string together a prompt and an LLM. The `|` operator is part of LangChain Expression Language (LCEL), which we'll explore further.

### 3. LangChain Core Components and LCEL

LangChain is built around several core abstractions, and LCEL makes it easy to combine them. Understanding these components is key to building advanced `LLM applications`.

#### 3.1. Models: LLMs and ChatModels

LangChain provides interfaces for different types of language models.
*   **LLMs**: Interact with text completion models (e.g., `text-davinci-003`). These typically take a string and return a string.
*   **ChatModels**: Interact with chat-based models (e.g., `gpt-3.5-turbo`, `gpt-4`). These take a list of message objects (system, human, AI) and return a message object.

ChatModels are generally preferred for conversational AI due to their structured input/output. You saw `ChatOpenAI` in the previous example.

#### 3.2. Prompt Engineering: Templates and Messages

`Prompt engineering` is the art of crafting effective inputs for LLMs. LangChain provides powerful tools for this.
*   **Prompt Templates**: Allow you to define reusable prompt structures with placeholders.
*   **Chat Message History**: Manages the list of `HumanMessage`, `AIMessage`, and `SystemMessage` objects for conversational context.

```python
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# A simple chat prompt template with a variable
chat_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant named {name}."),
    HumanMessagePromptTemplate.from_template("{query}")
])

# Example of messages for conversational context
messages = [
    HumanMessage(content="Hello there!"),
    AIMessage(content="Hello! How can I assist you today?"),
    HumanMessage(content="What is LangChain?")
]

# You can also use MessagesPlaceholder for dynamic message history in chains
conversation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly chatbot."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")
])
```

#### 3.3. Output Parsers: Structured Responses


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


LLMs often return free-form text. `Output parsers` help extract structured information, like JSON or specific data types, from these responses. This is crucial for integrating LLM outputs into other parts of your `Python AI development` workflow.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Simple string output parser
string_parser = StrOutputParser()

# Pydantic-based structured output parser
class Joke(BaseModel):
    setup: str = Field(description="the setup of the joke")
    punchline: str = Field(description="the punchline of the joke")

json_parser = JsonOutputParser(pydantic_object=Joke)

# Prompt with instructions for JSON output
json_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Output your response as JSON according to the following schema: {schema}"),
    ("user", "Tell me a short joke about a {topic}.")
]).partial(schema=json_parser.get_format_instructions())

json_chain = json_prompt | llm | json_parser

# Invoke and get a structured JSON object
joke_output = json_chain.invoke({"topic": "programmer"})
print(joke_output)
# Expected output (might vary slightly): {'setup': 'Why do programmers prefer dark mode?', 'punchline': 'Because light attracts bugs!'}
```

#### 3.4. Chains and LangChain Expression Language (LCEL)

Chains are sequences of components that run in a particular order. LCEL provides a powerful and flexible way to compose these chains. It uses the `|` operator for sequential composition.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
output_parser = StrOutputParser()

# Define a simple chain: Prompt -> LLM -> Output Parser
prompt = ChatPromptTemplate.from_template("Tell me a fun fact about {animal}.")
fun_fact_chain = prompt | llm | output_parser

# Invoke the chain
result = fun_fact_chain.invoke({"animal": "pandas"})
print(result)
```

LCEL allows for more complex structures:
*   **Parallel execution**: Using `RunnableParallel`.
*   **Conditional logic**: Using `RunnableLambda` with `if/else`.
*   **Fallbacks**: For robust error handling.

This declarative style is excellent for building and visualizing complex `LLM applications`.

### 4. Retrieval Augmented Generation (RAG) Systems

`RAG systems` are a cornerstone of advanced `LLM applications`, allowing models to access and utilize external, up-to-date, and domain-specific information. This overcomes the limitations of an LLM's pre-trained knowledge. You can find more details on different frameworks for RAG in [RAG Frameworks: LangChain, LangGraph, LlamaIndex]({% post_url 2026-11-11-rag-frameworks-langchain-langgraph-llamaindex %}).

#### 4.1. The RAG Architecture

A typical RAG system involves several steps:

1.  **Document Loading**: Ingesting data from various sources (PDFs, websites, databases).
2.  **Text Splitting (Chunking)**: Breaking down large documents into smaller, manageable chunks. This is crucial for fitting content into the LLM's context window. Dive deeper into this with [LangChain RAG Chunking Strategies]({% post_url 2026-11-11-langchain-rag-chunking-strategies %}).
3.  **Embedding**: Converting text chunks into numerical vector representations (embeddings).
4.  **Vector Store**: Storing these embeddings along with their original text. This allows for efficient semantic search.
5.  **Retrieval**: When a query comes in, finding the most relevant chunks from the vector store based on semantic similarity.
6.  **Generation**: Passing the retrieved chunks along with the user's query to the LLM to generate an informed response.

#### 4.2. Building a Basic RAG Chain

Let's build a simple `LangChain RAG tutorial` example. We'll load a document, chunk it, embed it, store it in a vector database (Chroma, a local one), and then query it.

```python
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Ensure your OPENAI_API_KEY is set in environment variables or .env file
# load_dotenv() # Uncomment if you're using .env

# 1. Prepare some data
# Create a dummy text file for demonstration
with open("my_document.txt", "w") as f:
    f.write("LangChain is a framework for developing applications powered by large language models. "
            "It enables applications to be data-aware and agentic. "
            "LangChain is available as a Python package and a JavaScript package. "
            "It was founded by Harrison Chase.")

# 2. Load the document
loader = TextLoader("my_document.txt")
docs = loader.load()

# 3. Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# 4. Create embeddings and a vector store
# You need an embedding model; OpenAIEmbeddings is a common choice.
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# 5. Define a retriever
# This will fetch the most relevant chunks from the vector store.
retriever = vectorstore.as_retriever()

# 6. Set up the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 7. Define the RAG prompt
# The 'context' variable will be populated by the retriever
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
               "If you don't know the answer, just say that you don't know.\n\n"
               "Context: {context}"),
    ("user", "{question}")
])

# 8. Construct the RAG chain using LCEL
# The 'context' key is created by piping the input to the retriever, which then formats the results.
rag_chain = (
    {"context": retriever | (lambda x: "\n\n".join([doc.page_content for doc in x])), "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 9. Invoke the RAG chain with a question
question = "Who founded LangChain?"
response = rag_chain.invoke(question)
print(f"Question: {question}")
print(f"Answer: {response}")

question_2 = "What is the capital of Japan?" # This question is not in our document
response_2 = rag_chain.invoke(question_2)
print(f"Question: {question_2}")
print(f"Answer: {response_2}")

# Clean up
os.remove("my_document.txt")
```

This simple `LangChain RAG tutorial` provides a foundational understanding. You can extend this with more complex document loaders, different vector stores (like Qdrant as shown in [LangChain Llama2 Qdrant RAG Chatbot]({% post_url 2026-11-14-langchain-llama2-qdrant-rag-chatbot %})), and advanced retrieval strategies. For a more interactive RAG experience, see [Observable ArXiv RAG with LangChain and Chainlit]({% post_url 2026-11-14-observable-arxiv-rag-langchain-chainlit %}).

### 5. Advanced LangChain Features

LangChain offers powerful capabilities to build more sophisticated `AI apps`.

#### 5.1. Agents and Tools

`LangChain agents` enable LLMs to decide which actions to take, what tools to use, and in what order. They are excellent for tasks requiring multiple steps, external data access, or interaction with APIs. You can debug agents using techniques described in [Debug LangChain Tool Agents]({% post_url 2026-11-12-debug-langchain-tool-agents %}), and test them in a [LangChain Agents Free Sandbox]({% post_url 2026-11-13-langchain-agents-free-sandbox %}).


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


**Architecture of an Agent:**
1.  **LLM**: The brain of the agent, responsible for reasoning.
2.  **Tools**: Functions that the agent can call to interact with the outside world (e.g., search engine, calculator, API call).
3.  **Agent Executor**: The runtime that takes the agent's decision and executes the chosen tool.
4.  **Prompt**: Guides the agent on how to reason and what actions to take.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
import wikipediaapi

# 1. Define custom tools for the agent

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers and returns the result."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds two integers and returns the result."""
    return a + b

@tool
def wikipedia_search(query: str) -> str:
    """Searches Wikipedia for the given query and returns a summary."""
    wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        return page_py.summary[0:500] # Return first 500 chars
    return "No information found on Wikipedia."

# List of tools available to the agent
tools = [multiply, add, wikipedia_search]

# 2. Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Define the agent prompt
# This is a common ReAct style prompt for agents
prompt_template = PromptTemplate.from_template("""
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

# 4. Create the ReAct agent
# create_react_agent is a helper function to create an agent using the ReAct pattern
agent = create_react_agent(llm, tools, prompt_template)

# 5. Create an AgentExecutor to run the agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# 6. Invoke the agent
print("\n--- Agent Example 1: Arithmetic ---")
result_arithmetic = agent_executor.invoke({"input": "What is 12 multiplied by 5 and then add 10?"})
print(f"Final Answer: {result_arithmetic['output']}")

print("\n--- Agent Example 2: Wikipedia Search ---")
# Install wikipediaapi: pip install wikipedia-api
result_wiki = agent_executor.invoke({"input": "Tell me about the history of Artificial Intelligence."})
print(f"Final Answer: {result_wiki['output']}")
```

This example demonstrates how `LangChain agents` can perform multi-step reasoning and use external tools. You can create tools for almost any functionality, making your `LLM applications` incredibly versatile.

#### 5.2. Memory

For conversational `AI apps`, maintaining context across turns is crucial. LangChain's `Memory` modules store and manage conversation history, allowing the LLM to remember previous interactions.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage

# Initialize components (simplified for memory demo)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Dummy vector store for demonstration (in a real app, load your actual documents)
docs = [Document(page_content="The capital of France is Paris.")]
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# 1. History-aware retriever chain
# This chain takes conversation history and the new question, then generates a standalone question for the retriever.
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given a chat history and the latest user question "
               "which might reference context in the chat history, "
               "formulate a standalone question which can be understood "
               "without the chat history. Do NOT answer the question, "
               "just reformulate it if needed and otherwise return it as is."),
    MessagesPlaceholder("chat_history"),
    ("user", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

# 2. Main RAG chain (as seen before)
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
               "If you don't know the answer, just say that you don't know.\n\n"
               "Context: {context}"),
    MessagesPlaceholder("chat_history"), # Include chat history in final QA
    ("user", "{input}")
])
rag_chain = create_retrieval_chain(history_aware_retriever, qa_prompt | llm) # This combines retrieval with generation

# Example usage with chat history
chat_history = []

# First turn
query1 = "What is the capital of France?"
response1 = rag_chain.invoke({"input": query1, "chat_history": chat_history})
print(f"User: {query1}\nAI: {response1['answer']}")
chat_history.extend([HumanMessage(content=query1), AIMessage(content=response1["answer"])])

# Second turn, referring back to the previous context
query2 = "What else can you tell me about it?"
response2 = rag_chain.invoke({"input": query2, "chat_history": chat_history})
print(f"User: {query2}\nAI: {response2['answer']}")
```

#### 5.3. Callbacks and Observability

Understanding how your `LLM applications` execute is vital for debugging and optimization. LangChain's `Callbacks` system provides hooks into various stages of a chain's execution. `LangSmith` is LangChain's dedicated platform for observability, evaluation, and monitoring.

You can learn more about this in [LangChain Observability with LangSmith Tutorial]({% post_url 2026-11-13-langchain-observability-langsmith-tutorial %}) and [LangChain, LangSmith, and Weights & Biases Tutorial]({% post_url 2026-11-12-langchain-langsmith-wandb-tutorial %}).

To use LangSmith:
1.  Sign up at [https://smith.langchain.com/](https://smith.langchain.com/).
2.  Set environment variables:
    ```bash
    export LANGCHAIN_TRACING_V2="true"
    export LANGCHAIN_API_KEY="your_langsmith_api_key"
    export LANGCHAIN_PROJECT="MyAwesomeLangChainApp" # Optional
    ```
3.  Your LangChain chains will automatically be traced and logged to LangSmith.

### 6. Building a Complete AI Application: A RAG Chatbot Example

Let's combine what we've learned into a more complete `AI app` – a sophisticated RAG-powered chatbot that can answer questions about a collection of documents.

#### 6.1. Architecture Overview

Here's a high-level view of our RAG chatbot's architecture:

| Component                 | Role                                                                        | LangChain Module / Tool        |
| :------------------------ | :-------------------------------------------------------------------------- | :----------------------------- |
| **User Interface**        | Accepts user queries, displays responses.                                   | CLI, Streamlit, Chainlit       |
| **Document Loader**       | Ingests raw data (PDFs, text files, web pages).                             | `TextLoader`, `PyPDFLoader`    |
| **Text Splitter**         | Breaks documents into smaller chunks for context management.                | `RecursiveCharacterTextSplitter` |
| **Embeddings Model**      | Converts text chunks into numerical vectors.                                | `OpenAIEmbeddings`             |
| **Vector Store**          | Stores document embeddings for efficient semantic search.                   | `Chroma`, `Qdrant`             |
| **Retriever**             | Queries the vector store to fetch relevant document chunks.                 | `vectorstore.as_retriever()`   |
| **Chat History**          | Stores previous turns of the conversation.                                  | `MessagesPlaceholder`          |
| **LLM (Chat Model)**      | Generates responses based on the prompt, retrieved context, and chat history. | `ChatOpenAI`                   |
| **Prompt Template**       | Formulates clear instructions for the LLM, including context and history.   | `ChatPromptTemplate`           |
| **Output Parser**         | Extracts structured information from LLM responses (optional).              | `StrOutputParser`              |
| **LangChain Chain (LCEL)**| Orchestrates the entire flow: `User Input -> History-aware Retriever -> RAG LLM -> Output`. | `|`, `create_history_aware_retriever`, `create_retrieval_chain` |

#### 6.2. Step-by-Step Implementation

This `LangChain Python tutorial` will walk you through building a RAG chatbot capable of answering questions about a set of documents. We'll use local `.txt` files, but you can easily adapt this for PDFs or web pages.

**Prerequisites:**
*   `pip install langchain langchain-openai langchain-community pypdf python-dotenv`
*   Set your `OPENAI_API_KEY` environment variable.

```python
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage


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


# --- Configuration ---
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true" # Enable LangSmith tracing
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY") # Ensure this is set
os.environ["LANGCHAIN_PROJECT"] = "FullGuideRAGChatbot"

LLM_MODEL = "gpt-3.5-turbo-0125"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
PERSIST_DIRECTORY = "./chroma_db" # Directory to save your vector store

# --- 1. Document Loading ---
def load_documents(data_path="./data"):
    """Loads documents from a specified directory."""
    documents = []
    for root, _, files in os.walk(data_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".txt"):
                loader = TextLoader(file_path)
                documents.extend(loader.load())
            elif file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            # Add more loaders as needed (e.g., CSVLoader, WebBaseLoader)
    print(f"Loaded {len(documents)} documents.")
    return documents

# --- 2. Text Splitting ---
def split_documents(documents):
    """Splits documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True
    )
    splits = text_splitter.split_documents(documents)
    print(f"Split into {len(splits)} chunks.")
    return splits

# --- 3. Embedding and Vector Store ---
def setup_vector_store(splits):
    """Creates or loads a Chroma vector store with OpenAI embeddings."""
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        print("Loading existing Chroma DB...")
        vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    else:
        print("Creating new Chroma DB...")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        vectorstore.persist()
        print("Chroma DB created and persisted.")
    return vectorstore

# --- 4. Main Chatbot Chain Setup ---
def create_rag_chatbot_chain(vectorstore):
    """
    Creates the complete RAG chatbot chain using LangChain Expression Language (LCEL).
    """
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.3)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 relevant chunks

    # Contextualize question prompt
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", "Given a chat history and the latest user question "
                   "which might reference context in the chat history, "
                   "formulate a standalone question which can be understood "
                   "without the chat history. Do NOT answer the question, "
                   "just reformulate it if needed and otherwise return it as is."),
        MessagesPlaceholder("chat_history"),
        ("user", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    # Answer question prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Use the following pieces of retrieved context to answer the question. "
                   "If you don't know the answer, just say that you don't know, but try your best to provide a helpful answer based on the context. "
                   "Keep your answers concise and informative.\n\n"
                   "Context: {context}"),
        MessagesPlaceholder("chat_history"),
        ("user", "{input}")
    ])

    # Create the RAG chain
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_prompt | llm)

    return rag_chain

# --- Main execution flow ---
if __name__ == "__main__":
    # Create a dummy data directory and files if they don't exist
    if not os.path.exists("./data"):
        os.makedirs("./data")
        with open("./data/langchain_intro.txt", "w") as f:
            f.write("LangChain is a framework designed to simplify the creation of applications using large language models. "
                    "It offers tools for chaining components, managing memory, and integrating external data sources. "
                    "Key features include Prompt Templates, LLMs, Chains, Agents, and Retrievers. "
                    "It was founded by Harrison Chase in 2022 and quickly gained popularity for its modular approach to AI development. "
                    "LangChain supports a wide array of models from OpenAI, Hugging Face, Anthropic, and more. "
                    "Retrieval Augmented Generation (RAG) is one of its most powerful applications, allowing LLMs to query external knowledge bases.")
        with open("./data/rag_benefits.txt", "w") as f:
            f.write("RAG systems enhance LLMs by providing them with up-to-date and domain-specific information. "
                    "This reduces hallucination, improves factual accuracy, and allows for more relevant responses. "
                    "Benefits include improved knowledge, reduced data drift, and enhanced transparency. "
                    "Common components of a RAG system are document loaders, text splitters, embedding models, and vector stores.")
        print("Created dummy data files in ./data/")

    # Load and process documents
    documents = load_documents()
    splits = split_documents(documents)

    # Set up vector store
    vectorstore = setup_vector_store(splits)

    # Create the RAG chatbot chain
    rag_chatbot_chain = create_rag_chatbot_chain(vectorstore)

    print("\n--- RAG Chatbot Ready! Type 'exit' to quit. ---")
    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting chatbot.")
            break

        try:
            response = rag_chatbot_chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            ai_message = response["answer"]
            print(f"AI: {ai_message}")

            # Update chat history
            chat_history.extend([HumanMessage(content=user_input), AIMessage(content=ai_message)])
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again or check your API keys/setup.")
```

This `LangChain Python tutorial` example demonstrates a full RAG cycle. You can deploy such a `LangChain tutorial` example as a web service or integrate it into larger `AI apps`. Remember to integrate with LangSmith for full observability as shown in [LangChain Observability with LangSmith Tutorial]({% post_url 2026-11-13-langchain-observability-langsmith-tutorial %}).

### 7. LangChain Integrations and Ecosystem

LangChain's strength lies in its extensive ecosystem of integrations, allowing you to connect to almost any tool or service. This makes `LangChain integrations` incredibly flexible for `Python AI development`.

*   **LLMs/ChatModels**: OpenAI, Hugging Face Hub, Anthropic, Google Gemini, Azure OpenAI, Llama C++ (via `llama-cpp-python`).
*   **Document Loaders**: PDF (`PyPDFLoader`), Markdown (`UnstructuredMarkdownLoader`), HTML (`BSHTMLLoader`), CSV (`CSVLoader`), web pages (`WebBaseLoader`), databases (`SQLDatabaseLoader`), ArXiv (`ArxivLoader`).
*   **Text Splitters**: `RecursiveCharacterTextSplitter`, `CharacterTextSplitter`, `NLTKTextSplitter`.
*   **Embeddings**: OpenAI Embeddings, HuggingFace Embeddings, Cohere Embeddings.
*   **Vector Stores**: Chroma, Pinecone, Qdrant, Weaviate, FAISS, Milvus. (e.g., [LangChain Llama2 Qdrant RAG Chatbot]({% post_url 2026-11-14-langchain-llama2-qdrant-rag-chatbot %})).
*   **Memory**: ConversationBufferMemory, ConversationSummaryBufferMemory, VectorStoreRetrieverMemory.
*   **Agents/Tools**: Search tools (Google Search, DuckDuckGo), mathematical tools, API tools (e.g., calling custom REST APIs), calendar tools, code interpreter.
*   **Callbacks**: LangSmith, Weights & Biases ([LangChain, LangSmith, and Weights & Biases Tutorial]({% post_url 2026-11-12-langchain-langsmith-wandb-tutorial %})).

This vast array of `LangChain integrations` means you're rarely limited by what LangChain itself provides, but rather by the availability of external APIs and services.

### 8. Best Practices and Tips for `LLM Applications`

To `build AI apps` effectively with LangChain, consider these best practices:

*   **Iterative `Prompt Engineering`**: Start with simple prompts and gradually refine them. Experiment with system messages, few-shot examples, and output instructions.
*   **Chunking Strategy**: The way you split documents significantly impacts RAG performance. Experiment with `chunk_size`, `chunk_overlap`, and metadata. See [LangChain RAG Chunking Strategies]({% post_url 2026-11-11-langchain-rag-chunking-strategies %}).
*   **Model Selection**: Choose the right LLM for your task. Smaller, faster models (e.g., `gpt-3.5-turbo`) are great for simple tasks, while larger models (e.g., `gpt-4`) excel at complex reasoning. Consider open-source models for cost efficiency and privacy.
*   **Observability**: Always use tools like LangSmith to trace, debug, and understand your chains. This is critical for diagnosing issues and optimizing performance.
*   **Evaluation**: Don't rely solely on qualitative assessment. Implement quantitative evaluation metrics for your `LLM applications`, especially for RAG and agent-based systems.
*   **Cost Management**: LLM API calls can be expensive. Monitor usage, optimize token counts, and consider local/open-source models where appropriate.
*   **Security and Privacy**: Be mindful of sensitive data. Sanitize inputs, avoid sending private information to LLMs if not necessary, and consider self-hosted models for strict privacy requirements.

### 9. Troubleshooting Common Issues

Even with a robust framework like LangChain, you might encounter issues. Here are some common ones and how to address them:

*   **API Key Errors**: Ensure your `OPENAI_API_KEY` (or similar) is correctly set in your environment variables or `.env` file and is valid. Incorrect keys will result in authentication failures.
*   **Context Window Limits**: If your prompts or retrieved documents are too long, you'll hit token limits.
    *   Reduce `chunk_size` for RAG.
    *   Summarize chat history before passing it to the LLM.
    *   Use LLMs with larger context windows (e.g., `gpt-4-turbo`, `Claude 3 Opus`).
*   **Hallucinations/Inaccurate Responses**:
    *   Improve your RAG system's retrieval quality (better chunks, more relevant retrieval, higher `k`).
    *   Refine `prompt engineering` to instruct the LLM to only use provided context.
    *   Ensure your underlying data is accurate and comprehensive.
*   **Slow Response Times**:
    *   Use faster, smaller LLMs.
    *   Optimize your retrieval process (e.g., faster vector store, fewer retrieval calls).
    *   Process documents offline for RAG rather than on-the-fly.
*   **Parsing Errors from LLM**:
    *   Provide clearer `prompt engineering` instructions for the desired output format (e.g., "Always respond in JSON").
    *   Use LangChain's `OutputParsers` and instruct the LLM on the expected schema.
    *   Adjust the `temperature` of the LLM; lower temperatures often lead to more deterministic outputs.

### 10. Frequently Asked Questions (FAQs)

#### Q1: What is LangChain and why should I use it for `Python AI development`?
LangChain is an open-source framework for developing applications powered by large language models. You should use it because it simplifies `LLM applications` by providing tools for `prompt engineering`, chaining LLMs with external data, `LangChain agents`, and memory, allowing you to `build AI apps` faster and more robustly.

#### Q2: Is this `LangChain Python tutorial` suitable for beginners?
Yes, this `LangChain Python tutorial` is designed to be accessible to developers with basic Python knowledge. We start with fundamental concepts and gradually introduce more complex features, providing practical `LangChain Python examples` along the way.

#### Q3: What is RAG and why is it important for `LLM applications`?
RAG stands for Retrieval Augmented Generation. It's crucial for `LLM applications` because it allows LLMs to access and incorporate external, up-to-date, and domain-specific information. This significantly reduces hallucinations, improves factual accuracy, and expands the LLM's knowledge beyond its training data.

#### Q4: How do `LangChain agents` work and when should I use them?
`LangChain agents` enable LLMs to reason about a problem, decide on a sequence of actions, and execute those actions using `tools`. You should use them when your application requires multiple steps, conditional logic, or interaction with external APIs (like search engines, databases, or custom functions).

#### Q5: What's the difference between LangChain and LangGraph?
LangChain provides a comprehensive set of tools and abstractions for building LLM applications. LangGraph is an extension of LangChain specifically designed for building highly stateful, multi-actor applications, often modeled as cyclical graphs. While LangChain can build many types of applications, LangGraph excels at more complex, dynamic agentic workflows. You can learn more in [RAG Frameworks: LangChain, LangGraph, LlamaIndex]({% post_url 2026-11-11-rag-frameworks-langchain-langgraph-llamaindex %}).

#### Q6: How do I choose the right LLM for my `AI apps`?
Consider your application's requirements:
*   **Cost**: Smaller models (e.g., `gpt-3.5-turbo`) or open-source models are cheaper.
*   **Performance/Accuracy**: Larger models (e.g., `gpt-4`, `Claude 3 Opus`) offer better reasoning but are slower and more expensive.
*   **Latency**: For real-time `AI apps`, faster models are crucial.
*   **Specific task**: Some models are better fine-tuned for certain tasks.
*   **Privacy**: Self-hosted or open-source models offer more control over data.

### Conclusion

You've now embarked on a comprehensive journey through the world of LangChain, mastering its core components and advanced features. This `LangChain Python tutorial` has equipped you with the knowledge to `build AI apps` ranging from simple `LLM applications` to sophisticated `RAG systems` and intelligent `LangChain agents`.

The landscape of `Python AI development` is constantly evolving, and LangChain provides a robust and flexible foundation for innovation. Continue to explore `prompt engineering` techniques, experiment with different `LangChain integrations`, and leverage observability tools like LangSmith. The power to create truly intelligent and impactful `LLM applications` is now at your fingertips. Go forth and build!