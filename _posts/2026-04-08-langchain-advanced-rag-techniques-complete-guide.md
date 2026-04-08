---
title: "LangChain Advanced RAG Techniques: The Complete Guide to Production-Ready Retrieval"
description: "Master LangChain advanced RAG techniques for production-ready retrieval. This complete guide provides everything to build robust, scalable systems."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain advanced RAG techniques]
featured: false
image: '/assets/images/langchain-advanced-rag-techniques-complete-guide.webp'
---

## Unlocking Super-Smart AI: Your Guide to LangChain Advanced RAG Techniques

Imagine you're asking a super-smart robot a question. If that robot only knows what it learned from its training, it might not have the very latest information. This is where Retrieval-Augmented Generation, or RAG, comes in. RAG lets your AI robot look up information in real-time, just like you would use a search engine.

This guide will show you how to make your AI robot even smarter using LangChain advanced RAG techniques. We will explore how to build a RAG pipeline that is ready for the real world. You will learn about better ways to find information and give your AI the best answers.

### What is Retrieval-Augmented Generation (RAG)? A Quick Peek

RAG is a clever way to make large language models (LLMs) smarter. Instead of just relying on what they were trained on, LLMs can "look up" extra information. This lookup happens from a special knowledge base you provide.

Think of it like this: The LLM is a brilliant student, and the RAG pipeline is their open textbook. When asked a question, the student first quickly checks the textbook for relevant pages. Then, they use those pages to give you a much better and more accurate answer.

### The Basic RAG Pipeline: How It Works

A simple RAG pipeline has a few main steps. First, you gather all your documents and break them into smaller pieces called chunks. Next, you turn these chunks into special numbers called embeddings using an embedding model. These embeddings are then stored in a [vector store]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

When you ask a question, your question also gets turned into an embedding. The system then searches the vector store to find chunks that are most similar to your question. Finally, these matching chunks are given to the LLM, along with your original question, to generate an answer. This basic setup is a good start, but production-ready systems need more.

### Why Go Advanced? Challenges in Simple RAG

While basic RAG is great, it can run into problems when you use it for real applications. Sometimes, the system might not find the best information to answer your question. This can happen if the chunks are too big, too small, or if the search method isn't smart enough.

The AI might also "hallucinate," meaning it makes up answers if the retrieved information is not good. Plus, handling lots of documents and many users at once can be tricky. This is why we need LangChain advanced RAG techniques to make your applications truly powerful and reliable.

### LangChain Advanced RAG Techniques for Better Retrieval

Making your RAG system truly excellent involves refining each step of the RAG pipeline. LangChain provides many tools to help you improve how information is prepared, found, and used. Let's dive into some of these powerful LangChain advanced RAG techniques.

#### 1. Smarter Chunking Strategies

Breaking your documents into chunks is a critical first step. If chunks are too small, you might lose important context. If they are too big, the LLM might get confused or exceed its context window limit. Smarter chunking ensures your AI gets just the right amount of information.

LangChain offers various text splitters to handle this. For example, `RecursiveCharacterTextSplitter` tries to keep chunks meaningful by splitting on different characters. Even more advanced, semantic chunking helps split text based on its meaning, which is very helpful for complex documents. You can learn more about this in our guide on [semantic text splitting]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}).

Here's a simple example of recursive chunking:

{% raw %}
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

