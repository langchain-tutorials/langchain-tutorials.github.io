---
title: "LangChain Quick Start Guide"
excerpt: "Complete beginner's guide to getting started with LangChain - Learn how to build AI-powered applications in minutes"
permalink: /quick-start-guide
layout: single
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true # Table of contents - IMPORTANT for tutorials
toc_sticky: true # Sticky TOC - Better UX
toc_label: "Tutorial Contents"
toc_icon: "list-ul"
---

Welcome to the complete quick start guide for LangChain! This tutorial will get you building AI-powered applications in under 15 minutes.



## What is LangChain? {#what-is-langchain}

LangChain is a framework for developing applications powered by language models. It helps you:

- Connect LLMs to your data sources
- Chain multiple LLM calls together
- Build conversational AI agents
- Create RAG (Retrieval Augmented Generation) systems
- Integrate with vector databases

**Think of it as:** The bridge between your data and AI models like GPT-4, Claude, or Llama.

---

##  Installation {#installation}

### Prerequisites

- Python 3.8 or higher
- pip package manager
- An API key (OpenAI, Anthropic, or other LLM provider)

### Install LangChain

```bash
# Install core LangChain
pip install langchain

# Install OpenAI integration
pip install langchain-openai

# Install community integrations (optional)
pip install langchain-community

# Install for document loading
pip install pypdf chromadb
```

### Set Up API Keys

```bash
# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'

# Or create a .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

---

## Your First LangChain App {#your-first-app}

### Example 1: Simple Text Generation

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Initialize the model
llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

# Create a message
message = HumanMessage(content="Write a haiku about programming")

# Get response
response = llm.invoke([message])
print(response.content)
```

**Output:**
```
Code flows like water
Logic builds bridges of thought
Bugs teach us patience
```

### Example 2: Prompt Templates

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful coding assistant."),
    ("user", "Explain {concept} in simple terms.")
])

# Initialize model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create chain
chain = prompt | llm

# Run the chain
response = chain.invoke({"concept": "recursion"})
print(response.content)
```

### Example 3: Simple Chain

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser

# Create components
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
llm = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

# Chain them together
chain = prompt | llm | output_parser

# Run the chain
result = chain.invoke({"topic": "programming"})
print(result)
```

---

## Core Concepts {#core-concepts}

### 1. **Models**

LangChain supports multiple LLM providers:

```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4")

# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-opus-20240229")

# Local models (Ollama)
from langchain_community.llms import Ollama
llm = Ollama(model="llama2")
```

### 2. **Prompts**

Structure your inputs effectively:

```python
from langchain.prompts import PromptTemplate

# Simple template
template = "Write a {adjective} story about {subject}"
prompt = PromptTemplate.from_template(template)

# Chat template
from langchain.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}"),
    ("user", "{user_input}"),
])
```

### 3. **Chains**

Connect components together:

```python
# Using LCEL (LangChain Expression Language)
chain = prompt | llm | output_parser

# Sequential chain
from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(topic="AI")
```

### 4. **Memory**

Add conversation history:

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# Chat maintains context
conversation.predict(input="Hi, my name is Alice")
conversation.predict(input="What's my name?")  # Will remember "Alice"
```

### 5. **Agents**

Let AI decide what to do:

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

# Define tools
def calculator(query):
    return eval(query)

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations"
    )
]

# Create agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Run agent
agent_executor.invoke({"input": "What is 25 * 4?"})
```

---

## Common Use Cases {#use-cases}

### Use Case 1: Document Q&A (RAG)

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Load documents
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# Create Q&A chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# Ask questions
response = qa_chain.invoke("What is the main topic of this document?")
print(response['result'])
```

### Use Case 2: Chatbot with Memory

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

# Keep last 5 interactions
memory = ConversationBufferWindowMemory(k=5)

chatbot = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Continuous conversation
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    
    response = chatbot.predict(input=user_input)
    print(f"Bot: {response}")
```

### Use Case 3: Data Analysis Agent

```python
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd

# Load data
df = pd.read_csv("sales_data.csv")

# Create agent
agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    allow_dangerous_code=True
)

# Ask questions about data
agent.invoke("What are the total sales by region?")
agent.invoke("Which product has the highest profit margin?")
```

### Use Case 4: Web Scraping + AI Analysis

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain

# Load web page
loader = WebBaseLoader("https://python.langchain.com/docs/introduction/")
docs = loader.load()

# Summarize
chain = load_summarize_chain(llm, chain_type="map_reduce")
summary = chain.run(docs)
print(summary)
```

---

## Next Steps {#next-steps}

### Beginner Projects

1. **Personal AI Assistant**
   - Build a chatbot that remembers conversations
   - Add web search capabilities
   - Integrate with your calendar

2. **Document Analyzer**
   - Create a Q&A system for your PDFs
   - Add summarization features
   - Export insights to markdown

3. **Content Generator**
   - Blog post writer with SEO optimization
   - Social media post scheduler
   - Email response generator

### Advanced Topics

- **Vector Databases**: Pinecone, Weaviate, Qdrant
- **Streaming Responses**: Real-time output
- **Custom Tools**: Build your own agent tools
- **Multi-agent Systems**: Agents working together
- **Production Deployment**: LangServe, FastAPI

### Resources

- **Official Docs**: [python.langchain.com](https://python.langchain.com)
- **GitHub**: [github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- **Discord Community**: Join the LangChain Discord
- **YouTube**: LangChain official channel
- **Twitter**: @LangChainAI

---

## Troubleshooting

### Common Issues

**1. API Key Errors**
```bash
# Make sure your key is set
echo $OPENAI_API_KEY

# Or load from .env
pip install python-dotenv
```

**2. Rate Limits**
```python
# Add retry logic
from langchain.llms import OpenAI

llm = OpenAI(
    max_retries=3,
    request_timeout=60
)
```

**3. Memory Issues with Large Documents**
```python
# Use streaming for large docs
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)
```

---

## Quick Reference

### Installation Commands
```bash
pip install langchain langchain-openai langchain-community
pip install pypdf chromadb  # For RAG
pip install pandas  # For data analysis
```

### Basic Pattern
```python
# 1. Import
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 2. Setup
llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("{input}")

# 3. Chain
chain = prompt | llm

# 4. Run
response = chain.invoke({"input": "Hello!"})
```

---

## Get Help

- **Stack Overflow**: Tag `langchain`
- **GitHub Issues**: Report bugs
- **Discord**: Real-time help
- **Twitter**: @LangChainAI

---

**Ready to build?** Start with the examples above and experiment! The best way to learn LangChain is by building real projects.
