---
title: "Complete Guide to LangChain Text Splitters: Every Splitter Type with Examples"
description: "Explore all LangChain text splitter types in this complete guide. Get practical examples for every splitter to boost your LLM application's performance."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain text splitter types]
featured: false
image: '/assets/images/langchain-text-splitters-complete-guide-all-types.webp'
---

## Complete Guide to LangChain Text Splitters: Every Splitter Type with Examples

Imagine you have a really long storybook, but you want to ask a clever robot to understand just a tiny part of it at a time. This is a bit like what happens when you work with big language models (LLMs) and lots of text. LLMs are smart, but they can only read so much text at once.

This is where LangChain text splitter types come in handy! They are like special tools that help you cut down big chunks of text into smaller, more manageable pieces. This guide will walk you through all the different ways LangChain can split your text, with simple examples for each.

### Why Do We Need to Split Text?

Think about talking to a friend. If you tell them a super long story without a break, they might get confused or forget the beginning. LLMs are similar; they have a "context window," which is like their short-term memory. If your text is longer than this window, the LLM can't process it all.

Splitting text into smaller chunks means the LLM can focus on one part at a time. This helps it understand your questions better and give more accurate answers. It's a crucial step in building many helpful AI applications, especially those that need to "read" and understand large documents, like RAG applications.

### Understanding the Core Ideas Behind Text Splitting

Before we dive into the different LangChain text splitter types, let's learn some basic ideas. These ideas help all text splitters work their magic.

#### Chunk Size

`chunk_size` tells the splitter how big each piece of text should be. It's like saying, "Cut the story into chapters of about 500 words each." This number is super important because it directly impacts how much information each small piece holds.

If your chunks are too small, they might lose important context or meaning. If they are too large, they might still be too big for your LLM's context window. Finding the right `chunk_size` is often a bit of an experiment.

#### Chunk Overlap

`chunk_overlap` is like a safety net. When you cut text into chunks, sometimes a sentence or idea might be split right in the middle. To prevent losing information at the edges of chunks, `chunk_overlap` makes sure that the end of one chunk also appears at the beginning of the next.

This overlap helps keep the meaning flowing smoothly between chunks. It ensures that if an important idea spans across two chunks, the LLM still sees both parts in context. This often improves the quality of responses you get from your LLM.

#### Separators

`separators` are the rules the splitter uses to decide where to cut. Imagine cutting a cake; you might use a knife along the lines of each slice. For text, separators can be things like double newlines (`\n\n`), single newlines (`\n`), spaces (` `), or even just single characters.

Some LangChain text splitter types use multiple separators, trying them one by one. If it can't split with the first separator, it tries the next, and so on. This intelligent approach helps create meaningful chunks.

#### Length Function

The `length_function` tells the splitter how to measure the size of a chunk. By default, it often counts characters. However, for LLMs, it's often more useful to count "tokens." Tokens are like words or parts of words that LLMs understand.

Different LLMs use different ways to count tokens, so choosing the right `length_function` can be important for accuracy. You might want to use a specific tokenizer that matches the LLM you are working with.

### The Base of All Splitters: `TextSplitter`

In LangChain, all the special text splitters come from a main helper called `TextSplitter`. You usually don't use `TextSplitter` directly because it's like a blueprint. Instead, you use the more specific LangChain text splitter types built upon it. These specific splitters add smart rules for how to cut text.

Let's explore the most common and useful LangChain text splitter types.

### 1. `CharacterTextSplitter`: Simple and Direct

The `CharacterTextSplitter` is one of the most basic LangChain text splitter types. It works by splitting text based on a given character or sequence of characters. It’s like taking a pair of scissors and cutting wherever you see a specific pattern.

You tell it what character to use as a separator, for example, a newline character (`\n`) or a period (`.`). It then tries to make chunks of a certain size, keeping the overlap in mind.

#### How it Works