long_text = "LangChain advanced RAG techniques are essential for production. " \
            "They help improve retrieval accuracy and overall system performance. " \
            "Smart chunking is one of the foundational steps in optimizing your RAG pipeline. " \
            "Using recursive splitters can maintain context better than simple splits."

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_text(long_text)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: '{chunk}'")
```
{% endraw %}

This code snippet shows how LangChain helps you break down long text into smaller, manageable pieces. Each chunk now has some overlap with the next, helping to keep important ideas connected. This is a basic but very important step in any RAG pipeline.

#### 2. Enhanced Vector Stores and Indexing

Your vector store is like the library where all your document chunks live. To make retrieval-augmented generation better, you need a smart library. This means not just storing chunks, but also making them easy to find with extra rules.

LangChain lets you use metadata filtering, which means you can add labels to your chunks. For example, if you have documents from different years or departments, you can label them. Then, you can tell the RAG pipeline to only search documents from "2026" or "Sales Department." This greatly improves the relevance of the retrieved information.

Another powerful technique is self-querying. Instead of just searching for similar text, the system can understand your question and automatically build a filter. So, if you ask "Show me documents about LangChain from last year," the system automatically filters for "LangChain" and "2025" (or whatever "last year" implies based on your data).

Multi-vector retrieval stores different "views" of the same chunk. For example, you might have a summary of a chunk and the full chunk. When you search, the system uses the summary to find relevant information quickly, then retrieves the full chunk for the LLM. This can make the RAG pipeline faster and more accurate.

#### 3. Hybrid Search

Imagine you're looking for a book. Sometimes you know the exact title (keyword search). Other times, you only know the topic, like "books about space travel" (semantic search). Hybrid search combines both these methods to give you the best of both worlds. It's one of the most effective LangChain advanced RAG techniques.

Hybrid search uses a vector store to find documents that are *similar in meaning* to your query. At the same time, it also looks for documents that contain *exact keywords* from your query. By combining these results, you get a much more comprehensive and relevant set of documents. This is especially useful for queries that are a mix of specific terms and broader ideas.

Using hybrid search can significantly improve retrieval accuracy. It makes your LangChain RAG pipeline much more robust. We have a detailed guide on how to implement this with [Weaviate and LangChain]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

Here’s a conceptual example of how hybrid search might be set up in LangChain:

{% raw %}
```python
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document

# This is a conceptual example. Actual setup would involve
# connecting to a Weaviate instance and configuring embeddings.

# Assuming you have a Weaviate client and embeddings model
# vectorstore = Weaviate(
#     client=weaviate_client,
#     index_name="MyDocs",
#     text_key="text",
#     embedding=OpenAIEmbeddings(),
#     by_text=False # This flag might vary based on Weaviate version/setup
# )

# A more generic retriever setup for illustration
class HybridRetriever:
    def __init__(self, vectorstore_retriever, keyword_retriever):
        self.vectorstore_retriever = vectorstore_retriever
        self.keyword_retriever = keyword_retriever

    def get_relevant_documents(self, query):
        # Semantic search
        semantic_docs = self.vectorstore_retriever.get_relevant_documents(query)
        # Keyword search (e.g., using a custom retriever or database)
        keyword_docs = self.keyword_retriever.get_relevant_documents(query)
        
        # Combine and deduplicate
        combined_docs = {doc.page_content: doc for doc in semantic_docs + keyword_docs}
        return list(combined_docs.values())

