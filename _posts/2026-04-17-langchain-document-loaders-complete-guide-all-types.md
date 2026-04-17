---
title: "Complete Guide to LangChain Document Loaders: Every Loader Type with Examples"
description: "Master every LangChain document loader type with our complete guide, featuring practical examples to efficiently load data into your powerful LLM applications."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain document loader types]
featured: false
image: '/assets/images/langchain-document-loaders-complete-guide-all-types.webp'
---

## Complete Guide to LangChain Document Loaders: Every Loader Type with Examples

Welcome to this in-depth guide on LangChain document loader types! If you're building smart AI applications, you know how important it is to get your data into a usable format. LangChain document loaders are like magical tools that help you do just that. They transform raw information from all sorts of places into a special format LangChain can understand.

This guide will show you how to use every important LangChain document loader type. You'll learn what they are, when to use them, and see practical examples for each. By the end, you'll be a pro at bringing your data into your LangChain projects. Let's dive into the world of getting your data ready for AI.

### What Are LangChain Document Loaders?

Imagine you have information stored in many different ways – a PDF file, text on a website, a spreadsheet, or a simple text document. For your AI application to "read" and understand this information, it needs a common way to access it. LangChain document loader types provide this common way. They take your data from its original home and turn it into `Document` objects.

A `Document` in LangChain is a simple container. It holds the actual text content of your data and some extra information, called metadata. This metadata can tell you things like where the document came from or its title. Think of it as a labeled box containing a piece of information.