1.  It looks for your chosen `separator`.
2.  It splits the text at every point it finds that separator.
3.  It then tries to combine these smaller pieces to form chunks that are close to your `chunk_size`, ensuring `chunk_overlap`.

#### When to Use `CharacterTextSplitter`

Use this splitter when your text has clear, consistent separators that mark natural breaks. For example, if you have a log file where each entry is on a new line, or a document where paragraphs are clearly separated by double newlines. It's straightforward and works well for simple structured texts.

#### Example of `CharacterTextSplitter`

Let's see how `CharacterTextSplitter` works with a simple story.

```python
from langchain.text_splitter import CharacterTextSplitter

long_text = """
Once upon a time, there was a tiny village nestled deep in a valley.
The villagers lived simple lives, farming the fertile land and telling stories by the fire.

One day, a mysterious traveler arrived.
He brought tales of distant lands and strange creatures.
The children gathered around him, wide-eyed with wonder.

The elder of the village, wise and old, listened carefully.
He knew that new ideas could bring both good and challenge.
"""

# Create a splitter that splits by double newline and makes chunks of 100 characters with 10 overlap
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=10,
    length_function=len,
    is_separator_regex=False, # Not using regular expressions for separator
)

chunks = text_splitter.create_documents([long_text])

print(f"Number of chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk.page_content)
    print(f"Chunk length: {len(chunk.page_content)}")
```

This code snippet will show you how the text is divided. You'll notice that the chunks try to respect the double newlines as primary breaks. The `chunk_size` and `chunk_overlap` then guide how these pieces are put together.

You can play around with the `separator` to see how it changes the splitting. For example, try `separator="\n"` to split by single newlines.

### 2. `RecursiveCharacterTextSplitter`: The Smart Chopper

The `RecursiveCharacterTextSplitter` is one of the most popular and versatile LangChain text splitter types. It's like a very clever person who tries different ways to cut text to find the best spots. It uses a list of separators and tries them one by one.

If the text is too big for the first separator, it tries the second, and so on. This makes it really good at handling documents with complex structures.

#### How it Works

1.  You give it a list of separators, like `["\n\n", "\n", " ", ""]`.
2.  It first tries to split the entire document using the first separator (`\n\n`).
3.  If any of the resulting chunks are still too big (longer than `chunk_size`), it takes those big chunks and tries to split *them* using the next separator (`\n`).
4.  This process continues recursively until all chunks are smaller than `chunk_size` or it runs out of separators. The last separator, usually an empty string `""`, will split by every character if necessary.

#### When to Use `RecursiveCharacterTextSplitter`

This is your go-to splitter for most general-purpose documents. It's excellent for articles, reports, books, or any text that has a natural hierarchy of breaks. For instance, a document might have sections separated by double newlines, paragraphs by single newlines, and sentences by spaces. This splitter will gracefully handle all these levels.

#### Example of `RecursiveCharacterTextSplitter`

Let's use a slightly more complex text to show its power.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

article_text = """
# Chapter 1: The Beginning

This is the first paragraph of the first chapter. It talks about a hero's humble origins.
The hero lived in a small village, far from the bustling cities.

## Section 1.1: Early Life

Here's a sub-section about the hero's childhood. He loved to explore the nearby woods.
His days were filled with adventure and innocent curiosity.

### Subsection 1.1.1: A Mysterious Discovery

One day, while playing, the hero stumbled upon an ancient artifact.
This discovery would change his life forever.
It was glowing faintly, hidden beneath a gnarled tree root.

# Chapter 2: The Journey Begins

The hero, now older and wiser, decided to leave his village.
He embarked on a perilous journey to uncover the artifact's secrets.

## Section 2.1: Trials and Tribulations

His path was fraught with danger. He faced mythical beasts and cunning sorcerers.
But his resolve never wavered.
"""

# Create a recursive splitter with common separators
recursive_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""], # Try double newline, then single, then space, then character
    chunk_size=200,
    chunk_overlap=20,
    length_function=len,
)