# In a real LangChain setup, you'd integrate this with existing retriever interfaces.
# For example, using a multi-retriever chain.
```
{% endraw %}

This snippet shows the idea of combining results from two different search types. The `HybridRetriever` would first perform a semantic search through your vector store. Then, it would also perform a keyword search. Finally, it merges the results to give you a more complete set of documents, enhancing your retrieval-augmented generation.

#### 4. Reranking for Precision

After your initial search, you might get a good number of documents. However, not all of them will be equally helpful. Reranking is like having a smart assistant review these documents and put the most relevant ones at the very top. This is a powerful step in the RAG pipeline to ensure the LLM sees the best information first.

Reranking models are special AI models trained to judge the relevance of a document to a query. They take the query and each retrieved document, then give a score indicating how good a match it is. Documents with higher scores are then presented to the LLM.

This process significantly improves the quality of the information fed to the LLM. It helps the LLM focus on the most important details, leading to more accurate and concise answers. Popular rerankers include Cohere's reranker and models like `bge-reranker`.

Here’s an example using a hypothetical reranker in LangChain:

{% raw %}
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import DocumentCompressor
from langchain_core.documents import Document

# Imagine you have a custom reranker model
class MyCustomReranker(DocumentCompressor):
    def compress_documents(self, documents, query):
        # In a real scenario, this would call a reranking API or model
        # For simplicity, we'll just sort based on a hypothetical relevance score
        
        # Simulate scoring (higher score means more relevant)
        scored_documents = []
        for doc in documents:
            # Example: Assign a random score, in reality, it'd be a model prediction
            import random
            score = random.random() * 10 
            # You might modify the document metadata with the score
            doc.metadata["relevance_score"] = score
            scored_documents.append(doc)
            
        # Sort documents by their simulated relevance score in descending order
        reranked_docs = sorted(scored_documents, key=lambda x: x.metadata["relevance_score"], reverse=True)
        
        # Return only the top N documents after reranking
        return reranked_docs[:3] # Example: keep top 3

# Assume base_retriever is already set up (e.g., a vector store retriever)
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import OpenAIEmbeddings
# vectorstore = Chroma.from_texts(["text1", "text2", "text3", "text4", "text5"], embedding=OpenAIEmbeddings())
# base_retriever = vectorstore.as_retriever()

# For demonstration, let's create a dummy base_retriever
class DummyRetriever:
    def get_relevant_documents(self, query):
        return [
            Document(page_content="The sky is blue today. LangChain is cool.", metadata={"source": "doc1"}),
            Document(page_content="Advanced RAG techniques are vital.", metadata={"source": "doc2"}),
            Document(page_content="Birds fly high in the evening. LangChain helps with retrieval.", metadata={"source": "doc3"}),
            Document(page_content="Learning about reranking improves RAG.", metadata={"source": "doc4"}),
            Document(page_content="Production-ready systems use LangChain advanced RAG.", metadata={"source": "doc5"})
        ]
dummy_base_retriever = DummyRetriever()

# Create a compressor with your custom reranker
compressor = MyCustomReranker()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=dummy_base_retriever
)

query = "Tell me about LangChain advanced RAG techniques"
compressed_docs = compression_retriever.get_relevant_documents(query)

print(f"Query: '{query}'")
print("Reranked and compressed documents:")
for doc in compressed_docs:
    print(f"- '{doc.page_content}' (Score: {doc.metadata.get('relevance_score', 'N/A')})")
```
{% endraw %}

This example illustrates how a reranker takes an initial set of retrieved documents and sorts them by relevance. The `ContextualCompressionRetriever` in LangChain is designed to integrate such compressors. This ensures that the most important information is highlighted for the retrieval-augmented generation process, making your overall RAG pipeline much more efficient.

#### 5. Query Transformation and Expansion

Sometimes, your question might be too simple, or it might be phrased in a way that makes it hard for the search to find good matches. Query transformation and expansion techniques modify your original question to improve retrieval. These are clever LangChain advanced RAG techniques that pre-process your query.

One method is the multi-query approach. Here, your single question is turned into several different questions, each focusing on a slightly different aspect. All these new questions are then used to search the vector store, retrieving a broader set of relevant documents.

Another technique is HyDE (Hypothetical Document Embedding). For this, the LLM first generates a hypothetical (fake) answer to your question. Then, this fake answer is used to search the vector store. The idea is that an answer-like document will be semantically very close to the actual relevant documents.

LangChain provides tools to implement these. For example, `MultiQueryRetriever` can generate multiple queries, and then combine the results. This greatly increases the chances of finding all necessary information for a complete answer, making your retrieval-augmented generation more comprehensive.

Example of a Multi-Query Retriever:

{% raw %}
```python
from langchain.retrievers import MultiQueryRetriever
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# This is a conceptual example. Replace with actual LLM/Embeddings/VectorStore setup.
# from langchain_openai import OpenAI, OpenAIEmbeddings

# For demonstration, we'll use dummy LLM and VectorStore
class DummyLLM:
    def invoke(self, prompt):
        # Simulate query generation
        if "query for information" in prompt:
            return "What are LangChain advanced RAG techniques?\n" \
                   "How to improve retrieval in RAG?\n" \
                   "What makes RAG production-ready?"
        return "Dummy LLM response."

class DummyEmbeddings:
    def embed_documents(self, texts):
        return [[0.1]*10 for _ in texts] # Dummy embeddings

    def embed_query(self, text):
        return [0.1]*10 # Dummy embedding

# Setup a dummy vector store with some content
dummy_texts = [
    "LangChain offers many advanced RAG techniques.",
    "Improving retrieval is key for a production-ready RAG pipeline.",
    "Hybrid search and reranking are powerful tools.",
    "Semantic chunking enhances context understanding.",
    "Multi-query retrievers can broaden search results.",
    "The future of RAG includes agentic retrieval and self-correction.",
    "You can build scalable RAG applications with LangChain.",
    "Explore LangChain advanced RAG techniques in this complete guide."
]
dummy_vectorstore = Chroma.from_texts(
    dummy_texts, embedding=DummyEmbeddings()
)
dummy_retriever = dummy_vectorstore.as_retriever(search_kwargs={"k": 2})

llm = DummyLLM() # Replace with actual LLM, e.g., OpenAI()

# Initialize MultiQueryRetriever
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=dummy_retriever, llm=llm
)

question = "What are the latest LangChain advanced RAG techniques?"
retrieved_docs = retriever_from_llm.get_relevant_documents(question)

print(f"Original Query: '{question}'")
print("\nGenerated Queries (simulated by LLM):")
# In a real run, MultiQueryRetriever would show these.
# For this dummy, we can infer from LLM's invoke output.
print("- What are LangChain advanced RAG techniques?")
print("- How to improve retrieval in RAG?")
print("- What makes RAG production-ready?")

print("\nRetrieved documents:")
for doc in retrieved_docs:
    print(f"- '{doc.page_content}'")
```
{% endraw %}

This example shows how `MultiQueryRetriever` generates several different versions of your original question. Each of these queries is then used to search the vector store. By doing this, you're much more likely to find all relevant pieces of information, leading to richer and more complete answers from your retrieval-augmented generation system.

#### 6. Multi-hop and Agentic Retrieval

Sometimes, answering a question needs more than just looking up a single piece of information. Imagine asking, "Who was the CEO of company X when they acquired company Y, and what year was that?" This might require finding Company X's acquisition history, then finding the CEO at that specific time. This is where multi-hop and agentic retrieval shine as LangChain advanced RAG techniques.

Multi-hop retrieval involves taking the answer from one search and using it as part of a new search. It's like a detective following clues. LangChain agents are perfect for this. An agent can decide what tools to use (like a search tool, a calculator, or a different RAG pipeline) and in what order, to answer complex questions. This creates a very dynamic and smart RAG pipeline.

You can create powerful AI agents with LangChain that can make decisions. You might be interested in our guides on [LangChain with Google Gemini function calling]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}) and [LangGraph StateGraph for multi-step agents]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}). These frameworks allow you to build AI systems that can perform complex, multi-step reasoning and retrieval.

Example of Agentic Retrieval (conceptual):