These loaders are super important for building applications like Retrieval-Augmented Generation (RAG). RAG applications need to fetch relevant information to answer questions or generate text. Properly loading your data is the first crucial step in such systems. You can learn more about building robust RAG applications in LangChain here: [Build RAG Applications with LangChain Vector Store in 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

### The Core Idea: Loading Data into LangChain

Every LangChain document loader type works in a similar way. First, you choose the right loader for your data source. Then, you tell the loader where your data is located. Finally, you call a special method, usually `load()`, to get your data as a list of `Document` objects.

Let's look at the basic steps. You'll install the necessary libraries, then import the specific loader you need. After that, you'll create an instance of the loader, often by giving it a path or a URL. The `load()` method then does all the heavy lifting, giving you back your ready-to-use documents.

### Getting Started: Installation

Before we begin with the examples, you'll need to install LangChain and some other libraries. These extra libraries help LangChain understand different file types. We'll mention specific installations as we go for each LangChain document loader type.

However, a good start is to install LangChain itself. You can do this using `pip`. Many loaders also rely on `unstructured` for advanced parsing, so installing it early is often a good idea.

{% raw %}
```bash
pip install langchain
pip install unstructured
```
{% endraw %}

Now, let's explore the various LangChain document loader types. We will start with loaders for local files, which are often the most common starting point.

### Local File LangChain Document Loader Types

Many times, your data lives right on your computer as files. LangChain provides several loaders designed specifically for these local files. These are fundamental LangChain document loader types that you'll use constantly.

#### TextLoader: The Simplest Way to Load Text

The `TextLoader` is perhaps the most straightforward of all LangChain document loader types. It's used for loading plain text files. If your data is just raw text, this is your go-to option.

You use it when you have `.txt` files containing information you want your AI to process. It treats each file as one document. This makes it perfect for simple articles, notes, or code snippets.

**Example: Loading a Simple Text File**

First, let's create a sample text file. Name it `example.txt` in the same folder where your Python code will be. This will be the content our `TextLoader` will read.

**`example.txt`**
```
This is a sample text document.
It contains some information about LangChain.
LangChain helps build powerful AI applications.
```

Now, here's the Python code to load this file.

{% raw %}
```python
from langchain_community.document_loaders import TextLoader

# Create a sample text file (if not already created)
with open("example.txt", "w") as f:
    f.write("This is a sample text document.\n")
    f.write("It contains some information about LangChain.\n")
    f.write("LangChain helps build powerful AI applications.")

# Initialize the TextLoader with the path to your file
loader = TextLoader("example.txt")

# Load the documents
documents = loader.load()

# Print the loaded document
print(documents[0].page_content)
print(documents[0].metadata)
```
{% endraw %}

When you run this code, you'll see the full text content printed. You'll also see some metadata, like the `source` which tells you the file path. This shows how easily the `TextLoader` transforms your simple text file into a LangChain `Document`.

#### PDFLoader: Bringing PDFs to Life

PDFs are a very common way to share documents, from reports to research papers. The `PDFLoader` allows you to extract text from these files. This is one of the most powerful LangChain document loader types for dealing with common business and academic data.

You'll use it whenever you have information trapped inside PDF files. This could be anything from contracts and manuals to academic papers and e-books. It unlocks the knowledge within these often-difficult-to-parse formats.

To use `PDFLoader`, you need to install the `pypdf` library. This library is what LangChain uses behind the scenes to read PDF files.

{% raw %}
```bash
pip install pypdf
```
{% endraw %}

**Example: Loading a PDF Document**

Let's imagine you have a PDF file named `report.pdf`. For this example, you'd typically create a simple PDF with some text. You can use any PDF creator or even print a short text document to PDF.

**Python Code for PDFLoader**

{% raw %}
```python
from langchain_community.document_loaders import PyPDFLoader
import os

# Create a dummy PDF file for demonstration
# In a real scenario, you would have your PDF file ready.
# For simplicity, we'll assume 'report.pdf' exists in the current directory.
# You can manually create a simple PDF with content like "This is a PDF report about AI."
# For a runnable example, you'd need a way to generate a PDF,
# but for teaching, assume 'report.pdf' is present.

# Let's mock the existence of 'report.pdf' for explanation
# In a real run, ensure 'report.pdf' is in your directory.
if not os.path.exists("report.pdf"):
    print("Please create a 'report.pdf' file with some text content.")
    print("You can use an online tool or a text editor's print-to-PDF function.")
    # For demonstration, we will assume it exists and proceed.
    # If you are running this, ensure 'report.pdf' is present.

try:
    # Initialize the PyPDFLoader
    loader = PyPDFLoader("report.pdf")

    # Load the documents
    # Each page of the PDF often becomes a separate document
    documents = loader.load()

    # Print the content of the first page
    if documents:
        print(f"Content of page 1:\n{documents[0].page_content[:200]}...") # Print first 200 chars
        print(f"Metadata of page 1:\n{documents[0].metadata}")
    else:
        print("No documents loaded from the PDF. Is the PDF empty?")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Ensure 'report.pdf' exists and 'pypdf' is installed.")
```
{% endraw %}

The `PyPDFLoader` often creates one LangChain `Document` for each page of your PDF. This is very helpful if you want to process pages individually. The metadata for each document will typically include the `source` file and the `page` number.

#### CSVLoader: Working with Tabular Data

CSV files are like simple spreadsheets, used to store data in rows and columns. The `CSVLoader` helps you turn each row of a CSV file into a LangChain `Document`. This is one of the most useful LangChain document loader types for data-driven applications.

You'll use this loader when you have structured data in a CSV format. This could be anything from customer lists and sales data to sensor readings. Each row represents a record, and the `CSVLoader` makes each record a separate document.

To use `CSVLoader`, you need to install `pandas`, a powerful data analysis library.

{% raw %}
```bash
pip install pandas
```
{% endraw %}

**Example: Loading a CSV File**

Let's create a sample CSV file named `products.csv`. It will contain some simple product information.

**`products.csv`**
```csv
id,name,category,price
1,Laptop,Electronics,1200
2,Keyboard,Accessories,75
3,Mouse,Accessories,25
4,Monitor,Electronics,300
```

Now, here's the Python code to load this CSV data.

{% raw %}
```python
from langchain_community.document_loaders.csv_loader import CSVLoader
import os

# Create a sample CSV file (if not already created)
csv_content = """id,name,category,price
1,Laptop,Electronics,1200
2,Keyboard,Accessories,75
3,Mouse,Accessories,25
4,Monitor,Electronics,300
"""
with open("products.csv", "w") as f:
    f.write(csv_content)

# Initialize the CSVLoader
# You can specify the text_content_columns if you want specific columns to be the main content.
# Otherwise, it concatenates all columns into the page_content.
loader = CSVLoader(file_path="products.csv", encoding="utf-8")

# Load the documents
documents = loader.load()

# Print the loaded documents
for i, doc in enumerate(documents[:2]): # Print first two for brevity
    print(f"--- Document {i+1} ---")
    print(f"Content:\n{doc.page_content}")
    print(f"Metadata:\n{doc.metadata}")
```
{% endraw %}

Notice how each row becomes a document. The `page_content` combines the values from all columns, and the `metadata` includes the `source` and `row` number. You can also specify which columns should be part of the `page_content` if you want more control.

#### JSONLoader: Parsing Structured JSON Data

JSON (JavaScript Object Notation) is a very popular format for storing structured data, especially when working with APIs and web services. The `JSONLoader` is one of the essential LangChain document loader types for integrating such data.

You use it when your data is in a JSON file or obtained as JSON from an API. It's great for configurations, user profiles, or complex data structures. The `JSONLoader` is powerful because it can extract specific parts of your JSON data using a method similar to `jq` queries.

To use `JSONLoader`, you might need `jq` for more complex paths, but often it works out of the box.

{% raw %}
```bash
pip install "jq" # if you need jq functionality, though it's often not strictly required for simple paths
```
{% endraw %}

**Example: Loading a JSON File**

Let's create a sample JSON file named `config.json`. This file will hold some settings.

**`config.json`**
```json
[
  {
    "app_name": "AI Assistant",
    "version": "1.0",
    "settings": {
      "mode": "dark",
      "language": "en"
    },
    "features": ["chat", "summarize"]
  },
  {
    "app_name": "Data Analyzer",
    "version": "2.1",
    "settings": {
      "mode": "light",
      "language": "es"
    },
    "features": ["analyze", "report"]
  }
]
```

Now, here's the Python code to load this JSON data. We'll use a `jq` path to tell the loader how to split the JSON into documents and what content to extract.

{% raw %}
```python
from langchain_community.document_loaders import JSONLoader
import os
import json

# Create a sample JSON file (if not already created)
json_data = [
  {
    "app_name": "AI Assistant",
    "version": "1.0",
    "settings": {
      "mode": "dark",
      "language": "en"
    },
    "features": ["chat", "summarize"]
  },
  {
    "app_name": "Data Analyzer",
    "version": "2.1",
    "settings": {
      "mode": "light",
      "language": "es"
    },
    "features": ["analyze", "report"]
  }
]
with open("config.json", "w") as f:
    json.dump(json_data, f, indent=2)

# Initialize the JSONLoader
# The jq_schema helps extract specific parts. '$[]' means iterate through the top-level array.
# You can also provide a metadata_func to add custom metadata.
loader = JSONLoader(
    file_path="config.json",
    jq_schema=".", # '.' means load the whole object as a document. '$[]' for array elements.
    text_content=False # Set to True if you want a specific field as content, False to dump the whole dict
)

# Load the documents
documents = loader.load()

# Print the loaded documents
for i, doc in enumerate(documents):
    print(f"--- Document {i+1} ---")
    print(f"Content:\n{doc.page_content}")
    print(f"Metadata:\n{doc.metadata}")

# Example with a specific jq_schema for extraction
print("\n--- Loading with specific jq_schema for content ---")
loader_specific = JSONLoader(
    file_path="config.json",
    jq_schema=".[]", # Iterate over array elements
    text_content=False # Will dump each dict as string if False. If True, needs a content_key.
)
documents_specific = loader_specific.load()
for i, doc in enumerate(documents_specific):
    print(f"--- Document {i+1} (specific) ---")
    print(f"Content:\n{doc.page_content}")
    print(f"Metadata:\n{doc.metadata}")


# Example with content_key for page_content
print("\n--- Loading with content_key ---")
loader_content_key = JSONLoader(
    file_path="config.json",
    jq_schema=".[]",
    content_key="app_name" # Use 'app_name' field as the main content
)
documents_content_key = loader_content_key.load()
for i, doc in enumerate(documents_content_key):
    print(f"--- Document {i+1} (content_key) ---")
    print(f"Content:\n{doc.page_content}")
    print(f"Metadata:\n{doc.metadata}")
```
{% endraw %}

The `JSONLoader` is very flexible. You can use `jq_schema` to tell it exactly how to break down your JSON and what pieces of information to put into the `page_content`. You can also define a `content_key` if you want a specific field from your JSON object to be the `page_content`.

#### UnstructuredLoader: Handling Many Document Types

Sometimes, your data isn't neatly in a `.txt`, `.pdf`, or `.csv` file. You might have Word documents (`.docx`), PowerPoints (`.pptx`), or even emails. The `UnstructuredLoader` is a powerful and versatile tool for these situations. It's one of the most comprehensive LangChain document loader types for diverse file formats.

You should use `UnstructuredLoader` when you have a mix of document types or formats that other specific loaders don't cover. It can intelligently extract text and metadata from a wide range of files. This includes documents like `.doc`, `.docx`, `.pptx`, `.eml`, and many more.

To use this loader, you need to install the `unstructured` library and potentially some extra dependencies based on the file types you want to process.

{% raw %}
```bash
pip install unstructured
# For specific file types, you might need extra dependencies, e.g.:
# pip install "unstructured[docx]"
# pip install "unstructured[pdf]"
# pip install "unstructured[pptx]"
```
{% endraw %}

**Example: Loading a Word Document with UnstructuredLoader**

For this example, you'd typically create a simple `.docx` file. Let's imagine you have `meeting_notes.docx`. You can use Microsoft Word or Google Docs to create one with content like: "These are meeting notes from the Q1 review. Key topics included sales performance and marketing strategies."

**Python Code for UnstructuredLoader**

{% raw %}
```python
from langchain_community.document_loaders import UnstructuredFileLoader
import os

# Create a dummy .docx file for demonstration purposes.
# In a real scenario, you would have your .docx file ready.
# Manually create 'meeting_notes.docx' with some text.
if not os.path.exists("meeting_notes.docx"):
    print("Please create a 'meeting_notes.docx' file with some text content.")
    print("You can use a word processor like Microsoft Word or LibreOffice Writer.")
    # For demonstration, we will assume it exists and proceed.

try:
    # Initialize the UnstructuredFileLoader with the path to your .docx file
    loader = UnstructuredFileLoader("meeting_notes.docx")

    # Load the documents
    documents = loader.load()

    # Print the loaded document content and metadata
    if documents:
        print(f"Content of the document:\n{documents[0].page_content[:300]}...") # Print first 300 chars
        print(f"Metadata of the document:\n{documents[0].metadata}")
    else:
        print("No documents loaded from the .docx file. Is it empty?")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Ensure 'meeting_notes.docx' exists and 'unstructured' is installed.")
```
{% endraw %}

The `UnstructuredFileLoader` is incredibly flexible. It automatically detects the file type and uses the best parsing method. This means you can use it for many different local file LangChain document loader types. Its metadata can also be very rich, including elements like `file_type`, `filename`, and `last_modified`.

#### DirectoryLoader: Loading Files in Bulk

When you have many files of the same type in a folder, you don't want to load them one by one. The `DirectoryLoader` comes to the rescue. It can process all files in a specified directory using a single underlying loader. This is a very efficient way to handle multiple LangChain document loader types at once.

You use `DirectoryLoader` when your data is organized into folders, and you want to ingest everything inside. This is common for document archives, code repositories, or large datasets split into many files. It streamlines the process of bulk data loading.

**Example: Loading Multiple Text Files from a Directory**

First, let's create a directory named `data` and put a few text files inside it.

**`data/file1.txt`**
```
This is the first document.
It talks about artificial intelligence.
```

**`data/file2.txt`**
```
This is the second document.
It discusses machine learning concepts.
```

Now, here's the Python code to load all `.txt` files from the `data` directory.

{% raw %}
```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
import os

# Create a 'data' directory and sample files
if not os.path.exists("data"):
    os.makedirs("data")

with open("data/file1.txt", "w") as f:
    f.write("This is the first document.\n")
    f.write("It talks about artificial intelligence.")

with open("data/file2.txt", "w") as f:
    f.write("This is the second document.\n")
    f.write("It discusses machine learning concepts.")

# Initialize the DirectoryLoader
# We specify the loader_cls to be TextLoader to handle .txt files.
loader = DirectoryLoader(
    "data/",
    glob="*.txt", # Only load files ending with .txt
    loader_cls=TextLoader,
    recursive=True # Set to True to search subdirectories as well
)

# Load the documents
documents = loader.load()

# Print the loaded documents
for i, doc in enumerate(documents):
    print(f"--- Document {i+1} ---")
    print(f"Content:\n{doc.page_content}")
    print(f"Metadata:\n{doc.metadata}")
```
{% endraw %}

The `DirectoryLoader` is a powerful wrapper. You can swap `TextLoader` with any other file-based loader like `PyPDFLoader` or `CSVLoader` to process directories full of different file types. It makes handling large collections of documents much simpler.

### Web and API LangChain Document Loader Types

Data doesn't always live on your local machine. A lot of valuable information is on the internet or accessible through APIs. LangChain offers specialized LangChain document loader types to fetch this web-based content.

#### WebBaseLoader: Capturing Web Page Content

The `WebBaseLoader` is your tool for grabbing content directly from web pages. If you need to include information from websites in your AI application, this loader makes it easy. It fetches the HTML content of a URL and then uses a library like `BeautifulSoup` to extract the main text.

You would use `WebBaseLoader` when you want to ingest articles, blog posts, or documentation from specific URLs. It's excellent for building knowledge bases from online sources. You might want to consider how to split these documents effectively for RAG, possibly using a semantic splitter like in [LangChain Semantic Text Splitter: Chunk by Meaning]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}).

To use `WebBaseLoader`, you need to install `BeautifulSoup4` and `requests`.

{% raw %}
```bash
pip install beautifulsoup4 requests
```
{% endraw %}

**Example: Loading Content from a Website**

Let's load content from a public website. We'll use the LangChain documentation website as an example.

{% raw %}
```python
from langchain_community.document_loaders import WebBaseLoader

# Initialize the WebBaseLoader with a list of URLs
loader = WebBaseLoader(["https://www.langchain.com/"])

# Load the documents
documents = loader.load()

# Print the loaded document content and metadata
if documents:
    print(f"Content from URL:\n{documents[0].page_content[:500]}...") # Print first 500 chars
    print(f"Metadata from URL:\n{documents[0].metadata}")
else:
    print("No documents loaded from the URL. Check the URL or your internet connection.")
```
{% endraw %}

The `WebBaseLoader` returns the main text content of the web page. The metadata usually includes the `source` URL and potentially the `title` of the page. This is a powerful way to bring live internet content into your LangChain applications.

#### YouTubeLoader: Transcribing Video Content

YouTube videos are a massive source of information. The `YouTubeLoader` can download the transcript of a YouTube video and turn it into a LangChain `Document`. This is a specialized but incredibly useful addition to the LangChain document loader types.

You would use `YouTubeLoader` if your knowledge base includes video tutorials, lectures, or interviews. By extracting the transcript, your AI can "read" and understand the spoken content of these videos. This opens up entirely new possibilities for RAG and information retrieval from multimedia.

To use `YouTubeLoader`, you need to install `youtube-transcript-api`.

{% raw %}
```bash
pip install youtube-transcript-api
```
{% endraw %}

**Example: Loading a YouTube Video Transcript**

We'll use a public YouTube video URL for this example.

{% raw %}
```python
from langchain_community.document_loaders import YoutubeLoader

# Initialize the YoutubeLoader with the video URL
# Use a public YouTube video URL. Example: a LangChain official video.
# For instance, a video like "LangChain Basics: Agents"
youtube_url = "https://www.youtube.com/watch?v=Lqg4wQx8u44" # Replace with a valid, public YouTube URL

loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=True)

# Load the documents
documents = loader.load()

# Print the loaded document content and metadata
if documents:
    print(f"Transcript content:\n{documents[0].page_content[:500]}...") # Print first 500 chars
    print(f"Metadata:\n{documents[0].metadata}")
else:
    print("No transcript loaded. Check the YouTube URL or if transcripts are available.")
```
{% endraw %}

The `YouTubeLoader` provides the video's transcript as the `page_content`. Its metadata is rich, often including the video `title`, `author`, `publish_date`, and the original `source` URL. This turns spoken words into searchable text for your AI.

#### NotionLoader: Accessing Your Notion Workspace

Many teams and individuals use Notion for notes, project management, and knowledge bases. The `NotionLoader` allows you to pull content directly from your Notion pages. This is a fantastic way to integrate your team's knowledge into AI applications.

You would use `NotionLoader` when your organization's documentation, meeting notes, or project details reside in Notion. It helps centralize your knowledge by making Notion content accessible to your LangChain agents. This is one of the more enterprise-focused LangChain document loader types.

To use `NotionLoader`, you need to set up a Notion integration and get an API token. You'll also need to install the `notion-client` library.

{% raw %}
```bash
pip install notion-client
```
{% endraw %}

**Example: Loading Content from Notion**

This example requires you to have a Notion integration and an API token. Replace `YOUR_NOTION_TOKEN` with your actual token and `YOUR_NOTION_PAGE_ID` with the ID of the page you want to load. Ensure your integration has access to the page.

{% raw %}
```python
from langchain_community.document_loaders import NotionLoader
import os

# Set your Notion API token as an environment variable
# Replace "YOUR_NOTION_TOKEN" with your actual Notion API token
# Replace "YOUR_NOTION_PAGE_ID" with the ID of the Notion page you want to load
# You can find the page ID in the URL of the Notion page: notion.so/{workspace}/{page_id}?v=...
os.environ["NOTION_TOKEN"] = "YOUR_NOTION_TOKEN"
notion_page_id = "YOUR_NOTION_PAGE_ID" # e.g., "aBcD1eF2..."

if os.environ.get("NOTION_TOKEN") == "YOUR_NOTION_TOKEN" or notion_page_id == "YOUR_NOTION_PAGE_ID":
    print("Please replace 'YOUR_NOTION_TOKEN' and 'YOUR_NOTION_PAGE_ID' with actual values.")
    print("Skipping NotionLoader example as credentials are not set.")
else:
    try:
        # Initialize the NotionLoader
        # Use the Notion block ID or page ID.
        loader = NotionLoader(notion_page_id, parent_as_page_content=True)

        # Load the documents
        documents = loader.load()

        # Print the loaded document content and metadata
        if documents:
            print(f"Content from Notion:\n{documents[0].page_content[:500]}...") # Print first 500 chars
            print(f"Metadata:\n{documents[0].metadata}")
        else:
            print("No documents loaded from Notion. Check page ID and token permissions.")

    except Exception as e:
        print(f"An error occurred loading from Notion: {e}")
        print("Ensure your Notion API token is valid and the integration has access to the page.")
```
{% endraw %}

The `NotionLoader` pulls text content from your specified Notion page. The metadata can include useful information like the `source` Notion page URL and `last_edited_time`. This makes your Notion knowledge base easily queryable by your LangChain applications.

#### GitHubLoader: Ingesting Code and Documentation

For developers, GitHub is a primary source of code, issues, and project documentation. The `GitHubLoader` lets you pull files directly from a GitHub repository. This is an indispensable tool for building AI assistants that understand your codebases or project wikis.

You would use `GitHubLoader` to ingest repository content for code analysis, bug reporting, or generating documentation. It's perfect for creating AI agents that can answer questions about your software projects. This is a specialized but powerful example of LangChain document loader types for technical teams.

To use `GitHubLoader`, you need to install `PyGithub`. You also need a GitHub Personal Access Token (PAT) for private repositories or to avoid rate limits on public ones.

{% raw %}
```bash
pip install PyGithub
```
{% endraw %}

**Example: Loading Files from a GitHub Repository**

Replace `YOUR_GITHUB_TOKEN` with your GitHub Personal Access Token if needed. For public repositories, you might not strictly need a token, but it helps avoid rate limits. Replace `repo_url` with the URL of the GitHub repository you want to load.

{% raw %}
```python
from langchain_community.document_loaders import GitHubLoader
from github import Github
import os

# Set your GitHub Personal Access Token (PAT) as an environment variable
# It's recommended to use an environment variable for tokens.
# Replace "YOUR_GITHUB_TOKEN" with your actual GitHub PAT.
# You can generate a PAT from your GitHub settings -> Developer settings -> Personal access tokens.
os.environ["GITHUB_TOKEN"] = "YOUR_GITHUB_TOKEN"

# Public repository example: LangChain's own repo for tutorials
repo_owner = "langchain-ai"
repo_name = "langchain"
repo_branch = "master" # Or 'main', 'dev', etc.

if os.environ.get("GITHUB_TOKEN") == "YOUR_GITHUB_TOKEN":
    print("Please set your GITHUB_TOKEN environment variable for better usage,")
    print("especially for private repos or to avoid rate limits.")
    print("Proceeding with public repo without explicit token, might hit rate limits.")
    github_token = None # No token for public access, may get rate limited.
else:
    github_token = os.environ.get("GITHUB_TOKEN")

try:
    # Initialize PyGithub client (optional, but good for authentication)
    if github_token:
        github_client = Github(github_token)
    else:
        github_client = Github() # Anonymous access

    # Get the repository object
    repo = github_client.get_user(repo_owner).get_repo(repo_name)

    # Initialize the GitHubLoader
    # filter_paths can specify which files/folders to include.
    # E.g., filter_paths=["docs/", "src/"]
    loader = GitHubLoader(
        repo=repo,
        branch=repo_branch,
        # filter_paths=["docs/"] # Example: only load files from the 'docs' folder
    )

    # Load the documents
    # This might take some time for large repositories.
    documents = loader.load()

    # Print the loaded document content and metadata (first few documents)
    if documents:
        print(f"Loaded {len(documents)} documents from GitHub.")
        for i, doc in enumerate(documents[:3]): # Print first 3 documents
            print(f"--- Document {i+1} ---")
            print(f"Source: {doc.metadata.get('source')}")
            print(f"Content:\n{doc.page_content[:200]}...") # Print first 200 chars
            print(f"Metadata:\n{doc.metadata}")
            print("-" * 20)
    else:
        print("No documents loaded from GitHub. Check repo details or token permissions.")

except Exception as e:
    print(f"An error occurred loading from GitHub: {e}")
    print("Ensure the repo_owner, repo_name, and GITHUB_TOKEN are correct.")
```
{% endraw %}

The `GitHubLoader` is very useful for code-related tasks. Each file from the repository that matches your criteria becomes a `Document`. The metadata often includes the `source` file path, `repo_name`, `branch`, and other relevant GitHub-specific details.

### Database and Cloud Storage LangChain Document Loader Types

Modern applications often store vast amounts of data in databases or cloud storage services. LangChain provides LangChain document loader types to access these critical data sources directly.

#### S3DirectoryLoader / GCSDirectoryLoader: From Cloud Storage

Cloud storage services like Amazon S3 and Google Cloud Storage (GCS) are popular for storing large datasets and various files. `S3DirectoryLoader` and `GCSDirectoryLoader` let you pull data from specified buckets or folders within them. These are essential LangChain document loader types for cloud-native applications.

You'd use these loaders when your source data is hosted in the cloud. This could be anything from log files and backup documents to large media archives. They enable your AI to access vast amounts of data stored reliably in the cloud.

To use these, you need to install the respective cloud SDKs (`boto3` for S3, `google-cloud-storage` for GCS). You also need to configure your AWS or GCP credentials.

{% raw %}
```bash
pip install boto3 # For S3
pip install google-cloud-storage # For GCS
```
{% endraw %}

**Example: Loading from Google Cloud Storage (GCS)**

This example assumes you have a GCS bucket with some files and your GCP credentials are set up. Replace `YOUR_BUCKET_NAME` with your actual bucket name and `YOUR_PREFIX` with a folder path if needed.

{% raw %}
```python
from langchain_community.document_loaders import GCSDirectoryLoader
import os

# Replace with your actual GCS bucket name and an optional prefix (folder path)
bucket_name = "YOUR_BUCKET_NAME"
prefix = "my_documents/" # Example: if your files are in a folder called 'my_documents'

if bucket_name == "YOUR_BUCKET_NAME":
    print("Please replace 'YOUR_BUCKET_NAME' with your actual GCS bucket name.")
    print("Skipping GCSDirectoryLoader example as bucket name is not set.")
else:
    try:
        # For a practical example, ensure your GCP credentials are configured (e.g., via gcloud CLI or service account).
        # You can also manually upload some text files to your GCS bucket under the specified prefix.

        # Initialize the GCSDirectoryLoader
        # You can specify a loader_cls to process specific file types, e.g., TextLoader.
        # If not specified, it uses UnstructuredFileLoader by default for diverse types.
        loader = GCSDirectoryLoader(
            project_name="your-gcp-project-id", # Optional: Specify your GCP project ID
            bucket=bucket_name,
            prefix=prefix,
            loader_cls=TextLoader, # Example: use TextLoader for .txt files
            # glob="*.txt" # Optional: only load files matching this pattern
        )

        # Load the documents
        documents = loader.load()

        # Print the loaded documents
        if documents:
            print(f"Loaded {len(documents)} documents from GCS.")
            for i, doc in enumerate(documents[:2]): # Print first 2 documents
                print(f"--- Document {i+1} ---")
                print(f"Content:\n{doc.page_content[:200]}...")
                print(f"Metadata:\n{doc.metadata}")
        else:
            print("No documents loaded from GCS. Check bucket, prefix, and permissions.")

    except Exception as e:
        print(f"An error occurred loading from GCS: {e}")
        print("Ensure your GCP credentials are set up and the bucket/prefix exist.")
```
{% endraw %}

These cloud loaders effectively bridge your cloud storage with your LangChain applications. They ensure that even geographically distributed or highly scaled data sources can feed into your AI.

#### WeaviateLoader: Loading from a Vector Database

While most loaders bring data *into* LangChain from raw sources, some can load existing `Document` objects from vector databases. The `WeaviateLoader` is an example that allows you to fetch documents stored in a Weaviate instance. This is a special case of LangChain document loader types for advanced RAG patterns.

You would use `WeaviateLoader` if you want to perform operations on documents already stored in a vector database. This could be for re-processing, debugging, or migrating data. It allows you to retrieve the original `Document` objects, including their `page_content` and metadata. This ties into scalable RAG architectures, as discussed in [LangChain Weaviate Hybrid Search for Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

To use `WeaviateLoader`, you need to install `weaviate-client`. You also need a running Weaviate instance.

{% raw %}
```bash
pip install weaviate-client
```
{% endraw %}

**Example: Loading Documents from Weaviate**

This example assumes you have a Weaviate instance running and some data already indexed within a collection (class). We'll first create a dummy Weaviate instance and add some data for demonstration.

{% raw %}
```python
from langchain_community.document_loaders import WeaviateLoader
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
import weaviate
from weaviate.embedded import EmbeddedClient
import os

# Set dummy API key for OpenAIEmbeddings if you're not using it or provide a real one
# os.environ["OPENAI_API_KEY"] = "sk-..." # Replace with your actual OpenAI API key if needed

# 1. Start an embedded Weaviate instance for testing
client = weaviate.Client(embedded=EmbeddedClient())
client.schema.delete_all() # Clear existing schema

# 2. Create a Weaviate schema (class)
class_name = "MyLangChainDocument"
client.schema.create({
    "classes": [{
        "class": class_name,
        "properties": [
            {"name": "text", "dataType": ["text"]},
            {"name": "source", "dataType": ["text"]}
        ],
        "vectorizer": "text2vec-openai" # Requires OpenAI API key or other vectorizer
    }]
})

# 3. Add some dummy documents to Weaviate
documents_to_add = [
    Document(page_content="The quick brown fox jumps over the lazy dog.", metadata={"source": "story"}),
    Document(page_content="LangChain makes building LLM applications easier.", metadata={"source": "blog"}),
    Document(page_content="Vector databases are crucial for RAG.", metadata={"source": "tutorial"}),
]

# Use a dummy embedding model if OpenAI key is not set, or a real one.
# For simplicity, if no OpenAI key, we'll skip actual vectorization for now
# or use a mock. For a full RAG, embeddings are crucial.
if os.environ.get("OPENAI_API_KEY"):
    embeddings = OpenAIEmbeddings()
    vectorstore = Weaviate(client, class_name, "text", embeddings)
    vectorstore.add_documents(documents_to_add)
    print("Documents added to Weaviate with embeddings.")
else:
    print("OPENAI_API_KEY not set. Skipping actual document addition with embeddings to Weaviate.")
    print("For WeaviateLoader to work, documents must already exist in Weaviate.")
    print("Please ensure your Weaviate instance has data for a full test.")
    # For this example, we will assume some documents exist if this path is taken.
    # In a real scenario, you'd have pre-existing data or the above embeddings config.

# 4. Use WeaviateLoader to load documents from Weaviate
print("\n--- Loading documents using WeaviateLoader ---")
try:
    loader = WeaviateLoader(query=None, attributes=["text", "source"], client=client, index_name=class_name)

    # Load the documents
    # The query can be customized to filter documents from Weaviate
    documents = loader.load()

    # Print the loaded documents
    if documents:
        print(f"Loaded {len(documents)} documents from Weaviate.")
        for i, doc in enumerate(documents):
            print(f"--- Document {i+1} ---")
            print(f"Content:\n{doc.page_content}")
            print(f"Metadata:\n{doc.metadata}")
    else:
        print("No documents loaded from Weaviate. Check class name and if data exists.")

except Exception as e:
    print(f"An error occurred with WeaviateLoader: {e}")
    print("Ensure Weaviate is running and contains data in the specified class.")

finally:
    # Clean up (optional for embedded client)
    try:
        client.close()
    except Exception as e:
        print(f"Error closing Weaviate client: {e}")
```
{% endraw %}

The `WeaviateLoader` is powerful for retrieving existing `Document` objects from your vector store. You can specify a query to fetch only relevant documents, making it versatile for many advanced RAG patterns.

### Specialized Loaders and Advanced Concepts

Beyond the common LangChain document loader types, there are many specialized ones for various niches. LangChain's ecosystem is vast, covering almost any data source imaginable.

*   **Email Loader:** For `.eml` files, perfect for processing customer support tickets or internal communications.
*   **Evernote Loader:** To pull notes from Evernote.
*   **Confluence Loader:** For organizations using Confluence as a knowledge base.
*   **Google Drive Loaders:** For documents stored in Google Drive, Sheets, Docs, etc.
*   **Microsoft SharePoint Loader:** Integrating with enterprise SharePoint environments.
*   **Figma Loader:** For design documents and UI/UX research.
*   **Obsidian Loader:** For users who keep notes in Obsidian.

The list goes on, and new LangChain document loader types are constantly being added. Always check the official LangChain documentation for the most up-to-date list and specific installation instructions.

### Beyond Loading: What Happens Next?

Once your data is loaded into `Document` objects, the journey often doesn't end there. For many AI applications, especially RAG, you'll need to process these documents further. A common next step is "chunking" or "splitting" the documents into smaller, manageable pieces. This helps the AI focus on relevant information.

You can use various text splitters for this purpose. LangChain offers `RecursiveCharacterTextSplitter`, `MarkdownTextSplitter`, and even more advanced options like the `SemanticTextSplitter`. Learning about these is crucial for effective RAG. Check out how to split text by meaning here: [LangChain Semantic Text Splitter: Chunk by Meaning]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}).