chunks = recursive_splitter.create_documents([article_text])

print(f"Number of chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk.page_content)
    print(f"Chunk length: {len(chunk.page_content)}")
```

Notice how the splitter tries to keep related sentences and paragraphs together. It first respects the chapter and section breaks, then paragraphs, and finally sentences. This makes the chunks much more meaningful for an LLM to process.

For more advanced semantic splitting, you might also be interested in the [LangChain Semantic Text Splitter]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}), which chunks text based on meaning rather than just characters or tokens.

### 3. `TokenTextSplitter`: For LLM-Friendly Chunks

The `TokenTextSplitter` is a special LangChain text splitter that doesn't count characters. Instead, it counts "tokens." Tokens are the basic units of text that large language models understand. Different LLMs have different ways of breaking text into tokens.

Using a `TokenTextSplitter` helps you create chunks that are directly aligned with an LLM's input limits. This is often more accurate than character-based splitting when dealing with LLMs.

#### How it Works

1.  You choose a specific tokenizer, like `Tiktoken` (used by OpenAI models) or a Hugging Face tokenizer.
2.  The splitter uses this tokenizer to convert your text into a list of tokens.
3.  It then splits this list of tokens into chunks of `chunk_size` tokens, ensuring `chunk_overlap` in terms of tokens.
4.  Finally, it converts these token chunks back into human-readable text strings.

#### When to Use `TokenTextSplitter`

This splitter is perfect when you need precise control over the token count for a specific LLM. If you are using OpenAI models, `Tiktoken` is the recommended choice. For other models, you might use a tokenizer from the Hugging Face `transformers` library. It's crucial for optimizing performance and avoiding exceeding an LLM's context window.

#### Example of `TokenTextSplitter` with Tiktoken

Let's use `Tiktoken` for our example, which is common for OpenAI's models.

```python
from langchain.text_splitter import TokenTextSplitter
# You might need to install tiktoken: pip install tiktoken
import tiktoken

long_story = """
The old lighthouse stood proudly on the jagged cliffs, its beam sweeping across the dark,
churning sea. For centuries, it had guided ships safely to shore, a silent guardian against the tempest.
Its keeper, an elderly man named Silas, had dedicated his life to its unwavering light.
He lived a solitary existence, his only companions the gulls and the relentless roar of the ocean.

One stormy night, a ship found itself in dire straits, caught in the grip of a fierce gale.
Silas, seeing the flickering signal of distress, knew he had to act.
He braved the howling winds and driving rain to ensure the light remained strong, a beacon of hope.
His dedication saved the ship, and its crew spoke of the lighthouse keeper's courage for years to come.
"""

# Create a TokenTextSplitter using the 'cl100k_base' encoding (common for OpenAI models)
# This encoding determines how tokens are counted.
token_splitter = TokenTextSplitter(
    encoding_name="cl100k_base", # For OpenAI models like GPT-4, GPT-3.5
    chunk_size=50, # 50 tokens per chunk
    chunk_overlap=10, # 10 tokens overlap
)

# You can also define your own length function if needed, but for TokenTextSplitter,
# specifying encoding_name is usually sufficient as it internally uses a token-based length.

chunks = token_splitter.create_documents([long_story])

print(f"Number of chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk.page_content)
    # To get the exact token length, we'd re-tokenize.
    # For simplicity, we'll just print character length, but remember the chunk_size is token-based.
    encoding = tiktoken.get_encoding("cl100k_base")
    print(f"Chunk token length: {len(encoding.encode(chunk.page_content))}")
```

In this example, `chunk_size=50` means each piece will contain roughly 50 tokens. This is often more precise for LLM inputs than counting characters. The `encoding_name` ensures that the token counting matches what the specific OpenAI models expect.

### 4. `MarkdownTextSplitter`: Understanding Markdown Structure

Many documents, especially those for developers or online articles, are written in Markdown format. Markdown uses special symbols like `#` for headings, `*` for lists, and ```` for code blocks. The `MarkdownTextSplitter` is one of the LangChain text splitter types designed to understand these symbols.

It splits text intelligently by respecting the structure of your Markdown document. This helps keep related information together, like a heading and its content, in the same chunk.

#### How it Works

1.  It uses specific Markdown elements as separators. These typically include headings (H1, H2, etc.), code blocks, blockquotes, and lists.
2.  It prioritizes larger structural breaks (like H1 headings) first.
3.  If a section is still too large, it will then try smaller breaks, much like the `RecursiveCharacterTextSplitter`.

#### When to Use `MarkdownTextSplitter`

If your input documents are in Markdown format, this splitter is your best friend. It ensures that your chunks maintain the logical flow and hierarchy of your document. This is particularly useful for processing documentation, blog posts, or README files.

#### Example of `MarkdownTextSplitter`

Let's see how it handles a Markdown-formatted document.

```python
from langchain.text_splitter import MarkdownTextSplitter

markdown_doc = """
# Project Overview

This document describes the amazing new project.
It aims to solve challenging problems using AI.

## Key Features

*   Feature A: Does X, Y, Z
*   Feature B: Integrates with existing systems
*   Feature C: User-friendly interface

### Installation

To install, follow these steps:

1.  Clone the repository:
    ```python
    git clone https://github.com/your/project.git
    cd project
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Future Plans

We plan to add more features in Q3 2026.
"""

# Create a MarkdownTextSplitter
markdown_splitter = MarkdownTextSplitter(
    chunk_size=150, # Example chunk size
    chunk_overlap=20, # Example overlap
    length_function=len,
)

chunks = markdown_splitter.create_documents([markdown_doc])

print(f"Number of chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk.page_content)
    print(f"Chunk length: {len(chunk.page_content)}")
```

You will observe that this splitter tries to keep headings, list items, and code blocks together within their respective chunks. This preserves the context that Markdown's structure provides, making it easier for an LLM to understand the document's organization.

### 5. `HTMLTextSplitter`: Parsing Web Pages

The internet is full of information stored in HTML format. HTML uses tags like `<p>` for paragraphs, `<h1>` for headings, and `<div>` for sections. The `HTMLTextSplitter` is another specialized LangChain text splitter designed to understand and break down web page content.

It intelligently extracts text from HTML, focusing on human-readable content and ignoring many of the structural tags. It then splits this cleaned text based on HTML elements.

#### How it Works

1.  It first uses a tool (like `BeautifulSoup`) to parse the HTML and extract the meaningful text. It tries to get rid of boilerplate like navigation menus or footers if possible.
2.  It then uses a list of HTML tags (like `<h1>`, `<h2>`, `<p>`, `<li>`, `<div>`) as separators.
3.  Similar to the recursive splitter, it tries the larger, more significant tags first for splitting.

#### When to Use `HTMLTextSplitter`

If you are scraping web pages or working with documents that are primarily in HTML, this is the splitter for you. It helps you get clean, readable chunks from web content, which is often messy and full of irrelevant tags. This is crucial for applications that process online articles, product descriptions, or forum posts.

#### Example of `HTMLTextSplitter`

Let's use a mock HTML snippet to demonstrate.

```python
from langchain.text_splitter import HTMLTextSplitter

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>My Awesome Blog Post</title>
</head>
<body>
    <header>
        <h1>Welcome to My Blog</h1>
        <p>A place for thoughts and ideas.</p>
    </header>
    <main>
        <article>
            <h2>Understanding Text Splitting</h2>
            <p>Text splitting is a crucial step in preparing documents for large language models. Without it, you cannot process very long texts.</p>
            <p>There are many different strategies, as we are exploring in this guide.</p>

            <h3>Why HTML splitting is useful</h3>
            <ul>
                <li>Extracts clean text</li>
                <li>Respects document structure</li>
                <li>Good for web scraping</li>
            </ul>

            <div class="footer-note">
                <p>This is a small note at the bottom.</p>
            </div>
        </article>
    </main>
    <footer>
        <p>Copyright 2026</p>
    </footer>
</body>
</html>
"""

# Create an HTMLTextSplitter
html_splitter = HTMLTextSplitter(
    chunk_size=100, # Example chunk size
    chunk_overlap=15, # Example overlap
    length_function=len,
)

chunks = html_splitter.create_documents([html_content])

print(f"Number of chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk.page_content)
    print(f"Chunk length: {len(chunk.page_content)}")
{% raw %}
``` 

This example shows how the `HTMLTextSplitter` intelligently pulls out the content. It will primarily focus on text within elements like `h1`, `h2`, `p`, and `li`, creating chunks that respect these natural breaks in web content.

### Other Useful LangChain Text Splitter Types

While the above are the most commonly used, LangChain offers even more specialized splitters:

*   **`SentenceTransformersTokenTextSplitter`**: Similar to `TokenTextSplitter` but specifically designed for models from the Sentence Transformers library, often used for embeddings. It uses the model's own tokenizer.
*   **`NLTKTextSplitter` and `SpacyTextSplitter`**: These splitters use powerful natural language processing (NLP) libraries, NLTK and SpaCy, to split text primarily by sentences. They are great if you need highly accurate sentence-level splitting.
*   **`SemanticTextSplitter`**: This is a more advanced splitter that uses embeddings to split text based on meaning, rather than just characters or tokens. It tries to ensure that each chunk represents a coherent idea. You can learn more about it in the [LangChain Semantic Text Splitter]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}) guide.

### Choosing the Right LangChain Text Splitter

With so many LangChain text splitter types, how do you pick the best one? Here's a quick guide:

| Document Type         | Recommended Splitter                                          | Why                                                                                                    |
| :-------------------- | :------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------- |
| General Documents     | `RecursiveCharacterTextSplitter`                              | Most flexible, tries multiple separators, good for varied structures.                                  |
| Simple Text, Logs     | `CharacterTextSplitter`                                       | When you have a very clear, consistent separator like `\n\n` or `\n`.                                  |
| LLM Input (OpenAI)    | `TokenTextSplitter` (with `tiktoken`)                         | Precise token count for specific LLMs, avoids exceeding context windows.                               |
| Markdown Files        | `MarkdownTextSplitter`                                        | Respects Markdown headings, lists, and code blocks, preserving document structure.                     |
| HTML Web Pages        | `HTMLTextSplitter`                                            | Cleans HTML and splits by semantic HTML tags like headings and paragraphs.                             |
| Sentence-level Needs  | `NLTKTextSplitter` or `SpacyTextSplitter`                     | When you absolutely need to split at sentence boundaries for linguistic tasks.                          |
| Meaning-based Chunks  | `SemanticTextSplitter`                                        | Advanced; chunks based on the meaning of the text, ideal for nuanced RAG.                              |

### Practical Considerations and Best Practices

Using LangChain text splitter types effectively involves more than just picking one. Here are some tips to get the best results:

#### Experimentation is Key

There's no single perfect `chunk_size` or `chunk_overlap` for every document or every LLM. You need to experiment! Try different values and examine the output chunks. What works best for a long novel might not work for a short FAQ document.

#### Maintaining Context

The goal of splitting is to create chunks that are still understandable on their own. Too small, and a chunk loses context. Too large, and it defeats the purpose of splitting. Aim for chunks that capture a complete idea or a few related sentences. `chunk_overlap` is crucial here to ensure continuity.

#### Handling Metadata

Many LangChain text splitter types can also help you attach `metadata` to your chunks. Metadata is extra information about where a chunk came from, like the page number, document title, or URL. This metadata is super useful later when the LLM needs to cite sources or understand the context of a retrieved chunk.

For instance, if you're building a RAG application, good metadata can help you identify the original source of the information. Learning about vector stores and RAG can further enhance your applications, as discussed in [Build RAG Applications with LangChain Vector Store in 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}). For more advanced RAG setups, consider [LangChain Weaviate Hybrid Search for Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

```
{% endraw %}python
# Example of adding metadata (often handled automatically by document loaders, but you can also pass it)
from langchain.docstore.document import Document

doc = Document(
    page_content="This is the content of my document.",
    metadata={"source": "my_report.pdf", "page": 1}
)

# When you split this, the metadata will often be carried over to the chunks
# For instance, if you were to load documents using a LangChain document loader:
# from langchain_community.document_loaders import TextLoader
# loader = TextLoader("example.txt")
# docs = loader.load() # Docs will have metadata like 'source'
```

#### Integration with Retrieval-Augmented Generation (RAG)

Text splitting is a foundational step for RAG applications. When you build a RAG system, you typically:
1.  Load your documents.
2.  Split them into small, relevant chunks using one of the LangChain text splitter types.
3.  Create numerical representations (embeddings) of these chunks.
4.  Store these embeddings in a vector store.
5.  When a user asks a question, you find the most similar chunks in your vector store.
6.  You then give these chunks to the LLM along with the user's question, so it can generate an informed answer.

Effective text splitting directly leads to better retrieval and therefore better answers from your RAG system.

#### Handling Large-Scale Data

When dealing with many documents, say thousands of articles, you might need to process them in batches. Ensure your splitting process is efficient. Parallel processing can help speed things up if you have many documents to split.

### Advanced Scenarios with Text Splitters

Sometimes, a single splitter isn't enough. You might encounter documents that blend different formats or require very specific handling.

#### Combining Splitters

You can chain different LangChain text splitter types together. For example, you might use an `HTMLTextSplitter` to extract clean text from a web page, and then pass that cleaned text to a `RecursiveCharacterTextSplitter` for a more granular chunking. This allows you to tackle complex document processing pipelines.

```python
from langchain.text_splitter import HTMLTextSplitter, RecursiveCharacterTextSplitter

# First, split HTML and clean it up
html_splitter_stage_1 = HTMLTextSplitter()
html_chunks = html_splitter_stage_1.create_documents([html_content]) # Use the html_content from earlier example

# Now, take the page_content of these initial chunks and split them further
all_final_chunks = []
recursive_splitter_stage_2 = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", ""], # More aggressive splitting
    chunk_size=50,
    chunk_overlap=10,
)

for doc in html_chunks:
    smaller_chunks = recursive_splitter_stage_2.create_documents([doc.page_content])
    all_final_chunks.extend(smaller_chunks)

print(f"Total final chunks after two stages: {len(all_final_chunks)}")
# for i, chunk in enumerate(all_final_chunks):
#     print(f"--- Final Chunk {i+1} ---")
#     print(chunk.page_content)
```

This two-stage approach gives you fine-grained control over how your text is processed, allowing you to first handle the overall document structure and then refine the chunks for specific content types.

#### Custom Text Splitters

If none of the existing LangChain text splitter types meet your exact needs, you can create your own custom splitter. This involves inheriting from the `TextSplitter` base class and implementing your own `split_text` method. This gives you complete freedom to define how text is broken down, based on your unique data format or business rules.

For example, you might have a very specific file format for scientific papers, where each section is marked by a unique identifier. A custom splitter could be tailored to recognize these identifiers and split accordingly. This level of customization is a powerful feature of LangChain.

### Conclusion

Understanding and effectively using LangChain text splitter types is a fundamental skill for anyone building applications with large language models. Whether you're working with simple text files, complex Markdown documents, or messy HTML pages, there's a splitter designed to help you prepare your data perfectly. These tools are vital for ensuring that your LLMs receive manageable, context-rich information, leading to better performance and more reliable AI applications.

Remember to experiment with `chunk_size`, `chunk_overlap`, and different `separators` to find the sweet spot for your specific use case. By mastering text splitting, you unlock the full potential of your LLM-powered projects. Happy splitting!