{% raw %}
```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import OpenAI

# This is a conceptual example for an agent.
# In a real setup, you'd define actual tools and a more complex LLM.

# Define a tool that mimics document retrieval
@tool
def search_company_docs(query: str) -> str:
    """Searches company internal documents for specific information."""
    if "CEO of ACME Corp in 2020" in query:
        return "John Doe was the CEO of ACME Corp in 2020."
    elif "acquisition of Widgets Inc by ACME Corp" in query:
        return "ACME Corp acquired Widgets Inc in 2021."
    return "Could not find relevant information."

@tool
def get_current_date() -> str:
    """Returns the current date."""
    return "Today is 2026-05-01."

tools = [search_company_docs, get_current_date]

# A dummy LLM for agent to use
class DummyAgentLLM:
    def invoke(self, prompt):
        if "ACME Corp acquired Widgets Inc" in prompt and "CEO" in prompt:
            # Simulate agent reasoning: "I found acquisition year. Now I need CEO for that year."
            return "I need to find the CEO of ACME Corp in 2021. " \
                   "Action: search_company_docs\nAction Input: CEO of ACME Corp in 2021"
        elif "CEO of ACME Corp in 2021" in prompt:
            return "Final Answer: Jane Smith was the CEO of ACME Corp in 2021 when they acquired Widgets Inc."
        return "Final Answer: I cannot answer that."

llm = DummyAgentLLM() # Replace with actual LLM like OpenAI()

# Define the agent's prompt
prompt_template = PromptTemplate.from_template("""
You are a helpful assistant. Answer the following questions as best you can.
You have access to the following tools:
{tools}
Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Observation can repeat multiple times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}
""")

# Create the agent
# Note: create_react_agent is for specific LLM types, for general use,
# you might use AgentExecutor.from_agent_and_tools directly or define a custom agent.
# For this example, we'll simulate the agent's thought process.

# A simple agent workflow simulation
question = "Who was the CEO of ACME Corp when they acquired Widgets Inc?"
print(f"Question: {question}")

# Step 1: LLM (agent) thinks and uses search_company_docs for acquisition info
print("Thought: I need to find when ACME Corp acquired Widgets Inc.")
print("Action: search_company_docs")
print("Action Input: acquisition of Widgets Inc by ACME Corp")
observation1 = search_company_docs("acquisition of Widgets Inc by ACME Corp")
print(f"Observation: {observation1}")

# Step 2: LLM (agent) thinks again, now knowing the year, and uses search_company_docs for CEO info
print("Thought: ACME Corp acquired Widgets Inc in 2021. Now I need to find the CEO of ACME Corp in 2021.")
print("Action: search_company_docs")
print("Action Input: CEO of ACME Corp in 2021")
observation2 = search_company_docs("CEO of ACME Corp in 2021")
print(f"Observation: {observation2}")

# Step 3: LLM (agent) forms final answer
print("Thought: I have found that ACME Corp acquired Widgets Inc in 2021 and Jane Smith was the CEO at that time.")
print("Final Answer: Jane Smith was the CEO of ACME Corp in 2021 when they acquired Widgets Inc.")

```
{% endraw %}

This simulated example shows how a LangChain agent can break down a complex question into smaller steps. It uses different tools (like a RAG retriever or an external API) for each step. This allows for much more sophisticated retrieval-augmented generation that goes beyond simple lookups, making your RAG pipeline highly capable.

#### 7. Adapting for Different Data Types

Most RAG examples focus on text documents. But what if your knowledge base includes images, videos, or structured data like tables? LangChain advanced RAG techniques can extend to these as well. This is often called multi-modal RAG.

For images or videos, you might create text descriptions or use special models to turn them into embeddings. Then, you can store these embeddings in your vector store alongside text. When a query comes in, the system can retrieve not just text, but also relevant images or video clips. This enriches the information available for retrieval-augmented generation, providing a more comprehensive response.

### Building a Production-Ready LangChain RAG Pipeline

Moving from a basic RAG setup to one that's ready for real users requires careful planning. You need to pick the right tools and constantly check if your system is working well. This section will guide you through making your RAG pipeline robust and reliable.

#### Choosing Your Tools

The heart of your RAG pipeline depends on a few key choices:

*   **Vector Store:** This is where your document embeddings live. Popular choices for LangChain include Weaviate, Pinecone, Chroma, and many others. Each has its strengths in terms of scalability, features (like hybrid search or metadata filtering), and cost. For example, Weaviate is excellent for hybrid search, as we discussed.
*   **Embedding Model:** This model turns your text into numerical embeddings. Models like OpenAI's `text-embedding-ada-002` or various open-source models (e.g., from Hugging Face) are common. The quality of your embeddings directly impacts retrieval accuracy, so choose wisely.
*   **LLM (Large Language Model):** This is the "brain" that generates the answer. You might use models like OpenAI's GPT-4, Google's Gemini, or open-source alternatives like Llama 3. The LLM's capability to understand context and generate coherent text is crucial for good retrieval-augmented generation.

