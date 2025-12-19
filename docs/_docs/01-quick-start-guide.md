---
layout: single
title: "Quick Start Guide"
permalink: /quick-start/
toc: true
toc_label: "Quick Start"
toc_icon: "rocket"
---

# Quick Start Guide

Welcome to LangChain Tutorials! This guide will help you get started with LangChain and build your first AI agent in minutes.

## Prerequisites

Before you begin, make sure you have:

- Python 3.8 or higher installed
- Basic understanding of Python programming
- An OpenAI API key (or other LLM provider API key)
- A code editor (VS Code, PyCharm, etc.)

## Installation

### Step 1: Create a Virtual Environment

```bash
# Create a new directory for your project
mkdir my-langchain-project
cd my-langchain-project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install LangChain

```bash
# Install LangChain and OpenAI
pip install langchain langchain-openai

# Optional: Install additional dependencies
pip install python-dotenv
```

### Step 3: Set Up Your API Key

Create a `.env` file in your project directory:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Your First LangChain Application

### Simple LLM Call

Create a file called `simple_llm.py`:

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Make a simple call
response = llm.invoke("What is LangChain?")
print(response.content)
```

Run it:

```bash
python simple_llm.py
```

### Using Prompt Templates

Create `prompt_template.py`:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant specializing in {topic}."),
    ("user", "{question}")
])

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create a chain
chain = prompt | llm

# Invoke the chain
response = chain.invoke({
    "topic": "programming",
    "question": "What is the difference between a list and a tuple in Python?"
})

print(response.content)
```

### Building a Simple Chain

Create `simple_chain.py`:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Define components
prompt = ChatPromptTemplate.from_template(
    "Tell me a short joke about {topic}"
)
llm = ChatOpenAI(model=