After splitting, these chunks are often converted into numerical representations called embeddings. These embeddings are then stored in a vector database, making them searchable by similarity. This forms the backbone of a RAG pipeline, enabling your AI to find and use relevant information.

### Choosing the Right LangChain Document Loader

With so many LangChain document loader types available, how do you pick the best one? Here's a quick guide:

1.  **Identify Your Data Source:** Where is your data currently stored? (e.g., local file, website, cloud storage, database).
2.  **Determine Your Data Format:** What type of file is it? (e.g., text, PDF, CSV, JSON, Word, Notion page).
3.  **Check Dependencies:** Does the loader require any extra installations? Make sure you have them.
4.  **Consider Structure:** Is your data highly structured (like CSV/JSON) or unstructured (like plain text/PDF)? This affects how you'll want to process it.

Here's a table summarizing some common LangChain document loader types and their use cases:

| Loader Type           | Data Source         | File Type/Format          | Key Dependencies (if any)      | Typical Use Case                                     |
| :-------------------- | :------------------ | :------------------------ | :----------------------------- | :--------------------------------------------------- |
| `TextLoader`          | Local Files         | `.txt`                    | None                           | Simple text articles, code snippets                  |
| `PyPDFLoader`         | Local Files         | `.pdf`                    | `pypdf`                        | Reports, research papers, e-books                    |
| `CSVLoader`           | Local Files         | `.csv`                    | `pandas`                       | Tabular data, spreadsheets                           |
| `JSONLoader`          | Local Files         | `.json`                   | `jq` (optional for complex paths) | Structured data, API responses                       |
| `UnstructuredFileLoader` | Local Files         | `.docx`, `.pptx`, `.eml`  | `unstructured` (with extras)   | Diverse document types, emails, presentations        |
| `DirectoryLoader`     | Local Folders       | Multiple (with `loader_cls`) | Depends on `loader_cls`         | Batch processing many files in a folder              |
| `WebBaseLoader`       | Web                 | HTML pages                | `beautifulsoup4`, `requests`   | Websites, blogs, online documentation                |
| `YoutubeLoader`       | YouTube             | Video transcripts         | `youtube-transcript-api`       | Video content, lectures, interviews                  |
| `NotionLoader`        | Notion              | Notion pages              | `notion-client`                | Team wikis, project notes, internal documentation    |
| `GitHubLoader`        | GitHub              | Repository files          | `PyGithub`                     | Codebases, project documentation, issue discussions  |
| `GCSDirectoryLoader`  | Google Cloud Storage| Multiple (with `loader_cls`) | `google-cloud-storage`         | Cloud-hosted files, logs, backups                    |
| `S3DirectoryLoader`   | AWS S3              | Multiple (with `loader_cls`) | `boto3`                        | Cloud-hosted files, large data lakes                 |
| `WeaviateLoader`      | Weaviate Vector DB  | `Document` objects        | `weaviate-client`              | Retrieving already-indexed documents for re-processing |

This table should help you quickly identify the best LangChain document loader type for your specific needs. Remember, the LangChain library is always evolving, so explore its latest offerings! You can also build custom solutions, which you might find yourself doing for more unique data types. For example, creating custom output parsers to interpret specific data formats after loading is another advanced technique: [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}).

### Conclusion

You've now explored a wide array of LangChain document loader types, from simple text files to complex cloud storage and even vector databases. Understanding how to get your data into LangChain is the fundamental first step for almost any AI application you build. Without effective loaders, your AI agents wouldn't have the information they need to be intelligent.

These loaders empower you to connect your AI with the vast amount of information available in the world. Whether it's local files, web content, or enterprise systems, there's likely a LangChain document loader type ready to help. Keep experimenting with different loaders and integrating them into your projects. This will unlock powerful capabilities for your next AI application.

Remember, the quality of your AI's output often depends on the quality and relevance of the data it receives. Master these LangChain document loader types, and you'll be well on your way to building truly remarkable AI solutions. If you are exploring other frameworks, you might find this guide useful: [Top LangChain Alternatives 2026: 10 Frameworks Compared & Ranked]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}). Happy building!