#### Evaluation and Monitoring

How do you know if your LangChain advanced RAG techniques are actually working? You need to measure their performance.

*   **Retrieval Metrics:**
    *   **Precision:** How many of the retrieved documents were actually relevant?
    *   **Recall:** How many of the *truly relevant* documents did your system manage to retrieve?
    *   **MRR (Mean Reciprocal Rank):** How high up in the list of retrieved documents was the *first relevant* document?
*   **Generation Metrics:**
    *   **Faithfulness:** Does the generated answer only use information from the retrieved documents? (Avoids hallucination).
    *   **Answer Relevance:** Is the generated answer truly relevant to the original question?
    *   **Context Relevance:** Is the retrieved context actually useful for answering the question?

Tools like LangSmith (from LangChain itself) can help you track and visualize these metrics. Setting up continuous monitoring ensures your RAG pipeline stays healthy.

#### Iterative Improvement

Building a perfect RAG system isn't a one-time job. It's an ongoing process. You will constantly learn from user feedback and evaluation metrics. Maybe some chunks are too long, or your reranker needs fine-tuning.

This iterative approach means you keep experimenting with different chunking strategies, vector store settings, query transformations, and reranking models. Each small improvement contributes to a more robust and effective RAG pipeline, ensuring your LangChain advanced RAG techniques truly deliver for your users.

### Practical Examples with LangChain

Let's put some of these ideas together with more comprehensive examples. These snippets will show you how to combine different LangChain advanced RAG techniques to build a smarter RAG pipeline.

#### Example 1: Hybrid Search with Reranking

This example demonstrates how to set up a RAG pipeline that uses both semantic and keyword search, then reranks the results. This is a powerful combination for production-ready retrieval-augmented generation.

First, you'd set up your vector store (like Weaviate for hybrid search) and embedding model. Then, you'd define your reranker.

{% raw %}
```python
import os
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import DocumentCompressor
from langchain_core.prompts import PromptTemplate

# --- 0. Set up API Keys and dummy components for demonstration ---
# In a real application, get these from environment variables
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# os.environ["WEAVIATE_API_KEY"] = "YOUR_WEAVIATE_API_KEY"
# os.environ["WEAVIATE_URL"] = "YOUR_WEAVIATE_URL"

# Dummy Weaviate client and embeddings for example purposes
class DummyWeaviateClient:
    def query(self):
        class QueryBuilder:
            def get(self, *args, **kwargs):
                return self
            def with_near_text(self, *args, **kwargs):
                return self
            def with_where(self, *args, **kwargs):
                return self
            def with_limit(self, *args, **kwargs):
                return self
            def do(self):
                # Simulate results for hybrid search
                return {
                    "data": {
                        "Get": {
                            "Docs": [
                                {"text": "LangChain provides many advanced RAG techniques for production."},
                                {"text": "Hybrid search combines vector and keyword search for better retrieval."},
                                {"text": "Reranking improves the precision of documents in the RAG pipeline."},
                                {"text": "The latest LangChain features include agentic retrieval."}
                            ]
                        }
                    }
                }
        return QueryBuilder()

dummy_weaviate_client = DummyWeaviateClient()

# Dummy embeddings
class DummyOpenAIEmbeddings:
    def embed_query(self, text: str) -> list[float]:
        return [0.1] * 1536 # Dummy vector
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[0.1] * 1536 for _ in texts]

embeddings = DummyOpenAIEmbeddings() # Replace with OpenAIEmbeddings()

# Dummy LLM
class DummyOpenAI:
    def invoke(self, prompt: str) -> str:
        if "LangChain advanced RAG techniques" in prompt and "hybrid search and reranking" in prompt:
            return "LangChain offers advanced RAG techniques like hybrid search and reranking. Hybrid search combines semantic and keyword searches to find the most relevant documents. Reranking then orders these documents to present the best ones first to the LLM, ensuring highly precise and production-ready retrieval."
        return "I am a dummy LLM and can't answer complex questions."

llm = DummyOpenAI() # Replace with OpenAI()

# --- 1. Set up Hybrid Retriever (Weaviate) ---
# In a real setup, connect to your Weaviate instance:
# from weaviate import Client
# weaviate_client = Client(url=os.environ["WEAVIATE_URL"], auth_client_secret=auth.AuthApiKey(api_key=os.environ["WEAVIATE_API_KEY"]))

# For demonstration, use the dummy client
vectorstore = Weaviate(
    client=dummy_weaviate_client,
    index_name="Docs", # Replace with your actual index name
    text_key="text",
    embedding=embeddings,
    by_text=False # Crucial for Weaviate's hybrid search to work as expected
)

# Weaviate's .as_retriever() can handle hybrid search directly with certain configurations.
# For this example, we'll demonstrate its use.
# A more explicit hybrid setup might involve custom combining of semantic and keyword search.
# For simplicity, assuming the vectorstore.as_retriever handles text and near_text
base_retriever = vectorstore.as_retriever(
    search_type="mmr", # Or "similarity_score_threshold", "similarity"
    search_kwargs={
        "k": 10, # Retrieve more documents initially for reranking
        "alpha": 0.5, # For MMR (Maximal Marginal Relevance) - balance diversity and relevance
        # For actual Weaviate hybrid search, you'd specify query parameters like:
        # "query_properties": ["text"], "hybrid": {"query": "...", "alpha": 0.75}
    }
)

# --- 2. Implement Reranker ---
class CustomReranker(DocumentCompressor):
    def compress_documents(self, documents, query):
        print(f"\nReranker received {len(documents)} documents for query: '{query}'")
        # In a real reranker, you'd use a model (e.g., Cohere, bge-reranker) to score
        # For this example, we'll simulate sorting by a simple keyword presence.
        
        scored_docs = []
        for doc in documents:
            score = 0
            if "LangChain" in doc.page_content: score += 3
            if "RAG" in doc.page_content: score += 2
            if "hybrid search" in doc.page_content: score += 4
            if "reranking" in doc.page_content: score += 5
            if "production" in doc.page_content: score += 1
            doc.metadata["rerank_score"] = score
            scored_docs.append(doc)
            
        reranked_docs = sorted(scored_docs, key=lambda x: x.metadata["rerank_score"], reverse=True)
        
        # Return only the top 3 most relevant documents
        print(f"Reranker returning top 3 documents out of {len(reranked_docs)}")
        return reranked_docs[:3]

compressor = CustomReranker()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=base_retriever
)

# --- 3. Build the RAG Chain ---
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=compression_retriever,
    return_source_documents=True
)

# --- 4. Ask a question ---
query = "What are the benefits of using LangChain advanced RAG techniques like hybrid search and reranking?"
result = qa_chain.invoke({"query": query})

print(f"\n--- Original Query --- \n{query}")
print(f"\n--- Generated Answer --- \n{result['result']}")
print(f"\n--- Source Documents (after hybrid search and reranking) ---")
for i, doc in enumerate(result["source_documents"]):
    print(f"Doc {i+1} (Score: {doc.metadata.get('rerank_score', 'N/A')}): {doc.page_content}")
```
{% endraw %}

This example sets up a more sophisticated RAG pipeline. It first retrieves documents using a method that mimics hybrid search. Then, it uses a custom reranker to sort these documents, ensuring the most relevant ones are passed to the LLM. This combination of LangChain advanced RAG techniques significantly boosts the accuracy and precision of your retrieval-augmented generation.

#### Example 2: Multi-Query Retriever

This example shows how a multi-query retriever can broaden your search. Instead of just one query, the LLM generates multiple variations, increasing the chance of finding more diverse and relevant information.

{% raw %}
```python
from langchain.retrievers import MultiQueryRetriever
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# --- 0. Set up API Keys and dummy components for demonstration ---
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Dummy LLM
class DummyLLMMultiQuery:
    def invoke(self, prompt: str) -> str:
        if "generate alternative questions" in prompt:
            # Simulate generating multiple questions for a single user query
            return "Alternative questions:\n" \
                   "1. What are the key features of LangChain's advanced RAG?\n" \
                   "2. How can I make my RAG pipeline production-ready with LangChain?\n" \
                   "3. What are effective retrieval strategies using LangChain?"
        return "Dummy LLM response."

llm = DummyLLMMultiQuery() # Replace with OpenAI()

# Dummy embeddings
embeddings = DummyOpenAIEmbeddings() # Using the same dummy from previous example

# Sample documents for our vector store
documents = [
    Document(page_content="LangChain provides tools for building robust RAG pipelines."),
    Document(page_content="Advanced RAG techniques include hybrid search and reranking."),
    Document(page_content="To make RAG production-ready, focus on evaluation and iterative improvement."),
    Document(page_content="Semantic chunking is a key LangChain advanced RAG technique."),
    Document(page_content="LangChain agents enable multi-hop retrieval for complex queries."),
    Document(page_content="Ensure your RAG pipeline is scalable for real-world applications."),
    Document(page_content="Explore various vector stores to optimize your LangChain RAG system."),
    Document(page_content="This guide covers a complete set of LangChain advanced RAG techniques."),
    Document(page_content="You can use custom output parsers in LangChain for structured responses."),
    Document(page_content="LangGraph helps build multi-step AI agents and stateful applications.")
]

# --- 1. Create a Vector Store and Base Retriever ---
vectorstore = Chroma.from_documents(documents, embeddings)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) # Retrieve 2 docs per query

# --- 2. Initialize MultiQueryRetriever ---
multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever, llm=llm
)

# --- 3. Ask a question and retrieve ---
original_query = "What are the best ways to improve RAG with LangChain?"
retrieved_docs = multiquery_retriever.get_relevant_documents(original_query)

print(f"Original Query: '{original_query}'")
print("\n--- Simulated Generated Queries ---")
print("1. What are the key features of LangChain's advanced RAG?")
print("2. How can I make my RAG pipeline production-ready with LangChain?")
print("3. What are effective retrieval strategies using LangChain?")

print("\n--- Retrieved Documents (from all queries) ---")
# MultiQueryRetriever automatically deduplicates, so we print unique ones
unique_docs_content = set()
for doc in retrieved_docs:
    if doc.page_content not in unique_docs_content:
        print(f"- {doc.page_content}")
        unique_docs_content.add(doc.page_content)

print(f"\nTotal unique documents retrieved: {len(unique_docs_content)}")
```
{% endraw %}

This example clearly shows how a `MultiQueryRetriever` in LangChain helps your RAG pipeline. By generating several queries from a single user input, it explores more angles in your vector store. This leads to a wider and often more relevant set of documents. This technique significantly enhances the retrieval-augmented generation process, especially for complex or ambiguous questions, making your system much more effective.

### Future of LangChain Advanced RAG Techniques

The world of AI is always changing, and so are LangChain advanced RAG techniques. We can expect even smarter ways for RAG pipelines to work. Imagine systems that can automatically detect when they've made a mistake and correct themselves. This is called self-correction.

Future RAG systems will likely include more sophisticated agents. These agents will be able to reason, plan, and use a wider variety of tools to gather information. Active learning will also become more common. This means the RAG system learns from its mistakes and improves its retrieval over time. These advancements will make retrieval-augmented generation even more powerful and reliable.

### Conclusion

You've now explored the exciting world of LangChain advanced RAG techniques. We've seen how to move beyond basic retrieval to build a truly production-ready RAG pipeline. From smarter chunking and hybrid search to reranking and multi-query retrievers, you have the knowledge to make your AI applications super smart.

These LangChain advanced RAG techniques are essential for delivering accurate, reliable, and powerful retrieval-augmented generation. By understanding and implementing these strategies, you can build AI systems that truly understand and answer complex questions. Start experimenting with these tools today and unlock the full potential of your RAG applications!